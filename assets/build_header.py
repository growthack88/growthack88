#!/usr/bin/env python3
"""Generate the profile header SVGs (dark + light) from one template.

The chart is static on purpose: GitHub serves SVGs as images, and some
viewers never tick animations there. Only the pulse ring animates, and it is
invisible when it doesn't run.

Run from the repo root:  python3 assets/build_header.py
"""
from pathlib import Path

THEMES = {
    "dark": {
        "bg1": "#0b0f14", "bg2": "#0f1a1c", "glow": "#14b8a6", "glow_op": "0.16",
        "ink": "#f5f7fa", "muted": "#9aa7b4", "accent": "#2dd4bf",
        "gold": "#f5c542", "chip": "#151c24", "chip_line": "#2a3440",
        "grid": "#1f2a35",
    },
    "light": {
        "bg1": "#ffffff", "bg2": "#f2f7f6", "glow": "#14b8a6", "glow_op": "0.10",
        "ink": "#0b1220", "muted": "#4b5868", "accent": "#0f766e",
        "gold": "#a16207", "chip": "#ffffff", "chip_line": "#d5dde3",
        "grid": "#e3e9ee",
    },
}

# (label, width) — widths tuned for 15px system sans
CHIPS = [("Egypt · GCC · MENA", 176), ("English + العربية", 168), ("mahmoudomar.com", 168)]

# Growth curve: slow start, inflection, compounding
CURVE = "M0 170 C 60 168, 100 160, 140 140 S 220 70, 300 18"


def chips(c):
    x, out = 64, []
    for label, w in CHIPS:
        out.append(
            f'<rect x="{x}" y="232" width="{w}" height="36" rx="18" fill="{c["chip"]}" stroke="{c["chip_line"]}"/>'
            f'<text x="{x + w / 2}" y="255.5" class="chip" text-anchor="middle">{label}</text>'
        )
        x += w + 12
    return "\n    ".join(out)


def grid(c):
    dots = []
    for gx in range(0, 321, 40):
        for gy in range(0, 181, 30):
            dots.append(f'<circle cx="{gx}" cy="{gy}" r="1.4" fill="{c["grid"]}"/>')
    return "".join(dots)


def svg(c):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="t d">
  <title id="t">Mahmoud Omar — Growth Cofounder and Fractional Head of Growth</title>
  <desc id="d">I build growth machines for founders in Egypt, the GCC and MENA, and as my own products.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.1" r="0.6">
      <stop offset="0" stop-color="{c["glow"]}" stop-opacity="{c["glow_op"]}"/>
      <stop offset="1" stop-color="{c["glow"]}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{c["accent"]}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, "Noto Sans Arabic", "Geeza Pro", Tahoma, sans-serif; }}
    .eyebrow {{ font-size: 15px; font-weight: 600; letter-spacing: 3px; fill: {c["accent"]}; }}
    .name {{ font-size: 58px; font-weight: 800; letter-spacing: -1px; fill: {c["ink"]}; }}
    .ar {{ font-size: 30px; font-weight: 600; fill: {c["muted"]}; }}
    .tag {{ font-size: 22px; fill: {c["muted"]}; }}
    .chip {{ font-size: 15px; font-weight: 600; fill: {c["muted"]}; }}
    .label {{ font-size: 12px; font-weight: 600; letter-spacing: 2px; fill: {c["muted"]}; }}
    .pulse {{ transform-box: fill-box; transform-origin: center; opacity: 0; animation: pulse 2.4s ease-out 1s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: .55; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(3.2); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .pulse {{ animation: none; }}
    }}
  </style>

  <rect width="1200" height="320" fill="url(#bg)"/>
  <rect width="1200" height="320" fill="url(#glow)"/>

  <line x1="64" y1="73" x2="104" y2="73" stroke="{c["accent"]}" stroke-width="2.5" stroke-linecap="round"/>
  <text x="118" y="78" class="eyebrow">GROWTH COFOUNDER · FRACTIONAL HEAD OF GROWTH</text>

  <text x="62" y="148" class="name">Mahmoud Omar<tspan class="ar" dx="20">محمود عمر</tspan></text>

  <text x="64" y="196" class="tag">I build <tspan font-weight="700" fill="{c["ink"]}">growth machines</tspan> — for founders, and as my own products.</text>

  {chips(c)}

  <g transform="translate(820 62)">
    <text x="0" y="-14" class="label">COMPOUNDING, NOT CAMPAIGNS</text>
    {grid(c)}
    <path d="{CURVE} L300 180 L0 180 Z" fill="url(#area)"/>
    <path d="{CURVE}" fill="none" stroke="{c["accent"]}" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="300" cy="18" r="6" fill="{c["gold"]}" class="pulse"/>
    <circle cx="300" cy="18" r="6" fill="{c["gold"]}"/>
  </g>
</svg>
'''


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, palette in THEMES.items():
        (here / f"header-{name}.svg").write_text(svg(palette), encoding="utf-8")
        print(f"wrote assets/header-{name}.svg")
