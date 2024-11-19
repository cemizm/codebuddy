import unittest
from pycodebuddy.base_client import BaseClient
from pycodebuddy.config_loader import Configuration


class BaseClientTest(BaseClient):
    def get_completion(self, user_request, file_list, file_contents, command_result):
        return {'action': 'response', 'message': 'Test'}


class TestBaseClient(unittest.TestCase):

    def setUp(self):
        config = Configuration(instructions="Some instructions")
        self.client = BaseClientTest(config)

    def test_initialization(self):
        self.assertEqual(self.client._get_user_instructions(),
                         "Some instructions")
        self.assertEqual(self.client.config.history_size, 10)
        self.assertEqual(self.client.history, [])

    def test_append_history(self):
        message = "New event"
        self.client._append_history(message)
        self.assertIn(message, self.client.history)

        # Fill history to exceed history size
        for i in range(11):
            self.client._append_history(f"event {i}")

        # Ensure it doesn't exceed history_size
        self.assertEqual(len(self.client.history), 10)
        self.assertNotIn("New event", self.client.history)

    def test_internal_instructions(self):
        # Accessing internal instructions to ensure it's set correctly but not used directly
        self.assertTrue(
            "Possible response actions include:" in self.client.internal_instructions)


if __name__ == '__main__':
    unittest.main()
