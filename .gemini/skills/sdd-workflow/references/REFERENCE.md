# Spec Driven Development Reference

## The SDD Lifecycle

```
Specify (spec.md) → Plan (plan.md) → Tasks (tasks.md) → Implement → Validate
```

## Speckit Commands

| Command               | Purpose                                    | Input Required         |
| :-------------------- | :----------------------------------------- | :--------------------- |
| `/speckit.specify`    | Create feature specification               | Feature description    |
| `/speckit.clarify`    | Identify & resolve ambiguities in spec     | Existing spec.md       |
| `/speckit.plan`       | Generate technical implementation plan     | Approved spec.md       |
| `/speckit.tasks`      | Break plan into ordered tasks              | Approved plan.md       |
| `/speckit.implement`  | Execute tasks from tasks.md                | Approved tasks.md      |
| `/speckit.analyze`    | Cross-artifact consistency check           | spec + plan + tasks    |
| `/speckit.checklist`  | Generate a domain-specific checklist       | Feature context        |

## Artifact Locations

All spec artifacts live under `specs/<###-feature-name>/`:

```text
specs/005-rag-pipeline/
├── spec.md         # User scenarios & requirements
├── plan.md         # Technical design & constitution check
├── research.md     # Phase 0 research findings
├── data-model.md   # Entity definitions
├── contracts/      # Interface contracts
├── tasks.md        # Implementation task list
└── quickstart.md   # Getting started guide
```

## Constitution Alignment

Every `plan.md` MUST pass the Constitution Check gate before implementation:

- **I. Platform over Silo**: Typed interfaces via `vindicta-foundation`
- **II. Test-Driven Architecture**: 90% coverage, tests first
- **III. Transparent Decisions**: ADR for architectural changes
- **IV. Observability & Logging**: Structured logging required
- **V. Simplicity (YAGNI)**: No speculative complexity
