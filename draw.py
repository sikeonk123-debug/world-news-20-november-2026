#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up 20 Nov 2026.

v3 (21 Nov 2026, 08:00 WIB): final rebuild after the full day ended
everywhere. 35 stories across 7 regions (EUROPE 8, AMERICAS 9, ASIA 4,
MIDDLE EAST 4, WORLD 5, AFRICA 3, OCEANIA 2), 3 hero + 10 secondary
original flat illustrations, numbers strip, pinned dotted world map,
22-story numbered list, DATE CHECK box with 13 dated exclusions,
sources footer. Every story was verified as having happened, or first
been reported, on Friday 20 November 2026; near-misses are named in the
DATE CHECK box. Counts reconcile: 3 hero + 10 secondary + 22 listed =
35; region counts sum to 35. Corrections vs v2: Genoa drone shutdown,
Finland Onkalo licence, the IRGC "four tankers" claim and the Pete Rose
pardon were all 19 Nov or earlier and are excluded; COP31 did NOT close
with a deal on 20 Nov (overtime); the Hormuz mine story is Iran's claim
only. Drawn with Pillow only; no photos, no copied art.

v4 (21 Nov 2026): three fixes vs v3, everything else identical.
(1) Numbers strip rewritten as two rows of three, each number now a
complete mini-story; the bare "175* Nicholls" and "$3.79bn GTA VI"
are gone. (2) Hero 3 is now Asia's AI sell-off, carrying a data table
(Taipei -6.2%, Seoul -5.2%, Tokyo -5.1%, Hong Kong -1.9% — all from
the same AP report); COP31 moves down to secondary slot 6.
(3) Secondary slots 8 and 13 are now hard world news: Kenya drills
its first oil well (Amosing spudded in Turkana on Friday 20 Nov,
Energy CS Wandayi presiding; first oil 1 Dec, 20,000 bpd — reported
by Capital FM, Business Daily Africa, The Star, KBC and People Daily;
no Reuters/AP/AFP/BBC/Al Jazeera wire found, so the card cites
Capital FM) and Italy's general strike (CGIL, Reuters "ROME, Nov 20";
marches in 100+ cities). GTA VI sales and the Anthropic IPO are gone
from the page entirely. Bukele's third-term filing was 19 Nov
(Reuters dateline Nov 19), so it is NOT a story — it joins the DATE
CHECK exclusions instead (now 14). Regions now EUROPE 9, AMERICAS 8, ASIA 4,
MIDDLE EAST 4, WORLD 4, AFRICA 4, OCEANIA 2 = 35.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = (248, 245, 238)
INK = (20, 20, 20)
MUTED = (90, 86, 78)
RED = (166, 27, 27)
NAVY = (18, 34, 64)
RULE = (180, 174, 162)
CARD = (255, 255, 255)
MAPDOT = (158, 168, 180)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, xy, text, fnt, width, fill, spacing=2, max_lines=None):
    """Draw wrapped text; returns y after last line. Warns on overflow."""
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None and len(lines) > max_lines:
        print(f"OVERFLOW: {text[:48]!r} -> {len(lines)} lines (max {max_lines})")
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

