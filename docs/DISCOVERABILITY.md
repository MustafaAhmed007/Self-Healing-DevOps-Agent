# Discoverability, Search Intent & Community Growth

This document defines the project's public-language layer: the words developers, platform engineers, SREs, DevOps teams, security engineers, and AI builders are likely to use when searching for this class of software.

The goal is simple: make the project easy to understand, easy to find, easy to try, and easy to contribute to. Search language should describe real capabilities rather than manufacture claims.

## Core positioning

**Self-Healing DevOps Agent** is an evidence-driven autonomous software repair system for GitHub issues. It combines AI coding agents with reproducible debugging, sandboxed execution, deterministic policy gates, security scanning, independent verification, audit evidence, and pull-request delivery.

## High-value search vocabulary

### Primary terms

- self-healing DevOps
- self-healing software
- autonomous software repair
- autonomous debugging
- AI software repair
- AI coding agent
- agentic DevOps
- agentic software engineering
- autonomous coding agent
- autonomous code repair
- AI-powered bug fixing
- automated bug fixing
- automated software maintenance

### Developer and platform terms

- DevOps automation
- AIOps
- GitHub automation
- GitHub Actions automation
- GitHub issue automation
- pull request automation
- automated pull requests
- CI/CD automation
- continuous software repair
- developer productivity
- software engineering automation
- repository-aware coding agent
- code agent
- coding agents

### Reliability and SRE terms

- SRE automation
- incident remediation
- automated remediation
- reliability engineering
- production incident automation
- regression prevention
- failure diagnosis
- root cause analysis automation
- test-driven repair
- verification-first automation

### Security and trust terms

- secure coding agent
- sandboxed coding agent
- AI agent security
- autonomous agent security
- prompt injection defense
- repository security
- secure DevOps automation
- supply chain security
- software provenance
- audit trail
- policy-gated automation
- least privilege automation

### AI infrastructure terms

- LLM code agent
- LLM software engineering
- multi-model routing
- model routing
- local LLM coding agent
- Ollama coding agent
- LiteLLM agent
- LangGraph agent
- agent orchestration
- agent evaluation
- AI agent observability
- LLM observability

## Search-intent pages we should support

The repository should naturally answer questions such as:

- How do I automatically fix GitHub issues with AI?
- How can an AI coding agent safely modify a repository?
- How do I build a self-healing DevOps system?
- How can I sandbox an autonomous coding agent?
- How do I verify an AI-generated code fix?
- How do I automate bug fixing and pull requests?
- How do I build an autonomous software repair agent?
- How do I evaluate an AI coding agent?
- How do I protect repositories from prompt injection by coding agents?
- How do I run an AI developer agent with Docker isolation?

These phrases should appear where they are genuinely useful: README sections, tutorials, examples, benchmark descriptions, issue templates, architecture documents, and release notes. Avoid keyword stuffing.

## Natural contribution loops

The repository is designed so that useful developer actions create more useful public artifacts:

```text
Try the quickstart
      ↓
Run a benchmark / fixture
      ↓
Find an edge case
      ↓
Open an issue or improve a test
      ↓
Contribute a scanner / adapter / benchmark
      ↓
Document the result
      ↓
Release a reproducible improvement
```

This creates a practical open-source loop around **code + benchmarks + evidence + integrations + documentation**, rather than around promotional claims.

## Content surfaces

Future public documentation should prioritize:

1. **Quickstarts** — get from clone to first repair experiment quickly.
2. **Architecture guides** — explain the repair transaction and safety boundaries.
3. **How-to guides** — GitHub integration, Docker sandboxing, model providers, scanners, observability.
4. **Benchmark reports** — publish reproducible measurements and raw methodology.
5. **Failure reports** — document what the agent could not safely repair and why.
6. **Integration examples** — GitHub Actions, PostgreSQL, Redis, Ollama, LiteLLM, LangGraph, OpenTelemetry.
7. **Security research** — prompt injection, repository escape, secret exposure, malicious dependency, and supply-chain test cases.
8. **Release notes** — make meaningful technical changes easy to discover and reference.

## Metadata and repository classification

Use concise, capability-based repository metadata and GitHub topics. GitHub documents topics as a way to help people discover repositories and related projects, with a maximum of 20 topics and lowercase hyphenated topic names. citeturn0search2

Recommended topic set:

```text
ai
ai-agent
ai-coding-agent
aiops
autonomous-agents
autonomous-coding
autonomous-software-engineering
autonomous-software-repair
coding-agent
devops
devops-automation
github-actions
llm
llm-agents
self-healing
software-engineering
software-repair
sre
agentic-ai
python
```

Not every topic needs to be used forever. Keep only topics that accurately describe the repository.

## README language principles

The public README should:

- lead with the problem and outcome;
- use terminology developers actually search for;
- explain the architecture with concrete nouns;
- include runnable examples early;
- link concepts to implementation files;
- distinguish implemented features from roadmap items;
- publish measured results instead of invented performance claims;
- make contribution paths obvious;
- keep security limitations visible;
- avoid repetitive keyword stuffing.

GitHub's own documentation recommends writing for a defined audience, matching search intent, using relevant keywords in page copy and metadata, structuring content with clear headings, and maintaining accuracy. citeturn0search4turn0search6

## What should compound over time

The strongest long-term discovery assets are technical artifacts that other developers genuinely want to reference:

- reproducible benchmark datasets;
- repair traces and failure analyses;
- security test suites;
- reusable sandbox policies;
- model-routing evaluations;
- GitHub integration recipes;
- adapters for common languages and CI systems;
- architecture diagrams;
- tutorials and examples;
- real-world issue-to-PR case studies.

The objective is not to manufacture popularity. It is to make every useful contribution, benchmark, integration, and technical lesson easier for the next developer to discover and reuse.
