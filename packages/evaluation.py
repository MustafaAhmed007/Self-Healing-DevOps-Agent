from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import time


@dataclass(frozen=True)
class EvalCase:
    id: str
    description: str
    command: list[str]


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    success: bool
    latency_ms: int
    iterations: int = 1
    tokens: int = 0
    cost_usd: float = 0.0


def load_cases(directory: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for path in sorted(directory.glob("*.json")):
        data = json.loads(path.read_text())
        cases.append(EvalCase(data["id"], data.get("description", ""), data["command"]))
    return cases


def run_case(case: EvalCase, runner) -> EvalResult:
    start = time.monotonic()
    success = bool(runner(case.command))
    return EvalResult(case.id, success, round((time.monotonic() - start) * 1000), 1)


def summarize(results: list[EvalResult]) -> dict[str, float]:
    if not results:
        return {"cases": 0, "issue_resolution_rate": 0.0, "median_latency_ms": 0.0}
    successes = sum(r.success for r in results)
    latencies = sorted(r.latency_ms for r in results)
    mid = len(latencies) // 2
    median = latencies[mid] if len(latencies) % 2 else (latencies[mid - 1] + latencies[mid]) / 2
    return {"cases": len(results), "issue_resolution_rate": successes / len(results), "median_latency_ms": median}
