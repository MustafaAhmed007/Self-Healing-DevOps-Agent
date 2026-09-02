# V2 Security Contract

The repair worker assumes repository source, issue bodies, READMEs, tests, build scripts and dependency metadata are hostile inputs.

## Hard boundaries

1. Never mount host secrets into a repair sandbox.
2. Network is disabled by default.
3. Sandbox commands run as a non-root user with dropped Linux capabilities and `no-new-privileges`.
4. CPU, memory, PID and wall-clock budgets are mandatory.
5. Protected paths include CI workflows, environment files and private-key extensions.
6. Dependency and workflow changes require explicit policy approval.
7. Default branches are never mutated by the repair worker.
8. LLM output is data until validated by deterministic policy.
9. A model claim of success is never sufficient; tests and independent verification are required.
10. Sandbox escape or policy violation terminates the run.

## Production note

Docker is the first sandbox provider, not a claim of perfect isolation. High-risk multi-tenant deployments should use a stronger isolation layer such as a microVM runtime and dedicated worker hosts.
