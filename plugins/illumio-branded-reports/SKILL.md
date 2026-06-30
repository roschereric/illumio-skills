---
name: illumio-branded-reports
description: >
  Generate professional branded PDF and HTML reports using Illumio's visual identity
  (or adaptable to other brands). Produces print-ready A4 documents with running page
  headers, architecture diagrams, code blocks, callouts, and phase-based deployment guides.
  Uses WeasyPrint for HTML-to-PDF conversion with CSS Paged Media features.
  MANDATORY: Use this skill whenever the user asks to create a report, guide, runbook,
  deployment document, technical brief, or any professional document for Illumio customers.
  Also trigger when the user mentions "branded PDF", "print-ready document",
  "customer-facing guide", "deployment guide", "technical document with diagrams",
  or asks to format content in Illumio style.
---

# Illumio Branded Report Generator

Create professional, print-ready PDF and HTML documents using Illumio's brand identity.
The system produces A4 documents with consistent running headers, architecture diagrams,
syntax-highlighted code blocks, callout boxes, and structured deployment phases.

## Workflow

0. **Personal information & sensitive data check (MANDATORY — read FIRST).** Read `references/personal-info-policy.md` and apply its §2 protocol *before generating any content*. Inventory every value the report will need (names, emails, contact details, customer/partner identifiers, IPs, hostnames, license counts, etc.). For any value classified as Missing-critical, STOP and ask the user. Default to the placeholder convention in §3 of that policy for Missing-substitutable fields. Never invent personal or organizational identifiers — these reports go to customers, partners, and Illumio leadership.
1. Read `references/branding-tokens.md` for color palette and typography
2. Copy `template.html` **together with the `assets/` and `styles/` directories** from this skill's directory as the starting point. The template is intentionally small (~8 KB of markup + a single `<link>` tag) — the heavy styling lives in `styles/report.css` and the logos in `assets/*.png` so the template stays token-light when Claude reads it.
3. Read `references/css-print-architecture.md` for the print CSS system (or open `styles/report.css` directly if you need to tweak tokens or print rules)
4. Read `references/component-catalog.md` for available UI components
5. Customize the template content for the specific document. Keep the `<link rel="stylesheet" href="styles/report.css">` intact unless you intentionally want to fork the CSS.
6. Generate PDF using WeasyPrint (Python) — ensure both `assets/` AND `styles/` are present next to the HTML (or pass `base_url` pointing at a directory that contains them)
7. **Programmatic pre-flight (MANDATORY).** Before the human visual review, run the four deterministic checks documented in `references/visual-verification.md` — SVG text overflow, DOM horizontal overflow, image load, and z-index sanity. The bundled `scripts/visual_verify.py` runs them in one pass against the rendered HTML. Fix anything it flags before continuing. These checks catch a class of bugs that the human visual checklist below cannot reliably spot (especially silent SVG text overflow).
8. **Visual review loop (MANDATORY — every section, no sampling).** Render every page of the PDF to PNG and inspect each one before delivery. Compare against the Visual Review Checklist below. **Do NOT sample "a couple of representative sections"** — walk every section, every page, every diagram. Customer-, partner-, and executive-facing collateral does not tolerate sampling. If any item fails — logo distortion, text overflow, diagram label collision, split element, half-empty page — fix the HTML/CSS and re-render. Loop until all checks pass. Do NOT deliver a PDF that has not been visually inspected page-by-page.
9. **Deliver BOTH the HTML and the PDF.** Always save the final `.html` AND the final `.pdf` side-by-side in the user's output folder and present both. The HTML lets the user hand the file to a web designer, re-edit, or host on an intranet; the PDF is the print-ready deliverable. Never ship only one format.
10. **Cleanup — retain only error evidence.** After all checks pass, archive the rendered evidence: keep ONLY the PNGs that documented an actual defect (move them to a `_findings/` folder with a short `README.md` cross-referencing each capture to the bug and fix). Delete intermediate `_render/` PNGs from successive iterations. The deliverable folder should contain the final HTML + PDF + (optionally) `_findings/` evidence, not 30+ intermediate captures.

