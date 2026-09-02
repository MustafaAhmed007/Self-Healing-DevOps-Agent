# Threat Model

| Threat | Control | Evidence |
|---|---|---|
| Prompt injection in repository | Content/authority boundary | security test |
| Secret exfiltration | no secret mounts + scans | security event |
| Network abuse | network none by default | sandbox policy |
| Resource exhaustion | CPU/memory/PID/time limits | sandbox event |
| Malicious patch | diff policy + verification | policy report |
| Dependency supply chain | dependency gate + scanner | security report |
| CI persistence | workflow path protected | policy report |
| False fix | reproduction + independent verification | verification report |
| Worker crash | checkpoint/resume | checkpoint record |

## Security invariant

No model output can directly grant itself capabilities. Capabilities are selected by deterministic policy before a tool executes.
