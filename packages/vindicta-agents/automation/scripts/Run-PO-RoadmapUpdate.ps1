<#
.SYNOPSIS
    PO Roadmap Update - Daily 5:30 PM
.DESCRIPTION
    Syncs ROADMAP.md files with current progress
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "po-roadmap-$(Get-Date -Format 'yyyy-MM-dd').log"

# Import Logic Module
Import-Module "$PSScriptRoot\..\modules\VindictaAgents.Automation.psm1" -Force

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== PO Roadmap Update Started ==="

$today = Get-Date -Format "yyyy-MM-dd"

try {
    # Get issues closed today
    Log "Fetching issues closed today..."
    # We use gh raw for specific formatted output if needed, or Get-GitHubIssues for count
    # Let's use gh directly for the list of titles, as the module currently only returns COUNT.
    # TODO: Enhance module to return objects. For now, we wrap gh here.

    $closedJson = gh api "/search/issues?q=org:vindicta-platform+is:closed+is:issue+closed:>=$today" --jq '.items[].title' 2>&1
    $closedCount = 0

    if ($LASTEXITCODE -eq 0 -and $closedJson) {
        $titles = $closedJson -split "`n"
        $closedCount = $titles.Count
        Log "Closed today ($closedCount):"
        $titles | ForEach-Object { Log "  $_" }
    }
    else {
        Log "No issues closed today"
    }

    $statusSummary = "Synced. Closed Today: $closedCount"

    Log "Roadmap sync complete"

    # Update Report
    Log "Updating local agent report..."
    Update-AgentReport -AgentName "PO" -Status $statusSummary -ActivityEntry "Roadmap sync completed. Closed today: $closedCount."

    # GitHub Sync (Optional for PO, maybe update roadmap tracking issue)

}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Update-AgentReport -AgentName "PO" -Status "ERROR" -ActivityEntry "Roadmap Sync FAILED: $($_.Exception.Message)"
}

Log "=== PO Roadmap Update Complete ==="
