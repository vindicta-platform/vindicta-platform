---
name: sdd-workflow
description: "Spec Driven Development (SDD) Workflow. Use this skill to enforce creating and validating functional specifications (spec.md) before technical design (plan.md) and task breakdown (tasks.md). Activates for any complex feature implementation."
---

# `sdd-workflow` Skill (Spec Driven Development)

Vindicta heavily relies on SDD. Code is the *output* of the specification process, not the beginning of it.

## The Core Process

1. **Specify (`spec.md`)**: Define the *what* and *why*. User-centric.
   - Use `/speckit.specify` or follow `.specify/templates/spec-template.md`.
   - Must include prioritized User Scenarios mapped to Independent Tests.
2. **Plan (`plan.md`)**: Define the *how*. Technical translation of the spec.
   - Use `/speckit.plan`. Must pass the Constitution Check gate.
3. **Tasks (`tasks.md`)**: Define the *steps*.
   - Use `/speckit.tasks`. Tasks grouped by User Story from `spec.md`.

See [assets/sdd-lifecycle.md](assets/sdd-lifecycle.md) for the visual flow diagram.

## Validation Gate

Before implementing, verify all artifacts exist:
```powershell
scripts/validate-sdd-artifacts.ps1 -FeatureDir "specs/005-rag-pipeline"
```

This checks that `spec.md`, `plan.md`, and `tasks.md` all exist. Implementation is BLOCKED if any are missing.

See [references/REFERENCE.md](references/REFERENCE.md) for the full speckit command reference and artifact layout.

## Available Resources

| Resource | Path | Purpose |
| :------- | :--- | :------ |
| Artifact Validator | [scripts/validate-sdd-artifacts.ps1](scripts/validate-sdd-artifacts.ps1) | Verify spec/plan/tasks exist |
| Speckit Reference | [references/REFERENCE.md](references/REFERENCE.md) | Command reference & artifact layout |
| Lifecycle Diagram | [assets/sdd-lifecycle.md](assets/sdd-lifecycle.md) | Mermaid flow diagram of SDD lifecycle |
