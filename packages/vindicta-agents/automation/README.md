# Vindicta Agent Automation

Windows Task Scheduler automation for AI agent workflows.

## Schedule

| Time | Agent | Workflow | Task Name |
|------|-------|----------|-----------|
| 8:30 AM | SM | `/sm-check-in` | VindictaAgents\SM-CheckIn |
| 9:00 AM | ADL | `/adl-standup` | VindictaAgents\ADL-Standup |
| Monday 9:30 AM | PO | `/po-sprint-planning` | VindictaAgents\PO-SprintPlanning |
| Friday 4:00 PM | ADL | `/adl-weekly-report` | VindictaAgents\ADL-WeeklyReport |
| 5:00 PM | ADL | `/adl-pr-review` | VindictaAgents\ADL-PRReview |
| 5:30 PM | PO | `/po-roadmap-update` | VindictaAgents\PO-RoadmapUpdate |
| 6:00 PM | SM | `/sm-end-day` | VindictaAgents\SM-EndDay |

## Setup

```powershell
# Run as Administrator
.\Register-AgentTasks.ps1
```

## Scripts

- `Run-SM-CheckIn.ps1` — Morning check-in (org-wide status)
- `Run-ADL-Standup.ps1` — Morning standup
- `Run-PO-SprintPlanning.ps1` — Monday planning
- `Run-ADL-WeeklyReport.ps1` — Friday velocity report
- `Run-ADL-PRReview.ps1` — Afternoon PR sweep
- `Run-PO-RoadmapUpdate.ps1` — Daily roadmap sync
- `Run-SM-EndDay.ps1` — End of day status

## Logs

Logs are written to `automation/logs/` with daily rotation.

## Manual Execution

```powershell
# Run a task immediately
Start-ScheduledTask -TaskPath "\VindictaAgents\" -TaskName "ADL-Standup"

# Or run script directly
.\scripts\Run-ADL-Standup.ps1
```
