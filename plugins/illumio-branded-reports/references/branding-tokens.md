# Illumio Branding Tokens

## Color Palette

### Primary Colors
| Token                | Hex       | RGB             | Usage                                          |
|----------------------|-----------|-----------------|------------------------------------------------|
| `--ill-orange`       | `#E8611A` | `232, 97, 26`   | Primary accent: borders, badges, buttons       |
| `--ill-orange-light` | `#F28C50` | `242, 140, 80`  | Secondary accent: geometric shapes, highlights |
| `--ill-orange-dark`  | `#C4500F` | `196, 80, 15`   | Callout labels, dark accent contexts           |
| `--ill-cream`        | `#F5F0EA` | `245, 240, 234` | Page background                                |
| `--ill-cream-dark`   | `#EDE6DC` | `237, 230, 220` | Borders, code inline background, dividers      |
| `--ill-charcoal`     | `#2D2D2D` | `45, 45, 45`    | Body text, table headers, phase banners        |

### Neutral Grays
| Token              | Hex       | Usage                    |
|--------------------|-----------|--------------------------|
| `--ill-gray-700`   | `#3D3D3D` | Paragraph text           |
| `--ill-gray-600`   | `#555555` | Secondary text           |
| `--ill-gray-400`   | `#999999` | Section labels, metadata |
| `--ill-gray-300`   | `#BBBBBB` | Footer text, subtle info |

### Semantic Colors
| Token              | Hex       | Usage                               |
|--------------------|-----------|-------------------------------------|
| `--ill-success`    | `#2E8B57` | Success callouts, positive states   |
| `--ill-info-blue`  | `#3B7DD8` | Info callouts, informational notes  |
| `--ill-danger`     | `#D63031` | Critical/error callouts, warnings   |
| `--ill-code-bg`    | `#1E1E1E` | Code block background (VS Code dark)|

### Cover-Specific Colors
| Token                | Hex       | Usage                           |
|----------------------|-----------|---------------------------------|
| `--ill-cover-dark`   | `#3B4856` | Cover gradient end              |
| `--ill-cover-darker` | `#2B3640` | Cover gradient start            |
| Cover gradient end   | `#4A5A6A` | Cover gradient light end        |

## Typography

### Font Stack
- **Body**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- **Code**: `'JetBrains Mono', 'Fira Code', 'Consolas', monospace`

### Font Weights Used
| Weight | Usage                                     |
|--------|-------------------------------------------|
| 300    | Light — cover subtitle                    |
| 400    | Regular — body text                       |
| 500    | Medium — metadata                         |
| 600    | Semibold — phase titles, table headers    |
| 700    | Bold — h3, step titles, callout labels    |
| 800    | Extrabold — h1, h2, step numbers          |
| 900    | Black — available for emphasis            |

### Type Scale
| Element          | Size   | Weight | Color              |
|------------------|--------|--------|--------------------|
| Cover h1         | 38px   | 800    | White              |
| Cover subtitle   | 15px   | 400    | White 70% opacity  |
| h2 (section)     | 24px   | 800    | Charcoal           |
| h3 (subsection)  | 16px   | 700    | Charcoal           |
| h4 (step title)  | 14px   | 700    | Charcoal           |
| Body paragraph   | 13.5px | 400    | Gray-700           |
| Code block       | 11.5px | 400    | #D4D4D4 on dark    |
| Section label    | 11px   | 400    | Gray-400 uppercase |
| Table header     | 11px   | 600    | White uppercase    |
| Callout label    | 11.5px | 700    | Semantic color     |

### Line Heights
| Context    | Value |
|------------|-------|
| Body       | 1.7   |
| Code       | 1.6   |
| Headings   | 1.2   |
| Callouts   | 1.65  |
| Cover sub  | 1.6   |

## Spacing System

| Context             | Value  |
|---------------------|--------|
| Section padding     | 36px 60px (screen), 20px 50px (print) |
| Callout padding     | 14px 18px                              |
| Code block padding  | 16px 20px                              |
| Step gap            | 14px                                   |
| Phase banner margin | 28px top, 14px bottom                  |
| Cover padding       | 80px                                   |
| Border radius       | 8px (most), 10px (diagram), 3px (code inline) |

## Geometric Shapes (Cover)

The cover uses three skewed parallelogram shapes in the upper-right area:

```css
.geo-1 { top:-60px; right:80px;  width:130px; height:360px; background:var(--ill-orange);       skewX(-8deg); opacity:0.92; }
.geo-2 { top:20px;  right:230px; width:90px;  height:280px; background:var(--ill-orange-light);  skewX(-8deg); opacity:0.65; }
.geo-3 { bottom:-30px; right:40px; width:70px; height:220px; background:var(--ill-orange-dark);  skewX(-8deg); opacity:0.55; }
```

Plus two dot-matrix patterns:
```css
.dots   { top:40px;    right:340px; 80x80px;  radial-gradient white 30% opacity }
.dots-2 { bottom:80px; right:180px; 60x60px;  radial-gradient orange 50% opacity }
```

