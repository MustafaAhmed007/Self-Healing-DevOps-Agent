# Architecture

## Control plane

FastAPI accepts repair requests and a worker executes a LangGraph-compatible state machine. PostgreSQL is the durable system of record; Redis is intended for queues, locks and transient coordination.

## Repair state machine

`LOAD_ISSUE → EXPLORE → REPRODUCE → DIAGNOSE → PATCH → POLICY_GATE → TEST → VERIFY → PR`

A failed test returns to reflection and a bounded retry. Budget and policy gates are deterministic and cannot be overridden by model output.

## Data plane

Repository code is treated as hostile input. Code execution happens in an ephemeral sandbox through a `Sandbox` interface. Docker is the initial provider; a future Firecracker/Kubernetes provider can implement the same contract.

## Evidence chain

Every diagnosis should be backed by reproduction output, source locations, tests or other concrete artifacts. Model confidence never constitutes proof of repair.

## Model routing

The intended production adapter is LiteLLM with Ollama as an offline/local provider. Models are selected by task class and can be evaluated on cost, latency and repair success.
