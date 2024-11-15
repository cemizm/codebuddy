import logging
import subprocess

class TransactionHandler:
    """
    A class to handle commit and rollback operations.

    Methods:
        commit: Executes a commit operation if there are any changes.
        rollback: Executes a rollback operation.
    """

    def __init__(self):
        logging.info("TransactionHandler initialized.")

    def commit(self, message):
        logging.info("Checking for changes before commit.")
        if not self._has_changes():
            logging.info("No changes detected, skipping commit.")
            return

        logging.info("Starting commit operation.")
        try:
            subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
            subprocess.run(['git', 'commit', '-m', f'{message}'], check=True, capture_output=True, text=True)
            logging.info("Commit successful.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Commit operation failed: {e.stderr}")
            raise RuntimeError("Commit failed") from e

    def rollback(self):
        logging.info("Starting rollback operation.")
        try:
            subprocess.run(["git", "reset", "--hard", "HEAD"], check=True, capture_output=True, text=True)
            subprocess.run(["git", "clean", "-fd"], check=True, capture_output=True, text=True)
            logging.info("Rollback successful.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Rollback operation failed: {e.stderr}")
            raise RuntimeError("Rollback failed") from e

    def _has_changes(self):
        """Check if there are any changes in the working directory."""
        try:
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to check for changes: {e.stderr}")
            raise RuntimeError("Failed to check for changes") from e
