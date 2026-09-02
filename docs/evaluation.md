# Evaluation

The evaluation harness is intentionally separate from the repair runtime.

## Metrics

- Issue Resolution Rate
- Patch Acceptance Rate
- Regression Rate
- False Fix Rate
- Iterations / Issue
- Tokens / Issue
- Cost / Issue
- Median/P95 Latency
- Sandbox Violations
- Security-policy violations

## Reproducibility

Each case should pin an immutable repository commit and store the issue, reproduction command, environment and constraints. Hidden expected artifacts must never be mounted into the agent workspace.

## Benchmark policy

Never place guessed or illustrative performance numbers in the README. A benchmark result is published only after the harness actually executes the case set and records its provenance.

## Growth path

Start with a small, high-quality Python corpus, then expand to multi-language bugs, dependency failures, configuration bugs, security cases, flaky tests and adversarial repositories. Every production failure should be converted into a regression case where legally and ethically possible.
