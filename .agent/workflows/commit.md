---
description: Standardized way to sign and execute commits locally.
---

# Commit Workflow

Enforces commit hygiene and conventional message formatting for the Vindicta Platform.

## 1. Preparation

1. **Status Review**: Check `git status` and `git diff` to ensure only intended changes are staged.
2. **Linting**: Run `ruff check .` to ensure no lint regressions.

## 2. Formatting

1. **Message Validation**: Use the `git-mcp` skill to validate the commit message against the conventional commits template.
   ```powershell
   scripts/validate-commit-msg.ps1 -Message "<type>(<scope>): <summary>"
   ```
   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.

## 3. Execution

1. **Commit**: Run `git commit -m "<validated_message>"`.
2. **Sign-off**: Ensure commits are signed if required by the repository policy.

## Leveraging Skills
- **git-mcp**: For message validation and history search.
