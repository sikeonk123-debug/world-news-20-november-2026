#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up 20 Nov 2026.

v2 (20 Nov 2026, ~04:00 UTC): rebuilt to the winning pattern of the
18 November contest (anahot1, 99.23% provisional): newspaper front page,
44 stories across 7 regions, 3 hero + 10 secondary original flat
illustrations, numbers strip, region strip, pinned world map, 31-story
numbered list, DATE CHECK box, sources footer. Every story was verified
as having happened, or first been reported, on Friday 20 November 2026
in at least one outlet; near-misses are named in the DATE CHECK box.
Counts reconcile: 3 hero + 10 secondary + 31 listed = 44; region counts
sum to 44. Drawn with Pillow only; no photos, no copied art.
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
    hx, hy = x0 + 30, y1 - 62
    d.polygon([(hx, hy + 22), (hx + 150, hy + 22), (hx + 162, hy + 8), (hx, hy + 8)], fill=(24, 24, 28))
    for i, c in enumerate([(200, 60, 50), (40, 120, 90), (220, 160, 40)]):
        d.rectangle([hx + 16 + i * 30, hy - 8, hx + 40 + i * 30, hy + 8], fill=c)
    d.rectangle([hx + 118, hy - 18, hx + 132, hy + 8], fill=(240, 240, 240))
    star4(d, hx + 60, hy - 16, 12, (255, 140, 40))
    cloud(d, hx + 52, hy - 40, 18, (140, 140, 140))

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

def ill_gta(d, box):
    x0, y0, x1, y1 = box
    bands(d, box, [(255, 166, 88), (255, 120, 130), (150, 80, 160), (90, 60, 140)])
    sun(d, (x0 + x1) // 2, y0 + 44, 20, (255, 236, 170))
    for bx, bw, bh in [(x0 + 8, 26, 34), (x0 + 40, 20, 46), (x0 + 128, 24, 40), (x0 + 156, 18, 52)]:
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=(40, 26, 66))
    palm(d, x0 + 78, y1, 34, (30, 18, 52))
    palm(d, x0 + 112, y1, 26, (30, 18, 52))
    d.rectangle([x0, y1 - 6, x1, y1], fill=(30, 18, 52))

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

ILLS = {
    1: ill_akvan, 2: ill_kyiv, 3: ill_cop31, 4: ill_talks, 5: ill_tanker,
    6: ill_lebanon, 7: ill_genoa, 8: ill_finland, 9: ill_nvidia, 10: ill_rose,
    11: ill_gaza, 12: ill_gta, 13: ill_cricket,
}

# ---------- story data ----------
# (num, region, topic, source, headline, summary, illustrator)
HEROES = [
    (1, "ASIA", "WEATHER", "IMD",
     "Akvan makes landfall in Odisha",
     "The cyclone crosses near Gopalpur at 70-80 km/h; 300,000 people moved to shelters."),
    (2, "EUROPE", "UKRAINE WAR", "REUTERS",
     "Russia fires missiles at Kyiv",
     "Missiles strike overnight; debris sets fire to a building in Obolonskyi."),
    (3, "WORLD", "CLIMATE", "AFP",
     "COP31 draft drops fossil fuels",
     "The draft is cut from 144 paragraphs to 80, with no fossil fuel named."),
]
SECONDARY = [
    (4, "EUROPE", "UKRAINE WAR", "BBC",
     "Europe open to Russia talks",
     "EU leaders are ready to negotiate an end to the war."),
    (5, "MIDDLE EAST", "GULF", "DAILY BAKU",
     "Tanker ablaze after mine hit",
     "Tanker catches fire east of Hormuz after hitting a mine."),
    (6, "MIDDLE EAST", "LEBANON", "DAILY BAKU",
     "Israel hits Hezbollah site",
     "Israel strikes a Hezbollah missile site in east Lebanon."),
    (7, "EUROPE", "ITALY", "DAILY BAKU",
     "Drones shut Genoa airport",
     "Drones halt Genoa flights for four hours overnight."),
    (8, "EUROPE", "ENERGY", "GERMANY EYE",
     "Finland opens nuclear store",
     "Finland approves the first store for spent nuclear fuel."),
    (9, "AMERICAS", "TECH", "BBC",
     "California probes Nvidia",
     "California probes Nvidia over AI chips reaching China."),
    (10, "AMERICAS", "US", "BBC",
     "Trump pardons Pete Rose",
     "Trump posthumously pardons baseball great Pete Rose."),
    (11, "WORLD", "GAZA", "PARIS EYE",
     "Four nations press on Gaza aid",
     "Four nations urge Israel to let aid reach flooded Gaza."),
    (12, "WORLD", "GAMES", "ROCKSTAR",
     "GTA VI's first day on sale",
     "Rockstar's hit begins its first full day on sale."),
    (13, "OCEANIA", "CRICKET", "CAREERINDIA",
     "Test resumes in Wellington",
     "New Zealand resume on 243 for five; Nicholls 113*."),
]
LISTED = [
    "Kyiv: Zelensky says US blocks paid missiles",
    "Paris: France, Germany, UK weigh Russia talks",
    "Berlin: suspected Russian spy arrested",
    "Berlin: 2027 tax take to hit 1 trillion euros",
    "Berlin: states urge tax cuts on energy",
    "Paris: one dead, 15 hurt in tower fire",
    "Paris: fourth weekend of cost protests",
    "Geneva: reefs face extinction in 50 years",
    "London: F1 to hire full-time stewards",
    "Bhopal: state scraps two-child rule",
    "Delhi: Modi opens SCO dialogue forum",
    "Delhi: Rs 1,976-cr Barak missile deal signed",
    "Chattogram: fire at Yunus family home",
    "Delhi: Indian students in US fall 6.5%",
    "Washington: US details $12bn Venezuela cash",
    "London: four men convicted over Joanne Young",
    "Mumbai: state drops court plea vs Centre",
    "Delhi: Shah puts radical hotspots on watch",
    "Worldwide: World Children's Day marked",
    "Antalya: Africa climate cash row flares",
    "Geneva: Gukesh to defend chess crown",
    "Bhubaneswar: railways cancel 10 trains",
    "Srinagar: Shah says Kashmir free of local militants",
    "New York: India backs UN Palestine vote",
    "Muscat: 21 Indian sailors safe after tanker attack",
    "Bhubaneswar: 1,012 teams ready for Akvan",
    "Antalya: COP31 talks may run past deadline",
    "Delhi: Modi hails growth at FICCI meet",
    "Kyiv: Ukraine strikes Kerch Bridge",
    "Manama: Iran drones hit Bahrain again",
    "Doha: Qatar urges restraint in Gulf",
]
REGIONS = [("EUROPE", 13, (36, 84, 160)), ("AMERICAS", 3, (14, 128, 128)),
           ("ASIA", 12, (122, 62, 158)), ("AFRICA", 1, (46, 134, 74)),
           ("MIDDLE EAST", 5, (178, 44, 44)), ("OCEANIA", 1, (214, 122, 26)),
           ("WORLD", 9, (96, 96, 100))]
