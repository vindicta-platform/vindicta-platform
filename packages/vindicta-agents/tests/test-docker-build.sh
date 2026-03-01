#!/usr/bin/env bash
# Test 1: Docker Build Test
# Verifies the dev container image builds successfully with all required tools.
#
# Usage: bash tests/test-docker-build.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
IMAGE_NAME="vindicta-agent-test"
PASSED=0
FAILED=0

pass() { echo "  ✅ $1"; PASSED=$((PASSED + 1)); }
fail() { echo "  ❌ $1"; FAILED=$((FAILED + 1)); }

echo "=== Test 1: Docker Build ==="
echo ""

# 1.1 — Image builds successfully
echo "[1.1] Building image..."
if docker build -t "$IMAGE_NAME" "$REPO_ROOT/.devcontainer/" > /dev/null 2>&1; then
  pass "Image builds successfully"
else
  fail "Image build failed"
  echo "  Run manually to see errors: docker build -t $IMAGE_NAME .devcontainer/"
  exit 1
fi

# 1.2 — Required binaries exist
echo "[1.2] Checking required binaries..."
for bin in gpg git curl jq dos2unix gh; do
  if docker run --rm "$IMAGE_NAME" which "$bin" > /dev/null 2>&1; then
    pass "$bin is installed"
  else
    fail "$bin is NOT installed"
  fi
done

# 1.3 — init-agent.sh exists and is executable
echo "[1.3] Checking init-agent.sh..."
if docker run --rm "$IMAGE_NAME" test -x /usr/local/bin/init-agent.sh; then
  pass "init-agent.sh is executable at /usr/local/bin/"
else
  fail "init-agent.sh missing or not executable"
fi

# 1.4 — GPG directory is pre-configured
echo "[1.4] Checking GPG config..."
if docker run --rm "$IMAGE_NAME" test -d /home/vscode/.gnupg; then
  pass ".gnupg directory exists"
else
  fail ".gnupg directory missing"
fi

GPG_CONF=$(docker run --rm "$IMAGE_NAME" cat /home/vscode/.gnupg/gpg.conf 2>/dev/null || true)
if echo "$GPG_CONF" | grep -q "no-tty"; then
  pass "gpg.conf has no-tty set"
else
  fail "gpg.conf missing no-tty"
fi

# 1.5 — Cleanup
docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
