from __future__ import annotations

from pathlib import Path
from .models import Verification, CommandResult
from .sandbox import LocalSandbox


class Verifier:
    def __init__(self, sandbox=None):
        self.sandbox = sandbox or LocalSandbox()

    def run(self, workspace: Path, commands: list[list[str]], regression: list[list[str]] | None = None) -> Verification:
        results: list[CommandResult] = []
        checks: dict[str, bool] = {}
        for i, command in enumerate(commands):
            result = self.sandbox.run(workspace, command, timeout=120)
            results.append(result)
            checks[f"verification_{i}"] = result.exit_code == 0 and not result.timed_out
            if not checks[f"verification_{i}"]:
                return Verification(passed=False, checks=checks, results=results, regression_passed=False)
        regression_commands = regression or []
        regression_passed = True
        for i, command in enumerate(regression_commands):
            result = self.sandbox.run(workspace, command, timeout=120)
            results.append(result)
            checks[f"regression_{i}"] = result.exit_code == 0 and not result.timed_out
            regression_passed = regression_passed and checks[f"regression_{i}"]
        return Verification(passed=all(checks.values()) if checks else True, checks=checks, results=results, regression_passed=regression_passed)
