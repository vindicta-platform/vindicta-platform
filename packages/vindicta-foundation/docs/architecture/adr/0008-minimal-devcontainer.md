# ADR-0008: Minimal Devcontainer Configuration

**Status**: Accepted
**Date**: 2026-02-21
**Decision Makers**: Brandon Fox

## Context

The Foundation devcontainer was initially over-engineered with a custom `Dockerfile` (to fix a Yarn GPG key issue), an `init.sh` bootstrap script (to install `uv`, `just`, clone context repos, and seed `.gemini` knowledge), and multiple devcontainer features (`common-utils`, `docker-outside-of-docker`, `github-cli`).

This caused persistent build and startup failures:

- The `docker-outside-of-docker` feature's `socat` entrypoint blocked the container's main process.
- The custom `Dockerfile` layered unnecessary complexity on top of the Microsoft image.
- The `init.sh` script introduced fragile multi-step bootstrapping.
- Stale `.venv` directories owned by root from Docker test runs caused `uv sync` permission failures.
- The Antigravity IDE's devcontainer CLI does not stream `postCreateCommand` output, making all these failures appear as silent hangs.

## Decision

Apply YAGNI. The devcontainer configuration is reduced to a single 7-line `devcontainer.json`:

```json
{
    "name": "Vindicta Foundation",
    "image": "mcr.microsoft.com/devcontainers/python:1-3.12-bookworm",
    "containerEnv": { "UV_LINK_MODE": "copy" },
    "postCreateCommand": "pipx install uv && uv sync --all-extras"
}
```

No `Dockerfile`. No `init.sh`. No extra features. The Microsoft Python base image already provides `pipx`, `git`, `gh`, the `vscode` user, and proper devcontainer lifecycle handling.

## Consequences

### Positive

- Zero-config onboarding: open repo → Rebuild in Container → working environment
- No custom Dockerfile to maintain or debug
- No shell script failure modes
- Eliminates all observed startup hang/failure patterns

### Negative

- `just` is not pre-installed (install manually with `uv tool install rust-just`)
- Context repos from other platform domains are not auto-cloned (clone manually as needed)

### Neutral

- Yarn GPG key issue in the Microsoft image is not triggered because we don't install features that run `apt-get update`

## Alternatives Considered

1. **Custom Dockerfile + init.sh**: Over-engineered, fragile, multiple failure modes.
2. **Vanilla `python:3.12-bookworm` image**: Lacks devcontainer lifecycle plumbing (no `vscode` user, no `pipx`, Antigravity CLI probe hangs).
3. **Pre-built custom Docker image**: Adds registry dependency and image maintenance burden.

## References

- [Devcontainer specification](https://containers.dev/implementors/json_reference/)
- [Microsoft Python devcontainer images](https://github.com/devcontainers/images/tree/main/src/python)
