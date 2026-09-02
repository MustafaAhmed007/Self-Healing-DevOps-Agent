# SHDA v0.3 — Complete Reference Implementation

This directory contains the executable repair engine and its control-plane surfaces.

## Repair lifecycle

```text
GitHub Issue
   ↓
Normalize / classify trust
   ↓
Immutable checkout + provenance
   ↓
Baseline reproduction
   ↓
Repository context + evidence
   ↓
LLM diagnosis
   ↓
Minimal structured patch
   ↓
Policy + risk gate
   ↓
Security scanners
   ↓
Sandboxed verification
   ↓
PASS ─────────────→ evidence → optional PR
   │
   └─ FAIL → evidence → bounded reflection → retry
```

## Components

| Component | Responsibility |
|---|---|
| `app/engine.py` | bounded repair state machine |
| `app/github.py` | issue acquisition, checkout, provenance |
| `app/llm.py` | structured model gateway |
| `app/policy.py` | deterministic authorization |
| `app/diff.py` | safe patch application and diff generation |
| `app/sandbox.py` | local/Docker execution |
| `app/scanners.py` | Gitleaks/Semgrep/Trivy adapters |
| `app/verify.py` | independent verification |
| `app/audit.py` | append-only evidence + manifest hash |
| `app/persistence.py` | memory/PostgreSQL state |
| `app/queue.py` | in-process/Redis queue |
| `app/graph.py` | optional LangGraph orchestration/checkpoints |
| `app/pr.py` | verified branch and PR publication |
| `app/api.py` | HTTP control plane |
| `app/worker.py` | Redis worker entrypoint |
| `console/` | operator dashboard |
| `evals/` | executable fixture benchmark |

## Design invariant

**The model may reason; it may not become the authority.** Only deterministic, policy-approved tools may execute commands or mutate the workspace.

## Production boundary

The reference implementation is deployable, but production certification requires real credentials, external services and adversarial acceptance tests. See `docs/BUILD_LEDGER.md` for the exact evidence boundary.
