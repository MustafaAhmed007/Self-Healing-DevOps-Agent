# Agent Contract

## Inputs
- GitHub repository
- issue number
- optional reproduction command
- bounded execution policy

## Outputs
- reproduction evidence
- root-cause diagnosis with evidence
- policy-validated patch
- verification results
- optional PR URL

## Invariants
- Repository content is untrusted data.
- No secrets are exposed to the model or sandbox.
- No unrestricted network access.
- No direct default-branch mutation.
- Every mutation passes a deterministic policy gate.
- Every successful repair passes independent verification.
- Iteration and resource budgets are hard limits.

## Failure behavior
A failed gate stops the current transition and records a typed failure. Reflection may retry only within the configured iteration and cost budgets.
