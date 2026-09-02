from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class EvidenceLedger:
    """Append-only JSONL ledger suitable for local evidence and later object storage."""
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def append(self, run_id: str, event: str, payload: dict[str, Any]) -> None:
        path = self.root / f"{run_id}.jsonl"
        record = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, "payload": payload}
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, default=str) + "\n")

    def write_manifest(self, run_id: str, state: Any) -> Path:
        path = self.root / f"{run_id}.json"
        data = state.model_dump(mode="json")
        encoded = json.dumps(data, sort_keys=True, indent=2).encode()
        manifest = {"run_id": str(run_id), "sha256": sha256_bytes(encoded), "state": data}
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
        return path
