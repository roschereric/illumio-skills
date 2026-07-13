# CSS Print Architecture for WeasyPrint

## Overview

The print system uses two CSS layers:
1. **Screen CSS** — the default styles (visible in browser)
2. **Print CSS** (`@media print`) — overrides for PDF generation via WeasyPrint

WeasyPrint supports CSS Paged Media Level 3 features that browsers don't:
`position: running()`, `content: element()`, named `@page` rules, and margin boxes.

## Page Setup

### Named Pages

The default `@page` defines running header (top), page number (bottom-right), and document-title footer (bottom-left). Two named pages override the default for special cases: cover (no header, no numbers) and TOC (header yes, numbers no).

```css
@page {
  size: A4 portrait;              /* 210mm x 297mm */
  margin: 60px 0 50px 0;          /* +20px on bottom to house the footer */

  @top-left {
    content: element(running-header);
    width: 100%;
  }

  @bottom-right {
    content: counter(page);
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    font-weight: 500;
    color: #999999;
    padding: 0 50px 18px 0;
  }

  @bottom-left {
    content: "";  /* real title injected per-document by new_report.py into <style id="doc-overrides"> */
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    color: #BBBBBB;
    padding: 0 0 18px 50px;
  }
}

/* Cover: full bleed, no header, no page number, no footer */
@page cover-page {
  margin: 0;
  @top-left { content: none; }
  @bottom-right { content: none; }
  @bottom-left { content: none; }
}

/* TOC: keeps the running header, suppresses page number and footer.
   TOC is "page 2", before content numbering begins visually. */
@page toc-page {
  @bottom-right { content: none; }
  @bottom-left { content: none; }
}
```

**Per-document tweaks live in `<style id="doc-overrides">` in the HTML** —
short-section flow overrides and the @bottom-left footer text. Never edit
`styles/report.css` per document (it is hash-checked by `check_brand.py`).

The page counter starts at 1 with the cover. So in practice:
- Cover = page 1 (counter exists, just not rendered)
- TOC = page 2 (counter exists, just not rendered)
- Section 1 = page 3 (first visible page number: `3`)

If you prefer numbering to start at `1` on the first content section, add `counter-reset: page 0` to `.section:first-of-type` — but be aware this breaks coherence with the TOC's `target-counter` resolution, which always reports absolute page positions.

### Why 60px Top Margin and 50px Bottom?

The running header contains:
- 3px orange top border
- 12px padding-top
- 22px logo height (flex-aligned with section label text)
- 8px padding-bottom
- 1px bottom border

Total = ~47px. The 60px top margin gives 13px breathing room so content doesn't touch the header.

The 50px bottom margin houses the page number + footer text with ~18px padding from the page edge, plus breathing room above so body text doesn't touch the footer.

## Running Headers — The Key Mechanism

### How It Works

```css
/* In @media print: */
.section-header {
  position: running(running-header);
  /* ... styling ... */
}
```

1. `position: running(name)` removes the element from the document flow
2. It places the element into a "running element slot" identified by `name`
3. `content: element(name)` in a `@page` margin box renders that element
4. Each time a new `.section-header` is encountered, it **replaces** the previous one in the slot
5. On overflow pages (where no new section starts), the **last assigned** header persists

This means: if "Deployment Procedure" spans 3 pages, all 3 pages show "DEPLOYMENT PROCEDURE" in the header. No manual duplication needed.

### Running Header Styling (in print)

```css
.section-header {
  position: running(running-header);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 50px 8px 50px;
  border-top: 3px solid var(--ill-orange);
  border-bottom: 1px solid var(--ill-line);
  background: var(--ill-paper);
  margin: 0;
}
```

The header contains:
- Left: `<img>` with the dark Illumio logo (22px height)
- Right: `<span class="section-label">` with the section name (uppercase, gray-400)

## Page Break Strategy

### Section-Level Breaks

```css
.section {
  break-before: page;           /* Default: each section starts on a new page */
  padding: 20px 50px 30px 50px; /* Top padding reduced since header is in margin */
}
.section:first-child {
  break-before: auto;           /* First section flows after cover */
}
.section:nth-child(3) {
  break-before: auto;           /* Example: short section flows after previous */
}
```

Adjust `:nth-child()` overrides based on content length. Short sections (under half a page)
should flow into the previous section's page to avoid wasted whitespace.

### Element-Level Break Control

```css
/* Never break inside these */
.step, .callout, .diagram-container, table, .checklist li {
  break-inside: avoid;
}

/* Keep headings with their following content */
h2, h3, h4 { break-after: avoid; }

/* Keep phase banners with their first step */
.phase-banner {
  break-after: avoid;
  break-inside: avoid;
  padding-top: 10px;
}

/* The element directly after a phase-banner must not start a new page */
.phase-banner + .step,
.phase-banner + pre,
.phase-banner + .code-multipart,
.phase-banner + p { break-before: avoid; }

/* Orphan/widow control for text */
p, li { orphans: 3; widows: 3; }
```

### Code Block Atomicity (UPDATED — supersedes earlier "allow splitting" guidance)

