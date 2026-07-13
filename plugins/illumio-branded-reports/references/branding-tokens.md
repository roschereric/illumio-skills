# Illumio Branding Tokens — OFFICIAL (Illumio Brand Hub / Frontify)

Verified against the Illumio Brand Hub (illumio.frontify.com, Design System:
Color / Typography / Logo / Pattern & Shape / Imagery; guidelines last
modified May 2026). Values below marked **[official]** are verbatim from the
Brand Hub; values marked *[derived]* are pragmatic derivations for print
legibility and are documented as such.

## Color Palette

Rule from the Brand Hub: *"Designs should always lead with Illumio Orange."*
Secondary colors support, never overshadow. Tertiary accents are used
sparingly and never alone.

### Primary Colors [official]
| Name | Hex | RGB | CMYK | PMS |
|---|---|---|---|---|
| **Illumio Orange** | `#FF5500` | 255, 85, 0 | 0, 77, 100, 0 | Orange 21C |
| **White** | `#FFFFFF` | 255, 255, 255 | 0, 0, 0, 0 | — |
| **Server Slate 100** | `#313638` | 49, 54, 56 | 70, 57, 63, 65 | 447C |

Server Slate tint scale [official]: 90 `#464A4C` · 80 `#64686A` · 70 `#6F7274`
· 60 `#838688` · 50 `#989A9B` · 40 `#ADAFAF` · 30 `#C1C3C3` · 20 `#D6D7D7`
· 10 `#EAEBEB` · 5 `#F5F5F5`. Server Slate is the primary TEXT color.

### Secondary Colors [official]
| Name | Scale (hex) | Use |
|---|---|---|
| **System Cyan** | 120 `#1A2C32` · 110 `#24393F` · 100 `#2D454C` · 90 `#325158` · 80 `#356069` | Cool dark backgrounds that ground designs (our code blocks use 120) |
| **Zero Trust Tan** | 130 `#D1BEA0` · 120 `#E3D8C5` · 110 `#F2EDE2` · 100 `#F7F4EE` | Warm subtle backgrounds (our panel fills use 100) |
| **Cloud Cerulean** | 120 `#94CEE5` · 110 `#C2E2F0` · 100 `#E5F2F9` · 90 `#F3F8FC` | Calm light backgrounds (our info callouts use 100) |

### Tertiary Colors & Accents [official — use sparingly, never alone]
| Name | Scale (hex) | Use |
|---|---|---|
| **Circuit Gold** | 110 `#F97607` · 100 `#FFA22F` · 90 `#FFB74A` · 80 `#FFD388` · 70 `#FFEAC6` · 60 `#FFF8EB` | Chart/diagram highlights; 60 is our warning-callout fill |
| **Protocol Purple** | 130 `#3C1632` … 80 `#C66FB6` (100 `#8B407A`) | Product illustrations/abstractions ONLY |
| **Cyber Chartreuse** | 100 `#BBFF22` | Fine lines / thin shapes ONLY, smallest possible amounts |

### Diagram Colors [official — charts, diagrams, product abstractions ONLY]
| Name | Scale (hex) | Use |
|---|---|---|
| **Safeguard Green** | 130 `#08261B` · 120 `#11432F` · 100 `#166644` · 80 `#299B65` | Benefits / positive aspects (our success callouts use 100) |
| **Risk Red** | 130 `#4C0514` · 120 `#88132E` · 100 `#BE122F` · 80 `#F43F51` | Risks / negative aspects (our critical callouts use 100) |

### Skill CSS tokens → official mapping
| Token | Value | Source |
|---|---|---|
| `--ill-orange` | `#FF5500` | Illumio Orange [official] |
| `--ill-slate` | `#313638` | Server Slate 100 [official] |
| `--ill-paper` | `#FFFFFF` | White [official] |
| `--ill-mist` | `#F7F4EE` | Zero Trust Tan 100 [official] |
| `--ill-line` | `#EAEBEB` | Server Slate 10 [official] |
| `--ill-gray-700/600/400/300` | `#464A4C` / `#6F7274` / `#989A9B` / `#C1C3C3` | Server Slate 90/70/50/30 [official] |
| `--ill-code-bg`, `--ill-syscyan-deep` | `#1A2C32` | System Cyan 120 [official] |
| `--ill-syscyan` | `#2D454C` | System Cyan 100 [official] |
| `--ill-success` | `#166644` | Safeguard Green 100 [official] |
| `--ill-danger` | `#BE122F` | Risk Red 100 [official] |
| `--ill-info-blue` | `#356069` | System Cyan 80 [official] |
| `--ill-gold` | `#FFA22F` | Circuit Gold 100 [official] |
| `--ill-chartreuse` | `#BBFF22` | Cyber Chartreuse [official] |
| `--ill-orange-deep` | `#C43C00` | *[derived]* darker orange for small text/links on white (AA contrast); official orange stays the accent |
| `--ill-orange-light` | `#FF7A33` | *[derived]* tint for underlines/soft accents |

