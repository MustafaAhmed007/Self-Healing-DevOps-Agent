# SIA CORE Ω — Portfolio Alignment

## Purpose

Self-Healing DevOps Agent is a domain implementation of the portfolio-wide SIA CORE Ω operating architecture:

**objective → context/research → evidence → strategy → bounded execution → verification → outcome → learning → next decision**

## Universal contract

| Capability | Status | Domain implementation |
|---|---|---|
| Objective / outcome contract | Implemented | Issue/repair state, budgets and acceptance criteria |
| Evidence + provenance | Implemented | Immutable checkout, audit ledger and evidence manifests |
| Multi-aspect research | Implemented | Problem, implementation, verification and security research |
| Deterministic core | Implemented | Policy, command/path/diff limits, bounded state machine |
| Intelligence/provider boundary | Implemented | Provider-neutral LLM gateway and local path |
| Economic routing | Partial | Model/tool cost metadata; add explicit value-aware escalation |
| Orchestration | Implemented | Repair state machine |
| Verification/release gates | Implemented | Reproduction, tests, regression, security and independent verification |
| Security/adversarial lane | Implemented | Sandbox/policy/scanners; expand adversarial campaign corpus |
| Runtime verification | Implemented | Reproduction and independent execution |
| Telemetry | Implemented | Structured events, traces and cost hooks |
| Benchmarking | Implemented | Executable repair benchmark harness |
| Experimentation | Partial | Compare repair strategies/models; formalize champion/challenger promotion |
| Outcome measurement | Partial | Resolution/acceptance/regression metrics; connect deployed outcomes |
| Causal learning | Planned | Intervention/control/outcome contracts |
| Genome / failure memory | Partial | Repair evidence corpus; normalize reusable failure/repair rules |
| One-click bootstrap / doctor | Implemented | Cross-platform install and post-install verification |
| Artifact evidence trail | Implemented | Audit/evidence manifests and benchmark reports |
| Adapter boundaries | Implemented | GitHub, LLM, research, sandbox, scanner and observability adapters |

## Domain boundary

Repository repair remains domain-specific: issue acquisition, immutable Git checkout, reproduction, patch generation, sandbox execution, policy enforcement, security scanning and PR publication.

## Non-negotiables

1. Model confidence is never proof.
2. Untrusted repository, issue, research and tool content must not become executable authority.
3. Mutation is bounded, policy-gated and reversible where possible.
4. Required verification failures stop delivery.
5. Production claims require raw reproducible evidence.

## Target end state

Adopt the portfolio SIA CORE Ω contracts for objective, evidence, research, intelligence routing, economics, verification, outcomes, experiments, learning and artifacts, while keeping repair-specific execution inside this repository.
