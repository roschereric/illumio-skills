#!/usr/bin/env bash
# install_marketplace.sh — One-time setup for a new Mac.
#
# Adds the illumio-skills marketplace to Claude Code and installs the
# illumio-branded-reports plugin. Also creates a fallback symlink for
# Cowork (which does not yet support plugin marketplaces natively).
#
# Usage:
#   bash scripts/install_marketplace.sh
#   bash scripts/install_marketplace.sh --cowork-only    # skip Claude Code commands
#   bash scripts/install_marketplace.sh --claude-only    # skip Cowork symlink

set -eu

MARKETPLACE_REPO="roschereric/illumio-skills"
INSTALL_CLAUDE=1
INSTALL_COWORK=1

while [ $# -gt 0 ]; do
  case "$1" in
    --cowork-only) INSTALL_CLAUDE=0; shift ;;
    --claude-only) INSTALL_COWORK=0; shift ;;
    -h|--help)
      sed -n '1,12p' "$0"
      exit 0 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

echo "=== illumio-skills marketplace install ==="
echo ""

# ----- Claude Code install path -----
if [ "$INSTALL_CLAUDE" -eq 1 ]; then
  if command -v claude >/dev/null 2>&1; then
    echo "Adding marketplace to Claude Code..."
    claude /plugin marketplace add "$MARKETPLACE_REPO" || {
      echo "WARNING: 'claude /plugin marketplace add' failed. You may need to"
      echo "run it manually inside a Claude Code session."
    }
    echo ""
    echo "Installing illumio-branded-reports plugin..."
    claude /plugin install "illumio-branded-reports@illumio-skills" || {
      echo "WARNING: 'claude /plugin install' failed. Run manually inside a session."
    }
    echo ""
    echo "NOTE: due to claude-code#10997, the SessionStart hook does not fire"
    echo "      on the very first session after install. Run /skill-update once"
    echo "      manually after your first session starts."
  else
    echo "claude CLI not found; skipping Claude Code install."
    echo "If you want Claude Code support, install it from:"
    echo "  https://docs.claude.com/en/docs/claude-code"
  fi
fi

# ----- Cowork install path (fallback: clone + symlink) -----
if [ "$INSTALL_COWORK" -eq 1 ]; then
  echo ""
  echo "Setting up Cowork install (clone + symlink)..."

  CLONE_DIR="${HOME}/.illumio-skills"
  if [ -d "$CLONE_DIR/.git" ]; then
    echo "  Clone exists at $CLONE_DIR; pulling latest..."
    (cd "$CLONE_DIR" && git pull --ff-only --quiet) || {
      echo "WARNING: pull failed; not in sync"
    }
  else
    echo "  Cloning to $CLONE_DIR..."
    git clone "https://github.com/${MARKETPLACE_REPO}.git" "$CLONE_DIR"
  fi

  # Cowork reads skills from .claude/skills/ inside the mounted workspace folder.
  # We can't predict which folder the user mounts, but we can place a symlink
  # in a common workshop location.
  WORKSHOP_CANDIDATES=(
    "${HOME}/Library/Mobile Documents/com~apple~CloudDocs/Documents/Claude/Projects/Illumio Skills"
    "${HOME}/Projects/Illumio Skills"
  )

  for WORKSHOP in "${WORKSHOP_CANDIDATES[@]}"; do
    if [ -d "$WORKSHOP" ]; then
      mkdir -p "$WORKSHOP/.claude/skills"
      LINK_PATH="$WORKSHOP/.claude/skills/illumio-branded-reports"
      if [ -L "$LINK_PATH" ]; then
        rm "$LINK_PATH"
      fi
      ln -s "$CLONE_DIR/plugins/illumio-branded-reports" "$LINK_PATH"
      echo "  Linked $LINK_PATH -> $CLONE_DIR/plugins/illumio-branded-reports"
    fi
  done
fi

echo ""
echo "Install complete."
echo ""
echo "Next steps:"
echo "  - In Claude Code: open a session, then run /skill-update once."
echo "  - In Cowork: mount the workshop folder; the skill will be visible at"
echo "    .claude/skills/illumio-branded-reports."
