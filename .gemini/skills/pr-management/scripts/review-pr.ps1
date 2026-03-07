<#
.SYNOPSIS
    Lists open PRs and optionally shows detailed diff for a specific PR.
.PARAMETER PrNumber
    Optional PR number to view in detail.
.EXAMPLE
    .\review-pr.ps1
.EXAMPLE
    .\review-pr.ps1 -PrNumber 42
#>
param(
    [int]$PrNumber = 0
)

$ErrorActionPreference = "Stop"

if ($PrNumber -eq 0) {
    Write-Host "Open Pull Requests:" -ForegroundColor Cyan
    gh pr list --state open
}
else {
    Write-Host "PR #$PrNumber Details:" -ForegroundColor Cyan
    gh pr view $PrNumber
    Write-Host ""
    Write-Host "PR #$PrNumber Diff:" -ForegroundColor Cyan
    gh pr diff $PrNumber
}
