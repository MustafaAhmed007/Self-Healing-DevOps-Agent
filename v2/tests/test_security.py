from pathlib import Path
from v2.app.security import scan_text, scan_workspace

def test_private_key_detected():
    assert scan_text('-----BEGIN PRIVATE KEY-----')

def test_workspace_scan(tmp_path: Path):
    (tmp_path/'x.txt').write_text('api_key=abcdefghijklmnopqrstuvwxyz')
    assert 'x.txt' in scan_workspace(tmp_path)
