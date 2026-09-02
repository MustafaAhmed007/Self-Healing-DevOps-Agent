from __future__ import annotations

from dataclasses import dataclass
import subprocess
import tempfile
from pathlib import Path


@dataclass(frozen=True)
class SandboxConfig:
    image: str = "python:3.12-slim"
    cpus: float = 1.0
    memory: str = "1g"
    pids: int = 128
    timeout_seconds: int = 300
    network: bool = False
    read_only_root: bool = True


@dataclass(frozen=True)
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int


class Sandbox:
    """Docker sandbox contract. The control plane never executes repository code directly."""

    def __init__(self, config: SandboxConfig | None = None) -> None:
        self.config = config or SandboxConfig()

    def run(self, command: list[str], workspace: Path) -> CommandResult:
        if not command:
            raise ValueError("command cannot be empty")
        workspace = workspace.resolve()
        with tempfile.NamedTemporaryFile() as _:
            args = [
                "docker", "run", "--rm",
                "--cpus", str(self.config.cpus),
                "--memory", self.config.memory,
                "--pids-limit", str(self.config.pids),
                "--network", "none" if not self.config.network else "bridge",
                "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges:true",
                "--user", "65532:65532",
                "-v", f"{workspace}:/workspace:rw",
                "-w", "/workspace",
                self.config.image,
                *command,
            ]
            completed = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                check=False,
            )
        return CommandResult(completed.returncode, completed.stdout, completed.stderr, 0)
