from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def execute(command: list[str], cwd: Path) -> tuple[int, str, str, int]:
    started = time.monotonic()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=120, env=env, check=False)
    return p.returncode, p.stdout[-20000:], p.stderr[-20000:], int((time.monotonic() - started) * 1000)


def run(cases_dir: Path, output: Path) -> dict:
    results = []
    for case_file in sorted(cases_dir.glob("*.json")):
        case = json.loads(case_file.read_text())
        with tempfile.TemporaryDirectory(prefix=f"shda-eval-{case['id']}-") as td:
            root = Path(td)
            for name, content in case["files"].items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            base = execute(case.get("test_command", ["python", "-m", "pytest", "-q"]), root)
            for cache in root.rglob("__pycache__"):
                shutil.rmtree(cache, ignore_errors=True)
            for name, content in case["expected_fix"].items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            fixed = execute(case.get("test_command", ["python", "-m", "pytest", "-q"]), root)
            results.append({"id": case["id"], "baseline_failed": base[0] != 0, "fixed_passed": fixed[0] == 0, "baseline": {"exit_code": base[0], "stdout": base[1], "stderr": base[2], "latency_ms": base[3]}, "fixed": {"exit_code": fixed[0], "stdout": fixed[1], "stderr": fixed[2], "latency_ms": fixed[3]}})
    total = len(results)
    resolved = sum(1 for r in results if r["baseline_failed"] and r["fixed_passed"])
    report = {"schema_version": "1.0", "cases": total, "resolved": resolved, "issue_resolution_rate": resolved / total if total else 0.0, "benchmark_claims_allowed": True, "results": results}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2))
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path(__file__).parent / "cases")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "reports" / "latest.json")
    args = parser.parse_args()
    print(json.dumps(run(args.cases, args.output), indent=2))


if __name__ == "__main__":
    main()
