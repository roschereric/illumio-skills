---
description: Commit local changes to illumio-skills plugins, push to GitHub, and open a PR (or push direct to main with --direct).
argument-hint: [-m "commit message"] [--direct]
allowed-tools: Bash
---

Run the publish script with any arguments the user provided:

!bash "${CLAUDE_PLUGIN_ROOT}/scripts/publish_changes.sh" $ARGUMENTS

Behavior:
- If the user did NOT supply `-m "..."`, the script will prompt for a commit
  message. The typed-prefix convention applies (`feat:`, `fix:`, `ref:`,
  `docs:`, `eval:`, `adapt:`).
- By default the script creates a timestamped branch and opens a PR via
  `gh`. The user remains on `main` after the PR is opened.
- If the user passed `--direct`, the script commits to `main` and pushes
  directly. Only use this when the user is a solo maintainer of the
  marketplace.

After the script finishes, report the PR URL (if a PR was opened) or the
new HEAD SHA (if direct-pushed). Remind the user that other devices will
pick up the change automatically on next session start, or immediately via
`/skill-update`.
