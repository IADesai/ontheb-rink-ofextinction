"""Test code for load.py"""
import pytest
from unittest.mock import MagicMock
from load import send_email

def test_ensure_email_task_is_string():
    """Test that checks that if a task is not a string, an exception is raised"""
    fake_config = MagicMock()
    with pytest.raises(Exception) as not_string:
        send_email(fake_config, 0, "msg")
    assert "Task should be a string" in str(not_string)


def test_ensure_email_message_is_string():
    """Test that checks that if a message is not a string, an exception is raised"""
    fake_config = MagicMock()
    with pytest.raises(Exception) as not_string:
        send_email(fake_config, "task", 0)
    assert "Message should be a string" in str(not_string)