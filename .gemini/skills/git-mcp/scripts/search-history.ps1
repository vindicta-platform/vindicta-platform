<#
.SYNOPSIS
    Searches git history for a string using pickaxe (-S) or regex (-G).
.PARAMETER Query
    The string or regex pattern to search for.
.PARAMETER UseRegex
    If set, uses -G (regex) instead of -S (literal string).
.PARAMETER MaxResults
    Maximum number of commits to return. Default: 20.
.EXAMPLE
    .\search-history.ps1 -Query "VindictaModel" -MaxResults 10
.EXAMPLE
    .\search-history.ps1 -Query "def.*calculate" -UseRegex
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Query,

    [switch]$UseRegex,

    [int]$MaxResults = 20
)

$ErrorActionPreference = "Stop"

if ($UseRegex) {
    $flag = "-G"
} else {
    $flag = "-S"
}

Write-Host "Searching git history for: '$Query' (mode: $flag)" -ForegroundColor Cyan
git log $flag $Query --oneline --source --all -n $MaxResults

if ($LASTEXITCODE -ne 0) {
    Write-Error "git log search failed with exit code $LASTEXITCODE"
    exit 1
}
