<#
.SYNOPSIS
    Scaffolds a failing test file for a new module before any implementation.
.PARAMETER ModuleName
    The Python module name (e.g. "dice_engine").
.PARAMETER PackageName
    The package containing the module. Default: vindicta-foundation.
.EXAMPLE
    .\scaffold-test.ps1 -ModuleName "dice_engine" -PackageName "vindicta-engine"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$ModuleName,

    [string]$PackageName = "vindicta-foundation"
)

$ErrorActionPreference = "Stop"

$packageDir = "packages/$PackageName"
$testsDir = Join-Path $packageDir "tests"
$testFile = Join-Path $testsDir "test_$ModuleName.py"

if (Test-Path $testFile) {
    Write-Host "Test file already exists: $testFile" -ForegroundColor Yellow
    exit 0
}

$packagePython = $PackageName -replace '-', '_'

$testContent = @"
"""Tests for $ModuleName module.

RED phase: These tests MUST fail before implementation.
Run: uv run pytest $testFile -v
"""
import pytest


class Test$($ModuleName -replace '(^|_)(\w)', { $_.Groups[2].Value.ToUpper() }):
    """Test suite for the $ModuleName module."""

    def test_module_importable(self):
        """Verify the module can be imported."""
        from ${packagePython} import $ModuleName
        assert $ModuleName is not None

    def test_placeholder(self):
        """Replace with real test logic."""
        # TODO: Write specific tests for $ModuleName
        pytest.fail("RED: Implement this test before writing production code")
"@

New-Item -ItemType Directory -Force -Path $testsDir | Out-Null
Set-Content -Path $testFile -Value $testContent -Encoding UTF8

Write-Host "Created failing test: $testFile" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps (Red-Green-Refactor):" -ForegroundColor Cyan
Write-Host "  1. RED:    Run 'uv run pytest $testFile -v' — confirm tests FAIL" -ForegroundColor Red
Write-Host "  2. GREEN:  Implement src/$ModuleName.py to make tests PASS" -ForegroundColor Green
Write-Host "  3. REFACTOR: Clean up, then re-run tests" -ForegroundColor Yellow
