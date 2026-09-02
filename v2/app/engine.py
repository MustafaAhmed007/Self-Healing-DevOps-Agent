from __future__ import annotations
import tempfile
from pathlib import Path
from .models import Issue, RepairState, RunStatus
from .github import GitHubClient
from .sandbox import LocalSandbox
from .verify import Verifier
from .llm import LLM
from .policy import validate_patch

class RepairEngine:
    def __init__(self, github=None, sandbox=None, llm=None):
        self.github=github or GitHubClient(); self.sandbox=sandbox or LocalSandbox(); self.llm=llm
    def start(self, issue: Issue, reproduction_cmd: list[str]|None=None) -> RepairState:
        state=RepairState(issue=issue)
        with tempfile.TemporaryDirectory(prefix=f"shda-{state.run_id}-") as td:
            state.workspace=Path(td)
            state.status=RunStatus.REPRODUCING
            self.github.checkout(issue.repository,state.workspace/"repo")
            repo=state.workspace/"repo"
            cmd=reproduction_cmd or ["python","-m","pytest","-q"]
            state.reproduction=self._reproduce(repo,cmd)
            state.history.append({"stage":"reproduction","reproduced":state.reproduction.reproduced})
            if not state.reproduction.reproduced: state.status=RunStatus.FAILED; return state
            if not self.llm: state.status=RunStatus.FAILED; state.history.append({"stage":"diagnosis","error":"LLM not configured"}); return state
            state.status=RunStatus.DIAGNOSING
            evidence=state.reproduction.result.stderr + "\n" + state.reproduction.result.stdout
            state.diagnosis=self.llm.diagnose(issue.title+"\n"+issue.body,evidence)
            state.status=RunStatus.PATCHING
            files={"README.md":(repo/"README.md").read_text()[:12000]} if (repo/"README.md").exists() else {}
            state.patch=self.llm.propose(state.diagnosis,files)
            errors=validate_patch(state.patch,state.budget)
            if errors: state.status=RunStatus.FAILED; state.history.append({"stage":"policy","errors":errors}); return state
            for path,content in state.patch.files.items():
                target=repo/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content)
            state.status=RunStatus.VERIFYING
            state.verification=Verifier(self.sandbox).run(repo,[cmd,["python","-m","compileall","-q","."]])
            state.status=RunStatus.PASSED if state.verification.passed else RunStatus.FAILED
            return state
    def _reproduce(self,repo,cmd):
        r=self.sandbox.run(repo,cmd,timeout=120)
        from .models import Reproduction
        return Reproduction(reproduced=r.exit_code != 0,result=r,failure_signature=r.stderr[-1000:] if r.exit_code else None)
