from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]
    required: bool = True


@dataclass(frozen=True)
class VerificationReport:
    passed: bool
    checks: dict[str, bool]
    output: dict[str, str]


DEFAULT_CHECKS = (
    Check("pytest", ("python", "-m", "pytest"), True),
)


def verify(root: Path, checks: tuple[Check, ...] = DEFAULT_CHECKS, timeout: int = 300) -> VerificationReport:
    results: dict[str, bool] = {}
    output: dict[str, str] = {}
    for check in checks:
        try:
            start = time.monotonic()
            p = subprocess.run(check.command, cwd=root, capture_output=True, text=True, timeout=timeout, check=False)
            results[check.name] = p.returncode == 0
            output[check.name] = f"duration={time.monotonic()-start:.2f}s\n{p.stdout}\n{p.stderr}"
        except (subprocess.TimeoutExpired, OSError) as exc:
            results[check.name] = False
            output[check.name] = repr(exc)
    passed = all(results.get(c.name, False) for c in checks if c.required)
    return VerificationReport(passed, results, output)
