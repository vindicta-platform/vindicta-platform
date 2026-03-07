---
description: Product Owner roadmap management, sprint planning, and release coordination.
---

# PO Workflow

Generic workspace-wide workflow for managing product vision, roadmap alignment, and sprint commitments.

## 1. Roadmap Sync (Daily 5:30 PM)

// turbo
1. **Progress Scan**: Search for issues closed today across all repositories.
2. **Roadmap Update**: Update `ROADMAP.md` in relevant packages with current progress status (`[x]`, `[/]`, ⚠️).
3. **Risk Analysis**: Identify if the 6-week roadmap goals are at risk.

## 2. Sprint Planning (Monday 9:30 AM)

// turbo
1. **Goal Setting**: Review overall roadmap and define the goal for the upcoming cycle.
2. **Issue Creation**: Create prioritized GitHub issues (P0-P3) for planned features.
3. **Project Board Alignment**: Add new items to the platform project board and assign to relevant tracks.

## 3. Release Management

// turbo
1. **Changelog Update**: Aggregate merged PRs into the platform `CHANGELOG.md`.
2. **Release Tagging**: Create GitHub releases for stable milestones across relevant packages.

## Leveraging Skills
- Use `pr-management` to track features linked to PRs.
- Use `git-mcp` to search history for roadmap alignment checks.
