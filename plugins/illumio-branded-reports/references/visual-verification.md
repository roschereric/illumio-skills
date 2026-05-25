# Visual Verification — Programmatic Pre-Flight

> **When to read this:** at Step 7 of the workflow, before the human visual
> review loop. The four checks below are deterministic and catch a class of
> defects that the human visual checklist cannot reliably spot — especially
> silent SVG text overflow, which renders without warning and only becomes
> visible in the final PDF.

The bundled `scripts/visual_verify.py` runs all four checks in one pass.
This reference explains what each check looks for, why it exists, and how
to interpret the output.

---

## Why this layer exists

The canonical Visual Review Checklist (in `SKILL.md`) is a human-eye layer:
"does the cover look right? do labels collide?" Those judgments require
taste. But four failure categories are *not* judgment calls — they're
deterministic geometry that a script can verify in milliseconds and that
human review misses in long documents:

1. **SVG `<text>` overflowing its parent `<svg>`** — silent in markup, often
   clipped only at PDF time when page margins kick in.
2. **DOM horizontal overflow** — any element whose `scrollWidth > clientWidth`
   indicates content escaping its container.
3. **Image load failure** — a `404` on a logo or asset, or a `<img>` with
   `naturalWidth === 0`. The markup looks fine; the rendered output has a
   broken-image icon.
4. **Z-index intersection** — an `<h1>` whose bounding rect overlaps a
   decorative absolutely-positioned element with a higher effective z-index.
   The title is silently obscured.

Running these checks BEFORE the human visual review means the human only
has to judge taste, not catch missed pixels.

---

## The four checks

### Check 1 — SVG text overflow

**What it looks for:** every `<text>` element inside every `<svg>`, the
text's `getBoundingClientRect()` must lie fully within the parent `<svg>`'s
`getBoundingClientRect()`.

**Why this fails silently:** SVG `<text>` does not auto-wrap. If a caption
or legend caption exceeds the remaining horizontal space inside the
`viewBox`, the text just keeps rendering past the SVG's right edge. In
screen view the diagram container's `border-radius` or `overflow: hidden`
may clip it; in PDF the page margin clips it entirely. Markup review
notices nothing.

**Output when it fires:**
```
SVG_TEXT_OVERFLOW  svg#diagram-3  text="9. firewall installed -> port..."
                   text right edge: 805 px
                   svg right edge:  740 px
                   overflow:        65 px
```

**Typical fix:** split the `<text>` into two rows at `text-anchor="middle"`,
incrementing `y`. Or replace with a `<foreignObject>` containing an HTML
`<div>` (which DOES wrap). Long Spanish/Portuguese sentences especially —
see SKILL.md Visual Review Checklist item 9.

### Check 2 — DOM horizontal overflow

**What it looks for:** every element except `<pre>` (where horizontal
scroll is intentional for code blocks) must satisfy
`scrollWidth <= clientWidth + 1`. The `+ 1` tolerates sub-pixel
rounding artifacts.

**Why this matters:** any element whose `scrollWidth > clientWidth` is
hiding content from the user. In screen view they may not see it; in
print it's clipped at the page edge.

**Output when it fires:**
```
DOM_OVERFLOW  div.callout.callout-warning
              scrollWidth: 612 px
              clientWidth: 580 px
              overflow:    32 px
```

**Typical fix:** narrow the content (shorter label), widen the container
(adjust grid layout), or apply `overflow-wrap: anywhere` to long
unbreakable strings.

### Check 3 — Image load

**What it looks for:** every `<img>` element must satisfy
`complete === true && naturalWidth > 0`.

**Why this matters:** logos and asset references break for prosaic
reasons — wrong relative path, typo in filename, asset folder not
copied alongside the HTML. The PDF renders with a broken-image icon
that's instantly noticeable to a customer.

**Output when it fires:**
```
IMG_LOAD_FAIL  <img src="assets/logo-orange.png">
               (file did not load — check path / case sensitivity)
```

