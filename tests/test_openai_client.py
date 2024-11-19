import unittest
from pycodebuddy.config_loader import Configuration
from pycodebuddy.openai_client import OpenAIClient


class TestOpenAIClient(unittest.TestCase):

    def setUp(self):

        self.client = OpenAIClient(Configuration())

    # Example test, requires proper mocking of openai
    def test_get_completion_success(self):
        user_request = "Test request"
        file_list = []
        file_contents = []
        command_result = ""
        with unittest.mock.patch.object(self.client.client.chat.completions, "create") as mocked_create:
            mocked_create.return_value.choices[0].message.content = 'action: response\nmessage: "Test"'
            result = self.client.get_completion(
                user_request, file_list, file_contents, command_result)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
