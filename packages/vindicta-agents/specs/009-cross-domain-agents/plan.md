# Implementation Plan: Cross-Domain Agent Deployment

**Branch**: `009-cross-domain-agents` | **Date**: 2026-02-11 | **Spec**: [spec.md](./spec.md)

## Summary
Expand the Vindicta Agents swarm to operate as a centralized coordination layer across 8 distinct domain repositories. This involves non-invasive scaffolding of workflows into target repos and expanding the LangGraph control plane to support routing across the full organizational surface.

## Technical Context

**Language/Version**: Python 3.12 (Swarm), Shell/PowerShell (Scaffolding)
**Primary Dependencies**: LangGraph, FastAPI, GitHub MCP
**Testing**: pytest, behave
**Target Platform**: GitHub Repositories
**Project Type**: Multi-repo Swarm Orchestration

## Constitution Check

- **MCP-First**: Mandatory use of GitHub MCP for cross-repo operations.
- **SDD**: This plan follows the speckit SDD pattern.
- **Economic**: All nodes and workflows operate within free tier limits.

## Project Structure

### Documentation (this feature)

```text
specs/009-cross-domain-agents/
├── plan.md              # This file
├── spec.md              # Feature specification
└── tasks.md             # To be generated
```

### Source Code (Vindicta-Agents root)

```text
src/vindicta_agents/
├── swarm/
│   ├── domain_graph.py  # Expanded with new nodes
│   ├── meta_graph.py    # Updated for cross-domain awareness
│   └── domain_registry.py # NEW: Central registry of domains
└── nexus/
    └── orchestrator.py  # Supporting multi-domain envelopes
```
