# Self-Healing DevOps Agent

> **A sandboxed AI coding agent for autonomous software repair: investigate GitHub issues, reproduce failures, generate bounded patches, run security and regression gates, and open evidence-backed pull requests.**

[![CI](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/MustafaAhmed007/Self-Healing-DevOps-Agent/actions)

**GitHub issue → immutable checkout → reproduce → research → diagnose → bounded patch → policy → security → verify → evidence → PR**

This is an engineering reference architecture for **self-healing DevOps, autonomous software repair, AI coding agents, AIOps/DevSecOps automation, and repository-aware debugging**. It is designed around one rule: **model confidence is not proof**. Every repair must be constrained, reproducible, independently verified, and reviewable.

## Try it without a week of setup

The repository now has a **one-command installation and verification path**. It creates the virtual environment, installs the development dependencies, runs the test suite, and leaves the project ready to use.

**Windows PowerShell**

```powershell
./install.ps1
```

**Linux / macOS**

```bash
./install.sh
```

Or from `v2/`:

```bash
python install.py
```

After installation:

```bash
cd v2
.venv/bin/python -m app.cli demo       # Linux/macOS
# .venv/Scripts/python.exe -m app.cli demo  # Windows
```

The installer removes the repeated dependency/debugging work that commonly makes AI-agent repositories painful to evaluate. It does not pretend that external infrastructure such as GitHub credentials, an LLM, Docker, PostgreSQL, or Redis can be installed without their own system requirements.

## 60-second local path

```bash
cd v2
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m app.cli demo
```

Complete local stack:

```bash
cd v2
docker compose up --build
```

## Multi-aspect auto-research

Repair should not depend on a single search vendor. SHDA now has an **evidence-first multi-aspect research layer** with three paths:

```text
                  Research question
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
        Optional      Direct URL   Local repo
        cloud search   retrieval    evidence
             │           │           │
             └───────────┼───────────┘
                         ▼
                 Deduplicated evidence
                         ▼
                Diagnosis / verification
```

- **Optional cloud search:** set `SHDA_RESEARCH_URL` to a compatible JSON research endpoint. Cloud search is an accelerator, not a hard dependency.
- **Direct URL fallback:** pass one or more URLs to the research CLI when you already know the authoritative source.
- **Local/direct repository fallback:** relevant repository documentation and source files are searched locally, so research remains useful without a cloud search service.
- **Multiple aspects:** problem, implementation, verification, and security are the default research dimensions.
- **Evidence boundary:** research is context, not authority. The repair policy, sandbox, security gates, and independent verifier remain authoritative.

Example:

```bash
python -m app.cli research "How should this failure be fixed safely?" \
  --repo . \
  --aspect problem \
  --aspect implementation \
  --aspect verification \
  --aspect security \
  --url https://docs.python.org/3/
```

During an actual repair, configure direct sources with `SHDA_RESEARCH_URLS` (comma-separated) and optionally `SHDA_RESEARCH_URL`; the engine automatically gathers research before diagnosis and records a research event in the run evidence.

## What it actually builds

Most coding agents optimize for generating a plausible patch. This system optimizes for a **verifiable repair transaction**:

1. Acquire an issue and exact repository revision.
2. Reproduce the failure before mutation.
3. Gather multi-aspect evidence when available.
4. Diagnose from failure evidence, repository context, and research.
5. Generate a bounded patch rather than unrestricted workspace changes.
6. Apply deterministic policy and security gates.
7. Verify the change independently and check regressions.
8. Reflect only within a hard iteration budget.
9. Preserve an evidence/audit manifest.
10. Publish a reviewable PR only when policy permits.

## System architecture

```text
                         CONTROL PLANE
          API / CLI / jobs / approvals / persistence
                              │
                              ▼
 ISSUE ──► CONTEXT ──► IMMUTABLE CHECKOUT ──► RESEARCH
                              │                    │
                              └──────────┬─────────┘
                                         ▼
                               INTELLIGENCE PLANE
                         LLM gateway / diagnosis / patch
                                         │
                                         ▼
                               EXECUTION + POLICY
                         sandbox / commands / diff limits
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                         SECURITY GATES        VERIFICATION
                              │                     │
                              └──────────┬──────────┘
                                         ▼
                                  EVIDENCE + AUDIT
                                         │
                                         ▼
                                REVIEWABLE PR / STOP
```

### Control plane
FastAPI, CLI, job lifecycle, approvals, PostgreSQL/Redis integration surfaces, checkpoints, and evidence storage.

### Intelligence plane
Provider-neutral LLM gateway, optional LiteLLM/LangGraph integration, local-model path, evidence-first diagnosis, bounded reflection, and research context.

### Execution plane
Immutable Git checkout, local/Docker execution, resource/network controls, deterministic command/path policy, bounded diffs, and pluggable stronger isolation.

### Verification plane
Baseline reproduction, tests/compile checks, regression verification, secret/SAST/dependency scanning, and independent verification.

### Delivery plane
Branch creation, commit, PR publication, evidence summary, and approval gates. Default-branch mutation is not part of the normal repair path.

### Observability plane
Structured run events, evidence manifests, trace/metric hooks, model/tool cost metadata, and OpenTelemetry/Langfuse/Prometheus/Grafana-compatible paths.

## Repository architecture

```text
.
├── install.ps1 / install.sh       # one-command setup + verification
├── v2/
│   ├── app/
│   │   ├── api.py                 # HTTP control plane
│   │   ├── audit.py               # evidence ledger
│   │   ├── cli.py                 # operator CLI + research command
│   │   ├── config.py              # environment/runtime configuration
│   │   ├── engine.py              # repair state machine + research integration
│   │   ├── github.py               # issue/checkout/provenance
│   │   ├── llm.py                  # provider-neutral model gateway
│   │   ├── models.py               # typed domain state
│   │   ├── policy.py               # deterministic safety policy
│   │   ├── research.py             # cloud/direct-URL/local research
│   │   ├── sandbox.py              # local + Docker execution
│   │   ├── scanners.py             # security/dependency/SAST adapters
│   │   └── verify.py               # independent verification
│   ├── evals/                     # executable benchmark harness
│   ├── tests/                     # unit/security/integration tests
│   ├── docs/                      # architecture, threat model, operations
│   ├── console/                   # operator web console
│   ├── infra/                     # PostgreSQL, Redis, observability
│   ├── install.py                 # cross-platform installer
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── pyproject.toml
├── docs/DISCOVERABILITY.md        # organic search/discovery strategy
├── .github/workflows/             # CI/security workflows
├── SECURITY.md
└── LICENSE
```

`v2/` is a historical implementation workspace name. **The current release is v0.3.0.** It does not mean the project is currently “V2”. A future structural cleanup can flatten this workspace without changing the architecture contract.

## Safety contract

The default policy is deliberately conservative:

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

For hostile public-repository workloads, stronger isolation such as microVM-grade execution remains the production hardening path. A normal container is defence in depth, not a claim of VM-equivalent isolation.

## Runnable examples

### Deterministic health/demo

```bash
python -m app.cli demo
```

### Benchmark harness

```bash
python -m evals.harness --cases evals/cases --output evals/reports/latest.json
```

### Research without cloud search

```bash
python -m app.cli research "Python dependency failure" --repo .
```

### Research from authoritative URLs

```bash
python -m app.cli research "How does this API behave?" \
  --url https://docs.python.org/3/
```

### Repair workflow

```bash
python -m app.cli repair OWNER/REPO ISSUE_NUMBER --repro python -m pytest -q
```

### API

```bash
uvicorn app.api:app --reload
```

## Evaluation, not marketing

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

Fixture benchmarks are **engineering verification**, not proof of real-world autonomous repair success. No performance number should be presented as a production claim without a reproducible raw report.

## Self-improvement loop

```text
Run → Observe → Classify failure → Preserve evidence
  → Compare strategy/model/tool choice
  → Evaluate on held-out cases
  → Promote only if better
  → Deploy → Observe again
```

The compounding asset is the repair evidence and benchmark corpus: every measured outcome can improve policies, routing, verification, and future repair strategies.

## Who this is for

- **Developers:** automate repetitive bug investigation and regression repair.
- **SRE / platform teams:** experiment with bounded automated remediation and AIOps workflows.
- **DevSecOps teams:** combine coding agents with policy, security scanning, provenance, and verification.
- **AI-agent builders:** study a repository-aware, sandboxed autonomous coding architecture.
- **Researchers:** run reproducible repair experiments instead of relying on demo screenshots or unverifiable claims.

## Implementation status

### Substantially implemented and executable

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
- [x] executable benchmark fixtures/harness
- [x] API + CLI
- [x] operator console
- [x] Docker/Compose stack
- [x] one-command installation and post-install test verification
- [x] multi-aspect research with optional cloud + direct-URL + local fallback
- [x] CI/security workflow surfaces

### External operational dependencies

- GitHub App/token credentials
- Docker daemon or stronger sandbox provider
- LLM provider credentials or local model
- PostgreSQL/Redis for durable distributed operation
- observability backends when enabled
- scanner binaries when those adapters are enabled
- human approval/reviewer integration for governed deployments

### Production hardening roadmap

- microVM-grade execution backend
- GitHub App + webhook → queue → repair → PR lifecycle
- 100+ benchmark cases with raw evidence
- adversarial prompt-injection/repository-escape campaign
- held-out learned model/strategy routing
- multi-tenant hosted control plane
- artifact attestations and stronger supply-chain provenance

## Technology stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.11+ |
| API | FastAPI + Uvicorn |
| Contracts | Pydantic v2 |
| Agent orchestration | LangGraph boundary |
| Model routing | LiteLLM-compatible + Ollama-compatible local path |
| Research | Optional cloud endpoint + stdlib direct-URL + local repository retrieval |
| Persistence | PostgreSQL + psycopg |
| Queue | Redis |
| Sandbox | Docker; stronger Firecracker/Kata/gVisor-class path |
| SCM | Git + GitHub API |
| Verification | pytest + project-native commands |
| Security | Gitleaks / Semgrep / Trivy / CodeQL adapters |
| Observability | OpenTelemetry + Langfuse-compatible path |
| UI | Next.js / React |
| Delivery | Docker Compose + GitHub Actions |
| Evaluation | Executable benchmark harness |

## Product path

**Open-source repair engine → hosted repair platform → team governance/security → enterprise/on-prem execution → repair benchmark/evaluation platform.**

The defensible asset is not a prompt. It is the combination of **repair traces, benchmark corpus, policy engine, verification evidence, and deployment feedback**.

## Security

Read `SECURITY.md` and `v2/docs/THREAT_MODEL.md` before enabling autonomous PR publication. The project treats repository content, issue text, model output, research results, and tool output as untrusted data.

## License

Apache-2.0
