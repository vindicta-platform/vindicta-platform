---
description: Architecture review for significant changes affecting platform structure
---

# Architecture Review

Global workflow for reviewing changes that impact the platform's structural integrity or cross-package dependencies.

## 1. Context Gathering

1. **Change Analysis**: Review the proposed changes in the PR, Issue, or Specification.
2. **Impact Assessment**: Use `uv tree` and search code to identify affected packages and dependency shifts.
3. **Constitution Check**: Verify alignment with the Platform Constitution at `.specify/memory/constitution.md`.

## 2. Review Process

1. **Domain Isolation**: Ensure changes do not break package boundaries or introduce circular dependencies.
2. **Pattern Matching**: Search for similar implementations in the codebase to ensure consistency.
   ```yaml
   mcp_github-mcp-server_search_code
   query: "org:vindicta-platform <pattern>"
   ```
3. **ADR Verification**: Ensure major structural changes are documented via an ADR in `docs/architecture/adr/`.

## 3. Decision

1. **Approval**: Document approval and link to relevant architectural precedents.
2. **Revision**: Request changes with specific links to architectural violations or suggestions for alternative patterns.

## Leveraging Skills
- Use `git-mcp` to analyze the history of the affected architectural components.
- Use `sdd-workflow` to verify that the specification matches the architectural intent.
