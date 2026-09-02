from __future__ import annotations

from pathlib import Path
import subprocess

from packages.evaluation import load_cases, run_case, summarize


def local_runner(command: list[str]) -> bool:
    p = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    return p.returncode == 0


def main() -> None:
    cases = load_cases(Path(__file__).parent / "devops")
    results = [run_case(case, local_runner) for case in cases]
    print(summarize(results))
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
