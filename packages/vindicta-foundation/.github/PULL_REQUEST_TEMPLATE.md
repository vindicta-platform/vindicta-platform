## Description
<!-- Describe your changes in detail here. Explain the motivation and rationale. -->

## Foundation Law & Architectural Decision Checklist
Please cross off any items that do not apply by striking them out (e.g. ~~- [ ] N/A~~), but do not delete them.

- [ ] Does this PR adhere to all **Zero-Order Axioms** outlined in `docs/constitution.md`?
- [ ] For any architectural decisions, has an ADR been introduced or an existing ADR updated in `docs/architecture/adr/`?

## Development Quality Checklist
- [ ] My code includes full rigorous test coverage (>=90%) for the introduced behaviors.
- [ ] My code strictly adheres to the type checking models and passes all `mypy` verifications.
- [ ] I have run `uv run ruff check` and `uv run ruff format` and have no remaining issues.
- [ ] Any related documentation has been created or updated (and `uv run mkdocs build --strict` succeeded).
- [ ] If this PR adds or deprecates features, I have added a valid `towncrier` fragment to the `news/` folder.

## Linked Issue
<!-- Link to any relevant issue (e.g. Closes #123) -->
