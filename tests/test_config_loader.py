import unittest
import os
import yaml
from codebuddy.config_loader import ConfigLoader, Configuration

class TestConfigLoader(unittest.TestCase):

    def setUp(self):
        """
        Create a test configuration file for testing.
        """
        self.test_config_path = 'config_test.yaml'
        self.valid_config_data = {
            'api_key': 'test_key',
            'instructions': 'Some instructions',
            'allow_command_execution': True
        }
        with open(self.test_config_path, 'w') as file:
            yaml.safe_dump(self.valid_config_data, file)

    def tearDown(self):
        """
        Remove the test configuration file after testing.
        """
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def test_load_configuration_success(self):
        """
        Test loading of a valid configuration file.
        """
        loader = ConfigLoader()
        config = loader.load_configuration(self.test_config_path)

        self.assertIsInstance(config, Configuration)
        self.assertEqual(config.api_key, self.valid_config_data['api_key'])
        self.assertEqual(config.instructions, self.valid_config_data['instructions'])
        self.assertEqual(config.allow_command_execution, self.valid_config_data['allow_command_execution'])

    def test_load_configuration_file_not_found(self):
        """
        Test loading with a filename that doesn't exist, expecting SystemExit.
        """
        loader = ConfigLoader()
        with self.assertRaises(SystemExit):
            loader.load_configuration('non_existent_file.yaml')

    def test_load_configuration_no_api_key(self):
        """
        Test loading a configuration where the API key is missing, expecting SystemExit.
        """
        faulty_config_path = 'config_no_api_key.yaml'
        faulty_config_data = {
            'instructions': 'No API key here',
            'allow_command_execution': False
        }
        with open(faulty_config_path, 'w') as file:
            yaml.safe_dump(faulty_config_data, file)

        loader = ConfigLoader()
        with self.assertRaises(SystemExit):
            loader.load_configuration(faulty_config_path)

        os.remove(faulty_config_path)

    def test_load_configuration_default_values(self):
        """
        Test loading a configuration and ensure default values are set.
        """
        partial_config_path = 'config_partial.yaml'
        partial_config_data = {
            'api_key': 'partial_key'
        }
        with open(partial_config_path, 'w') as file:
            yaml.safe_dump(partial_config_data, file)

        loader = ConfigLoader()
        config = loader.load_configuration(partial_config_path)
        self.assertEqual(config.api_key, 'partial_key')
        self.assertEqual(config.instructions, '')
        self.assertFalse(config.allow_command_execution)

        os.remove(partial_config_path)

if __name__ == '__main__':
    unittest.main()
