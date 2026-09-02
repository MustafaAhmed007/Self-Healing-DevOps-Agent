from __future__ import annotations

import os
import httpx


class GitHubClient:
    """Minimal REST client. Prefer a GitHub App installation token in production."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN is required for GitHub operations")
        self.base = "https://api.github.com"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_issue(self, owner: str, repo: str, number: int) -> dict:
        response = httpx.get(f"{self.base}/repos/{owner}/{repo}/issues/{number}", headers=self._headers(), timeout=20)
        response.raise_for_status()
        return response.json()

    def create_pull_request(self, owner: str, repo: str, title: str, body: str, head: str, base: str = "main") -> dict:
        response = httpx.post(
            f"{self.base}/repos/{owner}/{repo}/pulls",
            headers=self._headers(),
            json={"title": title, "body": body, "head": head, "base": base, "draft": True},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()
