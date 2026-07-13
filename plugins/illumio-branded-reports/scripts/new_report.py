#!/usr/bin/env python3
"""
new_report.py — scaffold a new Illumio branded report (fail-closed).

This is the ONLY sanctioned way to start a report. It copies the canonical
template + styles/ + assets/ into an output folder and fills the cover
placeholders. The generating model then edits ONLY the region between the
SECTIONS START/END markers in the produced report.html.

Fail-closed design: if any canonical asset (logo, fonts, CSS, cover art) is
missing or unreadable, the script REFUSES to scaffold and prints an
ASK-THE-USER message. Never improvise a replacement asset.

Usage:
  python scripts/new_report.py --out ./my-report \
      --title "Guía de Despliegue VEN" \
      --subtitle "Plan de implementación por fases" \
      --author "Nombre – Illumio SE" \
      --date "Julio 2026" [--lang es] [--variant orange|slate|paper] \
      [--classification CONFIDENTIAL] [--footer-contact ""] \
      [--cover-art path/to/art.{svg,png,jpg}] [--force]
"""
from __future__ import annotations

import argparse
import html as html_mod
import shutil
import sys
from datetime import date
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_ASSETS = [
    "template.html",
    "styles/report.css",
    "assets/logo-white.png",
    "assets/logo-dark.png",
    "assets/copy.js",
    "assets/fonts/Montserrat-Light.ttf",
    "assets/fonts/Montserrat-Regular.ttf",
    "assets/fonts/Montserrat-Bold.ttf",
    "assets/fonts/JetBrainsMono-Regular.ttf",
]

VARIANTS = {"orange": "", "slate": "cover--slate", "paper": "cover--paper"}

# Localized disclaimer strings. {author} and {purpose} are filled at scaffold
# time. The disclaimer is ON by default: these documents are self-published
# working guides, not official Illumio publications.
DISCLAIMER = {
    "en": {
        "cover": "Working guide prepared by {author} — not an official Illumio, Inc. publication.",
        "title": "About this document",
        "body": ("This guide was prepared by {author} to {purpose}. It is a working aid for the "
                 "recipient and is not an official publication of Illumio, Inc.; it does not modify "
                 "or replace official product documentation, contractual agreements, or statements "
                 "of work. Validate all technical details against the official documentation for "
                 "your specific product versions before acting on them. Illumio and the Illumio "
                 "logo are trademarks of Illumio, Inc., used here to identify the subject matter."),
        "purpose": "help the recipient clarify the concepts presented",
        "author_fallback": "the author",
    },
    "es": {
        "cover": "Guía de trabajo preparada por {author} — no es una publicación oficial de Illumio, Inc.",
        "title": "Acerca de este documento",
        "body": ("Esta guía fue preparada por {author} para {purpose}. Es un material de apoyo para "
                 "el destinatario y no constituye una publicación oficial de Illumio, Inc.; no "
                 "modifica ni reemplaza la documentación oficial del producto, los acuerdos "
                 "contractuales ni los alcances de trabajo (SOW). Valide todos los detalles técnicos "
                 "contra la documentación oficial correspondiente a sus versiones específicas antes "
                 "de actuar sobre ellos. Illumio y el logotipo de Illumio son marcas de Illumio, "
                 "Inc., utilizadas aquí para identificar el tema tratado."),
        "purpose": "ayudar al destinatario a clarificar los conceptos presentados",
        "author_fallback": "el autor",
    },
    "pt": {
        "cover": "Guia de trabalho preparado por {author} — não é uma publicação oficial da Illumio, Inc.",
        "title": "Sobre este documento",
        "body": ("Este guia foi preparado por {author} para {purpose}. É um material de apoio para o "
                 "destinatário e não constitui uma publicação oficial da Illumio, Inc.; não modifica "
                 "nem substitui a documentação oficial do produto, os acordos contratuais ou os "
                 "escopos de trabalho (SOW). Valide todos os detalhes técnicos na documentação "
                 "oficial correspondente às suas versões específicas antes de agir sobre eles. "
                 "Illumio e o logotipo da Illumio são marcas da Illumio, Inc., utilizadas aqui para "
                 "identificar o tema tratado."),
        "purpose": "ajudar o destinatário a esclarecer os conceitos apresentados",
        "author_fallback": "o autor",
    },
}


