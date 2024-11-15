import pytest
from unittest.mock import patch, mock_open, MagicMock
from codebuddy.file_handler import FileHandler
import os

@pytest.fixture
def file_handler():
    return FileHandler()

@patch('builtins.open', new_callable=mock_open, read_data="file content")
def test_get_content_exists(mock_file, file_handler):
    assert file_handler.get_content('test.txt') == "file content"
    mock_file.assert_called_once_with('test.txt', 'r')

@patch('builtins.open', new_callable=mock_open)
@patch('codebuddy.file_handler.os.path.exists', return_value=False)
def test_get_content_not_exists(mock_exists, mock_file, file_handler):
    assert "# File not found: test.txt\n" == file_handler.get_content('test.txt')
    mock_exists.assert_called_once_with('test.txt')
    mock_file.assert_not_called()

@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open)
@patch('codebuddy.file_handler.os.path.exists', return_value=True)
def test_apply_changes_to_project_modify(mock_exists, mock_file, mock_makedirs, file_handler):
    changes = [{'filename': 'dir/test.txt', 'action': 'modify', 'content': 'new content'}]
    file_handler.apply_changes_to_project(changes)
    mock_makedirs.assert_called_once_with('dir', exist_ok=True)
    mock_file().write.assert_called_once_with('new content')

@patch('codebuddy.file_handler.os.remove')
@patch('codebuddy.file_handler.os.path.exists', return_value=True)
def test_apply_changes_to_project_delete(mock_exists, mock_remove, file_handler):
    changes = [{'filename': 'test.txt', 'action': 'delete'}]
    file_handler.apply_changes_to_project(changes)
    mock_remove.assert_called_once_with('test.txt')

@patch('codebuddy.file_handler.os.walk')
@patch('codebuddy.file_handler.Path.exists', return_value=True)
@patch('codebuddy.file_handler.parse_gitignore')
def test_list_directory_files(mock_parse_gitignore, mock_path_exists, mock_walk, file_handler):
    gitignore_parser = MagicMock()
    
    # Correct mock implementation to ignore 'ignored.txt'
    gitignore_parser.side_effect = lambda x: x.endswith("ignored.txt")
    mock_parse_gitignore.return_value = gitignore_parser
    mock_walk.return_value = [
        ('./', ['subdir'], ['file1.txt', 'ignored.txt']),
        ('./subdir', [], ['file2.txt']),
    ]

    files = file_handler.list_directory_files()
    expected_files = ['file1.txt', 'subdir/file2.txt']
    assert files == expected_files, f"Expected {expected_files}, but got {files}"
