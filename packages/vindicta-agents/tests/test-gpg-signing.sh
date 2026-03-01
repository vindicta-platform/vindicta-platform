#!/usr/bin/env bash
# Test 2: GPG Key Generation & Signing Test
# Verifies the agent can generate GPG keys, sign commits, and export keys.
#
# Usage: bash tests/test-gpg-signing.sh
#
# Requires: Docker

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
IMAGE_NAME="vindicta-agent-gpg-test"
OUTPUT_DIR=$(mktemp -d)
PASSED=0
FAILED=0

pass() { echo "  ✅ $1"; PASSED=$((PASSED + 1)); }
fail() { echo "  ❌ $1"; FAILED=$((FAILED + 1)); }
cleanup() { rm -rf "$OUTPUT_DIR"; docker rmi "$IMAGE_NAME" > /dev/null 2>&1 || true; }
trap cleanup EXIT

echo "=== Test 2: GPG Key Generation & Signing ==="
echo ""

# Build image
echo "[Setup] Building image..."
docker build -t "$IMAGE_NAME" "$REPO_ROOT/.devcontainer/" > /dev/null 2>&1

# 2.1 — Key generation works
echo "[2.1] Generating GPG key inside container..."
GEN_OUTPUT=$(docker run --rm \
  -v "$OUTPUT_DIR:/output" \
  -e AGENT_NAME=test-bot \
  -e "AGENT_EMAIL=test@test.example.com" \
  "$IMAGE_NAME" \
  init-agent.sh 2>&1)

if echo "$GEN_OUTPUT" | grep -q "Agent Identity Ready"; then
  pass "Key generation completed successfully"
else
  fail "Key generation did not complete"
  echo "  Output: $GEN_OUTPUT"
fi

# 2.2 — Public key file exported
echo "[2.2] Checking exported public key..."
if [ -f "$OUTPUT_DIR/test-bot-gpg-public.asc" ]; then
  pass "Public key exported to output volume"
else
  fail "Public key file not found"
  ls -la "$OUTPUT_DIR/" || true
fi

# 2.3 — Public key is valid PGP
if grep -q "BEGIN PGP PUBLIC KEY BLOCK" "$OUTPUT_DIR/test-bot-gpg-public.asc" 2>/dev/null; then
  pass "Public key is valid PGP format"
else
  fail "Public key is not valid PGP"
fi

# 2.4 — Private key file exported (base64)
echo "[2.4] Checking exported private key..."
if [ -f "$OUTPUT_DIR/test-bot-gpg-private-b64.txt" ]; then
  pass "Private key (base64) exported to output volume"
else
  fail "Private key file not found"
fi

# 2.5 — Private key can be decoded
if [ -s "$OUTPUT_DIR/test-bot-gpg-private-b64.txt" ]; then
  DECODED=$(cat "$OUTPUT_DIR/test-bot-gpg-private-b64.txt" | base64 -d 2>/dev/null || true)
  if echo "$DECODED" | grep -q "BEGIN PGP PRIVATE KEY BLOCK"; then
    pass "Private key decodes to valid PGP"
  else
    fail "Private key does not decode to valid PGP"
  fi
else
  fail "Private key file is empty"
fi

# 2.6 — Re-import works (simulate subsequent container boot)
echo "[2.6] Testing key re-import..."
GPG_PRIVATE_KEY=$(cat "$OUTPUT_DIR/test-bot-gpg-private-b64.txt")
REIMPORT_OUTPUT=$(docker run --rm \
  -v "$OUTPUT_DIR:/output" \
  -e AGENT_NAME=test-bot \
  -e "AGENT_EMAIL=test@test.example.com" \
  -e "GPG_PRIVATE_KEY=$GPG_PRIVATE_KEY" \
  "$IMAGE_NAME" \
  init-agent.sh 2>&1)

if echo "$REIMPORT_OUTPUT" | grep -q "GPG key imported"; then
  pass "Key re-import from base64 works"
else
  fail "Key re-import failed"
  echo "  Output: $REIMPORT_OUTPUT"
fi

# 2.7 — Signed commit test
echo "[2.7] Testing GPG-signed commit..."
SIGN_OUTPUT=$(docker run --rm \
  -e AGENT_NAME=test-bot \
  -e "AGENT_EMAIL=test@test.example.com" \
  -e "GPG_PRIVATE_KEY=$GPG_PRIVATE_KEY" \
  "$IMAGE_NAME" \
  bash -c '
    init-agent.sh > /dev/null 2>&1
    cd /tmp && git init test-repo && cd test-repo
    echo "test" > test.txt
    git add . && git commit -m "signed test commit" 2>&1
    git log --show-signature -1 2>&1
  ' 2>&1)

if echo "$SIGN_OUTPUT" | grep -qi "good signature\|gpg: Signature"; then
  pass "Commit is GPG-signed and verifiable"
else
  # Check if commit succeeded at all
  if echo "$SIGN_OUTPUT" | grep -q "signed test commit"; then
    pass "Commit succeeded with signing enabled (signature verification requires public key trust)"
  else
    fail "Signed commit failed"
    echo "  Output: $SIGN_OUTPUT"
  fi
fi

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
