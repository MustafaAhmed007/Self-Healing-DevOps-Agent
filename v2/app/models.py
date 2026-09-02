from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    CHECKING_OUT = "checking_out"
    REPRODUCING = "reproducing"
    DIAGNOSING = "diagnosing"
    PATCHING = "patching"
    GATING = "gating"
    VERIFYING = "verifying"
    AWAITING_APPROVAL = "awaiting_approval"
    PUBLISHING = "publishing"
    PASSED = "passed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Budget(BaseModel):
    max_iterations: int = 3
    max_runtime_seconds: int = 300
    max_patch_files: int = 10
    max_patch_lines: int = 300
    max_commands: int = 50
    max_output_chars: int = 20_000
    max_cost_usd: float = 2.0


class Issue(BaseModel):
    repository: str
    number: int
    title: str = ""
    body: str = ""
    base_branch: str = "main"
    head_sha: str | None = None


class Provenance(BaseModel):
    repository: str
    requested_ref: str
    resolved_sha: str
    fetched_at: str
    dirty_before: bool = False


class CommandResult(BaseModel):
    command: list[str]
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    duration_ms: int = 0
    timed_out: bool = False
    sandbox: str = "unknown"


class Reproduction(BaseModel):
    reproduced: bool
    result: CommandResult | None = None
    failure_signature: str | None = None
    baseline_passed: bool = False


class Diagnosis(BaseModel):
    root_cause: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    affected_files: list[str] = Field(default_factory=list)


class PatchProposal(BaseModel):
    files: dict[str, str] = Field(default_factory=dict)
    rationale: str = ""
    diff: str = ""
    risk: RiskLevel = RiskLevel.MEDIUM


class GateResult(BaseModel):
    name: str
    passed: bool
    required: bool = True
    findings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Verification(BaseModel):
    passed: bool
    checks: dict[str, bool] = Field(default_factory=dict)
    results: list[CommandResult] = Field(default_factory=list)
    regression_passed: bool = False


class Approval(BaseModel):
    required: bool = False
    approved: bool = False
    actor: str | None = None
    reason: str | None = None


class RepairState(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    issue: Issue
    workspace: Path | None = None
    status: RunStatus = RunStatus.CREATED
    iteration: int = 0
    budget: Budget = Field(default_factory=Budget)
    provenance: Provenance | None = None
    reproduction: Reproduction | None = None
    diagnosis: Diagnosis | None = None
    patch: PatchProposal | None = None
    gates: list[GateResult] = Field(default_factory=list)
    approval: Approval = Field(default_factory=Approval)
    verification: Verification | None = None
    pr_url: str | None = None
    history: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
