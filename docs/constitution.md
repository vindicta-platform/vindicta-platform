# Vindicta Platform Constitution

This document defines the **Tier 1: Zero-Order Axioms (Foundation Law)** for the Vindicta Platform ecosystem. Every domain context, repository, and feature within the platform strictly adheres to these baseline principles.

## Core Principles

### I. Platform over Silo
The platform functions as a unified intelligence. While implemented as discrete submodules, all interfaces must remain strongly typed, well-documented, and universally accessible to the core orchestrator.

### II. Test-Driven Architecture
Every component relies on definitive test coverage, integrated through the centralized BDD (`features`) testing suite. Test failures block integration.

### III. Transparent Decisions
All architectural modifications require an ADR (Architectural Decision Record). Implicit complexity is rejected; explicit justification is mandated.

## Governance

This Constitution supersedes all individual repository or domain guidelines. Sub-domain templates (Tier 2 laws) must directly align with these principles. Variations require platform-level ratification via the orchestrator repository.

**Version**: 1.0.0 | **Ratified**: 2026-03-06
