# Implementation Plan - Agent Isolation

**Feature**: Agent Isolation
**Status**: Draft
**Spec**: [specs/011-agent-isolation/spec.md](specs/011-agent-isolation/spec.md)

## Technical Context

We need to implement an execution environment for agents that isolates them from the host system while allowing them to perform git operations.

**Selected Approach**: Docker Containers (as per clarification).

**Key Components**:

1. **Information Architecture**:
   - `AgentExecutionEnvironment` (interface)
   - `DockerExecutionEnvironment` (implementation)
   - `CredentialInjector` (service)
   - `WorkspaceManager` (service)

2. **Dependencies**:
   - `docker` (Python SDK) or `docker-py`
   - Host system must have Docker Engine installed

**Unknowns & Clarifications**:
- [NEEDS CLARIFICATION] specific base image for agents? (e.g. `python:3.11-slim` vs custom image with git installed)
- [NEEDS CLARIFICATION] Volume mounting strategy? (Bind mounts vs Docker volumes)

## Constitution Check

**Goal**: Ensure architectural alignment and no regression of core principles.

1. **System boundaries**: Does this respect the boundaries between agents?
   - *Analysis*: Yes, Docker provides strong isolation boundaries.
2. **Data persistence**: How is data handled?
   - *Analysis*: Workspaces are ephemeral or explicitly managed.
3. **Security**: Are credentials handled securely?
   - *Analysis*: Environment variables in containers are standard, but need to ensure they aren't logged.

*Result*: Pass (Proceed with Docker approach)

## Proposed Changes

### [Phase 0] Research

Resolved during research phase:

1. **Base Image Selection**: Selected `python:3.11-slim`. Will need to ensure `git` is installed at runtime or via a custom derived image.
2. **Volume Strategy**: Selected **Bind Mounts**. This allows easier inspection of the agent's work from the host and simpler cleanup logic.

### [Phase 1] Data Model & Contracts

1. **Data Model**:
   - `AgentContainerConfig` (pydantic model):
       - `image`: str (default: "python:3.11-slim")
       - `env_vars`: Dict[str, str] (for credentials)
       - `workspace_path`: Path (host path to bind mount)
       - `command`: List[str] (entrypoint)
   - `WorkspaceConfig`:
       - `base_dir`: Path (e.g. `%TEMP%/vindicta-agents/{agent_id}`)
       - `cleanup_on_exit`: bool

2. **Contracts**:
   - `ExecutionEnvironment` (Protocol):
       - `run(task: Task, context: Context) -> Result`
       - `cleanup()`
   - `DockerEnvironment(ExecutionEnvironment)`:
       - `__init__(config: AgentContainerConfig)`
       - `start() -> str` (returns container ID)
       - `wait() -> int` (exit code)
       - `logs() -> Generator`

### [Phase 2] Implementation

#### [vindicta-agents] Core Logic

##### [NEW] `src/vindicta_agents/execution/docker_env.py`
- Implement `DockerExecutionEnvironment` class.
- Handles container lifecycle: create, start, monitor, stop, remove.
- Injects credentials associated with the agent identity.

##### [NEW] `src/vindicta_agents/execution/workspace.py`
- Implement `WorkspaceManager` to setup/teardown directories.

##### [MODIFY] `src/vindicta_agents/swarm/agent.py` (or equivalent)
- Update agent runtime to use `ExecutionEnvironment` abstraction instead of running directly on host process (if currently doing so).

## Verification Plan

### Automated Tests
- **Unit Tests**: Mock `docker` client to verify container config generation and lifecycle calls.
- **Integration Tests**:
    - Run a real docker container (requires dind or host socket).
    - script: `pytest tests/integration/execution/test_docker_env.py`
    - Verify container starts, runs simple echo command, and cleanup removes it.

### Manual Verification
1. Run a test script that spawns an agent.
2. `docker ps` to see it running.
3. Check agent logs for successful git clone (if credentials provided).
4. Verify `docker ps -a` shows no leftover containers after run.
