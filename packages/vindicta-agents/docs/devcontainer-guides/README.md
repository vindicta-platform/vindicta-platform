# Dev Container Setup Guides

This directory contains IDE-specific guides for working with the Vindicta Agent dev container.

| Guide                         | IDE                          |
| ----------------------------- | ---------------------------- |
| [VSCode](vscode.md)           | Visual Studio Code           |
| [PyCharm](pycharm.md)         | JetBrains PyCharm / IntelliJ |
| [Windsurf](windsurf.md)       | Codeium Windsurf             |
| [Antigravity](antigravity.md) | Google Antigravity           |
| [Docker CLI](docker-cli.md)   | Manual / headless            |

## Prerequisites (All IDEs)

1. **Docker Desktop** installed and running
2. **Git** installed
3. **Clone the repo:**

   ```bash
   git clone https://github.com/vindicta-platform/Vindicta-Agents.git
   cd Vindicta-Agents
   ```

4. **Create your `.env` file:**

   ```bash
   cp .devcontainer/.env.example .devcontainer/.env
   # Edit .devcontainer/.env with your secrets
   ```