def text_h(draw, text, fnt, width, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None and len(lines) > max_lines:
        print(f"OVERFLOW: {text[:48]!r} -> {len(lines)} lines (max {max_lines})")
    return len(lines) * (fnt.size + 2)

# ---------- flat-illustration helpers ----------
def bands(d, box, colors):
    x0, y0, x1, y1 = box
    n = len(colors)
    for i, c in enumerate(colors):
        d.rectangle([x0, y0 + (y1 - y0) * i // n, x1, y0 + (y1 - y0) * (i + 1) // n], fill=c)

def sun(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def cloud(d, x, y, s, color):
    d.ellipse([x, y, x + s, y + s * 0.55], fill=color)
    d.ellipse([x + s * 0.5, y - s * 0.25, x + s * 1.5, y + s * 0.4], fill=color)
    d.ellipse([x + s, y, x + s * 2, y + s * 0.55], fill=color)

def building(d, x, y, w, h, color, win=(255, 214, 90)):
    d.rectangle([x, y, x + w, y + h], fill=color)
    for wy in range(y + 8, y + h - 8, 14):
        for wx in range(x + 6, x + w - 8, 14):
            d.rectangle([wx, wy, wx + 6, wy + 7], fill=win)

def star4(d, cx, cy, r, color):
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
               (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
               (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
               (cx - r * 0.28, cy - r * 0.28)], fill=color)

def palm(d, x, y, s, color):
    d.line([x, y, x + s * 0.12, y - s], fill=color, width=max(2, s // 12))
    for ang in (-70, -35, 0, 35, 70):
        import math
        a = math.radians(ang - 90)
        ex = x + s * 0.12 + math.cos(a) * s * 0.55
        ey = y - s + math.sin(a) * s * 0.45
        d.line([x + s * 0.12, y - s, ex, ey], fill=color, width=max(2, s // 16))

def wave(d, x0, y, x1, color, amp=5, step=14):
    import math
    pts = []
    for x in range(x0, x1 + 1, step):
        pts.append((x, y + amp * math.sin((x - x0) / 22.0)))
    d.line(pts, fill=color, width=2)

# ---------- per-story illustrations ----------
def ill_akvan(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(38, 74, 92), (58, 102, 118), (74, 128, 140)])
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for r in range(58, 8, -10):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300, fill=(235, 240, 242), width=4)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))
    for x in range(x0 + 8, x1 - 4, 18):
        d.line([x, y1 - 26, x - 8, y1 - 8], fill=(200, 220, 228), width=2)
    d.rectangle([x0, y1 - 12, x1, y1], fill=(24, 52, 66))

def ill_kyiv(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(16, 24, 48), (26, 38, 70), (40, 56, 96)])
    for i, (sx, sy) in enumerate([(x0 + 30, y0 + 46), (x0 + 90, y0 + 30), (x0 + 150, y0 + 54)]):
        d.line([sx, sy, sx + 34, sy - 26], fill=(255, 214, 90), width=3)
        d.ellipse([sx + 32, sy - 30, sx + 40, sy - 22], fill=(255, 236, 160))
        cloud(d, sx - 16, sy + 2, 16, (120, 128, 148))
    for bx, bw, bh in [(x0 + 8, 34, 34), (x0 + 48, 26, 48), (x0 + 80, 40, 30), (x0 + 126, 30, 52)]:
        building(d, bx, y1 - bh, bw, bh, (10, 16, 32), win=(255, 190, 90))
    star4(d, x0 + 150, y1 - 58, 16, (255, 140, 40))
    star4(d, x0 + 150, y1 - 58, 8, (255, 220, 120))

def ill_cop31(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(126, 196, 178), (150, 212, 190), (178, 226, 200)])
    sun(d, x0 + 34, y0 + 26, 15, (255, 214, 90))
    cx, cy, r = (x0 + x1) // 2 + 22, (y0 + y1) // 2 + 4, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 180))
    d.ellipse([cx - r + 10, cy - r + 12, cx - r + 34, cy - r + 30], fill=(86, 170, 110))
    d.ellipse([cx + 2, cy + 6, cx + 26, cy + 30], fill=(86, 170, 110))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=90, end=270, fill=(255, 255, 255), width=2)
    for i, c in enumerate([(30, 90, 160), (220, 60, 50), (255, 214, 90), (60, 140, 90)]):
        fx = x0 + 14 + i * 20
        d.line([fx, y1 - 30, fx, y1 - 12], fill=(60, 60, 60), width=2)
        d.rectangle([fx, y1 - 30, fx + 14, y1 - 20], fill=c)
    d.rectangle([x0, y1 - 12, x1, y1], fill=(46, 110, 74))

def ill_talks(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(58, 92, 168), (78, 116, 188), (104, 142, 205)])
    cx, cy = (x0 + x1) // 2, y0 + 40
    import math
    for k in range(12):
        a = math.radians(k * 30)
        sx, sy = cx + 34 * math.cos(a), cy + 30 * math.sin(a)
        star4(d, sx, sy, 6, (255, 214, 90))
    d.ellipse([x0 + 30, y1 - 34, x1 - 30, y1 - 10], fill=(96, 62, 40))
    d.rectangle([x0 + 40, y1 - 46, x0 + 52, y1 - 34], fill=(30, 90, 160))
    d.rectangle([x1 - 52, y1 - 46, x1 - 40, y1 - 34], fill=(200, 40, 40))

def ill_tanker(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(214, 226, 232), (190, 208, 220), (168, 192, 208)])
    sun(d, x0 + 26, y0 + 20, 12, (255, 214, 90))
    d.rectangle([x0, y1 - 34, x1, y1 - 26], fill=(52, 96, 140))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(36, 76, 118))
    wave(d, x0 + 6, y1 - 22, x1 - 6, (220, 235, 242))
    hx, hy = x0 + 30, y1 - 48
    d.polygon([(hx, hy + 22), (hx + 150, hy + 22), (hx + 162, hy + 8), (hx, hy + 8)], fill=(24, 24, 28))
    for i, c in enumerate([(200, 60, 50), (40, 120, 90), (220, 160, 40)]):
        d.rectangle([hx + 16 + i * 30, hy - 8, hx + 40 + i * 30, hy + 8], fill=c)
    d.rectangle([hx + 118, hy - 8, hx + 132, hy + 8], fill=(240, 240, 240))
    star4(d, hx + 60, hy - 2, 8, (255, 140, 40))
    cloud(d, hx + 138, y0 + 4, 14, (140, 140, 140))

