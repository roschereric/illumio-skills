#!/usr/bin/env python3
"""
render_report.py — render report.html to PDF + per-page PNGs in one command.

    python <skill>/scripts/render_report.py path/to/report.html \
        [--pdf out.pdf] [--png-dir _render] [--dpi 110] [--no-png]

Produces:
  * the PDF (default: alongside the HTML, same stem)
  * _render/page-01.png … one PNG per page (pdftoppm, else pdf2image)

Always Read/inspect EVERY PNG afterwards — no sampling. Exit codes:
0 ok · 1 render produced 0 pages · 2 setup error (missing deps → install,
do not silently skip; if the environment cannot run WeasyPrint, STOP and
tell the user instead of shipping an unrendered HTML).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--pdf", default=None)
    ap.add_argument("--png-dir", default=None)
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()

    src = Path(args.html).resolve()
    if not src.is_file():
        print(f"ERROR: {src} not found", file=sys.stderr)
        return 2
    pdf = Path(args.pdf).resolve() if args.pdf else src.with_suffix(".pdf")

    try:
        from weasyprint import HTML  # noqa: deferred import for clear error
    except ImportError:
        print("ERROR: WeasyPrint missing. Install first:\n"
              "  pip install weasyprint --break-system-packages", file=sys.stderr)
        return 2

    doc = HTML(filename=str(src)).render()
    n = len(doc.pages)
    print(f"Rendered {n} page(s).")
    if n == 0:
        print("ERROR: zero pages — check the HTML.", file=sys.stderr)
        return 1
    doc.write_pdf(str(pdf))
    print(f"PDF: {pdf}")

    if args.no_png:
        return 0

    png_dir = Path(args.png_dir).resolve() if args.png_dir else src.parent / "_render"
    png_dir.mkdir(parents=True, exist_ok=True)
    for old in png_dir.glob("page-*.png"):
        old.unlink()

    if shutil.which("pdftoppm"):
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(args.dpi), str(pdf), str(png_dir / "page")],
            check=True,
        )
        # normalize names to page-01.png style
        for p in sorted(png_dir.glob("page-*.png")):
            num = p.stem.split("-")[-1]
            p.rename(png_dir / f"page-{int(num):02d}.png")
    else:
        try:
            from pdf2image import convert_from_path
        except ImportError:
            print("ERROR: neither pdftoppm (poppler-utils) nor pdf2image available.\n"
                  "  apt-get install poppler-utils   OR   pip install pdf2image --break-system-packages",
                  file=sys.stderr)
            return 2
        for i, img in enumerate(convert_from_path(str(pdf), dpi=args.dpi), 1):
            img.save(png_dir / f"page-{i:02d}.png")

    pages = sorted(png_dir.glob("page-*.png"))
    print(f"PNGs: {png_dir} ({len(pages)} pages)")
    print("NOW: Read every page PNG and check it against the SKILL.md visual checklist. No sampling.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
