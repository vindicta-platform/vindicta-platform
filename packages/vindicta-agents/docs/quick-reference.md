# Quick Reference Cheat Sheet

Essential commands and patterns for SDD.

---

## Lifecycle Commands

| Stage   | Command                 | Output         |
| ------- | ----------------------- | -------------- |
| Specify | `/speckit-spec`         | `spec.md`      |
| Plan    | `/speckit-plan`         | `plan.md`      |
| Tasks   | `/speckit-tasks`        | `tasks.md`     |
| Verify  | `/speckit-checklist`    | `checklist.md` |
| Govern  | `/speckit-constitution` | Version bump   |
| Review  | `/review-prs`           | PR summary     |

---

## Task Notation

| Symbol  | Meaning              |
| ------- | -------------------- |
| `[P]`   | Parallelizable       |
| `[USX]` | Maps to User Story X |
| `[B:X]` | Blocked by Task X    |
| ✅       | Complete             |
| 🔄       | In Progress          |
| ⏸️       | Blocked              |

---

## Commit Prefixes

| Prefix      | Usage                        |
| ----------- | ---------------------------- |
| `test:`     | RED phase (failing tests)    |
| `feat:`     | GREEN phase (implementation) |
| `refactor:` | REFACTOR phase (cleanup)     |
| `fix:`      | Bug fixes                    |
| `docs:`     | Documentation                |
| `chore:`    | Maintenance                  |

---

## Quality Gates

```bash
# Tests with coverage
pytest --cov --cov-report=term-missing

# Type checking
mypy --strict src/

# Linting
ruff check .

# Security scan
detect-secrets scan .
```

---

## Constitution Quick Reference

| #   | Principle | Rule                 |
| --- | --------- | -------------------- |
| I   | Economic  | GCP Free Tier only   |
| II  | SDD       | No code without spec |
| V   | Async     | All I/O async        |
| VI  | Tests     | <60s, >80% coverage  |
| XI  | Commits   | Red-Green-Refactor   |
| XII | MCP       | No CLI for GitHub    |

---

## Repository Tiers

| Tier | Priority | Repos        |
| ---- | -------- | ------------ |
| P0   | Highest  | Portal       |
| P1   | High     | Core engines |
| P2   | Medium   | Integration  |
| P3   | Standard | Utilities    |

---

## File Locations

```
repo/.specify/specs/001-feature/
├── spec.md        # Specification
├── plan.md        # Implementation plan
├── tasks.md       # Task breakdown
└── checklist.md   # Verification

repo/.antigravity/
├── ARCHITECTURE.md
├── CONSTRAINTS.md
├── GRAMMAR.md      (WARScribe only)
└── HEURISTICS.md   (AI repos only)
```

---

## User Story Format

```markdown
**As a** {{role}}
**I want** {{goal}}
**So that** {{benefit}}
```

---

## Acceptance Criteria

```gherkin
Given {{context}}
When {{action}}
Then {{expected}}
```

---

## PR Checklist

- [ ] Spec exists
- [ ] Tests fail first
- [ ] Coverage >80%
- [ ] Types clean
- [ ] Lint clean
- [ ] <1000 lines
