"""
Copyright 2024 Logan Kirkland

This file is part of term-assist.

term-assist is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

term-assist is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with
term-assist. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from warnings import warn

from yaml import safe_load

from term_assist.test.base import (
    project_dir,
    run_cmd,
    test_data_dir,
    read_std_and_rewrite,
    data_dir,
)

logger = logging.getLogger(__name__)


class TestInstall:
    def test_build(self):
        run_cmd(f"cd {str(project_dir)}; python -m build", raise_on_failure=True)

    def test_install(self):
        run_cmd(
            f"pipx install {str(next(project_dir.joinpath("dist").glob("*.whl")))}",
            raise_on_failure=True,
        )


class TestCLI:
    def test_help(self, capfd):
        with open(test_data_dir / "help.txt", "r") as f:
            help_text = _remove_newline_and_space(f.read())

        run_cmd(f"ta -h", raise_on_failure=True)
        self._verify_cmd_output(capfd, help_text)

        run_cmd(f"ta --help", raise_on_failure=True)
        self._verify_cmd_output(capfd, help_text)

        run_cmd(f"ta", raise_on_failure=True)
        self._verify_cmd_output(capfd, help_text)

    @staticmethod
    def _verify_cmd_output(capfd, expected: str) -> None:
        out, _ = read_std_and_rewrite(capfd)
        out = _remove_newline_and_space(out)
        assert out == expected

    def test_basic_prompt(self, capfd):
        with open(test_data_dir / "help.txt", "r") as f:
            help_text = f.read()

        run_cmd(f"ta unzip a tgz archive", raise_on_failure=True)
        out, _ = read_std_and_rewrite(capfd)
        assert out != ""
        assert out != help_text


class TestModels:
    def test_models_short(self, capfd):
        with open(data_dir / "models.yaml", "r") as f:
            models = safe_load(f)

        model_strings = []
        for brand, models_dict in models.items():
            for model in models_dict.keys():
                model_strings.append(f"{brand}:{model}")

        responses = []
        for model in model_strings:
            logger.info(f"Testing model '{model}'")
            run_cmd(f"ta --model {model} unzip a tgz archive", raise_on_failure=True)
            out, _ = read_std_and_rewrite(capfd)
            responses.append(out)
            logger.info(f"Response: '{out}'")

            # Verify the response is not empty
            assert out != ""

        # Verify that not all strings are exactly the same (would likely indicate the
        # --model arg is not working)
        if len(set(responses)) <= 1:
            warn(
                "All responses are exactly the same. Verify that the `--model` arg is "
                "working properly."
            )


def _remove_newline_and_space(string: str) -> str:
    return string.replace("\n", "").replace(" ", "")
