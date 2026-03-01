# Research: Agent Isolation

**Feature**: Agent Isolation (011)

## Decisions

### 1. Base Image selection

**Decision**: Use `python:3.11-slim` and install `git` at runtime or build a custom image.
**Rationale**:
- `Vindicta-Agents` is Python-based.
- `slim` variants are smaller but contain necessary build tools often needed for python packages.
- Need to install `git` explicitly as it's not in slim by default.

**Alternatives Considered**:
- `python:3.11-alpine`: Too many wheel compatibility issues with complex dependencies.
- `python:3.11` (full): unnecessary size overhead.

### 2. Volume Strategy

**Decision**: Use **Bind Mounts** for the agent workspace.
**Rationale**:
- Allows easer debugging (files visible on host).
- Simplifies artifact retrieval (logs, outputs) without `docker cp`.
- We can clean up by deleting the host directory after container exit.

**Alternatives Considered**:
- **Docker Volumes**: Better isolation, but harder to inspect/debug for the user on Windows. Harder to clean up programmatically without leaving orphans.

## Dependencies

- **Docker SDK for Python**: `docker` package.
- **Git**: Must be installed in the container.
