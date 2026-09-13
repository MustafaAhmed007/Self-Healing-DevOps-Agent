# Self-Healing DevOps Agent

> **A sandboxed AI coding agent for autonomous software repair: investigate GitHub issues, reproduce failures, generate bounded patches, run security and regression gates, and open evidence-backed pull requests.**

[![CI](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions)

**GitHub issue → immutable checkout → reproduce → research → diagnose → bounded patch → policy → security → verify → evidence → PR**

This is an engineering reference architecture for **self-healing DevOps, autonomous software repair, AI coding agents, AIOps/DevSecOps automation, and repository-aware debugging**. Model confidence is never treated as proof: repairs are constrained, reproducible, independently verified, and reviewable.

## Install and verify

The repository has a one-command setup path that creates the virtual environment, installs dependencies, runs the test suite, and only then reports success.

**Windows — double-click friendly**

```bat
install.bat
```

**Windows PowerShell**

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

**Linux / macOS**

```bash
bash install.sh
```

The installers require Python 3.11+. They intentionally do not pretend that external infrastructure such as Docker, PostgreSQL, Redis, GitHub credentials, or an LLM can be provisioned without its own environment requirements.

For a normal development install:

```bash
cd v2
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m app.cli demo
```

The root `pyproject.toml` now targets the same authoritative `v2` runtime, so `pip install -e '.[dev]'` from the repository root is also supported.

## Multi-aspect auto-research

Repair can gather evidence through independent paths rather than depending on one search vendor:

```text
                    Research question
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Optional cloud   Direct URLs   Local repository
          endpoint       retrieval       evidence
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Deduplicated context
                           ▼
                   Evidence-driven diagnosis
```

- **Optional cloud search:** configure `SHDA_RESEARCH_URL` with a compatible JSON endpoint.
- **Direct URL fallback:** use `--url` for authoritative public documentation or references.
- **Local fallback:** repository source and documentation are searched locally when external research is unavailable.
- **Multiple aspects:** problem, implementation, verification, and security are the default dimensions.
- **Security boundary:** direct URL retrieval rejects malformed, credential-bearing, localhost, private, loopback, link-local, reserved, multicast, and unspecified destinations. Research is context—not an authority that can bypass policy or verification.

Example:

```bash
cd v2
python -m app.cli research \
  "How should this failure be fixed safely?" \
  --repo . \
  --aspect problem \
  --aspect implementation \
  --aspect verification \
  --aspect security \
  --url https://docs.python.org/3/
```

During repair, direct sources can be supplied with `SHDA_RESEARCH_URLS` (comma-separated). The repair engine gathers research before diagnosis and records a research event in the evidence ledger.

## Runnable examples

```bash
# deterministic health/demo
cd v2
python -m app.cli demo

# local evidence research
python -m app.cli research "Python dependency failure" --repo .

# executable benchmark fixtures
python -m evals.harness --output evals/reports/latest.json

# repair workflow
python -m app.cli repair OWNER/REPO ISSUE_NUMBER --repro python -m pytest -q

# API
uvicorn app.api:app --reload
```

Complete local infrastructure:

```bash
cd v2
docker compose up --build
```

## System architecture

```text
                         CONTROL PLANE
             API / CLI / jobs / approvals / evidence
                              │
                              ▼
 Issue → immutable checkout → baseline reproduction
                              │
                              ▼
                       MULTI-ASPECT RESEARCH
                  cloud? → URLs → local repository
                              │
                              ▼
                     INTELLIGENCE PLANE
                  diagnosis → bounded patch
                              │
                              ▼
                      EXECUTION + POLICY
             sandbox / resource limits / diff gates
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
          SECURITY GATES             VERIFICATION
                 │                         │
                 └────────────┬────────────┘
                              ▼
                       EVIDENCE + AUDIT
                              │
                              ▼
                    REVIEWABLE PR / STOP
```

### Control plane
FastAPI, CLI, lifecycle, approvals, checkpoints, evidence, PostgreSQL and Redis integration surfaces.

### Intelligence plane
Provider-neutral LLM gateway, optional LiteLLM/LangGraph integration, local-model path, evidence-first diagnosis, bounded reflection, and research context.

### Execution plane
Immutable Git checkout, local/Docker sandbox, resource/network/capability controls, deterministic command/path policy, bounded diffs, and stronger-isolation extension points.

### Verification plane
Baseline reproduction, project tests, compile checks, regression verification, security scanner adapters, and independent verification.

### Delivery plane
Branch creation, commit, PR publication, evidence summary, and approval gates. Normal operation does not mutate the default branch.

### Observability plane
Structured events, evidence manifests, trace/metric hooks, model/tool cost metadata, and OpenTelemetry/Langfuse/Prometheus/Grafana-compatible paths.

## Repository layout

```text
.
├── install.bat / install.ps1 / install.sh
├── pyproject.toml                 # root metadata targeting authoritative v0.3 runtime
├── README.md
├── SECURITY.md
├── docs/
│   ├── DISCOVERABILITY.md
│   ├── SIA_CORE_ALIGNMENT.md
│   ├── architecture.md
│   ├── evaluation.md
│   ├── flow.md
│   ├── operations.md
│   ├── security.md
│   └── threat-model.md
├── .github/workflows/
│   ├── ci.yml
│   └── security.yml
└── v2/                            # historical workspace name; authoritative v0.3 implementation
    ├── app/                       # API, engine, policy, sandbox, research, verification, etc.
    ├── evals/                     # executable benchmark harness and fixtures
    ├── tests/                     # unit, security, adversarial and regression tests
    ├── console/                   # operator UI
    ├── infra/                     # persistence/observability infrastructure
    ├── docs/                      # implementation-specific architecture and threat docs
    ├── install.py
    ├── Dockerfile
    ├── docker-compose.yml
    └── pyproject.toml
```

The obsolete root `app/`, `packages/`, `web/`, database schema, root Dockerfile/Compose stack, and root Makefile were removed because they represented an older pre-v0.3 architecture and were not part of the authoritative runtime.

## Safety contract

The default policy is conservative:

- no default-branch mutation
- no empty commands
- block privileged/container-host escape flags
- block path traversal and absolute patch paths
- block secrets/private-key/protected files
- bound changed files/lines, commands, runtime, iterations, and model cost
- no network and no credentials in the default Docker repair boundary
- explicit approval for high-risk paths
- provenance before mutation
- fail closed when a required gate cannot run

For hostile public-repository workloads, microVM-grade isolation remains the production hardening path. A normal container is defence in depth, not VM-equivalent isolation.

## End-to-end repair contract

A successful run must preserve:

- run ID and timestamps
- issue and repository identity
- exact resolved revision
- baseline reproduction result
- bounded command outputs
- diagnosis and supporting evidence
- proposed diff and policy decision
- security gate results
- verification results
- bounded reflection history
- final commit/PR information when publication is enabled
- machine-readable evidence manifest

A model saying “fixed” is never sufficient.

## Evaluation

The executable benchmark layer measures:

- Issue Resolution Rate
- Patch Acceptance Rate
- Regression Rate
- False Fix Rate
- iterations per issue
- latency
- command count
- security gate outcomes
- model/tool cost metadata when available

Current fixture benchmarks are deterministic engineering verification, **not proof of real-world autonomous repair performance**. Production claims require reproducible raw reports.

## Self-improvement loop

```text
Run → Observe → Classify failure → Preserve evidence
  → Compare strategy/model/tool choice
  → Evaluate on held-out cases
  → Promote only if better
  → Deploy → Observe again
```

The compounding asset is the repair evidence and benchmark corpus: measured outcomes can improve policy, routing, verification, and future repair strategies.

## Implementation status

### Built and executable

- [x] typed repair state and budgets
- [x] GitHub issue acquisition and immutable checkout
- [x] provenance capture
- [x] local and Docker sandbox adapters
- [x] deterministic command/path/diff policy
- [x] security scanner interfaces
- [x] baseline reproduction and independent verification
- [x] bounded reflection
- [x] checkpoints and evidence/audit manifests
- [x] PostgreSQL/Redis integration surfaces
- [x] structured LLM gateway
- [x] branch/commit/PR publisher
- [x] approval/risk model
- [x] executable benchmark harness
- [x] API + CLI
- [x] operator console
- [x] Docker/Compose stack under `v2/`
- [x] one-command installation and post-install test verification
- [x] multi-aspect research with cloud/direct-URL/local fallback
- [x] SSRF-oriented direct URL validation
- [x] CI/security workflow verification surfaces

### External operational dependencies

- GitHub App/token credentials
- Docker daemon or stronger sandbox provider
- LLM provider credentials or local model
- PostgreSQL/Redis for durable distributed operation
- observability backends when enabled
- scanner binaries when those adapters are enabled
- human approval/reviewer integration for governed deployments

### Production hardening

- microVM-grade execution backend
- GitHub App + webhook → queue → repair → PR lifecycle
- 100+ benchmark cases with raw evidence
- adversarial prompt-injection/repository-escape campaign
- held-out learned model/strategy routing
- multi-tenant hosted control plane
- artifact attestations and stronger supply-chain provenance

## Who this is for

- **Developers:** automate repetitive bug investigation and regression repair.
- **SRE / platform teams:** experiment with bounded automated remediation and AIOps workflows.
- **DevSecOps teams:** combine coding agents with policy, security scanning, provenance, and verification.
- **AI-agent builders:** study repository-aware, sandboxed autonomous coding architecture.
- **Researchers:** run reproducible repair experiments instead of relying on unverifiable claims.

## Technology stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.11+ |
| API | FastAPI + Uvicorn |
| Contracts | Pydantic v2 |
| Agent orchestration | LangGraph boundary |
| Model routing | LiteLLM-compatible + Ollama-compatible local path |
| Research | Optional cloud endpoint + direct URL + local retrieval |
| Persistence | PostgreSQL + psycopg |
| Queue | Redis |
| Sandbox | Docker; stronger Firecracker/Kata/gVisor-class path |
| SCM | Git + GitHub API |
| Verification | pytest + project-native commands |
| Security | Gitleaks / Semgrep / Trivy / CodeQL adapters |
| Observability | OpenTelemetry + Langfuse-compatible path |
| UI | Next.js / React console |
| Delivery | Docker Compose + GitHub Actions |
| Evaluation | Executable benchmark harness |

## Product path

**Open-source repair engine → hosted repair platform → team governance/security → enterprise/on-prem execution → repair benchmark/evaluation platform.**

The defensible asset is the combination of **repair traces, benchmark corpus, policy engine, verification evidence, and deployment feedback**—not a prompt alone.

## Security

Read `SECURITY.md` and `v2/docs/THREAT_MODEL.md` before enabling autonomous PR publication. Repository content, issue text, model output, research results, and tool output are all treated as untrusted data.

## License

Apache-2.0
