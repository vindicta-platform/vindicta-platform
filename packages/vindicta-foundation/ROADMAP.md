# Vindicta Platform Roadmap

This roadmap tracks the development of the Vindicta Platform across all domain contexts.

## Vision
To build the most mechanically faithful, cryptographically secure, and accessible competitive wargaming platform in the world, running entirely on free-tier infrastructure.

---

## Phase 1: Foundation & Shared Kernel (COMPLETED)
- [x] Establish **Zero-Order Axioms** (Constitution).
- [x] Define canonical **Shared Models** (Unit, Roll, Score).
- [x] Consolidate 29 repositories into 7 specialized **Meso-repos**.
- [x] Implement **VindictaModel** base class for Pydantic V2.

## Phase 2: Mechanics & Notation (ACTIVE)
*The Foundation serves as the core dependency for all mechanical implementations.*
- [x] **WARScribe**: Finalize notation parsing for 10th Edition.
- [ ] **Dice Engine**: Implement CSPRNG with verifiable entropy proofs.
- [ ] **Combat Sim**: First end-to-end simulation of a full combat round.
- [x] **Documentation Migration**: Move truth source to `vindicta-foundation`.
- [x] **Stability Pass**: Harmonize ADRs and stabilize dev environments (Feb 2026).
    - [x] Minimal devcontainer (ADR-0008), YAGNI rules, retrospective docs.
    - [x] PR workflow standardization (body-file mandate).
    - [x] Ruff format enforcement in pre-flight checks.
- [ ] **CI Hardening**: Add `pytest-cov` dependency and configure GitHub Actions CI.

## Phase 3: Identity & Gateway
- [ ] **Portal Redesign**: Split-pane entry for Club and Platform.
- [ ] **Auth Consolidation**: Unified Firebase Auth across all subdomains.
- [ ] **API Gateway**: Central entry point via `vindicta-platform`.

## Phase 4: Economy & Oracle
- [ ] **Gas Tank Phase 1**: Atomic ledger for credit management.
- [ ] **Meta-Oracle**: First ML model for win-rate prediction based on WARScribe logs.
- [ ] **Quota Manager**: Service-level rate limiting to maintain free-tier viability.

## Phase 5: Agent Swarm
- [ ] **Agent SDK**: Release of the autonomous auditor SDK.
- [ ] **Swarm Control Plane**: Nexus for multi-agent coordination.
- [ ] **Autonomous Testing**: Agents routinely fuzzing the engine via WARScribe transcripts.

---

## Long-Term Goals
- **Tournament Mode**: Real-time integration with BCP/ITC.
- **Vision Integration**: OCR/Computer Vision for physical score-sheet ingestion.
- **Multi-System Support**: Expanding beyond 10th Ed to other tabletop systems.

---

*Last updated: 2026-02-21*
