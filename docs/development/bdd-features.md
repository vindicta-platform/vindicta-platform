# Validating with Centralized BDD Features

The Vindicta Platform relies heavily on Behavior-Driven Development (BDD) to ensure the various independent domain submodules work together successfully.

## The `features` Submodule

All platform-level integration and acceptance tests live in the `features` submodule (mapped to the `packages/features/` directory).

By centralizing these tests, we guarantee that updates to `vindicta-engine`, for instance, do not break expectations established by `warscribe-system` or `vindicta-economy`.

## Running the Tests

To run the full suite from the platform root:

```bash
# Sync all dependencies across the workspace
uv sync

# Run the tests
uv run pytest packages/features/
```

## Writing New Features

1. Define `.feature` files using Gherkin syntax within `packages/features/`.
2. Write corresponding step definitions (in Python) that orchestrate the interactions across the relevant submodule packages. 
3. Ensure all tests run green (`uv run pytest`) before proposing changes that affect multiple domains.
