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

import argparse
import os
import platform
from argparse import ArgumentParser, Namespace
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path
from shutil import copy
from stat import S_IREAD, S_IXUSR
from subprocess import run

import keyboard
import pyperclip
from yaml import safe_load

from term_assist.models.anthropic_model import AnthropicModel
from term_assist.models.openai_model import OpenAIModel

user_config_dir = Path.home() / ".config" / "term-assist"
user_config_file = user_config_dir / "config.yaml"

# files() gets a MultiplexedPath here even though there is only one data dir. As a
# workaround, we need to access the protected attribute `_paths`.
data_dir = files("term_assist.data")._paths[0]  # noqa

config_default_file = data_dir.joinpath("config_default.yaml")
models_file = data_dir.joinpath("models.yaml")


def main():
    parser, args = _parse_args()
    _initialize_config()

    if args.version:
        print("term-assist version", version("term-assist"))
        exit(0)
    if not args.prompt:
        parser.print_help()
        exit(0)

    config, models = _load_config()
    system, shell = _load_environment()

    # If the `model` arg is passed, prefer that over the config file
    if args.model:
        config["ai"]["model"] = args.model[0]

    try:
        brand, brand_model = config["ai"]["model"].split(":")
        config["ai"]["model"] = brand_model
    except ValueError as e:
        if len(config["ai"]["model"].split(":")) < 2:
            raise ValueError(
                f"Cannot parse model string '{config["ai"]["model"]}'. Check configuration "
                f"file and ensure model brand and model type are separated by ':'."
            ) from e
        else:
            raise ValueError(
                f"Cannot parse model string '{config["ai"]["model"]}'. Check configuration "
                f"file."
            ) from e

    if not config["debug"]["no_ai"]:
        if brand == "openai":
            model = OpenAIModel(config, models, system, shell)
        elif brand == "anthropic":
            model = AnthropicModel(config, models, system, shell)
        else:
            raise ValueError(f"Unknown brand '{brand}'. Check configuration file.")

        response = model.message(prompt=" ".join(args.prompt))
    else:
        response = "echo Hello world!"

    print_response = True
    if config["behavior"]["auto_copy"]:
        pyperclip.copy(response)

        os_ = platform.system()
        if config["behavior"]["auto_paste"]:
            if os_ == "Darwin":
                keyboard.send(55, do_press=True, do_release=False)
                keyboard.send(9, do_press=True, do_release=True)
                keyboard.send(55, do_press=False, do_release=True)
            elif os_ in ["Linux", "Windows"]:
                keyboard.send("ctrl+v")
            else:
                raise RuntimeError(
                    f"Your operating system ({os_}) does not support auto_paste. "
                    f"Please disable it in your configuration file."
                )
            print_response = False

    if print_response:
        print(response)


def _parse_args() -> tuple[ArgumentParser, Namespace]:
    """Parses any command line arguments."""
    arg_parser = argparse.ArgumentParser(
        prog="ta",
        description="term-assist: an AI assistant for your terminal.",
    )
    arg_parser.add_argument(
        "prompt",
        nargs="*",
        type=str,
        help="prompt for the AI model",
    )
    arg_parser.add_argument(
        "--version", action="store_true", help="display the program version"
    )
    arg_parser.add_argument(
        "--model",
        "-m",
        action="store",
        nargs=1,
        type=str,
        help="specify a model to use in the format BRAND:MODEL (overrides the setting "
        "in your config file)",
    )
    return arg_parser, arg_parser.parse_args()


def _initialize_config():
    new_config = False

    # Create our config directory if it does not exist
    if not user_config_dir.exists():
        new_config = True
        user_config_dir.mkdir(parents=True, exist_ok=True)

        # Since this is a new config, let's set file permissions too
        for file in data_dir.iterdir():
            os.chmod(file, S_IREAD)
        os.chmod(data_dir, S_IREAD | S_IXUSR)

    # Symlink data folder for easier user access
    if new_config or not user_config_dir.joinpath("data").exists(follow_symlinks=False):
        os.symlink(data_dir, user_config_dir / "data", target_is_directory=True)

    # Copy default config if user config does not exist
    if new_config or not user_config_file.exists():
        copy(src=config_default_file, dst=user_config_file)


def _load_config():
    with open(user_config_file, "r") as f:
        config = safe_load(f)
    with open(models_file, "r") as f:
        models = safe_load(f)

    return config, models


def _load_environment():
    system = f"{platform.system()} {platform.release()}"
    shell = (
        run(f"{os.environ.get("SHELL")} --version", shell=True, capture_output=True)
        .stdout.decode()
        .strip("\n")
    )
    return system, shell


if __name__ == "__main__":
    main()
