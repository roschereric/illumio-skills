#!/usr/bin/env bash
# migrate_repo.sh — One-time helper to bootstrap the marketplace.
#
# Copies an existing standalone skill repo into the plugins/ layout of
# this marketplace. Use it once per skill being migrated. After running,
# review the result, commit, and push.
#
# Usage:
#   bash scripts/migrate_repo.sh ../illumio-branded-reports
#   bash scripts/migrate_repo.sh /path/to/some-other-skill
#
# What it does NOT do:
#   - Preserve git history of the source repo. The source repo stays on
#     GitHub as an archive; this marketplace has its own history starting
#     fresh. If you need history preservation, use `git filter-repo
#     --to-subdirectory-filter plugins/<name>` against a clone of the source
#     repo, then `git merge --allow-unrelated-histories` into this marketplace.
#   - Delete the source repo. That's a separate, manual decision.

set -eu

if [ $# -ne 1 ]; then
  echo "Usage: bash scripts/migrate_repo.sh <path-to-source-skill-folder>"
  exit 1
fi

SRC="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MARKETPLACE_ROOT="$(dirname "$SCRIPT_DIR")"

if [ ! -d "$SRC" ]; then
  echo "ERROR: source path does not exist: $SRC"
  exit 1
fi
if [ ! -f "$SRC/SKILL.md" ]; then
  echo "ERROR: $SRC has no SKILL.md — not a skill folder?"
  exit 1
fi

SKILL_NAME="$(basename "$SRC")"
DEST="$MARKETPLACE_ROOT/plugins/$SKILL_NAME"

if [ -d "$DEST" ] && [ "$(ls -A "$DEST" 2>/dev/null | grep -v '^\.claude-plugin$' | wc -l)" -gt 0 ]; then
  echo "ERROR: $DEST already has content. Refusing to overwrite."
  echo "Remove or rename the destination, then re-run."
  exit 1
fi

mkdir -p "$DEST"

echo "Copying $SRC/ → $DEST/ (excluding .git and .DS_Store)..."
(cd "$SRC" && find . \
  -name '.git' -prune -o \
  -name '.DS_Store' -prune -o \
  -name '__pycache__' -prune -o \
  -type f -print0) | \
  (cd "$SRC" && xargs -0 -I{} cp --parents {} "$DEST/" 2>/dev/null) || \
  (cd "$SRC" && find . \
    -name '.git' -prune -o \
    -name '.DS_Store' -prune -o \
    -name '__pycache__' -prune -o \
    -type f -print | while read -r f; do
      mkdir -p "$DEST/$(dirname "$f")"
      cp "$SRC/$f" "$DEST/$f"
    done)

# Preserve the existing .claude-plugin/plugin.json that migrate_repo expects
# to find from the marketplace bootstrap (don't overwrite with anything from src).
if [ ! -f "$DEST/.claude-plugin/plugin.json" ]; then
  echo "WARNING: $DEST/.claude-plugin/plugin.json was not present after copy."
  echo "Make sure the marketplace was bootstrapped before running this script."
fi

echo ""
echo "Migration complete."
echo "  Source:      $SRC"
echo "  Destination: $DEST"
echo ""
echo "Next steps:"
echo "  1. cd $MARKETPLACE_ROOT"
echo "  2. Review what changed: git status"
echo "  3. Commit: git add -A && git commit -m \"feat: migrate $SKILL_NAME into marketplace\""
echo "  4. Push: git push origin main"
echo "  5. (Optional) Archive the source repo $SRC on GitHub by updating its README"
echo "     to point at https://github.com/roschereric/illumio-skills."
