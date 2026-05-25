#!/usr/bin/env bash
# manual_update.sh — Body of the /skill-update slash command.
#
# Same logic as auto_update.sh but verbose: prints what it's doing and
# why each branch was taken. Use this when:
#   - The auto-update silently skipped and you want to know why.
#   - You just pushed a change from another machine and want to pull now.
#   - You suspect the local plugin is stale.

set -u

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
MARKETPLACE_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"

echo "manual_update: marketplace root = $MARKETPLACE_ROOT"
cd "$MARKETPLACE_ROOT" 2>/dev/null || {
  echo "ERROR: marketplace root not found at $MARKETPLACE_ROOT"
  exit 1
}

if [ ! -d ".git" ]; then
  echo "ERROR: no .git directory at marketplace root"
  exit 1
fi

echo ""
echo "Current state:"
echo "  branch:        $(git branch --show-current)"
echo "  local HEAD:    $(git rev-parse --short HEAD)"

if ! git diff --quiet --ignore-submodules HEAD 2>/dev/null; then
  echo ""
  echo "WARNING: local working tree has uncommitted changes:"
  git status --short
  echo ""
  echo "Refusing to update. Commit or stash your changes first."
  exit 1
fi

echo ""
echo "Fetching from origin..."
if ! git fetch origin; then
  echo "ERROR: git fetch failed. Check network connectivity and gh auth."
  exit 1
fi

LOCAL="$(git rev-parse @)"
REMOTE="$(git rev-parse @{u} 2>/dev/null || echo '')"
BASE="$(git merge-base @ @{u} 2>/dev/null || echo '')"

echo "  remote HEAD:   $(git rev-parse --short @{u} 2>/dev/null || echo '???')"

if [ -z "$REMOTE" ]; then
  echo "ERROR: no upstream configured for the current branch."
  exit 1
fi

if [ "$LOCAL" = "$REMOTE" ]; then
  echo ""
  echo "Already up to date."
  exit 0
fi

if [ "$LOCAL" = "$BASE" ]; then
  echo ""
  echo "Local is behind origin by $(git rev-list --count HEAD..@{u}) commit(s). Fast-forwarding..."
  git merge --ff-only origin/main
  echo ""
  echo "Update complete. New HEAD: $(git rev-parse --short HEAD)"
  echo ""
  echo "Changed files:"
  git diff --stat "$LOCAL"..HEAD
  exit 0
fi

if [ "$REMOTE" = "$BASE" ]; then
  echo ""
  echo "Local is AHEAD of origin by $(git rev-list --count @{u}..HEAD) commit(s)."
  echo "Run /skill-publish to push your changes."
  exit 0
fi

echo ""
echo "WARNING: local and origin have diverged."
echo "  local has $(git rev-list --count @{u}..HEAD) commit(s) not on origin"
echo "  origin has $(git rev-list --count HEAD..@{u}) commit(s) not on local"
echo ""
echo "Manual resolution required. Recommended: 'git pull --rebase' if you want"
echo "your local commits on top of origin, or push to a branch and open a PR."
exit 1
