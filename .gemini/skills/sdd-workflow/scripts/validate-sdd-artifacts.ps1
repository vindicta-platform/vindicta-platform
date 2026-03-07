<#
.SYNOPSIS
    Validates that the SDD artifacts (spec.md, plan.md, tasks.md) exist for a feature.
.PARAMETER FeatureDir
    Path to the feature specs directory (e.g. specs/005-rag-pipeline).
.EXAMPLE
    .\validate-sdd-artifacts.ps1 -FeatureDir "specs/005-rag-pipeline"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$FeatureDir
)

$ErrorActionPreference = "Stop"

$requiredFiles = @("spec.md", "plan.md", "tasks.md")
$missing = @()
$found = @()

foreach ($file in $requiredFiles) {
    $path = Join-Path $FeatureDir $file
    if (Test-Path $path) {
        $found += $file
    }
    else {
        $missing += $file
    }
}

Write-Host "SDD Artifact Validation for: $FeatureDir" -ForegroundColor Cyan
Write-Host ""

foreach ($f in $found) {
    Write-Host "  [PASS] $f" -ForegroundColor Green
}

foreach ($m in $missing) {
    Write-Host "  [MISSING] $m" -ForegroundColor Red
}

Write-Host ""

if ($missing.Count -gt 0) {
    Write-Host "BLOCKED: Cannot proceed to implementation. Missing artifacts: $($missing -join ', ')" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "All SDD artifacts present. Ready for implementation." -ForegroundColor Green
    exit 0
}
