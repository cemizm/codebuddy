import pytest
from unittest.mock import patch, mock_open
from pycodebuddy.file_handler import FileHandler


@pytest.fixture
def file_handler():
    return FileHandler()


@patch('builtins.open', new_callable=mock_open, read_data="file content")
def test_get_content_exists(mock_file, file_handler):
    # Since we're mocking 'open', we should ensure 'os.path.exists' returns True
    with patch('os.path.exists', return_value=True):
        assert file_handler.get_content('test.txt') == "file content"


@patch('os.path.exists', return_value=False)
def test_get_content_not_found(mock_exists, file_handler):
    # Ensure that when a file doesn't exist, it returns the not found message
    assert file_handler.get_content(
        'test.txt') == "# File not found: test.txt\n"


@patch('builtins.open', new_callable=mock_open)
def test_write_content(mock_file, file_handler):
    file_handler.write_content('test.txt', "New Content")
    mock_file.assert_called_once_with('test.txt', 'w')
    mock_file().write.assert_called_once_with("New Content")


@patch('builtins.open', side_effect=PermissionError)
def test_write_content_permission_error(mock_file, file_handler):
    with pytest.raises(PermissionError):
        file_handler.write_content('test.txt', "New Content")


@patch('os.remove')
@patch('os.path.exists', return_value=True)
def test_apply_changes_to_project_delete(mock_exists, mock_remove, file_handler):
    change = [{'filename': 'test.txt', 'action': 'delete'}]
    file_handler.apply_changes_to_project(change)
    mock_remove.assert_called_once_with('test.txt')


@patch('builtins.open', new_callable=mock_open)
@patch('os.path.exists', return_value=False)
@patch('os.makedirs')
def test_apply_changes_to_project_modify(mock_makedirs, mock_exists, mock_file, file_handler):
    change = [{'filename': 'test.txt',
               'action': 'modify', 'content': 'new content'}]
    file_handler.apply_changes_to_project(change)
    mock_file.assert_called_once_with('test.txt', 'w')
    mock_file().write.assert_called_once_with('new content')


@patch('os.walk', return_value=[('.', [], ['file1.txt', 'file2.txt'])])
@patch('gitignore_parser.parse_gitignore', return_value=lambda x: False)
def test_list_directory_files(mock_parse, mock_walk, file_handler):
    files = file_handler.list_directory_files()
    assert files == ['file1.txt', 'file2.txt']
