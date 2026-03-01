# ⚔️ Vindicta Platform — Orchestrator

Mono-entry point for the [Vindicta Platform](https://github.com/vindicta-platform). Clone once, get all domain contexts as submodules, and run Hello World examples immediately.

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

## Capabilities

The platform is continuously evolving. Recent additions include:
- **Monte Carlo Tree Search (MCTS)**: Advanced Game AI capabilities across the platform.
- **RAG Pipeline**: Integrated LLM embeddings via MCP and ChromaDB.

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

## Submodules

| Domain     | Submodule                        |
| :--------- | :------------------------------- |
| Foundation | `packages/vindicta-foundation/`  |
| Engine     | `packages/vindicta-engine/`      |
| Scribe     | `packages/warscribe-system/`     |
| Economy    | `packages/vindicta-economy/`     |
| Oracle     | `packages/vindicta-oracle/`      |
| Agents     | `packages/vindicta-agents/`      |
| Features   | `packages/features/`             |

All submodules are wired as editable `uv` workspace members — changes to any submodule are immediately reflected across the entire platform.

## Documentation

> **📌 Important:** All architectural decisions, shared models, and the project Constitution live in [**vindicta-foundation**](https://github.com/vindicta-platform/vindicta-foundation).

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

---

*Built with 🎲 by the Vindicta Team*