### Visual Review Checklist

After rendering, inspect every page against these checks. Fix and re-render if any item fails.

| # | Check | Likely fix |
|---|-------|-----------|
| 1 | Cover is full-bleed, no running header, gradient + geometric shapes visible | Confirm `.cover { page: cover-page; }` and `@page cover-page { margin: 0 }` |
| 2 | Running header on every content page: orange top border + logo + SECTION LABEL | Confirm `position: running(running-header)` and `@page { @top-left { content: element(running-header); } }` |
| 3 | Logo orange mark is a **perfect circle**, not a vertical ellipse | Use an embedded PNG from `assets/` or an inline `<svg><circle></svg>`. Do NOT use a CSS `::before` pseudo-element with `border-radius: 50%` inside an `inline-flex` container — WeasyPrint stretches it into an ellipse |
| 4 | Section subtitles (uppercase tracking text) fit on one line | Reduce `letter-spacing` to ~1.2px and `font-size` to ~11.5px; keep subtitles short |
| 5 | Diagram labels and arrows do not overlap the boxes on either side | Widen the SVG `viewBox`, shrink label text, or reposition |
| 6 | Code blocks, tables, callouts, and diagrams stay on a single page | Apply `break-inside: avoid` |
| 7 | No empty or half-empty pages where the next section could have flowed in | Override with `.section:nth-child(N) { break-before: auto; }` for short sections |
| 8 | Headings are not orphaned at the bottom of a page | Apply `break-after: avoid` to `h2, h3, h4` |
| 9 | In non-English versions, no Spanish/Portuguese text overflows boxes in diagrams | Widen SVG boxes or shorten translated labels (Spanish runs ~15% longer than English). **SVG sub-rule:** SVG `<text>` does NOT auto-wrap. For ES/PT sentences over ~80 characters inside an SVG, pre-wrap into multiple `<text>` rows (with `text-anchor="middle"` and incremented `y`) OR render inside a `<foreignObject>` HTML block which DOES wrap. |
| 10 | Page numbers appear in bottom-right of every content page (NOT on cover, NOT on TOC) | Verify `@page { @bottom-right { content: counter(page); } }` is set and `@page cover-page` + `@page toc-page` override with `content: none`. See `references/css-print-architecture.md` Page Setup. |
| 11 | Footer text (document title) appears in bottom-left of every content page | Verify `@page { @bottom-left { content: "..." } }` is set with the actual document title. |
| 12 | If the document has a TOC: every TOC entry shows a real page number (not the screen-fallback `•`, `0`, or a blank) | Verify `target-counter(attr(href), page)` resolves. Common causes of failure: `::after` applied to a `<span>` inside the `<a>` instead of the `<a>` itself; href doesn't match any `id` on a section; running in browser preview (TOC numbers only resolve in WeasyPrint, not Chrome). See `references/component-catalog.md` Table of Contents. |
| 13 | Code blocks: long blocks split BETWEEN logical sub-sections, never WITHIN one. A comment like `# --- Section ---` never sits alone at the bottom of a page with its code on the next | Use the `.code-multipart` pattern: wrap multi-section code in `<div class="code-multipart">` with each sub-section in its own atomic `<pre>`. Each `<pre>` has `break-inside: avoid`; the container has `break-inside: auto`. See `references/css-print-architecture.md` Code Block Atomicity. |
| 14 | SVG arrows: arrowhead polygon terminates EXACTLY at the destination rect's edge — never inside, never outside | Set `line.x2 = X_destino - 10`, `polygon points = "X_destino-10,Y-4 X_destino,Y X_destino-10,Y+4"`. See `references/diagrams-guide.md` SVG Arrows. |
| 15 | SVG text labels (especially between rects or on arrows) fit in the available horizontal space — no text mounted on a sibling rect | Calculate `(X_destino - X_origen_borde_der)` before placing the label. If text doesn't fit: shorten/abbreviate, split with `<tspan>`, reposition off the critical axis, or delete the label if it's redundant. See `references/diagrams-guide.md` SVG Text Fitting. |
| 16 | **Brand asset integrity** — every logo reference resolves to the OFFICIAL asset (`assets/logo-dark.png` or `assets/logo-white.png` or an SVG variant generated by fill-substitution from the official file). No inline SVG approximations, no `<span>` text wordmarks in alternate fonts, no CSS-shape pseudo-logos | If a document needs the logo on a dark background, generate the white variant with `sed` from the official SVG (see `references/branding-tokens.md` Logo Handling). Never use CSS `filter` to recolor SVG logos in WeasyPrint — filters don't propagate into embedded SVG. |

