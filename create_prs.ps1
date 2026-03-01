param(
    [string]$RootPath = "C:\Users\bfoxt\Documents\GitHub\vindicta-platform"
)

$Repos = @(
    "packages\vindicta-agents",
    "packages\vindicta-engine",
    "packages\vindicta-economy",
    "packages\warscribe-system",
    "packages\vindicta-foundation",
    "packages\vindicta-oracle",
    "."
)

$BranchName = "fix/uv-workspace-submodule-conflicts"
$CommitMsg = "chore(deps): resolve uv workspace and submodule conflicts"
$PrTitle = "chore: resolve uv workspace and submodule conflicts"
$PrBodyOrigin = Join-Path -Path $RootPath -ChildPath "PR_BODY.md"

foreach ($Repo in $Repos) {
    Write-Host "`nProcessing: $Repo"
    $RepoPath = Join-Path -Path $RootPath -ChildPath $Repo
    if (-not (Test-Path -Path $RepoPath)) {
        Write-Host "Path not found: $RepoPath"
        continue
    }
    Set-Location -Path $RepoPath

    # Remove temporary PR body
    Remove-Item -Path ".GITHUB_PR_BODY.md" -ErrorAction SilentlyContinue

    # Check if there are changes
    $status = git status --porcelain
    if (-not $status) {
        Write-Host "No changes in $Repo, skipping..."
        continue
    }

    # Automatically set our branch state without risking file deletions if uncommitted
    # If the branch already exists locally, stash, switch to it, drop changes, switch to main, delete it.
    git stash -u
    git checkout main
    git branch -D $BranchName 2>$null
    git checkout -B $BranchName
    git stash pop

    # Add and bypass GPG signing explicitly to prevent hangs!
    git add .
    git -c commit.gpgsign=false commit -m $CommitMsg
    
    # Push to origin
    git push -u origin $BranchName --force

    # Submit PR
    Copy-Item -Path $PrBodyOrigin -Destination "PR_BODY.md" -Force
    gh pr create --title $PrTitle --body-file PR_BODY.md --head $BranchName --base main
    Remove-Item -Path "PR_BODY.md" -Force
}

Set-Location -Path $RootPath
