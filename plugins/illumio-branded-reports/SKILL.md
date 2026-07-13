---
name: illumio-branded-reports
description: >
  Generate professional branded PDF and HTML reports using Illumio's visual identity
  (or adaptable to other brands). Produces print-ready A4 documents with running page
  headers, architecture diagrams, code blocks, callouts, and phase-based deployment guides.
  Uses WeasyPrint for HTML-to-PDF conversion with CSS Paged Media features.
  MANDATORY: Use this skill whenever the user asks to create a report, guide, runbook,
  deployment document, technical brief, one-pager, or any professional document for
  Illumio customers. Also trigger when the user mentions "branded PDF", "print-ready
  document", "customer-facing guide", "deployment guide", "technical document with
  diagrams", or asks to format content in Illumio style.
---

# Illumio Branded Report Generator

Print-ready A4 PDF + HTML documents in Illumio's Orange & Slate identity
(#FF5500 / #313638, Montserrat, isometric pattern motif (official Pattern & Shape system)). The pipeline is
**script-driven and fail-closed**: canonical template, hash-checked CSS,
official logo assets, bundled fonts, and deterministic gates between you and
delivery. Your job is the CONTENT; the scripts own the skeleton and brand.

## HARD RULES — non-negotiable, in force for the entire run

1. **Never hand-write the skeleton.** Every report starts with
   `python <skill>/scripts/new_report.py`. Never re-type the HTML boilerplate,
   the CSS, or an "equivalent" structure from memory — even for a "quick" doc.
2. **Edit only between the markers.** In the scaffolded `report.html`, write
   content ONLY between `<!-- ===== SECTIONS START -->` and
   `<!-- ===== SECTIONS END -->`, plus small print tweaks in
   `<style id="doc-overrides">` (≤ ~40 lines). `styles/report.css` and
   `assets/copy.js` are READ-ONLY and hash-verified; no other scripts or
   styles are permitted in the document.
3. **Official logos only, byte-identical.** `assets/logo-white.png` (orange/
   slate backgrounds) and `assets/logo-dark.png` (light backgrounds). Never
   redraw, approximate, recolor via CSS `filter`, or substitute a text
   wordmark — in ANY font, for ANY reason.
4. **No network at render time.** Fonts are bundled in `assets/fonts/`; no
   Google Fonts links, no external images, no base64 blobs.
5. **Never invent facts or identities.** Personal/org data →
   `references/personal-info-policy.md`. Technical claims (versions, ports,
   service names, commands, diagrams) → verify against current official docs
   and cite them → `references/fact-verification.md`.
6. **Gates are blocking.** A report is deliverable ONLY after
   `check_brand.py` PASSES, `visual_verify.py` PASSES, and you have Read
   every rendered page PNG. Exit code 1 = stop and fix, not "note and continue".

**Escalation protocol (fail closed):** if any rule cannot be satisfied —
logo/font/CSS file missing, artwork unavailable, a value or fact you cannot
verify, a script erroring — **STOP and ASK THE USER** for the missing input
or decision. State exactly what is missing and why you won't improvise it.
A paused report is always better than an off-brand or invented one.
The scripts enforce this posture: `new_report.py` refuses to scaffold without
the canonical assets, and `check_brand.py` fails on tampered ones.

## Workflow

Replace `<skill>` with this skill's directory. Run steps in order.

**Step 0 — Sensitive-data inventory (before any content).**
Read `references/personal-info-policy.md`; inventory every name, email,
customer identifier, IP, count, or date the report needs. Missing-critical →
ask the user now. Missing-substitutable → `<PLACEHOLDER>` convention.

**Step 1 — Scaffold.**
```bash
python <skill>/scripts/new_report.py --out ./report-workspace \
  --title "..." --subtitle "..." --author "..." --date "Month Year" \
  --lang es --variant orange   # orange (default) | slate | paper
```
The cover is PLAIN ORANGE by default (logo + white text only). Optional:
`--cover-art builtin` (bundled isometric pattern strip) or
`--cover-art file.svg|png` (approved imagery supplied by the user);
`--purpose "..."` (fills the disclaimer's objective); `--no-disclaimer`
ONLY if the user explicitly asks; `--classification ""`; `--force`.
The script copies `styles/` + `assets/` and fills the cover. If it refuses
(missing assets), relay its message to the user — do not work around it.

**Step 2 — Write the content sections.**
Components: `references/component-catalog.md`. Diagrams:
`references/diagrams-guide.md`. Structure rules below. While drafting,
verify every technical claim against CURRENT official documentation and add
per-section `.ref-list` source blocks with visible URLs —
protocol in `references/fact-verification.md`. Diagrams depict only
verified statements.

**Step 3 — Brand gate (blocking).**
```bash
python <skill>/scripts/check_brand.py ./report-workspace/report.html
```
Fix every FAIL and re-run until it passes. Address or consciously accept WARNs.

**Step 4 — Render.**
```bash
python <skill>/scripts/render_report.py ./report-workspace/report.html
```
Prints page count, writes the PDF and `_render/page-NN.png` for every page.

**Step 5 — Programmatic visual pre-flight (blocking).**
```bash
python <skill>/scripts/visual_verify.py ./report-workspace/report.html
```
Four deterministic checks (SVG text overflow, DOM overflow, image load,
z-index) — details in `references/visual-verification.md`.

**Step 6 — Page-by-page visual review (blocking, no sampling).**
Read EVERY `_render/page-NN.png` and check it against the Visual Review
Checklist below. Fix → re-render → re-review until clean. Do not sample
"representative" pages: in an 11-section document, sampling 5 ships the
defects in the other 6.

**Step 7 — Deliver BOTH formats (+ standalone HTML).**
Save final `.html` (with its `styles/` + `assets/`) AND `.pdf` side by side
and present both. HTML = editable/intranet copy; PDF = the customer
deliverable. ALSO run:
```bash
python <skill>/scripts/export_standalone.py ./report-workspace/report.html
```
and deliver `report-standalone.html` — a single self-contained file (CSS,
fonts, logos, copy.js inlined, ~5 MB) that renders correctly when
double-clicked from ANY folder (macOS blocks sibling-file reads in protected
folders like Downloads, which strips the styling from the folder version).
Never run `check_brand.py` on the standalone (it is a generated artifact;
inline styles/base64 are correct THERE and violations in the working file).

**Optional third output — editable Word (.docx).** When the customer requires
an editable copy, derive it from the SAME content (never re-author):
`pandoc report.html -o Report.docx`. Render inline-SVG diagrams to PNG first
for Word fidelity and size them explicitly. The HTML/PDF remain canonical —
the .docx is a derivative convenience.

**Step 8 — Cleanup.**
Keep only defect-evidence PNGs (move to `_findings/` with a one-line README
each); delete the rest of `_render/`. Deliverable folder = HTML + PDF +
assets/styles + optional `_findings/`.

## Visual Review Checklist (step 6)

| # | Check | Likely fix |
|---|-------|-----------|
| 1 | Cover: full-bleed plain orange (or chosen variant), white logo top-left, light-weight title, bold subtitle, byline + date, disclaimer line, no running header. Art strip appears ONLY when the user requested one | `.cover { page: cover-page }` intact; if a strip was requested, its `<img>` loads (`check_brand` + `visual_verify` catch most) |
| 2 | Cover text never collides with the art strip when one is used, at any wrap length | Title lives in `.cover-content` (max-width enforced); shorten title if it exceeds 3 lines |
| 3 | Running header on every content page: 3px orange top border + dark logo + SECTION LABEL | `position: running(running-header)` + `@top-left { content: element(running-header) }` |
| 4 | Overflow pages show the SAME section label as their parent section | One `.section-header` per section, nothing between sections |
| 5 | Logo crisp, correct variant, undistorted (never a circle mark, never stretched) | Official PNGs at natural aspect; height-only sizing |
| 6 | Section `h2` shows the orange pixel tick and is never orphaned at a page bottom | `break-after: avoid` is in the CSS; move content if needed |
| 7 | Code blocks, tables, callouts, diagrams, ref-lists never split across pages | `break-inside: avoid` (already in CSS); long code → `.code-multipart` |
| 8 | Long code splits BETWEEN logical sub-blocks, never within; no lone `# --- Section ---` comment at a page bottom | `.code-multipart` pattern — `references/css-print-architecture.md` |
| 9 | No empty/half-empty pages where the next section could flow | doc-overrides: `.section:nth-child(N) { break-before: auto; }` |
| 10 | Diagram labels/arrows don't overlap boxes; arrowheads end exactly at rect edges | `references/diagrams-guide.md` (SVG arrows, text fitting) |
| 11 | ES/PT text fits — no overflow in diagram boxes or subtitles (Spanish runs ~15% longer); SVG `<text>` does NOT wrap — pre-wrap long labels into multiple rows or use `<foreignObject>` | Widen boxes, shorten labels, or wrap rows |
| 12 | Page number bottom-right and title footer bottom-left on content pages; neither on cover/TOC | `@page` margin boxes; doc-overrides sets the footer text |
| 13 | TOC (if present): every entry resolves a real page number — no `•`, `0`, or blank | `target-counter` notes in `references/component-catalog.md` |
| 14 | Every `.ref-list` shows readable full URLs (paper-friendly), one per fact-bearing section | `references/fact-verification.md` §4 |
| 15 | Colors match tokens: #FF5500 orange accents, #313638 slate text/headers, white pages | Only token drift can cause this — restore canonical CSS |
| 16 | No invented content: names, versions, ports, flows in diagrams all trace to user input or cited docs | `references/fact-verification.md` §1–§2 |
| 17 | Disclaimer present: short line on the cover + "About this document" end-matter block (unless the user explicitly opted out) | Scaffold sets both; `--no-disclaimer` only on explicit user request |
| 18 | PDF pages show NO Copy buttons on code blocks (they are HTML-view-only) | `.copy-btn { display:none }` in print — if visible, report.css was tampered |

## Document structure rules

- Cover → (optional TOC) → sections. Each `<div class="section">` = one
  top-level division with exactly ONE `.section-header` (feeds the running
  header; keep labels 1–3 words).
- Phases (`.phase-banner`) live INSIDE their parent section — never as
  separate sections. The running header shows the section, not the phase.
- Sections default to `break-before: page`; let short ones flow via
  doc-overrides `nth-child` rule.
- Components are unlimited and mix freely; the print CSS is structural.
- Language: match the user's audience (es/en/pt). No creative-writing
  analogies in customer-facing copy; no AI-speech patterns
  (`leverage`, `utilize`, `in order to`, `delve`, `seamless`) — plain language.

## Brand quick facts

Full tokens in `references/branding-tokens.md` (read before any styling
decision). Anchors [official Brand Hub]: **Illumio Orange `#FF5500`** (PMS Orange 21C),
**Server Slate `#313638`** (PMS 447C), white pages, Zero Trust Tan `#F7F4EE`
panels, System Cyan `#1A2C32` code blocks, Safeguard Green / Risk Red for
diagram semantics. Montserrat (300 light titles / 700 bold emphasis) — the
Brand Hub's sanctioned typeface for self-publishing templates (FK Grotesk is
licensed, never bundle/embed it). Isometric grid / rhombus / container motif. Logos:
`assets/logo-white.png` on orange/slate/dark, `assets/logo-dark.png` on light.

## Adapting to another brand

1. Copy the skill folder; edit `:root` tokens in `styles/report.css` and add
   `FORKED-CSS` inside its top comment (downgrades the hash check to a warning).
2. Replace both logo PNGs with the target brand's official files (same
   filenames) — ask the user for them; never approximate.
