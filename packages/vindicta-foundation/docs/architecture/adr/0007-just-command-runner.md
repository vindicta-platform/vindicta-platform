# ADR-0007: Just as the Command Runner

## Status
Accepted

## Context
Developer environments across different operating systems consistently struggle with command runners. Scripts often reside in `make` (which lacks native Windows support), `npm package.json` (which requires node.js), or undocumented `uv run` / shell scripts. Lengthy commands for formatting, testing, and continuous integration can easily be mistyped or forgotten, leading to DX friction.

## Decision
We will use [`just`](https://github.com/casey/just) as the primary command runner for the `vindicta-foundation` repository and strongly recommend its use across the platform.

### Rationale
- **Cross-Platform by Default**: `just` runs identical recipes on Windows, macOS, and Linux, which aligns well with our developer ecosystem.
- **Self-Documenting**: Running `just` without arguments lists all available commands with their comments, making onboarding frictionless.
- **Dependency Management**: We can easily chain tasks (e.g., `prepush` running `lint` then `test`), similar to `make` but without the idiosyncrasies of Makefiles (like tab requirements).
- **Environment Isolation**: It plays perfectly well with `uv run`, allowing us to explicitly invoke our sealed virtual environment commands.

## Consequences
- Developers are highly encouraged to install `just` to maximize their DX, though the native `uv run` commands remain accessible as fallbacks.
- New scripts and automation tasks must be added to the `Justfile` instead of standalone `.bat` or `.sh` files where applicable.
