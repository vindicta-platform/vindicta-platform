# Vindicta-Agents v0.2.x Roadmap

## Problem

v0.1.0 provides agent identity (GPG, PAT, dev container). The gap is **workspace lifecycle** — no tooling for cloning repos, managing branches, or finishing sessions with PRs.

## Constraints

| Rule | Source |
|---|---|
| **No `workspace.yml`** — workspace config is the caller's responsibility | User feedback |
| **No custom CLI** — [Vindicta-CLI](https://github.com/vindicta-platform/Vindicta-CLI) is the platform CLI | Constitution |
| **MCP-first** — if MCP is available, MUST use. `gh` CLI as fallback | Constitution |
| **No templates in `.devcontainer/`** — domain boundary violation | User feedback |
| **No constitution enforcement** — that is individual agents' responsibility | User feedback |
| **Workspace MUST be locally isolated** — no resource contention | User feedback |
| **Atomic commits** — regular, short messages, best practice for clarity | User feedback |
| **Chores/docs/fixes to `main`** — keep feature branches concise for human reviewers | User feedback |
| **Config-driven** — externalize filter options, no hardcoded groups | User feedback |
| **PR summaries include tech debt** — discovered/created issues surfaced | User feedback |

---

## v0.2.0 — Workspace Isolation & Devcontainer Spike

**Goal:** Understand how devcontainer workspaces connect to multi-repo setups across IDEs, and ensure local isolation.

### SPIKE: Devcontainer Multi-Repo Workspace

> **Note:** This is a research spike before writing code. Output is a tested reference setup, not production tooling.

**Questions to answer:**
1. How does VS Code handle multi-root workspaces inside devcontainers?
2. How does Antigravity connect to workspaces? Can workspace config be passed in?
3. Can a devcontainer mount multiple repo directories from the host?
4. What is the isolation model — one container per repo, or shared container with isolated directories?

**Deliverables:**
- Sample devcontainer configs for single-repo and multi-repo workspace patterns
- Tested on VS Code and Docker CLI
- Documented gotchas (volume mounts, git identity per-repo, branch conflicts)

### Changes

- **[NEW]** `docs/workspace-patterns.md` — reference doc from the spike
- **[MODIFY]** `Dockerfile.slim` — workspace isolation structure (`/workspace/<repo>/`)
- **[MODIFY]** `init-agent.sh` — detect repos in `/workspace/`, print status

---

## v0.2.1 — Multi-Repo Operations

**Goal:** Utilities for common multi-repo operations using `gh` CLI and MCP.

### Design Principles

- `gh` CLI + MCP are primary — no competing CLI
- Config-driven — repo lists from external config or args, never hardcoded
- Workspace isolation — each repo is its own git directory
- Stash safety — warn and prompt, never auto-stash
- No data loss — never force-checkout without confirmation

### Changes

- **[NEW]** `.devcontainer/bin/workspace-status` — multi-repo status table (branch, modified, ahead/behind)
- **[NEW]** `.devcontainer/bin/workspace-sync` — fetch/pull all repos with error handling

### workspace-sync Error Handling

| Scenario | Behavior |
|---|---|
| Dirty working tree | Warn + skip (never auto-stash) |
| Merge conflict | Abort pull, report, continue other repos |
| Remote branch deleted | Warn, switch to main |
| Network timeout | Retry once, then skip |
| Repo missing | Skip with warning |
| Detached HEAD | Warn, no pull |
| Rebase conflict | Abort rebase, restore state, report |

---

## v0.2.2 — PR Lifecycle

**Goal:** Streamline commit → push → PR with atomic commits, MCP-first PR creation, human-reviewer-friendly output.

### Commit Rules

| Rule | Rationale |
|---|---|
| Commits MUST be atomic | One logical change per commit |
| Messages ≤72 chars (subject) | Git best practice |
| Conventional commits | `feat:`, `fix:`, `chore:`, `docs:` |
| Chores/docs/fixes to `main` | Keep feature branches concise |
| Feature branches short-lived | Reduce conflict risk |

### PR Creation Protocol (MCP Retry-with-Memory)

```
1. MCP available?  → Use mcp_github-mcp-server_create_pull_request
2. MCP errors?     → Attempt resolution (up to 3 troubleshooting steps)
3. MCP fails?      → Fall back to `gh pr create`, record failure timestamp
4. gh fails?       → Ask for user support
5. Next PR call    → If 5 min elapsed since MCP failure, retry MCP first
                     Otherwise use gh directly
```

> Failures are remembered but MCP is periodically retried to restore priority. Never permanently degrade to `gh`.

### Changes

- **[NEW]** `.devcontainer/bin/workspace-finish` — commit, push, create PRs (draft, dry-run modes)
- **[NEW]** `.devcontainer/bin/workspace-pr` — PR status table across workspace

---

## Version Summary

| Version | Name | Delivers | Size |
|---|---|---|---|
| **v0.2.0** | Workspace Spike | Research + reference configs | Small |
| **v0.2.1** | Multi-Repo Ops | `workspace-status`, `workspace-sync` | Medium |
| **v0.2.2** | PR Lifecycle | `workspace-finish`, `workspace-pr` | Medium |

## Verification

### BDD Feature Specs (Gherkin) — `tests/features/`

```gherkin
Feature: Workspace Sync
  Scenario: Sync clean workspace
    Given all repos have clean working trees
    When I run workspace-sync
    Then all repos are updated to latest remote

  Scenario: Sync with dirty repo
    Given "Vindicta-Core" has uncommitted changes
    When I run workspace-sync
    Then "Vindicta-Core" is skipped with a warning
    And all other repos are synced
```

### TDD Test Scripts (AAA Pattern)

| Test | Validates |
|---|---|
| `test-workspace-status.sh` | Status across multi-repo workspace |
| `test-workspace-sync.sh` | Fetch/pull with edge case safety |
| `test-workspace-finish.sh` | Commit → push → PR (dry-run) |
