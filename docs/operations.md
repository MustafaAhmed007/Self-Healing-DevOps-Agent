# Operations

## Local stack

Use `docker compose up -d` for PostgreSQL, Redis and optional Ollama.

## Production principles

- Separate control-plane and execution workers.
- Give workers only the GitHub permissions they need.
- Store secrets in a secret manager, never repository files.
- Use ephemeral sandboxes and destroy them after every run.
- Keep model, prompt, policy and sandbox versions in run provenance.
- Persist checkpoints and large artifacts separately from hot state.
- Alert on sandbox violations, budget exhaustion and repeated repair failures.

## Recovery

A repair run is resumable from its last durable checkpoint. If a sandbox disappears, recreate it from the immutable repository commit rather than trusting mutable workspace state.

## Cost control

Route classification and summarization to inexpensive/local models; reserve stronger reasoning/coding models for diagnosis and patch generation. Stop immediately when token, cost, time or iteration budgets are exceeded.
