# Build Ledger

## v0.1 foundation
- Architecture and mission README
- Security principles and repository map
- Initial API/web/infrastructure/evaluation foundations

## v0.2 built
- Pydantic repair state, issue, diagnosis, patch and verification models
- Explicit iteration/runtime/cost/patch/command budgets
- GitHub issue API and repository checkout
- Local executor and Docker sandbox implementation
- Network-disabled Docker execution, dropped capabilities, non-root user, no-new-privileges, resource limits
- Deterministic path/command policy gate
- Optional LiteLLM diagnosis and patch generation
- Independent verification runner
- Issue-to-verify engine
- Verified branch/PR publisher
- FastAPI endpoint and CLI
- LangGraph graph boundary with bounded reflection route
- Portable checkpoint store
- Benchmark case schema and honest harness
- Unit tests
- Docker/Compose/requirements/env/CI
- V2 security contract

## Still required
### V2 completion
- Durable PostgreSQL persistence
- Redis-backed worker execution
- Full LangGraph checkpointer integration
- Real trace emission to Langfuse/OpenTelemetry
- Immutable commit checkout and provenance capture
- Patch/diff application rather than whole-file replacement only
- Real secret/static/dependency scanner adapters
- Human approval workflow for risky changes
- Robust reflection loop driven by failed-test evidence
- End-to-end PR test with a disposable fixture repository
- Actual benchmark execution and stored raw reports

### V3
- Next.js live console
- GitHub App/webhooks
- multi-language environment adapters
- stronger microVM sandbox provider
- benchmark expansion to 100+ cases
- adversarial security suite
- learned model routing and strategy promotion
- hosted multi-tenant control plane

## Evidence rule
A feature is marked built only when code and tests exist. A benchmark metric is marked measured only when the benchmark has actually run and its evidence is retained.
