# Self-Healing DevOps Agent

Sandboxed, evidence-driven autonomous software repair for GitHub issues.

## Mission

Turn a GitHub issue into a reproducible, bounded, test-verified repair and a reviewable pull request:

`Issue → Explore → Reproduce → Diagnose → Patch → Validate → Verify → PR`

The project is deliberately built around safe autonomy: repository content is untrusted data, execution is isolated, changes are policy-gated, and success is established by verification rather than model confidence.

## Status

**v0.1 foundation / vertical-slice architecture.** Benchmark numbers are intentionally not fabricated. Run the evaluation harness to produce actual measurements.

## Architecture

```text
GitHub Issue
    ↓
Issue Analyzer → Repository Explorer
    ↓
Reproduction Engine
    ↓
Evidence-backed Diagnosis
    ↓
Bounded Patch Generator
    ↓
Diff / Security / Budget Gates
    ↓
Sandboxed Tests
    ↓
Independent Verification
   ├─ PASS → Pull Request
   └─ FAIL → Reflection → bounded retry
```

## Safety model

- Ephemeral Docker execution
- Non-root container user
- Network disabled by default
- CPU, memory, PID, disk and wall-clock budgets
- No secrets mounted into repair sandboxes
- Repository instructions are treated as untrusted data
- Dependency/config/workflow changes can be blocked by policy
- Patch size and file-count limits
- Secret, dependency and static-security gates
- Maximum repair iterations and token/cost budgets
- Checkpoint/resume state
- Never modify the default branch directly

Docker supports explicit CPU and memory limits; production deployments should treat Docker as one sandbox implementation and provide stronger isolation where the threat model requires it.

## Quickstart

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
python -m app.cli demo
```

API:

```bash
uvicorn app.api:app --reload
```

## Evaluation

```bash
python -m evals.harness
```

The harness reports Issue Resolution Rate, Patch Acceptance Rate, Regression Rate, False Fix Rate, Iterations/Issue, Tokens/Issue, Cost/Issue, latency, and security outcomes. Results are only published after actual benchmark execution.

## Repository map

- `app/` — API, CLI and orchestration
- `packages/` — domain, sandbox, policy, verification and model routing
- `evals/` — reproducible benchmark harness and cases
- `tests/` — unit, integration and security tests
- `docs/` — architecture, threat model, operations and evaluation
- `infra/` — local PostgreSQL/Redis/observability stack
- `.github/` — CI and repository governance

## Product path

Open-source repair engine → hosted repair platform → team governance/security → enterprise/on-prem execution → evaluation infrastructure.

## License

Apache-2.0
