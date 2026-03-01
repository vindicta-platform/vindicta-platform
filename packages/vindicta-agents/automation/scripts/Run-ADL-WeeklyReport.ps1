<#
.SYNOPSIS
    ADL Weekly Report - Friday 4:00 PM
.DESCRIPTION
    Generates weekly velocity report
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "adl-weekly-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== ADL Weekly Report Started ==="

$mondayDate = (Get-Date).AddDays(-((Get-Date).DayOfWeek.value__ - 1)).ToString("yyyy-MM-dd")
Log "Week starting: $mondayDate"

try {
    # Closed issues this week
    Log "Fetching closed issues..."
    $closed = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:closed is:issue closed:>=$mondayDate" --jq '.total_count' 2>&1
    Log "Issues closed: $closed"

    # Merged PRs this week
    Log "Fetching merged PRs..."
    $merged = gh api -X GET "/search/issues" -f q="org:vindicta-platform is:merged is:pr merged:>=$mondayDate" --jq '.total_count' 2>&1
    Log "PRs merged: $merged"

    # Generate report
    $report = @"

# Weekly Velocity Report
Week of $mondayDate

| Metric | Value |
|--------|-------|
| Issues Closed | $closed |
| PRs Merged | $merged |

---
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
"@
    Log $report
}
catch {
    Log "ERROR: $($_.Exception.Message)"
}

Log "=== ADL Weekly Report Complete ==="
