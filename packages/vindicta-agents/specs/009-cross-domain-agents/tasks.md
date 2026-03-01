# Tasks: Cross-Domain Agent Deployment

**Input**: Design documents from `/specs/009-cross-domain-agents/`
**Prerequisites**: plan.md, spec.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 [P] Create folder structure in target domain repositories
- [ ] T002 [P] Research GitHub MCP limitations for cross-repo branch protections

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T003 [P] Create `src/vindicta_agents/swarm/domain_registry.py` with all 8 active domain repos
- [ ] T004 [P] Update `src/vindicta_agents/swarm/state.py` to support multi-domain task tracking
- [ ] T005 Update `src/vindicta_agents/swarm/config.py` MockLLMProvider for 8 realms

---

## Phase 3: User Story 1 - Workflow Scaffolding (Priority: P1) 🎯 MVP

**Goal**: Deploy agent playbooks and templates to target domain repos.

**Independent Test**: Verify `.agent/workflows/` and `.specify/` presence in `Primordia-AI`.

- [ ] T006 [P] [US1] Create template workflows in `.specify/templates/domain-workflows/`
- [ ] T007 [US1] Implement scaffolding logic in `src/vindicta_agents/utils/scaffolder.py`
- [ ] T008 [US1] Create automation script `automation/scripts/Scaffold-Domains.ps1`
- [ ] T009 [US1] Verify scaffolding successfully deploys to a test branch in `Primordia-AI`

---

## Phase 4: User Story 2 - Swarm Graph Expansion (Priority: P1)

**Goal**: Expand the control plane to route tasks to all 8 domains.

**Independent Test**: Unit test router logic with all 8 realm keys.

- [ ] T010 [P] [US2] Create unit test `tests/unit/test_expanded_router.py`
- [ ] T011 [US2] Implement new domain nodes in `src/vindicta_agents/swarm/domain_graph.py`
- [ ] T012 [US2] Update `task_router` logic in `src/vindicta_agents/swarm/domain_graph.py`
- [ ] T013 [US2] Verify routing ensures domain isolation in `tests/shadow/test_cross_domain_isolation.py`

---

## Phase 5: User Story 3 - Autonomous Development Pipeline (Priority: P2)

**Goal**: Enable end-to-end issues-to-PR loop across domain boundaries.

**Independent Test**: Simulate cross-repo goal and verify task generation.

- [ ] T014 [US3] Update `src/vindicta_agents/swarm/meta_graph.py` for cross-domain awareness
- [ ] T015 [US3] Implement issue-to-realm mapping in `src/vindicta_agents/sdk/models.py`
- [ ] T016 [US3] Create end-to-end simulation `tests/shadow/test_autonomous_cross_domain_loop.py`

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T017 [P] Update `docs/architecture.md` with cross-domain swarm topology
- [ ] T018 [P] Update `docs/quick-reference.md` with new domain node profiles
- [ ] T019 Run final platform sync and verify all 8 domains are online

---

## Dependencies & Execution Order

- **Foundational (Phase 2)**: MUST complete before any User Story work.
- **Workflow Scaffolding (Phase 3)**: Prerequisite for actual execution in domains.
- **Swarm Expansion (Phase 4)**: Can proceed in parallel with Phase 3 scaffolding.
- **Autonomous Pipeline (Phase 5)**: Depends on US1 and US2 completion.
