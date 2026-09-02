from __future__ import annotations
from pathlib import Path
from .models import Verification
from .sandbox import LocalSandbox

class Verifier:
    def __init__(self, sandbox=None): self.sandbox=sandbox or LocalSandbox()
    def run(self, workspace: Path, commands: list[list[str]]) -> Verification:
        results=[]; checks={}
        for i,cmd in enumerate(commands):
            r=self.sandbox.run(workspace,cmd,timeout=120); results.append(r); checks[f"check_{i}"]=r.exit_code==0
            if r.exit_code != 0: return Verification(passed=False,checks=checks,results=results)
        return Verification(passed=True,checks=checks,results=results)
