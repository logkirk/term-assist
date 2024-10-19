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
from pathlib import Path
from subprocess import run
from sys import stdout, stderr

project_dir = Path(__file__).parents[3]
src_dir = Path(__file__).parents[2]
data_dir = Path(__file__).parents[1] / "data"
test_dir = Path(__file__).parent
test_data_dir = Path(__file__).parent / "data"

logger = logging.getLogger(__name__)


def run_cmd(cmd, shell=True, capture_output=False, text=True, raise_on_failure=False):
    result = run(cmd, shell=shell, capture_output=capture_output, text=text)
    if raise_on_failure:
        result.check_returncode()

    return result


def read_std_and_rewrite(capfd):
    out, err = capfd.readouterr()
    stdout.write(out)
    stderr.write(err)
    return out, err
