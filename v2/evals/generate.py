from __future__ import annotations

import argparse
import json
from pathlib import Path


def make_case(i: int) -> dict:
    return {
        "id": f"synthetic_{i:03d}",
        "language": "python",
        "description": "Deterministic arithmetic repair fixture",
        "test_command": ["python", "-m", "pytest", "-q"],
        "files": {
            "app.py": f"def value(x):\n    return x + {i} - 1\n",
            "test_app.py": f"from app import value\n\ndef test_value():\n    assert value(10) == {10 + i}\n",
        },
        "expected_fix": {"app.py": f"def value(x):\n    return x + {i}\n"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "generated")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for i in range(1, args.count + 1):
        (args.output / f"synthetic_{i:03d}.json").write_text(json.dumps(make_case(i), indent=2))
    print(f"generated {args.count} cases in {args.output}")


if __name__ == "__main__":
    main()
