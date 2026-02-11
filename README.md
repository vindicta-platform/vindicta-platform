# ⚔️ Vindicta Platform — Orchestrator

Mono-entry point for the [Vindicta Platform](https://github.com/vindicta-platform). Clone once, get all domain contexts as submodules, and run Hello World examples immediately.

## Quick Start

```bash
# Clone with all submodules
git clone --recurse-submodules https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform

# Install dependencies
uv sync

# Run the examples
uv run examples/dice_roll.py
uv run examples/warscribe_actions.py
uv run examples/combat_sim.py
```

## Repository Structure

```
vindicta-platform/
├── vindicta-foundation/   # Shared kernel: base models & architecture
├── vindicta-engine/       # Physics, dice, and AI core
├── warscribe-system/      # Notation parsing & game state
├── examples/
│   ├── dice_roll.py       # 🎲 Roll dice with cryptographic proofs
│   ├── warscribe_actions.py  # 📜 Create & serialize game actions
│   └── combat_sim.py      # ⚔️ Full combat simulation
└── pyproject.toml         # uv workspace root
```

## Submodules

| Domain | Submodule | Package |
|:-------|:----------|:--------|
| Foundation | `vindicta-foundation/` | `vindicta_foundation` |
| Engine | `vindicta-engine/` | `vindicta_engine` |
| Scribe | `warscribe-system/` | `warscribe` |

All submodules are wired as editable `uv` workspace members — changes to any submodule are immediately reflected.

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

---

*Built with 🎲 by the Vindicta Team*
