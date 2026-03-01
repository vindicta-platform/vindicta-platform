<#
.SYNOPSIS
    SM Morning Check-In - Daily 8:30 AM
.DESCRIPTION
    Senior Manager morning check-in: org-wide status overview
#>

$ErrorActionPreference = "Continue"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "sm-checkin-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

# Import Logic Module
Import-Module "$PSScriptRoot\..\modules\VindictaAgents.Automation.psm1" -Force

Log "=== SM Morning Check-In Started ==="

# Calculate week number
$weekNum = Get-VindictaWeek
Log "Week $weekNum of 6"

try {
    # Org-wide open issues
    Log "Fetching org-wide open issues..."
    $issues = Get-GitHubIssues -Query "org:vindicta-platform is:open is:issue"
    Log "Open issues: $issues"

    # Org-wide open PRs
    Log "Fetching org-wide open PRs..."
    $prs = Get-GitHubIssues -Query "org:vindicta-platform is:open is:pr"
    Log "Open PRs: $prs"

    # Blocked items
    Log "Checking for blocked items..."
    $blocked = Get-GitHubIssues -Query "org:vindicta-platform is:open label:blocked"
    Log "Blocked: $blocked"

    # High priority items
    Log "Checking high priority items..."
    $priority = Get-GitHubIssues -Query "org:vindicta-platform is:open label:priority:high"
    Log "High Priority: $priority"

    # Summary construction
    $statusSummary = @"
- **Week**: $weekNum
- **Open Issues**: $issues
- **Open PRs**: $prs
- **Blocked Items**: $blocked
- **High Priority**: $priority
"@

    Log ""
    Log "# SM Check-In Summary - $(Get-Date -Format 'dddd, MMMM dd')"
    Log ($statusSummary -replace "- \*\*", "| " -replace "\*\*:", "" -replace "`n", " ")

    # [NEW] Update Local Report
    Log "Updating local agent report..."
    Update-AgentReport -AgentName "SM" -Status $statusSummary -ActivityEntry "Morning Check-In completed. Found $issues issues, $prs PRs."

    # [NEW] Sync to GitHub
    Log "Syncing status to GitHub..."
    # Example: Sync to a weekly tracking issue (assuming one exists with label 'tracking' and 'week-X')
    $ghSyncSuccess = Sync-GitHubEntity -Query "org:vindicta-platform label:tracking label:sm-agent is:open" -CommentBody "## SM Check-In $(Get-Date -Format 'yyyy-MM-dd')`n$statusSummary"
    if ($ghSyncSuccess) { Log "GitHub sync successful." } else { Log "GitHub sync skipped (no tracking issue found)." }

    # Orchestrator: Trigger Sub-Agents
    Log "--- Triggering Sub-Agent Workflows ---"

    # 1. ADL Standup (Daily)
    Log "Triggering ADL-Standup..."
    & "$PSScriptRoot\Run-ADL-Standup.ps1"

    # 2. PO Roadmap Update (Daily)
    Log "Triggering PO-RoadmapUpdate..."
    & "$PSScriptRoot\Run-PO-RoadmapUpdate.ps1"

    # 3. PO Sprint Planning (Mondays)
    if ((Get-Date).DayOfWeek -eq 'Monday') {
        Log "Monday detected: Triggering PO-SprintPlanning..."
        & "$PSScriptRoot\Run-PO-SprintPlanning.ps1"
    }
}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Update-AgentReport -AgentName "SM" -Status "ERROR" -ActivityEntry "Check-In FAILED: $($_.Exception.Message)"
}

Log "=== SM Morning Check-In Complete ==="
