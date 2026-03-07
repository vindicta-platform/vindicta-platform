# Git MCP Reference

## Conventional Commits Cheat Sheet

| Type       | When to Use                                    |
| :--------- | :--------------------------------------------- |
| `feat`     | A new feature                                  |
| `fix`      | A bug fix                                      |
| `docs`     | Documentation only changes                     |
| `style`    | Formatting, missing semicolons, etc.           |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                        |
| `test`     | Adding or correcting tests                     |
| `build`    | Changes to build system or dependencies        |
| `ci`       | CI configuration changes                       |
| `chore`    | Other changes that don't modify src or tests   |
| `revert`   | Reverts a previous commit                      |

## Git Search Quick Reference

| Goal                         | Command                                            |
| :--------------------------- | :------------------------------------------------- |
| Find who introduced a string | `git log -S "string" --oneline --all`              |
| Regex search in history      | `git log -G "pattern" --oneline`                   |
| File history                 | `git log --oneline -- path/to/file`                |
| Blame a line                 | `git blame -L 10,20 path/to/file`                  |
| Show commit details          | `git show --name-status <hash>`                    |
| Diff between branches        | `git diff main..feature-branch --stat`             |
| Find merge commit            | `git log --merges --oneline -n 10`                 |

## Submodule Operations (Vindicta Platform)

The platform uses git submodules for all packages. Key commands:

```powershell
# Update all submodules to latest remote
git submodule update --remote

# Check submodule status
git submodule status

# Initialize after fresh clone
git submodule update --init --recursive
```
