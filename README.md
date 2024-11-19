# Codebuddy

Codebuddy is an advanced command-line tool designed for executing user queries using OpenAI's GPT models within a Git-integrated shell environment. It provides intelligent automation of project file and configuration management, enabling efficient and dynamic interaction with projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive Shell**: Engage in an interactive shell environment with Git-based rollback capabilities to ensure safe modifications.
- **AI-Driven Query Processing**: Leverage OpenAI's GPT models to intelligently handle user queries and automate project management tasks.
- **Seamless File Management**: Facilitates project updates, file modifications, and configuration adjustments in response to user interactions.
- **Robust Command Execution**: Securely execute system commands as part of an integrated workflow.

## Installation

Codebuddy requires Python 3.8 or later. Install using Poetry with:

```bash
pip install pycodebuddy
```

## Usage

Enter the interactive shell ...

```bash
$ codebuddy
$ Entering interactive shell. Type 'exit' to exit or use Ctrl+C to abort.
$ User:
```

... or execute direct queries via:

```bash
codebuddy "<your request here>"
```

Ensure your OpenAI API key is configured in the config.yaml.

## Configuration

Codebuddy uses a configuration file for setting various parameters. This can be found at `.user_config.yaml` in the user's home directory, but it can be overridden by a `config.yaml` located in the project's root directory. Below are the configuration parameters:

- **api_key**: The API key for authentication (e.g., OpenAI). Default is 'api-key'.
- **instructions**: Additional instructions or notes used within to prepare the chat bot for his task.
- **allow_command_execution**: Boolean flag for allowing/disallowing command execution. Default is `False`.
- **client_type**: The type of client, like 'openai'. Default is 'openai'.
- **base_url**: Optional base URL for the openai backend to use. useful to run local models.
- **history_size**: Size of the history to maintain. Default is 10.
- **model**: The specified model to use, such as 'gpt-4o'.

Example `config.yaml` file:
```yaml
api_key: 'your-api-key-here'
instructions: 'additional setup instructions'
allow_command_execution: true
client_type: 'openai'
base_url: 'http://localhost:11434/v1' # to use ollama
history_size: 10
model: 'gpt-4o'
```

## Architecture

Codebuddy's architecture is modular and comprises the following components:
- `main.py`: The entry point for the interactive shell and query execution.
- `openai_client.py`: Manages API integration with OpenAI for query processing.
- `file_handler.py`: Oversees file operations, including file management.
- `command_executor.py`: Responsible for executing system commands securely.
- `config_loader.py`: Loads configuration parameters from the YAML files.
- `transaction_handler.py`: Utilizes Git for safe rollbacks and transaction management.

## Dependencies

Managed via Poetry and specified within `pyproject.toml`. Key dependencies include:
- openai
- PyYAML

## Development

Install additional development tools using:

```bash
poetry install --with dev
```

Use `black` for formatting, `flake8` for style checks, `mypy` for type checks, and `isort` for organizing imports.

## Contributing

Contributions are encouraged. Fork, implement improvements, and submit a pull request with test coverage for new features.

## License

Licensed under MIT License. See [LICENSE](LICENSE) for more information.
