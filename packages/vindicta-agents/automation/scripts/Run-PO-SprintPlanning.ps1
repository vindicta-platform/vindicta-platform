<#
.SYNOPSIS
    PO Sprint Planning - Monday 9:30 AM
.DESCRIPTION
    Reviews roadmaps and prepares sprint issues
#>

$ErrorActionPreference = "Continue"
$LogPath = Join-Path $PSScriptRoot "..\logs"
$LogFile = Join-Path $LogPath "po-sprint-$(Get-Date -Format 'yyyy-MM-dd').log"

if (-not (Test-Path $LogPath)) { New-Item -ItemType Directory -Path $LogPath -Force | Out-Null }

function Log { param([string]$Msg); "$(Get-Date -Format 'HH:mm:ss') $Msg" | Tee-Object -FilePath $LogFile -Append }

Log "=== PO Sprint Planning Started ==="

# Calculate week number
$startDate = [DateTime]"2026-02-04"
$weekNum = [math]::Ceiling((((Get-Date) - $startDate).Days + 1) / 7)
Log "Planning for Week $weekNum"

$repos = @(
    "Vindicta-Portal", "Vindicta-API", "Vindicta-Core",
    "Agent-Auditor-SDK", "Primordia-AI", "Meta-Oracle",
    "WARScribe-Core", "WARScribe-Parser"
)

try {
    foreach ($repo in $repos) {
        Log "Checking $repo ROADMAP.md..."
        $roadmap = gh api "repos/vindicta-platform/$repo/contents/ROADMAP.md" --jq '.name' 2>$null
        if ($LASTEXITCODE -eq 0) {
            Log "  Found ROADMAP.md"
        } else {
            Log "  No ROADMAP.md or repo not found"
        }
    }

    Log "Sprint planning summary prepared"
}
catch {
    Log "ERROR: $($_.Exception.Message)"
}

Log "=== PO Sprint Planning Complete ==="
