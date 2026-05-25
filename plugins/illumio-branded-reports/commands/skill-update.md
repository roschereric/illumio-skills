---
description: Pull the latest version of illumio-skills plugins from GitHub. Verbose — explains what was fetched and what changed.
allowed-tools: Bash
---

Run the marketplace-update script:

!bash "${CLAUDE_PLUGIN_ROOT}/scripts/manual_update.sh"

If the script reports new commits, summarize the changes for the user from
the `git diff --stat` output it printed. If the script reports the local
copy is ahead of origin, remind the user they can run `/skill-publish` to
push their changes.
