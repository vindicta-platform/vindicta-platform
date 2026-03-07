---
description: General developer workflow for implementation and bug fixing.
---

# Developer Workflow

Generic workflow for feature implementation and bug fixing, following the platform's engineering standards.

## 1. Requirement Analysis

1. **Review Specification**: Read the `spec.md` or Issue description.
2. **Clarification**: Ask for details if requirements or edge cases are underspecified.

## 2. Iterative Development

1. **Branching**: Create a feature or bugfix branch.
   ```powershell
   git checkout -b <type>/<id>-<summary>
   ```
2. **TDD Cycle**:
   - Write failing test in `tests/` (`tdd-workflow`).
   - Implement minimal code in `src/`.
   - Pass test.
   - Refactor.
3. **BDD Verification**: Run integration tests if applicable (`bdd-workflow`).

## 3. Submission

1. **Commit**: Use `/commit` workflow intent.
2. **Push**: Sync branch with origin.
3. **PR Creation**: Use `/pr` workflow intent.

## Leveraging Skills
- **tdd-workflow**: For unit tests.
- **bdd-workflow**: For integration tests.
- **git-mcp**: For commit hygiene.
- **pr-management**: For PR creation.
