from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import Settings
from .engine import RepairEngine
from .models import Issue
from .research import MultiAspectResearch


def main():
    p = argparse.ArgumentParser(prog="shda")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("repair")
    r.add_argument("repository")
    r.add_argument("issue", type=int)
    r.add_argument("--repro", nargs="+")
    research = sub.add_parser("research", help="gather evidence from cloud, URLs, and local repository")
    research.add_argument("question")
    research.add_argument("--repo", type=Path)
    research.add_argument("--url", action="append", default=[])
    research.add_argument("--aspect", action="append", default=[])
    sub.add_parser("demo")
    a = p.parse_args()
    if a.cmd == "demo":
        print(json.dumps({"status": "ready", "version": "0.3.0", "research": "cloud-optional/local-fallback"}, indent=2))
        return
    if a.cmd == "research":
        s = Settings.from_env()
        results = MultiAspectResearch(s.research_url, s.research_timeout, s.research_max_chars).gather(
            a.question, a.repo, a.url, a.aspect or None
        )
        print(json.dumps([r.__dict__ for r in results], indent=2))
        return
    state = RepairEngine().start(Issue(repository=a.repository, number=a.issue), a.repro)
    print(state.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
