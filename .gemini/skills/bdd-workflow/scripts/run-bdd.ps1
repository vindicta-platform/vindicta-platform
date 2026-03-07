<#
.SYNOPSIS
    Runs BDD tests via behave and reports results.
.PARAMETER Tags
    Optional behave tag expression to filter scenarios (e.g. "@smoke").
.PARAMETER FeaturesDir
    Path to the features directory. Default: packages/features.
.EXAMPLE
    .\run-bdd.ps1
.EXAMPLE
    .\run-bdd.ps1 -Tags "@smoke"
#>
param(
    [string]$Tags = "",
    [string]$FeaturesDir = "packages/features"
)

$ErrorActionPreference = "Stop"

$cmd = "uv run behave $FeaturesDir"
if ($Tags -ne "") {
    $cmd += " --tags=$Tags"
}

Write-Host "Running BDD tests: $cmd" -ForegroundColor Cyan
Invoke-Expression $cmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "BDD tests FAILED" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "BDD tests PASSED" -ForegroundColor Green
    exit 0
}
