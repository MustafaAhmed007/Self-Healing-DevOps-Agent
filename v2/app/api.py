from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .engine import RepairEngine
from .models import Issue

app=FastAPI(title="Self-Healing DevOps Agent",version="0.2.0")
class RepairRequest(BaseModel): repository:str; issue_number:int; reproduction_command:list[str]|None=None

@app.get("/health")
def health(): return {"status":"ok","version":"0.2.0"}

@app.post("/v1/repairs")
def repair(req: RepairRequest):
    try: return RepairEngine().start(Issue(repository=req.repository,number=req.issue_number),req.reproduction_command).model_dump(mode="json")
    except Exception as e: raise HTTPException(500,str(e))