## Logo Usage

- **White logo** on dark backgrounds (cover, footer CTA)
- **Dark logo** on light backgrounds (section headers, content area)
- Height: 40px on cover, 22px in section headers
- Both logos are embedded as base64 PNG in the template — no external files needed

---

## Logo Handling — Two Variants of the Official Asset

### Fundamental principle — NEVER recreate or substitute brand elements

> **Never substitute, recreate, or approximate brand image elements.** This
> includes logos, wordmarks, isotypes, and any representation of the brand.
> The ONLY permitted modification of an official brand asset is changing
> fill colors while keeping paths, viewBox, proportions, and composition
> identical.

Explicitly forbidden anti-patterns:

- ❌ Replacing the wordmark "illumio" with text in another font (Inter, Helvetica, etc.)
- ❌ Drawing the isotype with rectangles, circles, or inline SVG shapes that approximate the mark
- ❌ "Inspired" simplified versions of the logo
- ❌ Variations not approved by brand (removing the isotype, changing element spacing, etc.)

Correct patterns:

- ✅ Use the official SVG file as-is
- ✅ When a different palette is needed (e.g., white-on-dark), generate a fill-substituted variant of the SAME file — never modify paths or structure
- ✅ If the official asset is not accessible (sandbox without network, blocked CDN), STOP and ask the user for the file. Do not improvise.

### Why CSS `filter` doesn't work for SVG logos in WeasyPrint

The earlier pattern of `filter: brightness(0) invert(1)` on `<img src="logo.svg">` works in browsers but **fails silently in WeasyPrint** — WeasyPrint v60+ implements `filter` for HTML elements but does NOT propagate it into the vectorial content of an embedded SVG. The PDF renders the SVG's native fills.

This produces a particularly confusing failure: the browser preview looks correct, the developer assumes the build is fine, and only the PDF (which the customer actually receives) shows the broken result. **Always verify in the PDF, not in the browser.**

### Solution — generate fill-substituted variants

```bash
# 1. Inspect the official SVG to find the fills that need substituting
grep -o 'fill="[^"]*"' assets/logo-dark.svg | sort -u
# Typical output:
#   fill="none"            <- leave alone (transparencies)
#   fill="#313638"         <- charcoal of the wordmark
#   fill="#FF5500"         <- orange of the isotype (if applicable)

# 2. Generate the white variant by substituting opaque fills
sed -e 's/fill="#313638"/fill="white"/g' \
    -e 's/fill="#FF5500"/fill="white"/g' \
    assets/logo-dark.svg > assets/logo-white.svg

# 3. Verify — only "none" and "white" should remain
grep -o 'fill="[^"]*"' assets/logo-white.svg | sort -u
```

> **Note on the current skill assets.** This skill ships PNG variants
> (`assets/logo-dark.png` and `assets/logo-white.png`). PNG works
> universally in WeasyPrint and is the safe default. If you need crisper
> rendering at large sizes, you can swap to SVG variants generated by the
> `sed` pattern above, but keep PNG as the canonical fallback for
> production documents until you've verified SVG renders cleanly in your
> target environment.

### Variant A — Cover (dark background)

```html
<div class="cover-logo">
  <img src="assets/logo-white.png" alt="Illumio" style="height:36px;">
  <!-- or, if using SVG variants: src="assets/logo-white.svg" -->
</div>
```

```css
.cover-logo { display: flex; align-items: center; }
.cover-logo img { height: 36px; }
```

### Variant B — Section running headers (cream background)

```html
<div class="section-header">
  <div class="logo-mini">
    <img src="assets/logo-dark.png" alt="Illumio" style="height:22px;">
  </div>
  <span class="section-label">SECTION NAME</span>
</div>
```

```css
.section-header .logo-mini img { height: 22px; }
```

### Documented anti-pattern — the "rectangles + Inter text" rollback

A previous iteration of this skill, when it couldn't load the official asset, attempted a rollback to an inline SVG made of two colored rectangles plus a `<span>illumio</span>` in Inter font. That passed the "contrast on dark background" check but violated the no-invention principle: the Illumio wordmark has a specific type design that Inter does not replicate, and the isotype is a particular composition, not two rectangles.

If the official asset truly cannot be loaded, **the correct response is to pause and ask the user for the file**. A delayed render is infinitely better than shipping a PDF with an apocryphal logo.

### Logo usage checklist

- [ ] Both files exist in `assets/`: `logo-dark.png` (or `.svg`) and `logo-white.png` (or `.svg`)
- [ ] Both variants share identical structure (paths, viewBox, dimensions) — only fills differ
- [ ] Cover uses the white variant directly, no `filter`
- [ ] Section headers use the dark variant directly, no `filter`
- [ ] No inline `<svg>` in the document approximates the logo
- [ ] No `<span>` simulates the wordmark in an alternate font
- [ ] Render to PDF and verify visually — browser preview is not sufficient
