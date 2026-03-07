---
description: Generate a standardized Pull Request description and submit or update it via GitHub CLI.
---

# PR Workflow

Standardized procedure for creating and managing high-quality Pull Requests across all Vindicta modules.

## 1. Pre-flight Checks

// turbo
1. **Push Changes**: Ensure the current branch is pushed to origin.
2. **Validation**: Run `tdd-workflow` and `bdd-workflow` validation scripts to ensure 90%+ coverage.
3. **Artifact Sync**: For features, run `sdd-workflow` validation to ensure spec/plan/tasks are complete.

## 2. PR Creation

1. **Scaffold Body**: Generate `PR_BODY.md` using the `pr-management` skill.
   ```powershell
   scripts/create-pr.ps1 -Title "<Title>" -Fixes <IssueNumber>
   ```
2. **Review & Refine**: Flesh out the description, focusing on *why* the change was made and any technical trade-offs.
3. **Submit**: Use `gh pr create` with the `--body-file` flag.

## 3. Post-Creation

1. **Cleanup**: Remove the temporary `PR_BODY.md` file.
2. **Review Cycle**: Monitor for comments and use `pr-management` scripts to respond or update.

## Leveraging Skills
- **pr-management**: Primary skill for all `gh` CLI interactions.
- **tdd-workflow / bdd-workflow**: For pre-commit quality gates.
