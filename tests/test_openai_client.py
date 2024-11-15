from unittest import TestCase
from unittest.mock import Mock, patch
from codebuddy.openai_client import CodeBuddy

class TestCodeBuddy(TestCase):
    def setUp(self) -> None:
        self.client = CodeBuddy(api_key='test', instructions='instructions')

    @patch('codebuddy.openai_client.openai.chat.completions.create')
    def test_get_completion(self, mock_create) -> None:
        # Mocking the response from the OpenAI API
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='- action: response\n  message: yaml_response'))]
        mock_create.return_value = mock_response

        # Call the method under test
        result = self.client.get_completion(
            "user_query",
            ['file1', 'file2'],
            [{'name': 'file3', 'content': 'file_content'}],
            "context"
        )

        # Assert that the result is a list and contains a dictionary with expected keys
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        self.assertIn('action', result[0])
        self.assertIn('message', result[0])
        self.assertEqual(result[0]['message'], 'yaml_response') 
