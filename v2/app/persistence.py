from __future__ import annotations

import json
from typing import Any
from .models import RepairState


class MemoryRepository:
    def __init__(self):
        self._items: dict[str, RepairState] = {}

    def save(self, state: RepairState) -> None:
        self._items[str(state.run_id)] = state.model_copy(deep=True)

    def get(self, run_id: str) -> RepairState | None:
        state = self._items.get(run_id)
        return state.model_copy(deep=True) if state else None


class PostgresRepository:
    """Small DB adapter. psycopg is optional so the local control plane stays dependency-light."""
    def __init__(self, dsn: str):
        try:
            import psycopg
        except ImportError as exc:
            raise RuntimeError("install the 'postgres' extra to use PostgreSQL") from exc
        self._psycopg = psycopg
        self.dsn = dsn
        with self._psycopg.connect(dsn) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS repair_runs (run_id TEXT PRIMARY KEY, state JSONB NOT NULL, updated_at TIMESTAMPTZ DEFAULT now())")

    def save(self, state: RepairState) -> None:
        payload = json.dumps(state.model_dump(mode="json"))
        with self._psycopg.connect(self.dsn) as conn:
            conn.execute("INSERT INTO repair_runs(run_id,state) VALUES(%s,%s) ON CONFLICT(run_id) DO UPDATE SET state=EXCLUDED.state, updated_at=now()", (str(state.run_id), payload))

    def get(self, run_id: str) -> RepairState | None:
        with self._psycopg.connect(self.dsn) as conn:
            row = conn.execute("SELECT state FROM repair_runs WHERE run_id=%s", (run_id,)).fetchone()
        return RepairState.model_validate(row[0]) if row else None
