#!/usr/bin/env python3
"""
check_brand.py — deterministic brand-integrity gate for Illumio reports.

Run AFTER writing report content and BEFORE rendering the PDF:

    python <skill>/scripts/check_brand.py path/to/report.html

Exit codes:
    0  PASS (warnings allowed)
    1  FAIL — one or more brand invariants violated; fix and re-run
    2  script/setup error

What it enforces (stdlib only, no browser needed):
  A. styles/report.css exists next to the HTML and is byte-identical to the
     skill's canonical CSS (hash check). "FORKED-CSS" marker downgrades to WARN.
  B. Logos exist and are byte-identical to the official assets — catches
     regenerated/approximated logos, the #1 brand failure.
  C. Bundled fonts present (no silent fallback typography).
  D. HTML invariants: single stylesheet link; no external CSS/font URLs;
     no base64 images; cover uses the official logo; every section has a
     header with logo + label; no <style> other than doc-overrides (size-capped);
     no CSS filter on logos; no leftover {{placeholders}}; exactly one <h1>.
  E. Content hygiene: warns on AI-speech patterns and on sections that look
     fact-heavy but cite no official documentation (.ref-list).

If a check FAILS because an official asset is missing: STOP and ASK THE USER
for the file. Never substitute or redraw brand assets.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

CANONICAL = {
    "styles/report.css": SKILL_ROOT / "styles" / "report.css",
    "assets/logo-white.png": SKILL_ROOT / "assets" / "logo-white.png",
    "assets/logo-dark.png": SKILL_ROOT / "assets" / "logo-dark.png",
    "assets/copy.js": SKILL_ROOT / "assets" / "copy.js",
}
FONT_SENTINELS = [
    "assets/fonts/Montserrat-Light.ttf",
    "assets/fonts/Montserrat-Regular.ttf",
    "assets/fonts/Montserrat-Bold.ttf",
    "assets/fonts/JetBrainsMono-Regular.ttf",
]

AI_PATTERNS = [
    r"\bleverag(e|es|ed|ing)\b", r"\butiliz(e|es|ed|ing)\b", r"\bin order to\b",
    r"\bdelv(e|es|ing)\b", r"\bseamless(ly)?\b", r"\bgame.chang", r"\bcutting.edge\b",
]

FACT_HINTS = re.compile(
    r"(version|versión|port|puerto|TCP|UDP|CLI|API|PowerShell|cmdlet|servicio|service"
    r"|VEN|PCE|SecureConnect|enforcement|24\.\d|25\.\d|Windows Server|RHEL|Ubuntu)", re.I)


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    html_path = Path(sys.argv[1]).resolve()
    if not html_path.is_file():
        print(f"ERROR: {html_path} not found", file=sys.stderr)
        return 2
    base = html_path.parent
    html = html_path.read_text(encoding="utf-8", errors="replace")

    fails: list[str] = []
    warns: list[str] = []

    # ---- A/B: canonical files present and untampered ----------------------
    for rel, canon in CANONICAL.items():
        local = base / rel
        if not canon.is_file():
            fails.append(f"Skill install is missing canonical {rel} — run /skill-update "
                         f"or ASK THE USER for the official file. Never improvise it.")
            continue
        if not local.is_file():
            fails.append(f"{rel} missing next to the HTML. Re-scaffold with scripts/new_report.py "
                         f"(it copies styles/ and assets/). Do NOT hand-create it.")
            continue
        if sha256(local) != sha256(canon):
            head = local.read_text(encoding="utf-8", errors="replace")[:600] if rel.endswith(".css") else ""
            if rel.endswith(".css") and "FORKED-CSS" in head:
                warns.append(f"{rel} differs from canonical (declared FORKED-CSS — other-brand fork).")
            elif rel.endswith(".css"):
                fails.append(f"{rel} was modified. The stylesheet is READ-ONLY; put per-document "
                             f"tweaks in <style id=\"doc-overrides\"> instead, then restore the "
                             f"canonical file (re-run new_report.py --force or re-copy styles/).")
            elif rel.endswith(".js"):
                fails.append(f"{rel} was modified — it is canonical. Restore it from the skill "
                             f"(re-run new_report.py --force or re-copy assets/).")
            else:
                fails.append(f"{rel} does NOT match the official asset (byte-level). A regenerated/"
                             f"approximated logo is a brand violation — restore the official file "
                             f"from the skill's assets/ or ASK THE USER for it.")

    for rel in FONT_SENTINELS:
        if not (base / rel).is_file():
            fails.append(f"Bundled font missing: {rel} — typography would silently fall back. "
                         f"Re-copy assets/ from the skill (new_report.py does this).")

    # ---- D: HTML invariants ------------------------------------------------
    if len(re.findall(r'<link[^>]+href="styles/report\.css"', html)) != 1:
        fails.append('Exactly one <link rel="stylesheet" href="styles/report.css"> is required.')

    for m in re.finditer(r'<link[^>]+href="(https?://[^"]+)"', html):
        fails.append(f"External stylesheet/font link forbidden (render must be offline-safe): {m.group(1)}")
    if "fonts.googleapis.com" in html or "fonts.gstatic.com" in html:
        fails.append("Google Fonts reference found — fonts are bundled in assets/fonts; remove the link.")

    if re.search(r'src="data:image/', html):
        fails.append("Base64 <img> found — reference files in assets/ instead (keeps HTML light).")

    # scripts: exactly the canonical copy.js include; nothing else, no inline JS
    scripts = re.findall(r'<script\b[^>]*>', html)
    for s in scripts:
        if 'src="assets/copy.js"' not in s:
            fails.append(f"Unexpected <script> tag ({s[:70]}…) — only the canonical "
                         f'<script src="assets/copy.js" defer></script> is allowed.')
    if not any('src="assets/copy.js"' in s for s in scripts):
        warns.append("assets/copy.js include missing — code blocks won't get Copy buttons in the "
                     "HTML view. Scaffold with new_report.py to get the canonical head.")

    styles = re.findall(r'<style\b([^>]*)>(.*?)</style>', html, re.S)
    for attrs, body in styles:
        if 'id="doc-overrides"' not in attrs:
            fails.append("A <style> block other than doc-overrides was found — move rules to "
                         "<style id=\"doc-overrides\"> (per-doc) or drop them; report.css is canonical.")
        elif len(body) > 2600:
            fails.append(f"doc-overrides block too large ({len(body)} chars > 2600). It is for small "
                         f"per-document print tweaks, not a stylesheet.")

    cover = re.search(r'class="cover[^"]*"(.*?)<!-- =+ CONTENT', html, re.S)
    cover_html = cover.group(1) if cover else ""
    if not cover:
        fails.append('No <div class="cover"> found before the content wrap.')
    else:
        if not re.search(r'<img src="assets/logo-(white|dark)\.png" alt="Illumio">', cover_html):
            fails.append("Cover must use the official logo file "
                         '(<img src="assets/logo-white.png" alt="Illumio"> on orange/slate, '
                         "logo-dark.png on paper variant). No inline SVG or text wordmarks.")
        logo_div = re.search(r'class="cover-logo"(.*?)</div>', cover_html, re.S)
        if logo_div and re.search(r'<(svg|span)\b', logo_div.group(1)):
            fails.append("cover-logo contains <svg>/<span> — approximated wordmarks are forbidden; "
                         "use the official PNG assets only.")

    # split on exact section divs (NOT .section-header, which shares the prefix)
    sections = re.split(r'<div class="section"[^>]*>', html)[1:]
    for i, sec in enumerate(sections, 1):
        if '<div class="section-header">' not in sec:
            fails.append(f"Section #{i} lacks .section-header (feeds the running page header).")
        elif 'src="assets/logo-dark.png"' not in sec.split("</div>")[0]:
            fails.append(f"Section #{i} header must use assets/logo-dark.png (official dark logo).")
        if '<span class="section-label">' not in sec:
            fails.append(f"Section #{i} lacks .section-label (running-header text).")

    if re.search(r'{{\s*[A-Z_]+\s*}}', html):
        fails.append("Unresolved {{PLACEHOLDER}} tokens remain — fill them (new_report.py flags).")
    if "<DOCUMENT TITLE>" in html or "<PLACEHOLDER" in html:
        warns.append("Explicit <PLACEHOLDER> markers present — confirm they are intentional "
                     "(values the user must supply) before delivery.")

    h1_count = len(re.findall(r'<h1[\s>]', html))
    if h1_count != 1:
        fails.append(f"Expected exactly one <h1> (cover title); found {h1_count}.")

    if re.search(r'<img[^>]+logo[^>]+style="[^"]*filter\s*:', html):
        fails.append("CSS filter on a logo <img> — WeasyPrint does not propagate filters into "
                     "images; use the correct official variant file instead.")

    if 'class="disclaimer"' not in html and 'class="cover-disclaimer"' not in html:
        warns.append("No not-an-official-document disclaimer found (cover line + end matter). "
                     "It is ON by default in new_report.py — confirm the user explicitly asked "
                     "to omit it (--no-disclaimer).")

    # ---- E: content hygiene (warnings) ------------------------------------
    text = re.sub(r"<[^>]+>", " ", html)
    for pat in AI_PATTERNS:
        n = len(re.findall(pat, text, re.I))
        if n:
            warns.append(f"AI-speech pattern /{pat}/ appears {n}x — rewrite in plain language.")

    if sections:
        fact_secs = [i for i, sec in enumerate(sections, 1)
                     if FACT_HINTS.search(re.sub(r"<[^>]+>", " ", sec))]
        no_refs = [i for i in fact_secs if 'class="ref-list"' not in sections[i - 1]]
        if no_refs and 'class="ref-list"' not in html:
            warns.append(f"No .ref-list anywhere, but sections {no_refs} look fact-heavy — add official "
                         f"documentation sources (references/fact-verification.md).")
        elif no_refs:
            warns.append(f"Sections {no_refs} state technical facts without a .ref-list sources block — "
                         f"add official-doc links or confirm the facts are covered elsewhere on the page.")

    # ---- report ------------------------------------------------------------
    for w in warns:
        print(f"WARN: {w}")
    if fails:
        print(f"\nBRAND CHECK FAILED — {len(fails)} violation(s):\n")
        for i, f in enumerate(fails, 1):
            print(f"  {i}. {f}")
        print("\nFix the violations and re-run. If an official asset is unavailable, "
              "STOP and ASK THE USER — never substitute brand assets.")
        return 1
    print(f"BRAND CHECK PASSED ({len(warns)} warning(s)). Proceed to render_report.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
