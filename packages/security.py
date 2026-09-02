from __future__ import annotations

from pathlib import Path
import re
import subprocess

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{12,}"),
]


def scan_text(text: str) -> list[str]:
    findings: list[str] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(pattern.pattern)
    return findings


def scan_workspace(root: Path) -> list[str]:
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            findings.extend(f"{path.relative_to(root)}: {x}" for x in scan_text(path.read_text(errors="ignore")))
        except OSError:
            continue
    return findings


def run_security_tool(command: list[str], cwd: Path, timeout: int = 60) -> tuple[int, str]:
    """Run an installed security scanner; callers should execute it inside a sandbox."""
    p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
    return p.returncode, p.stdout + p.stderr
