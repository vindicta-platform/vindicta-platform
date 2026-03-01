# ADR-003: Platform Consolidation & Deprecation Strategy

## Status
Proposed

## Context
Following **ADR-001 (Consolidation)**, the physical migration of code from 29+ repositories into 7 Meso-repositories is the primary focus. However, we lack a standardized method for decommissioned repositories, leading to "ghost repos" that confuse new contributors.

## 1. Deprecation Standard (The "Decommission" Protocol)

Every repository slated for consolidation MUST follow this checklist before being marked as **Archived** in GitHub:

### A. The README Banner
The top of the README must be replaced with the following block:
```markdown
# ⚠️ ARCHIVED — Consolidated into `[NEW-REPO-NAME]`

> **This repository has been superseded.**
> All functionality has been ported into [`[NEW-REPO-NAME]/[PATH]`](https://github.com/vindicta-platform/[NEW-REPO-NAME]) as part of [ADR-001](https://github.com/vindicta-platform/vindicta-foundation/blob/main/docs/architecture/adr/0005-consolidation.md).

## Migration Mapping
| Legacy Path | New Path                      |
| :---------- | :---------------------------- |
| `src/`      | `[NEW-REPO]/src/[PACKAGE]/`   |
| `tests/`    | `[NEW-REPO]/tests/[PACKAGE]/` |

## Status
- **Read-only**: No new development or security patches will occur here.
- **Issues**: Redirected to the target repository.
```

### B. Repository Cleanup
1.  **Issue redirection**: Close all open issues with a pointer to the new repository.
2.  **Secret Scrub**: Verify all repository secrets are migrated to the target Meso-repo.
3.  **GitHub Archive**: Set the repository status to "Archived" (read-only).

---

## 2. Consolidation Map (Audit)

Based on a scan of the organization, the following repositories are identified as **Stale/Legacy** and require consolidation:

### Domain 1: Foundation (The Lex)
- [x] `Platform-Docs` -> `vindicta-foundation/docs`
- [ ] `Atomic-Ledger-Py` -> `vindicta-foundation` (Base objects) or `vindicta-economy`
- [ ] `devcontainers` -> `vindicta-platform/.devcontainer` (shared config)
- [ ] `docs` -> (Redundant, merge with foundation/docs)

### Domain 2: Economy (The Market)
- [ ] `Economy-Engine` -> `vindicta-economy`
- [ ] `Quota-Manager` -> `vindicta-economy`
- [ ] `Metered-SaaS-Logic` -> `vindicta-economy`
- [ ] `Audit-Log-Pro` -> `vindicta-economy`

### Domain 3: Engine (The Physics)
- [ ] `Dice-Engine` -> `vindicta-engine`
- [ ] `Entropy-Buffer` -> `vindicta-engine`
- [ ] `Primordia-AI` -> `vindicta-engine`

### Domain 4: Scribe (The Scribe)
- [ ] `WARScribe-Core` -> `warscribe-system`
- [ ] `WARScribe-Parser` -> `warscribe-system`
- [ ] `WARScribe-CLI` -> `warscribe-system`

### Domain 5: Oracle (The Oracle)
- [ ] `Meta-Oracle` -> `vindicta-oracle`
- [ ] `Arbiter-Predictor` -> `vindicta-oracle`

### Domain 6: Gateway (The Interface)
- [ ] `Vindicta-API` -> `vindicta-platform`
- [ ] `Logi-Slate-UI` -> `vindicta-platform/ui/logi-slate`
- [ ] `platform-core` -> `vindicta-platform/api`

---

## 3. Consolidation Workflow

To ensure history is preserved where possible:

1.  **Subtree Merge**: Use `git subtree add` to bring the legacy repo into the target folder while preserving commit history.
2.  **Dependency Fix**: Update `pyproject.toml` or `package.json` in the target Meso-repo to include the new code as an internal module.
3.  **CI/CD Alignment**: Move the original repo's test suite into the target's `/tests` directory and ensure the monolithic runner detects them.
4.  **Axiom check**: Verify that all ported models inherit from `VindictaModel` in foundation.
