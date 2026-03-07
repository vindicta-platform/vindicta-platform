# Developer Guide: Working with Submodules

The Vindicta Platform Orchestrator connects many independent repositories using Git submodules. This allows developers to pull down the entire platform context easily while maintaining strict boundaries between decoupled domains.

## Initial Setup

When cloning the repository for the first time, use `--recurse-submodules`:

```bash
git clone --recurse-submodules https://github.com/vindicta-platform/vindicta-platform.git
cd vindicta-platform
```

If you already cloned it without the flag, initialize them manually:
```bash
git submodule update --init --recursive
```

## Pulling Latest Changes

To sync the `vindicta-platform` repository and fetch the latest main branch heads for all submodules simultaneously:

```bash
git pull --recurse-submodules
git submodule update --remote --recursive
```

## Making Changes Across Submodules

Each submodule (e.g., `packages/vindicta-foundation`) is a full standard Git repository. 

1. `cd` into the submodule directory:
   ```bash
   cd packages/vindicta-engine
   ```
2. Checkout a new branch or `main` (submodules default to a detached HEAD):
   ```bash
   git checkout -b feature/new-dice-roller
   ```
3. Make your changes, commit, and push from within that directory.
4. **Crucial Next Step**: After a submodule branch is merged to its `main`, you must return to the root `vindicta-platform` directory and commit the submodule pointer update:
   ```bash
   cd ../../
   git add packages/vindicta-engine
   git commit -m "chore: bump vindicta-engine to latest"
   ```

## Using `uv` Workspaces

Because we use `uv` workspaces defined in `pyproject.toml`, any change you make inside `packages/vindicta-engine` is immediately available to `packages/warscribe-system` (assuming they depend on each other) without needing to rebuild or reinstall packages across the submodules.

To sync all dependencies across the entire mono-workspace:
```bash
uv sync
```
