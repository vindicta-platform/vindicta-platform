> **Part of the [Vindicta Platform](https://github.com/vindicta-platform)**

# Vindicta Economy

> 📢 **Notice:** This repository is a Component Submodule of the Vindicta Platform Monorepo. For local development, testing, and dependency resolution, please clone the root [vindicta-platform](https://github.com/vindicta-platform/vindicta-platform) repository.


Ledger, Quotas, and Gas Tank for the Vindicta Platform.

## Installation

```bash
uv sync
```

## Features

- **Atomic Ledger**: Immutable transaction history for platform credits.
- **Gas Tank**: Predictive billing and quota management.
- **Achievements**: Platform-wide achievement and reward system.

## Testing & Coverage

```bash
uv run pytest --cov
uv run behave
```
Coverage Mandate: ≥90%

## Docs

- [Architecture & Standards](https://github.com/vindicta-platform/vindicta-foundation)
- [Economics Technical Specification](docs/index.md)
