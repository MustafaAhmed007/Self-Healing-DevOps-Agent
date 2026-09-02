from __future__ import annotations

from pathlib import Path
from typing import Protocol

from packages.models import Diagnosis, IssueAnalysis, RepairState


class Reasoner(Protocol):
    def analyze_issue(self, issue_title: str, issue_body: str) -> IssueAnalysis: ...
    def diagnose(self, evidence: str) -> Diagnosis: ...
    def propose_patch(self, diagnosis: Diagnosis, source: str) -> str: ...
    def reflect(self, failure: str, prior_patch: str) -> str: ...


class HeuristicReasoner:
    """Offline-safe baseline used for demos and tests; replace with LiteLLM/Ollama adapters."""

    def analyze_issue(self, issue_title: str, issue_body: str) -> IssueAnalysis:
        return IssueAnalysis(
            problem_statement=f"{issue_title}\n{issue_body}".strip(),
            acceptance_criteria=["The original failure no longer reproduces", "Regression tests pass"],
            confidence=0.5,
        )

    def diagnose(self, evidence: str) -> Diagnosis:
        return Diagnosis(
            root_cause="Diagnosis requires execution evidence and repository context.",
            evidence=[],
            patch_strategy="Inspect the failing path and make the smallest test-backed change.",
            confidence=0.2,
        )

    def propose_patch(self, diagnosis: Diagnosis, source: str) -> str:
        return source

    def reflect(self, failure: str, prior_patch: str) -> str:
        return f"Review failed verification evidence and revise the patch: {failure}"


def repository_snapshot(root: Path) -> str:
    files = sorted(p for p in root.rglob("*") if p.is_file())
    return "\n".join(str(p.relative_to(root)) for p in files[:500])


def initial_state(state: RepairState) -> RepairState:
    state.status = "running"
    state.events.append({"event": "run_started", "run_id": str(state.run_id)})
    return state
