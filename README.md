# Chat

This is a simple command line interface to [OpenAI's chat API](https://platform.openai.com/),
also powering ChatGPT.

## Installation

To install the `chat` tool, simply run

```
pip install .
```

This should install all dependencies and make the `chat` tool available. 
Note that we are currently requiring Python 3.10.
If this Python version is not supported by your operating system, you can install it via [asdf](https://asdf-vm.com/) or a similar tool.


## Usage
To use the bot, first get an OpenAI API key on their [website](https://platform.openai.com/) and set the `OPENAI_API_KEY` environment variable via
```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

You should now be able to start a chat session via (note that this might lead to some charges by OpenAI)
```bash
chat
```

You can also change the chat mode by specifying the `--with` or `-w` option (see below for details).
You can also change the temperature using the`-t` parameter.
The temperature should be a float between `0.0` and `2.0` with `0.0` more deterministic output and `2.0`
more random. The default is `1.0`.


## Modes
Currently we support the following modes out of the box:

* **assistant**: Default assistant mode
* **linux_terminal**: Emulates a LINUX terminal
* **translator**: Translates any language to English and suggests better formulations
* **interviewer**: Performs an interview for a tech role with you

These prompts were mostly adapted from the [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) project.

You can configure additional modes by creating a `.chat.yml` file in your home directory with the following syntax:
```yaml
modes:
  - name: <name of your agent>
    instruction: <description what the agent should do>
    conversation:
      - user: <previous input by user>
      - assistant: <previous input by assistant>
      - ...
  - ...
```
Both the `instruction` and `conversation` fields are optional.
You can add as many previous user prompts and responses as you like.


