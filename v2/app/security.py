from __future__ import annotations
import re
from pathlib import Path

SECRET_PATTERNS=[
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|secret|token|password)\\s*[:=]\\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
]

def scan_text(text: str) -> list[str]:
    return [f"pattern:{i}" for i,p in enumerate(SECRET_PATTERNS) if p.search(text)]

def scan_workspace(root: Path) -> dict[str,list[str]]:
    findings={}
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            try: hits=scan_text(p.read_text(errors="ignore"))
            except OSError: continue
            if hits: findings[str(p.relative_to(root))]=hits
    return findings
