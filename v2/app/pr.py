from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

import httpx


class PRPublisher:
    """Publishes an already-verified local branch without placing the token in argv or remotes."""

    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("GITHUB_TOKEN")

    def publish(self, repository: str, workspace: Path, branch: str, title: str, body: str, base: str = "main") -> str:
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN is required")
        env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        with tempfile.NamedTemporaryFile("w", delete=False) as askpass:
            askpass.write("#!/bin/sh\necho \"$SHDA_GITHUB_TOKEN\"\n")
            askpass_path = askpass.name
        os.chmod(askpass_path, 0o700)
        env.update({"GIT_ASKPASS": askpass_path, "SHDA_GITHUB_TOKEN": self.token})
        try:
            subprocess.run(["git", "checkout", "-b", branch], cwd=workspace, check=True, env=env, capture_output=True, text=True)
            subprocess.run(["git", "add", "-A"], cwd=workspace, check=True, env=env, capture_output=True, text=True)
            status = subprocess.check_output(["git", "status", "--porcelain"], cwd=workspace, env=env, text=True).strip()
            if not status:
                raise RuntimeError("refusing to publish an empty branch")
            subprocess.run(["git", "commit", "-m", title], cwd=workspace, check=True, env=env, capture_output=True, text=True)
            subprocess.run(["git", "push", f"https://github.com/{repository}.git", branch], cwd=workspace, check=True, env=env, capture_output=True, text=True, timeout=120)
            headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {self.token}", "X-GitHub-Api-Version": "2022-11-28"}
            response = httpx.post(f"https://api.github.com/repos/{repository}/pulls", headers=headers, json={"title": title, "body": body, "head": branch, "base": base}, timeout=20)
            response.raise_for_status()
            return response.json()["html_url"]
        finally:
            try:
                os.unlink(askpass_path)
            except OSError:
                pass
