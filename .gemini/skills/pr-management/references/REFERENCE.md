# PR Management Reference

## `gh` CLI Cheat Sheet

| Goal                        | Command                                         |
| :-------------------------- | :---------------------------------------------- |
| List open PRs               | `gh pr list --state open`                       |
| View PR details             | `gh pr view <number>`                           |
| View PR diff                | `gh pr diff <number>`                           |
| Checkout PR locally         | `gh pr checkout <number>`                       |
| Create PR (body file)       | `gh pr create --title "..." --body-file PR.md`  |
| Edit PR body                | `gh pr edit <number> --body-file PR.md`          |
| Merge PR (squash)           | `gh pr merge <number> --squash --delete-branch` |
| Enable auto-merge           | `gh pr merge <number> --auto --squash`          |
| List PR checks              | `gh pr checks <number>`                         |
| Add reviewer                | `gh pr edit <number> --add-reviewer @user`      |
| List your PRs               | `gh pr list --author @me`                       |

## Workspace PR Rules

1. **NEVER** use `--body` inline. Always use `--body-file`.
2. **ALWAYS** clean up `PR_BODY.md` after successful PR creation.
3. Use `.github/PULL_REQUEST_TEMPLATE.md` if it exists.
4. Commit messages should follow Conventional Commits (see `git-mcp` skill).
