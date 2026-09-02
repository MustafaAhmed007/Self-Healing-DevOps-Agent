# Build Ledger

This is the canonical implementation ledger. **Built** means code/configuration plus a meaningful test or usage path exists. **Operational** means the external provider/infrastructure has been configured and a live acceptance test has passed.

## v0.1 — foundation

- [x] Mission, architecture and safety model
- [x] Initial API/CLI/infrastructure/evaluation structure

## v0.2 — vertical slice

- [x] Typed repair state and bounded budgets
- [x] GitHub issue acquisition and repository checkout
- [x] Local + Docker execution adapters
- [x] Network/resource/capability restrictions
- [x] Deterministic command/path policy
- [x] LLM gateway boundary
- [x] Diagnosis/patch/verification flow
- [x] PR publisher
- [x] Checkpoint/evidence foundation

## v0.3 — complete reference implementation surfaces

- [x] Provenance capture and resolved revision metadata
- [x] Bounded file patch application + unified diff generation
- [x] Secret scanner + Gitleaks/Semgrep/Trivy adapters
- [x] Baseline reproduction and independent verification
- [x] Bounded reflection loop driven by observed failures
- [x] PostgreSQL persistence adapter
- [x] Redis queue adapter
- [x] LangGraph checkpoint-capable orchestration boundary
- [x] Append-only evidence ledger + hashed manifests
- [x] Human approval state model/API
- [x] Secure Git push authentication without token in argv/remotes
- [x] FastAPI lifecycle endpoints
- [x] CLI
- [x] Executable benchmark fixtures and raw report writer
- [x] Operator console
- [x] Docker Compose local stack
- [x] CI + dependency audit workflow
- [x] Architecture/threat/operations documentation surfaces

## Operational acceptance still required

These cannot honestly be marked operational until their external dependencies are configured and evidence is retained:

- [ ] Real GitHub App/token + disposable-repository PR acceptance test
- [ ] Docker sandbox acceptance on a hardened host
- [ ] PostgreSQL persistence/recovery under process restart
- [ ] Redis queue/worker restart semantics
- [ ] LLM provider/local model repair measurements
- [ ] OpenTelemetry/Langfuse live traces
- [ ] Gitleaks/Semgrep/Trivy installed and exercised against fixtures
- [ ] High-risk approval + persistent resume workflow
- [ ] 100+ case benchmark with retained raw results
- [ ] Stronger microVM sandbox backend
- [ ] GitHub App/webhook ingestion
- [ ] Adversarial prompt-injection/repository-escape suite
- [ ] Multi-tenant isolation/load testing

## Evidence rule

Never label an unexecuted benchmark metric as measured. Never label an external integration operational until a live acceptance test produces retained evidence.
