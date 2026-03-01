<#
.SYNOPSIS
    Vindicta Agents Automation Logic Module
.DESCRIPTION
    Contains reusable logic for agent automation workflows to enable unit testing.
#>

function Get-VindictaWeek {
    <#
    .SYNOPSIS
        Calculates the current week number in the 6-week roadmap.
    #>
    param (
        [DateTime]$StartDate = "2026-02-04",
        [DateTime]$CurrentDate = (Get-Date)
    )

    $days = ($CurrentDate - $StartDate).Days + 1
    return [math]::Ceiling($days / 7)
}

function Get-GitHubIssues {
    <#
    .SYNOPSIS
        Wraps 'gh api' call for searching issues.
    #>
    param (
        [string]$Query
    )

    try {
        $json = gh api -X GET "/search/issues" -f q=$Query --jq '.total_count' 2>&1
        if ($LASTEXITCODE -eq 0) {
            return [int]$json
        }
        Write-Error "GitHub CLI Error: $json"
    }
    catch {
        Write-Error $_.Exception.Message
    }
    return 0
}

function Submit-AgentTask {
    <#
    .SYNOPSIS
        Submits a task to the Agent-Auditor-SDK queue.
        Uses pure shell execution to allow mocking in Pester tests.
    #>
    param (
        [string]$Prompt,
        [string]$Priority = "normal"
    )

    try {
        # Integration point: python -m agent_auditor submit ...
        # Using Invoke-Expression or direct execution for testability
        $output = python -m agent_auditor submit "$Prompt" --priority $Priority --json 2>&1

        if ($LASTEXITCODE -eq 0) {
            return ($output | ConvertFrom-Json)
        }
        Write-Error "SDK Error: $output"
    }
    catch {
        Write-Error $_.Exception.Message
    }
    return $null
}

function Update-AgentReport {
    <#
    .SYNOPSIS
        Updates the local markdown report for a specific agent.
    #>
    param (
        [string]$AgentName,
        [string]$Status,
        [string]$ActivityEntry
    )

    $ReportDir = Join-Path $PSScriptRoot "..\reports"
    if (-not (Test-Path $ReportDir)) { New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null }

    $ReportFile = Join-Path $ReportDir "${AgentName}_Report.md"
    $Date = Get-Date -Format "yyyy-MM-dd HH:mm"

    # Header & Status Section
    $ReportContent = @"
# $AgentName Automation Report
**Last Updated**: $Date

## Current Status
$Status

## Activity Log
"@

    # Read existing log if file exists
    $ExistingLog = ""
    if (Test-Path $ReportFile) {
        $RawContent = Get-Content $ReportFile -Raw
        if ($RawContent -match "## Activity Log\s+([\s\S]*)") {
            $ExistingLog = $matches[1].Trim()
        }
    }

    # Prepend new entry
    $NewLogEntry = "- **$Date**: $ActivityEntry"
    $FullLog = "$NewLogEntry`n$ExistingLog"

    # Write full report
    "$ReportContent`n$FullLog" | Set-Content $ReportFile -Encoding UTF8
}

function Sync-GitHubEntity {
    <#
    .SYNOPSIS
        Updates a GitHub issue with automation status.
        Searches for an issue matching 'Query' and adds a comment.
    #>
    param (
        [string]$Query,
        [string]$CommentBody
    )

    try {
        # Find issue URL/Number
        $issueUrl = gh issue list --search "$Query" --json url --jq '.[0].url' 2>&1

        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($issueUrl)) {
            # Add comment
            gh issue comment $issueUrl --body "$CommentBody" 2>&1 | Out-Null
            return $true
        }
        else {
            Write-Warning "No GitHub issue found for query: $Query"
            return $false
        }
    }
    catch {
        Write-Error "GitHub Sync Error: $($_.Exception.Message)"
        return $false
    }
}

Export-ModuleMember -Function Get-VindictaWeek, Get-GitHubIssues, Submit-AgentTask, Update-AgentReport, Sync-GitHubEntity
