---
name: bdd-workflow
description: "Behavior Driven Development (BDD) Workflow. Use this skill to construct, execute, and validate Gherkin feature files and Python step definitions. Activates for cross-package integration testing and .feature file work."
---

# `bdd-workflow` Skill (Behavior Driven Development)

Vindicta uses BDD centrally via `packages/features/` to validate cross-package integrations.

## Core Rules

1. **Feature First.** Before changing integration logic, ensure a `.feature` file exists in `packages/features/`.
2. **Given-When-Then.** Use proper Gherkin syntax. See [references/REFERENCE.md](references/REFERENCE.md) for the full syntax guide.
3. **Fail First.** Run `uv run behave` and ensure new steps fail *before* implementing logic.
4. **Implementation.** Never alter the `.feature` file to make a test pass. Fix the step definitions or application code.

## Scaffolding a New Feature

Use the scaffold script to create both a `.feature` file and step definition stubs:

```powershell
scripts/scaffold-feature.ps1 -FeatureName "gas-deduction"
```

This creates:
- `packages/features/gas-deduction.feature`
- `packages/features/steps/test_gas_deduction.py`

Use [assets/feature-template.feature](assets/feature-template.feature) as a reference for structuring scenarios.

## Running BDD Tests

```powershell
# Run all features
scripts/run-bdd.ps1

# Run with tag filter
scripts/run-bdd.ps1 -Tags "@smoke"
```

## Available Resources

| Resource | Path | Purpose |
| :------- | :--- | :------ |
| Feature Scaffolder | [scripts/scaffold-feature.ps1](scripts/scaffold-feature.ps1) | Create .feature + step stubs |
| BDD Runner | [scripts/run-bdd.ps1](scripts/run-bdd.ps1) | Run behave with optional tag filtering |
| Gherkin Reference | [references/REFERENCE.md](references/REFERENCE.md) | Gherkin syntax & behave patterns |
| Feature Template | [assets/feature-template.feature](assets/feature-template.feature) | Gherkin feature file template |