def fail_ask_user(missing: list[str]) -> None:
    print("SCAFFOLD BLOCKED — canonical brand assets are missing:\n", file=sys.stderr)
    for m in missing:
        print(f"  MISSING: {m}", file=sys.stderr)
    print(
        "\nDO NOT improvise, redraw, or substitute these files (no text wordmarks,"
        "\nno approximated SVG logos, no alternate fonts, no re-typed CSS)."
        "\nSTOP and ASK THE USER to provide the official file(s), or reinstall the"
        "\nskill (/skill-update). A paused report is always better than an"
        "\noff-brand one.",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--out", required=True, help="Output folder for the report workspace")
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", default="", help="Byline, e.g. 'Name – Illumio SR. SE LATAM'. Never invent one.")
    ap.add_argument("--date", default="", help="Human date, e.g. 'June 2026' / 'Junio 2026'")
    ap.add_argument("--lang", default="en", help="Document language code (en, es, pt…)")
    ap.add_argument("--variant", default="orange", choices=sorted(VARIANTS))
    ap.add_argument("--classification", default="CONFIDENTIAL",
                    help="Cover-footer classification tag; pass '' to omit")
    ap.add_argument("--footer-contact", default="", help="Optional right-side text in the content footer")
    ap.add_argument("--cover-art", default=None,
                    help="Optional right-side cover strip: 'builtin' for the bundled isometric "
                         "pattern, or a path to approved artwork (svg/png/jpg). Default: none — "
                         "plain orange cover.")
    ap.add_argument("--purpose", default=None,
                    help="Document objective inserted into the disclaimer (e.g. 'support the VEN "
                         "deployment planning of <CLIENTE>'). Defaults to a generic clarification aim.")
    ap.add_argument("--disclaimer-text", default=None,
                    help="Full custom disclaimer body (overrides the localized default).")
    ap.add_argument("--no-disclaimer", action="store_true",
                    help="Omit the not-an-official-document disclaimer (cover line + end matter).")
    ap.add_argument("--force", action="store_true", help="Overwrite an existing report.html")
    args = ap.parse_args()

    # ---- Gate: canonical assets must exist (never improvise) -------------
    missing = [rel for rel in REQUIRED_ASSETS if not (SKILL_ROOT / rel).is_file()]
    if missing:
        fail_ask_user(missing)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    dst_html = out / "report.html"
    if dst_html.exists() and not args.force:
        print(f"ERROR: {dst_html} already exists. Use --force to overwrite, or pick another --out.",
              file=sys.stderr)
        return 1

    # ---- Copy canonical styles/ and assets/ ------------------------------
    for sub in ("styles", "assets"):
        dst = out / sub
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(SKILL_ROOT / sub, dst)

    # ---- Cover art is OPT-IN: default is a clean, plain-orange cover ------
    cover_logo = "assets/logo-dark.png" if args.variant == "paper" else "assets/logo-white.png"
    cover_art_block = ""
    cover_art_desc = "none (plain cover)"
    if args.cover_art:
        if args.cover_art.strip().lower() == "builtin":
            cover_art_src = "assets/cover-art.svg"
            cover_art_desc = "builtin isometric pattern"
        else:
            art = Path(args.cover_art).resolve()
            if not art.is_file():
                print(f"ERROR: --cover-art file not found: {art}\n"
                      "ASK THE USER for the correct artwork file. Do not invent one.",
                      file=sys.stderr)
                return 2
            ext = art.suffix.lower()
            if ext not in (".svg", ".png", ".jpg", ".jpeg"):
                print(f"ERROR: unsupported cover-art format {ext} (use svg/png/jpg).", file=sys.stderr)
                return 2
            dest = out / "assets" / f"cover-art-custom{ext}"
            shutil.copy2(art, dest)
            cover_art_src = f"assets/cover-art-custom{ext}"
            cover_art_desc = str(art.name)
        cover_art_block = (f'<div class="cover-art" data-decoration>\n'
                           f'    <img src="{cover_art_src}" alt="">\n  </div>')

    # ---- Fill template placeholders --------------------------------------
    esc = html_mod.escape
    footer_text = esc(args.title) + (f"  ·  {esc(args.subtitle)}" if args.subtitle else "")
    if len(footer_text) > 95:          # keep the @bottom-left footer to one line
        footer_text = esc(args.title)[:95]
    # @page content strings use CSS escaping; keep it plain and quote-safe:
    footer_text_css = footer_text.replace('"', "'")

    # ---- Disclaimer (default ON) ------------------------------------------
    L = DISCLAIMER.get(args.lang.lower()[:2], DISCLAIMER["en"])
    cover_disc = ""
    disc_block = ""
    if not args.no_disclaimer:
        author_name = args.author.strip() or L["author_fallback"]
        purpose = (args.purpose or L["purpose"]).strip().rstrip(".")
        body = args.disclaimer_text or L["body"]
        body = body.replace("{author}", author_name).replace("{purpose}", purpose)
        cover_line = L["cover"].replace("{author}", author_name)
        cover_disc = f'<p class="cover-disclaimer">{esc(cover_line)}</p>'
        disc_block = (f'<div class="disclaimer">\n'
                      f'  <div class="disclaimer-title">{esc(L["title"])}</div>\n'
                      f'  <p>{esc(body)}</p>\n'
                      f'</div>')

    tpl = (SKILL_ROOT / "template.html").read_text(encoding="utf-8")
    repl = {
        "{{TITLE}}": esc(args.title),
        "{{SUBTITLE}}": esc(args.subtitle),
        "{{AUTHOR}}": esc(args.author),
        "{{DATE}}": esc(args.date),
        "{{YEAR}}": str(date.today().year),
        "{{LANG}}": esc(args.lang),
        "{{VARIANT}}": VARIANTS[args.variant],
        "{{COVER_LOGO}}": cover_logo,
        "{{CLASSIFICATION}}": esc(args.classification),
        "{{FOOTER_CONTACT}}": esc(args.footer_contact),
        "{{FOOTER_TEXT}}": footer_text_css,
        "{{COVER_ART}}": cover_art_block,
        "{{COVER_DISCLAIMER}}": cover_disc,
        "{{DISCLAIMER_BLOCK}}": disc_block,
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)

    leftovers = [t for t in ("{{",) if t in tpl]
    if leftovers:
        print("ERROR: unresolved template placeholders remain — template/skill mismatch. "
              "Re-run /skill-update or ask the user.", file=sys.stderr)
        return 2

    dst_html.write_text(tpl, encoding="utf-8")

    print(f"Scaffolded: {dst_html}")
    print(f"  variant={args.variant}  lang={args.lang}  cover-art={cover_art_desc}  "
          f"disclaimer={'off' if args.no_disclaimer else 'on'}")
    print("\nNEXT STEPS (in order):")
    print("  1. Edit ONLY between the SECTIONS START/END markers in report.html")
    print("     (components: references/component-catalog.md; diagrams: references/diagrams-guide.md)")
    print("  2. Verify facts + add official-doc links per references/fact-verification.md")
    print(f"  3. python {SKILL_ROOT / 'scripts' / 'check_brand.py'} {dst_html}")
    print(f"  4. python {SKILL_ROOT / 'scripts' / 'render_report.py'} {dst_html}")
    print(f"  5. python {SKILL_ROOT / 'scripts' / 'visual_verify.py'} {dst_html}")
    print("  6. Read every _render/page-*.png against the SKILL.md visual checklist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