## Typography [official]

**Primary typeface: FK Grotesk** (Florian Karsten Typefaces). LICENSED —
the Brand Hub states the font file is *not authorized for distribution*;
production use requires Brand-team approval. Therefore this skill does NOT
bundle or embed it. Do not add FK Grotesk files to `assets/fonts/`; a PDF
embeds whatever font renders it, and embedding an unlicensed copy in
customer-facing files is a violation.

**Secondary typeface: Montserrat** — the Brand Hub's designated replacement
when FK Grotesk is unavailable, explicitly sanctioned for *"the Corporate
PowerPoint Template, or other self-publishing document templates where the
font can be embedded into the file"* (SIL OFL license). That is exactly this
skill's use case, so **Montserrat (bundled in `assets/fonts/`) is the default
and correct typeface for these reports.** Official weights in use:
ExtraLight 200, Light 300, Regular 400, Medium 500, SemiBold 600, Bold 700.

**Last-resort fallback: Arial** [official]. The CSS stack is
`'Montserrat', Arial, …`. Code uses JetBrains Mono (bundled; not a Brand Hub
face — *[derived]* choice for technical monospace, swap freely).

### Type scale (print) — skill spec
| Element | Size | Weight | Color |
|---|---|---|---|
| Cover h1 | 31pt | **300 Light** | White (slate on paper variant) |
| Cover subtitle | 13.5pt | **700 Bold** | White |
| Cover byline / date | 10.5pt | 500 / 400 | White 95% / 78% |
| h2 (section) | 25px | 700 | Slate + 10px orange square tick |
| h3 | 16px | 700 | Slate |
| Body | 13.5px | 400 | Server Slate 90 |
| Code | 10px | 400 | `#D9DCDD` on System Cyan 120 |
| Section label | 10.5px | 600 | Server Slate 50, tracking 1.6px |
| Ref-list entries | 10.5px | 400 | Server Slate 70; URLs orange-deep |

## Logo [official rules — Brand Hub, Design System > Logo]

The lock-up = glyph + logotype. The glyph represents the **PCE and VEN
joining within a contained boundary**. Four approved color variants:

| Variant | When |
|---|---|
| **White** | On any solid color or photo darker than 30% gray (our orange & slate covers) |
| **Orange & slate gray** | On anything lighter than 20% gray (our white pages/headers) |
| **Orange & white** | Alternative on dark backgrounds when keeping some orange |
| **Black** | Only when black is required (1-color printing etc.) |

Hard rules [official]:
- Design ratio is **4:1** (width = 4 × height) — never skew. The bundled
  PNGs are 800×200, exactly 4:1; height-only CSS sizing preserves it.
- **Clear space:** at least one glyph's width around the lock-up (half a
  glyph when pairing with a third-party logo, or more if the partner requires).
- The glyph may be used alone (avatar/compact); the **logotype never appears
  alone**, and the two are never rearranged or altered independently.
- Never: blur/pixelate, layer over busy imagery, change the logotype, add
  effects, use inline with text, squish/stretch, **recolor**, outline,
  underline, or rotate.

### Skill enforcement (unchanged)
- Use ONLY `assets/logo-white.png` (dark/orange backgrounds) and
  `assets/logo-dark.png` (= official "orange & slate gray", light backgrounds).
- `check_brand.py` hash-verifies both. Missing/new variant needed (e.g. the
  official SVG or orange-&-white version)? **STOP and ASK THE USER** —
  download from the Brand Hub ("Download logos") — never redraw or recolor.
- No CSS `filter` recoloring (WeasyPrint renders native fills; browsers lie).
- Verify in the rendered PDF, never only the browser preview.

## Pattern & Shape [official vocabulary]

Everything derives from the **isometric grid**: staggered rhombus patterns,
parallelograms (with rhombus shadows), hexagons, isometric **containers**
(prism building blocks used to compose "cities, networks, abstract
landscapes" that represent *growth, connection, protection*), and thin
**accent lines**. Sanctioned uses in this skill: the default cover strip
(`assets/cover-art.svg`, generated from these primitives on System Cyan 120),
the 10px orange square before h2 headings, and small square/diamond clusters
in the closing CTA box. Decoration never overlaps text — `visual_verify.py`
polices `[data-decoration]` elements.

## Imagery [official]

Hero "storytelling imagery" (the containment world-building renders seen on
corporate decks) comes from an **approved library** — appropriate for
"high engagement documents, guides, or briefs". When the user supplies one,
apply it with `new_report.py --cover-art <file>`; brand elements may be
overlaid. Do not generate imitation storytelling imagery.

---

Source: Illumio Brand Hub — https://illumio.frontify.com/hub/218823
(Design System document 428325: Logo, Color, Typography, Imagery,
Pattern & Shape). Re-verify against the hub when guidelines change.
