from app.policy import validate_command
from app.security import scan_text
import pytest


def test_shell_chaining_is_blocked():
    with pytest.raises(PermissionError):
        validate_command(["python", "-c", "print(1);__import__('os').system('id')"])


def test_host_proc_path_is_blocked():
    with pytest.raises(PermissionError):
        validate_command(["cat", "/proc/1/environ"])


def test_secret_like_model_output_is_detected():
    assert "credential_assignment" in scan_text("token='abcdefghijklmnopqrstuvwxyz1234'")
