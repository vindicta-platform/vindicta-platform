<!--
Sync Impact Report:
- Version Change: 1.1.0 → 1.1.1
- Modified Principles: None (Consistency refinement).
- Added Sections: None.
- Removed Sections: None.
- Templates requiring updates:
  - .specify/templates/plan-template.md (✅ updated - listed principles in Constitution Check)
  - .specify/templates/tasks-template.md (✅ updated - made tests mandatory)
  - .specify/templates/spec-template.md (✅ checked - already requires mandatory testing)
- Follow-up TODOs: None.
-->

# Vindicta Platform Constitution

## Core Principles

### I. Platform over Silo
The platform functions as a unified intelligence. While implemented as discrete submodules, all interfaces
MUST remain strongly typed, well-documented, and universally accessible to the core orchestrator.
Cross-package dependencies must be explicit and mediated through the `vindicta-foundation` models.

### II. Test-Driven Architecture
Every component MUST rely on definitive test coverage, integrated through the centralized BDD
(`features`) testing suite. Test failures in any submodule block integration into the platform.
New features are incomplete until verified by independent acceptance scenarios.

### III. Transparent Decisions
All architectural modifications REQUIRE an Architectural Decision Record (ADR). Implicit complexity is
rejected; explicit justification is mandated for any deviation from established patterns.
Decisions must be documented in `docs/architecture/adr/`.

### IV. Observability & Logging
Every feature MUST implement structured logging and observability hooks. Debuggability is a first-class
requirement; system state transitions and errors must be traceable without manual debugger
attachment. Use the platform's standardized logging utilities.

### V. Simplicity (YAGNI)
Reject speculative or "just-in-case" complexity. Implement only what is required by the current
feature specification. Code that does not directly serve a functional requirement or a mandated
architectural pattern should be removed.

## Additional Requirements

### Technology Stack
- **Python 3.12+**: Use modern features (type hints, `asyncio` where appropriate).
- **uv**: Primary package and workspace manager.
- **Ruff**: Mandatory for linting and formatting.
- **Mojo/Rust/Go**: Permitted for performance-critical kernels if justified by an ADR.

### Documentation Standards
- **MkDocs**: All documentation must be compatible with the root `mkdocs.yml`.
- **C4 Model**: Container and Component diagrams must be updated for structural changes.

## Development Workflow

### Feature Lifecycle
1. **Specify**: Define user stories and acceptance criteria in `/specs/`.
2. **Plan**: Technical research, data modeling, and task breakdown.
3. **Implement**: Test-first development with regular integration checks.
4. **Validate**: Verify against the original specification and platform benchmarks.

### Quality Gates
- **90% Coverage**: Mandatory for all new logic.
- **Type Safety**: No `Any` types without explicit justification.
- **Pre-commit**: All hooks must pass before code is submitted for review.

## Governance

This Constitution defines the mandatory requirements for all work within the Vindicta Platform.
Amendments require a formal proposal and ratification by the platform maintainers. Compliance is
verified during every feature implementation via the "Constitution Check" gate.

**Version**: 1.1.1 | **Ratified**: 2026-03-06 | **Last Amended**: 2026-03-07
