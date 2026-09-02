from __future__ import annotations

import re
from pathlib import Path

SECRET_PATTERNS = [
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("credential_assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9_./+=:-]{12,}")),
    ("github_token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}


def scan_text(text: str) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS if pattern.search(text)]


def scan_workspace(root: Path, max_bytes: int = 2_000_000) -> dict[str, list[str]]:
    findings: dict[str, list[str]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRS for part in path.parts):
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
            hits = scan_text(path.read_text(errors="ignore"))
        except OSError:
            continue
        if hits:
            findings[str(path.relative_to(root))] = hits
    return findings