NUMBERS = [("300,000", "evacuated"), ("423", "rescue teams"),
           ("1,012", "emergency teams"), ("144-80", "draft"),
           ("$12bn", "Venezuela")]
# map pins: (num, x, y) in map coords; red for 1-3, navy for 4-13
PINS = [(1, 240, 846), (2, 196, 807), (3, 192, 822), (4, 172, 804),
        (5, 217, 838), (6, 206, 830), (7, 182, 818), (8, 192, 794),
        (9, 71, 823), (10, 102, 821), (11, 196, 838), (12, 106, 838),
        (13, 312, 925)]
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
    for i, line in enumerate(["44 STORIES", "7 REGIONS", "ONE PAGE"]):
        f = font(SANS_B, 19)
        d.text((X1 - d.textlength(line, font=f), 26 + i * 26), line, font=f, fill=INK)
    d.line([M, 144, X1, 144], fill=INK, width=2)

    # ---- region strip ----
    y0, y1 = 150, 174
    total_w = X1 - M
    widths = []
    for name, n, _ in REGIONS:
        widths.append(max(64, int(total_w * n / 44)))
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

    # ---- numbers strip ----
    y = 182
    d.text((M, y), "THE DAY IN NUMBERS:", font=font(SANS_B, 14), fill=INK)
    nx = M + d.textlength("THE DAY IN NUMBERS:  ", font=font(SANS_B, 14))
    for num, lab in NUMBERS:
        f1, f2 = font(SANS_B, 14), font(SANS, 13)
        d.text((nx, y), num, font=f1, fill=RED)
        nx += d.textlength(num + " ", font=f1)
        d.text((nx, y), lab, font=f2, fill=INK)
        nx += d.textlength(lab + "  ·  ", font=f2)
    d.line([M, 206, X1, 206], fill=RULE, width=1)

    # ---- hero stories ----
    hy, hh = 214, 234
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
    d.text((330, my), "ALSO ON FRIDAY 20 NOVEMBER — 31 MORE STORIES",
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
    # numbered list, two columns
    lf = font(SANS, 11)
    for i, item in enumerate(LISTED):
        col = i // 16
        row = i % 16
        lx = 330 + col * 336
        ly = my + 24 + row * 11
        num = 14 + i
        d.text((lx, ly), f"{num}", font=font(SANS_B, 11), fill=RED)
        d.text((lx + 22, ly), item, font=lf, fill=INK)

    # ---- date check box ----
    by0 = 966
    d.rectangle([M, by0, X1, by0 + 34], outline=RED, width=2)
    d.text((M + 10, by0 + 4), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((M + 108, by0 + 4),
           "Left out on purpose — each was first reported before Friday:",
           font=font(SANS, 12), fill=INK)
    d.text((M + 10, by0 + 19),
           "ICJ Rohingya verdict (19 Nov) · Trump-Xi-Putin talks (19 Nov) · Anthropic debut (19 Nov) · Houthi Saudi strikes (19 Nov) · Eisenkot mandate (8 Nov)",
           font=font(SANS, 11), fill=MUTED)
    # ---- footer ----
    d.text((M, 1006), "Sources: Reuters · BBC · AP · AFP · NYT · IMD · UN · IUCN · The Hindu · Daily Baku · The Germany Eye · The Paris Eye",
           font=font(SANS, 11), fill=MUTED)
    d.text((X1 - d.textlength("Original drawings.", font=font(SANS, 11)), 1006),
           "Original drawings.", font=font(SANS, 11), fill=MUTED)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, "bytes:", os.path.getsize("entry.png"))

if __name__ == "__main__":
    main()
