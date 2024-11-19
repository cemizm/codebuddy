import subprocess
import logging


class CommandExecutor:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def run(self, command: str) -> str:
        """
        Execute a system command.

        Args:
            command (str): The command to execute.

        Returns:
            str: The combined stdout and stderr from the command execution.

        Note:
            This method will return both stdout and stderr output,
            regardless of the command success.
        """

        if not self.enabled:
            return "Command execution is not allowed"

        logging.info(f"Executing command: {command}")
        result = subprocess.run(
            command, shell=True, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        return result.stdout + result.stderr


if __name__ == "__main__":
    executor = CommandExecutor()
    print(executor.run('echo "Test run"'))
