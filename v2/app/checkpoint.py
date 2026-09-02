from __future__ import annotations
import json
from pathlib import Path
from .models import RepairState

class FileCheckpointStore:
    """Portable checkpoint store; production adapter can use LangGraph/PostgreSQL."""
    def __init__(self, root: Path): self.root=root; self.root.mkdir(parents=True,exist_ok=True)
    def save(self,state: RepairState) -> Path:
        p=self.root/f"{state.run_id}.json"; p.write_text(state.model_dump_json(indent=2)); return p
    def load(self,run_id:str)->RepairState:
        return RepairState.model_validate_json((self.root/f"{run_id}.json").read_text())
