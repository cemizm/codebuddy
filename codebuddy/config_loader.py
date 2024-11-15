import os
import sys
import yaml
from typing import Any

class Configuration:
    """
    A class to hold configuration data.
    """
    def __init__(self, api_key: str, instructions: str, allow_command_execution: bool):
        self.api_key = api_key
        self.instructions = instructions
        self.allow_command_execution = allow_command_execution

class ConfigLoader:
    """
    A loader for application configuration from a YAML file.
    """

    def load_configuration(self, config_path: str = 'config.yaml') -> Any:
        """
        Loads the configuration for the application from a YAML file.

        Args:
            config_path (str): Path to the configuration file. Defaults to 'config.yaml'.

        Returns:
            Configuration: An object containing the API key, any additional instructions,
                           and a boolean indicating if command execution is allowed.

        Raises:
            SystemExit: If the configuration file or API key is not found.
        """
        if not os.path.exists(config_path):
            print(f"Configuration file not found: {config_path}")
            sys.exit(1)

        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)

        api_key = config.get('api_key')
        instructions = config.get('instructions', '')
        allow_command_execution = config.get('allow_command_execution', False)

        if not api_key:
            print("API key not found in configuration file.")
            sys.exit(1)

        return Configuration(api_key, instructions, allow_command_execution)