### Visual review — implementation pattern

```python
# After doc.write_pdf('report.pdf'):
from pdf2image import convert_from_path
imgs = convert_from_path('report.pdf', dpi=110)
for i, img in enumerate(imgs, 1):
    img.save(f'page_{i}.png')
# Then, via the Read tool, read each page_*.png and compare
# against the checklist. Iterate on HTML/CSS until all checks pass.
```

`pdf2image` requires `poppler-utils`. On Debian/Ubuntu: `apt-get install poppler-utils`. On macOS: `brew install poppler`.

### Output delivery — both formats, always

```bash
cp report.html "$OUTPUT_DIR/Document_Name.html"
cp report.pdf  "$OUTPUT_DIR/Document_Name.pdf"
```

Then present BOTH files to the user (via `present_files` in Cowork, or direct links if Claude Code). The HTML enables further editing, intranet hosting, and re-use; the PDF is what goes to the customer.

## Branding Overview

Illumio's visual identity uses three anchor colors with a warm, professional tone:

| Token              | Value     | Usage                                    |
|--------------------|-----------|------------------------------------------|
| `--ill-orange`     | `#E8611A` | Primary accent, buttons, badges, borders |
| `--ill-cream`      | `#F5F0EA` | Page background, section fills           |
| `--ill-charcoal`   | `#2D2D2D` | Body text, table headers, phase banners  |

Typography: **Inter** (Google Fonts) at weights 300-900. Code: JetBrains Mono / Fira Code / Consolas.

Logos are stored as PNG files in `assets/`:
- `assets/logo-white.png` — used on the cover (dark backgrounds)
- `assets/logo-dark.png` — used in section running headers (light backgrounds)

The template references them via relative `src="assets/..."` paths. When generating
a document, ensure the `assets/` directory is copied alongside the HTML file so
WeasyPrint can resolve the image paths.

## Repository Structure

The skill is deliberately split into three kinds of files so that the HTML template stays lightweight and cheap to read into context:

```
illumio-branded-reports/
├── template.html           ← ~8 KB — markup only, links to CSS + images
├── styles/
│   └── report.css          ← all screen + print CSS lives here
├── assets/
│   ├── logo-white.png      ← cover (dark backgrounds)
│   └── logo-dark.png       ← section running headers (light backgrounds)
├── references/             ← deep-dive docs (read only when needed)
├── SKILL.md
└── README.md
```

**Why the split?** When Claude reads `template.html` it sees structure, not 100 KB of base64 logos or 11 KB of inline CSS. That keeps token usage low across every session that touches this skill. Read `styles/report.css` only when you need to tweak tokens (colors, fonts, page margins) or print rules — otherwise leave it alone and it never enters context.

### Rendering pattern

WeasyPrint resolves `styles/report.css` and `assets/logo-*.png` relative to the HTML's base URL. When the working document sits inside the skill folder (or `assets/` and `styles/` are copied alongside it), this just works:

```python
from weasyprint import HTML
HTML(filename='document.html').render().write_pdf('Document.pdf')
```

When rendering from a different location, either (a) copy `assets/` and `styles/` next to `document.html`, or (b) pass `base_url` pointing at the skill root:

```python
HTML(filename='/path/to/document.html',
     base_url='/path/to/illumio-branded-reports/').write_pdf('Document.pdf')
```

## Document Architecture

Every document follows this structure:

```
Cover Page          → Full-bleed dark gradient, geometric shapes, white logo
  ↓
Section 1           → Running header (logo + label), content
  ↓
Section 2           → New page (or flows from previous)
  ↓
...                 → Sections continue, overflow pages keep the running header
  ↓
Final Section       → Closing callout, footer with copyright
```

