<#
.SYNOPSIS
    Runs pytest with coverage and checks against the 90% threshold.
.PARAMETER Package
    Package directory to test. Default: current directory.
.PARAMETER Threshold
    Minimum coverage percentage. Default: 90.
.EXAMPLE
    .\run-tests-coverage.ps1 -Package "packages/vindicta-engine"
#>
param(
    [string]$Package = ".",
    [int]$Threshold = 90
)

$ErrorActionPreference = "Stop"

Write-Host "Running tests with coverage for: $Package" -ForegroundColor Cyan
uv run pytest $Package --cov --cov-report=term-missing --cov-fail-under=$Threshold

if ($LASTEXITCODE -ne 0) {
    Write-Host "FAILED: Tests or coverage below ${Threshold}%" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "PASSED: All tests pass with >=${Threshold}% coverage" -ForegroundColor Green
    exit 0
}
