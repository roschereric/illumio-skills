# Troubleshooting — Plugin Updates Not Reaching Claude (Cowork / Claude Code)

> **Audience:** maintainers AND AI assistants debugging "I published a new
> version but Claude still runs the old one." Based on a real four-layer
> incident (July 2026) where every layer masked the next. Work top-down;
> verify each layer before moving on.

## Quick symptom matrix

| Symptom | Likely layer | Fix section |
|---|---|---|
| Skill behaves like an old version / ignores new rules | Duplicate account-level skill shadowing the plugin | §1 |
| Fresh session reports an old `plugin.json` version although GitHub is updated | Version pinning — no version bump published | §2 |
| Plugin page shows "Last updated: N weeks ago", Update button inert | Version pinning (§2) or broken sync (§4) |
| Local git clone never fast-forwards on session start | SessionStart hook broken | §3 |
| "Marketplace sync failed. Check the repository URL and try again." | Server-side content validation rejected the plugin | §4 |
| Claude Code CLI installs fine, Cowork app refuses the same repo | §4 — CLI is permissive, Cowork server validation is strict |

## §0 — Establish ground truth FIRST

Never debug from local state. Verify what GitHub actually serves:

```bash
git ls-remote https://github.com/roschereric/illumio-skills.git HEAD
rm -rf /tmp/vc && git clone --depth 1 -q https://github.com/roschereric/illumio-skills.git /tmp/vc
python3 -c "import json; print(json.load(open('/tmp/vc/plugins/illumio-branded-reports/.claude-plugin/plugin.json'))['version'])"
bash -n /tmp/vc/plugins/illumio-branded-reports/scripts/*.sh && echo scripts-OK
```

If GitHub is wrong, fix and push before touching any client.

**Know the three registries.** A plugin lives in three independent places;
updating one never updates the others:

1. **Claude Code CLI** (per machine): `claude plugin marketplace update illumio-skills`
   then `claude plugin update illumio-branded-reports@illumio-skills`.
2. **Cowork / Claude app** (account level): Customize → Plugins → plugin page
   → **Update** button (or remove + re-add the marketplace). This is what
   cloud sessions are provisioned from.
3. **Running sessions**: ephemeral copies provisioned at session start.
   Editing them proves nothing and propagates nowhere.

**Verification ritual** after any fix: open a **brand-new** conversation and
ask *"Read the illumio-branded-reports plugin.json and tell me the version."*
Only a fresh session exercises the provisioning chain.

## §1 — Duplicate account-level skill shadows the plugin

**Symptom:** Claude sometimes follows an older SKILL.md even though the
plugin is current; two skills with the same name appear in listings.

**Fix:** claude.ai → Customize → Skills → find the STANDALONE
`illumio-branded-reports` (not the plugin-namespaced one) → disable → "…"
→ Delete. The plugin must be the single source.

## §2 — Version pinning: content changes without a version bump are invisible

Per Claude Code marketplace semantics: if `version` is set in `plugin.json`
or in the `marketplace.json` plugin entry, **users only receive updates when
that string changes**. Pushing new content under the same version looks like
"nothing new" to the Update button and to account-level sync.

**Fix / prevention:** every release bumps the version in BOTH files:
`plugins/<plugin>/.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` (kept in sync; CI enforces equality).
Then the app's Update button lights up and works.

## §3 — SessionStart auto-update hook silently broken

**Symptom:** Claude Code shows `SessionStart:startup hook error … syntax
error near unexpected token` on launch; git clones never fast-forward.

**Cause (July 2026):** `auto_update.sh` closed an `if/then` block with `}`
instead of `fi`. Shipped unnoticed because the CI failure wasn't watched.

**Fix:** `bash -n plugins/*/scripts/*.sh` locally before publishing; CI runs
shellcheck — **treat a red X on main as a stop-ship**. Consider enabling
branch protection so main cannot advance with failing checks.

## §4 — Cowork server-side validation: "Marketplace sync failed"

**Symptom:** the app's Add-marketplace dialog fails with a generic
*"Marketplace sync failed. Check the repository URL and try again."* even
though the URL is correct and `git clone` works everywhere. Claude Code CLI
accepts the same repo fine.

**Reality:** the Cowork app syncs through Anthropic's server, which VALIDATES
plugin content strictly and reports only a generic error in the UI. The real
reason is in the app logs on macOS:

```bash
grep -iaE "marketplace|failed_content" ~/Library/Logs/Claude/claude.ai-web.log | tail -5
grep -a "remoteMarketplaceOps\|pollSyncUntilDone" ~/Library/Logs/Claude/main.log | tail -10
```

Look for `status: failed_content` with a per-plugin `error` message. In the
July 2026 incident it was:

> `Unknown hook field(s) ['$schema'] in hooks config. Hooks must only use
> fields the approval UI can display`

The `$schema` editor-hint field in `hooks/hooks.json` — harmless to Claude
Code — fails Cowork's remote validation, and the app then deletes the
half-created marketplace (`deleteAccountMarketplace` in main.log), so the
plugin vanishes entirely.

**Fix / prevention:** hooks.json (and manifests generally) contain ONLY
documented fields — no `$schema`, no comments-by-convention keys. CI now
rejects unknown hook fields. If a documented field is rejected by the
server, that is an Anthropic-side schema gap: report it (the error text says
as much) and remove the field meanwhile.

**Note on grandfathering:** an install that predates a validation rule keeps
working and keeps showing old content ("Last updated: N weeks ago") while
every re-sync fails. That combination — old snapshot + generic sync error —
is the signature of this layer.

## Appendix — editing the repo through a Cowork session (device bridge)

The mounted folder forbids `unlink`, so git leaves phantom `*.lock` files and
`tmp_obj_*` litter that later block commits ("Unable to create HEAD.lock:
File exists"). Recover from a REAL terminal on the machine:

```bash
cd ~/illumio-skills && rm -f .git/*.lock .git/index.lock .git/objects/maintenance.lock
```

Then commit/push normally. Prefer doing final git operations in a local
terminal; use the bridge for file content only.

## Release checklist (the "never again" list)

1. Bump `version` in `plugin.json` AND `marketplace.json` (equal strings).
2. `bash -n` / shellcheck every `*.sh`; valid JSON everywhere; no unknown
   fields in hooks/manifests. (CI enforces — keep main green.)
3. Update `README.md` changelog.
4. Push to main; confirm `git ls-remote` shows the new SHA.
5. In the app: plugin page → **Update** → "Last updated" flips to now and
   Version shows the new string.
6. Fresh-session verification question returns the new version.
