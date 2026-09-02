# Threat Model

## Assets

- source code and repository history
- GitHub credentials
- model/API credentials
- build and deployment infrastructure
- repair evidence
- developer trust and repository integrity

## Threats

| Threat | Control |
|---|---|
| Prompt injection in issue/repo | untrusted-data contract + deterministic tools |
| Arbitrary command execution | argv policy + sandbox |
| Container escape | non-root, dropped caps, no-new-privileges, seccomp, resource limits; stronger isolation planned |
| Secret exfiltration | no secrets in repair workspace + secret scanners |
| Malicious dependency | dependency audit + policy gate |
| Workflow tampering | protected workflow paths |
| Path traversal | resolved-path checks |
| Infinite agent loop | iteration/runtime/command/cost budgets |
| False fix | baseline reproduction + independent verification |
| Token exposure during push | askpass instead of token in remote/argv |
| Supply-chain compromise | least-privilege CI + pinned actions |
| Evidence tampering | append-only events + hashed manifest |

## Residual risk

Docker is treated as a practical isolation adapter, not a universal hostile-code boundary. For high-risk multi-tenant execution, use an ephemeral VM/microVM or equivalent stronger isolation layer and validate it with adversarial tests.

Never expose the Docker socket to repair code. Never place production credentials inside the repair workspace.
