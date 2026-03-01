<#
.SYNOPSIS
    Register Windows Scheduled Tasks for Vindicta Agents
.DESCRIPTION
    Creates scheduled tasks for all agent workflows
.NOTES
    Run as Administrator
#>

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"
$ScriptsPath = Join-Path $PSScriptRoot "scripts"
$TaskFolder = "\VindictaAgents\"

Write-Host "=== Vindicta Agent Task Registration ===" -ForegroundColor Cyan

# Task definitions
$tasks = @(
    @{ Name = "SM-CheckIn"; Desc = "SM Morning Check-In"; Script = "Run-SM-CheckIn.ps1"; Daily = $true; At = "08:30" }
    @{ Name = "ADL-Standup"; Desc = "ADL Morning Standup"; Script = "Run-ADL-Standup.ps1"; Daily = $true; At = "09:00" }
    @{ Name = "PO-SprintPlanning"; Desc = "PO Monday Planning"; Script = "Run-PO-SprintPlanning.ps1"; Weekly = "Monday"; At = "09:30" }
    @{ Name = "ADL-WeeklyReport"; Desc = "ADL Friday Report"; Script = "Run-ADL-WeeklyReport.ps1"; Weekly = "Friday"; At = "16:00" }
    @{ Name = "ADL-PRReview"; Desc = "ADL Afternoon PR Review"; Script = "Run-ADL-PRReview.ps1"; Daily = $true; At = "17:00" }
    @{ Name = "PO-RoadmapUpdate"; Desc = "PO Daily Roadmap Sync"; Script = "Run-PO-RoadmapUpdate.ps1"; Daily = $true; At = "17:30" }
    @{ Name = "SM-EndDay"; Desc = "SM End of Day Status"; Script = "Run-SM-EndDay.ps1"; Daily = $true; At = "18:00" }
)

foreach ($task in $tasks) {
    $scriptPath = Join-Path $ScriptsPath $task.Script
    Write-Host "`nRegistering: $($task.Name)" -ForegroundColor Yellow

    # Remove existing
    Unregister-ScheduledTask -TaskName $task.Name -TaskPath $TaskFolder -Confirm:$false -ErrorAction SilentlyContinue

    # Create action
    $action = New-ScheduledTaskAction -Execute "pwsh.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""

    # Create trigger
    if ($task.Daily) {
        $trigger = New-ScheduledTaskTrigger -Daily -At $task.At
    }
    else {
        $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $task.Weekly -At $task.At
    }

    # Register
    try {
        Register-ScheduledTask -TaskName $task.Name -TaskPath $TaskFolder -Action $action -Trigger $trigger -Description $task.Desc -User $env:USERNAME
        Write-Host "  Registered: $($task.Name) at $($task.At)" -ForegroundColor Green
    }
    catch {
        Write-Host "  Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== Registration Complete ===" -ForegroundColor Cyan
Write-Host "View: Get-ScheduledTask -TaskPath '$TaskFolder'"
