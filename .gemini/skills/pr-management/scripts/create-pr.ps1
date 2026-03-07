<#
.SYNOPSIS
    Generates a PR body markdown file from a template and opens a PR.
.PARAMETER Title
    The PR title.
.PARAMETER Fixes
    Optional issue number this PR fixes (e.g. 42).
.PARAMETER Draft
    If set, creates the PR as a draft.
.PARAMETER BaseBranch
    The base branch to target. Default: main.
.EXAMPLE
    .\create-pr.ps1 -Title "feat(engine): add MCTS support" -Fixes 42
.EXAMPLE
    .\create-pr.ps1 -Title "fix(foundation): correct model export" -Draft
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$Title,

    [int]$Fixes = 0,

    [switch]$Draft,

    [string]$BaseBranch = "main"
)

$ErrorActionPreference = "Stop"

$templatePath = Join-Path $PSScriptRoot ".." "assets" "pr-body-template.md"
if (-not (Test-Path $templatePath)) {
    Write-Error "PR body template not found at: $templatePath"
    exit 1
}

$body = Get-Content $templatePath -Raw
$body = $body -replace '\[TITLE\]', $Title

if ($Fixes -gt 0) {
    $body = $body -replace '\[FIXES_LINE\]', "Fixes #$Fixes"
}
else {
    $body = $body -replace '\[FIXES_LINE\]', ""
}

$prBodyFile = "PR_BODY.md"
Set-Content -Path $prBodyFile -Value $body -Encoding UTF8

Write-Host "PR body written to $prBodyFile" -ForegroundColor Cyan
Write-Host "Review and edit the file, then run:" -ForegroundColor Yellow

$draftFlag = if ($Draft) { "--draft" } else { "" }
Write-Host "  gh pr create --title `"$Title`" --body-file $prBodyFile --base $BaseBranch $draftFlag" -ForegroundColor Green