3. Regenerate or replace `assets/cover-art.svg`
   (`scripts/gen_cover_art.py`, or `--cover-art`).
4. Swap font files in `assets/fonts/` + the `@font-face` block if the brand
   uses different typography.

## Reference map

| File | When |
|---|---|
| `references/personal-info-policy.md` | Step 0 — always |
| `references/fact-verification.md` | Step 2 — always (claims, diagrams, citations) |
| `references/component-catalog.md` | Step 2 — adding content |
| `references/diagrams-guide.md` | Step 2 — any diagram |
| `references/branding-tokens.md` | Any styling decision; brand adaptation |
| `references/css-print-architecture.md` | Page-break tuning, doc-overrides |
| `references/visual-verification.md` | Step 5 — interpreting findings |
| `scripts/new_report.py` / `check_brand.py` / `render_report.py` / `visual_verify.py` | Steps 1 / 3 / 4 / 5 |
| `scripts/export_standalone.py` | Step 7 — single-file HTML for sharing |
| `evals/evals.json` | Regression cases from real past failures |

## Final gate — restate before delivery

Confirm ALL of these, explicitly, before presenting files:

- [ ] Scaffolded via `new_report.py`; edits only between SECTION markers + doc-overrides
- [ ] `check_brand.py` PASSED on the exact HTML being delivered
- [ ] `visual_verify.py` PASSED
- [ ] Every rendered page PNG was Read and checked — no sampling
- [ ] Official logos untouched; fonts bundled; no external URLs in `<head>`
- [ ] No invented names/facts; `<TO-VERIFY>` markers all resolved; fact-bearing
      sections carry `.ref-list` official-doc links with visible URLs
- [ ] Disclaimer on cover + end matter (or the user explicitly opted out)
- [ ] HTML view has working Copy buttons on code blocks; PDF has none
- [ ] Both HTML and PDF delivered, plus `report-standalone.html`; `_render/` cleaned per step 8

If any box cannot be ticked: it is not deliverable. Fix it or ask the user.
