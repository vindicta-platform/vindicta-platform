# Vindicta Foundation

**Shared core models, constitutional axioms, and architectural documentation for the Vindicta Platform.**

---

## The Shared Kernel

The `vindicta-foundation` repository is the **Single Source of Truth** for the entire Vindicta ecosystem. Every other repository in the platform depends on the models and axioms defined here.

## Core Pillars

### 📜 [The Constitution](constitution.md)
The supreme law governing the platform. It defines the Zero-Order Axioms (the physics of the simulation) and the First-Order Postulates (the abstract mechanics).

### 🏗️ [Architecture](architecture/overview.md)
The structural blueprint of the platform. This includes the [C4 Target State](architecture/C4-Target-State.md) and the [Consolidation Plan](architecture/adr/0005-consolidation.md) to migrate from 29 repositories to 7 specialized Meso-repos.

### 🧬 [Shared Models](https://github.com/vindicta-platform/vindicta-foundation/tree/main/src/vindicta_foundation/models)
Canonical Pydantic models for `Unit`, `DiceRoll`, `Action`, and `GameScore`. By sharing these models, we ensure perfect interoperability between the engine, the scribe, and the interface.

---

## Quick Links

- ⚖️ **[Read the Constitution](constitution.md)**
- 🗺️ **[System Architecture](architecture/overview.md)**
- 📜 **[WARScribe Notation](concepts/warscribe.md)**
- 📉 **[Cost Model](architecture/cost-model.md)**

---

## Meso-Repositories

Vindicta is organized into 7 domain-driven repositories:

| Repository                                                                          | Purpose               |
| ----------------------------------------------------------------------------------- | --------------------- |
| **[vindicta-foundation](https://github.com/vindicta-platform/vindicta-foundation)** | Shared Kernel & Truth |
| **[vindicta-engine](https://github.com/vindicta-platform/vindicta-engine)**         | Physics & Simulation  |
| **[warscribe-system](https://github.com/vindicta-platform/warscribe-system)**       | Notation & Game State |
| **[vindicta-economy](https://github.com/vindicta-platform/vindicta-economy)**       | Ledger & Quotas       |
| **[vindicta-oracle](https://github.com/vindicta-platform/vindicta-oracle)**         | Predictions & Meta    |
| **[vindicta-platform](https://github.com/vindicta-platform/vindicta-platform)**     | Identity & Interface  |
| **[vindicta-agents](https://github.com/vindicta-platform/vindicta-agents)**         | Swarm & Automation    |

---

*Built with 🎲 by the Vindicta Team. The foundation is the law.*
