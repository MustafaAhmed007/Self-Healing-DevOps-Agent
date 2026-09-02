from __future__ import annotations
import os, re, subprocess
from pathlib import Path
import httpx
from .models import Issue

class GitHubClient:
    def __init__(self, token: str|None=None): self.token=token or os.getenv("GITHUB_TOKEN")
    def issue(self, repository: str, number: int) -> Issue:
        headers={"Accept":"application/vnd.github+json"}
        if self.token: headers["Authorization"]=f"Bearer {self.token}"
        r=httpx.get(f"https://api.github.com/repos/{repository}/issues/{number}",headers=headers,timeout=20); r.raise_for_status(); d=r.json()
        return Issue(repository=repository,number=number,title=d.get("title", ""),body=d.get("body") or "")
    def checkout(self, repository: str, dest: Path, ref: str="") -> None:
        dest.parent.mkdir(parents=True,exist_ok=True)
        cmd=["git","clone","--depth","1"]
        if ref: cmd += ["--branch",ref]
        cmd += [f"https://github.com/{repository}.git",str(dest)]
        subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=120)
