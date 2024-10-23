term-assist
===========

[project](https://sr.ht/~logankirkland/term-assist/) /
[repo](https://git.sr.ht/~logankirkland/term-assist) /
[mailing list](https://lists.sr.ht/~logankirkland/term-assist) /
[issues](https://todo.sr.ht/~logankirkland/term-assist)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![builds.sr.ht status](https://builds.sr.ht/~logankirkland/term-assist.svg)](https://builds.sr.ht/~logankirkland/term-assist?)

> ℹ️ **Note**  
> The canonical project locations are linked above. Other locations are
> mirrors.

An AI assistant for your terminal.

<img src="resources/tgz.png" width="300" alt="[screenshot: ta unzip a tgz archive]"/>
<img src="resources/vim.png" width="530" alt="[screenshot: ta how to exit vim]"/>

Features
--------

- **Works with Anthropic and OpenAI models**
- **Configurable parameters**: change models, system prompt,
  response length, and other parameters
- **Automatic environment detection**: automatically detects your system
  and shell environment for accurate responses
- **Automatic copy and paste**: optionally copies the generated response
  to the clipboard and pastes it in your terminal, ready to execute

Installation
------------

1. [Install `pipx`](https://pipx.pypa.io/stable/installation/)

2. Install `term-assist` using `pipx`:

   ```shell
   pipx install term-assist
   ```

3. In your terminal, configure your API keys depending on which model(s)
   you want to use.
    - [Anthropic instructions](https://docs.anthropic.com/en/docs/initial-setup#set-your-api-key)
    - [OpenAI instructions](https://platform.openai.com/docs/quickstart/create-and-export-an-api-key)

Usage
-----

```
usage: ta [-h] [--version] [--model MODEL] [--environment ENVIRONMENT]
          [prompt ...]

term-assist: an AI assistant for your terminal.

positional arguments:
  prompt                prompt for the AI model

options:
  -h, --help            show this help message and exit
  --version             display the program version
  --model MODEL, -m MODEL
                        specify a model to use in the format
                        BRAND:MODEL (overrides the setting in your
                        config file)
  --environment ENVIRONMENT, -e ENVIRONMENT
                        specify environment details (overrides
                        automatic environment detection)
```

### Examples

#### Basic prompt

```
> ta unzip a tgz archive
```

#### Override AI model configuration

```
> ta --model openai:gpt-4o follow a file as it updates
> ta -m ...
```

#### Override environment detection

```
> ta --environment "windows 95 dos" list com ports
> ta --environment bash list free drive space
> ta -e ...
```

Configuration
-------------

The configuration file is `~/.config/term-assist/config.json` and will
be created on first run and initialized with default configuration
parameters if it does not already exist.

See `~/.config/term-assist/config_default.json` for the default
configuration.

### AI configuration

#### model

The AI model to use.

This parameter should be set in the format `BRAND:MODEL`. For example,
to use OpenAI's GPT-4o model, set this parameter
to `openai:gpt-4o`.

See `~/.config/term-assist/models.json` for available models.

#### max_tokens

The maximum number of tokens that will be generated for output.

#### temperature

The amount of randomness injected into the response. Ranges from 0.0 to
1.0.

#### system_prompt

The system prompt that is given to the model.

Automatically collected information about your system environment will
be appended to the end of the string. This information can be overridden
using the `--environment/-e` command.

### Program behavior configuration

#### auto_copy

If true, automatically copy the AI's response to your clipboard.

#### auto_paste

If true (and if auto_copy is true), automatically paste the AI's
response so it is ready to execute.

Testing
-------

Module tests are located in the `src/term_assist/test/` directory.

1. [Install docker](https://docs.docker.com/engine/install/).
2. Run `run.sh`, which will build the docker image and initiate testing
   inside a container.
3. Results will be copied to an `src/term_assist/test/output` in both
   XML and plaintext log format.
