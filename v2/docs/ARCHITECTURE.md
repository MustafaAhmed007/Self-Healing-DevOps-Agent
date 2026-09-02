# Architecture

## Core transaction

`Issue → Context → Immutable Checkout → Reproduce → Diagnose → Patch → Gate → Verify → Reflect → Evidence → PR`

The control plane owns state and policy. The intelligence plane proposes actions. The execution plane performs only approved deterministic actions. The verification plane establishes whether the repair actually works.

## Control loops

### Repair loop

Observe failure → form hypothesis → produce minimal patch → run gates → verify → either publish or reflect.

### Security loop

Input → normalize → classify risk → deny dangerous actions → isolate execution → scan → verify → retain evidence.

### Learning loop

Run outcome → failure taxonomy → benchmark case → compare model/strategy/tool choices → held-out evaluation → promotion only on measured improvement.

## Trust boundaries

1. GitHub and issue content are external input.
2. Repository source is untrusted executable content.
3. LLM output is untrusted data.
4. Sandbox is the execution boundary.
5. Policy engine is the mutation authorization boundary.
6. Evidence ledger is the audit boundary.
7. PR publication is the final external side effect.

## Scaling path

Local process → Docker isolated worker → ephemeral VM/microVM worker → distributed Redis workers → hosted multi-tenant control plane.
