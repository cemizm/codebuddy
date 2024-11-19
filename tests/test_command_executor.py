import pytest
from unittest.mock import patch, MagicMock
from pycodebuddy.command_executor import CommandExecutor


@patch('pycodebuddy.command_executor.subprocess.run')
def test_run_command_failure(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_result.stderr = "Error occurred"
    mock_result.returncode = 1
    mock_run.return_value = mock_result

    executor = CommandExecutor(enabled=True)
    command = 'exit 1'  # Simulating a failing command
    result = executor.run(command)

    assert result.strip() == "Error occurred"  # Update to reflect actual result
