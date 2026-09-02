from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .config import Settings
from .engine import RepairEngine
from .models import Issue, RepairState
from .persistence import MemoryRepository

app = FastAPI(title="Self-Healing DevOps Agent", version="0.3.0", description="Bounded evidence-driven autonomous software repair")
settings = Settings.from_env()
repository = MemoryRepository()


class RepairRequest(BaseModel):
    repository: str
    issue_number: int = Field(gt=0)
    reproduction_command: list[str] | None = None
    base_branch: str = "main"
    publish: bool = False


class ApprovalRequest(BaseModel):
    approved: bool
    actor: str = Field(min_length=1, max_length=200)
    reason: str = Field(default="", max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.3.0", "sandbox": settings.sandbox_backend}


@app.post("/v1/repairs", response_model=RepairState)
def repair(req: RepairRequest):
    try:
        issue = Issue(repository=req.repository, number=req.issue_number, base_branch=req.base_branch)
        engine = RepairEngine(repository=repository, settings=settings)
        return engine.start(issue, req.reproduction_command, req.publish)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"repair failed: {type(exc).__name__}: {exc}") from exc


@app.get("/v1/repairs/{run_id}", response_model=RepairState)
def get_repair(run_id: str):
    state = repository.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="run not found")
    return state


@app.post("/v1/repairs/{run_id}/approval", response_model=RepairState)
def approve(run_id: str, req: ApprovalRequest):
    state = repository.get(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="run not found")
    state.approval.required = True
    state.approval.approved = req.approved
    state.approval.actor = req.actor
    state.approval.reason = req.reason
    repository.save(state)
    return state
