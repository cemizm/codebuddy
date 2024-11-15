# Codebuddy

Codebuddy is an advanced command-line tool designed for executing user queries using OpenAI's GPT models within a Git-integrated shell environment. It provides intelligent automation of project file and configuration management, enabling efficient and dynamic interaction with projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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
poetry install
```

## Usage

Enter the interactive shell or execute direct queries via:

```bash
poetry shell
codebuddy "<your request here>"
```

Ensure your OpenAI API key is configured as an environment variable.

## Architecture

Codebuddy features a robust, modular architecture:
- `main.py`: Serves as the entry point for the interactive shell and direct query execution.
- `openai_client.py`: Manages integration with the OpenAI API to process user queries and generate actionable responses.
- `file_handler.py`: Handles dynamic file operations and manages project files.
- `command_executor.py`: Facilitates execution of system commands with necessary checks.
- `transaction_handler.py`: Provides Git-based transaction management to aid in safe rollbacks.

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