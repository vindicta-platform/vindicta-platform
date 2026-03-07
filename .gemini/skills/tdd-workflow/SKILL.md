---
name: tdd-workflow
description: "Test Driven Development (TDD) Workflow. Use this skill to strictly enforce the Red-Green-Refactor cycle for all unit-level feature logic. Activates when implementing features within individual packages."
---

# `tdd-workflow` Skill (Test Driven Development)

This skill enforces Principle II: Test-Driven Architecture from the Constitution.

## Strict Red-Green-Refactor Rules

1. **RED (Write the Failing Test FIRST)**
   - Before editing any `src/` code, write the test in `tests/`.
   - Scaffold a failing test:
     ```powershell
     scripts/scaffold-test.ps1 -ModuleName "dice_engine" -PackageName "vindicta-engine"
     ```
   - Run: `uv run pytest <test_file> -v` — confirm it FAILS.

2. **GREEN (Make it Pass)**
   - Implement the minimal code in `src/` to pass the test. No over-engineering (YAGNI).
   - Run: `uv run pytest <test_file> -v` — confirm it PASSES.

3. **REFACTOR (Improve Design)**
   - Clean up code without changing behavior.
   - Run tests again to confirm nothing broke.

## Coverage Validation

Run with coverage threshold enforcement:
```powershell
scripts/run-tests-coverage.ps1 -Package "packages/vindicta-engine" -Threshold 90
```

See [references/REFERENCE.md](references/REFERENCE.md) for pytest patterns, fixtures, and the AAA pattern.

Use [assets/test-template.py](assets/test-template.py) as a starting point for new test files.

## Available Resources

| Resource | Path | Purpose |
| :------- | :--- | :------ |
| Test Scaffolder | [scripts/scaffold-test.ps1](scripts/scaffold-test.ps1) | Scaffold a failing test file |
| Coverage Runner | [scripts/run-tests-coverage.ps1](scripts/run-tests-coverage.ps1) | Run pytest with coverage threshold |
| Pytest Reference | [references/REFERENCE.md](references/REFERENCE.md) | Pytest commands, patterns, quality gates |
| Test Template | [assets/test-template.py](assets/test-template.py) | Python test file template |
