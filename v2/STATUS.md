# V2 / V0.3 Status

## Implementation state

**Reference implementation surfaces: built.**

The repository now contains the end-to-end architecture and code surfaces for controlled repair: GitHub intake, provenance, sandboxing, diagnosis/patch gateway, policy, diff application, security gates, independent verification, bounded reflection, evidence, persistence adapters, queue adapter, PR publication, API, CLI, benchmark fixtures, console and CI.

## Operational state

**Not yet certified production-operational.** External credentials, infrastructure and hostile-environment acceptance tests are required. See `docs/BUILD_LEDGER.md`.

## Non-negotiable acceptance gate

A production release is not considered proven until a disposable repository demonstrates:

`issue → exact revision → reproduction → diagnosis → minimal patch → policy/security gates → verification → branch → PR → retained evidence`

and the benchmark/security suite produces raw reports.

This distinction is intentional: implementation completeness and deployment evidence are separate states.
