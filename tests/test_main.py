import pytest
from unittest.mock import patch, MagicMock
from codebuddy.main import main, InteractiveShell

@patch('codebuddy.main.ConfigLoader')
@patch('codebuddy.main.InteractiveShell')
@patch('codebuddy.main.sys')
def test_main_with_args(mock_sys, MockInteractiveShell, MockConfigLoader):
    mock_sys.argv = ['main.py', 'test query']
    mock_config = MockConfigLoader.return_value.load_configuration.return_value
    mock_shell = MockInteractiveShell.return_value

    main()

    MockConfigLoader.assert_called_once()
    MockInteractiveShell.assert_called_once_with(mock_config)
    mock_shell.process_query.assert_called_once_with("test query")

@patch('codebuddy.main.ConfigLoader')
@patch('codebuddy.main.InteractiveShell')
@patch('codebuddy.main.sys')
def test_main_no_args(mock_sys, MockInteractiveShell, MockConfigLoader):
    mock_sys.argv = ['main.py']
    mock_config = MockConfigLoader.return_value.load_configuration.return_value
    mock_shell = MockInteractiveShell.return_value

    main()

    MockConfigLoader.assert_called_once()
    MockInteractiveShell.assert_called_once_with(mock_config)
    mock_shell.run.assert_called_once()

@pytest.fixture
def interactive_shell():
    with patch('codebuddy.main.FileHandler'), \
         patch('codebuddy.main.TransactionHandler'), \
         patch('codebuddy.main.CodeBuddy'), \
         patch('codebuddy.main.CommandExecutor'):
        yield InteractiveShell(MagicMock())

@patch('builtins.input', side_effect=['exit'])
def test_interactive_shell_run_exit(mock_input, interactive_shell):
    with patch('builtins.print') as mock_print:
        interactive_shell.run()
        mock_print.assert_any_call("Entering interactive shell. Type 'exit' to exit or use Ctrl+C to abort.")

@patch('builtins.input', side_effect=['rollback', 'exit'])
def test_interactive_shell_run_rollback(mock_input, interactive_shell):
    with patch.object(interactive_shell.transaction_handler, 'rollback') as mock_rollback:
        interactive_shell.run()
        mock_rollback.assert_called_once()

@patch('builtins.input', side_effect=['test query', 'exit'])
def test_interactive_shell_process_query(mock_input, interactive_shell):
    with patch.object(interactive_shell, 'process_query') as mock_process_query:
        interactive_shell.run()
        mock_process_query.assert_called_once_with('test query')
