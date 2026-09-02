from __future__ import annotations
import json
from pathlib import Path

def run():
    cases=list(Path(__file__).parent.glob("cases/*.json")); rows=[]
    for p in cases:
        d=json.loads(p.read_text()); rows.append({"id":d["id"],"status":"not_executed","note":"requires runnable fixture or immutable repository"})
    print(json.dumps({"cases":len(rows),"results":rows,"benchmark_claims_allowed":False},indent=2))

if __name__=="__main__": run()
