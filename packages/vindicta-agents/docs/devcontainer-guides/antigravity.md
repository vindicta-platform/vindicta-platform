# Antigravity Dev Container Setup

Antigravity (Google DeepMind) operates as a terminal-based agent. It doesn't have
native dev container UI integration, so the workflow uses the Docker CLI.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- Antigravity session active

## Setup

### 1. Build the Image

```powershell
cd Vindicta-Agents
docker build --no-cache -t vindicta-agent .devcontainer/
```

### 2. Run with Agent Identity

**First run (generate GPG key):**

```powershell
docker run --rm `
  -v "${PWD}/.keys:/output" `
  -v "${PWD}:/workspace" `
  -e AGENT_NAME=vindicta-bot `
  -e "AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com" `
  -e "AGENT_GITHUB_TOKEN=ghp_YOUR_TOKEN" `
  -w /workspace `
  -it vindicta-agent bash
```

Inside the container:

```bash
init-agent.sh   # generates key, exports to /output/, uploads to GitHub if PAT allows
```

**Subsequent runs (import existing key):**

```powershell
$GPG_KEY = Get-Content .keys/vindicta-bot-gpg-private-b64.txt -Raw
docker run --rm `
  -v "${PWD}/.keys:/output" `
  -v "${PWD}:/workspace" `
  -e AGENT_NAME=vindicta-bot `
  -e "AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com" `
  -e "AGENT_GITHUB_TOKEN=ghp_YOUR_TOKEN" `
  -e "GPG_PRIVATE_KEY=$GPG_KEY" `
  -w /workspace `
  -it vindicta-agent bash
```

### 3. Agent Workflow Inside Container

```bash
# Init identity
init-agent.sh

# Work on a feature
git checkout -b feat/my-feature
# ... make changes ...
git add -A && git commit -m "feat: description"
git push origin feat/my-feature

# Create PR
gh pr create --title "feat: description" --body "Details" --base main
```

## Antigravity-Specific Patterns

### Running Commands Inside the Container

Antigravity can use `run_command` to execute Docker commands on the host, which in
turn run inside the container:

```powershell
# One-shot command inside container
docker exec <container_id> git log --oneline -5

# Or use docker run for stateless operations
docker run --rm -v "${PWD}:/workspace" -w /workspace vindicta-agent git status
```

### Long-Running Container

For extended sessions, start the container and keep it running:

```powershell
# Start in background
docker run -d --name vindicta-agent-session `
  -v "${PWD}/.keys:/output" `
  -v "${PWD}:/workspace" `
  -e AGENT_NAME=vindicta-bot `
  -e "AGENT_EMAIL=260104759+vindicta-bot@users.noreply.github.com" `
  -e "AGENT_GITHUB_TOKEN=ghp_YOUR_TOKEN" `
  -w /workspace `
  vindicta-agent sleep infinity

# Init identity
docker exec vindicta-agent-session init-agent.sh

# Run commands
docker exec vindicta-agent-session git status
docker exec vindicta-agent-session gh pr list

# Stop when done
docker stop vindicta-agent-session && docker rm vindicta-agent-session
```

## Troubleshooting

<!-- markdownlint-disable MD013 -->
| Issue                          | Fix                                                      |
| ------------------------------ | -------------------------------------------------------- |
| `bash\r` errors                | Rebuild with `--no-cache` — Dockerfile runs `dos2unix`   |
| GPG errors                     | Ensure `GPG_PRIVATE_KEY` is base64-encoded (no newlines) |
| `+` in email breaks PowerShell | Wrap the `-e` value in double quotes                     |
| Container can't push           | Check `AGENT_GITHUB_TOKEN` has `repo` scope              |
<!-- markdownlint-enable MD013 -->