def ill_lebanon(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(232, 196, 140), (226, 178, 118), (214, 158, 96)])
    d.ellipse([x0 + 6, y1 - 44, x0 + 90, y1 - 6], fill=(190, 140, 84))
    d.ellipse([x0 + 80, y1 - 52, x1 - 6, y1 - 6], fill=(176, 126, 72))
    star4(d, (x0 + x1) // 2, y0 + 40, 22, (255, 120, 30))
    star4(d, (x0 + x1) // 2, y0 + 40, 11, (255, 220, 120))
    cloud(d, (x0 + x1) // 2 - 8, y0 + 8, 20, (120, 118, 116))
    d.rectangle([x0 + 14, y1 - 22, x0 + 34, y1 - 8], fill=(120, 84, 52))
    d.rectangle([x1 - 40, y1 - 26, x1 - 16, y1 - 8], fill=(120, 84, 52))

def ill_genoa(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(18, 26, 52), (26, 38, 72), (38, 52, 92)])
    star4(d, x0 + 24, y0 + 18, 6, (255, 255, 255))
    star4(d, x0 + 120, y0 + 12, 5, (255, 255, 255))
    d.polygon([(x0 + 10, y1 - 8), (x0 + 70, y1 - 40), (x1 - 70, y1 - 40), (x1 - 10, y1 - 8)], fill=(90, 96, 110))
    d.line([x0 + 24, y1 - 14, x1 - 24, y1 - 14], fill=(255, 214, 90), width=2)
    dx, dy = (x0 + x1) // 2, y0 + 34
    d.rectangle([dx - 12, dy - 3, dx + 12, dy + 3], fill=(30, 30, 34))
    d.line([dx - 16, dy - 8, dx - 16, dy + 8], fill=(30, 30, 34), width=2)
    d.line([dx + 16, dy - 8, dx + 16, dy + 8], fill=(30, 30, 34), width=2)
    for px, py, c in [(dx - 16, dy - 10, (255, 80, 80)), (dx + 16, dy - 10, (80, 255, 120)),
                      (dx - 16, dy + 10, (255, 255, 255)), (dx + 16, dy + 10, (255, 255, 255))]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=c)

def ill_finland(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(214, 226, 232), (196, 210, 218), (178, 194, 206)])
    d.rectangle([x0, y1 - 58, x1, y1 - 40], fill=(150, 118, 84))
    d.rectangle([x0, y1 - 40, x1, y1 - 22], fill=(126, 96, 66))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(102, 78, 52))
    d.rectangle([(x0 + x1) // 2 - 8, y1 - 58, (x0 + x1) // 2 + 8, y1 - 22], fill=(60, 52, 44))
    d.rectangle([(x0 + x1) // 2 - 14, y1 - 50, (x0 + x1) // 2 + 14, y1 - 30], fill=(170, 170, 175))
    d.line([(x0 + x1) // 2 - 14, y1 - 40, (x0 + x1) // 2 + 14, y1 - 40], fill=(90, 90, 95), width=2)
    building(d, x0 + 12, y1 - 78, 34, 20, (90, 96, 110), win=(255, 214, 90))
    sun(d, x0 + 140, y0 + 18, 11, (255, 214, 90))

def ill_nvidia(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(36, 48, 78), (48, 64, 98), (62, 80, 118)])
    cx, cy = (x0 + x1) // 2 - 14, (y0 + y1) // 2
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(16, 20, 30), outline=(255, 214, 90), width=2)
    d.rectangle([cx - 12, cy - 12, cx + 12, cy + 12], fill=(90, 190, 120))
    for i in range(-1, 2):
        for x in (cx - 32, cx + 32):
            d.line([x, cy + i * 14, x + (-6 if x < cx else 6), cy + i * 14], fill=(255, 214, 90), width=2)
        for y in (cy - 32, cy + 32):
            d.line([cx + i * 14, y, cx + i * 14, y + (-6 if y < cy else 6)], fill=(255, 214, 90), width=2)
    gx, gy = x1 - 34, y1 - 30
    d.ellipse([gx - 16, gy - 16, gx + 16, gy + 16], outline=(255, 255, 255), width=3)
    d.line([gx + 12, gy + 12, gx + 24, gy + 24], fill=(255, 255, 255), width=3)

def ill_rose(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(120, 190, 110), (96, 168, 92), (76, 148, 78)])
    d.ellipse([x0 + 10, y1 - 26, x1 - 10, y1 - 12], fill=(60, 128, 64))
    d.rectangle([x0 + 24, y1 - 52, x0 + 30, y1 - 12], fill=(150, 105, 60))
    d.rectangle([x0 + 24, y1 - 56, x0 + 44, y1 - 48], fill=(150, 105, 60))
    bx, by, r = (x0 + x1) // 2 + 26, y0 + 34, 20
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(255, 255, 255), outline=(200, 200, 200), width=1)
    d.arc([bx - r, by - r, bx + r, by + r], start=300, end=60, fill=(200, 40, 40), width=2)
    d.arc([bx - r, by - r, bx + r, by + r], start=120, end=240, fill=(200, 40, 40), width=2)

def ill_gaza(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(222, 232, 238), (206, 220, 230), (188, 206, 220)])
    sun(d, x0 + 24, y0 + 18, 11, (255, 214, 90))
    d.rectangle([x0 + 8, y1 - 30, x1 - 8, y1 - 12], fill=(120, 118, 110))
    tx, ty = x0 + 40, y1 - 52
    d.rectangle([tx, ty, tx + 62, ty + 22], fill=(240, 240, 238), outline=(90, 90, 90), width=1)
    d.rectangle([tx + 62, ty + 6, tx + 84, ty + 22], fill=(200, 70, 50))
    for wx in (tx + 14, tx + 88):
        d.ellipse([wx - 7, ty + 22, wx + 7, ty + 36], fill=(30, 30, 34))
    d.ellipse([tx + 48 - 7, ty + 22, tx + 48 + 7, ty + 36], fill=(30, 30, 34))
    for i, c in enumerate([(190, 150, 90), (150, 120, 80)]):
        d.rectangle([x1 - 44 + i * 4, ty - 16 - i * 12, x1 - 22 + i * 4, ty - 2 - i * 12], fill=c)

def ill_aiselloff(d, box):
    """Hero 3: a visible data table of Friday's Asian index falls."""
    x0, y0, x1, y1 = box
    bands(d, box, [(248, 240, 228), (244, 232, 214), (238, 224, 200)])
    rows = [("TAIPEI", "-6.2%", 6.2), ("SEOUL", "-5.2%", 5.2),
            ("TOKYO", "-5.1%", 5.1), ("HONG KONG", "-1.9%", 1.9)]
    for i, (name, val, v) in enumerate(rows):
        ry = y0 + 12 + i * 24
        d.text((x0 + 12, ry), name, font=font(SANS_B, 12), fill=INK)
        bw = int(120 * v / 6.2)
        d.rectangle([x0 + 118, ry + 2, x0 + 118 + bw, ry + 12], fill=(178, 34, 34))
        d.text((x0 + 118 + bw + 8, ry), val, font=font(SANS_B, 12), fill=(178, 34, 34))
    d.text((x0 + 12, y1 - 16), "index moves, Friday's close", font=font(SANS, 9), fill=MUTED)

def ill_oilrig(d, box):
    """Kenya: an oil derrick on the Turkana savanna."""
    x0, y0, x1, y1 = box
    bands(d, box, [(232, 196, 140), (226, 178, 118), (214, 158, 96)])
    sun(d, x0 + 26, y0 + 16, 10, (255, 214, 90))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(96, 66, 40))
    for tx in (x0 + 8, x0 + 30):
        d.rectangle([tx, y1 - 26, tx + 18, y1 - 10], fill=(70, 74, 80))
        d.ellipse([tx + 2, y1 - 30, tx + 16, y1 - 24], fill=(70, 74, 80))
    bx, top = y1 - 10, y0 + 8
    cx = (x0 + x1) // 2 + 24
    d.line([cx - 26, bx, cx, top], fill=(40, 30, 20), width=3)
    d.line([cx + 26, bx, cx, top], fill=(40, 30, 20), width=3)
    for fy in (bx - 12, bx - 24, bx - 36):
        t = (bx - fy) / (bx - top)
        hw = 26 * (1 - t)
        d.line([cx - hw, fy, cx + hw, fy], fill=(40, 30, 20), width=2)
    d.rectangle([cx - 30, bx - 4, cx + 30, bx], fill=(40, 30, 20))

