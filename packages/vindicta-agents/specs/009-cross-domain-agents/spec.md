# Feature Specification: Cross-Domain Agent Deployment

**Feature Branch**: `009-cross-domain-agents`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "I Want to deploy vindicta agents to other domains while keeping the domains distinct. The agents domain is continuoing to develop, but using other domains as places where contributions can start to happen is key for advancing. Plan how to integrate this by first exploring the org and memories, then come up with a planning phase for using the agents setup for autnomous development."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Workflow Scaffolding (Priority: P1)

As an Architect, I want to deploy the agent workflow layer (playbooks and templates) to all target domain repositories so that agents have the necessary context to perform development tasks within those repositories.

**Why this priority**: This is the fundamental prerequisite for any cross-domain agent activity. Without the workflows, agents don't know the "how" of each domain.

**Independent Test**: Can be tested by verifying that `.agent/workflows/` and `.specify/` directories exist and contain valid markdown in each target repo.

**Acceptance Scenarios**:

1. **Given** a target domain repository (e.g., `Primordia-AI`), **When** the scaffolding script is run, **Then** all standard agent workflows and speckit templates are present in the repo.

---

### User Story 2 - Swarm Graph Expansion (Priority: P1)

As an Architect, I want to expand the swarm control plane in `Vindicta-Agents` to include all 8 active domain realms as routable nodes in the `domain_graph.py`.

**Why this priority**: This enables the centralized swarm to actually dispatch work to the newly scaffolded domains.

**Independent Test**: Can be tested via unit tests in `Vindicta-Agents` that verify the router can correctly identify and route to the new realm keys.

**Acceptance Scenarios**:

1. **Given** a task with `target_realm: "primordia-ai"`, **When** the swarm router processes the state, **Then** it correctly targets the `SeersOracle` node.

---

### User Story 3 - Autonomous Development Pipeline (Priority: P2)

As a Product Owner, I want to enable the full autonomous loop where agents can pick up tasks across domain repositories, from issue detection to PR creation.

**Why this priority**: This fulfills the vision of autonomous platform development across the entire organization.

**Independent Test**: Can be tested by simulating a cross-domain feature request and verifying that the swarm generates tasks across multiple repos and activates the corresponding domain nodes.

**Acceptance Scenarios**:

1. **Given** a cross-domain goal, **When** the meta-graph (PO/Architect/ADL) processes it, **Then** it generates tasks assigned to the appropriate domain realm keys.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide standardized workflow templates for both Python and Node.js domains.
- **FR-002**: Swarm router MUST support all 8 active domains: `vindicta-engine`, `warscribe-system`, `vindicta-economy`, `primordia-ai`, `meta-oracle`, `logi-slate-ui`, `vindicta-portal`, `vindicta-api`.
- **FR-003**: Domain boundaries MUST be preserved; no cross-repo code imports permitted.
- **FR-004**: Each domain repo MUST maintain its own constitution.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of active domain repos (8/8) have agent workflow scaffolding.
- **SC-002**: Swarm graph can successfully route a composite task spanning 3+ domains.
- **SC-003**: Zero manual environment setup required for an agent to move between domains.
