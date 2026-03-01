<#
.SYNOPSIS
    ADL Morning Standup - Daily 9:00 AM
.DESCRIPTION
    Executes the Agile Delivery Lead standup workflow via Gemini CLI
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "adl-standup-$(Get-Date -Format 'yyyy-MM-dd').log"

# Import Logic Module
Import-Module "$PSScriptRoot\..\modules\VindictaAgents.Automation.psm1" -Force

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== ADL Standup Started ==="

# Calculate week number
$weekNum = Get-VindictaWeek
Log "Week $weekNum of 6"

try {
    Log "Fetching open issues..."
    $issues = Get-GitHubIssues -Query "org:vindicta-platform is:open is:issue"
    Log "Open issues: $issues"

    Log "Fetching open PRs..."
    $prs = Get-GitHubIssues -Query "org:vindicta-platform is:open is:pr"
    Log "Open PRs: $prs"

    Log "Fetching blocked issues..."
    $blocked = Get-GitHubIssues -Query "org:vindicta-platform is:open label:blocked"
    Log "Blocked: $blocked"

    # Summary
    $statusSummary = @"
- **Week**: $weekNum
- **Open Issues**: $issues
- **Open PRs**: $prs
- **Blocked**: $blocked
"@
    Log ""
    Log "# Daily Standup - $(Get-Date -Format 'dddd, MMMM dd')"
    Log ($statusSummary -replace "- \*\*", "| " -replace "\*\*:", "" -replace "`n", " ")

    # Update Report
    Log "Updating local agent report..."
    Update-AgentReport -AgentName "ADL" -Status $statusSummary -ActivityEntry "Standup completed. Week $weekNum. Open: $issues, Blocked: $blocked."

    # GitHub Sync
    Log "Syncing status to GitHub..."
    $ghSyncSuccess = Sync-GitHubEntity -Query "org:vindicta-platform label:tracking label:adl-agent is:open" -CommentBody "## ADL Standup $(Get-Date -Format 'yyyy-MM-dd')`n$statusSummary"
    if ($ghSyncSuccess) { Log "GitHub sync successful." } else { Log "GitHub sync skipped." }

}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Update-AgentReport -AgentName "ADL" -Status "ERROR" -ActivityEntry "Standup FAILED: $($_.Exception.Message)"
}

Log "=== ADL Standup Complete ==="
