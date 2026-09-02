from __future__ import annotations

import tempfile
import time
from pathlib import Path
from .audit import EvidenceLedger
from .config import Settings
from .diff import apply_proposal, unified_diff
from .github import GitHubClient
from .models import Issue, RepairState, Reproduction, RunStatus, RiskLevel
from .persistence import MemoryRepository
from .policy import validate_patch
from .sandbox import DockerSandbox, LocalSandbox
from .scanners import run_security_suite
from .verify import Verifier
from .llm import LLM


class RepairEngine:
    def __init__(self, github=None, sandbox=None, llm=None, repository=None, evidence=None, settings=None):
        self.settings = settings or Settings.from_env()
        self.github = github or GitHubClient(self.settings.github_token)
        self.sandbox = sandbox or (DockerSandbox(self.settings.sandbox_image) if self.settings.sandbox_backend == "docker" else LocalSandbox())
        self.llm = llm
        self.repository = repository or MemoryRepository()
        self.evidence = evidence or EvidenceLedger(Path(self.settings.evidence_dir))

    def start(self, issue: Issue, reproduction_cmd: list[str] | None = None, publish: bool = False) -> RepairState:
        state = RepairState(issue=issue)
        self.repository.save(state)
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix=f"shda-{state.run_id}-") as td:
            state.workspace = Path(td)
            try:
                state.status = RunStatus.CHECKING_OUT
                self._event(state, "checkout_started", {})
                state.provenance = self.github.checkout(issue.repository, state.workspace / "repo", issue.head_sha or issue.base_branch)
                repo = state.workspace / "repo"
                self._event(state, "checkout_completed", {"sha": state.provenance.resolved_sha})

                command = reproduction_cmd or ["python", "-m", "pytest", "-q"]
                state.status = RunStatus.REPRODUCING
                state.reproduction = self._reproduce(repo, command)
                self._event(state, "reproduction", state.reproduction.model_dump(mode="json"))
                if not state.reproduction.reproduced:
                    return self._fail(state, "baseline did not reproduce a failure")
                if not self.llm:
                    return self._fail(state, "LLM not configured")

                context = self._repository_context(repo)
                state.status = RunStatus.DIAGNOSING
                state.diagnosis = self.llm.diagnose(issue.title + "\n" + issue.body, self._evidence_text(state), context)
                self._event(state, "diagnosis", state.diagnosis.model_dump(mode="json"))

                for iteration in range(1, state.budget.max_iterations + 1):
                    state.iteration = iteration
                    state.status = RunStatus.PATCHING
                    files = self._context_files(repo, state.diagnosis.affected_files)
                    state.patch = self.llm.propose(state.diagnosis, files, self._evidence_text(state))
                    errors = validate_patch(state.patch, state.budget)
                    if errors:
                        return self._fail(state, "policy gate failed: " + "; ".join(errors))
                    state.status = RunStatus.GATING
                    state.patch.diff = unified_diff(repo, state.patch.files)
                    state.gates = run_security_suite(repo)
                    self._event(state, "security_gates", [g.model_dump(mode="json") for g in state.gates])
                    required_failures = [g for g in state.gates if g.required and not g.passed]
                    if required_failures:
                        return self._fail(state, "security gate failed")
                    if state.patch.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL} and self.settings.approval_required_for_high_risk:
                        state.status = RunStatus.AWAITING_APPROVAL
                        state.approval.required = True
                        return self._fail(state, "human approval required before high-risk patch")

                    apply_proposal(repo, state.patch, state.budget)
                    state.status = RunStatus.VERIFYING
                    state.verification = Verifier(self.sandbox).run(repo, [command, ["python", "-m", "compileall", "-q", "."]])
                    self._event(state, "verification", state.verification.model_dump(mode="json"))
                    if state.verification.passed:
                        state.status = RunStatus.PASSED
                        self._event(state, "repair_passed", {"iteration": iteration})
                        if publish and self.settings.auto_publish_pr:
                            from .pr import PRPublisher
                            state.status = RunStatus.PUBLISHING
                            state.pr_url = PRPublisher(self.settings.github_token).publish(issue.repository, repo, f"shda/{state.run_id}", f"fix: {issue.title}", self._pr_body(state), issue.base_branch)
                        return self._finish(state)
                    state.history.append({"stage": "reflection", "iteration": iteration, "failure": self._verification_failure(state)})
                    if iteration < state.budget.max_iterations:
                        state.status = RunStatus.DIAGNOSING
                        state.diagnosis = self.llm.diagnose(issue.title + "\n" + issue.body, self._evidence_text(state), self._repository_context(repo))
                return self._fail(state, "iteration budget exhausted")
            except Exception as exc:
                return self._fail(state, f"unexpected failure: {type(exc).__name__}: {exc}")
            finally:
                state.history.append({"stage": "runtime", "duration_ms": int((time.monotonic()-started)*1000)})
                self._finish(state)

    def _reproduce(self, repo: Path, command: list[str]) -> Reproduction:
        result = self.sandbox.run(repo, command, timeout=120)
        signature = (result.stderr or result.stdout)[-2000:] if result.exit_code else None
        return Reproduction(reproduced=result.exit_code != 0 and not result.timed_out, result=result, failure_signature=signature, baseline_passed=result.exit_code == 0)

    def _repository_context(self, repo: Path) -> str:
        files = []
        for path in sorted(repo.rglob("*")):
            if path.is_file() and ".git" not in path.parts and len(files) < 150:
                files.append(str(path.relative_to(repo)))
        return "\n".join(files)

    def _context_files(self, repo: Path, preferred: list[str]) -> dict[str, str]:
        candidates = preferred or [str(p.relative_to(repo)) for p in sorted(repo.rglob("*.py"))[:12]]
        result = {}
        for name in candidates[:12]:
            path = (repo / name).resolve()
            if repo.resolve() in path.parents and path.is_file():
                try: result[name] = path.read_text(errors="replace")[:20000]
                except OSError: pass
        return result

    def _evidence_text(self, state: RepairState) -> str:
        parts = []
        if state.reproduction and state.reproduction.result:
            parts.append(state.reproduction.result.stdout)
            parts.append(state.reproduction.result.stderr)
        if state.verification:
            for result in state.verification.results:
                parts.extend([result.stdout, result.stderr])
        return "\n".join(parts)[-20000:]

    def _verification_failure(self, state: RepairState) -> str:
        if not state.verification: return "no verification result"
        failed = [r for r in state.verification.results if r.exit_code != 0]
        return "\n".join((r.stderr or r.stdout) for r in failed)[-4000:]

    def _pr_body(self, state: RepairState) -> str:
        return f"Automated repair run `{state.run_id}`.\n\nIssue: #{state.issue.number}\nRevision: `{state.provenance.resolved_sha if state.provenance else 'unknown'}`\n\nRoot cause: {state.diagnosis.root_cause if state.diagnosis else 'unknown'}\n\nVerification: `{state.verification.passed if state.verification else False}`\n"

    def _event(self, state: RepairState, name: str, payload: dict) -> None:
        state.history.append({"stage": name, **payload})
        self.repository.save(state)
        self.evidence.append(str(state.run_id), name, payload)

    def _fail(self, state: RepairState, error: str) -> RepairState:
        state.status = RunStatus.FAILED
        state.errors.append(error)
        self._event(state, "failed", {"error": error})
        return self._finish(state)

    def _finish(self, state: RepairState) -> RepairState:
        self.repository.save(state)
        try: self.evidence.write_manifest(str(state.run_id), state)
        except Exception: pass
        return state
