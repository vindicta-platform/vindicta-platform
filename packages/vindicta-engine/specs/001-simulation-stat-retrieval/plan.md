# Implementation Plan: Simulation Stat Retrieval

**Branch**: `001-simulation-stat-retrieval` | **Date**: 2026-02-23 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-simulation-stat-retrieval/spec.md`

## Summary

This feature adds asynchronous retrieval and caching of game statistics for the vindicta-engine. It integrates with the RAG server to natively parse markdown rules into distinct numeric `UnitProfile`, `WeaponStatLine`, and `StatModifier` Pydantic models using regex extraction heuristics and an embedded local async-safe LRU cache system to optimize Monte Carlo pipeline latencies.

## Technical Context

**Technical Setup & Integration**:
- **Domain Context**: Resides entirely within the `vindicta-engine` package domain.
- **Data Architecture**: Reads from `vindicta-foundation` schemas implicitly (requires `VindictaModel`).
- **Dependencies**: Depends on the MCP Client integration for requesting `search_40k_rules`.

**Language/Version**: Python 3.12+ (uv workspace)
**Primary Dependencies**: `pydantic` (models), `mcp` (MCP SDK for RAG server queries), `logging`
**Storage**: Embedded in-memory LRU cache
**Testing**: `pytest`, `pytest-asyncio`
**Target Platform**: Any system running the local MVP platform
**Performance Goals**: RAG latency lookup minimal constraints, cache lookups < 1ms
**Constraints**: 1 retry per RAG access. Cache invalidates structurally via rules versioning keys.

## Constitution Check
- [x] **I. Foundation Adherence**: Models align with AX-01 (Entity Identity) — unique identifiers on all entities.
- [x] **II. Model Integrity**: Models `UnitProfile`, `WeaponStatLine`, `StatModifier` inherit `VindictaModel` from `vindicta_foundation/models/base`.
- [x] **IV. Documentation Discipline**: No container boundary changes — C4 model update not required.
- [x] **V. Quality Mandate**: `pytest` + `pytest-asyncio` running coverage bounds. `ruff` and `mypy --strict` enforced.
- [x] **VII. Spec Directory**: Feature resides in `specs/001-simulation-stat-retrieval/` following `NNN-short-name` convention.

## Project Structure

### Documentation
```text
specs/001-simulation-stat-retrieval/
├── plan.md              # This file
├── spec.md
└── tasks.md             # To be generated
```

### Source Code
```text
src/vindicta_engine/
├── ai/
├── physics/
│   ├── engine.py
│   └── models.py
└── retrieval/                        # NEW DOMAIN
    ├── __init__.py                   # Public API exports
    ├── exceptions.py                 # RAGQueryError, StatParseError
    ├── metrics.py                    # CacheMetrics counters
    ├── models.py                     # UnitProfile, WeaponStatLine, StatModifier
    ├── mcp_client.py                 # MCP connectivity & retry logic
    ├── parser.py                     # Markdown → Pydantic parser
    └── stat_cache.py                 # Async-safe LRU cache + StatRetriever facade

tests/
└── retrieval/
    ├── test_models.py                # Model construction & validation
    ├── test_mcp_client.py            # RAG client & retry logic
    ├── test_parser.py                # Markdown parsing & keyword extraction
    ├── test_stat_cache.py            # Cache hits, LRU, async-safety, metrics
    └── test_integration.py           # End-to-end retrieval flow
```
