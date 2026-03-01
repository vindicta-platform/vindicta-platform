<#
.SYNOPSIS
    SM End of Day - Daily 6:00 PM
.DESCRIPTION
    Senior Manager end-of-day status: daily summary and aging PR alerts
#>

$ErrorActionPreference = "Continue"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "sm-endday-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

# Import Logic Module
Import-Module "$PSScriptRoot\..\modules\VindictaAgents.Automation.psm1" -Force

Log "=== SM End of Day Started ==="



# Calculate Start of Week (Monday)
$delta = (Get-Date).DayOfWeek.value__ - 1
if ($delta -lt 0) { $delta = 6 }
$startOfWeek = (Get-Date).AddDays(-$delta).ToString("yyyy-MM-dd")

try {
    # Issues closed this week
    Log "Fetching issues closed since $startOfWeek..."
    $closedIssues = Get-GitHubIssues -Query "org:vindicta-platform is:closed is:issue closed:>=$startOfWeek"
    Log "Issues closed (Week): $closedIssues"

    # PRs merged this week
    Log "Fetching PRs merged since $startOfWeek..."
    $mergedPRs = Get-GitHubIssues -Query "org:vindicta-platform is:merged is:pr closed:>=$startOfWeek"
    Log "PRs merged (Week): $mergedPRs"

    # Aging PRs (>24h open)
    Log "Checking for aging PRs..."
    $prsJson = gh pr list --search "org:vindicta-platform state:open" --json number, title, createdAt, url --limit 50 2>$null

    $agingCount = 0
    $criticalCount = 0

    if ($LASTEXITCODE -eq 0 -and $prsJson) {
        $prList = $prsJson | ConvertFrom-Json
        foreach ($pr in $prList) {
            $age = ((Get-Date) - [DateTime]$pr.createdAt).TotalHours
            if ($age -gt 48) {
                Log "  ⚠️ CRITICAL: PR #$($pr.number) - $($pr.title) ($([math]::Round($age))h)"
                $criticalCount++
            }
            elseif ($age -gt 24) {
                Log "  ⏰ AGING: PR #$($pr.number) - $($pr.title) ($([math]::Round($age))h)"
                $agingCount++
            }
        }
        Log "Aging PRs (>24h): $agingCount | Critical (>48h): $criticalCount"
    }

    # Summary
    $statusSummary = @"
- **Closed Issues (Week)**: $closedIssues
- **Merged PRs (Week)**: $mergedPRs
- **Aging PRs**: $agingCount
- **Critical PRs**: $criticalCount
"@

    Log ""
    Log "# SM End of Day Summary - $(Get-Date -Format 'dddd, MMMM dd')"
    Log ($statusSummary -replace "- \*\*", "| " -replace "\*\*:", "" -replace "`n", " ")

    # Update Report
    Log "Updating local agent report..."
    Update-AgentReport -AgentName "SM" -Status $statusSummary -ActivityEntry "End Day completed. Closed (Week): $closedIssues issues, Merged (Week): $mergedPRs PRs."

    # GitHub Sync
    Log "Syncing status to GitHub..."
    $ghSyncSuccess = Sync-GitHubEntity -Query "org:vindicta-platform label:tracking label:sm-agent is:open" -CommentBody "## SM End-Day $(Get-Date -Format 'yyyy-MM-dd')`n$statusSummary"
    if ($ghSyncSuccess) { Log "GitHub sync successful." } else { Log "GitHub sync skipped." }

    # Orchestrator: Trigger Sub-Agents
    Log "--- Triggering Sub-Agent Workflows ---"

    # 1. ADL PR Review (Daily Sweep)
    Log "Triggering ADL-PRReview..."
    & "$PSScriptRoot\Run-ADL-PRReview.ps1"

    # 2. ADL Weekly Report (Fridays)
    if ((Get-Date).DayOfWeek -eq 'Friday') {
        Log "Friday detected: Triggering ADL-WeeklyReport..."
        & "$PSScriptRoot\Run-ADL-WeeklyReport.ps1"
    }

}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Update-AgentReport -AgentName "SM" -Status "ERROR" -ActivityEntry "End Day FAILED: $($_.Exception.Message)"
}

Log "=== SM End of Day Complete ==="
