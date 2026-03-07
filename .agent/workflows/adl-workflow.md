---
description: Agile Delivery Lead daily standup and review routine for the entire workspace.
---

# ADL Workflow

This workflow consolidates standup, PR sweeps, and velocity reporting for the entire Vindicta Platform.

## 1. Daily Standup (9:00 AM)

// turbo
1. **Context Collection**: Analyze `tasks.md` and `ROADMAP.md` in all active packages to identify progress and slipped items.
2. **Issue Scan**: Search for in-progress issues across the organization.
   ```yaml
   mcp_github-mcp-server_search_issues
   query: "org:vindicta-platform is:open label:status:in-progress"
   ```
3. **Blocker Identification**: Flag blockers with comments and timestamp.
4. **Project Sync**: Update GitHub Project boards (e.g., reviews, roadmap).

## 2. PR Review Sweep (5:00 PM)

// turbo
1. **Search PRs**: Find all open PRs in the organization.
   ```yaml
   mcp_github-mcp-server_search_pull_requests
   query: "org:vindicta-platform is:open"
   ```
2. **Review Check**: For each PR, check if it needs a human or Copilot review (based on file count and complexity).
3. **Merge**: Merge PRs that pass all checks and have necessary approvals.

## 3. Weekly Velocity Report (Friday 4:00 PM)

// turbo
1. **Data Gathering**: Retrieve all closed issues and merged PRs for the current week.
2. **Report Generation**: Create or update the weekly report in `automation/reports/`.
3. **Metrics**: Calculate completion rates and cycle times against platform targets.

## Leveraging Skills
- Use `pr-management` skill for all PR interactions.
- Use `git-mcp` skill to verify code provenance if needed.
