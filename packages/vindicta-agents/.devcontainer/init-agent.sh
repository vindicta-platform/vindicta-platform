#!/usr/bin/env bash
set -euo pipefail

# --- Resolve token: accept GITHUB_TOKEN or AGENT_GITHUB_TOKEN, but not both ---

if [ -n "${GITHUB_TOKEN:-}" ] && [ -n "${AGENT_GITHUB_TOKEN:-}" ]; then
  echo "❌ ERROR: Both GITHUB_TOKEN and AGENT_GITHUB_TOKEN are set."
  echo "  Provide only one. GITHUB_TOKEN is used by convention inside the container."
  echo "  AGENT_GITHUB_TOKEN is the host-side name mapped by devcontainer.json."
  exit 1
fi

# Normalize to GITHUB_TOKEN
if [ -z "${GITHUB_TOKEN:-}" ] && [ -n "${AGENT_GITHUB_TOKEN:-}" ]; then
  GITHUB_TOKEN="$AGENT_GITHUB_TOKEN"
fi

# --- Volume detection ---

OUTPUT_DIR="/output"
HAS_VOLUME=false
mkdir -p "$OUTPUT_DIR" 2>/dev/null || true
if touch "$OUTPUT_DIR/.volume-test" 2>/dev/null; then
  rm -f "$OUTPUT_DIR/.volume-test"
  # Check if it's a real mount, not just the container's ephemeral fs
  if mount | grep -q "$OUTPUT_DIR" 2>/dev/null; then
    HAS_VOLUME=true
  fi
fi

echo "=== Initializing Vindicta Agent Identity ==="
echo ""

# --- PAT Access Check ---

GPG_READ=false
GPG_WRITE=false

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "[PAT] Checking GitHub token permissions..."

  # Test GPG read access
  GPG_READ_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/user/gpg_keys")

  if [ "$GPG_READ_RESPONSE" = "200" ]; then
    GPG_READ=true
    echo "  ✅ GPG keys: READ access"
  else
    echo "  ❌ GPG keys: no read access (HTTP $GPG_READ_RESPONSE)"
  fi

  # Test GPG write access with an invalid key (422 = has write, 404/403 = no write)
  GPG_WRITE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST "https://api.github.com/user/gpg_keys" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -d '{"armored_public_key": "test"}')

  if [ "$GPG_WRITE_RESPONSE" = "422" ] || [ "$GPG_WRITE_RESPONSE" = "201" ]; then
    GPG_WRITE=true
    echo "  ✅ GPG keys: WRITE access"
  else
    echo "  ❌ GPG keys: no write access (HTTP $GPG_WRITE_RESPONSE)"
  fi

  # Check authenticated user
  USER_LOGIN=$(curl -s \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/user" | jq -r '.login // "unknown"')
  echo "  👤 Authenticated as: $USER_LOGIN"
  echo ""
else
  echo "[PAT] No token provided (GITHUB_TOKEN or AGENT_GITHUB_TOKEN). GitHub features disabled."
  echo ""
fi

# --- Pre-flight warnings ---

if [ "$HAS_VOLUME" = false ] && [ "$GPG_WRITE" = false ]; then
  echo "  ⚠️⚠️⚠️  WARNING ⚠️⚠️⚠️"
  echo "  No /output volume mounted AND no GPG write access."
  echo "  Generated keys will be LOST when this container exits!"
  echo ""
  echo "  Fix by doing ONE of the following:"
  echo "    1. Mount a volume:  -v \"\${PWD}/.keys:/output\""
  echo "    2. Add GPG write to PAT:  'admin:gpg_key' (classic) or 'gpg_keys: write' (fine-grained)"
  echo ""
  read -p "  Continue anyway? (y/N) " -n 1 -r
  echo ""
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "  Aborted."
    exit 1
  fi
fi

# --- GPG Key Setup ---

if [ -n "${GPG_PRIVATE_KEY:-}" ]; then
  # === IMPORT EXISTING KEY ===
  echo "[GPG] Importing provided GPG key..."
  echo "$GPG_PRIVATE_KEY" | base64 -d | gpg --batch --import 2>/dev/null
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)

  # Trust the key ultimately
  echo "${GPG_KEY_ID}:6:" | gpg --import-ownertrust 2>/dev/null
  echo "  Key imported: $GPG_KEY_ID"

  # Validate the key exists on GitHub (read-only check)
  if [ "$GPG_READ" = true ]; then
    echo "[GPG] Validating key is registered on GitHub..."
    FOUND=$(curl -s \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/user/gpg_keys" | \
      grep -c "${GPG_KEY_ID}" 2>/dev/null || true)

    if [ "${FOUND:-0}" -gt 0 ]; then
      echo "  ✅ Key is registered on GitHub"
    else
      echo "  ⚠️  Key NOT found on GitHub"
      if [ "$GPG_WRITE" = true ]; then
        echo "  Uploading key to GitHub..."
        ARMORED_KEY=$(gpg --armor --export "$GPG_KEY_ID")
        UPLOAD_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
          -X POST "https://api.github.com/user/gpg_keys" \
          -H "Authorization: Bearer $GITHUB_TOKEN" \
          -H "Accept: application/vnd.github+json" \
          -d "$(jq -n --arg key "$ARMORED_KEY" '{armored_public_key: $key}')")
        if [ "$UPLOAD_CODE" = "201" ] || [ "$UPLOAD_CODE" = "422" ]; then
          echo "  ✅ Key uploaded to GitHub"
        else
          echo "  ❌ Upload failed (HTTP $UPLOAD_CODE)"
        fi
      else
        echo "  ℹ️  PAT lacks write access. Add the key manually:"
        echo "     1. Copy: $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
        echo "     2. Paste at: https://github.com/settings/keys"
        echo "     To fix: add 'admin:gpg_key' (classic) or 'gpg_keys: write' (fine-grained)"
      fi
    fi
  fi

