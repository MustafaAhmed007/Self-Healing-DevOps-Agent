from pathlib import Path
from v2.app.security import scan_text, scan_workspace


def test_private_key_detected():
    assert "private_key" in scan_text("-----BEGIN PRIVATE KEY-----")


def test_github_token_detected():
    assert "github_token" in scan_text("ghp_" + "A" * 24)


def test_workspace_scan(tmp_path: Path):
    (tmp_path / "config.txt").write_text("password = 'this-is-a-long-secret-value'\n")
    assert "config.txt" in scan_workspace(tmp_path)
