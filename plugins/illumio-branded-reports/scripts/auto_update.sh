#!/usr/bin/env bash
# auto_update.sh — SessionStart hook for illumio-branded-reports plugin.
#
# Runs at the start of every Claude Code session. Fast-forwards the local
# plugin checkout to origin/main when safe to do so. Designed to be silent
# on the happy path and fail-open so it never blocks a session.
#
# Safety guards:
#   - Skip if offline (no internet / git fetch fails).
#   - Skip if local working tree has uncommitted changes (preserves user edits).
#   - Skip if local branch has diverged from origin (preserves user commits).
#   - Only fast-forward; never merge, rebase, or reset.
#
# Logs to a timestamped file under the plugin's .cache/ directory so a
# user can audit what happened if a session looks stale.

set -u

# CLAUDE_PLUGIN_ROOT is set by Claude Code to the plugin's install directory.
# When the hook is invoked outside Claude Code (manual test), fall back to
# the script's parent's parent directory.
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
MARKETPLACE_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"
LOG_DIR="$PLUGIN_ROOT/.cache"
LOG_FILE="$LOG_DIR/auto_update.log"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG_FILE"
}

# Truncate log if it grows beyond 200 KB.
if [ -f "$LOG_FILE" ] && [ "$(wc -c < "$LOG_FILE" 2>/dev/null || echo 0)" -gt 204800 ]; then
  tail -c 102400 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi

log "auto_update.sh starting (PLUGIN_ROOT=$PLUGIN_ROOT)"

# The git repo lives at the marketplace root (one level up from plugins/).
cd "$MARKETPLACE_ROOT" 2>/dev/null || {
  log "marketplace root not found; aborting"
  exit 0
}

if [ ! -d ".git" ]; then
  log "no .git directory at marketplace root; aborting"
  exit 0
}

# Skip if working tree is dirty.
if ! git diff --quiet --ignore-submodules HEAD 2>/dev/null; then
  log "local working tree has uncommitted changes; skipping auto-update"
  exit 0
fi

# Try to fetch with a short timeout — fail open if offline.
if ! timeout 5s git fetch --quiet origin 2>/dev/null; then
  log "git fetch failed or timed out (offline?); skipping"
  exit 0
fi

LOCAL="$(git rev-parse @ 2>/dev/null)"
REMOTE="$(git rev-parse @{u} 2>/dev/null)"
BASE="$(git merge-base @ @{u} 2>/dev/null)"

if [ -z "$LOCAL" ] || [ -z "$REMOTE" ] || [ -z "$BASE" ]; then
  log "could not determine local/remote/base SHAs; skipping"
  exit 0
fi

if [ "$LOCAL" = "$REMOTE" ]; then
  log "already up to date (SHA=$LOCAL)"
  exit 0
fi

if [ "$LOCAL" = "$BASE" ]; then
  # Local is behind remote and can fast-forward.
  if git merge --ff-only --quiet origin/main 2>/dev/null; then
    NEW="$(git rev-parse @ 2>/dev/null)"
    log "fast-forwarded $LOCAL -> $NEW"
    exit 0
  else
    log "fast-forward failed; skipping (local=$LOCAL remote=$REMOTE)"
    exit 0
  fi
fi

if [ "$REMOTE" = "$BASE" ]; then
  log "local has unpushed commits ($LOCAL ahead of $REMOTE); run /skill-publish to push"
  exit 0
fi

log "local and remote have diverged (local=$LOCAL remote=$REMOTE base=$BASE); manual resolution required"
exit 0
