import sys
import signal
from codebuddy.command_executor import CommandExecutor
from codebuddy.config_loader import ConfigLoader, Configuration
from codebuddy.codebuddy import CodeBuddy
from codebuddy.file_handler import FileHandler
from codebuddy.transaction_handler import TransactionHandler


class InteractiveShell:
    """
    An interactive shell for user interaction with Git-based rollback support.
    """

    def __init__(self, config: Configuration):
        self.file_handler = FileHandler()
        self.buddy = CodeBuddy(config)
        self.transaction_handler = TransactionHandler()
        self.command_executor = CommandExecutor(config.allow_command_execution)
        self.initial_commit_made = False
        self.file_contents = {}  # Added to store file contents

    def signal_handler(self, sig, frame):
        print("\nExiting shell due to Ctrl+C...")
        sys.exit(0)

    def run(self) -> None:
        """
        Runs the interactive shell, processing input queries continuously.
        """
        print("Entering interactive shell. Type 'exit' to exit or use Ctrl+C to abort.")
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            query = input("User: ")
            if query.lower() == 'exit':
                print("Exiting shell...")
                break
            else:
                self.process_query(query)

    def process_query(self, query: str) -> None:
        """
        Processes a given query by interacting with the OpenAI API and performing file operations.

        Args:
            query (str): The user query to process.
        """
        if not self.initial_commit_made:
            self.transaction_handler.commit("Initial backup before changes")

        response_files = []
        cmd_result = None
        while True:
            requested_files = []
            command = None

            response = self.buddy.get_completion(query, self.file_handler.list_directory_files(), response_files, cmd_result)

            for change in response:
                action = change.get('action')
                if action == 'response':
                    user_response = change.get('message', '')
                    if user_response:
                        print("\033[92m" + "Assistant: " + user_response + "\033[0m")
                elif action == 'modify' or action == 'delete':
                    self.file_handler.apply_changes_to_project([change])
                    self.transaction_handler.commit(f"Applied changes for query: {query}")
                elif action == 'command':
                    command = change.get('command', '')
                    if command:
                        print("\033[91m" + f"Running: '{command}'..." + "\033[0m")
                        cmd_result = self.command_executor.run(command)
                elif action == 'request_files':
                    filenames = change.get('filename')
                    if type(filenames) is not list:
                        filenames = [filenames]
                    for filename in filenames:
                        print(f"Reading {filename}...")
                        requested_files.append(filename)

            if not requested_files and not command:
                break

            response_files = []
            for filename in requested_files:
                response_files.append({'name': filename, 'content': self.file_handler.get_content(filename)})

def main():
    config_loader = ConfigLoader()
    config = config_loader.load_configuration()
    shell = InteractiveShell(config)

    if len(sys.argv) >= 2:
        query = " ".join(sys.argv[1:])
        shell.process_query(query)
    else:
        shell.run()

if __name__ == "__main__":
    main()