# Fix Workspace and Submodule Dependencies

## Problem
When a submodule is cloned standalone (outside the root monorepo workspace), `uv` fails because `[tool.uv.sources]` explicitly specifies `vindicta-foundation = { workspace = true }`, which breaks resolution when the local workspace parent does not exist. Similarly, standalone `uv.lock` files cause versioning conflicts, and duplicate `.gitmodules` entries from prior refactors were causing pathing confusion. 

## Solution
1. **Removed Child `tool.uv.sources`:** Workspace source overrides are now centralized strictly in the root `pyproject.toml`. Children correctly fall back to public/private remote artifact resolution when cloned standalone.
2. **Standardized Root Lock:** All per-submodule `uv.lock` files have been removed, and `.gitignore` has been updated to ignore them inside subpackages. Dependency trees are now strictly managed at the `vindicta-platform` monorepo level.
3. **Build Backend Consolidation:** Ensured `hatchling` is the standardized `build-system` backend over legacy `setuptools` where applicable.
4. **Gitmodule Cleanup:** Dropped invalid root-level `.gitmodules` paths.

## Validation
- `uv sync --all-packages` executes seamlessly from the root `vindicta-platform`.
- Individual submodule standalone clones will no longer error on `workspace = true` definitions.