### Sections and Page Breaks

Each `<div class="section">` represents a logical document section. In print:
- Default: each section forces a new page via `break-before: page`
- Override short sections to flow after the previous one: `.section:nth-child(N) { break-before: auto; }`
- The first section always flows after the cover (`:first-child`)

### Cover Stacking Rules (Critical — Read This)

The cover places decorative absolutely-positioned shapes (`.geo-1`, `.geo-2`, `.geo-3`, dot matrices) on the same canvas as the title, subtitle, and logo. Without an explicit stacking context, source order determines paint order — meaning a long title can render *behind* a decorative shape, with the trailing glyphs clipped or completely hidden. This is silent: the title is in the DOM, but the reader sees only part of it.

**The rule:** wrap all foreground cover content in a `.cover-content` container with its own stacking context, and constrain its `max-width` so it cannot intrude into the decoration zone even when the title wraps.

```css
.cover {
  position: relative;
  isolation: isolate;          /* creates a stacking context */
  overflow: hidden;
}
.cover-content {
  position: relative;
  z-index: 2;                  /* always above decorative shapes */
  max-width: 560px;            /* keeps title out of the geo zone */
}
.cover .geo-1,
.cover .geo-2,
.cover .geo-3 { position: absolute; z-index: 1; }
```

```html
<div class="cover">
  <div class="geo-1"></div>
  <div class="geo-2"></div>
  <div class="geo-3"></div>
  <div class="cover-content">
    <img class="cover-logo" src="assets/logo-white.png" alt="Illumio">
    <span class="cover-tag">SECTION / POC LABEL</span>
    <h1>Document Title (Spanish titles may run wider)</h1>
    <p class="subtitle">…</p>
  </div>
</div>
```

**Why `max-width` matters even when `z-index` is correct:** a long Spanish title (e.g., `Reacción ante Nuevas Amenazas`) running ~38px font-weight 800 will *wrap* into the decoration zone if its container is full-width. The reader then sees the second line behind a parallelogram. `max-width: 560px` forces it to wrap earlier and stay inside the safe zone. Adjust the value if your cover layout differs.

The programmatic pre-flight (`scripts/visual_verify.py`, check 4) flags any `<h1>`/`<h2>` whose bounding rect intersects a `.geo-*` element with insufficient z-index.

### Running Headers (Critical — Read This)

The running header system uses WeasyPrint's CSS Paged Media support:

```css
/* Each section-header is removed from flow and placed in the page margin */
.section-header { position: running(running-header); }

/* The @page rule picks it up */
@page {
  margin: 60px 0 30px 0;
  @top-left {
    content: element(running-header);
    width: 100%;
  }
}

/* Cover page overrides: no margin, no header */
@page cover-page {
  margin: 0;
  @top-left { content: none; }
}
.cover { page: cover-page; }
```

This ensures **every page** — including overflow pages — gets the correct header
with the Illumio logo and the current section label. The header auto-updates
each time a new section begins.

### Section Hierarchy Rules

- A "section" is a top-level document division (Overview, Prerequisites, Procedure, etc.)
- Phases (Phase 1, Phase 2...) live **inside** sections, never as separate sections
- If content like "Validate the Deployment" is Phase 4 of Deployment Procedure,
  it stays inside the Deployment Procedure section — do NOT create a separate section for it
- The running header always shows the parent section name, not the phase name

## PDF Generation

### WeasyPrint (Required)

```bash
pip install weasyprint --break-system-packages
```

```python
from weasyprint import HTML

src = 'document.html'
dst = 'Document.pdf'

# Render and inspect page count
doc = HTML(filename=src).render()
print(f"Pages: {len(doc.pages)}")

# Write PDF
doc.write_pdf(dst)
```

### Verification Checklist

After generating a PDF, verify:

