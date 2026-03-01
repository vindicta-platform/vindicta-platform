# VS Code Dev Container Setup

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- [VS Code](https://code.visualstudio.com/) installed
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
  installed

## Setup

1. **Open the repo in VS Code:**

   ```powershell
   code Vindicta-Agents
   ```

2. **VS Code will detect `.devcontainer/`** and show a notification:
   > "Folder contains a Dev Container configuration file. Reopen folder to develop
   > in a container."

   Click **"Reopen in Container"**.

   Or use the Command Palette: `Ctrl+Shift+P` → **"Dev Containers: Reopen in
   Container"**

3. **Wait for the build.** First build takes 2-3 minutes. VS Code will:
   - Build the Docker image from `.devcontainer/Dockerfile`
   - Install dev container features (git, gh CLI)
   - Run `init-agent.sh` automatically (generates/imports GPG key)

4. **Check the terminal output** for:
   - `=== Agent Identity Ready ===` — confirms identity is configured
   - If a new key was generated, the public key will be in `/output/`

## Working Inside the Container

- **Terminal:** `` Ctrl+` `` opens a bash terminal inside the container
- **Git:** All commits are auto-signed with the bot's GPG key
- **GitHub CLI:** Pre-authenticated if `AGENT_GITHUB_TOKEN` was set

## Useful Commands

<!-- markdownlint-disable MD013 -->
| Action                      | Command                                                        |
| --------------------------- | -------------------------------------------------------------- |
| Rebuild container           | `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"           |
| Attach to running container | `Ctrl+Shift+P` → "Dev Containers: Attach to Running Container" |
| View container logs         | `Ctrl+Shift+P` → "Dev Containers: Show Container Log"          |
| Reopen locally              | `Ctrl+Shift+P` → "Dev Containers: Reopen Folder Locally"       |

## Troubleshooting

| Issue                | Fix                                                                            |
| -------------------- | ------------------------------------------------------------------------------ |
| "Docker not running" | Start Docker Desktop                                                           |
| Build fails          | Run `Ctrl+Shift+P` → "Dev Containers: Rebuild Without Cache"                   |
| `bash\r` error       | Image needs rebuild — the Dockerfile includes `dos2unix` to fix this           |
| GPG key not found    | Check `init-agent.sh` output in the terminal, re-run manually: `init-agent.sh` |
<!-- markdownlint-enable MD013 -->
