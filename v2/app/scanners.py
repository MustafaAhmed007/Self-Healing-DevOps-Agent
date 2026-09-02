from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from .models import GateResult


class Scanner:
    name = "scanner"
    binary = ""
    args: tuple[str, ...] = ()

    def run(self, workspace: Path) -> GateResult:
        if not self.binary or not shutil.which(self.binary):
            return GateResult(name=self.name, passed=True, required=False, findings=[f"{self.binary or self.name} not installed"])
        try:
            p = subprocess.run([self.binary, *self.args], cwd=workspace, capture_output=True, text=True, timeout=180)
            output = (p.stdout + "\n" + p.stderr)[-20000:]
            return GateResult(name=self.name, passed=p.returncode == 0, findings=[] if p.returncode == 0 else [output])
        except subprocess.TimeoutExpired:
            return GateResult(name=self.name, passed=False, findings=["scanner timed out"])


class GitleaksScanner(Scanner):
    name = "gitleaks"
    binary = "gitleaks"
    args = ("detect", "--no-banner", "--redact", "--exit-code", "1")


class SemgrepScanner(Scanner):
    name = "semgrep"
    binary = "semgrep"
    args = ("scan", "--config", "auto", "--error")


class TrivyScanner(Scanner):
    name = "trivy"
    binary = "trivy"
    args = ("fs", "--scanners", "vuln,secret", "--exit-code", "1", ".")


def run_security_suite(workspace: Path) -> list[GateResult]:
    return [scanner.run(workspace) for scanner in (GitleaksScanner(), SemgrepScanner(), TrivyScanner())]
