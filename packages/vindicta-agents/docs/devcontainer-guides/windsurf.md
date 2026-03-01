# Windsurf Dev Container Setup

Windsurf is built on the VS Code engine and supports dev containers via the same
extension.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- [Windsurf](https://codeium.com/windsurf) installed
- Dev Containers extension installed (should be available in Windsurf's extension
  marketplace)

## Setup

1. **Install the Dev Containers extension:**
   - Open Extensions sidebar (`Ctrl+Shift+X`)
   - Search for **"Dev Containers"** (by Microsoft)
   - Install it

2. **Open the repo:**

   ```powershell
   windsurf Vindicta-Agents
   ```

   Or: `File → Open Folder → Vindicta-Agents/`

3. **Reopen in Container:**
   - Windsurf detects `.devcontainer/` and prompts to reopen
   - Click **"Reopen in Container"**
   - Or use Command Palette: `Ctrl+Shift+P` → **"Dev Containers: Reopen in
     Container"**

4. **Wait for the build** (2-3 min first time). The `init-agent.sh` runs automatically.

5. **Verify in terminal** (`` Ctrl+` ``):

   ```bash
   git config user.name       # → vindicta-bot
   gpg --list-secret-keys     # → agent's GPG key
   gh auth status             # → authenticated as vindicta-bot
   ```

## Windsurf AI + Agent Identity

When using Windsurf's Cascade AI inside the dev container:

- All code written by Cascade and committed through the container terminal will be signed with the `vindicta-bot` GPG key
- The git identity is `vindicta-bot`, not your personal account
- PRs created via `gh pr create` from the terminal use the bot's PAT

> **Tip:** Use Windsurf Cascade to write code, then commit and push from the integrated terminal to maintain the agent identity chain.

## Troubleshooting

<!-- markdownlint-disable MD013 -->
| Issue                              | Fix                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| Dev Containers extension not found | Check Windsurf's extension compatibility; may need the VSIX from VS Code marketplace |
| Container build fails              | Try `Ctrl+Shift+P` → "Dev Containers: Rebuild Without Cache"                         |
| Cascade uses wrong git identity    | Ensure you're using the terminal **inside** the container, not the host terminal     |
<!-- markdownlint-enable MD013 -->
