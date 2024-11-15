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
            str: The stdout from the command execution.

        Raises:
            RuntimeError: If the command execution fails.
        """

        if not self.enabled:
            return "Command execution is not allowed"
        
        logging.info(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            return f"Command execution failed: {result.stderr}"

        return result.stdout
