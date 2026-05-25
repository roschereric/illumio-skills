# Maintenance Guide — Installing and Updating illumio-skills

This guide covers the full lifecycle of the `illumio-skills` marketplace on
any device: first-time install, daily auto-update, manual refresh,
publishing changes, troubleshooting, and rollback.

> **Audience.** Eric (across personal and work Macs) and any LATAM colleague
> granted access to the marketplace repo. Read sections 1 and 2 once per
> device; sections 3-5 as needed.

---

## 1. First-time install on a new device

### Prerequisites

- macOS or Linux with bash, git, and Python ≥ 3.10.
- `gh` CLI installed and authenticated as the user who has read access to
  `roschereric/illumio-skills`:
  ```bash
  brew install gh
  gh auth login
  ```
- One of:
  - Claude Code installed (recommended path — auto-update is native).
  - Or Cowork installed (fallback path — manual symlink + cron pull).

### Option A — Claude Code (recommended)

Inside any Claude Code session:

```
/plugin marketplace add roschereric/illumio-skills
/plugin install illumio-branded-reports@illumio-skills
```

**First-session caveat.** Due to [claude-code#10997](https://github.com/anthropics/claude-code/issues/10997),
the `SessionStart` hook does not fire on the very first session after
install — the marketplace cache lands during that first session, not before
it. So **run `/skill-update` once manually** after install. From the next
session onward, the hook auto-pulls at session start.

Verify the install:

```
/skill-status
```

Expected output: "in sync" with the local HEAD showing the latest commit
from `roschereric/illumio-skills@main`.

### Option B — Cowork fallback

Cowork doesn't yet support plugin marketplaces natively. Use the bundled
install script:

```bash
git clone https://github.com/roschereric/illumio-skills.git ~/.illumio-skills
bash ~/.illumio-skills/scripts/install_marketplace.sh --cowork-only
```

This clones the marketplace to `~/.illumio-skills` and symlinks the plugin
into the workshop folder's `.claude/skills/` directory. The skill becomes
visible the next time Cowork loads the workshop.

For ongoing updates on this device:

```bash
cd ~/.illumio-skills && git pull --ff-only
```

If you want it automated on Cowork-only devices, schedule a daily pull via
`launchd` (one-time setup):

```bash
cat > ~/Library/LaunchAgents/com.eric.illumio-skills-pull.plist << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.eric.illumio-skills-pull</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-lc</string>
    <string>cd ~/.illumio-skills && git pull --ff-only --quiet 2>&1 | logger -t illumio-skills</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
</dict>
</plist>
PLIST
launchctl load ~/Library/LaunchAgents/com.eric.illumio-skills-pull.plist
```

This runs `git pull --ff-only` daily at 09:00 local. Logs go to the system
log (`log show --predicate 'eventMessage contains "illumio-skills"' --info`).

### Option C — Both (most common Eric setup)

Install via Option A first (gets Claude Code working), then also run Option
B (gets Cowork working). Both paths share `~/.illumio-skills` underneath,
so you maintain a single local checkout.

---

## 2. Daily workflow — keeping up to date

### Auto-update (Claude Code)

Open any Claude Code session. The `SessionStart` hook fires before your
first prompt and runs `git fetch + git merge --ff-only` against
`origin/main`. Outcomes you might see:

| Outcome | What it means | What to do |
|---|---|---|
| (silent) | Already in sync, or pulled cleanly | Nothing — proceed |
| Log entry: "fast-forwarded ABC → XYZ" | Pulled new commits | Nothing — they're already active |
| Log entry: "local has unpushed commits" | You committed locally but didn't push | Run `/skill-publish` to push |
| Log entry: "local working tree has uncommitted changes" | You have uncommitted edits | Either commit them (run `/skill-publish`), stash them, or revert |
| Log entry: "diverged" | Local and origin both moved separately | Resolve manually — see section 4 |
| Log entry: "fetch failed (offline?)" | No network | Will retry on next session — no action needed |

You can read the auto-update log anytime:

```bash
cat ~/.claude/plugins/.../illumio-branded-reports/.cache/auto_update.log
```

Or invoke `/skill-status` inside a session for a clean summary.

### Manual refresh (when you can't wait for the next session)

```
/skill-update
```

This runs the same logic as the SessionStart hook but verbose — it prints
what it found and what it pulled. Use it when:

- You just pushed a change from another device and want it here NOW.
- The auto-update silently skipped and you want to know why.
- You suspect the local copy is stale.

### Cowork-only devices

No automatic refresh. Either:

- Open a Terminal and run `cd ~/.illumio-skills && git pull --ff-only`.
- Or rely on the launchd job (Option B above) for daily pulls.

---

## 3. Publishing a change

The marketplace pattern: edit any local copy, commit, push, and within
seconds every other device will pick up the change on next session start.

### From inside Claude Code

The simplest path. Inside any session, after editing files:

```
/skill-publish
```

By default this creates a timestamped branch (`skill-update-YYYYMMDD-HHMMSS`),
commits with a message you supply, pushes the branch, and opens a PR via
`gh`. You stay on `main` after.

For solo maintainers (you're the only one ever pushing), you can skip the
PR step:

```
/skill-publish --direct
```

This commits directly to `main` and pushes. Faster, less audit trail.

### From the Terminal

Same pattern, manually:

```bash
cd ~/.illumio-skills    # or wherever your local checkout lives
git status               # confirm what's about to be committed
git add -A
git commit -m "feat: short description per typed-prefix convention"
git push origin main
```

### Typed-prefix convention

| Prefix | When to use |
|---|---|
| `feat:` | New capability or major addition |
| `fix:` | Bug fix or correction |
| `ref:` | Refactor (same behavior, better structure) |
| `docs:` | Documentation only |
| `eval:` | Test cases / evals |
| `adapt:` | Platform adapter changes |

---

## 4. Troubleshooting

### "The skill on Device B isn't getting my updates from Device A"

Sequence to check:

1. On Device A: confirm the change is pushed.
   ```bash
   cd ~/.illumio-skills && git log -1 --oneline
   git status   # should say "Your branch is up to date with 'origin/main'"
   ```
2. On Device B: open a Claude Code session, then `/skill-status`. It will
   show `Remote HEAD` and `Sync state`.
3. If Device B says "behind by N": run `/skill-update`. Auto-update may
   have been blocked by uncommitted local edits — `/skill-status` will tell
   you.
4. If Device B says "already in sync" but the change still isn't visible:
   the local plugin install probably extracted to a different cache
   directory. Re-install:
   ```
   /plugin uninstall illumio-branded-reports
   /plugin install illumio-branded-reports@illumio-skills
   ```

### "iCloud created a `* 2.md` file in my workshop folder"

iCloud conflict artifact — happens when two devices edited the same file
while one was offline. **The marketplace is supposed to make this rare**
(GitHub is canonical, not iCloud), but stray edits in the iCloud working
copy can still trigger it.

Resolution:

1. Compare the two files: `diff foo.md "foo 2.md"`.
2. Pick the winner. Copy its content into the canonical name. Delete the
   loser.
3. Commit and push so GitHub has the resolution.

### "Diverged" — my local and origin both have new commits

```
local has 2 commit(s) not on origin
origin has 3 commit(s) not on local
```

Don't panic; don't force-push. Two options:

**Option 1 — rebase your local on top of origin:**
```bash
cd ~/.illumio-skills
git fetch origin
git rebase origin/main
# resolve any conflicts file by file
git push origin main
```

**Option 2 — push your local to a feature branch and open a PR:**
```bash
cd ~/.illumio-skills
git checkout -b fix/your-changes
git push -u origin fix/your-changes
gh pr create --base main --head fix/your-changes
```

If you're not sure which is right, prefer Option 2 — it keeps the change
reviewable and reversible.

### "The auto-update hook ran but my session still uses the old skill"

Claude Code's plugin loader sometimes caches skill content from a previous
session. Force a reload:

```
/plugin reload illumio-branded-reports
```

If that doesn't work, restart Claude Code.

### "I broke the skill and want to undo my last commit"

If you haven't pushed yet:
```bash
cd ~/.illumio-skills
git reset --hard HEAD~1
```

If you already pushed and it's on `main`:
```bash
cd ~/.illumio-skills
git revert HEAD            # creates a new commit that undoes the previous
git push origin main
```

Every device will pick up the revert on next session start. You can also
run `/skill-update` on each device immediately for instant rollback.

### "I want to test a change before pushing"

The local checkout IS the test environment. Edit `~/.illumio-skills/plugins/illumio-branded-reports/`,
start a fresh session, and the change is live for that session. When
satisfied, `/skill-publish`. When unsatisfied, `git checkout -- .` to
revert your unstaged edits.

---

## 5. Editing the skill

There are TWO sources of truth historically — that's a transitional state.
This guide reflects the target state.

### Target state (current)

- **Canonical source:** `roschereric/illumio-skills` on GitHub (the marketplace).
- **Local working copy:** `~/.illumio-skills/` on each device (clone of the marketplace).
- **Runtime install:** `~/.claude/plugins/.../illumio-branded-reports/` (Claude Code manages this; for Cowork, the symlink set up by Option B).

Editing flow:
1. `cd ~/.illumio-skills/plugins/illumio-branded-reports/`
2. Make changes to `SKILL.md`, references, etc.
3. Restart a Claude Code session to load the changes locally, OR run `/skill-update` to be sure the runtime sees them.
4. When satisfied, `/skill-publish` (or `cd ~/.illumio-skills && git commit && git push`).

### Transitional state (during marketplace bootstrap)

If the marketplace hasn't been pushed to GitHub yet (or you're working from
the iCloud workshop folder directly), the canonical is the standalone
`roschereric/illumio-branded-reports` repo. Edit there, commit there, push
there. Re-sync into the marketplace folder when ready to migrate.

This guide assumes the target state. Section 6 below covers the migration
from transitional → target.

---

## 6. Migrating from the standalone repo to the marketplace

One-time operation, performed when bootstrapping the marketplace on a fresh
GitHub repo. After this completes, the standalone repo (`roschereric/illumio-branded-reports`)
becomes an archive.

```bash
# 1. Create the marketplace repo on GitHub
gh repo create roschereric/illumio-skills --private \
  --description "Claude Code plugin marketplace for Illumio pre-sales engineering skills"

# 2. cd into the local marketplace checkout (already exists in iCloud)
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Claude/Projects/Illumio\ Skills/illumio-skills

# 3. Initialize git, push initial commit
git init
git branch -M main
git remote add origin https://github.com/roschereric/illumio-skills.git
git add -A
git commit -m "feat: bootstrap illumio-skills marketplace"
git push -u origin main

# 4. Install the marketplace on this device
bash scripts/install_marketplace.sh

# 5. (Optional) Update the old standalone repo's README to point at the new marketplace
cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/Claude/Projects/Illumio\ Skills/illumio-branded-reports
# Edit README.md to add a "This repo is archived" notice
git add README.md && git commit -m "docs: archive notice pointing to illumio-skills marketplace"
git push
```

After this, the standalone `~/.../illumio-branded-reports/` folder in your
workshop is a stale snapshot. You can either:

- Delete it: `rm -rf ~/Library/Mobile\ Documents/.../Illumio\ Skills/illumio-branded-reports/`
- Leave it as a historical reference (it stays out of the way)

---

## 7. Adding more skills to the marketplace

When you build a new skill (e.g., `illumio-knowledge-base`), add it to the
marketplace rather than creating a new standalone repo:

```bash
cd ~/.illumio-skills

# 1. Use the bundled helper
bash scripts/migrate_repo.sh ~/path/to/illumio-knowledge-base

# 2. Author plugin.json, hooks.json, commands/ for the new plugin
# (Copy from plugins/illumio-branded-reports/.claude-plugin/ as a template)

# 3. Update the marketplace manifest
# Edit .claude-plugin/marketplace.json — add a new entry to "plugins" array

# 4. Commit and push
git add -A
git commit -m "feat: add illumio-knowledge-base plugin"
git push
```

Colleagues will see the new plugin appear in `/plugin install` choices on
their next session.

---

## Quick reference card

```
First install (Claude Code):    /plugin marketplace add roschereric/illumio-skills
                                /plugin install illumio-branded-reports@illumio-skills
                                /skill-update     # one-time, due to hook misfire

Daily check:                    /skill-status

Refresh now:                    /skill-update

Publish a change:               /skill-publish

Roll back a change:             cd ~/.illumio-skills && git revert HEAD && git push

Diagnose drift:                 /skill-status
                                cat ~/.claude/plugins/.../*/scripts/.cache/auto_update.log
```