**Typical fix:** correct the path, copy the missing asset, or check
case sensitivity (macOS local filesystem is case-insensitive but
WeasyPrint's path resolution can be strict).

### Check 4 — Z-index sanity

**What it looks for:** any `<h1>` or `<h2>` whose bounding rect intersects
a decorative absolutely-positioned element (`.geo-*`, `.dots`, `.dots-2`,
or any element with `position: absolute`) AND whose effective z-index is
≤ the decoration's effective z-index.

**Why this matters:** the cover stacking bug. A long title silently
renders *behind* a parallelogram or dot matrix. The DOM is intact; the
rendered glyph is hidden. This is the failure mode behind BUG-01 in the
post-mortem.

**Output when it fires:**
```
Z_INDEX_INTERSECT  h1 "Reaccion ante Nuevas Amenazas"
                   intersects .geo-1
                   h1 effective z-index:  auto (treated as 0)
                   geo-1 effective z-index: auto (treated as 0)
                   intersection area: 8,640 sq px
```

**Typical fix:** apply the Cover Stacking Rules pattern from SKILL.md.
Wrap foreground content in `.cover-content` with `position: relative;
z-index: 2; max-width: 560px;`. Set decorations to `z-index: 1`.

---

## Running the checks

### Dependencies

```bash
pip install playwright --break-system-packages
playwright install chromium
```

Playwright bundles Chromium for headless rendering. ~150 MB on first
install; cached afterward.

### Invocation

```bash
python scripts/visual_verify.py path/to/document.html
```

The script:
1. Opens `document.html` in headless Chromium at 1280×800 viewport.
2. Waits for `networkidle` (all images loaded).
3. Runs all four checks via injected JavaScript.
4. Prints findings grouped by check.
5. Exits `0` if clean, `1` if any check fails.

### Interpreting exit codes

- `0` — clean. Proceed to Step 8 (human visual review).
- `1` — one or more checks failed. Read the findings, fix the HTML/CSS,
  re-render, re-run. Do not continue until clean.

### Iterating fast

The script is fast (~2-3 seconds on a typical document). Run it after
every HTML/CSS edit during development, not just at the end. It will
catch new overflows the moment you introduce them.

---

## Triage table — programmatic finding → quick fix

| Check fires | First thing to try | If that doesn't work |
|---|---|---|
| `SVG_TEXT_OVERFLOW` | Split `<text>` into 2 rows at `text-anchor="middle"` | Replace with `<foreignObject>` + HTML `<div>` |
| `DOM_OVERFLOW` on a `.callout` or `.diagram-title` | Shorten the label | Apply `overflow-wrap: anywhere` |
| `DOM_OVERFLOW` on a `<table>` | Convert wide column to truncated + `title` tooltip | Re-layout as 2-column table or wrap to next row |
| `IMG_LOAD_FAIL` | Check relative path, case sensitivity, `base_url` passed to WeasyPrint | Copy `assets/` next to the HTML |
| `Z_INDEX_INTERSECT` | Apply Cover Stacking Rules pattern | Increase `max-width` on `.cover-content` |

---

## When the checks are wrong

These are heuristics. A few false positives are expected:

- **Check 2 may flag `<pre>` content** in some configurations. The script
  excludes `<pre>` by tag, but if you wrap code in `<div class="code-block">
  <pre>...</pre></div>` and the outer `<div>` overflows, you'll see it.
  Decide case-by-case whether to suppress.
- **Check 4 may flag intentional overlap** — sometimes a designer wants a
  title to overlap a decoration deliberately, with the title in front. If
  z-index is set explicitly (e.g., `z-index: 10`), the check correctly
  reports no failure. The false positive is only when z-index is `auto`
  on both sides.

If a finding is a genuine false positive, document why in the rendered
HTML's comment block (`<!-- VERIFY-IGNORE: check_4 intentional overlap -->`)
so the next reviewer doesn't re-investigate.

---

## Extending this layer

New defect categories surface over time. To add a check:

1. Add the JavaScript check function to `scripts/visual_verify.py`.
2. Add a section here describing what it looks for, why, the output
   format, and typical fixes.
3. Add an eval case to `evals/evals.json` that demonstrates the failure.
4. Update SKILL.md Step 7 if the new check belongs in the mandatory
   pre-flight set.

The bar for adding a check: it must be deterministic geometry or DOM
state, not taste. Taste belongs in the human visual checklist.
