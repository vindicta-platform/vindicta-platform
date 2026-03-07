---
description: Senior Manager daily routine for platform status and blocker escalation.
---

# SM Workflow

Unified management routine to ensure platform health and coordinate between ADL and PO roles.

## 1. Daily Check-In (8:30 AM)

// turbo-all
1. **Aggregated Status**: Execute `/adl-workflow` (Standup) and `/po-workflow` (Roadmap Sync) intent to gather the current platform state.
2. **Platform Health Scan**: Count open issues by severity and identify stale PRs (>48h).
3. **Blocker Scrub**: Aggregate and prioritize blockers requiring escalation.
4. **Platform Status Report**: Generate a high-level report covering sprint execution, roadmap alignment, and health metrics.

## 2. Work Initialization / End-of-Day

// turbo
1. **Start Work**: Synchronize local workspace, check for critical upstream changes, and review the daily playbook.
2. **End-of-Day**: Summarize achieved progress, ensure all commits are pushed, and update the flight recorder.

## Leveraging Skills
- Use `pr-management` to monitor PR cycle times.
- Use `git-mcp` to verify workspace synchronization.
