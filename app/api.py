from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from packages.models import Issue, RepairState, RepositoryRef
from packages.orchestrator import RepairOrchestrator

app = FastAPI(title="Self-Healing DevOps Agent", version="0.1.0")
runs: dict[str, RepairState] = {}


class RepairRequest(BaseModel):
    repository_url: HttpUrl
    issue_number: int
    issue_title: str
    issue_body: str = ""
    commit: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/repairs")
def create_repair(req: RepairRequest) -> dict[str, Any]:
    state = RepairState(
        repository=RepositoryRef(url=req.repository_url, commit=req.commit),
        issue=Issue(number=req.issue_number, title=req.issue_title, body=req.issue_body),
    )
    orchestrator = RepairOrchestrator()
    state = orchestrator.start(state)
    runs[str(state.run_id)] = state
    return state.model_dump(mode="json")


@app.get("/v1/repairs/{run_id}")
def get_repair(run_id: str) -> dict[str, Any]:
    state = runs.get(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="repair run not found")
    return state.model_dump(mode="json")
