# Vindicta Platform Orchestrator Overview

Welcome to the **Vindicta Platform** documentation — the unified orchestrator for all Vindicta domain contexts.

This repository serves as the mono-entry point for the [Vindicta Platform](https://github.com/vindicta-platform). Clone once, get all domain contexts as submodules, and run platform-wide integration tests or examples immediately.

## Quick Start

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform

# Sync the unified workspace dependencies
uv sync

# Run the examples
uv run examples/dice_roll.py
uv run examples/warscribe_actions.py
uv run examples/combat_sim.py

# Pull latest updates from all submodules
git submodule update --remote
```

## Repository Structure

```text
vindicta-platform/
├── packages/
│   ├── vindicta-foundation/   # Shared kernel: base models & architecture
│   ├── vindicta-engine/       # Physics, dice, and AI core
│   ├── warscribe-system/      # Notation parsing & game state
│   ├── vindicta-economy/      # Ledger, quotas, and gas tank
│   ├── vindicta-oracle/       # Predictive models and meta analysis
│   ├── vindicta-agents/       # Swarm Orchestration & SDKs
│   └── features/              # Centralized BDD Feature tests
├── examples/
│   ├── dice_roll.py           # 🎲 Roll dice with cryptographic proofs
│   ├── warscribe_actions.py   # 📜 Create & serialize game actions
│   └── combat_sim.py          # ⚔️ Full combat simulation
└── pyproject.toml             # uv workspace root
```

## Subsystems

The Vindicta Platform is composed of several specialized domains, each maintained in its own repository and brought together here via Git submodules.

| Domain | Submodule Path | Purpose |
| :--- | :--- | :--- |
| **Foundation** | `packages/vindicta-foundation/` | Core architecture, shared models, constitutional interfaces. |
| **Engine** | `packages/vindicta-engine/` | Physics core, dice engines, and AI foundation (e.g., MCTS). |
| **Scribe** | `packages/warscribe-system/` | Notation parsing and turn-based game state management. |
| **Economy** | `packages/vindicta-economy/` | Managed ledgers, resource quotas, and transaction "gas" tank. |
| **Oracle** | `packages/vindicta-oracle/` | Predictive models, analysis tools, and LLM integrations. |
| **Agents** | `packages/vindicta-agents/` | Orchestration SDKs for autonomous agent swarms. |

## Important Resources

- **GitHub Repository**: [vindicta-platform](https://github.com/vindicta-platform/vindicta-platform)
- **Foundation & Standards**: [vindicta-foundation](https://github.com/vindicta-platform/vindicta-foundation)
