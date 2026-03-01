# PyCharm Dev Container Setup

> **Requires:** PyCharm 2023.3+ (Professional) or IntelliJ IDEA Ultimate
> with Docker plugin. Community Edition does **not** support dev containers natively.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) running
- [PyCharm Professional](https://www.jetbrains.com/pycharm/) 2023.3+
- Docker plugin enabled (Settings → Plugins → Docker)

## Option A: Native Dev Container Support (PyCharm 2023.3+)

1. **Open the repo** in PyCharm: `File → Open → Vindicta-Agents/`

2. **PyCharm detects `.devcontainer/devcontainer.json`** and shows a notification:
   > "Dev container configuration detected"

   Click **"Create Dev Container and Mount Sources"**.

3. **Wait for the build.** PyCharm will:
   - Build the Docker image
   - Mount the project sources
   - Run `init-agent.sh` via `postCreateCommand`

4. **Open the terminal** (`Alt+F12`) to verify:

   ```bash
   git config user.name    # → vindicta-bot
   gpg --list-secret-keys  # → shows the agent's key
   ```

## Option B: Docker Interpreter (Older PyCharm)

If your PyCharm version doesn't support dev containers natively:

1. **Build the image manually:**

   ```powershell
   docker build --no-cache -t vindicta-agent .devcontainer/
   ```

2. **Add Docker interpreter:**
   - `File → Settings → Project → Python Interpreter → Add Interpreter`
   - Select **Docker**
   - Image: `vindicta-agent`

3. **Run init script manually** in the Docker terminal:

   ```bash
   init-agent.sh
   ```

## Option C: Docker Compose Wrapper

For full dev container features without native support, use `docker-compose`:

1. Create `docker-compose.dev.yml` in repo root:

   ```yaml
   version: '3.8'
   services:
     agent:
       build: .devcontainer/
       env_file: .devcontainer/.env
       volumes:
         - .:/workspace
         - ./.keys:/output
       working_dir: /workspace
       command: sleep infinity
   ```

2. Start:

   ```powershell
   docker compose -f docker-compose.dev.yml up -d
   docker compose -f docker-compose.dev.yml exec agent init-agent.sh
   ```

3. In PyCharm: `File → Settings → Project → Python Interpreter → Docker Compose`

## Troubleshooting

| Issue                           | Fix                                           |
| ------------------------------- | --------------------------------------------- |
| "Dev containers not supported"  | Upgrade to PyCharm Professional 2023.3+       |
| Docker connection failed        | Settings → Build → Docker → verify connection |
| `postCreateCommand` not running | Run `init-agent.sh` manually in terminal      |
