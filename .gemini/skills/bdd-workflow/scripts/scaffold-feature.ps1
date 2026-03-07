<#
.SYNOPSIS
    Scaffolds a new BDD feature file and step definition stub.
.PARAMETER FeatureName
    Name of the feature (e.g. "gas-deduction").
.PARAMETER FeaturesDir
    Path to the features directory. Default: packages/features.
.EXAMPLE
    .\scaffold-feature.ps1 -FeatureName "gas-deduction"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$FeatureName,

    [string]$FeaturesDir = "packages/features"
)

$ErrorActionPreference = "Stop"

$featureFile = Join-Path $FeaturesDir "$FeatureName.feature"
$stepsDir = Join-Path $FeaturesDir "steps"
$stepFile = Join-Path $stepsDir "test_$($FeatureName -replace '-', '_').py"

if (Test-Path $featureFile) {
    Write-Host "Feature file already exists: $featureFile" -ForegroundColor Yellow
    exit 0
}

# Create feature file
$featureContent = @"
Feature: $($FeatureName -replace '-', ' ' -replace '(^|\s)(\w)', { $_.Value.ToUpper() })

  Scenario: [Describe the scenario]
    Given [initial state]
    When [action occurs]
    Then [expected outcome]
"@

New-Item -ItemType Directory -Force -Path (Split-Path $featureFile) | Out-Null
Set-Content -Path $featureFile -Value $featureContent -Encoding UTF8
Write-Host "Created: $featureFile" -ForegroundColor Green

# Create step definition stub
if (-not (Test-Path $stepsDir)) {
    New-Item -ItemType Directory -Force -Path $stepsDir | Out-Null
}

$stepContent = @"
"""Step definitions for $FeatureName."""

from behave import given, when, then


@given("[initial state]")
def step_given_initial_state(context):
    raise NotImplementedError("Implement this step")


@when("[action occurs]")
def step_when_action(context):
    raise NotImplementedError("Implement this step")


@then("[expected outcome]")
def step_then_outcome(context):
    raise NotImplementedError("Implement this step")
"@

Set-Content -Path $stepFile -Value $stepContent -Encoding UTF8
Write-Host "Created: $stepFile" -ForegroundColor Green

Write-Host ""
Write-Host "Next: Edit the .feature file, then run 'uv run behave' to see it fail." -ForegroundColor Cyan