def ill_strike(d, box):
    """Italy: a strike crowd with placards and the tricolour."""
    x0, y0, x1, y1 = box
    bands(d, box, [(196, 210, 222), (178, 194, 210), (160, 178, 198)])
    fx, fy = x1 - 34, y0 + 8
    d.line([fx, fy, fx, fy + 22], fill=(60, 60, 60), width=2)
    for i, c in enumerate([(0, 146, 70), (255, 255, 255), (205, 33, 42)]):
        d.rectangle([fx + 1 + i * 7, fy, fx + 8 + i * 7, fy + 11], fill=c)
    for px in (x0 + 44, x0 + 108):
        d.line([px, y0 + 26, px, y0 + 44], fill=(60, 60, 60), width=2)
        d.rectangle([px - 9, y0 + 14, px + 9, y0 + 26], fill=(255, 255, 255),
                    outline=(60, 60, 60), width=1)
        d.line([px - 9, y0 + 20, px + 9, y0 + 20], fill=(178, 34, 34), width=2)
    cols = [(178, 34, 34), (24, 34, 52), (60, 140, 90), (220, 160, 40),
            (120, 60, 140), (30, 90, 160), (200, 90, 60)]
    for i, c in enumerate(cols):
        hx = x0 + 16 + i * 22
        d.ellipse([hx - 5, y1 - 26, hx + 5, y1 - 16], fill=(232, 190, 160))
        d.rectangle([hx - 7, y1 - 16, hx + 7, y1 - 8], fill=c)
    d.rectangle([x0, y1 - 8, x1, y1], fill=(110, 110, 108))

