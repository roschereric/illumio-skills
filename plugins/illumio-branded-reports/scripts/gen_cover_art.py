#!/usr/bin/env python3
"""
gen_cover_art.py — regenerate assets/cover-art.svg (decorative isometric strip).

Built strictly from the official Illumio Pattern & Shape system (Brand Hub,
Design System > Pattern & Shape): the isometric grid, staggered rhombus dot
patterns, and isometric "container" prisms, on a System Cyan 120 field with
Illumio Orange and Server Slate tones. It is DECORATIVE — not a logo — and
may be replaced with approved storytelling imagery from the brand library
via the cover-art flag of new_report.py.

Deterministic: fixed seed, stable output across runs and Python versions.
Usage:
    python scripts/gen_cover_art.py [--seed 20260712] [--out assets/cover-art.svg]
"""
import argparse
from pathlib import Path

W, H = 560, 2970            # 56mm x 297mm at 10 units/mm (A4-height strip)
SYSCYAN_120 = "#1A2C32"     # official dark background
ORANGE = "#FF5500"          # Illumio Orange
ORANGE_DEEP = "#C43C00"
GOLD = "#FFA22F"            # Circuit Gold 100 (sparing)
SLATE_90 = "#464A4C"
SLATE_100 = "#313638"
SLATE_30 = "#C1C3C3"
SLATE_10 = "#EAEBEB"
WHITE = "#FFFFFF"


class LCG:
    def __init__(self, seed: int):
        self.state = seed & 0x7FFFFFFF

    def rand(self) -> float:
        self.state = (1103515245 * self.state + 12345) & 0x7FFFFFFF
        return self.state / 0x7FFFFFFF


def diamond(cx, cy, w, fill, opacity=1.0):
    """Isometric rhombus (2:1) centered at (cx, cy) with half-width w."""
    h = w / 2
    o = f' opacity="{opacity:.2f}"' if opacity < 1 else ""
    return (f'<polygon points="{cx},{cy - h} {cx + w},{cy} {cx},{cy + h} {cx - w},{cy}" '
            f'fill="{fill}"{o}/>')


def prism(cx, top_y, w, height, top_fill, left_fill, right_fill, opacity=1.0):
    """Isometric container: top rhombus + left/right faces (official 'Containers')."""
    h = w / 2
    o = f' opacity="{opacity:.2f}"' if opacity < 1 else ""
    parts = [
        f'<polygon points="{cx - w},{top_y} {cx},{top_y + h} {cx},{top_y + h + height} '
        f'{cx - w},{top_y + height}" fill="{left_fill}"{o}/>',
        f'<polygon points="{cx + w},{top_y} {cx},{top_y + h} {cx},{top_y + h + height} '
        f'{cx + w},{top_y + height}" fill="{right_fill}"{o}/>',
        diamond(cx, top_y, w, top_fill, opacity if opacity < 1 else 1.0),
    ]
    return "\n".join(parts)


def build(seed: int) -> str:
    rng = LCG(seed)
    el = []

    # --- Isometric rhombus dot grid (staggered), subtle across the field ---
    dx, dy, dot_w = 40, 23, 7
    row = 0
    y = 20
    while y < H - 20:
        x0 = 20 + (dx // 2 if row % 2 else 0)
        x = x0
        while x < W - 10:
            v = rng.rand()
            if v > 0.45:
                # density/color varies by vertical zone
                zone = y / H
                if zone < 0.30:      # upper: orange cluster fading in
                    fill, op = (ORANGE, 0.55 + 0.35 * rng.rand()) if v > 0.72 else (SLATE_30, 0.16)
                elif zone < 0.62:    # middle: sparse pale grid
                    fill, op = (SLATE_10, 0.12) if v > 0.6 else (SLATE_30, 0.08)
                else:                # lower: mixed slate + occasional gold
                    if v > 0.955:
                        fill, op = GOLD, 0.75
                    elif v > 0.7:
                        fill, op = SLATE_10, 0.18
                    else:
                        fill, op = SLATE_30, 0.10
                el.append(diamond(x, y, dot_w, fill, op))
            x += dx
        y += dy
        row += 1

    # --- Thin accent line: hexagon outline, upper third (official accent lines) ---
    el.append(
        '<path d="M 420 620 L 500 574 L 500 482 L 420 436 L 340 482 L 340 574 Z" '
        f'fill="none" stroke="{ORANGE}" stroke-width="2.5" opacity="0.85"/>'
    )
    el.append(
        '<path d="M 452 780 L 520 741 L 520 663" '
        f'fill="none" stroke="{SLATE_30}" stroke-width="2" opacity="0.5"/>'
    )

    # --- Container prisms rising from the lower half (official containers) ---
    gradients = f'''
<defs>
  <linearGradient id="wfade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{WHITE}"/><stop offset="1" stop-color="{SLATE_30}"/>
  </linearGradient>
  <linearGradient id="ofade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_DEEP}"/>
  </linearGradient>
</defs>'''
    base = 2440
    el.append(prism(150, base - 620, 95, 620, ORANGE, ORANGE_DEEP, "url(#ofade)"))
    el.append(prism(345, base - 430, 85, 430, WHITE, SLATE_30, "url(#wfade)"))
    el.append(prism(475, base - 260, 70, 260, SLATE_10, SLATE_100, SLATE_90))
    el.append(prism(255, base - 175, 60, 175, ORANGE, ORANGE_DEEP, ORANGE, 0.92))

    # ground line of pale diamonds under the cluster
    for i, gx in enumerate(range(60, W - 20, 64)):
        el.append(diamond(gx, base + 40 + (10 if i % 2 else 0), 22, SLATE_10, 0.12))

    body = "\n".join(el)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">\n'
        f"<!-- Decorative cover strip built from the official Illumio Pattern and Shape\n"
        f"     system (isometric grid, rhombus pattern, containers, accent lines).\n"
        f"     Generated by scripts/gen_cover_art.py, seed {seed}. Replaceable with\n"
        f"     approved storytelling imagery via the cover-art flag of new_report.py -->\n"
        f'<rect width="{W}" height="{H}" fill="{SYSCYAN_120}"/>\n'
        f"{gradients}\n{body}\n</svg>\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260712)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out = Path(args.out) if args.out else Path(__file__).resolve().parent.parent / "assets" / "cover-art.svg"
    out.write_text(build(args.seed), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
