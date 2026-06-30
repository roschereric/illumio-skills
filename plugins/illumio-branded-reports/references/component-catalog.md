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
    <img src="DATA_URI_DARK_LOGO" alt="Illumio">
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
  <svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
    <!-- Boxes -->
    <rect x="10" y="60" width="180" height="100" rx="8" fill="#F5F0EA" stroke="#2D2D2D" stroke-width="2"/>
    <text x="100" y="90" text-anchor="middle" font-weight="700" font-size="13" fill="#2D2D2D">Box Title</text>
    <text x="100" y="110" text-anchor="middle" font-size="11" fill="#555">Subtitle</text>

    <!-- Arrows (dashed) -->
    <line x1="190" y1="110" x2="350" y2="110" stroke="#2D2D2D" stroke-width="1.5" stroke-dasharray="6,4"/>
    <polygon points="348,106 358,110 348,114" fill="#2D2D2D"/>

    <!-- Accent boxes (orange border) -->
    <rect x="400" y="40" width="200" height="130" rx="8" fill="none" stroke="#E8611A" stroke-width="2" stroke-dasharray="6,3"/>
    <text x="500" y="70" text-anchor="middle" font-weight="700" font-size="13" fill="#2D2D2D">Accent Box</text>

    <!-- Flow labels (orange background) -->
    <rect x="220" y="95" width="120" height="24" rx="4" fill="#E8611A"/>
    <text x="280" y="112" text-anchor="middle" font-size="10" fill="white" font-weight="600">1 Step Label</text>
  </svg>
</div>
```

### SVG Color Palette
| Usage            | Fill/Stroke | Value     |
|------------------|-------------|-----------|
| Box fill         | fill        | `#F5F0EA` |
| Box border       | stroke      | `#2D2D2D` |
| Accent border    | stroke      | `#E8611A` |
| Arrow lines      | stroke      | `#2D2D2D` |
| Flow labels      | fill (bg)   | `#E8611A` |
| Title text       | fill        | `#2D2D2D` |
| Subtitle text    | fill        | `#555`    |
| Accent text      | fill        | `#E8611A` |
| White on orange  | fill        | `white`   |

### Diagram Tips
- Use `rx="8"` on all rectangles for rounded corners
- Use `stroke-dasharray="6,3"` for dashed borders (emphasis/future items)
- Keep SVG `viewBox` proportional to A4 width (~700px wide works well)
- Always wrap in `<div class="diagram-container">` for consistent padding and `break-inside: avoid`

---

## Cover Page

The cover is a full-bleed section with a dark gradient, geometric shapes, and the white logo.

```html
<div class="cover">
  <div class="geo-1"></div><div class="geo-2"></div><div class="geo-3"></div>
  <div class="dots"></div><div class="dots-2"></div>
  <div class="cover-logo">
    <img src="DATA_URI_WHITE_LOGO" alt="Illumio" class="cover-logo-img" style="height:40px;">
  </div>
  <h1>Document Title Here</h1>
  <p class="subtitle">One-sentence description of the document purpose and audience.</p>
  <div class="cover-meta">
    <div class="cover-meta-item">Version<strong>1.0</strong></div>
    <div class="cover-meta-item">Date<strong>Month Year</strong></div>
  </div>
  <div class="cover-footer">
    <span>&copy; 2026 Illumio, Inc. All Rights Reserved.</span>
    <span>CONFIDENTIAL</span>
  </div>
</div>
```

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
.toc { padding: 36px 60px; background: var(--ill-cream); }
.toc h2 { margin-bottom: 20px; }
.toc-list { list-style: none; padding: 0; margin: 0; counter-reset: toc-num; }
.toc-list li {
  counter-increment: toc-num;
  margin: 0;
  padding: 0;
  border-bottom: 1px dashed var(--ill-cream-dark);
}
.toc-list li a {
  display: flex;
  align-items: baseline;
  text-decoration: none;
  color: var(--ill-charcoal);
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
  color: var(--ill-cream-dark);
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

Closing section with CTA and copyright.

```html
<div style="margin-top:28px;padding:20px;background:var(--ill-charcoal);border-radius:10px;text-align:center;position:relative;overflow:hidden;">
  <div style="position:absolute;top:-10px;right:30px;width:50px;height:100px;background:var(--ill-orange);transform:skewX(-8deg);opacity:0.12;"></div>
  <p style="color:rgba(255,255,255,0.6);font-size:12px;margin-bottom:4px;">Questions? Contact your Illumio pre-sales engineer</p>
  <p style="color:#fff;font-weight:700;font-size:14px;">We're here to support every phase of your deployment.</p>
</div>
<div class="content-footer">
  <span>&copy; 2026 Illumio, Inc. All Rights Reserved.</span>
</div>
```

<!-- BEGIN illumio-skill-update:docref-disclaimer -->
## Inline documentation reference (`docref`)

One per section, linking the exact official source pages (validate every URL first).

```html
<div class="docref"><strong>Official documentation:</strong>
  <a href="URL">Title</a> &middot; <a href="URL">Title</a></div>
```

```css
.docref{font-size:11.5px;color:#555;background:#FBF8F4;border-left:3px solid #E8611A;
  padding:8px 13px;border-radius:0 6px 6px 0;margin:14px 0;break-inside:avoid;}
.docref strong{color:#2D2D2D;}
```

## Disclaimer (non-official, customer-facing collateral)

```html
<div class="disclaimer"><div class="callout-label">Notice — unofficial document</div>
  Support guide, not official Illumio documentation; does not replace it.</div>
```

```css
.disclaimer{border:1.5px solid #E8611A;background:#FDF1E8;border-radius:8px;
  padding:14px 18px;margin:6px 0 18px;line-height:1.6;break-inside:avoid;}
```

Cover fields to support: `disclaimer_short` (one line on the cover) and `tag`
(e.g. "INTERNAL / CUSTOMER"). Keep the wording sober; one notice on the cover plus one
after the TOC is enough.
<!-- END illumio-skill-update:docref-disclaimer -->
