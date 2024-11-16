import pytest
from unittest.mock import patch, MagicMock
from codebuddy.main import InteractiveShell
from codebuddy.config_loader import Configuration


@pytest.fixture
def mock_config():
    return Configuration(
        client_type="dummy_client"
    )


@pytest.fixture
def interactive_shell(mock_config):
    return InteractiveShell(mock_config)


@patch('codebuddy.main.input', create=True)
def test_run_exit(mock_input, interactive_shell):
    """Test that the shell exits properly when 'exit' is typed."""
    mock_input.side_effect = ['exit']
    interactive_shell.run()


@patch('codebuddy.main.input', create=True)
def test_run_process_query(mock_input, interactive_shell):
    """Test that a user query is processed correctly in the shell."""
    with patch.object(interactive_shell, 'process_query') as mock_process_query:
        mock_input.side_effect = ['my query', 'exit']
        interactive_shell.run()
        mock_process_query.assert_called_once_with('my query')


@patch('codebuddy.main.CodeBuddy.get_completion', return_value=[])
@patch('codebuddy.main.TransactionHandler.commit')
def test_process_query_initial_commit(mock_commit, mock_get_completion, interactive_shell):
    """Test that an initial commit is made before processing the first query."""
    interactive_shell.process_query("test query")
    mock_commit.assert_called_once_with("Initial backup before changes")


@patch('codebuddy.main.CodeBuddy.get_completion', side_effect=[
    [{'action': 'response', 'message': 'Hello'}],
    []
])
def test_process_query_response(mock_get_completion, interactive_shell):
    """Test that a response from CodeBuddy is printed correctly."""
    with patch('builtins.print') as mock_print:
        interactive_shell.process_query("test query")
        mock_print.assert_any_call("\033[92m" + "Assistant: Hello" + "\033[0m")


@patch('codebuddy.main.CodeBuddy.get_completion', return_value=[
    {'action': 'modify', 'filename': 'test.txt', 'content': 'New content'}
])
@patch('codebuddy.main.TransactionHandler.commit')
@patch('codebuddy.main.FileHandler.apply_changes_to_project')
def test_process_query_modify(mock_apply_changes, mock_commit, mock_get_completion, interactive_shell):
    """Test that a modify action results in file modification."""
    interactive_shell.process_query("test query")
    mock_apply_changes.assert_called_once()
    mock_commit.assert_called_with("Applied changes for query: test query")


@patch('codebuddy.main.CodeBuddy.get_completion', side_effect=[
    [{'action': 'command', 'command': 'echo Hello'}],
    []
])
@patch('codebuddy.main.CommandExecutor.run')
def test_process_query_command(mock_run_command, mock_get_completion, interactive_shell):
    """Test that a command action results in command execution."""
    interactive_shell.process_query("test query")
    mock_run_command.assert_called_once_with('echo Hello')


@patch('codebuddy.main.CodeBuddy.get_completion', side_effect=[
    [{'action': 'request_files', 'filename': 'test.txt'}],
    []
])
@patch('codebuddy.main.FileHandler.get_content', return_value='File content')
def test_process_query_request_files(mock_get_content, mock_get_completion, interactive_shell):
    """Test that a request_files action results in file content being retrieved."""
    with patch('builtins.print') as mock_print:
        interactive_shell.process_query("test query")
        mock_get_content.assert_called_once_with('test.txt')
        mock_print.assert_any_call("Reading test.txt...")
