import pytest
import yaml
from unittest.mock import patch
from pycodebuddy.config_loader import ConfigLoader, Configuration


@pytest.fixture
def config_loader():
    return ConfigLoader()


@pytest.fixture
def test_project_config_path(tmp_path):
    return tmp_path / "project_config.yaml"


class TestConfigLoader:
    def test_load_configuration(self, config_loader, test_project_config_path):
        with open(test_project_config_path, 'w') as file:
            yaml.safe_dump({"api_key": "test_key"}, file)

        config = config_loader.load_configuration(test_project_config_path)
        assert config.api_key == "test_key"

    def test_load_configuration_with_complete_data(self, config_loader, test_project_config_path):
        test_config = {
            "api_key": "test_key",
            "instructions": "Test instructions",
            "allow_command_execution": True,
            "client_type": "dummy"
        }
        with open(test_project_config_path, 'w') as file:
            yaml.safe_dump(test_config, file)

        config = config_loader.load_configuration(test_project_config_path)
        assert config.api_key == "test_key"
        assert config.instructions == "Test instructions"
        assert config.allow_command_execution is True
        assert config.client_type == "dummy"
