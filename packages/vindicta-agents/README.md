> **Part of the [Vindicta Platform](https://github.com/vindicta-platform)**

# Vindicta Agents

> 📢 **Notice:** This repository is a Component Submodule of the Vindicta Platform Monorepo. For local development, testing, and dependency resolution, please clone the root [vindicta-platform](https://github.com/vindicta-platform/vindicta-platform) repository.


SDKs, Workflows, and Swarm for the Vindicta Platform.

## Installation

```bash
uv sync
```

## Features

- **Agent SDK**: Base classes and protocol for Vindicta Agents.
- **Swarm Management**: Coordination and orchestration logic via `Nexus`.
- **Governance**: Constitutional enforcement via `Axiomatic Supervisor`.
- **Flight Recorder**: SQLite-based auditing of all swarm events.

## Architecture

```mermaid
graph TD
    A[Agent (Tech-Priest)] -->|WebSocket/JSON-RPC| N[Nexus Orchestrator]
    N -->|State Transition| S[Axiomatic Supervisor]
    S -->|Validate| C[Constitution (Axioms)]
    S -->|Update| M[Shared Memory (Board State)]
    S -->|Log| L[(Flight Recorder DB)]
```

## Domain Boundaries

The Vindicta ecosystem is divided into two primary domains:

- **Meta-Agents (The Builders)**: Agents like the ADL, Architect, and SSE that build and maintain the platform. Governed by the [Vindicta Agents Constitution](.specify/memory/constitution.md).
- **Platform Agents (The Runtime)**: The Nexus Orchestrator and Axiomatic Supervisor that manage agent swarms and validate state transitions against the [Zero-Order Axioms](src/vindicta_agents/foundation/axioms.py).

For a detailed breakdown, see the [Architecture Guide](docs/architecture.md).

## Testing & Coverage

```bash
uv run pytest --cov
uv run behave
```
Coverage Mandate: ≥90%

## Docs

- [Architecture & Standards](https://github.com/vindicta-platform/vindicta-foundation)
- [Workflow Guide](docs/index.md)