else
  # === GENERATE NEW KEY ===
  echo "[GPG] No GPG_PRIVATE_KEY provided. Generating a new key..."
  cat > /tmp/gpg-key-params <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: ${AGENT_NAME:-vindicta-bot}
Name-Email: ${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}
Expire-Date: 1y
%commit
EOF
  gpg --batch --gen-key /tmp/gpg-key-params 2>/dev/null
  rm /tmp/gpg-key-params
  GPG_KEY_ID=$(gpg --list-secret-keys --keyid-format=long 2>/dev/null | grep sec | head -1 | awk '{print $2}' | cut -d'/' -f2)
  echo "  New key generated: $GPG_KEY_ID"

  # Try to auto-upload
  if [ "$GPG_WRITE" = true ]; then
    echo "[GPG] Uploading key to GitHub..."
    ARMORED_KEY=$(gpg --armor --export "$GPG_KEY_ID")
    UPLOAD_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
      -X POST "https://api.github.com/user/gpg_keys" \
      -H "Authorization: Bearer $GITHUB_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      -d "$(jq -n --arg key "$ARMORED_KEY" '{armored_public_key: $key}')")

    if [ "$UPLOAD_CODE" = "201" ]; then
      echo "  ✅ Key uploaded to GitHub automatically"
    elif [ "$UPLOAD_CODE" = "422" ]; then
      echo "  ✅ Key already exists on GitHub"
    else
      echo "  ❌ Upload failed (HTTP $UPLOAD_CODE). Add manually."
    fi
  else
    echo ""
    echo "  ========================================"
    echo "  MANUAL STEP REQUIRED"
    echo "  ========================================"
    echo "  The key could not be uploaded automatically."
    if [ -n "${GITHUB_TOKEN:-}" ]; then
      echo "  Your PAT does not have GPG write permission."
      echo "  To fix for next run, update your PAT with:"
      echo "    - Classic PAT:       add 'admin:gpg_key' scope"
      echo "    - Fine-Grained PAT:  add 'gpg_keys: write' permission"
    else
      echo "  No token was provided."
    fi
    echo ""
    echo "  For now, add the key manually:"
    echo "    1. Copy:  $OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
    echo "    2. Go to: https://github.com/settings/keys"
    echo "    3. Click 'New GPG key' and paste the contents"
    echo "  ========================================"
  fi
fi

# --- Export keys to host volume (if mounted) ---

if [ "$HAS_VOLUME" = true ]; then
  echo ""
  echo "[Export] Writing keys to $OUTPUT_DIR/"
  PUBKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-public.asc"
  gpg --armor --export "$GPG_KEY_ID" > "$PUBKEY_FILE"
  echo "  Public key:  $PUBKEY_FILE"

  PRIVKEY_FILE="$OUTPUT_DIR/${AGENT_NAME:-vindicta-bot}-gpg-private-b64.txt"
  gpg --armor --export-secret-keys "$GPG_KEY_ID" | base64 -w0 > "$PRIVKEY_FILE"
  echo "  Private key: $PRIVKEY_FILE"
else
  if [ "$GPG_WRITE" = true ]; then
    echo ""
    echo "[Export] No /output volume mounted — skipping file export."
    echo "  (Key was uploaded to GitHub, so no file export needed.)"
  else
    echo ""
    echo "  ⚠️  No /output volume mounted. Keys only exist inside this container."
    echo "     They will be LOST when the container exits."
    echo "     To persist, re-run with: -v \"\${PWD}/.keys:/output\""
  fi
fi

# --- Configure git identity ---

git config --global user.name "${AGENT_NAME:-vindicta-bot}"
git config --global user.email "${AGENT_EMAIL:-260104759+vindicta-bot@users.noreply.github.com}"
git config --global user.signingkey "$GPG_KEY_ID"
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg

# --- Configure GitHub CLI auth ---

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null
  echo "[GH CLI] Authenticated."
fi

echo ""
echo "=== Agent Identity Ready ==="
echo "  Name:    $(git config user.name)"
echo "  Email:   $(git config user.email)"
echo "  GPG:     $GPG_KEY_ID"
echo "  Volume:  $([ "$HAS_VOLUME" = true ] && echo 'mounted ✅' || echo 'not mounted')"
echo "  GitHub:  $([ "$GPG_READ" = true ] && echo 'read ✅' || echo 'read ❌') $([ "$GPG_WRITE" = true ] && echo 'write ✅' || echo 'write ❌')"
