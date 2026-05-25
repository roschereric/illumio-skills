# Diagrams Guide

This document covers three approaches to creating architecture diagrams and visual
explainers for branded reports. Choose based on complexity and available tools.

## Table of Contents
1. [Approach Selection](#approach-selection)
2. [Excalidraw Diagrams](#excalidraw-diagrams)
3. [Hand-Coded SVG Diagrams](#hand-coded-svg-diagrams)
4. [Mermaid Diagrams (Fallback)](#mermaid-diagrams)
5. [Embedding in the Report](#embedding-in-the-report)
6. [Brand Palette for Diagrams](#brand-palette-for-diagrams)

---

## Approach Selection

| Approach     | Best For                                | Tools Required         | Brand Control |
|--------------|----------------------------------------|------------------------|---------------|
| Excalidraw   | Complex architecture, flow diagrams    | excalidraw.com or CLI  | High (manual) |
| Hand SVG     | Simple 2-5 box flows, inline in HTML   | None (code only)       | Perfect       |
| Mermaid      | Quick sequence/flow diagrams           | Mermaid CLI or online  | Low           |

**Default recommendation:** Use Excalidraw for anything with more than 5 boxes or
crossing arrows. Use hand-coded SVG for simple linear flows (A → B → C).

---

## Excalidraw Diagrams

Excalidraw (https://excalidraw.com) produces hand-drawn style diagrams that can be
exported as SVG. The SVGs embed cleanly in the HTML report.

### Workflow

1. **Create the diagram** in Excalidraw (web app or desktop)
   - Use the brand color palette below for fills and strokes
   - Use Inter font (select "Normal" in Excalidraw — it uses a hand-drawn font by default)
   - For a cleaner look: set stroke style to "Architect" or "Artist" mode

2. **Export as SVG**
   - File → Export image → SVG
   - Check "Embed scene" if you want to re-edit later
   - Check "Background" to include the white/transparent background

3. **Clean up the SVG for embedding**
   ```bash
   # Option A: Use Excalidraw CLI (if available in Claude Code)
   npx @excalidraw/excalidraw-cli export input.excalidraw --type svg --output diagram.svg

   # Option B: Manual — open the .svg file and:
   # 1. Remove the XML declaration (<?xml ...?>)
   # 2. Remove width/height attributes from the root <svg>, keep only viewBox
   # 3. Optionally replace Excalidraw's default colors with brand colors
   ```

4. **Embed in the HTML report**
   ```html
   <div class="diagram-container">
     <div class="diagram-title">Architecture Overview</div>
     <!-- Paste the SVG directly here -->
     <svg viewBox="..." xmlns="http://www.w3.org/2000/svg">
       ...
     </svg>
   </div>
   ```

### Excalidraw Brand Color Mapping

When drawing in Excalidraw, use these hex values:

| Excalidraw Element | Color to Use | Hex       | Illumio Token      |
|--------------------|--------------|-----------|--------------------|
| Box fill           | Light cream  | `#F5F0EA` | `--ill-cream`      |
| Box stroke         | Dark gray    | `#2D2D2D` | `--ill-charcoal`   |
| Accent box stroke  | Orange       | `#E8611A` | `--ill-orange`     |
| Arrow lines        | Dark gray    | `#2D2D2D` | `--ill-charcoal`   |
| Label backgrounds  | Orange       | `#E8611A` | `--ill-orange`     |
| Label text on orange | White      | `#FFFFFF` | —                  |
| Title text         | Dark gray    | `#2D2D2D` | `--ill-charcoal`   |
| Subtitle text      | Medium gray  | `#555555` | `--ill-gray-600`   |
| Status/accent text | Orange       | `#E8611A` | `--ill-orange`     |
| Dashed borders     | Orange       | `#E8611A` | (for TBD/pending)  |

### Excalidraw Tips for Print

- Set canvas background to transparent (not white) — the report has a cream background
- Keep diagrams under 700px logical width for good A4 fit
- Avoid very thin strokes (< 1.5px) — they may not print well
- Text should be at least 11px for readability in print
- Excalidraw's hand-drawn style works well at screen sizes but can look rough when
  printed small — test at A4 scale before finalizing

### Saving Excalidraw Files

Save the `.excalidraw` source file alongside the report for future editing:
```
project/
├── report.html
├── diagrams/
│   ├── architecture.excalidraw    ← source (editable)
│   └── architecture.svg           ← export (embedded in HTML)
└── Report.pdf
```

---

## Hand-Coded SVG Diagrams

For simple flows (2-5 boxes with arrows), coding the SVG directly is faster and
gives perfect brand alignment. See `component-catalog.md` for the full pattern.

### Quick Reference

```svg
<svg viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">
  <!-- Solid box -->
  <rect x="10" y="40" width="160" height="80" rx="8"
        fill="#F5F0EA" stroke="#2D2D2D" stroke-width="2"/>
  <text x="90" y="75" text-anchor="middle"
        font-weight="700" font-size="13" fill="#2D2D2D">Title</text>

  <!-- Dashed accent box (for pending/external components) -->
  <rect x="400" y="30" width="200" height="100" rx="8"
        fill="none" stroke="#E8611A" stroke-width="2" stroke-dasharray="6,3"/>

  <!-- Arrow with label -->
  <line x1="170" y1="80" x2="390" y2="80"
        stroke="#2D2D2D" stroke-width="1.5" stroke-dasharray="6,4"/>
  <polygon points="388,76 398,80 388,84" fill="#2D2D2D"/>
  <rect x="230" y="68" width="100" height="24" rx="4" fill="#E8611A"/>
  <text x="280" y="85" text-anchor="middle"
        font-size="10" fill="white" font-weight="600">1 Action</text>
</svg>
```

### When to Use Hand-Coded SVG vs Excalidraw

- **Hand SVG**: Linear flows (A → B → C), simple request/response diagrams, 
  component relationship diagrams with < 6 elements
- **Excalidraw**: Network topologies, complex architectures with crossing connections,
  anything requiring spatial layout decisions, diagrams the customer might want to edit

---

## Mermaid Diagrams

Mermaid is useful for quick sequence diagrams or flowcharts but offers limited
brand control. Use as a fallback when Excalidraw is unavailable.

### Workflow

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Create diagram definition
cat > diagram.mmd << 'EOF'
graph LR
    A[Domain Controller] -->|GPO delivers script| B[Windows Server]
    B -->|Downloads VEN| C[Illumio PCE]
    C -->|Policy sync| B
EOF

# Render as SVG
mmdc -i diagram.mmd -o diagram.svg -t neutral --backgroundColor transparent

# Then embed the SVG in the report (same as Excalidraw export)
```

### Mermaid Limitations
- Limited color control (theme-level only, not per-element)
- Hand-drawn look not available
- Complex layouts can produce cluttered output
- Always review the output — Mermaid's auto-layout may not match your mental model

---

## Embedding in the Report

All diagram types use the same embedding pattern:

```html
<div class="diagram-container">
  <div class="diagram-title">Diagram Title in Uppercase</div>
  <svg viewBox="..." xmlns="http://www.w3.org/2000/svg">
    <!-- SVG content (from Excalidraw export, hand-coded, or Mermaid output) -->
  </svg>
</div>
```

The `.diagram-container` provides:
- White background card with cream-dark border
- 10px rounded corners
- 22px padding
- `break-inside: avoid` in print (diagram never splits across pages)
- Centered SVG with `max-width: 100%`

### Multiple Diagrams

There's no limit on the number of diagrams per document. Place them where they add
context — after the paragraph that describes the concept. Avoid consecutive diagrams
without explanatory text between them.

---

## Brand Palette for Diagrams

Quick-copy hex values for use in any diagramming tool:

```
Primary:    #E8611A  (orange — accents, labels, active connections)
Background: #F5F0EA  (cream — box fills)
Dark:       #2D2D2D  (charcoal — borders, text, arrows)
Light text: #555555  (gray — subtitles, descriptions)
Accent:     #F28C50  (light orange — secondary elements)
Success:    #2E8B57  (green — completed/active states)
Info:       #3B7DD8  (blue — informational elements)
Danger:     #D63031  (red — errors/blockers)
White:      #FFFFFF  (text on dark/orange backgrounds)
```

---

## SVG Arrows — Arrowheads Land EXACTLY on Destination Edge

A common failure mode in hand-coded SVG diagrams: the arrowhead polygon
overshoots the destination rectangle by 5-10px, so the arrow's tip ends up
*inside* the destination box. This looks sloppy and is one of the most
common visual bugs caught by the post-render review.

The rule: **arrowhead polygon tip = destination rect's edge. Line ends
before the polygon's base.**

### Incorrect (arrowhead penetrates the rect)

```svg
<!-- Destination rect starts at x=200 -->
<line x1="140" y1="120" x2="240" y2="120" stroke="#2D2D2D"/>
<polygon points="238,116 248,120 238,124" fill="#2D2D2D"/>
<!-- polygon tip is at x=248: 48px INSIDE the destination rect -->
```

### Correct (arrowhead lands on the edge)

```svg
<!-- Destination rect starts at x=200 -->
<line x1="140" y1="120" x2="190" y2="120" stroke="#2D2D2D"/>
<polygon points="190,116 200,120 190,124" fill="#2D2D2D"/>
<!-- polygon base at x=190 (line ends there); tip at x=200 (the rect edge) -->
```

### Practical formula

If the destination rect starts at `X_dest`:

- `line.x2 = X_dest - 10`
- `polygon points = "X_dest-10,Y-4   X_dest,Y   X_dest-10,Y+4"`

The `10` is the polygon's pixel length. Adjust if you use larger or smaller
arrowheads, but keep the principle: line ends where polygon base begins;
polygon tip touches the rect edge.

### Diagram authoring checklist (arrows)

- [ ] Every arrowhead polygon's tip lands on the destination rect's edge — never inside, never outside.
- [ ] Every `<line>` preceding an arrowhead ends at the polygon's BASE (not the tip).
- [ ] Destination rects have explicit `stroke-width` — arrowheads aren't visually hidden under the stroke.
- [ ] Dashed arrows (deprecated or future state) use `stroke-dasharray="6,4"`.

---

## SVG Text — Labels Must Fit the Available Space

SVG `<text>` does NOT auto-wrap. A label placed between two rectangles (or
on an arrow line) will silently render past the available horizontal space,
visually mounting onto the next element. The DOM is intact; the rendered
PDF shows clipped or overlapping text.

### Concrete example

In one production document, the label `<text x="530" y="130" text-anchor="middle">TLS pasante</text>`
sat on the arrow between Firewall (right edge x=510) and PCE (left edge x=550). The label
width (~70px) extended from x≈495 to x≈565 — visually mounting onto the Firewall rect,
because only 40px of space actually existed.

### Authoring rule — calculate space BEFORE placing the label

1. **Calculate available space.** If the label sits between two rects:
   `available = X_destination - X_source_right_edge`. If it sits on an
   arrow, available = the arrow's length.

2. **Estimate label width.** For 9-10px sans-serif: each character ≈ 5-6px.
   "TLS pasante" (11 chars) ≈ 55-66px. Add 4px padding on each side.

3. **If the label doesn't fit, pick ONE of these in preference order:**

   **(a) Delete it if redundant.** If a nearby callout or the body text
   already explains the concept, the label is visual noise. Cleanest.

   **(b) Abbreviate.** "TLS pasante" → "TLS e2e". "Lightning Bolt" → "LB".
   Loses some formality but keeps the meaning.

   **(c) Split with `<tspan>`.** Multi-line label centered:
   ```svg
   <text x="530" y="130" text-anchor="middle" font-size="9" fill="#555">
     <tspan x="530" dy="0">TLS</tspan>
     <tspan x="530" dy="11">pasante</tspan>
   </text>
   ```

   **(d) Reposition off the critical axis.** Move the label above the
   source rect or below the destination rect — out of the line connecting
   them.

   **(e) Redesign the diagram.** If the space is structurally insufficient,
   widen the layout or change the topology.

4. **NEVER ship clipped or overlapping text.** It's a graphic-consistency
   error that breaks the professional appearance of the entire document.

### Diagram authoring checklist (text)

- [ ] Every `<text text-anchor="middle">` fits in the horizontal space between adjacent rects.
- [ ] Every `<text text-anchor="start">` doesn't extend into the next element.
- [ ] No `<text>` visually mounts a `<rect>` it doesn't belong to.
- [ ] If a label is borderline, prefer two `<tspan>` lines or deletion over a single line that *might* fit.
- [ ] In Spanish/Portuguese documents, recalculate widths: ES text is ~15% longer than the English equivalent.

The programmatic pre-flight (`scripts/visual_verify.py`, check 1) catches
SVG text that overflows its parent `<svg>`. The rules above prevent the
subtler case where text overflows a *sibling* rect inside the same SVG —
the script doesn't catch this; visual review must.
