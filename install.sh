#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo 'Python 3.11+ is required.'; exit 1; }
python3 v2/install.py
