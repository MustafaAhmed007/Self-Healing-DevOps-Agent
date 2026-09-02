# V2 Build Ledger

## Built
- Typed repair state and budgets
- GitHub issue/repository acquisition client
- Bounded command policy
- Docker sandbox with network disabled, non-root execution, dropped capabilities, no-new-privileges, CPU/memory/PID limits
- Local development executor
- Optional LiteLLM diagnosis/patch generation
- Independent verification runner
- Issue-to-verify repair engine
- Verified branch/PR publisher
- FastAPI endpoint
- CLI
- Evaluation case schema and harness
- Unit tests
- Container and Compose infrastructure
- CI workflow

## Remaining for V2 completion
- Real LangGraph StateGraph wiring and durable checkpointer
- PostgreSQL persistence and Redis worker queue
- Langfuse/OpenTelemetry trace emission
- Production GitHub App/webhook flow
- Robust immutable-commit checkout
- Docker image build/install lifecycle inside isolated sandbox
- Patch/diff parser instead of whole-file replacement only
- Secret scanning with Gitleaks/Trivy/Semgrep integration
- Dependency/config/workflow approval workflow
- Reflection node with bounded retries
- Real PR publication E2E test
- Real benchmark fixtures and measured results
- Security adversarial benchmark
- Next.js live run console

## Truth rule
No benchmark percentage is published until the harness executes real immutable cases and stores the raw evidence.
