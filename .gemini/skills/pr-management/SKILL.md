---
name: pr-management
description: "Pull Request creation, review, and management via GitHub CLI. Use this skill when asked to create a PR, update an existing PR, review open PRs, or check PR status."
---

# `pr-management` Skill

This skill governs interaction with Pull Requests on GitHub using the `gh` CLI.

## CRITICAL: PR Creation Rules

According to the workspace rules:
- **NEVER** use inline `--body` flags with `gh pr create` or `gh pr edit`.
- **ALWAYS** generate a markdown file and use `--body-file`.
- **ALWAYS** clean up the temporary body file after the PR is created.

## Workflow: Creating a New PR

1. **Verify State:** Ensure tests pass and branch is pushed: `git push -u origin HEAD`.
2. **Draft the Body:** Use the script to scaffold from template:
   ```powershell
   scripts/create-pr.ps1 -Title "feat(engine): add MCTS support" -Fixes 42
   ```
   This generates `PR_BODY.md` from [assets/pr-body-template.md](assets/pr-body-template.md). Edit it with specifics.
3. **Execute Creation:**
   ```powershell
   gh pr create --title "<Title>" --body-file PR_BODY.md
   ```
4. **Cleanup:**
   ```powershell
   Remove-Item PR_BODY.md
   ```

## Workflow: Reviewing a PR

Use the review script or direct commands:

```powershell
# List all open PRs
scripts/review-pr.ps1

# View specific PR details and diff
scripts/review-pr.ps1 -PrNumber 42
```

See [references/REFERENCE.md](references/REFERENCE.md) for the full `gh` CLI cheat sheet.

## Available Resources

| Resource | Path | Purpose |
| :------- | :--- | :------ |
| PR Creation Script | [scripts/create-pr.ps1](scripts/create-pr.ps1) | Scaffold PR body from template |
| PR Review Script | [scripts/review-pr.ps1](scripts/review-pr.ps1) | List and review open PRs |
| CLI Reference | [references/REFERENCE.md](references/REFERENCE.md) | Full `gh` CLI command reference |
| Body Template | [assets/pr-body-template.md](assets/pr-body-template.md) | PR body markdown template |
