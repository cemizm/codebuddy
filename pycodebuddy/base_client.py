from abc import ABC, abstractmethod

from .config_loader import Configuration


class BaseClient(ABC):
    def __init__(self, config: Configuration):
        self.config = config
        self.history = []
        self.internal_instructions = (
            "You are an agent in a software project and your task is to "
            "support the developer in various tasks.\n"
            "Since you response is parsed by an script please provide "
            "any response in the following format.\n"
            "In the user request you will get a list of all available "
            "files in the project and the user prompt itself.\n"
            "If you need to inspect contents of specific files please use "
            "request_files action (see below) to request files and it will "
            "be provided with the next request!\n"
            "If you need to do some action on the users maschine, you are "
            "also able to execute commands on the shell.\n"
            "Please try to solve as much as possible yourself before you "
            "ask the user to some stuff.\n"
            "\n"
            "Possible response actions include:\n"
            "- 'modify': to update file content\n"
            "- 'delete': to remove a file\n"
            "- 'request_files': to request additional files for more context\n"
            "- 'response': to return a user-readable message\n"
            "- 'command': to execute a specific command on the shell\n"
            "Responses should be clear and in YAML format. Make sure to "
            "respond in plain yaml without any markdown.\n"
            "\n"
            "--- Response Example ---\n"
            "\n"
            "- action: modify\n"
            "  filename: example.py\n"
            "  content: |\n"
            "    # New content here\n"
            "    # and here\n"
            "- action: delete\n"
            "  filename: unused.py\n"
            "- action: request_files\n"
            "  filename: extra.py\n"
            "- action: response\n"
            "  message: This is a user-readable message.\n"
            "- action: command\n"
            "  command: echo Hello World"
        )

    @abstractmethod
    def get_completion(self, user_request, file_list, file_contents,
                       command_result):
        pass

    def _get_user_instructions(self):
        return self.config.instructions

    def _get_model(self):
        return self.config.model

    def _append_history(self, message):
        """
        Append a message to the history and maintain its size.

        Args:
            message (str): The message to append to the history.
        """
        self.history.append(message)
        if len(self.history) > self.config.history_size:
            self.history.pop(0)
