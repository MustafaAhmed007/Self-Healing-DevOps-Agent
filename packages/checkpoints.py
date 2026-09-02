from __future__ import annotations

import json
from pathlib import Path

from packages.models import RepairState


class CheckpointStore:
    def __init__(self, root: Path = Path(".repair-checkpoints")) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, state: RepairState) -> Path:
        path = self.root / f"{state.run_id}.json"
        path.write_text(state.model_dump_json(indent=2))
        return path

    def load(self, run_id: str) -> RepairState:
        path = self.root / f"{run_id}.json"
        return RepairState.model_validate_json(path.read_text())
