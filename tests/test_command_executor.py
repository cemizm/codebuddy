import pytest
import subprocess
from unittest.mock import patch, MagicMock
from codebuddy.command_executor import CommandExecutor

@patch('codebuddy.command_executor.subprocess.run')
def test_run_command_success(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "Hello, World!"
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    executor = CommandExecutor()
    command = 'echo "Hello, World!"'
    result = executor.run(command)

    mock_run.assert_called_with(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.strip() == "Hello, World!"

@patch('codebuddy.command_executor.subprocess.run')
def test_run_command_failure(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_result.stderr = "command not found"
    mock_result.returncode = 1
    mock_run.return_value = mock_result

    executor = CommandExecutor()
    command = 'some_non_existent_command'
    result = executor.run(command)

    mock_run.assert_called_with(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result == "Command execution failed: command not found"

def test_command_execution_disabled():
    executor = CommandExecutor(enabled=False)
    command = 'echo "Hello, World!"'
    result = executor.run(command)
    assert result == "Command execution is not allowed"

def test_command_executor_initialization():
    executor_with_default = CommandExecutor()
    executor_with_disabled = CommandExecutor(enabled=False)

    assert executor_with_default.enabled is True
    assert executor_with_disabled.enabled is False

@patch('codebuddy.command_executor.subprocess.run')
def test_run_empty_command(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    executor = CommandExecutor()
    command = ''
    result = executor.run(command)

    mock_run.assert_called_with(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.strip() == ""

@patch('codebuddy.command_executor.subprocess.run')
def test_run_command_with_output(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "some output"
    mock_result.stderr = ""
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    executor = CommandExecutor()
    command = 'echo "some output"'
    result = executor.run(command)

    mock_run.assert_called_with(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.strip() == "some output"
