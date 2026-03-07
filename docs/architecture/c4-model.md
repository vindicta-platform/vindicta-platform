# Architecture: C4 Model

## System Context
The Vindicta Platform orchestrates multiple discrete domains (Engine, Scribe, Economy, Oracle, Agents) to provide a unified Game AI and rule-resolution environment.

## Container Diagram
The platform integrates the following containers via the `uv` workspace and Git submodules:
- **Foundation**: Core data structures and constitutional interfaces.
- **Engine**: Physics and Monte Carlo Tree Search rule evaluations.
- **Scribe**: Immutable game state and action notation parsing.
- **Economy**: Token, quota, and meta-currency management.
- **Oracle**: LLM-driven embeddings and analysis.
- **Agents**: SDKs for external or deterministic swarm agent orchestration.

## Component / Code
*(See individual submodule documentation for localized component and code topologies.)*
