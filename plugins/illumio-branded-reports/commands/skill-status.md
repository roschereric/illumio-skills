---
description: Diagnostic report on the illumio-skills plugin install — local SHA, origin SHA, drift, last auto-update log entries.
allowed-tools: Bash
---

Run a diagnostic and report cleanly to the user:

!bash -c '
set -u
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT not set}"
MARKETPLACE_ROOT="$(cd "$PLUGIN_ROOT/../.." && pwd)"

echo "=== illumio-skills plugin status ==="
echo ""
echo "Plugin root:       $PLUGIN_ROOT"
echo "Marketplace root:  $MARKETPLACE_ROOT"
echo ""

cd "$MARKETPLACE_ROOT" 2>/dev/null || { echo "ERROR: marketplace root unreachable"; exit 1; }

if [ ! -d ".git" ]; then
  echo "ERROR: not a git repository"
  exit 1
fi

echo "Branch:            $(git branch --show-current)"
echo "Local HEAD:        $(git rev-parse --short HEAD) — $(git log -1 --format=%s)"
echo "Local HEAD date:   $(git log -1 --format=%cd --date=iso)"

if git fetch --quiet origin 2>/dev/null; then
  REMOTE_SHA="$(git rev-parse --short @{u} 2>/dev/null || echo "???")"
  REMOTE_FULL="$(git rev-parse @{u} 2>/dev/null || echo "")"
  LOCAL_FULL="$(git rev-parse @ 2>/dev/null || echo "")"
  echo "Remote HEAD:       $REMOTE_SHA"
  if [ -n "$REMOTE_FULL" ] && [ -n "$LOCAL_FULL" ]; then
    if [ "$LOCAL_FULL" = "$REMOTE_FULL" ]; then
      echo "Sync state:        in sync"
    else
      BEHIND="$(git rev-list --count HEAD..@{u} 2>/dev/null || echo 0)"
      AHEAD="$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)"
      echo "Sync state:        $AHEAD ahead, $BEHIND behind"
    fi
  fi
else
  echo "Remote HEAD:       (fetch failed — offline?)"
fi

echo ""
echo "Working tree:"
if [ -z "$(git status --porcelain)" ]; then
  echo "  clean"
else
  git status --short | sed "s/^/  /"
fi

echo ""
echo "Last 5 commits:"
git log --oneline -5 | sed "s/^/  /"

LOG_FILE="$PLUGIN_ROOT/.cache/auto_update.log"
if [ -f "$LOG_FILE" ]; then
  echo ""
  echo "Last 5 auto-update log entries:"
  tail -5 "$LOG_FILE" | sed "s/^/  /"
fi
'

Summarize the output for the user in plain language: are they in sync,
behind, ahead, or diverged. If behind, suggest `/skill-update`. If ahead,
suggest `/skill-publish`. If diverged, suggest manual resolution.
