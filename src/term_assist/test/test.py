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

from term_assist.test.base import project_dir, run_cmd, data_dir, read_std_and_rewrite


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
        with open(data_dir / "help.txt", "r") as f:
            help_text = f.read()

        run_cmd(f"ta -h", raise_on_failure=True)
        out, _ = read_std_and_rewrite(capfd)
        assert out == help_text

        run_cmd(f"ta --help", raise_on_failure=True)
        out, _ = read_std_and_rewrite(capfd)
        assert out == help_text

        run_cmd(f"ta", raise_on_failure=True)
        out, _ = read_std_and_rewrite(capfd)
        assert out == help_text
