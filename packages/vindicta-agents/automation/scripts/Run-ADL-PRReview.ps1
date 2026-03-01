<#
.SYNOPSIS
    ADL PR Review - Daily 5:00 PM
.DESCRIPTION
    Executes the Agile Delivery Lead PR review workflow
#>

$ErrorActionPreference = "Stop"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "adl-pr-review-$(Get-Date -Format 'yyyy-MM-dd').log"

# Import Logic Module
Import-Module "$PSScriptRoot\..\modules\VindictaAgents.Automation.psm1" -Force

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== ADL PR Review Started ==="

try {
    # Get open PRs across organization
    Log "Searching open PRs (Org-Wide)..."
    # using gh search for org-wide visibility
    $prs = gh search prs --state open --owner vindicta-platform --json "number,title,createdAt,author,url" --limit 50 2>&1
    $count = 0
    $reviewNeeded = 0

    if ($LASTEXITCODE -eq 0 -and $prs) {
        $prList = $prs | ConvertFrom-Json
        $count = $prList.Count
        Log "Found $count open PRs"

        foreach ($pr in $prList) {
            $age = ((Get-Date) - [DateTime]$pr.createdAt).TotalHours
            $status = if ($age -gt 48) { "⚠️ AGING" } elseif ($age -gt 24) { "⏰ >24h" } else { "✅ OK" }
            Log "  PR #$($pr.number): $($pr.title) - $status ($([math]::Round($age))h)"
        }
    }

    # Check for PRs without reviews (Simple placeholder logic)
    Log "Checking for PRs without reviews..."
    # In full implementation, we'd query reviewDecision

    $statusSummary = "PR Sweep Complete. Open: $count."

    # Update Report (ADL shares report)
    Log "Updating local agent report..."
    Update-AgentReport -AgentName "ADL" -Status $statusSummary -ActivityEntry "PR Review completed. Found $count open PRs."

}
catch {
    Log "ERROR: $($_.Exception.Message)"
    Update-AgentReport -AgentName "ADL" -Status "ERROR" -ActivityEntry "PR Review FAILED: $($_.Exception.Message)"
}

Log "=== ADL PR Review Complete ==="
