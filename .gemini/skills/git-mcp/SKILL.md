---
name: git-mcp
description: "Advanced Git operations, commit hygiene, and history search. Use this skill for git tree traversal, code provenance checks, pickaxe searches, and ensuring conventional commit messages."
---

# `git-mcp` Skill

This skill ensures you are using Git optimally for analyzing history and making high-quality commits within the Vindicta Platform workspace.

## General Best Practices

1. **Prefer native `git` commands.** Use PowerShell-native CLI.
2. **Prioritize `--oneline` and filtering.** Do not run unbounded `git log` commands.
3. **Always use `--name-status` or `--stat`** when checking what files changed in a past commit.

## Code Search & History

When trying to understand code provenance or find when something was added:

1. **Search History for a String (Pickaxe)**
   Use `-S` to find commits that introduced or removed a specific string:
   ```powershell
   git log -S "SomeFunctionOrString" --oneline --source --all
   ```
   Or use the helper script: `scripts/search-history.ps1 -Query "SomeFunctionOrString"`

2. **Search History Using Regex**
   ```powershell
   scripts/search-history.ps1 -Query "def.*SomeFunction" -UseRegex
   ```

3. **See File History (Concise)**
   ```powershell
   git log --oneline -- <file_path>
   ```

4. **Show Specific Commit Changes**
   ```powershell
   git show --name-status <commit_hash>
   ```

See [references/REFERENCE.md](references/REFERENCE.md) for the full command cheat sheet including submodule operations.

## Commit Hygiene

When you are ready to commit changes:

1. **Status Check:** Always run `git status` and `git diff` before committing.
2. **Conventional Commits:** Validate your message format:
   ```powershell
   scripts/validate-commit-msg.ps1 -Message "feat(engine): add MCTS support"
   ```
   Format: `<type>(<scope>): <short summary>` — see [assets/commit-template.txt](assets/commit-template.txt) for the full template.
3. **Execution:** Run `git commit -m "<message>"`.

## Available Resources

| Resource | Path | Purpose |
| :------- | :--- | :------ |
| History Search Script | [scripts/search-history.ps1](scripts/search-history.ps1) | Search git history via pickaxe or regex |
| Commit Validator | [scripts/validate-commit-msg.ps1](scripts/validate-commit-msg.ps1) | Validate conventional commit messages |
| Command Reference | [references/REFERENCE.md](references/REFERENCE.md) | Git & submodule command cheat sheet |
| Commit Template | [assets/commit-template.txt](assets/commit-template.txt) | Conventional commit message template |
