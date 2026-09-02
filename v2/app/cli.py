from __future__ import annotations
import argparse, json
from .models import Issue
from .engine import RepairEngine

def main():
    p=argparse.ArgumentParser(prog="shda")
    sub=p.add_subparsers(dest="cmd",required=True)
    r=sub.add_parser("repair"); r.add_argument("repository"); r.add_argument("issue",type=int); r.add_argument("--repro",nargs="+")
    sub.add_parser("demo")
    a=p.parse_args()
    if a.cmd=="demo": print(json.dumps({"status":"ready","version":"0.2.0","mode":"control-plane-demo"},indent=2)); return
    state=RepairEngine().start(Issue(repository=a.repository,number=a.issue),a.repro)
    print(state.model_dump_json(indent=2))

if __name__=="__main__": main()
