# illumio-skills

Claude Code plugin marketplace for Illumio pre-sales engineering skills.
Distributes each skill as a versioned plugin with `SessionStart` auto-update
and slash-command publishing. Designed so a single GitHub repo is the
canonical source of truth for every device and every collaborator.

---

## Available plugins

| Plugin | Description |
|---|---|
| `illumio-branded-reports` | Generate branded PDF and HTML reports with WeasyPrint. Includes programmatic visual verification, PII guardrails, and bilingual EN/ES support. |

## Quick install

### Claude Code

In any Claude Code session:

```
/plugin marketplace add roschereric/illumio-skills
/plugin install illumio-branded-reports@illumio-skills
```

> **First-session caveat.** Due to [claude-code#10997](https://github.com/anthropics/claude-code/issues/10997),
> the `SessionStart` hook does not fire on the very first session after
> install. Run `/skill-update` once manually after your first session
> starts. From then on, auto-update works as expected.

### Cowork (fallback path — manual install)

Cowork does not yet support plugin marketplaces natively. Until it does,
use the install script:

```bash
# One-time setup per Mac
gh repo clone roschereric/illumio-skills ~/.illumio-skills
bash ~/.illumio-skills/scripts/install_marketplace.sh --cowork-only
```

This clones the marketplace to `~/.illumio-skills` and symlinks the
plugin into your workshop's `.claude/skills/` directory. To refresh
later:

```bash
cd ~/.illumio-skills && git pull --ff-only
```

## Daily workflow

| Goal | How |
|---|---|
| See the latest version on a device | Open a Claude Code session — `SessionStart` hook pulls automatically. Or run `/skill-update` to force a pull mid-session. |
| Check what's installed locally vs. on GitHub | `/skill-status` |
| Publish a local change | `/skill-publish` (creates a branch + PR by default; `/skill-publish --direct` to push to main for solo maintainers) |
| Roll back a bad change | `git revert` on the marketplace repo, then `git push`. Every device picks up the revert on next session start. |

## How the plugin works

Each plugin folder contains the standard Claude Code plugin shape:

```
plugins/<name>/
├── .claude-plugin/plugin.json     ← plugin manifest
├── hooks/hooks.json               ← SessionStart hook registration
├── scripts/                       ← hook bodies + slash command bodies
│   ├── auto_update.sh             ← runs on SessionStart, silent on happy path
│   ├── manual_update.sh           ← body of /skill-update, verbose
│   └── publish_changes.sh         ← body of /skill-publish
├── commands/                      ← slash command definitions
│   ├── skill-update.md
│   ├── skill-publish.md
│   └── skill-status.md
└── (the skill itself)
    ├── SKILL.md
    ├── template.html
    ├── styles/
    ├── assets/
    ├── references/
    ├── scripts/
    ├── evals/
    └── adapters/
```

The `auto_update.sh` script is the centerpiece. On every session start it:

1. Checks the local working tree for uncommitted changes → skips if dirty.
2. `git fetch` with a 5-second timeout → fails open if offline.
3. Compares local HEAD to `origin/main`:
   - In sync → done.
   - Local behind, no divergence → `git merge --ff-only`.
   - Local ahead → log a hint to run `/skill-publish`, otherwise skip.
   - Diverged → log and skip; manual resolution required.

All actions are logged to `plugins/<name>/.cache/auto_update.log` for
auditing.

## Why this exists

Originally, the canonical source of truth for these skills was an iCloud-
synced folder. That worked for cross-Mac sync of Eric's own devices but
had two failure modes: (1) the runtime skill version that Cowork loaded
could drift from the canonical iCloud copy, and (2) sharing with
colleagues required them to be in the same iCloud household.

The marketplace pattern fixes both by declaring GitHub the canonical
source. Every device — Eric's personal Mac, his work Mac, a colleague's
Mac — pulls from the same branch via the `SessionStart` hook. Edits go
through `git commit → git push → next session everywhere updates`.

Architecture decision: see
[`ADR-001 — Skill distribution`](https://github.com/roschereric/illumio-skills/blob/main/docs/adr-001-skill-distribution.md)
once we publish the ADR to this repo (currently lives in the workshop).

## License

Proprietary — for use by Eric Roscher and authorized Illumio LATAM
colleagues. Contact `roschereric@gmail.com` for access requests.

<!-- BEGIN illumio-skill-update:cross-env -->
## Updating the skill across your Cowork environments

This is a GitHub-backed marketplace plugin. **`main` in this repo is the single source of
truth** — every Mac / Cowork environment syncs from it, so you do **not** need to know which
machine originally created the skill.

**Publish a change** (from any machine or Cowork notebook with network + a token):

```bash
GH_TOKEN="$(gh auth token)"  bash publish_skill_update.sh     # or GH_TOKEN=<PAT>
```

The script clones this repo, applies the managed updates (marker-guarded, safe to re-run),
updates this README, and pushes to `main`.

**Apply the latest in each environment** (do this once per Mac / per Cowork space):

- It auto-updates on session start (`auto_update.sh` pulls from `main`), or force it:
  - `/illumio-branded-reports:skill-update`  — pull the latest from GitHub
  - `/illumio-branded-reports:skill-status`  — show local vs origin (should say *in sync*)

**Verify the guardrail is active:** a fresh session runs `python scripts/preflight_check.py`
and passes; if a partial/stale copy ever loads, the build stops with an error instead of
producing off-brand output (wrong logo / system fonts).
<!-- END illumio-skill-update:cross-env -->
