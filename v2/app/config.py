from __future__ import annotations

import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    github_token: str | None = None
    github_api_url: str = "https://api.github.com"
    default_branch: str = "main"
    sandbox_backend: str = "local"
    sandbox_image: str = "python:3.12-slim"
    postgres_dsn: str | None = None
    redis_url: str | None = None
    llm_model: str | None = None
    llm_api_key: str | None = None
    research_url: str | None = None
    research_timeout: int = Field(default=15, ge=1, le=120)
    research_max_chars: int = Field(default=12000, ge=1000, le=100000)
    langfuse_public_key: str | None = None
    langfuse_secret_key: str | None = None
    langfuse_host: str | None = None
    evidence_dir: str = "./data/evidence"
    approval_required_for_high_risk: bool = True
    auto_publish_pr: bool = False
    max_workers: int = Field(default=2, ge=1, le=32)

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            github_token=os.getenv("GITHUB_TOKEN"),
            github_api_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
            default_branch=os.getenv("DEFAULT_BRANCH", "main"),
            sandbox_backend=os.getenv("SANDBOX_BACKEND", "local"),
            sandbox_image=os.getenv("SANDBOX_IMAGE", "python:3.12-slim"),
            postgres_dsn=os.getenv("DATABASE_URL"),
            redis_url=os.getenv("REDIS_URL"),
            llm_model=os.getenv("LLM_MODEL"),
            llm_api_key=os.getenv("LLM_API_KEY"),
            research_url=os.getenv("SHDA_RESEARCH_URL"),
            research_timeout=int(os.getenv("SHDA_RESEARCH_TIMEOUT", "15")),
            research_max_chars=int(os.getenv("SHDA_RESEARCH_MAX_CHARS", "12000")),
            langfuse_public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            langfuse_secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            langfuse_host=os.getenv("LANGFUSE_HOST"),
            evidence_dir=os.getenv("EVIDENCE_DIR", "./data/evidence"),
            approval_required_for_high_risk=os.getenv("APPROVAL_REQUIRED_FOR_HIGH_RISK", "true").lower() == "true",
            auto_publish_pr=os.getenv("AUTO_PUBLISH_PR", "false").lower() == "true",
            max_workers=int(os.getenv("MAX_WORKERS", "2")),
        )