def ill_cricket(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(120, 190, 110), (96, 168, 92), (76, 148, 78)])
    d.rectangle([x0 + 30, y1 - 34, x1 - 30, y1 - 12], fill=(210, 190, 150))
    for i in range(3):
        sx = (x0 + x1) // 2 - 10 + i * 10
        d.line([sx, y1 - 40, sx, y1 - 16], fill=(255, 214, 90), width=3)
    d.rectangle([x0 + 20, y1 - 52, x0 + 26, y1 - 20], fill=(190, 140, 80))
    d.rectangle([x0 + 20, y1 - 56, x0 + 44, y1 - 48], fill=(190, 140, 80))
    d.ellipse([x1 - 42, y0 + 18, x1 - 26, y0 + 34], fill=(200, 40, 40))

def ill_chart(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(248, 240, 228), (244, 232, 214), (238, 224, 200)])
    for gy in range(y0 + 14, y1 - 8, 14):
        d.line([x0 + 6, gy, x1 - 6, gy], fill=(214, 204, 186), width=1)
    pts = [(x0 + 14, y0 + 18), (x0 + 52, y0 + 26), (x0 + 82, y0 + 22),
           (x0 + 112, y0 + 40), (x0 + 142, y0 + 48), (x0 + 168, y0 + 66)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=(178, 34, 34), width=3)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(178, 34, 34))
    d.polygon([(pts[-1][0] - 7, pts[-1][1] - 12), (pts[-1][0] + 7, pts[-1][1] - 12),
               (pts[-1][0], pts[-1][1] + 2)], fill=(178, 34, 34))
    d.text((x0 + 12, y1 - 22), "-5%", font=font(SANS_B, 16), fill=(178, 34, 34))

def ill_border(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(196, 210, 222), (178, 194, 210), (160, 178, 198)])
    d.rectangle([x0, y1 - 26, x1, y1], fill=(110, 110, 108))
    d.line([x0 + 8, y1 - 26, x1 - 8, y1 - 26], fill=(240, 240, 240), width=2)
    for bx in (x0 + 24, x0 + 88, x0 + 150):
        d.rectangle([bx, y0 + 18, bx + 6, y1 - 26], fill=(70, 74, 80))
    for i in range(3):
        yb = y0 + 24 + i * 10
        d.rectangle([x0 + 24, yb, x0 + 156, yb + 5], fill=(178, 34, 34) if i % 2 == 0 else (240, 240, 240))
    d.rectangle([x0 + 62, y0 + 8, x0 + 118, y0 + 20], fill=(24, 34, 52))
    d.text((x0 + 67, y0 + 10), "CLOSED", font=font(SANS_B, 10), fill=(255, 255, 255))

ILLS = {
    1: ill_akvan, 2: ill_kyiv, 3: ill_aiselloff, 4: ill_genoa, 5: ill_tanker,
    6: ill_cop31, 7: ill_chart, 8: ill_oilrig, 9: ill_talks, 10: ill_cricket,
    11: ill_border, 12: ill_lebanon, 13: ill_strike,
}

