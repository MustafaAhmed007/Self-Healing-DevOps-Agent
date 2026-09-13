from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


MIN_PYTHON = (3, 11)


def main() -> int:
    if sys.version_info < MIN_PYTHON:
        raise SystemExit(f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required; found {sys.version.split()[0]}")
    root = Path(__file__).resolve().parent
    venv = root / ".venv"
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(venv)])
    subprocess.check_call([str(python), "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([str(python), "-m", "pip", "install", "-e", ".[dev]"])
    subprocess.check_call([str(python), "-m", "pytest", "-q"], cwd=root)
    print("\nSHDA is installed and verified. Run:")
    print(f"  {python} -m app.cli demo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
