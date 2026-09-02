# Repair Control Plane

```text
GitHub issue
  ↓
IssueAnalyzer
  ↓
RepositoryExplorer
  ↓
BugReproducer ── evidence ──→ CodeAnalyst
                                  ↓
                            PatchGenerator
                                  ↓
                             PolicyGate
                                  ↓
                              Sandbox
                                  ↓
                             TestRunner
                                  ↓
                         IndependentVerifier
                           ↙             ↘
                       PASS             FAIL
                        ↓                 ↓
                  PR Generator       Reflection
                                        ↓
                                   bounded retry
```

The graph is a state machine, not an unconstrained conversation. Every tool call is authorized by deterministic policy, every execution has resource limits, and every run has a bounded budget.
