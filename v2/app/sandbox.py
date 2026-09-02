from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from .models import CommandResult
from .policy import validate_command


class LocalSandbox:
    """Development executor. It is not a security boundary."""
    name = "local"

    def run(self, workspace: Path, argv: list[str], timeout: int = 60) -> CommandResult:
        validate_command(argv)
        started = time.monotonic()
        env = {"PATH": os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin"), "HOME": str(workspace)}
        try:
            proc = subprocess.run(argv, cwd=workspace, capture_output=True, text=True, timeout=timeout, env=env)
            return CommandResult(command=argv, exit_code=proc.returncode, stdout=proc.stdout[-20000:], stderr=proc.stderr[-20000:], duration_ms=int((time.monotonic()-started)*1000), sandbox=self.name)
        except subprocess.TimeoutExpired as exc:
            return CommandResult(command=argv, exit_code=124, stdout=str(exc.stdout or ""), stderr=str(exc.stderr or ""), duration_ms=int((time.monotonic()-started)*1000), timed_out=True, sandbox=self.name)


class DockerSandbox:
    """Ephemeral network-disabled container sandbox. Stronger isolation should use a microVM backend."""
    name = "docker"

    def __init__(self, image: str = "python:3.12-slim", cpus: str = "1.0", memory: str = "512m", pids: int = 128):
        self.image, self.cpus, self.memory, self.pids = image, cpus, memory, pids

    def run(self, workspace: Path, argv: list[str], timeout: int = 60) -> CommandResult:
        validate_command(argv)
        started = time.monotonic()
        cmd = ["docker", "run", "--rm", "--network=none", "--read-only", "--cap-drop=ALL", "--security-opt", "no-new-privileges", "--security-opt", "seccomp=builtin", "--user", "65532:65532", "--cpus", self.cpus, "--memory", self.memory, "--memory-swap", self.memory, "--pids-limit", str(self.pids), "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m", "-v", f"{workspace}:/workspace:rw", "-w", "/workspace", self.image, *argv]
        try:
            proc = subprocess.run(cmd, cwd=Path("/"), capture_output=True, text=True, timeout=timeout)
            return CommandResult(command=argv, exit_code=proc.returncode, stdout=proc.stdout[-20000:], stderr=proc.stderr[-20000:], duration_ms=int((time.monotonic()-started)*1000), sandbox=self.name)
        except subprocess.TimeoutExpired as exc:
            return CommandResult(command=argv, exit_code=124, stdout=str(exc.stdout or ""), stderr=str(exc.stderr or ""), duration_ms=int((time.monotonic()-started)*1000), timed_out=True, sandbox=self.name)
