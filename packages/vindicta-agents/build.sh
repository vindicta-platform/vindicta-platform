#!/usr/bin/env bash
# Local build pipeline for Vindicta Agent images
# Usage:
#   bash build.sh              # build both
#   bash build.sh base         # base only
#   bash build.sh slim         # slim only
#   bash build.sh slim --test  # build slim + run tests

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONTEXT="$SCRIPT_DIR/.devcontainer"

IMAGE_BASE="vindicta-agent"
IMAGE_SLIM="vindicta-agent-slim"
TARGET="${1:-all}"
RUN_TESTS=false

# Check for --test flag
for arg in "$@"; do
  if [ "$arg" = "--test" ]; then
    RUN_TESTS=true
  fi
done

build_base() {
  echo "=== Building base image ($IMAGE_BASE) ==="
  docker build -t "$IMAGE_BASE" "$CONTEXT"
  SIZE=$(docker image inspect "$IMAGE_BASE" --format='{{.Size}}' | awk '{printf "%.0fMB", $1/1024/1024}')
  echo "  ✅ $IMAGE_BASE built ($SIZE)"
  echo ""
}

build_slim() {
  echo "=== Building slim image ($IMAGE_SLIM) ==="
  docker build -f "$CONTEXT/Dockerfile.slim" -t "$IMAGE_SLIM" "$CONTEXT"
  SIZE=$(docker image inspect "$IMAGE_SLIM" --format='{{.Size}}' | awk '{printf "%.0fMB", $1/1024/1024}')
  echo "  ✅ $IMAGE_SLIM built ($SIZE)"
  echo ""
}

run_tests() {
  echo "=== Running tests ==="
  bash "$SCRIPT_DIR/tests/test-docker-build.sh"
  echo ""
}

case "$TARGET" in
  base)
    build_base
    ;;
  slim)
    build_slim
    ;;
  all)
    build_base
    build_slim
    ;;
  *)
    echo "Usage: bash build.sh [base|slim|all] [--test]"
    exit 1
    ;;
esac

if [ "$RUN_TESTS" = true ]; then
  run_tests
fi

echo "=== Done ==="
docker images --filter "reference=vindicta-agent*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
