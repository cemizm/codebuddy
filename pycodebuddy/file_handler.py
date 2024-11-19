import os
from typing import List, Dict
from pathlib import Path
from gitignore_parser import parse_gitignore


class FileHandler:
    """
    A handler for performing file operations within a project.
    """

    def apply_changes_to_project(self, changes: List[Dict]) -> None:
        """
        Applies changes to the project files based on the specified actions.

        Args:
            changes (List[Dict]): A list of dictionaries specifying the
                                  changes, each containing 'filename',
                                  'action', and optionally 'content' keys.
        """
        for change in changes:
            filename = change['filename']
            action = change['action']
            if action == 'delete':
                if os.path.exists(filename):
                    os.remove(filename)
                    print("\033[93m" + f"Deleted {filename}")
            elif action == 'modify':
                content = change['content']
                # Ensure the directory exists
                base_path = os.path.dirname(filename)
                if base_path:
                    os.makedirs(base_path, exist_ok=True)
                with open(filename, 'w') as file:
                    file.write(content)
                print("\033[93m" + f"Modified {filename}" + "\033[0m")

    def list_directory_files(self, directory: str = '.') -> List[str]:
        """
        Lists all files in a specified directory excluding those matching
        .gitignore patterns.

        Args:
            directory (str): The directory to list files from. Defaults to
            the current directory.

        Returns:
            List[str]: A list of relative file paths.
        """
        files_list = []
        gitignore_file = Path('.gitignore')
        is_ignored = (
            parse_gitignore(gitignore_file)
            if gitignore_file.exists()
            else lambda x: False
        )

        for root, _, found_files in os.walk(directory):
            for file in found_files:
                full_path = os.path.join(root, file)
                if ".git" not in full_path and not is_ignored(full_path):
                    files_list.append(os.path.relpath(full_path, '.'))
        return files_list

    def get_content(self, filename: str) -> str:
        """
        Retrieves the content of a specified file.

        Args:
            filename (str): The name of the file to read.

        Returns:
            str: The file's content, or a not found message if the file does
            not exist.
        """
        if not os.path.exists(filename):
            return (f"# File not found: {filename}\n")
        with open(filename, 'r') as file:
            content = file.read()
        return content

    def write_content(self, filename: str, content: str) -> None:
        """
        Writes content to a specified file.

        Args:
            filename (str): The name of the file to write.
            content (str): The content to write into the file.
        """
        base_path = os.path.dirname(filename)
        if base_path:
            os.makedirs(base_path, exist_ok=True)
        with open(filename, 'w') as file:
            file.write(content)
