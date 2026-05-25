# ADR-001 — Skill distribution: GitHub-hosted Claude Code marketplace

**Status:** Accepted (May 2026) — implementation deferred to a follow-up project after the bug-fix merge for `illumio-branded-reports`.
**Decider:** Eric Roscher.
**Scope:** All skills in the Illumio Skills Lab.

---

## Context

The Skills Lab is used across multiple devices (personal Mac + Illumio-issued work Mac) and is intended to be shareable with LATAM colleagues. Until now, distribution has relied on **iCloud Drive replicating the workshop folder**, with **GitHub per-skill repos** acting as a snapshot/recovery layer (see CLAUDE.md §6).

Two problems with this model surfaced during real use:

1. **Runtime version mismatch.** Claude Cowork loads skills from a session-scoped working copy (e.g., a read-only plugin-extraction mount). When a session edits a skill, the changes don't always live where the next session reads from. The iCloud canonical copy and the runtime copy can drift silently. This is the failure that forced the May 2026 `illumio-branded-reports` post-mortem session to draft updates in a separate folder instead of editing the canonical skill.
2. **Colleague sharing.** iCloud is a personal-account file-sync mechanism. A LATAM colleague cannot subscribe to a skill via iCloud unless they're a member of Eric's iCloud household, which is not the right relationship. The current workaround (commit + push to GitHub + colleague clones + runs `deploy-to-cowork.sh`) works but has no auto-update — colleagues have to remember to pull.

A third concern is **corporate MDM risk**: if the Illumio work Mac's MDM ever restricts iCloud Drive, the entire dev path breaks. iCloud is a single point of failure.

## Decision

**Wrap each skill as a Claude Code plugin inside a public GitHub repo that is itself a marketplace.** Distribution mechanics:

- Skills are installed via `claude /plugin marketplace add roschereric/illumio-skills` and `claude /plugin install <skill>@illumio-skills`.
- A `SessionStart` hook in each plugin runs `git fetch && git pull --ff-only` against `main` at the start of every Cowork or Claude Code session. Fails open if offline; refuses if local edits exist.
- An on-demand `/skill-update` slash command pulls explicitly when the user wants to refresh mid-session.
- A `/skill-publish` slash command branches, commits, and opens a PR via the `gh` CLI for changes that originated on the local copy.
- GitHub Actions on every PR run lint and dogfood checks (manifest JSON-lint, SKILL.md frontmatter validation, a sample render against the verification toolchain).

**GitHub `main` becomes the canonical source of truth.** The iCloud working copy remains the dev environment where edits happen — but the runtime version on every device is fetched from GitHub, not from iCloud. iCloud's role narrows to "convenient local edit surface across Eric's own Macs"; it is no longer the transport layer for skill content.

For the linkage between the iCloud working copy and the runtime install location, **symlink** the plugin install directory to the iCloud working copy on each Mac. This lets Eric edit in the iCloud folder and see the change in the next session immediately — while `commit + push` is what propagates the change to other devices and colleagues.

## Alternatives considered

### Alternative 1 — Keep iCloud as the distribution layer (status quo)

- **Pros:** zero setup beyond what already exists.
- **Cons:** does not solve runtime version mismatch (the root failure of the May 2026 post-mortem). Does not solve colleague sharing. Vulnerable to corp MDM restrictions on iCloud. Symlinks inside iCloud are unreliable.

### Alternative 2 — Plain git + cron pull + symlinks

- Each Mac has the iCloud workshop folder symlinked into `~/.claude/skills/`. A launchd job runs `git pull --rebase` on every skill repo daily.
- **Pros:** lighter-weight than the marketplace; no Claude Code-specific plumbing.
- **Cons:** still no auto-update on session start (relies on launchd timing). No native distribution to colleagues — they still have to clone manually. No PR workflow for publishing changes. Updates are "eventual" rather than "every session."

### Alternative 3 — Anthropic-hosted skill registry (hypothetical)

