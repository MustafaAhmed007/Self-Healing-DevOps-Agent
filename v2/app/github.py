from __future__ import annotations

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import httpx

from .models import Issue, Provenance


class GitHubClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("GITHUB_TOKEN")

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def issue(self, repository: str, number: int) -> Issue:
        r = httpx.get(f"https://api.github.com/repos/{repository}/issues/{number}", headers=self._headers(), timeout=20)
        r.raise_for_status()
        data = r.json()
        return Issue(repository=repository, number=number, title=data.get("title", ""), body=data.get("body") or "", base_branch=data.get("milestone", {}).get("base_branch", "main") if isinstance(data.get("milestone"), dict) else "main")

    def default_branch(self, repository: str) -> str:
        r = httpx.get(f"https://api.github.com/repos/{repository}", headers=self._headers(), timeout=20)
        r.raise_for_status()
        return r.json().get("default_branch", "main")

    def checkout(self, repository: str, dest: Path, ref: str = "") -> Provenance:
        dest.parent.mkdir(parents=True, exist_ok=True)
        requested = ref or self.default_branch(repository)
        subprocess.run(["git", "clone", "--no-tags", f"https://github.com/{repository}.git", str(dest)], check=True, capture_output=True, text=True, timeout=180)
        if ref:
            subprocess.run(["git", "fetch", "--no-tags", "origin", ref], cwd=dest, check=True, capture_output=True, text=True, timeout=120)
        resolved = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dest, text=True, timeout=20).strip()
        if ref:
            subprocess.run(["git", "checkout", "--detach", resolved], cwd=dest, check=True, capture_output=True, text=True, timeout=30)
        return Provenance(repository=repository, requested_ref=requested, resolved_sha=resolved, fetched_at=datetime.now(timezone.utc).isoformat())
