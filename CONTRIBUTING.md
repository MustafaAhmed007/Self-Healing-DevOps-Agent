# Contributing

1. Create a focused branch.
2. Add or update tests.
3. Run `pytest` and `ruff check .`.
4. For security changes, add an adversarial test.
5. For repair behavior changes, add or update an evaluation case.
6. Do not commit credentials or benchmark oracle artifacts.

Prefer small changes with explicit evidence. The agent itself follows the same principle: reproduce first, patch minimally, verify independently.
