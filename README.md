# Self-Healing DevOps Agent

> **Evidence-driven autonomous software repair for GitHub issues — bounded, sandboxed, policy-gated, and reviewable.**

[![CI](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions/workflows/v2-ci.yml/badge.svg)](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions)

## What this is

Self-Healing DevOps Agent turns a software issue into a controlled repair attempt:

```text
Issue → Context → Immutable Checkout → Reproduce → Diagnose → Patch → Policy
     → Security Gates → Verify → Reflect (bounded) → Evidence → PR
```

The design goal is **safe autonomy, not blind autonomy**. Repository content, issue text, generated output, and tool output are untrusted data. Deterministic policy controls what the system is allowed to execute or mutate. Model confidence never counts as proof of correctness.

## Current release

**v0.3 engineering-complete control-plane target.** The repository now contains the complete reference architecture and implementation surfaces for the repair loop, persistence, queueing, sandboxing, security gates, verification, evidence, benchmark execution, API, CLI, observability hooks, PR publication, and operator console.

> **Important:** provider-backed integrations (GitHub credentials, PostgreSQL, Redis, Docker, scanners, LLMs and observability exporters) require their external services to be configured. The repository never fabricates benchmark or production measurements. CI and benchmark reports are evidence gates.

## Why it is different

Most coding agents optimize for generating a plausible patch. This project optimizes for a **verifiable repair transaction**:

1. Reproduce the reported failure before changing code.
2. Capture the exact revision and provenance.
3. Treat issue/repository instructions as untrusted input.
4. Generate a bounded patch instead of permitting arbitrary workspace mutation.
5. Run deterministic policy and security gates before verification.
6. Verify the fix independently, including regression checks.
7. Reflect only from observed failure evidence and within a hard iteration budget.
8. Produce an auditable evidence bundle and a reviewable pull request.

## Defence in depth

```text
                 UNTRUSTED INPUT
        issue / repo / PR / model output
                         │
                         ▼
              ┌─────────────────────┐
              │ Input normalization │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │ Policy + risk gate  │
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │ Immutable checkout  │
              └──────────┬──────────┘
                         ▼
       ┌──────────────────────────────────────┐
       │ Ephemeral sandbox                    │
       │ network=none • non-root • caps=drop  │
       │ no-new-privileges • CPU/RAM/PID/time │
       └──────────────────┬───────────────────┘
                          ▼
              ┌─────────────────────┐
              │ Reproduce + evidence│
              └──────────┬──────────┘
                         ▼
              ┌─────────────────────┐
              │ Model diagnosis     │
              │ + bounded patch     │
              └──────────┬──────────┘
                         ▼
       ┌──────────────────────────────────────┐
       │ Diff / path / size / secret / SAST   │
       │ dependency / provenance gates        │
       └──────────────────┬───────────────────┘
                          ▼
              ┌─────────────────────┐
              │ Independent verify │
              └───────┬───────┬─────┘
                      │PASS   │FAIL
                      ▼       ▼
                     PR    bounded reflection
                              │
                              └──→ evidence → retry
```

Docker explicitly supports runtime CPU and memory constraints, while the container runtime also provides controls such as `no-new-privileges`; these are useful layers but are not claimed to be a complete VM boundary. citeturn0search4turn0search9

For public repositories, the project does **not** assume a persistent self-hosted GitHub Actions runner is safe for untrusted code. GitHub warns that self-hosted runners can be persistently compromised by untrusted workflows and recommends strong isolation/ephemeral execution patterns. citeturn0search0turn0search1

## System architecture

### Control plane

- FastAPI API
- CLI
- repair job lifecycle
- PostgreSQL persistence adapter
- Redis queue adapter
- checkpoint/evidence store
- risk and approval state

### Intelligence plane

- provider-neutral LLM gateway
- optional LiteLLM routing
- structured diagnosis and patch proposals
- evidence-first prompts
- bounded reflection
- strategy/model metadata for future learned routing

### Execution plane

- immutable Git checkout
- local development executor
- Docker sandbox
- resource limits
- network isolation
- command/path policy
- no secrets by default
- scanner and verifier adapters

### Verification plane

- baseline reproduction
- compile/type/lint/test commands
- regression checks
- secret scan
- SAST adapter
- dependency scan adapter
- deterministic patch validation
- independent verification result

### Delivery plane

- branch creation
- commit
- GitHub API PR creation
- evidence summary
- approval gate for risky changes
- no default-branch mutation

## Repository architecture

```text
.
├── v2/
│   ├── app/
│   │   ├── api.py              # HTTP control plane
│   │   ├── audit.py            # append-only evidence events
│   │   ├── checkpoint.py       # portable checkpoint adapter
│   │   ├── cli.py              # operator CLI
│   │   ├── config.py           # environment/config model
│   │   ├── diff.py             # bounded unified-diff application
│   │   ├── engine.py           # repair state machine
│   │   ├── github.py           # GitHub issue/checkout/provenance
│   │   ├── graph.py            # optional LangGraph orchestration boundary
│   │   ├── llm.py              # provider-neutral model gateway
│   │   ├── models.py            # typed domain state
│   │   ├── persistence.py       # PostgreSQL-compatible repository
│   │   ├── policy.py            # deterministic safety policy
│   │   ├── pr.py                # verified PR publisher
│   │   ├── queue.py             # Redis/in-process job queue
│   │   ├── sandbox.py            # local + Docker execution
│   │   ├── scanners.py           # security/dependency/SAST adapters
│   │   ├── security.py           # secret/provenance helpers
│   │   └── verify.py             # independent verification
│   ├── evals/                   # executable benchmark harness + fixtures
│   ├── tests/                   # unit/integration/security tests
│   ├── docs/                    # architecture, threat model, operations
│   ├── console/                 # operator web console
│   ├── infra/                   # PostgreSQL, Redis, observability
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── STATUS.md
├── .github/workflows/           # hardened CI/security workflows
├── SECURITY.md
└── LICENSE
```

