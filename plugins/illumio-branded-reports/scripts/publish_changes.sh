#!/usr/bin/env bash
# publish_changes.sh — Body of the /skill-publish slash command.
#
# Stages, commits, and pushes local edits to the marketplace repo. By
# default opens a PR via `gh` against main; pass --direct to push directly
# to main (only safe for trusted maintainers).
#
# Usage (from the slash command, with no args):
#   /skill-publish
#     → creates a branch, commits, pushes, opens a PR.
#
# Usage (direct push, for solo maintainer):
#   /skill-publish --direct
#     → commits to main and pushes.

set -u

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
MARKETPLACE_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"
DIRECT_PUSH=0
COMMIT_MESSAGE=""

while [ $# -gt 0 ]; do
  case "$1" in
    --direct) DIRECT_PUSH=1; shift ;;
    -m|--message) COMMIT_MESSAGE="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

cd "$MARKETPLACE_ROOT" || { echo "ERROR: marketplace root not found"; exit 1; }

# Verify gh is installed and authenticated.
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: gh CLI not installed. brew install gh, then gh auth login."
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: gh CLI not authenticated. Run: gh auth login"
  exit 1
fi

if git diff --quiet --ignore-submodules HEAD 2>/dev/null && \
   [ -z "$(git status --porcelain)" ]; then
  echo "No changes to publish. Working tree is clean."
  exit 0
fi

echo "Changes to publish:"
git status --short
echo ""

if [ -z "$COMMIT_MESSAGE" ]; then
  echo "Enter a commit message (one line). Use the typed-prefix convention:"
  echo "  feat: new capability or major addition"
  echo "  fix:  bug fix or correction"
  echo "  ref:  refactor (same behavior, better structure)"
  echo "  docs: documentation only"
  echo "  eval: evals/test cases"
  echo "  adapt: platform adapter changes"
  printf "> "
  read -r COMMIT_MESSAGE
fi

if [ -z "$COMMIT_MESSAGE" ]; then
  echo "ERROR: empty commit message; aborting."
  exit 1
fi

git add -A
git commit -m "$COMMIT_MESSAGE" || { echo "ERROR: commit failed"; exit 1; }

if [ "$DIRECT_PUSH" -eq 1 ]; then
  echo ""
  echo "Direct-pushing to main..."
  git push origin main
  echo ""
  echo "Done. New HEAD: $(git rev-parse --short HEAD)"
  exit 0
fi

# Branch + PR flow.
TIMESTAMP="$(date -u +%Y%m%d-%H%M%S)"
BRANCH="skill-update-$TIMESTAMP"
echo ""
echo "Creating branch $BRANCH..."
git checkout -b "$BRANCH"
git push -u origin "$BRANCH"
echo ""
echo "Opening PR..."
gh pr create --base main --head "$BRANCH" \
  --title "$COMMIT_MESSAGE" \
  --body "Published via /skill-publish from $(hostname -s) on $(date -u +%Y-%m-%dT%H:%M:%SZ)."
echo ""
echo "PR opened. Switching back to main..."
git checkout main
echo ""
echo "Done. After the PR is merged, run /skill-update on any device to pull the change."
