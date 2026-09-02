# v0.2 Vertical Slice

The v0.2 slice is designed around one invariant: the agent may reason about untrusted repository content, but only deterministic policy-controlled tools may execute commands or mutate a workspace.

Flow: issue -> checkout -> inspect -> reproduce -> diagnose -> patch proposal -> policy gate -> apply -> verify -> bounded reflection.

This package is intentionally provider-neutral and can run without an LLM in `dry-run` mode for testing the control plane.
