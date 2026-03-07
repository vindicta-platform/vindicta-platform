<#
.SYNOPSIS
    Validates a commit message against Conventional Commits format.
.PARAMETER Message
    The commit message string to validate.
.EXAMPLE
    .\validate-commit-msg.ps1 -Message "feat(engine): add MCTS support"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Message
)

$pattern = "^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,72}$"

if ($Message -match $pattern) {
    Write-Host "VALID: '$Message'" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "INVALID: '$Message'" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected format: <type>(<scope>): <short summary>" -ForegroundColor Yellow
    Write-Host "  Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert" -ForegroundColor Yellow
    Write-Host "  Summary: max 72 chars, lowercase first letter, no period at end" -ForegroundColor Yellow
    exit 1
}
