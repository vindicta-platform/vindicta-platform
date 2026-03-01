#!/usr/bin/env bash
# Applies branch protections to all vindicta-platform repos
# Requires: gh CLI authenticated as org admin
#
# Usage: bash automation/apply-branch-protections.sh

set -euo pipefail

ORG="vindicta-platform"
REQUIRED_REVIEWS=1
ENFORCE_ADMINS=false  # Admins (brandon-fox) can bypass review requirement

echo "=== Applying Branch Protections to $ORG ==="
echo "  Required reviews: $REQUIRED_REVIEWS"
echo "  Enforce admins:   $ENFORCE_ADMINS"
echo ""

SUCCESS=0
FAILED=0
SKIPPED=0

repos=$(gh repo list "$ORG" --json name,isArchived --limit 100 --jq '.[] | select(.isArchived == false) | .name')

for repo in $repos; do
  echo "Applying protection to $ORG/$repo (main)..."

  if gh api -X PUT "repos/$ORG/$repo/branches/main/protection" \
    --input - <<EOF 2>/dev/null
{
  "required_status_checks": null,
  "enforce_admins": $ENFORCE_ADMINS,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": $REQUIRED_REVIEWS
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
  then
    echo "  ✅ $repo protected"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "  ❌ $repo FAILED"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "=== Branch Protection Complete ==="
echo "  ✅ Success: $SUCCESS"
echo "  ❌ Failed:  $FAILED"
