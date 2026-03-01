# ADR-009: Cross-Domain Agent Deployment

**Status**: Approved
**Date**: 2026-02-11
**Deciders**: Architect Agent, Human Stakeholder

## Context

The Vindicta Agents swarm control plane currently routes tasks to 3 domains (`vindicta-engine`, `warscribe-system`, `vindicta-economy`). Five additional active domains (`Primordia-AI`, `Meta-Oracle`, `Logi-Slate-UI`, `Vindicta-Portal`, `Vindicta-API`) lack agent integration. The platform needs cross-domain coordination without merging domain boundaries.

## Decision

Expand the swarm via 3 phases:
1. **Workflow Scaffolding** — Deploy `.agent/workflows/` and `.specify/` into target repos
2. **Domain Graph Expansion** — Add 5 new realm nodes to `domain_graph.py` following the established node pattern
3. **Autonomous Pipeline** — Wire issue→spec→plan→task→PR across all domains

### Key Constraints
- Domain boundaries are absolute: no cross-repo imports, domain-local CI/constitution, per-domain PRs only
- Foundation dependency flows downward only
- New nodes follow the identical signature pattern as existing nodes

## Consequences

- **Positive**: Agents can coordinate work across the full organization surface
- **Positive**: Additive change — zero risk to existing 3-realm routing
- **Risk**: Phase 3 depends on v2.0 autonomous PR management (AD-2)
- **Mitigated**: Phased rollout de-risks; Phase 1 is non-breaking file additions

## References
- [Implementation Plan](../../specs/009-cross-domain-agents/plan.md)
- [Tasks](../../specs/009-cross-domain-agents/tasks.md)
- GitHub Issues: #19–#37