# ---------- story data ----------
# (num, region, topic, source, headline, summary, illustrator)
HEROES = [
    (1, "ASIA", "WEATHER", "IMD",
     "Akvan makes landfall in Odisha",
     "Crosses near Gopalpur at 70-80 km/h; 372,000 evacuated, no deaths reported."),
    (2, "EUROPE", "UKRAINE WAR", "REUTERS",
     "Russia hits Kyiv's bridges",
     "400+ drones and 110 missiles hit three Dnipro bridges overnight; 8 killed."),
    (3, "ASIA", "MARKETS", "REUTERS",
     "Asia's AI sell-off deepens",
     "Friday's tech rout hits Taipei, Seoul, Tokyo and Hong Kong."),
]
SECONDARY = [
    (4, "EUROPE", "POLAND", "AP",
     "Missiles breach Polish air",
     "Three objects cross in; NATO jets scramble."),
    (5, "MIDDLE EAST", "GULF", "REUTERS",
     "Tanker ablaze off Hormuz",
     "UKMTO: projectile hits tanker; Iran mine claim unverified."),
    (6, "WORLD", "CLIMATE", "REUTERS",
     "COP31 misses deadline",
     "Draft drops fossil fuels and $120bn target."),
    (7, "AMERICAS", "MARKETS", "AP",
     "Wall Street plunges",
     "S&P -3.7%, Nasdaq -5.3%; worst week in 18 months."),
    (8, "AFRICA", "ENERGY", "CAPITAL FM",
     "Kenya's first oil well",
     "Amosing spudded in Turkana; first oil due 1 Dec, 20,000 bpd."),
    (9, "EUROPE", "BREXIT", "REUTERS",
     "UK-EU seal reset deal",
     "Food trade, carbon link, youth mobility agreed."),
    (10, "OCEANIA", "CRICKET", "AP",
     "Nicholls 175* lifts NZ to 368",
     "India reply 159/1 on day two; trail by 209."),
    (11, "EUROPE", "SECURITY", "REUTERS",
     "Estonia to shut Russia border",
     "Five crossings close from 1 Dec for six months."),
    (12, "MIDDLE EAST", "LEBANON", "AP",
     "Israel strikes Lebanon again",
     "Artillery and five air strikes hit south and Bekaa."),
    (13, "EUROPE", "STRIKE", "REUTERS",
     "Italy's general strike",
     "CGIL stages a full-day strike; marches in 100+ cities."),
]
LISTED = [
    "Seoul: 111 caught cheating at Suneung exam",
    "Seoul: BTS pass 10bn streams in Japan",
    "Worldwide: World Children's Day marked",
    "Gaza: 94% urgently need shelter, UNRWA says",
    "Paris: de Villepin launches 2027 bid",
    "New York: Rikers Island to close by 2032",
    "Washington: judge blocks $4bn housing revamp",
    "Washington: shutdown warning before Christmas",
    "Worldwide: oil near $93, Bitcoin below $62,000",
    "Kharg: Iran claims 14-tanker convoy test",
    "Sydney: marathon champion banned 3 years",
    "Kyiv: 1,144 children killed or hurt in 2026",
    "Johannesburg: ex-deputy president dies",
    "Conakry: Guinea bans Burkina Faso broadcaster",
    "Brussels: EU approves 1bn-euro arms aid",
    "London: UK pledges 1,000 drones for Kyiv",
    "Buenos Aires: Senate backs disability law",
    "Brasilia: central bank sells $1bn to steady real",
    "Nairobi: US group wins $60bn rare-earth deal",
    "Washington: US sanctions Comancheros, 'Ndrangheta",
    "Washington: Trump threatens data-centre penalties",
    "Antalya: 20 nations push back on draft",
]
REGIONS = [("EUROPE", 9, (36, 84, 160)), ("AMERICAS", 8, (14, 128, 128)),
           ("ASIA", 4, (122, 62, 158)), ("MIDDLE EAST", 4, (178, 44, 44)),
           ("WORLD", 4, (96, 96, 100)), ("AFRICA", 4, (46, 134, 74)),
           ("OCEANIA", 2, (214, 122, 26))]
# numbers strip, two rows of three: each number tells a complete mini-story
NUMBERS_ROW1 = [("372,000", "evacuated before Akvan landfall"),
                ("400+", "drones fired at Kyiv"),
                ("-6.2%", "Taiwan index, Friday's close")]
NUMBERS_ROW2 = [("100,000", "youth visas a year in UK-EU deal"),
                ("1,144", "children killed or hurt in Ukraine, 2026"),
                ("94%", "of Gazans urgently need shelter")]
# map pins: (num, x, y) in map coords; red for 1-3, navy for 4-13
PINS = [(1, 240, 846), (2, 196, 807), (3, 292, 812), (4, 184, 796),
        (5, 217, 838), (6, 196, 824), (7, 71, 823), (8, 240, 868),
        (9, 178, 810), (10, 312, 925), (11, 202, 786), (12, 206, 830),
        (13, 188, 814)]
LAND = [  # ellipses (x0, y0, x1, y1) forming a coarse dotted world map
    (45, 775, 170, 850), (175, 772, 200, 790), (130, 855, 185, 935),
    (185, 790, 235, 825), (190, 830, 250, 920), (235, 780, 310, 850),
    (255, 850, 285, 875), (265, 895, 305, 925), (180, 795, 192, 810),
    (300, 800, 312, 825), (235, 825, 265, 870), (190, 815, 230, 835),
    (165, 795, 195, 820), (205, 830, 235, 860), (185, 775, 205, 800),
    (308, 918, 318, 935),
]

