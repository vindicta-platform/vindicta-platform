# Agent Integration Guide

How AI agents use the `.specify` repository for organization-wide SDD.

---

## Quick Start

At the start of any task, agents should:

```
1. Read memory/platform-constitution.md
2. Read memory/repo-registry.md
3. Identify the target repository tier
4. Load repo-specific context artifacts
```

---

## Discovering Context

### Organization-Level Context

| File                              | Purpose              |
| --------------------------------- | -------------------- |
| `memory/platform-constitution.md` | Governance rules     |
| `memory/repo-registry.md`         | Repository inventory |

### Repository-Level Context

Each repo contains `.antigravity/` with:

| Artifact          | Found In                       |
| ----------------- | ------------------------------ |
| `ARCHITECTURE.md` | All P0-P2 repos                |
| `CONSTRAINTS.md`  | Portal, Oracle, SDK, API, Core |
| `GRAMMAR.md`      | WARScribe repos                |
| `HEURISTICS.md`   | Primordia-AI, Dice-Engine      |

---

## Using Workflows

### Slash Command Pattern

Workflows are invoked via slash commands:

```
/speckit-spec    → Create specification
/speckit-plan    → Generate implementation plan
/speckit-tasks   → Generate task breakdown
```

### Workflow Location

Workflows live in `workflows/`:
- `speckit-spec.md`
- `speckit-plan.md`
- `speckit-tasks.md`
- `speckit-checklist.md`
- `speckit-constitution.md`
- `review-prs.md`

### Turbo Annotations

Commands with `// turbo` can auto-execute:
```markdown
// turbo
```bash
git checkout main
```
```

`// turbo-all` enables auto-run for ALL commands in the workflow.

---

## Template Usage

### Finding Templates

Templates are in `templates/`:
- `spec-template.md`
- `plan-template.md`
- `tasks-template.md`
- `checklist-template.md`
- `agent-file-template.md`

### Copying Templates

```bash
cp .specify/templates/spec-template.md target-repo/.specify/specs/001-feature/spec.md
```

### Placeholder Syntax

Templates use `{{PLACEHOLDER}}` syntax:
- `{{DATE}}` — Current date
- `{{FEATURE_ID}}` — Feature number
- `{{feature-name}}` — Kebab-case name
- `{{REPOSITORY_NAME}}` — Target repo

---

## Constitution Compliance

### Mandatory Checks

Before any PR, verify:

| Principle        | How to Check          |
| ---------------- | --------------------- |
| II (Spec-Driven) | `spec.md` exists      |
| V (Async)        | No blocking I/O       |
| VI (Tests)       | Coverage >80%, <60s   |
| XI (Commits)     | Red-Green-Refactor    |
| XII (MCP)        | No CLI for GitHub ops |

### Quality Gates

Run these tools:
```bash
pytest --cov   # Tests + coverage
mypy --strict  # Type checking
ruff check .   # Linting
```

---

## Cross-Repository Operations

### Priority Order

Process repositories by tier:
1. P0 (Vindicta-Portal)
2. P1 (Core Platform)
3. P2 (Supporting)
4. P3 (Utilities)

### PR Review Workflow

Use `/review-prs` to check all open PRs across the org.

---

## Error Handling

### 3-Strategy Rule (Principle IX)

Try 3 different approaches before asking for help:
1. Strategy A
2. Strategy B
3. Strategy C
4. Then report with all attempts documented

### MCP Fallback (Principle XII)

If GitHub MCP is unavailable:
- **STOP** — Do not use CLI
- Report the issue
- Wait for MCP restoration
