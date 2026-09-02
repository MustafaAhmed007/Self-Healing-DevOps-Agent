from __future__ import annotations

from pathlib import Path

from packages.models import RepairState
from packages.reasoning import HeuristicReasoner


class RepairOrchestrator:
    """Deterministic control-plane skeleton. LLM adapters can be injected without changing policy boundaries."""

    def __init__(self, reasoner=None) -> None:
        self.reasoner = reasoner or HeuristicReasoner()

    def start(self, state: RepairState) -> RepairState:
        state.status = "running"
        state.issue_analysis = self.reasoner.analyze_issue(state.issue.title, state.issue.body)
        state.events.append({"node": "issue_analyzer", "status": "completed"})
        state.events.append({"node": "repository_explorer", "status": "pending_execution"})
        state.events.append({"node": "reproducer", "status": "pending_execution"})
        state.events.append({"node": "code_analyst", "status": "pending_execution"})
        state.events.append({"node": "patch_generator", "status": "pending_execution"})
        state.events.append({"node": "verifier", "status": "pending_execution"})
        return state