- If Anthropic ever ships a first-party skill registry, switch to it.
- **Pros:** zero infrastructure.
- **Cons:** does not exist yet; not actionable.

## Consequences

### Positive

- **Single source of truth.** Every device, every session, every colleague's install reads from the same GitHub branch. No more "which version did this session load?" ambiguity.
- **Auto-update is real.** The `SessionStart` hook makes "edit → commit → push → everyone has it next session" the default workflow.
- **Colleague distribution becomes trivial.** Add them as a collaborator on the GitHub marketplace repo, send them the two install commands, and they're synced going forward.
- **Survives MDM restrictions on iCloud.** Git over HTTPS works through corporate networks even when consumer cloud sync is blocked.
- **Aligns with the workshop's dev/prod model.** iCloud is dev (where edits happen on Eric's own machines), GitHub is prod (where the canonical version lives and where every install pulls from). This crystallizes a separation that was already implicit.

### Negative

- **Architectural shift.** GitHub becomes load-bearing in a way it wasn't before. If a colleague's `gh auth` lapses or the GitHub repo is unreachable, the `SessionStart` hook fails open but no updates land — silent drift unless someone notices the staleness.
- **Two file locations per skill.** The iCloud working copy (edit surface) and the plugin install location (runtime). Bridged via symlink, but the user needs to understand the relationship to avoid confusion ("why didn't my edit show up?" — answer: it did locally via the symlink, but other devices won't see it until `git push`).
- **First-session hook misfire.** Known Claude Code issue: the `SessionStart` hook does not fire on the very first session after `marketplace add`, because the marketplace cache lands during that session rather than before it. Workaround: run `/skill-update` once after install. Referenced upstream: `anthropics/claude-code#10997`.
- **GitHub Actions cost.** Validation workflow runs on every PR. Cheap (~minutes/month) but non-zero.

### Neutral

- **Cross-LLM portability is unchanged.** The marketplace solves cross-*device* consistency for Claude products only. Cross-*platform* portability (Gemini, ChatGPT, Perplexity, local LLMs) still goes through each skill's `adapters/` folder as before. The two mechanisms are orthogonal — a single skill can be both marketplace-distributed for Claude *and* adapter-ported for other platforms.

## Implementation plan (follow-up project)

Not part of this ADR's acceptance — captured here so the decision has a clear path forward.

1. Create `roschereric/illumio-skills` GitHub repo as the marketplace root.
2. Migrate `illumio-branded-reports/` into `plugins/illumio-branded-reports/` inside that repo, using `git mv` to preserve history.
3. Author manifests: `.claude-plugin/marketplace.json`, `plugins/illumio-branded-reports/.claude-plugin/plugin.json`.
4. Author hooks: `SessionStart` ff-only pull, with the offline/local-edit guards.
5. Author slash commands: `/skill-update`, `/skill-publish`, `/skill-status`.
6. Author CI: manifest lint, frontmatter validation, sample render.
7. Author `scripts/install_marketplace.sh` (per-Mac install) and document it in the workshop README.
8. Migrate `illumio-knowledge-base` and any other skills to the same marketplace.
9. Update CLAUDE.md §6 to reflect the new topology: GitHub is canonical via marketplace, iCloud is the local edit surface, symlinks bridge runtime to iCloud on each Mac.
10. Deprecate the iCloud-symlink fallback for skill distribution. Keep iCloud for ad-hoc working files, drafts, and the `_merge-staging/` workflow.

## Revisit triggers

Revisit this decision if:
- Anthropic ships a first-party skill registry that supersedes marketplaces.
- The `SessionStart` hook misfire becomes a persistent annoyance rather than a once-per-install workaround.
- Eric stops needing colleague distribution (back to a single user) — at which point iCloud-only would be simpler.
- Two-mac iCloud sync becomes more reliable for symlinks (unlikely, but documented as a watch-item).
