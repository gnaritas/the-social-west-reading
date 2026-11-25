#!/usr/bin/env python3
"""og.png 1200x630 — The Social — pine-green plate: dashed brass coaster rings,
huge uppercase geometric wordmark, chips line, address strip in mono."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

PINE = (18, 36, 27); PINE2 = (26, 49, 36)
BRASS = (192, 144, 67); BRASS_HI = (230, 193, 121)
BONE = (244, 238, 227); DIM = (168, 182, 164)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

disp = lambda s: font(["Futura.ttc", "Futura Bold.ttc", "Century Gothic.ttf", "Trebuchet MS Bold.ttf"], s)
mono = lambda s: font(["Menlo.ttc", "Menlo-Bold.ttf", "Courier New.ttf"], s)

img = Image.new("RGB", (W, H), PINE)
d = ImageDraw.Draw(img)

# subtle vertical sheen: lighter pine wedge from top
for yy in range(0, 230):
    a = yy / 230.0
    col = (PINE[0] + int((PINE2[0] - PINE[0]) * (1 - a)), 
           PINE[1] + int((PINE2[1] - PINE[1]) * (1 - a)),
           PINE[2] + int((PINE2[2] - PINE[2]) * (1 - a)))
    d.line([(0, yy), (W, yy)], fill=col)

# dashed brass rings (coaster motif), drawn as tick dashes
def ring(cx, cy, r, ticks, color, w=2):
    import math
    for i in range(ticks):
        a1 = 2 * 3.141592653589793 * i / ticks
        a2 = a1 + 2 * 3.141592653589793 / ticks * 0.55
        steps = 6
        for s in range(steps):
            t1 = a1 + (a2 - a1) * s / steps
            t2 = a1 + (a2 - a1) * (s + 1) / steps
            d.line([(cx + r * math.cos(t1), cy + r * math.sin(t1)),
                    (cx + r * math.cos(t2), cy + r * math.sin(t2))], fill=color, width=w)

ring(1065, 95, 190, 46, (150, 116, 58), 2)     # top-right, bleeds off canvas
ring(1065, 95, 150, 40, (112, 92, 52), 1)
ring(96, 585, 210, 52, (105, 86, 47), 2)       # bottom-left
ring(96, 585, 168, 44, (82, 71, 42), 1)

# thin brass frame
d.rectangle([26, 26, W - 27, H - 27], outline=(120, 96, 48), width=2)

def center_text(y, fnt, txt, color, tracking=0):
    if tracking:
        widths = [d.textlength(c, font=fnt) for c in txt]
        total = sum(widths) + tracking * (len(txt) - 1)
        x = (W - total) / 2
        for c, cw in zip(txt, widths):
            d.text((x, y), c, font=fnt, fill=color)
            x += cw + tracking
    else:
        w = d.textlength(txt, font=fnt)
        d.text(((W - w) / 2, y), txt, font=fnt, color=color)

# eyebrow
center_text(72, mono(20), "643 PENN AVENUE  ·  WEST READING, PENNSYLVANIA", BRASS_HI, 4)

# wordmark
center_text(150, disp(150), "THE SOCIAL", BONE, 12)

# subline
center_text(352, disp(30), "A NEW DRINKS-ONLY BAR", BRASS, 6)
center_text(398, mono(21), "from the owners of Oakbrook Brewing & Taqueria Comalli", DIM, 1)

# chips row
chips = ["OPENING DEC 2026 – JAN 2027", "DRINKS ONLY — NO FOOD SERVICE", "THE OLD WILLOW CREEK HOUSE"]
cf = disp(19)
gap = 26
ws = [d.textlength(c, font=cf) + 36 for c in chips]
total = sum(ws) + gap * (len(chips) - 1)
x = (W - total) / 2
yy = 470
for c, cw in zip(chips, ws):
    d.rounded_rectangle([x, yy, x + cw, yy + 42], 21, outline=(150, 116, 58), width=1)
    d.text((x + 18, yy + 10), c, font=cf, fill=(230, 193, 121))
    x += cw + gap

# footer strip
d.line([(26, 560), (W - 27, 560)], fill=(112, 92, 52), width=1)
center_text(578, mono(18), "THE SOCIAL · WEST READING PA 19611 · TAQUERIACOMALLI@GMAIL.COM", (122, 140, 122), 2)

img.save(OUT, "PNG", optimize=True)
print("og.png", img.size, os.path.getsize(OUT) // 1024, "KB")