## End-to-end repair contract

A successful run must produce all of the following evidence:

- run ID and timestamps
- issue identifier
- repository and exact commit SHA
- baseline reproduction result
- commands and bounded outputs
- diagnosis with evidence
- proposed diff and policy decision
- security scan results
- verification commands and results
- reflection history, if any
- final commit SHA / PR URL when publication is enabled
- machine-readable evidence manifest

A model saying “fixed” is never sufficient.

## Safety contract

The default policy is deliberately conservative:

- never modify the default branch directly
- never execute an empty command
- block privileged/container-host escape flags
- block path traversal and absolute patch paths
- block secrets/private-key extensions and protected files
- limit patch file count and changed lines
- limit commands, runtime, iterations and estimated model cost
- no network in the default Docker sandbox
- no credentials mounted into the repair workspace
- require explicit approval for high-risk paths
- preserve provenance before mutation
- fail closed when a required gate cannot run

GitHub also recommends least-privilege workflow permissions and immutable SHA pinning for third-party actions. The production CI surface therefore uses read-only defaults and should keep action references pinned. citeturn0search0

## Quickstart

```bash
cd v2
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m app.cli demo
uvicorn app.api:app --reload
```

For the complete local stack:

```bash
cd v2
docker compose up --build
```

Then open the console at `http://localhost:3000` and the API at `http://localhost:8000/docs`.

## CLI

```bash
# dry-run/control-plane health
python -m app.cli demo

# start a repair using an explicit reproduction command
python -m app.cli repair OWNER/REPO ISSUE_NUMBER --repro python -m pytest -q

# execute the deterministic benchmark suite
python -m evals.harness --cases evals/cases --output evals/reports/latest.json
```

## Evaluation

The benchmark harness reports, from actual executions:

- Issue Resolution Rate
- Patch Acceptance Rate
- Regression Rate
- False Fix Rate
- Iterations / issue
- latency
- command count
- security gate outcomes
- cost metadata when supplied by the model gateway

No score is published as a claim until a raw report exists in `evals/reports/`.

## Self-improvement loop

```text
Run → Observe → Classify failure → Preserve evidence
  → Compare strategy/model/tool choice
  → Evaluate on held-out cases
  → Promote only if statistically/operationally better
  → Deploy → Observe again
```

The agent is therefore designed to improve from **measured repair outcomes**, not from unverified self-generated conclusions.

## Roadmap / completeness ledger

### Built in the repository

- [x] typed repair state and budgets
- [x] GitHub issue acquisition and repository checkout
- [x] provenance capture
- [x] local and Docker sandbox adapters
- [x] network/resource/capability controls
- [x] deterministic command/path policy
- [x] bounded patch/diff application
- [x] secret/security/dependency scanner interfaces
- [x] baseline reproduction and independent verification
- [x] bounded reflection state machine
- [x] portable checkpoints
- [x] PostgreSQL/Redis integration surfaces
- [x] structured LLM gateway
- [x] branch/commit/PR publisher
- [x] approval/risk model
- [x] evidence/audit manifest
- [x] executable benchmark fixtures/harness
- [x] API + CLI
- [x] operator console
- [x] Docker/Compose local stack
- [x] unit/security/integration test surfaces
- [x] CI/security workflow surfaces
- [x] architecture/threat/operations documentation

### Requires environment credentials or infrastructure to become operational

- [ ] real GitHub token/App credentials
- [ ] production PostgreSQL
- [ ] production Redis
- [ ] Docker daemon or stronger sandbox provider
- [ ] LLM provider credentials / local model
- [ ] deployed Langfuse/OpenTelemetry collector
- [ ] installed Gitleaks/Semgrep/Trivy/CodeQL binaries where those adapters are enabled
- [ ] human reviewer identity/approval integration

### Next hardening tier

- [ ] production microVM backend (Firecracker/Kata/gVisor class)
- [ ] GitHub App + webhook ingestion
- [ ] 100+ benchmark cases with public raw evidence
- [ ] adversarial prompt-injection/repository-escape suite
- [ ] learned routing/strategy promotion with held-out evaluation
- [ ] multi-tenant hosted control plane

These are infrastructure/deployment milestones rather than missing core architecture. They must remain visible instead of being silently treated as complete.

## Product path

**Open-source repair engine → hosted repair platform → team governance/security → enterprise/on-prem execution → repair benchmark/evaluation platform.**

The moat is the combination of **repair traces + benchmark corpus + policy engine + verification evidence + deployment feedback**, not merely the prompt or model.

## Security

Read `SECURITY.md` and `v2/docs/THREAT_MODEL.md` before enabling autonomous PR publication. For public repositories, prefer ephemeral hosted or stronger isolated execution rather than persistent self-hosted runners; GitHub explicitly warns about the risk of untrusted code on self-hosted runners. citeturn0search0turn0search1

## License

Apache-2.0
