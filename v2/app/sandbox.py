from __future__ import annotations
import subprocess, time
from pathlib import Path
from .models import CommandResult
from .policy import validate_command

class LocalSandbox:
    """Development executor. Production mode must use DockerSandbox."""
    def run(self, workspace: Path, argv: list[str], timeout: int = 60) -> CommandResult:
        validate_command(argv)
        started=time.monotonic()
        try:
            p=subprocess.run(argv, cwd=workspace, capture_output=True, text=True, timeout=timeout, env={"PATH":"/usr/local/bin:/usr/bin:/bin"})
            return CommandResult(command=argv, exit_code=p.returncode, stdout=p.stdout[-20000:], stderr=p.stderr[-20000:], duration_ms=int((time.monotonic()-started)*1000))
        except subprocess.TimeoutExpired as e:
            return CommandResult(command=argv, exit_code=124, stdout=str(e.stdout or ""), stderr=str(e.stderr or ""), duration_ms=int((time.monotonic()-started)*1000), timed_out=True)

class DockerSandbox:
    """Runs commands in an ephemeral, non-root, network-disabled container."""
    def __init__(self, image="python:3.12-slim", cpus="1.0", memory="512m", pids=128):
        self.image=image; self.cpus=cpus; self.memory=memory; self.pids=pids

    def run(self, workspace: Path, argv: list[str], timeout: int=60) -> CommandResult:
        validate_command(argv)
        cmd=["docker","run","--rm","--network","none","--read-only","--cap-drop","ALL","--security-opt","no-new-privileges","--user","65532:65532","--cpus",self.cpus,"--memory",self.memory,"--pids-limit",str(self.pids),"--tmpfs","/tmp:rw,noexec,nosuid,size=64m","-v",f"{workspace}:/workspace:rw","-w","/workspace",self.image,*argv]
        return LocalSandbox().run(Path("/"),cmd,timeout)