Earlier versions of this skill let large `<pre>` blocks split freely (`break-inside: auto` with `orphans/widows: 4`). That produced a worse failure mode: WeasyPrint counts orphans/widows by *physical lines*, not logical sections, so a comment like `# --- Section ---` could end up alone at the bottom of a page with its code on the next. The split happened, but at the wrong place.

The current rule: **`<pre>` is atomic** (never splits within itself), and **long code that needs to span pages is split into multiple atomic `<pre>` elements wrapped in a `.code-multipart` container** that *can* be broken between (but not within) sub-blocks.

```css
/* <pre> is atomic — never splits */
pre {
  break-inside: avoid;
  font-size: 10px;
  padding: 12px 16px;
  orphans: 4;
  widows: 4;
}

/* Multi-part code: container can break between children; each child is atomic */
.code-multipart { break-inside: auto; margin: 14px 0; }
.code-multipart > pre {
  break-inside: avoid;
  margin: 0;
  border-radius: 0;
}
.code-multipart > pre:first-child { border-radius: 8px 8px 0 0; }
.code-multipart > pre:last-child  { border-radius: 0 0 8px 8px; }
.code-multipart > pre:not(:last-child) {
  border-bottom: 1px dashed #444;
  padding-bottom: 10px;
}
.code-multipart > pre:not(:first-child) { padding-top: 10px; }
```

#### How to use `.code-multipart`

When a code block exceeds about half a page, divide it into thematic sub-blocks. Each sub-`<pre>` represents a **logical section** of the file (e.g., for a config file: ACLs, Rules, Logs). The label inside the sub-`<pre>` names the file *and* the section: `/etc/squid/squid.conf · ACLs`.

```html
<div class="code-multipart">
  <pre><span class="label">/etc/squid/squid.conf · header and port</span>
http_port 3128
# ...
</pre>
  <pre><span class="label">/etc/squid/squid.conf · ACLs</span>
acl workloads_net src 10.10.0.0/16
# ...
</pre>
  <pre><span class="label">/etc/squid/squid.conf · access rules</span>
http_access deny !Safe_ports
# ...
</pre>
</div>
```

#### Rules for sub-block division

- Each sub-`<pre>` is one logical section.
- The first comment in a sub-block (`# --- Section ---`) sits at the TOP of the `<pre>` — that guarantees it's never orphaned.
- Accept a small empty area at the bottom of a page before an atomic sub-block — that's better than splitting mid-section.

#### Why this works

`break-inside: avoid` on each sub-`<pre>` means the page-break engine can ONLY cut between fully-rendered sub-blocks, never inside one. The container with `break-inside: auto` exposes those inter-block boundaries as valid break points. The visual treatment (rounded corners only on first/last, dashed borders between) preserves the single-file reading experience.

## Cover Page

```css
.cover {
  page: cover-page;        /* Uses the named page with margin: 0 */
  width: 210mm;
  height: 297mm;           /* Explicit A4 dimensions */
  page-break-after: always;
  padding: 80px 50px 60px 50px;
  position: relative;
  overflow: hidden;
}
```

The cover uses `page: cover-page` which maps to `@page cover-page { margin: 0; }`.
This gives full-bleed rendering without the running header. Layout inside the
cover is handled by `.cover-content` (flex column, z-index 2) and the
`.cover-art` strip (right, 56mm, z-index 1) — see `styles/report.css`; the
scaffolded markup already has the correct structure.

## Content Wrapper

```css
.content-wrap {
  max-width: 100%;  /* Full width in print (860px max in screen) */
  padding: 0;
  background: var(--ill-mist);
}
.content-wrap::before { display: none; }  /* Hide the orange top bar (causes blank page) */
```

## Print-Specific Spacing

WeasyPrint gives 0 extra padding at automatic page breaks. Add breathing room
to elements that might land at the top of a page:

```css
.step { padding-top: 14px; margin-top: 0; }
.callout { margin-top: 16px; }
.checklist li { padding-top: 10px; }
h3 { padding-top: 18px; }
.phase-banner { padding-top: 10px; }
table { margin-top: 16px; }
.diagram-container { margin-top: 16px; }
```

## Troubleshooting

### Header missing on some pages
- Verify `position: running(running-header)` is in the `@media print` block
- Verify `@page { @top-left { content: element(running-header); } }` exists
- Check that `margin-top` on `@page` is large enough (60px minimum)

### Cover shows a running header
- Ensure `.cover { page: cover-page; }` is set
- Ensure `@page cover-page { @top-left { content: none; } }` overrides the default

### Blank pages appearing
- Remove `content-wrap::before` in print (the orange bar forces a blank page)
- Check that no element has both `break-before: page` AND `break-after: always`

### Elements splitting awkwardly
- Add `break-inside: avoid` to the element
- For long code blocks, use the `.code-multipart` pattern (see Code Block Atomicity) — never let a single `<pre>` split

### Font not rendering
- Fonts are BUNDLED in `assets/fonts/` and declared via `@font-face` in
  `styles/report.css` — no network is used. If type falls back, the `assets/`
  folder wasn't copied next to the HTML (re-run `new_report.py`) or the
  `../assets/fonts/` relative path was broken by moving files. `check_brand.py`
  catches both.
