#!/usr/bin/env python3
"""
visual_verify.py — Programmatic pre-flight checks for branded report HTML.

Runs four deterministic checks against a rendered HTML document via headless
Chromium (Playwright). Designed to be invoked at Step 7 of the workflow,
BEFORE the human visual review loop.

Usage:
    python scripts/visual_verify.py path/to/document.html
    python scripts/visual_verify.py path/to/document.html --viewport 1440x900

Exit codes:
    0 — all checks passed, proceed to visual review
    1 — one or more checks failed, fix HTML/CSS and re-run
    2 — script error (missing deps, file not found, etc.)

Dependencies:
    pip install playwright --break-system-packages
    playwright install chromium

See references/visual-verification.md for what each check looks for
and how to interpret the output.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "ERROR: playwright is not installed.\n"
        "  pip install playwright --break-system-packages\n"
        "  playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# JavaScript checks injected into the page
# ---------------------------------------------------------------------------
#
# Each check returns a list of findings; an empty list means the check passed.
# All four are run in a single page.evaluate() call to minimize round-trips.

VERIFY_JS = r"""
() => {
  const findings = { svg_text_overflow: [], dom_overflow: [],
                     img_load_fail: [], z_index_intersect: [] };

  // ---------- Check 1: SVG text overflow ----------
  document.querySelectorAll('svg').forEach((svg, svgIdx) => {
    const svgRect = svg.getBoundingClientRect();
    svg.querySelectorAll('text').forEach((t, tIdx) => {
      const r = t.getBoundingClientRect();
      // ignore zero-size text (typically display:none or unrendered)
      if (r.width === 0 || r.height === 0) return;
      const overflow = {
        right:  r.right  - svgRect.right,
        left:   svgRect.left  - r.left,
        top:    svgRect.top   - r.top,
        bottom: r.bottom - svgRect.bottom,
      };
      const worst = Math.max(overflow.right, overflow.left,
                             overflow.top,   overflow.bottom);
      if (worst > 1) {
        findings.svg_text_overflow.push({
          svg_index: svgIdx,
          svg_id: svg.id || null,
          text_index: tIdx,
          text_snippet: (t.textContent || '').trim().slice(0, 60),
          overflow_px: Math.round(worst),
          direction: Object.keys(overflow).reduce(
            (a, k) => overflow[k] > overflow[a] ? k : a),
          svg_rect:  { left: svgRect.left, right: svgRect.right,
                       top: svgRect.top, bottom: svgRect.bottom },
          text_rect: { left: r.left, right: r.right,
                       top: r.top, bottom: r.bottom },
        });
      }
    });
  });

  // ---------- Check 2: DOM horizontal overflow ----------
  // Skip <pre> (code blocks expect horizontal scroll) and elements
  // explicitly marked overflow-allowed.
  document.querySelectorAll('*').forEach((el) => {
    if (el.tagName === 'PRE' || el.tagName === 'CODE') return;
    if (el.hasAttribute('data-verify-ignore-overflow')) return;
    // skip if not visible
    const cs = window.getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    if (el.clientWidth === 0) return;
    if (el.scrollWidth > el.clientWidth + 1) {
      findings.dom_overflow.push({
        tag: el.tagName.toLowerCase(),
        class_list: Array.from(el.classList),
        id: el.id || null,
        scroll_width: el.scrollWidth,
        client_width: el.clientWidth,
        overflow_px: el.scrollWidth - el.clientWidth,
        snippet: (el.textContent || '').trim().slice(0, 60),
      });
    }
  });

  // ---------- Check 3: Image load ----------
  document.querySelectorAll('img').forEach((img) => {
    if (!img.complete || img.naturalWidth === 0) {
      findings.img_load_fail.push({
        src: img.getAttribute('src'),
        alt: img.getAttribute('alt') || null,
        complete: img.complete,
        natural_width: img.naturalWidth,
      });
    }
  });

  // ---------- Check 4: Z-index sanity ----------
  // For every h1/h2, check whether its bounding rect overlaps any
  // absolutely-positioned decoration, and whether stacking permits it.
  const decorations = Array.from(document.querySelectorAll(
    '.geo-1, .geo-2, .geo-3, .dots, .dots-2, [data-decoration]'
  ));
  const headings = document.querySelectorAll('h1, h2');

  function rectsOverlap(a, b) {
    return !(a.right < b.left || b.right < a.left ||
             a.bottom < b.top || b.bottom < a.top);
  }
  function effectiveZ(el) {
    const z = window.getComputedStyle(el).zIndex;
    return z === 'auto' ? 0 : parseInt(z, 10) || 0;
  }

  headings.forEach((h) => {
    const hRect = h.getBoundingClientRect();
    if (hRect.width === 0 || hRect.height === 0) return;
    const hZ = effectiveZ(h);
    decorations.forEach((dec) => {
      const dRect = dec.getBoundingClientRect();
      if (dRect.width === 0 || dRect.height === 0) return;
      if (!rectsOverlap(hRect, dRect)) return;
      const dZ = effectiveZ(dec);
      if (hZ <= dZ) {
        // overlap detected and heading is NOT explicitly above decoration
        const ix = Math.max(0, Math.min(hRect.right, dRect.right) -
                               Math.max(hRect.left,  dRect.left));
        const iy = Math.max(0, Math.min(hRect.bottom, dRect.bottom) -
                               Math.max(hRect.top,    dRect.top));
        findings.z_index_intersect.push({
          heading_tag: h.tagName.toLowerCase(),
          heading_text: (h.textContent || '').trim().slice(0, 80),
          heading_z: hZ,
          decoration_class: Array.from(dec.classList),
          decoration_z: dZ,
          intersection_area_sqpx: Math.round(ix * iy),
        });
      }
    });
  });

  return findings;
}
"""


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def fmt_svg_text_overflow(f: dict) -> str:
    return (
        f"  svg_index={f['svg_index']} text=\"{f['text_snippet']}\"\n"
        f"    overflow {f['overflow_px']}px to the {f['direction']}\n"
        f"    text rect: left={f['text_rect']['left']:.0f} "
        f"right={f['text_rect']['right']:.0f}  | "
        f"svg rect: right={f['svg_rect']['right']:.0f}"
    )


def fmt_dom_overflow(f: dict) -> str:
    cls = '.'.join(f['class_list']) if f['class_list'] else '(no class)'
    return (
        f"  {f['tag']}.{cls}\n"
        f"    scrollWidth={f['scroll_width']} clientWidth={f['client_width']}"
        f"  overflow={f['overflow_px']}px\n"
        f"    snippet: {f['snippet']!r}"
    )


def fmt_img_load_fail(f: dict) -> str:
    return f"  <img src={f['src']!r}> alt={f['alt']!r}  natural_width={f['natural_width']}"


def fmt_z_index_intersect(f: dict) -> str:
    return (
        f"  {f['heading_tag']} \"{f['heading_text']}\"\n"
        f"    intersects {'.'.join(f['decoration_class'])}\n"
        f"    heading z={f['heading_z']}  decoration z={f['decoration_z']}"
        f"  area={f['intersection_area_sqpx']}sqpx"
    )


CHECK_LABELS = {
    'svg_text_overflow':  ('SVG_TEXT_OVERFLOW',  fmt_svg_text_overflow),
    'dom_overflow':       ('DOM_OVERFLOW',       fmt_dom_overflow),
    'img_load_fail':      ('IMG_LOAD_FAIL',      fmt_img_load_fail),
    'z_index_intersect':  ('Z_INDEX_INTERSECT',  fmt_z_index_intersect),
}


def print_findings(findings: dict) -> int:
    total = sum(len(v) for v in findings.values())
    if total == 0:
        print("visual_verify: OK — all four checks passed.")
        return 0
    print(f"visual_verify: FAIL — {total} finding(s) across "
          f"{sum(1 for v in findings.values() if v)} check(s).\n")
    for key, items in findings.items():
        if not items:
            continue
        label, formatter = CHECK_LABELS[key]
        print(f"=== {label} ({len(items)} finding(s)) ===")
        for f in items:
            print(formatter(f))
            print()
    return 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_viewport(s: str) -> tuple[int, int]:
    try:
        w, h = s.lower().split('x')
        return int(w), int(h)
    except Exception:
        raise argparse.ArgumentTypeError(
            f"viewport must be WIDTHxHEIGHT (got {s!r})")


def main() -> int:
    p = argparse.ArgumentParser(
        description="Programmatic pre-flight checks for branded report HTML.")
    p.add_argument('html', help="Path to the rendered HTML document.")
    p.add_argument('--viewport', type=parse_viewport, default=(1280, 800),
                   help="Browser viewport (default 1280x800).")
    p.add_argument('--json', action='store_true',
                   help="Emit findings as JSON instead of human text.")
    args = p.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        print(f"ERROR: {html_path} does not exist.", file=sys.stderr)
        return 2

    width, height = args.viewport

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={'width': width, 'height': height})
        page = context.new_page()
        page.goto(html_path.as_uri(), wait_until='networkidle')
        findings = page.evaluate(VERIFY_JS)
        browser.close()

    if args.json:
        print(json.dumps(findings, indent=2))
        return 0 if all(len(v) == 0 for v in findings.values()) else 1

    return print_findings(findings)


if __name__ == '__main__':
    sys.exit(main())
