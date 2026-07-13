# illumio-branded-reports

Print-ready A4 PDF + HTML reports in Illumio's **Orange & Slate** identity
(2026 corporate-template look): clean full-bleed orange cover (optional
isometric/imagery strip), Montserrat typography (bundled), running page
headers, architecture diagrams, callouts, phase-based guides, per-section
official-doc citations, a localized not-an-official-document disclaimer, and
Copy buttons on code blocks in the HTML view (never in the PDF).

Built for pre-sales collateral: deployment guides, runbooks, technical briefs,
POC documents — EN/ES/PT.

## Design: script-driven and fail-closed

Earlier versions asked the model to "copy the template and keep the styling" —
under long sessions models drift: they re-type the skeleton, regenerate logos,
lose the CSS link. v2 removes that failure mode structurally:

| Guarantee | Mechanism |
|---|---|
| Skeleton is never hand-written | `scripts/new_report.py` scaffolds every report; refuses to run if canonical assets are missing (ask the user, never improvise) |
| CSS can't drift | `styles/report.css` is canonical; `scripts/check_brand.py` hash-verifies it (per-doc tweaks go in a size-capped `doc-overrides` block) |
| Logos can't be faked | Both PNGs hash-checked against the official assets; CSS-filter recoloring and text wordmarks are lint failures |
| Typography can't silently fall back | Montserrat + JetBrains Mono TTFs bundled in `assets/fonts/`; external font/CSS URLs are lint failures |
| Facts can't ship unverified | `references/fact-verification.md` protocol + `.ref-list` citation component; lint warns on fact-heavy sections without sources |
| Rendering defects can't ship | `scripts/render_report.py` (PDF + per-page PNGs) → `scripts/visual_verify.py` (Playwright checks) → mandatory page-by-page review |

## Quickstart

```bash
python scripts/new_report.py --out ./my-report \
  --title "Guía de Despliegue VEN" --subtitle "Plan por fases" \
  --author "Nombre – Illumio SE" --date "Julio 2026" --lang es
# … edit my-report/report.html between the SECTION markers …
python scripts/check_brand.py   my-report/report.html   # blocking gate
python scripts/render_report.py my-report/report.html   # PDF + PNGs
python scripts/visual_verify.py my-report/report.html   # blocking gate
python scripts/export_standalone.py my-report/report.html # single-file HTML for sharing
```

## Repository structure

```
illumio-branded-reports/
├── SKILL.md                    ← workflow + hard rules (start here)
├── template.html               ← canonical skeleton (placeholders, markers)
├── styles/report.css           ← canonical CSS (hash-checked; FORKED-CSS marker for other brands)
├── assets/
│   ├── logo-white.png          ← official logo, dark/orange backgrounds
│   ├── logo-dark.png           ← official logo, light backgrounds
│   ├── cover-art.svg           ← optional isometric cover strip (--cover-art builtin)
│   ├── copy.js                 ← canonical Copy-button script (HTML view only)
│   └── fonts/                  ← Montserrat + JetBrains Mono TTFs (offline-safe)
├── scripts/
│   ├── new_report.py           ← fail-closed scaffolder
│   ├── check_brand.py          ← brand-integrity lint (blocking)
│   ├── render_report.py        ← WeasyPrint render + page PNGs
│   ├── export_standalone.py    ← self-contained single-file HTML export
│   ├── visual_verify.py        ← Playwright pre-flight (blocking)
│   └── gen_cover_art.py        ← regenerate the default cover strip
├── references/                 ← deep dives (brand tokens, print CSS, components,
│   │                              diagrams, PII policy, fact verification, visual checks)
├── evals/                      ← regression cases from real failures
└── commands/                   ← /skill-update, /skill-status, /skill-publish
```

## Brand anchors

Orange `#FF5500` · Slate `#313638` (the official "Orange and Slate" logo
palette) · white pages · mist `#F7F4EE` panels · Montserrat (Light 300 titles,
Bold 700 emphasis) · isometric pattern motif (official Pattern & Shape system). Full tokens:
`references/branding-tokens.md`.

## Changelog

### v2.1.0 — 2026-07-13
- Cover simplified: plain full-bleed Illumio Orange by default; decorative/imagery strip is now opt-in (`--cover-art builtin|<file>`)
- Localized disclaimer (EN/ES/PT) ON by default — cover line + "About this document" end matter stating the report is a working guide, not an official Illumio, Inc. publication; tune with `--purpose` / `--disclaimer-text`, omit only via explicit `--no-disclaimer` (lint warns)
- Copy buttons on code blocks in the HTML view via canonical `assets/copy.js` (hash-checked; hidden in print; lint rejects any other `<script>`)
- New `scripts/export_standalone.py` — single-file HTML with CSS/fonts/logos/JS inlined; survives double-click from macOS-protected folders (e.g. Downloads) and email forwarding
- Brand tokens verified against the official Illumio Brand Hub (Frontify): Server Slate tint scale, System Cyan, Zero Trust Tan, Cloud Cerulean, Circuit Gold, Safeguard Green / Risk Red diagram semantics; Montserrat confirmed as the sanctioned self-publishing typeface (FK Grotesk licensure documented — never bundled/embedded); official logo rules encoded (4:1 ratio, clear space, four variants)
- Default cover-art generator rebuilt on the official isometric Pattern & Shape primitives (rhombus grid, containers, accent lines)

### v2.0.0 — 2026-07-12
- Script-driven, fail-closed pipeline: `new_report.py` (refuses to scaffold without canonical assets — ask the user, never improvise), `check_brand.py` (blocking lint: CSS/logo/font hash checks, forbidden patterns, placeholder detection), `render_report.py` (PDF + per-page PNGs in one command)
- Montserrat + JetBrains Mono bundled in `assets/fonts/` — zero network at render time (kills the silent font-fallback failure)
- 2026 cover design in official Orange & Slate (#FF5500 / #313638); retired the legacy gradient/parallelogram cover and the #E8611A palette
- Anti-hallucination layer: `references/fact-verification.md` protocol (claims inventory → verify against current official docs → cite/`<TO-VERIFY>`/cut; diagrams are claims too) + `.ref-list` component printing full source URLs per section
- SKILL.md restructured for model reliability: six hard rules up front, blocking exit-code gates, stop-and-ask escalation protocol, final pre-delivery checklist

### v1.0.0
- Initial release: WeasyPrint CSS Paged Media system (running headers, page breaks, code-multipart), component catalog, PII policy, Playwright visual pre-flight, regression evals

## Updating / publishing

- `/skill-update` — pull latest from GitHub (also auto-runs on session start)
- `/skill-status` — local vs origin drift report
- `/skill-publish` — commit + push / open a PR with your changes

## Requirements

Python 3.9+, `weasyprint`, `poppler-utils` (or `pdf2image`), `playwright`
(+ chromium) for the visual pre-flight. The scripts print exact install
commands when something is missing.
