<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║                SYNC IMPACT REPORT                           ║
  ╠══════════════════════════════════════════════════════════════╣
  ║ Version Change: 1.0.0 → 1.1.0 (MINOR)                     ║
  ║ Bump Rationale: Two new principles added, new Development   ║
  ║   Workflow section, and materially expanded Governance.      ║
  ║                                                              ║
  ║ Modified Principles:                                         ║
  ║   - IV. Zero-Issue Stability — wording tightened             ║
  ║   - Quality Gate 2 — strengthened to ≥90% coverage mandate   ║
  ║                                                              ║
  ║ Added Sections:                                              ║
  ║   + VI. Axiom-Driven Design (derived from axioms.py)         ║
  ║   + VII. Agent-First Architecture (derived from repo scope)  ║
  ║   + Development Workflow (aligned with platform constitution)║
  ║   + Governance: Amendment Procedure & Versioning Policy      ║
  ║   + Governance: Compliance Review Expectations               ║
  ║                                                              ║
  ║ Removed Sections: (none)                                     ║
  ║                                                              ║
  ║ Templates Requiring Updates:                                 ║
  ║   ✅ plan-template.md — Constitution Check aligns with       ║
  ║      updated principles (generic gate; no update needed)     ║
  ║   ✅ spec-template.md — scope/requirements structure intact  ║
  ║   ✅ tasks-template.md — task categorization unchanged       ║
  ║   ✅ checklist-template.md — generic; no update needed       ║
  ║                                                              ║
  ║ Follow-up TODOs: (none)                                     ║
  ╚══════════════════════════════════════════════════════════════╝
-->

# Vindicta Agents Constitution

## Core Principles

### I. MCP-First Mandate

Always check for available MCP servers (GitHub, CloudRun, Firebase,
filesystem) before using CLI tools or manual scripts. For all GitHub,
GCP, or Firebase operations, agents MUST utilize the corresponding MCP
tools. Manual CLI usage is a fallback only when MCP capabilities are
exhausted.

### II. Spec-Driven Development (SDD)

Every feature implementation MUST start with an SDD bundle in
`.specify/specs/[ID]-[name]/`. This bundle MUST include `spec.md`,
`plan.md`, and `tasks.md`. Implementation MUST NOT proceed until the
SDD bundle is approved and merged into the main branch.

### III. Economic Prime Directive

All platform architecture and implementation MUST strictly comply with
the GCP Free Tier. Scaling beyond free tier limits requires an explicit
architectural review and documented justification.

### IV. Zero-Issue Stability

System stability and technical debt resolution take precedence over new
feature development. When the "Repo-Guard" audit reveals high issue
density or critical debt, the organization MUST shift into a
stabilization phase to restore and maintain a "Zero-Issue State."

### V. Vanilla-Forward & Modern Tooling

Favor vanilla JavaScript (ES2020+) and modern build systems (Vite 7+)
over heavy frameworks. Maintain compatibility with Firebase SDK v10+ and
leverage GitHub Actions for all CI/CD pipelines.

### VI. Axiom-Driven Design

All domain models and validation logic MUST trace back to the Zero-Order
Axioms codified in `src/vindicta_agents/foundation/axioms.py`. The four
Axioms are:

- **AX-01 Entity Identity**: Every object MUST have a unique, immutable
  UUID. State is a function of time.
- **AX-02 Dimensionality**: All spatial coordinates exist in a 3D
  Euclidean space within defined bounds (44×60″). Negative or
  out-of-bounds values are Constitutional Violations.
- **AX-03 Probability Source**: All random outcomes MUST be traceable to
  a central Entropy Provider.
- **AX-04 Temporal Discretization**: The system operates in discrete
  integer-valued phases. Fractional phases are Constitutional Violations.

The Constitutional Middleware (`core/middleware.py`) MUST validate all
proposed intents against these Axioms before execution.

### VII. Agent-First Architecture

This repository is the canonical home for agent SDKs, swarm
orchestration, and agentic workflows. All agent definitions MUST reside
in `agents/` with a corresponding `AGENT.md`. The `BaseAgent` protocol
in `src/vindicta_agents/core/base_agent.py` defines the contract that
every agent implementation MUST satisfy.

## Development Workflow

1. **Specify**: Tech-agnostic user stories and acceptance criteria.
2. **Clarify**: Three-cycle clarification (Ambiguity, Component Impact,
   Failure Mode).
3. **Plan**: Technical architecture, file changes, and risk assessment.
4. **Tasks**: Dependency-ordered (MODELS → SERVICES → ENDPOINTS) task
   list with user-story traceability.
5. **Implement**: Atomic TDD commits (Red-Green-Refactor).
6. **Verify**: Verification checklist with evidence.

## Quality Gates

1. **Linting & Formatting**: All commits MUST pass pre-commit hooks,
   `ruff` checks, and `mypy --strict` type checking.
2. **Test Coverage**: Code coverage MUST meet or exceed 90%
   (`fail_under = 90` in `pyproject.toml`). Critical paths MUST have
   associated unit and BDD feature tests (`behave`).
3. **Link Integrity**: Documentation MUST pass markdown link validation
   at all tiers.
4. **Agent Context**: Every repository MUST contain up-to-date
   `.antigravity/` context artifacts (`ARCHITECTURE.md`,
   `CONSTRAINTS.md`).

## Governance

This constitution supersedes all individual repository practices for the
Vindicta-Agents repository and MUST remain aligned with the Vindicta
Platform Constitution (ratified v1.0.0, 2026-02-06).

### Amendment Procedure

1. Proposed amendments MUST be documented in a pull request against this
   file.
2. Amendments require approval from the Platform Lead.
3. Each amendment MUST include a migration plan if existing code or
   workflows are affected.
4. The Sync Impact Report (HTML comment at the top of this file) MUST be
   updated to reflect the change.

### Versioning Policy

- **MAJOR**: Backward-incompatible governance or principle removals /
  redefinitions.
- **MINOR**: New principle or section added, or materially expanded
  guidance.
- **PATCH**: Clarifications, wording, typo fixes, non-semantic
  refinements.

### Compliance Review

All pull requests and code reviews MUST verify compliance with the
principles above. Complexity that violates a principle MUST be justified
in the PR description. Periodic audits (aligned with the Repo-Guard
initiative) confirm ongoing adherence.

**Version**: 1.1.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-10
