from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class StrategyLedger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, strategy: str, outcome: str, metrics: dict[str, Any]) -> None:
        row = {"strategy": strategy, "outcome": outcome, "metrics": metrics}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")

    def promote(self, candidate: str, baseline: str, minimum_gain: float = 0.05) -> bool:
        """Promotion is conservative: caller supplies held-out success rates; no self-approval from model output."""
        rows = [json.loads(line) for line in self.path.read_text().splitlines()] if self.path.exists() else []
        scores = {}
        for row in rows:
            if row.get("outcome") == "success":
                scores.setdefault(row["strategy"], []).append(float(row.get("metrics", {}).get("success_rate", 0)))
        c = sum(scores.get(candidate, [0])) / max(1, len(scores.get(candidate, [])))
        b = sum(scores.get(baseline, [0])) / max(1, len(scores.get(baseline, [])))
        return c >= b + minimum_gain