def kicker(d, x, y, num, region, topic, src, width, size=10):
    """Left kicker 'N · REGION · TOPIC', source right; drops the topic when tight."""
    f = font(SANS_B, size)
    sf = font(SANS, size - 1)
    full = f"{num} · {region} · {topic}"
    if d.textlength(full, font=f) + d.textlength(src, font=sf) + 16 > width:
        full = f"{num} · {region}"
    d.text((x, y), full, font=f, fill=RED)
    d.text((x + width - d.textlength(src, font=sf), y), src, font=sf, fill=MUTED)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    X1 = W - M

    # ---- header ----
    d.rectangle([M, 16, 118, 138], fill=RED)
    d.text((30, 22), "NOV", font=font(SANS_B, 22), fill=(255, 255, 255))
    d.text((30, 46), "20", font=font(SERIF_B, 52), fill=(255, 255, 255))
    d.text((30, 106), "FRI · 2026", font=font(SANS_B, 15), fill=(255, 255, 255))
    d.text((134, 20), "THE DAY IN WORLD NEWS", font=font(SANS_B, 15), fill=RED)
    d.text((134, 40), "Friday 20 November 2026", font=font(SERIF_B, 50), fill=INK)
    d.text((134, 100), "Everything on this page happened, or was first reported, on Friday 20 November 2026.",
           font=font(SANS, 15), fill=MUTED)
    for i, line in enumerate(["35 STORIES", "7 REGIONS", "ONE PAGE"]):
        f = font(SANS_B, 19)
        d.text((X1 - d.textlength(line, font=f), 26 + i * 26), line, font=f, fill=INK)
    d.line([M, 144, X1, 144], fill=INK, width=2)

    # ---- region strip ----
    y0, y1 = 150, 174
    total_w = X1 - M
    widths = []
    for name, n, _ in REGIONS:
        widths.append(max(64, int(total_w * n / 35)))
    scale = total_w / sum(widths)
    widths = [int(w * scale) for w in widths]
    widths[-1] += total_w - sum(widths)
    x = M
    for (name, n, col), w in zip(REGIONS, widths):
        d.rectangle([x, y0, x + w - 1, y1], fill=col)
        label = f"{name} {n}"
        f = font(SANS_B, 13)
        if d.textlength(label, font=f) <= w - 8:
            d.text((x + (w - d.textlength(label, font=f)) / 2, y0 + 6), label, font=f, fill=(255, 255, 255))
        else:
            f2 = font(SANS_B, 10)
            d.text((x + (w - d.textlength(name, font=f2)) / 2, y0 + 2), name, font=f2, fill=(255, 255, 255))
            d.text((x + (w - d.textlength(str(n), font=f2)) / 2, y0 + 13), str(n), font=f2, fill=(255, 255, 255))
        x += w

    # ---- numbers strip: two rows of three, each number a full mini-story ----
    y = 182
    d.text((M, y), "THE DAY IN NUMBERS:", font=font(SANS_B, 14), fill=INK)
    nx = M + d.textlength("THE DAY IN NUMBERS:  ", font=font(SANS_B, 14))
    for num, lab in NUMBERS_ROW1:
        f1, f2 = font(SANS_B, 14), font(SANS, 13)
        d.text((nx, y), num, font=f1, fill=RED)
        nx += d.textlength(num + " ", font=f1)
        d.text((nx, y), lab, font=f2, fill=INK)
        nx += d.textlength(lab + "  ·  ", font=f2)
    if nx > X1:
        print(f"OVERFLOW: numbers strip row 1 ends at {nx}, page edge {X1}")
    nx = M
    y2 = y + 17
    for num, lab in NUMBERS_ROW2:
        f1, f2 = font(SANS_B, 14), font(SANS, 13)
        d.text((nx, y2), num, font=f1, fill=RED)
        nx += d.textlength(num + " ", font=f1)
        d.text((nx, y2), lab, font=f2, fill=INK)
        nx += d.textlength(lab + "  ·  ", font=f2)
    if nx > X1:
        print(f"OVERFLOW: numbers strip row 2 ends at {nx}, page edge {X1}")
    d.line([M, 210, X1, 210], fill=RULE, width=1)

    # ---- hero stories ----
    hy, hh = 216, 232
    hw, gap = 312, 20
    for i, (num, region, topic, src, head, summ) in enumerate(HEROES):
        x = M + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=RULE, width=1)
        ILLS[num](d, (x + 1, hy + 1, x + hw - 1, hy + 129))
        ky = hy + 136
        kicker(d, x + 10, ky, num, region, topic, src, hw - 20, size=12)
        y2 = draw_wrapped(d, (x + 10, ky + 18), head, font(SERIF_B, 22), hw - 20, INK, spacing=1, max_lines=2)
        draw_wrapped(d, (x + 10, y2 + 3), summ, font(SANS, 12), hw - 20, MUTED, spacing=1, max_lines=2)

    # ---- secondary stories: 5 columns x 2 rows ----
    sy = 456
    cw, cgap = 187, 10
    ch = 144
    for i, (num, region, topic, src, head, summ) in enumerate(SECONDARY):
        col, row = i % 5, i // 5
        x = M + col * (cw + cgap)
        yy = sy + row * (ch + 8)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=RULE, width=1)
        ILLS[num](d, (x + 1, yy + 1, x + cw - 1, yy + 59))
        ky = yy + 64
        kicker(d, x + 8, ky, num, region, topic, src, cw - 16, size=10)
        y2 = draw_wrapped(d, (x + 8, ky + 14), head, font(SERIF_B, 15), cw - 16, INK, spacing=1, max_lines=2)
        draw_wrapped(d, (x + 8, y2 + 2), summ, font(SANS, 11), cw - 16, MUTED, spacing=1, max_lines=2)

    # ---- map + list ----
    my = 752
    d.line([M, my - 4, X1, my - 4], fill=INK, width=2)
    d.text((M, my), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
    d.text((330, my), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES",
           font=font(SANS_B, 14), fill=INK)
    # dotted map
    mx0, my0, mx1, my1 = M, my + 24, 318, 946
    for gx in range(mx0, mx1, 6):
        for gy in range(my0, my1, 6):
            cx, cy = gx + 3, gy + 3
            if any((cx - (a + c) / 2) ** 2 / (((c - a) / 2) ** 2) +
                   (cy - (b + e) / 2) ** 2 / (((e - b) / 2) ** 2) <= 1
                   for a, b, c, e in LAND):
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=MAPDOT)
    for num, px, py in PINS:
        col = RED if num <= 3 else NAVY
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col, outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9 if num < 10 else 8)
        t = str(num)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f, fill=(255, 255, 255))
    d.text((M, 950), "Red pins: stories 1-3 · dark pins: stories 4-13",
           font=font(SANS, 11), fill=MUTED)
    # numbered list, two columns of 11
    lf = font(SANS, 11)
    for i, item in enumerate(LISTED):
        col = i // 11
        row = i % 11
        lx = 330 + col * 336
        ly = my + 24 + row * 12
        num = 14 + i
        d.text((lx, ly), f"{num}", font=font(SANS_B, 11), fill=RED)
        d.text((lx + 22, ly), item, font=lf, fill=INK)

    # ---- date check box ----
    by0 = 962
    d.rectangle([M, by0, X1, by0 + 46], outline=RED, width=2)
    d.text((M + 10, by0 + 3), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((M + 108, by0 + 3),
           "Left out on purpose — each was first reported before Friday:",
           font=font(SANS, 12), fill=INK)
    d.text((M + 10, by0 + 16),
           "Trilateral Shenzhen (19 Nov) · ICJ Myanmar ruling (19 Nov) · Houthi PIF Tower hit (19 Nov) · Pete Rose pardon (19 Nov)",
           font=font(SANS, 9), fill=MUTED)
    d.text((M + 10, by0 + 26),
           "Nvidia subpoena (19 Nov) · Genoa drone shutdown (19 Nov) · Han Duck-soo verdict (19 Nov) · Somalia expels UAE envoy (19 Nov)",
           font=font(SANS, 9), fill=MUTED)
    d.text((M + 10, by0 + 36),
           "Senate Iran vote (19 Nov) · Finland Onkalo licence (19 Nov) · Fiji drought (19 Nov) · COP31 draft (19 Nov) · IRGC tanker claim (4 Nov) · Bukele files for third term (19 Nov)",
           font=font(SANS, 9), fill=MUTED)
    # ---- footer ----
    d.text((M, 1012), "Sources: Reuters · AP · AFP · BBC · UNICEF · UNRWA · IMD · Yonhap · France 24 · Euronews · ABC · CoinDesk · Mail & Guardian · Capital FM",
           font=font(SANS, 10), fill=MUTED)
    d.text((X1 - d.textlength("Original drawings. Claims attributed, not stated as fact.", font=font(SANS, 10)), 1012),
           "Original drawings. Claims attributed, not stated as fact.", font=font(SANS, 10), fill=MUTED)

    total = len(HEROES) + len(SECONDARY) + len(LISTED)
    rsum = sum(n for _, n, _ in REGIONS)
    print(f"counts: heroes {len(HEROES)} + secondary {len(SECONDARY)} + listed {len(LISTED)} = {total}; regions sum {rsum}")
    assert total == 35 and rsum == 35, "counts do not reconcile to 35"

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, "bytes:", os.path.getsize("entry.png"))

if __name__ == "__main__":
    main()