1. Cover page has no header, full-bleed gradient, geometric shapes visible
2. Every content page has the running header (orange top border + logo + section label)
3. Overflow pages show the SAME section label as the section they belong to
4. Phase banners never appear at the bottom of a page without content following
5. Code blocks have dark background with syntax highlighting preserved
6. Tables don't split across pages (small tables) or split cleanly (large tables)
7. Callout boxes don't split across pages
8. No orphaned headings (heading at bottom of page with content on next page)

## Adapting for Other Brands

The template is designed around Illumio but is parameterizable:

1. In `styles/report.css`, replace the CSS custom properties in `:root` with the target brand's colors
2. Replace the logo files in `assets/` (`logo-white.png` and `logo-dark.png`) with the target brand's logos (keep the same filenames so `template.html` still resolves)
3. In `styles/report.css`, adjust the cover gradient in `.cover { background: linear-gradient(...) }`
4. Adjust geometric shapes (`.geo-1`, `.geo-2`, `.geo-3`) in `styles/report.css` or remove them
5. Update the footer copyright text in `template.html`

The structural CSS (running headers, page breaks, components) in `styles/report.css` stays unchanged — that's why the template markup and the stylesheet live in separate files.

## Document Structure is Flexible

The template shows one example of each component type. The actual document you
produce should have as many (or few) sections, diagrams, phases, tables, and code
blocks as the content requires. The print CSS is structural — it works regardless
of how many components are used.

- Sections: 2 to 10+ (each gets a running header automatically)
- Diagrams: 0 to many (each wrapped in `.diagram-container`)
- Phases: 0 to many (all inside their parent section)
- Code blocks, callouts, tables, steps: unlimited, mix freely

For page break tuning on short sections, override with `.section:nth-child(N) { break-before: auto; }`
in the `@media print` block so short sections flow after the previous one instead of wasting a page.

## Reference Files

Read these for implementation details:

| File | When to Read | Content |
|------|-------------|---------|
| `references/personal-info-policy.md` | **MANDATORY — Step 0 of every run** | Categories of information not to hallucinate; protocol for asking the user before generating any content; placeholder convention. **Live policy — update as new categories surface.** |
| `references/branding-tokens.md` | Always | Full color palette, typography, spacing |
| `references/visual-verification.md` | **Step 7 — programmatic pre-flight** | Deep-dive on the four deterministic checks (SVG text overflow, DOM horizontal overflow, image load, z-index sanity), install/run instructions, defect-category catalog |
| `references/css-print-architecture.md` | When modifying print CSS | Page margins, running headers, break rules |
| `references/component-catalog.md` | When adding content | Callouts, code blocks, tables, steps, inline SVGs |
| `references/diagrams-guide.md` | When creating diagrams | Excalidraw workflow, hand-coded SVG, Mermaid fallback |
| `template.html` | Always — this is your starting point | Markup-only HTML (links to `styles/report.css` and `assets/*`) |
| `styles/report.css` | When tweaking colors, fonts, page margins, or print rules | All screen + print CSS, extracted from the template so the HTML stays small |
| `scripts/visual_verify.py` | Step 7 — run before visual review | Bundled Playwright-based pre-flight checker. Runs the four deterministic checks from `references/visual-verification.md` in one pass. |
| `assets/logo-white.png` | Copied with template | White logo for cover page and dark backgrounds |
| `assets/logo-dark.png` | Copied with template | Dark logo for section running headers |
| `evals/evals.json` | When testing or regression-checking | Real-world inputs that broke earlier versions of this skill — each case has input fixture, expected programmatic detection, and expected fix |

## Common Pitfalls

