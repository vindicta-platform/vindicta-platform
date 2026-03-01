# ADR: Consolidation and Standardization of Vindicta Platform

## Status
Accepted

## Context
The Vindicta Platform currently consists of ~29 repositories. While this provides maximum isolation, it has led to significant DRY (Don't Repeat Yourself) violations and fragmented Domain-Driven Design (DDD). Basic entities like `DiceRoll`, `Unit`, and `Action` are redefined across multiple repositories. The Constitution Rule VII ("No cross-repo runtime dependencies") currently blocks the use of a shared library, forcing duplication.

## Objectives
1. **Enforce DRY**: Eliminate duplicate model definitions and redundant logic.
2. **Strengthen DDD**: Clearly define Bounded Contexts.
3. **Standardize**: Align all Python components on Pydantic V2, `uv`, and common interfaces.
4. **Reduce Overhead**: Consolidate "nano-repos" into cohesive domain-driven repositories.

## Domain Boundary Mapping (Proposed)

### 1. **Foundation Context (The "Lex")**
*   **Purpose**: Shared base models, interfaces, constitutional axioms, and **System Architecture**.
*   **Consolidated Repositories**: `Vindicta-Core`, `Atomic-Ledger-Py`, `devcontainers`, `.github`, `Platform-Docs`.
*   **Result**: `vindicta-foundation`
*   **Architecture Documentation**: `vindicta-foundation/docs/architecture` (ADRs, C4 Models, RFCs).

### 2. **Economic Context (The "Market")**
*   **Purpose**: Ledger management, quotas, infra cost control (Gas Tank).
*   **Consolidated Repositories**: `Economy-Engine`, `Quota-Manager`, `Metered-SaaS-Logic`, `Audit-Log-Pro`.
*   **Result**: `vindicta-economy`

### 3. **Mechanical Context (The "Physics")**
*   **Purpose**: Dice, entropy, combat results, 10th Ed logic.
*   **Consolidated Repositories**: `Dice-Engine`, `Entropy-Buffer`, `Primordia-AI` (core engine).
*   **Result**: `vindicta-engine`

### 4. **Notation Context (The "Scribe")**
*   **Purpose**: Wargame Notation System (WNS), parsing, and recording.
*   **Consolidated Repositories**: `WARScribe-Core`, `WARScribe-Parser`, `WARScribe-CLI`, `Battle-Transcript-Toolkit`.
*   **Result**: `warscribe-system`

### 5. **Predictive Context (The "Oracle")**
*   **Purpose**: Probability, statistics, and AI prediction.
*   **Consolidated Repositories**: `Meta-Oracle`, `Arbiter-Predictor`.
*   **Result**: `vindicta-oracle`

### 6. **Interface Context (The "Gateway")**
*   **Purpose**: User interfaces and public APIs.
*   **Consolidated Repositories**: `Vindicta-API`, `Vindicta-Portal`, `Logi-Slate-UI`.
*   **Result**: `vindicta-platform`

### 7. **Agent Context (The "Swarm")**
*   **Purpose**: Agent SDKs, workflows, and monitoring.
*   **Consolidated Repositories**: `Vindicta-Agents`, `Agent-Auditor-SDK`, `agent-repo`, `specify-repo`.
*   **Result**: `vindicta-agents`

## Technical Standardization
1.  **Pydantic V2**: All data models MUST inherit from a base class in `foundation`.
2.  **Strict Typing**: `mypy` strict mode enforced across all repos.
3.  **Library Distribution**: `vindicta-foundation` will be published as a private package (or git-referenced in `pyproject.toml`) to allow reuse without breaking "runtime" independence (each service still owns its `venv`).
4.  **Axiom-Driven Engineering (ADE)**: Core logic must be derived from constitutional axioms defined in `foundation`.

## Refactoring Plan
1.  **Phase 1 (Foundation)**: Merge `Vindicta-Core` and shared models. Establish the base `VindictaModel`.
2.  **Phase 2 (Physics & Scribe)**: Consolidate `Dice-Engine` and `WARScribe` modules. Align them with `foundation` models.
3.  **Phase 3 (Economy)**: Unify credit and quota systems into a single transactional ledger.
4.  **Phase 4 (Legacy Cleanup)**: Archive redundant "nano-repos". Update CI/CD pipelines.

## Consequences
*   **Pros**: Significantly reduced code duplication, faster cross-domain feature development, consistent data structures.
*   **Cons**: Requires initial effort to merge history (or fresh start), updates to many imports.
