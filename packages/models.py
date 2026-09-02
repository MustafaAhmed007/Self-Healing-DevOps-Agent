from __future__ import annotations

from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class RunStatus(StrEnum):
    CREATED = "created"
    RUNNING = "running"
    BLOCKED = "blocked"
    VERIFYING = "verifying"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RepositoryRef(BaseModel):
    url: HttpUrl
    commit: str | None = None
    default_branch: str = "main"


class Issue(BaseModel):
    number: int
    title: str
    body: str = ""


class Evidence(BaseModel):
    kind: str
    summary: str
    artifact: str | None = None
    file: str | None = None
    line_start: int | None = None
    line_end: int | None = None


class IssueAnalysis(BaseModel):
    problem_statement: str
    expected_behavior: str | None = None
    actual_behavior: str | None = None
    acceptance_criteria: list[str] = Field(default_factory=list)
    suspected_components: list[str] = Field(default_factory=list)
    ambiguities: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class ReproductionResult(BaseModel):
    reproduced: bool
    command: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    failure_signature: str | None = None
    duration_ms: int = 0
    evidence: list[Evidence] = Field(default_factory=list)


class Diagnosis(BaseModel):
    root_cause: str
    evidence: list[Evidence] = Field(default_factory=list)
    candidate_files: list[str] = Field(default_factory=list)
    patch_strategy: str
    confidence: float = Field(ge=0, le=1)


class PatchPolicy(BaseModel):
    max_files_changed: int = 10
    max_lines_added: int = 300
    max_lines_deleted: int = 200
    allow_new_dependencies: bool = False
    allow_dependency_updates: bool = False
    allow_lockfile_changes: bool = False
    allow_config_changes: bool = False
    allow_ci_changes: bool = False
    protected_paths: list[str] = Field(default_factory=lambda: [".github/workflows", ".env", "*.pem", "*.key"])


class PatchAttempt(BaseModel):
    iteration: int
    strategy: str
    files_changed: list[str] = Field(default_factory=list)
    diff: str = ""
    accepted_by_policy: bool = False
    rejection_reasons: list[str] = Field(default_factory=list)


class VerificationResult(BaseModel):
    passed: bool
    checks: dict[str, bool] = Field(default_factory=dict)
    failures: list[str] = Field(default_factory=list)


class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0


class RepairState(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    repository: RepositoryRef
    issue: Issue
    status: RunStatus = RunStatus.CREATED
    issue_analysis: IssueAnalysis | None = None
    reproduction: ReproductionResult | None = None
    diagnosis: Diagnosis | None = None
    patch_attempts: list[PatchAttempt] = Field(default_factory=list)
    verification: VerificationResult | None = None
    iteration: int = 0
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    cost_usd: float = 0.0
    artifacts: list[str] = Field(default_factory=list)
    events: list[dict[str, Any]] = Field(default_factory=list)
