from .openai_client import OpenAIClient
from .dummy_client import DummyClient
from .config_loader import Configuration


class CodeBuddy:
    def __init__(self, config: Configuration):
        self.client = self.create_client(config.client_type, config)

    def create_client(self, client_type, config: Configuration):
        if client_type == "openai":
            return OpenAIClient(config)
        else:
            return DummyClient(config)

    def get_completion(self, user_request, file_list, file_contents,
                       command_result):
        return self.client.get_completion(
            user_request, file_list, file_contents, command_result
        )
