import logging
import subprocess
import os


class TransactionHandler:
    """
    A class to handle commit and rollback operations.

    Methods:
        commit: Executes a commit operation if there are any changes.
        rollback: Executes a rollback operation.
        _initialize_git_repo: Initializes a git repository if it does not exist.
    """

    def __init__(self):
        logging.info("TransactionHandler initialized.")
        self._initialize_git_repo()

    def commit(self, message):
        logging.info("Checking for changes before commit.")
        if not self._has_changes():
            logging.info("No changes detected, skipping commit.")
            return

        logging.info("Starting commit operation.")
        try:
            subprocess.run(
                ["git", "add", "."],
                check=True,
                capture_output=True,
                text=True
            )
            subprocess.run(
                ['git', 'commit', '-m', f'{message}'],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info("Commit successful.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Commit operation failed: {e.stderr}")
            raise RuntimeError("Commit failed") from e

    def rollback(self):
        logging.info("Starting rollback operation.")
        try:
            subprocess.run(
                ["git", "reset", "--hard", "HEAD"],
                check=True,
                capture_output=True,
                text=True
            )
            subprocess.run(
                ["git", "clean", "-fd"],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info("Rollback successful.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Rollback operation failed: {e.stderr}")
            raise RuntimeError("Rollback failed") from e

    def _has_changes(self):
        """Check if there are any changes in the working directory."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to check for changes: {e.stderr}")
            raise RuntimeError("Failed to check for changes") from e

    def _initialize_git_repo(self):
        """Initialize a git repository if it does not exist."""
        if not os.path.isdir('.git'):
            logging.info("No Git repository found. Initializing a new Git repository.")
            try:
                subprocess.run(
                    ["git", "init"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                logging.info("Initialized empty Git repository.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Initialization of Git repository failed: {e.stderr}")
                raise RuntimeError("Git initialization failed") from e
