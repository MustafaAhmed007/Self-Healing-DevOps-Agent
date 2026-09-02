# Self-Healing DevOps Agent

> **Evidence-driven autonomous software repair for GitHub issues — bounded, sandboxed, policy-gated, and reviewable.**

[![CI](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions/workflows/v2-ci.yml/badge.svg)](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions)

## What this is

Self-Healing DevOps Agent turns a software issue into a controlled repair transaction:

```text
Issue → Context → Immutable Checkout → Reproduce → Diagnose → Patch → Policy
     → Security Gates → Verify → Reflect (bounded) → Evidence → PR
```

The design goal is **safe, evidence-driven autonomy — not blind autonomy**. Repository content, issue text, generated output, and tool output are untrusted data. Deterministic policy controls what the system is allowed to execute or mutate. Model confidence never counts as proof of correctness.

## Current release and versioning

**Current implementation: v0.3 — engineering-complete reference architecture.**

The repository grew through earlier V0.1/V0.2 construction stages. The `v2/` directory is retained as the implementation workspace name from that evolution; it does **not** mean that the project is currently “V2”. The authoritative release/version is the package version in `v2/pyproject.toml`, currently **0.3.0**.

In other words:

```text
V0.1 foundation
      ↓
V0.2 repair-loop vertical slice
      ↓
V0.3 current reference implementation  ← YOU ARE HERE
      ↓
Future production hardening / hosted releases
```

The codebase contains the core reference architecture and implementation surfaces for repair orchestration, persistence adapters, queueing, sandboxing, security gates, verification, evidence, benchmarks, API, CLI, observability hooks, PR publication, and the operator console.

> **Important:** “built in the repository” and “operational in a live environment” are intentionally different states. GitHub credentials, PostgreSQL, Redis, Docker, scanners, LLM providers, and observability backends require external configuration. The repository never fabricates production measurements.

## Technology stack

| Layer | Technology | Role |
|---|---|---|
| Language | **Python 3.11+** | Core agent/runtime implementation |
| API | **FastAPI + Uvicorn** | Control-plane API and service runtime |
| Data validation | **Pydantic v2** | Typed repair state, contracts, configuration |
| Agent orchestration | **LangGraph boundary** | Stateful graph execution, checkpoint/HITL integration path |
| Model gateway | **LiteLLM-compatible** | Provider-neutral LLM routing and structured generation |
| Local inference | **Ollama-compatible path** | Optional local/private model execution |
| Database | **PostgreSQL + psycopg** | Durable jobs, runs, evidence metadata, approvals |
| Queue | **Redis** | Background repair jobs, coordination, future distributed workers |
| Sandbox | **Docker** | Default isolated execution boundary |
| Strong isolation | **Firecracker / Kata / gVisor class** | Production hardening path for hostile workloads |
| SCM | **Git + GitHub API** | Immutable checkout, branches, commits, pull requests |
| Verification | **pytest / project-native commands** | Baseline, patch and regression verification |
| Security | **Gitleaks / Semgrep / Trivy / CodeQL adapters** | Secrets, SAST, dependency and code scanning |
| Observability | **OpenTelemetry + Langfuse-compatible path** | Traces, metrics, logs, model/tool telemetry |
| Metrics | **Prometheus-compatible path** | Operational metrics and alerting |
| Dashboards | **Grafana-compatible path** | Repair/run/system observability |
| Web console | **Next.js / React** | Operator control and repair visibility |
| Containers | **Docker + Compose** | Reproducible local deployment |
| CI/CD | **GitHub Actions** | Test, lint, security and benchmark gates |
| Testing | **pytest + adversarial/security fixtures** | Unit, integration, policy and safety verification |
| Evaluation | **Executable benchmark harness** | Resolution, regression, latency, cost and safety metrics |
| Configuration | **Environment-based configuration** | Deploy-time secrets and runtime controls |

The stack is deliberately modular: the agent should not become coupled to one model provider, observability vendor, sandbox implementation, queue, or deployment target.

OpenTelemetry is used as the observability direction because it is vendor-neutral and supports correlated traces, metrics, and logs across distributed systems. citeturn0search1turn0search6

For CI supply-chain security, GitHub recommends least-privilege workflow permissions and pinning third-party Actions to full commit SHAs; the repository follows that direction for its hardened workflow surface. citeturn0search0turn0search13

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

Docker supports runtime CPU and memory constraints and other container security controls; these are treated as defence-in-depth layers, not as a claim that a normal container is equivalent to a hostile-code VM boundary.

