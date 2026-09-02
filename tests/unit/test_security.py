from pathlib import Path

from packages.security import scan_text, scan_workspace


def test_private_key_detection():
    assert scan_text("-----BEGIN RSA PRIVATE KEY-----")[0]


def test_workspace_scanner(tmp_path: Path):
    (tmp_path / "app.py").write_text("token = 'abcdefghijklmnop'")
    findings = scan_workspace(tmp_path)
    assert findings
