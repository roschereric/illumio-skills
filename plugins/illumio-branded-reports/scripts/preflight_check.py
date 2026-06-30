#!/usr/bin/env python3
"""
preflight_check.py — MANDATORY resource pre-flight for the illumio-branded-reports skill.
Run FIRST, before generating any document. Verifies the skill is fully present and every
branding resource is USABLE; raises an error (exit 2) with troubleshooting if not, because
a stale/partial skill load silently removes the branding guardrails.
Resolves the skill root relative to this script, or accepts an explicit root as argv[1].
Exit codes: 0 = OK; 2 = FAILED.
"""
from __future__ import annotations
import os, sys, struct

REQUIRED = {
    "template.html":            ("html", 500),
    "styles/report.css":        ("css",  2000),
    "assets/logo-white.png":    ("png",  1000),
    "assets/logo-dark.png":     ("png",  1000),
    "scripts/visual_verify.py": ("py",   500),
}

def _png_ok(path):
    try:
        d = open(path, "rb").read(33)
        return d[:8] == b"\x89PNG\r\n\x1a\n" and all(struct.unpack(">II", d[16:24]))
    except Exception:
        return False

def preflight(skill_root=None, verbose=True):
    if skill_root is None:
        skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    problems = []
    for rel, (kind, minsz) in REQUIRED.items():
        p = os.path.join(skill_root, rel)
        if not os.path.isfile(p):
            problems.append(f"MISSING: {rel}")
        elif os.path.getsize(p) < minsz:
            problems.append(f"TOO SMALL / CORRUPT: {rel} ({os.path.getsize(p)} bytes)")
        elif kind == "png" and not _png_ok(p):
            problems.append(f"INVALID PNG: {rel}")
    if problems:
        bar = "=" * 68
        sys.stderr.write("\n".join([
            bar, "PRE-FLIGHT FAILED - required skill resources missing or unusable.", bar,
            f"skill root: {skill_root}",
            *[" - " + p for p in problems], "",
            "TROUBLESHOOTING:",
            " 1) You are almost certainly on a STALE / PARTIAL copy of the skill.",
            " 2) Run:  /illumio-branded-reports:skill-update   then  /illumio-branded-reports:skill-status",
            " 3) The skill MUST ship: template.html, styles/report.css, assets/logo-white.png,",
            "    assets/logo-dark.png, scripts/visual_verify.py",
            " 4) DO NOT substitute a text wordmark, an invented mark, or system fonts to work",
            "    around missing assets. STOP and restore the skill first.",
            bar, ""]))
        raise SystemExit(2)
    if verbose:
        print(f"PRE-FLIGHT OK - all skill resources present and usable at {skill_root}")
        for rel in REQUIRED:
            print(f"  OK {rel}")
    return skill_root

if __name__ == "__main__":
    preflight(sys.argv[1] if len(sys.argv) > 1 else None)