For public repositories, the project does **not** assume a persistent self-hosted GitHub Actions runner is safe for untrusted code. GitHub documents the risks of untrusted workloads on self-hosted runners and recommends strong isolation/ephemeral execution patterns. citeturn0search0

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
- optional local-model path
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
- pluggable stronger isolation boundary

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

### Observability plane

- structured run events
- trace/span model
- metrics for latency, failures, iterations and resource use
- model/tool cost metadata
- OpenTelemetry export path
- Langfuse-compatible LLM tracing path
- Prometheus/Grafana-compatible operational monitoring

## Repository architecture

```text
.
├── v2/                         # historical implementation workspace; current package is v0.3
│   ├── app/
│   │   ├── api.py              # HTTP control plane
│   │   ├── audit.py            # append-only evidence events
│   │   ├── checkpoint.py       # portable checkpoint adapter
│   │   ├── cli.py              # operator CLI
│   │   ├── config.py           # environment/config model
│   │   ├── diff.py             # bounded unified-diff application
│   │   ├── engine.py           # repair state machine
│   │   ├── github.py            # GitHub issue/checkout/provenance
│   │   ├── graph.py             # orchestration boundary
│   │   ├── llm.py               # provider-neutral model gateway
│   │   ├── models.py             # typed domain state
│   │   ├── persistence.py        # PostgreSQL-compatible repository
│   │   ├── policy.py             # deterministic safety policy
│   │   ├── pr.py                 # verified PR publisher
│   │   ├── queue.py              # Redis/in-process job queue
│   │   ├── sandbox.py             # local + Docker execution
│   │   ├── scanners.py            # security/dependency/SAST adapters
│   │   ├── security.py            # secret/provenance helpers
│   │   └── verify.py               # independent verification
│   ├── evals/                    # executable benchmark harness + fixtures
│   ├── tests/                    # unit/integration/security tests
│   ├── docs/                     # architecture, threat model, operations
│   ├── console/                  # operator web console
│   ├── infra/                    # PostgreSQL, Redis, observability
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── pyproject.toml
│   └── STATUS.md
├── .github/workflows/            # hardened CI/security workflows
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

No score is published as a real-world claim until a raw report exists in `evals/reports/` and the benchmark definition is reproducible.

## Self-improvement loop

```text
Run → Observe → Classify failure → Preserve evidence
  → Compare strategy/model/tool choice
  → Evaluate on held-out cases
  → Promote only if operationally better
  → Deploy → Observe again
```

The agent is therefore designed to improve from **measured repair outcomes**, not from unverified self-generated conclusions.

## Implementation status

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

### Operational dependencies

These are intentionally listed separately because code cannot substitute for live infrastructure:

- [ ] real GitHub token/App credentials
- [ ] production PostgreSQL
- [ ] production Redis
- [ ] Docker daemon or stronger sandbox provider
- [ ] LLM provider credentials / local model
- [ ] deployed OpenTelemetry collector / Langfuse backend
- [ ] installed Gitleaks/Semgrep/Trivy/CodeQL binaries where those adapters are enabled
- [ ] human reviewer identity/approval integration

### Production hardening roadmap

- [ ] microVM-grade execution backend for high-risk hostile workloads
- [ ] full GitHub App + webhook → queue → repair → PR lifecycle
- [ ] 100+ benchmark cases with reproducible raw evidence
- [ ] adversarial prompt-injection and repository-escape campaign
- [ ] learned model/strategy routing with held-out evaluation
- [ ] multi-tenant hosted control plane
- [ ] artifact attestations / stronger software supply-chain provenance

This section is the **implementation status**, not a claim that every deployment dependency is already live. The rule is simple: code is marked built when it exists and is tested; operational capabilities are marked live only after the required environment and acceptance tests exist.

## Product path

**Open-source repair engine → hosted repair platform → team governance/security → enterprise/on-prem execution → repair benchmark/evaluation platform.**

The moat is the combination of **repair traces + benchmark corpus + policy engine + verification evidence + deployment feedback**, not merely the prompt or model.

## Security

Read `SECURITY.md` and `v2/docs/THREAT_MODEL.md` before enabling autonomous PR publication. For public repositories, prefer ephemeral hosted or stronger isolated execution rather than persistent self-hosted runners; GitHub explicitly warns about the risk of untrusted code on self-hosted runners. citeturn0search0

## License

Apache-2.0
