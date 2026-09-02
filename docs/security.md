# Security Model

## Threat model

Assume issue text, README files, source files, tests, build scripts, package metadata and dependency installation hooks can be malicious.

## Rules

1. Repository content is data, never authority.
2. Sandbox execution is deny-by-default.
3. Network is disabled unless an explicit policy grants it.
4. Credentials are never mounted into repair containers.
5. Containers run without Linux capabilities and with `no-new-privileges`.
6. Resource limits are mandatory.
7. Protected paths require explicit policy approval.
8. Dependency changes are blocked by default.
9. Workflow/CI changes are blocked by default.
10. The default branch is never modified directly by the agent.

## Defense in depth

`input validation → untrusted-content boundary → policy engine → ephemeral sandbox → resource/network limits → secret scan → diff validation → tests → security scan → independent verification → human review`

## Future hardening

For high-risk multi-tenant production execution, replace or augment Docker with a stronger VM/microVM isolation backend, immutable worker images, egress proxying, signed artifacts, dedicated workers, SBOM/provenance, and centralized audit storage.

## Security reporting

Do not disclose vulnerabilities publicly before coordinated remediation. See `SECURITY.md` for reporting guidance.
