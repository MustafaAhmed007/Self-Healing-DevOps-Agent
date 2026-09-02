from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class RunStatus(str, Enum):
    CREATED="created"; REPRODUCING="reproducing"; DIAGNOSING="diagnosing"; PATCHING="patching"; VERIFYING="verifying"; PASSED="passed"; FAILED="failed"

class Budget(BaseModel):
    max_iterations: int = 3
    max_runtime_seconds: int = 300
    max_patch_files: int = 10
    max_patch_lines: int = 300
    max_cost_usd: float = 2.0
    max_commands: int = 50

class Issue(BaseModel):
    repository: str
    number: int
    title: str = ""
    body: str = ""

class CommandResult(BaseModel):
    command: list[str]
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    timed_out: bool = False

class Reproduction(BaseModel):
    reproduced: bool
    result: CommandResult | None = None
    failure_signature: str | None = None

class Diagnosis(BaseModel):
    root_cause: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.0

class PatchProposal(BaseModel):
    files: dict[str, str] = Field(default_factory=dict)
    rationale: str = ""

class Verification(BaseModel):
    passed: bool
    checks: dict[str, bool] = Field(default_factory=dict)
    results: list[CommandResult] = Field(default_factory=list)

class RepairState(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    issue: Issue
    workspace: Path | None = None
    status: RunStatus = RunStatus.CREATED
    iteration: int = 0
    budget: Budget = Field(default_factory=Budget)
    reproduction: Reproduction | None = None
    diagnosis: Diagnosis | None = None
    patch: PatchProposal | None = None
    verification: Verification | None = None
    history: list[dict[str, Any]] = Field(default_factory=list)
