import os
import sys
import yaml
from typing import Any


class Configuration:
    """
    A class to hold configuration data.
    """

    def __init__(
        self,
        api_key: str = "api-key",
        instructions: str = "",
        allow_command_execution: bool = False,
        client_type: str = "openai",
        base_url: str = None,
        history_size: int = 10,
        model: str = "gpt-4o",
    ):
        self.api_key = api_key
        self.instructions = instructions
        self.allow_command_execution = allow_command_execution
        self.client_type = client_type
        self.base_url = base_url
        self.history_size = history_size
        self.model = model


class ConfigLoader:
    """
    A loader for application configuration from a YAML file.
    """

    def load_configuration(
        self, project_config_path: str = 'config.yaml'
    ) -> Any:
        """
        Loads the configuration for the application, first from the user's home
        directory and then overrides it with any configurations found in the
        project directory.

        Args:
            project_config_path (str): Path to the project configuration file.
                                       Defaults to 'config.yaml'.

        Returns:
            Configuration: An object containing the API key, any additional
            instructions, a boolean indicating if command execution is allowed,
            and the client type to be used.

        Raises:
            SystemExit: If the configuration file or API key is not found.
        """
        user_home_path = os.path.join(
            os.path.expanduser('~'), '.user_config.yaml'
        )

        user_config = self._load_yaml_config(user_home_path)
        project_config = self._load_yaml_config(project_config_path)

        final_config = {**user_config, **project_config}

        config = Configuration()

        config.api_key = final_config.get('api_key', config.api_key)
        config.instructions = final_config.get(
            'instructions', config.instructions)

        config.allow_command_execution = final_config.get(
            'allow_command_execution', config.allow_command_execution
        )
        config.client_type = final_config.get(
            'client_type', config.client_type)
        config.base_url = final_config.get('base_url', config.base_url)
        config.history_size = final_config.get(
            'history_size', config.history_size)
        config.model = final_config.get('model', config.model)

        return config

    @staticmethod
    def _load_yaml_config(config_path: str) -> dict:
        """
        Helper method to load a YAML configuration file.

        Args:
            config_path (str): Path to the YAML configuration file.

        Returns:
            dict: Dictionary containing configuration data.
        """
        if not os.path.exists(config_path):
            return {}

        with open(config_path, 'r') as config_file:
            return yaml.safe_load(config_file) or {}