- **Do NOT recreate, substitute, or "approximate" brand assets.** The Illumio wordmark and isotype are brand assets with a specific type design and composition. NEVER replace the logo with `<span>illumio</span>` in another font (Inter, Helvetica, etc.). NEVER draw the isotype with `<div>` rectangles or inline SVG shapes you invented. NEVER use a "simplified" version of the logo. The ONLY permitted modification of an official asset is changing fill colors while keeping paths, viewBox, and composition identical — see `references/branding-tokens.md` Logo Handling for the SVG variant pattern. If the official asset isn't accessible (sandbox without network, blocked CDN), STOP and ask the user for the file. A paused render is infinitely better than a PDF with an apocryphal logo.
- **Do NOT use CSS `filter` to recolor SVG logos in WeasyPrint.** `filter: brightness(0) invert(1)` works in browsers but WeasyPrint does NOT propagate filters into `<img src="*.svg">` content — the PDF will render the SVG's native fills. The correct pattern is generating a fill-modified variant of the SVG file (see `references/branding-tokens.md` Logo Handling). Always verify the rendered PDF, not just the browser preview.
- **Do NOT skip Step 0 (personal info policy).** Reports go to customers, partners, and Illumio leadership. Hallucinated names, emails, IPs, or deal sizes embarrass everyone involved. If the report needs a value and the user didn't supply it, ASK — or use a `<PLACEHOLDER>`. Never invent.
- **Do NOT sample "a couple of representative sections" during visual review.** Walk every section, every page, every diagram. In an 11-section document, sampling 5 will miss defects concentrated in the 6 you skipped. Sampling is the meta-bug that lets every other visual bug ship.
- **Do NOT use creative-writing analogies in customer-facing copy** (musical instruments, sports metaphors, food comparisons, animal references). Customer-facing collateral and executive review require direct, technical comparisons. *"The Sentinel playbook needs Azure + Logic Apps; the portable script applies when those are absent"* — yes. *"The playbook is a symphony orchestra, the script is an acoustic guitar"* — no.
- **Do NOT put cover decorative elements in the same stacking context as the title** without an explicit z-index pattern. See Cover Stacking Rules. A long title silently rendered behind a parallelogram is invisible in markup review and obvious only when rendered.
- **Do NOT use Chrome print for PDF** — it ignores `position: running()`. WeasyPrint is required.
- **Do NOT create separate sections for sub-phases** — phases belong inside their parent section.
- **Do NOT embed images as base64 in the HTML** — use external files in `assets/` and reference via `src="assets/..."`. This keeps the template lightweight and avoids burning AI context tokens. For diagrams, use inline SVG.
- **Do NOT paste the full CSS back into `<style>` inside `template.html`** — the stylesheet lives in `styles/report.css` precisely so the HTML stays under ~8 KB. Leave the `<link rel="stylesheet" href="styles/report.css">` in place.
- **Do NOT forget to copy `assets/` AND `styles/` alongside the HTML** — WeasyPrint needs both at their relative paths. When writing the final HTML to the output directory, copy both folders there too (or pass `base_url` to WeasyPrint pointing at a directory that has them).
- **Do NOT set `@page { margin: 0 }` globally** — the running header needs `margin-top: 60px`.
- **Do NOT use `leverages`, `utilize`, `in order to`** — these are AI speech patterns. Use plain language.
- **Do NOT hardcode API versions or tenant-specific values** — use `<PLACEHOLDER>` format.

<!-- BEGIN illumio-skill-update:addendum -->
## Update addendum (managed — do not hand-edit between the markers)

### Step 0 — MANDATORY resource pre-flight (run FIRST, every time)

Before generating anything, run:

    python scripts/preflight_check.py

It verifies `template.html`, `styles/report.css`, `assets/logo-white.png`,
`assets/logo-dark.png`, and `scripts/visual_verify.py` exist and are usable. If it exits
non-zero you are on a STALE/PARTIAL skill copy — STOP, run
`/illumio-branded-reports:skill-update`, then re-run the check. NEVER substitute a text
wordmark, an invented mark, or system fonts to work around missing assets. The generator
should import and call this check so a partial skill ABORTS the build instead of degrading.

### Editable Word (.docx) — optional third output

Generate Word from the SAME content (do not re-author) with pandoc so it never diverges
from the PDF/HTML:

    pandoc content.md -o Document.docx --toc --toc-depth=1 --resource-path <dir-with-PNGs>

Render inline-SVG diagrams to PNG for Word and size with `![caption](d.png){width=6.4in}`.
Pitfall: with pandoc `implicit_figures`, an image-only paragraph already gets a caption from
its alt text — do NOT add a second caption line or it duplicates.
<!-- END illumio-skill-update:addendum -->
