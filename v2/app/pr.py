from __future__ import annotations
import os, subprocess
from pathlib import Path
import httpx

class PRPublisher:
    """Publishes an already-verified local branch through GitHub's API."""
    def __init__(self, token=None): self.token=token or os.getenv("GITHUB_TOKEN")
    def publish(self, repository: str, workspace: Path, branch: str, title: str, body: str, base="main") -> str:
        if not self.token: raise RuntimeError("GITHUB_TOKEN is required")
        env={**os.environ,"GIT_TERMINAL_PROMPT":"0"}
        subprocess.run(["git","checkout","-b",branch],cwd=workspace,check=True,env=env)
        subprocess.run(["git","add","-A"],cwd=workspace,check=True,env=env)
        subprocess.run(["git","commit","-m",title],cwd=workspace,check=True,env=env)
        # Push through the authenticated GitHub API path via a temporary remote URL.
        remote=f"https://x-access-token:{self.token}@github.com/{repository}.git"
        subprocess.run(["git","push",remote,branch],cwd=workspace,check=True,env=env,capture_output=True,text=True,timeout=120)
        h={"Accept":"application/vnd.github+json","Authorization":f"Bearer {self.token}","X-GitHub-Api-Version":"2022-11-28"}
        r=httpx.post(f"https://api.github.com/repos/{repository}/pulls",headers=h,json={"title":title,"body":body,"head":branch,"base":base},timeout=20); r.raise_for_status()
        return r.json()["html_url"]
