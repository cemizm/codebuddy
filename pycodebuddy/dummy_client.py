from pycodebuddy.config_loader import Configuration
from .base_client import BaseClient


class DummyClient(BaseClient):
    def __init__(self, config: Configuration):
        super().__init__(config)

    def get_completion(
        self, user_request, file_list, file_contents, command_result
    ):
        return [
            {"action": "response",
             "message": "This is a dummy client response."}
        ]
