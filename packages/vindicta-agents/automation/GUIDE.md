# Vindicta Agent Automation Guide

This guide details the automation infrastructure for Vindicta Agents, covering execution, reporting, and GitHub integration.

## Architecture

```text
automation/
├── scripts/           # Workflow runners (Run-*.ps1)
├── modules/           # Shared logic (VindictaAgents.Automation.psm1)
├── logs/              # Execution logs (*.log)
├── reports/           # Persistent status reports (*_Report.md)
└── Register-AgentTasks.ps1  # Scheduler setup
```

## Reporting System

Agents generate local Markdown reports in `automation/reports/`.

### Report Structure (`<Agent>_Report.md`)
- **Main Header**: Agent Name & Last Update Timestamp.
- **Current Status**: Key metrics from the last run (Week, Issues, PRs).
- **Activity Log**: Reverse-chronological history of actions.

### Usage in Scripts
Use the `Update-AgentReport` function from the module:
```powershell
Update-AgentReport -AgentName "SM" `
    -Status "Week 1: 42 Issues" `
    -ActivityEntry "Check-in complete."
```

## GitHub Integration

Automation scripts sync their status to GitHub to keep the platform up-to-date.

### Sync Logic (`Sync-GitHubEntity`)
The `Sync-GitHubEntity` function searches for a relevant issue (e.g., "Weekly Tracking") and adds a comment.
```powershell
Sync-GitHubEntity `
    -Query "label:tracking label:sm-agent" `
    -CommentBody "## Status Update..."
```
*Note: If no tracking issue is found, the sync is skipped (logged as warning).*

## Testing

We use **Pester** for testing the automation logic.

to run tests:
```powershell
Invoke-Pester -Path .\tests\Automation.Tests.ps1
```
- **Unit Tests**: Verify internal logic.
- **Mock Tests**: Verify API interactions (mocked `gh` and `python`).

## Troubleshooting

- **Logs**: Check `automation/logs/` for detailed execution traces.
- **Reports**: Check `automation/reports/` for high-level status.
- **Scheduler**: Use `Get-ScheduledTask -Taskpath "\VindictaAgents\"` to check trigger status.
