# Operations Runbook

## Local

1. `cp .env.example .env`
2. Configure `GITHUB_TOKEN` only if GitHub operations are required.
3. Keep `AUTO_PUBLISH_PR=false` while validating.
4. `docker compose up --build`.
5. Run `python -m pytest -q` and the benchmark harness.

## Production checklist

- Use a GitHub App with minimum repository permissions.
- Use ephemeral execution hosts for untrusted repositories.
- Do not expose the Docker socket to repair workloads.
- Use PostgreSQL with backups and TLS where appropriate.
- Use Redis with authentication/TLS where required.
- Store model/GitHub credentials in a secret manager.
- Export traces to OpenTelemetry/Langfuse without source secrets.
- Enable Gitleaks/Semgrep/Trivy and fail closed for required scanners.
- Require human approval for high-risk changes.
- Keep PR publication disabled until acceptance tests pass.
- Pin CI actions to immutable commit SHAs and use least-privilege permissions.
- Retain evidence manifests and raw benchmark reports.

## Incident response

If suspicious behavior is observed: stop PR publication, revoke/rotate credentials, preserve the run evidence, isolate the worker host, inspect the generated diff and command history, and only then resume service.
