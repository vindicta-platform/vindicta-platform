# Contributing

## 🛡️ Pre-commit Setup

All contributors **must** use `pre-commit` to ensure code quality automatically before submitting changes.

1. Ensure `pre-commit` is installed globally (e.g., `uv tool install pre-commit` or `pip install pre-commit`).
2. Run the following command in the repository root:
   ```bash
   pre-commit install
   ```
This will set up the git hooks to enforce linting and formatting standards prior to any commit.
