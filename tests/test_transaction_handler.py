import pytest
from unittest.mock import patch, MagicMock
from codebuddy.transaction_handler import TransactionHandler
import subprocess
import os

@pytest.fixture
def handler():
    return TransactionHandler()

@patch('codebuddy.transaction_handler.subprocess.run')
@patch('codebuddy.transaction_handler.TransactionHandler._has_changes', return_value=True)
def test_commit_success(mock_has_changes, mock_run, handler):
    handler.commit("Test commit")
    mock_has_changes.assert_called_once()
    mock_run.assert_any_call(["git", "add", "."], check=True, capture_output=True, text=True)
    mock_run.assert_any_call(['git', 'commit', '-m', 'Test commit'], check=True, capture_output=True, text=True)

@patch('codebuddy.transaction_handler.subprocess.run')
@patch('codebuddy.transaction_handler.TransactionHandler._has_changes', return_value=False)
def test_commit_no_changes(mock_has_changes, mock_run, handler):
    handler.commit("Test commit")
    mock_has_changes.assert_called_once()
    mock_run.assert_not_called()

@patch('codebuddy.transaction_handler.subprocess.run')
@patch('codebuddy.transaction_handler.TransactionHandler._has_changes', return_value=True)
def test_commit_failure(mock_has_changes, mock_run, handler):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'git commit', "Error")
    with pytest.raises(RuntimeError, match="Commit failed"):
        handler.commit("Test commit")

@patch('codebuddy.transaction_handler.subprocess.run')
def test_rollback_success(mock_run, handler):
    handler.rollback()
    mock_run.assert_any_call(["git", "reset", "--hard", "HEAD"], check=True, capture_output=True, text=True)
    mock_run.assert_any_call(["git", "clean", "-fd"], check=True, capture_output=True, text=True)

@patch('codebuddy.transaction_handler.subprocess.run')
def test_rollback_failure(mock_run, handler):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'git reset', "Error")
    with pytest.raises(RuntimeError, match="Rollback failed"):
        handler.rollback()

@patch('codebuddy.transaction_handler.subprocess.run')
def test_has_changes_true(mock_run, handler):
    mock_run.return_value.stdout = " M codebuddy/file_handler.py"
    assert handler._has_changes() is True

@patch('codebuddy.transaction_handler.subprocess.run')
def test_has_changes_false(mock_run, handler):
    mock_run.return_value.stdout = ""
    assert handler._has_changes() is False

@patch('codebuddy.transaction_handler.subprocess.run')
def test_has_changes_failure(mock_run, handler):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'git status', "Error")
    with pytest.raises(RuntimeError, match="Failed to check for changes"):
        handler._has_changes()

@patch('codebuddy.transaction_handler.subprocess.run')
def test_initialize_git_repo_when_missing(mock_run):
    """Test if Git repo is initialized when it's missing."""
    with patch('os.path.isdir', return_value=False):
        TransactionHandler()
        mock_run.assert_called_with(["git", "init"], check=True, capture_output=True, text=True)
  
@patch('codebuddy.transaction_handler.subprocess.run')
def test_initialize_git_repo_when_present(mock_run):
    """Test if Git repo is not initialized again if present."""
    with patch('os.path.isdir', return_value=True):
        TransactionHandler()
        mock_run.assert_not_called()
