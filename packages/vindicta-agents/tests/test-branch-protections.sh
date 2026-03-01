#!/usr/bin/env bash
# Test 3: Branch Protection Verification
# Verifies that branch protections are correctly applied across all vindicta-platform repos.
#
# Usage: bash tests/test-branch-protections.sh
#
# Requires: gh CLI authenticated as org admin

set -euo pipefail

ORG="vindicta-platform"
PASSED=0
FAILED=0
SKIPPED=0

pass() { echo "  ✅ $1"; PASSED=$((PASSED + 1)); }
fail() { echo "  ❌ $1"; FAILED=$((FAILED + 1)); }
skip() { echo "  ⏭️  $1"; SKIPPED=$((SKIPPED + 1)); }

echo "=== Test 3: Branch Protection Verification ==="
echo "  Org: $ORG"
echo ""

# Get all non-archived repos
REPOS=$(gh repo list "$ORG" --json name,isArchived,isPrivate --limit 100 --jq '.[] | select(.isArchived == false) | "\(.name)|\(.isPrivate)"')

for entry in $REPOS; do
  REPO=$(echo "$entry" | cut -d'|' -f1)
  IS_PRIVATE=$(echo "$entry" | cut -d'|' -f2)

  echo "[$REPO]"

  # Fetch branch protection
  PROTECTION=$(gh api "repos/$ORG/$REPO/branches/main/protection" 2>&1 || true)

  # Check if protection exists
  if echo "$PROTECTION" | grep -q '"Branch not protected"'; then
    if [ "$IS_PRIVATE" = "true" ]; then
      skip "$REPO — private repo (GitHub Free limitation)"
    else
      fail "$REPO — main branch is NOT protected"
    fi
    continue
  fi

  if echo "$PROTECTION" | grep -q '"Upgrade to GitHub"'; then
    skip "$REPO — private repo (requires GitHub Team plan)"
    continue
  fi

  if echo "$PROTECTION" | grep -q '"Not Found"'; then
    fail "$REPO — protection API returned 404"
    continue
  fi

  # Validate required settings
  ERRORS=0

  # 3.1 — Required reviews = 1
  REVIEW_COUNT=$(echo "$PROTECTION" | jq -r '.required_pull_request_reviews.required_approving_review_count // 0')
  if [ "$REVIEW_COUNT" -ge 1 ]; then
    echo "    reviews: $REVIEW_COUNT ✓"
  else
    echo "    reviews: $REVIEW_COUNT ✗ (expected >= 1)"
    ERRORS=$((ERRORS + 1))
  fi

  # 3.2 — Dismiss stale reviews
  DISMISS_STALE=$(echo "$PROTECTION" | jq -r '.required_pull_request_reviews.dismiss_stale_reviews // false')
  if [ "$DISMISS_STALE" = "true" ]; then
    echo "    dismiss_stale: true ✓"
  else
    echo "    dismiss_stale: $DISMISS_STALE ✗"
    ERRORS=$((ERRORS + 1))
  fi

  # 3.3 — Enforce admins = false (admin bypass enabled)
  ENFORCE_ADMINS=$(echo "$PROTECTION" | jq -r '.enforce_admins.enabled // true')
  if [ "$ENFORCE_ADMINS" = "false" ]; then
    echo "    enforce_admins: false ✓ (bypass enabled)"
  else
    echo "    enforce_admins: $ENFORCE_ADMINS ✗ (expected false)"
    ERRORS=$((ERRORS + 1))
  fi

  # 3.4 — Force pushes blocked
  FORCE_PUSH=$(echo "$PROTECTION" | jq -r '.allow_force_pushes.enabled // true')
  if [ "$FORCE_PUSH" = "false" ]; then
    echo "    force_push: blocked ✓"
  else
    echo "    force_push: allowed ✗"
    ERRORS=$((ERRORS + 1))
  fi

  # 3.5 — Deletions blocked
  DELETIONS=$(echo "$PROTECTION" | jq -r '.allow_deletions.enabled // true')
  if [ "$DELETIONS" = "false" ]; then
    echo "    deletions: blocked ✓"
  else
    echo "    deletions: allowed ✗"
    ERRORS=$((ERRORS + 1))
  fi

  if [ "$ERRORS" -eq 0 ]; then
    pass "$REPO — all protections correct"
  else
    fail "$REPO — $ERRORS setting(s) incorrect"
  fi
done

echo ""
echo "=== Results ==="
echo "  ✅ Passed:  $PASSED"
echo "  ❌ Failed:  $FAILED"
echo "  ⏭️  Skipped: $SKIPPED (private repos — GitHub Free limitation)"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
