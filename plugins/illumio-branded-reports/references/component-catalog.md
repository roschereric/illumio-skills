# Component Catalog

All reusable UI components for Illumio branded reports.
Copy these HTML snippets into your document sections.

## Table of Contents
1. [Section with Header](#section-with-header)
2. [Callout Boxes](#callout-boxes)
3. [Code Blocks](#code-blocks)
4. [Phase Banners](#phase-banners)
5. [Numbered Steps](#numbered-steps)
6. [Data Tables](#data-tables)
7. [Checklists](#checklists)
8. [Architecture Diagrams (SVG)](#architecture-diagrams)
9. [Cover Page](#cover-page)
10. [Footer](#footer)

---

## Section with Header

Every content section follows this pattern. The `.section-header` feeds the running header in print.

```html
<div class="section">
  <div class="section-header">
    <img src="assets/logo-dark.png" alt="Illumio">
    <span class="section-label">Section Name Here</span>
  </div>
  <h2>Section Title</h2>
  <p>Section content goes here.</p>
</div>
```

Rules:
- One `section-header` per section (exactly one — it feeds the running header)
- The `section-label` text appears in the page header on every page of this section
- Keep labels short (1-3 words): "OVERVIEW", "PREREQUISITES", "DEPLOYMENT PROCEDURE"

---

## Callout Boxes

Four semantic variants. Use sparingly — one or two per page maximum.

### Warning (Orange) — Constraints, Timelines, Important Notes
```html
<div class="callout callout-warning">
  <div class="callout-label">Callout Title</div>
  Content text here. Supports <strong>bold</strong> and <code>inline code</code>.
</div>
```

### Info (Blue) — Background Information, FYI
```html
<div class="callout callout-info">
  <div class="callout-label">Information Title</div>
  Content text here.
</div>
```

### Success (Green) — Tips, Best Practices, Confirmations
```html
<div class="callout callout-success">
  <div class="callout-label">Tip or Best Practice</div>
  Content text here.
</div>
```

### Critical (Red) — Blockers, Destructive Actions, Hard Requirements
```html
<div class="callout callout-critical">
  <div class="callout-label">Critical Warning</div>
  Content text here. Use only for genuine blockers or risks.
</div>
```

---

## Code Blocks

Dark-themed code blocks with syntax highlighting via CSS classes.

```html
<pre><span class="label">FILENAME OR CONTEXT</span>
<span class="comment"># Comment text</span>
<span class="cmdlet">Command-Name</span> <span class="param">-Parameter</span> <span class="string">"value"</span>
<span class="variable">$variable</span> = something
</pre>
```

### Syntax Highlight Classes
| Class       | Color     | Usage                          |
|-------------|-----------|--------------------------------|
| `.comment`  | `#6A9955` | Comments (green)               |
| `.string`   | `#CE9178` | String literals (salmon)       |
| `.param`    | `#9CDCFE` | Parameters/flags (light blue)  |
| `.cmdlet`   | `#DCDCAA` | Commands/functions (yellow)    |
| `.variable` | `#C586C0` | Variables (purple)             |
| `.label`    | `#666`    | Top-right label (small, gray)  |

### Copy button (HTML view)

`assets/copy.js` (canonical, loaded from the template head) injects a Copy
button into the top-right of every `<pre>` in the HTML deliverable and shifts
the `.label` left to make room. It is hidden in print (`@media print`), so the
PDF never shows it. Do NOT hand-write buttons inside code blocks and do NOT
inline extra `<script>` tags — `check_brand.py` fails anything but the
canonical include.

### Inline Code
```html
<code>inline-code-here</code>
```
Renders with cream-dark background, charcoal text, small monospace font.

---

## Phase Banners

Mark major deployment phases. Always followed by steps or content.

```html
<div class="phase-banner">
  <span class="phase-num">PHASE 1</span>
  <span class="phase-title">Phase Title Here</span>
</div>
```

Rules:
- Phase banners belong INSIDE their parent section (never as separate sections)
- Use `break-after: avoid` to keep the banner with its first content element
- Add a `<div class="phase-spacer"></div>` between phases if needed for screen layout
  (hidden in print: `display: none`)

---

## Numbered Steps

Step-by-step instructions with orange number badges and white cards.

```html
<div class="step">
  <div class="step-number">1</div>
  <div class="step-content">
    <h4>Step Title</h4>
    <p>Step description. Use <code>inline code</code> for paths and commands.</p>
  </div>
</div>
```

Rules:
- Steps have `break-inside: avoid` — they won't split across pages
- Keep step content concise (2-3 lines). For longer content, use a callout after the step.
- Number sequentially within each phase (restart numbering per phase)

---

## Data Tables

Tables with dark charcoal headers and alternating row colors.

```html
<table>
  <tr>
    <th>Column 1</th>
    <th>Column 2</th>
    <th>Column 3</th>
  </tr>
  <tr>
    <td>Data</td>
    <td>Data</td>
    <td>Data</td>
  </tr>
  <tr>
    <td>Data</td>
    <td>Data</td>
    <td>Data</td>
  </tr>
</table>
```

For checklist-style tables with checkboxes:
```html
<table>
  <tr><th style="width:25px">#</th><th>Task</th><th>Owner</th><th style="width:45px">Done</th></tr>
  <tr><td>1</td><td>Task description</td><td>Role</td><td style="text-align:center">&#9744;</td></tr>
</table>
```

Use `&#9744;` (☐) for empty checkbox, `&#9745;` (☑) for checked.

---

## Checklists

CSS-only checkboxes (no JavaScript needed) with orange borders.

```html
<ul class="checklist">
  <li><strong>Item title</strong> — Description of the checklist item.</li>
  <li><strong>Another item</strong> — Another description.</li>
</ul>
```

The checkbox square is rendered via CSS `::before` pseudo-element with an orange border.

---

## Architecture Diagrams

Inline SVGs styled with the brand palette. No external images needed.

### Basic Pattern
```html
<div class="diagram-container">
  <div class="diagram-title">Diagram Title Here</div>
  <svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat, sans-serif">
    <!-- Boxes -->
    <rect x="10" y="60" width="180" height="100" rx="8" fill="#F7F4EE" stroke="#313638" stroke-width="2"/>
    <text x="100" y="90" text-anchor="middle" font-weight="700" font-size="13" fill="#313638">Box Title</text>
    <text x="100" y="110" text-anchor="middle" font-size="11" fill="#6F7274">Subtitle</text>

    <!-- Arrows (dashed) -->
    <line x1="190" y1="110" x2="350" y2="110" stroke="#313638" stroke-width="1.5" stroke-dasharray="6,4"/>
    <polygon points="348,106 358,110 348,114" fill="#313638"/>

    <!-- Accent boxes (orange border) -->
    <rect x="400" y="40" width="200" height="130" rx="8" fill="none" stroke="#FF5500" stroke-width="2" stroke-dasharray="6,3"/>
    <text x="500" y="70" text-anchor="middle" font-weight="700" font-size="13" fill="#313638">Accent Box</text>

    <!-- Flow labels (orange background) -->
    <rect x="220" y="95" width="120" height="24" rx="4" fill="#FF5500"/>
    <text x="280" y="112" text-anchor="middle" font-size="10" fill="white" font-weight="600">1 Step Label</text>
  </svg>
</div>
```

### SVG Color Palette
| Usage            | Fill/Stroke | Value     |
|------------------|-------------|-----------|
| Box fill         | fill        | `#F7F4EE` |
| Box border       | stroke      | `#313638` |
| Accent border    | stroke      | `#FF5500` |
| Arrow lines      | stroke      | `#313638` |
| Flow labels      | fill (bg)   | `#FF5500` |
| Title text       | fill        | `#313638` |
| Subtitle text    | fill        | `#555`    |
| Accent text      | fill        | `#FF5500` |
| White on orange  | fill        | `white`   |

### Diagram Tips
- Use `rx="8"` on all rectangles for rounded corners
- Use `stroke-dasharray="6,3"` for dashed borders (emphasis/future items)
- Keep SVG `viewBox` proportional to A4 width (~700px wide works well)
- Always wrap in `<div class="diagram-container">` for consistent padding and `break-inside: avoid`

---

## Cover Page

Full-bleed Illumio Orange with the isometric pattern strip. ALWAYS produced by
`scripts/new_report.py` — never hand-typed. Shown here only so you can
recognize the parts; do not deviate from this structure.

```html
<div class="cover">                      <!-- or cover cover--slate / cover--paper -->
  <!-- cover-art div appears here ONLY when the user requested a strip
       (new_report.py --cover-art builtin|file). Default: plain orange. -->
  <div class="cover-content">
    <div class="cover-logo">
      <img src="assets/logo-white.png" alt="Illumio">   <!-- logo-dark.png on paper variant -->
    </div>
    <div class="cover-spacer"></div>
    <h1>Document Title Here</h1>
    <p class="subtitle">One-sentence bold description of purpose and audience.</p>
    <p class="cover-byline">Author – Illumio Role</p>
    <p class="cover-date">Month Year</p>
    <p class="cover-disclaimer">Working guide prepared by the author — not an official Illumio, Inc. publication.</p>
    <div class="cover-bottom-spacer"></div>
  </div>
  <div class="cover-footer">
    <span>&copy; 2026 Illumio, Inc. All Rights Reserved.</span>
    <span>CONFIDENTIAL</span>
  </div>
</div>
```

Rules:
- Default cover is PLAIN ORANGE — no decorative strip unless the user asks
  (`--cover-art builtin` or an approved-imagery file); the logo is never optional
- Title: Montserrat Light 300 — long Spanish titles wrap to a maximum of 3 lines
- Subtitle: Bold 700, the "why it matters" sentence
- Byline/date: exactly the values the user supplied (never invent an author)
- The disclaimer line is inserted by the scaffolder (localized EN/ES/PT)

---

## Table of Contents

A TOC sits between the cover and the first section. WeasyPrint resolves the
page numbers automatically via CSS `target-counter()` — no JavaScript, no
manual numbering.

### HTML

Each `<a>` points at an `id` on the corresponding `.section`. The `::after`
pseudo-element on the `<a>` will be replaced with the resolved page number
at print time.

```html
<div class="toc">
  <div class="section-header">
    <div class="logo-mini">
      <img src="assets/logo-dark.png" alt="Illumio" style="height:22px;">
    </div>
    <span class="section-label">ÍNDICE</span>
  </div>
  <h2>Tabla de Contenidos</h2>
  <ul class="toc-list">
    <li><a href="#sec-resumen"><span class="toc-title">Resumen Ejecutivo</span><span class="toc-dots">··················</span></a></li>
    <li><a href="#sec-arquitectura"><span class="toc-title">Arquitectura</span><span class="toc-dots">··················</span></a></li>
    <!-- one <li> per section; href matches the section's id -->
  </ul>
</div>
```

Each section consumes the matching id:

```html
<div class="section" id="sec-resumen">...</div>
<div class="section" id="sec-arquitectura">...</div>
```

### CSS

```css
.toc { padding: 36px 60px; background: var(--ill-mist); }
.toc h2 { margin-bottom: 20px; }
.toc-list { list-style: none; padding: 0; margin: 0; counter-reset: toc-num; }
.toc-list li {
  counter-increment: toc-num;
  margin: 0;
  padding: 0;
  border-bottom: 1px dashed var(--ill-line);
}
.toc-list li a {
  display: flex;
  align-items: baseline;
  text-decoration: none;
  color: var(--ill-slate);
  padding: 11px 0;
  font-size: 13.5px;
  font-weight: 500;
}
.toc-list li a::before {
  content: counter(toc-num, decimal-leading-zero);
  color: var(--ill-orange);
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  margin-right: 14px;
  flex-shrink: 0;
}
.toc-list li a .toc-title { flex: 1; }
.toc-list li a .toc-dots {
  flex: 0 1 auto;
  color: var(--ill-line);
  margin: 0 8px;
  overflow: hidden;
  white-space: nowrap;
  letter-spacing: 2px;
}
.toc-list li a::after {
  /* On-screen fallback; replaced by target-counter in print */
  content: "•";
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--ill-gray-600);
  font-weight: 600;
  flex-shrink: 0;
  min-width: 28px;
  text-align: right;
}

@media print {
  .toc { page: toc-page; break-after: page; }
  /* WeasyPrint resolves the target page number automatically */
  .toc-list li a::after {
    content: target-counter(attr(href), page);
  }
}
```

### Why this works — and the failure modes

- **`attr(href)` must be read from the element that HAS the attribute.** That's why `::after` lives on the `<a>`, not on a `<span>` child. If you apply `::after` to a span inside the `<a>`, it renders empty — `target-counter()` returns nothing because `attr(href)` doesn't exist on a span.
- **WeasyPrint resolves `target-counter()` during pagination**, after the first layout pass. The TOC ends up with real numbers without any JS.
- **In browser preview, you see the fallback `•`.** That's deliberate: there's no print pagination in screen mode, so we render a discreet placeholder. Page numbers appear only in the PDF. **Always verify the PDF, not the browser preview.**

### Common bugs

| Symptom | Cause | Fix |
|---|---|---|
| TOC shows `•` everywhere in the PDF | `::after` is on a `<span>` inside the `<a>`, not on the `<a>` itself | Move `::after` to the `<a>` selector. |
| TOC shows `0` for every entry | Section `id` doesn't match the `<a href>`. `target-counter` returns 0 when target is missing | Verify each href matches a real section id. |
| TOC entries empty (no number visible) | Browser preview — page numbers only resolve in WeasyPrint | Render to PDF; check there. |
| Page numbers shifted (e.g. all off by 1) | TOC takes a page but `@page toc-page` not applied | Verify `.toc { page: toc-page; break-after: page; }` is in `@media print`. |

---

## Footer

Closing CTA with pixel accent + copyright line.

```html
<div class="cta-box">
  <svg class="px-accent" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
    <rect x="0"  y="0"  width="10" height="10" fill="#FF5500"/>
    <rect x="12" y="12" width="10" height="10" fill="#FF5500" opacity="0.7"/>
    <rect x="24" y="0"  width="10" height="10" fill="#FF5500" opacity="0.45"/>
    <rect x="24" y="24" width="10" height="10" fill="#FFFFFF" opacity="0.35"/>
  </svg>
  <p class="cta-sub">Questions? Contact your Illumio pre-sales engineer</p>
  <p class="cta-main">We're here to support every phase of your deployment.</p>
</div>
<div class="content-footer">
  <span>&copy; 2026 Illumio, Inc. All Rights Reserved.</span>
</div>
```

---

## Sources / Official-Doc Citations

> Legacy note: older documents used a `.docref` inline box for documentation
> links. The class remains in report.css so old files still render, but NEW
> documents must use `.ref-list` below (numbered, per-section, paper-readable).

End every fact-bearing section with a `.ref-list`. URLs must be readable on
paper (include the domain/path in the visible text). Inline markers use
`<sup class="ref">`. Full protocol: `references/fact-verification.md`.

```html
<p>El servicio del VEN es <code>venAgentMgrSvc</code><sup class="ref">1</sup>.</p>

<div class="ref-list">
  <div class="ref-title">Sources — official documentation</div>
  <ol>
    <li><a href="https://product-docs-repo.illumio.com/Tech-Docs/Core/25.x/...">
        Illumio Core 25.x — VEN Administration —
        product-docs-repo.illumio.com/Tech-Docs/Core/25.x/…</a></li>
  </ol>
</div>
```

---

## Disclaimer (auto-inserted)

`new_report.py` inserts a localized (EN/ES/PT) two-part disclaimer by default:
a one-line `.cover-disclaimer` under the cover date, and an
`.disclaimer` "About this document" block before the content footer stating
the document is a working guide prepared by the author, not an official
Illumio, Inc. publication, and that technical details must be validated
against official documentation. Customize the objective with `--purpose`,
override wording with `--disclaimer-text`, omit ONLY on explicit user request
(`--no-disclaimer`). Do not reword it ad-hoc inside the HTML — regenerate.

```html
<div class="disclaimer">
  <div class="disclaimer-title">Acerca de este documento</div>
  <p>Esta guía fue preparada por … no constituye una publicación oficial de Illumio, Inc. …</p>
</div>
```
