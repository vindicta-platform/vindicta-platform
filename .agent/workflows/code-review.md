---
description: Comprehensive code review with mentoring feedback
---

# Code Review Workflow

Standardizes how Senior Software Engineers and other roles review code changes.

## 1. Context Assessment

1. **Read Spec/Issue**: Understand the business requirement.
2. **Examine Diff**: Use the `pr-management` skill to view the PR diff.
   ```powershell
   scripts/review-pr.ps1 -PrNumber <num>
   ```

## 2. Technical Quality Gate

- **TDD/BDD**: Verify that new tests were added and they cover the acceptance criteria.
- **Complexity**: Identify over-engineering (YAGNI violations).
- **Architecture**: Check for domain boundary violations (Platform over Silo).

## 3. Mentoring Feedback

1. **Positive Reinforcement**: Highlight well-structured or clever implementations.
2. **Actionable Improvements**: Suggest specific refactors or alternative patterns.
3. **Draft Review**: Use `gh pr review` to submit comments (Review, Request Changes, or Approve).

## Leveraging Skills
- **pr-management**: For diff viewing and review submission.
- **git-mcp**: To check history of modified lines (blame/log).
