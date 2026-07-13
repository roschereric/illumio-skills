# Fact Verification & Official-Documentation Citations

> **When to read this:** MANDATORY during content drafting (Workflow step 2)
> and again before the brand check. Reports produced by this skill go to
> customers, partners, and Illumio leadership — a wrong port number, service
> name, or CLI flag in a branded PDF looks authoritative and does damage.

The rule: **every verifiable technical claim is either (a) verified against
current official documentation and cited, (b) explicitly marked as an
assumption/`<PLACEHOLDER>`, or (c) removed.** Never ship a fact you could not
verify just because it "sounds right" from training data.

---

## §1 — Claims that MUST be verified before they appear in a report

- Product versions, release names, EOL/EOS dates (Illumio PCE/VEN, OS versions, cloud services)
- Service names, process names, file paths, registry keys (e.g. the VEN Windows service is `venAgentMgrSvc` in current releases — legacy docs say `intpcad`)
- Ports, protocols, firewall/NSG requirements, connectivity matrices
- CLI commands, PowerShell cmdlets, API endpoints, flags and their defaults
- Enforcement-state names and UI labels (current: Idle / Visibility Only / Selective / Full)
- Sizing figures, scale limits, supported-platform matrices, license SKUs
- Competitor claims (only from public, citable sources — never invent comparisons)
- Cloud-provider specifics (Azure/AWS/GCP service names, quotas, pricing tiers)

**Diagrams are claims too.** Every box, arrow, port label, and flow in an SVG
diagram must be backed by a claim already verified in the text. A diagram that
shows a flow the verified text does not describe is a hallucination with a
border radius. After drawing, re-read each diagram element and ask: *"which
verified statement does this element depict?"* Remove or fix any element
without an answer.

## §2 — Verification protocol

1. **Inventory.** While drafting, keep a claims list: `claim → status
   (verified / assumed / user-supplied) → source URL`.
2. **Verify against CURRENT official sources** (web search/fetch, or connected
   MCP docs tools). Prefer, in order: vendor product docs → vendor KB/release
   notes → vendor blog/announcements. Community posts are corroboration, not
   proof.
3. **Version-check.** Illumio moved docs between generations; make sure the
   page you cite matches the customer's product generation and version.
4. **Unverifiable?** Do ONE of: ask the user, mark `<TO-VERIFY: claim>`, or
   cut the claim. Never leave it silently unverified. `<TO-VERIFY>` markers
   must be resolved (user confirms or claim removed) before final delivery —
   `check_brand.py` warns on leftover placeholders.
5. **Cite.** Add the source to the section's `.ref-list` (see §4).

## §3 — Primary official sources

| Domain | Use for | Notes |
|---|---|---|
| `product-docs-repo.illumio.com/Tech-Docs/` | Current PCE/VEN/Core docs | **Preferred.** Pick the version folder matching the customer (e.g. `Core/25.x/`) |
| `docs.illumio.com` | Legacy generations only | Verify the page's version banner — much of it is outdated |
| `support.illumio.com` / KB | Known issues, compatibility (OS support matrix), EOL notices | Login may be required — ask the user for exports if blocked |
| `www.illumio.com` | Positioning, product names, public claims | Marketing language — not a technical source |
| `learn.microsoft.com`, `docs.aws.amazon.com`, `cloud.google.com` | Cloud-provider facts | Always link the exact page, not the docs root |
| Other vendors' official docs | Third-party integration details | Same rule: exact page |

Search patterns that work well: `site:product-docs-repo.illumio.com <term>`,
`illumio VEN <version> release notes <term>`.

**Known legacy→current traps** (verify, don't assume):
- VEN Windows service: `intpcad` (legacy) → `venAgentMgrSvc` (current)
- Enforcement states: Build/Test (legacy) → Visibility Only/Selective (current)
- VEN control tool: `.ps1` only (legacy) → `.ps1` and `illumio-ven-ctl.exe` (newer VENs)
- Docs URLs themselves move — re-search rather than pasting remembered URLs,
  and fetch every URL you cite to confirm it resolves (no dead links in a PDF).

## §4 — Citations in the document (print-first)

A PDF is read on paper and in screen-share — links must be VISIBLE, not only
clickable. Two sanctioned patterns:

**Inline superscript + per-section sources block (preferred):**

```html
<p>El servicio del VEN en Windows es <code>venAgentMgrSvc</code><sup class="ref">1</sup> …</p>
…
<div class="ref-list">
  <div class="ref-title">Sources — official documentation</div>
  <ol>
    <li><a href="https://product-docs-repo.illumio.com/Tech-Docs/Core/25.x/...">
        Illumio Core 25.x — VEN Administration: Windows services —
        product-docs-repo.illumio.com/Tech-Docs/Core/25.x/…</a></li>
  </ol>
</div>
```

**Rules:**
- The visible link text INCLUDES the domain/path (readable on paper).
- One `.ref-list` per section that states technical facts, placed at the end
  of the section (same page as the claims — `break-inside: avoid` keeps it whole).
- Number `<sup class="ref">` markers per section (restart at 1 each section).
- Every URL cited was actually opened during verification. No remembered URLs.
- Version-stamp when relevant: "Core 25.2, consulted July 2026".

## §5 — What NEVER goes in unverified

Names/emails/orgs (see `personal-info-policy.md`), pricing and licensing
figures, dates and deadlines, deal- or customer-specific values, benchmark
numbers, and any statement about a competitor. These are ask-the-user or
placeholder items, not web-verifiable facts.
