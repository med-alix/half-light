"""Generate the HALF-LIGHT doc diagrams as self-contained SVGs (game palette, dark)."""
import math, os, datetime as dt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "assets", "diagrams")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, LINE = "#14110f", "#1f1a17", "#4a3f37"
TXT, MUTED = "#f1e7dc", "#a8998b"
EMBER, WARDEN, DRIFTER, OUTLAW, HEARTH, ICE = "#e8743b", "#3eb3a8", "#b08ce6", "#d9b44a", "#ffb35c", "#8fb8d8"
FONT = "Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h, self.items = w, h, []
        self.title = title

    def add(self, s):
        self.items.append(s)

    def text(self, x, y, s, size=15, color=TXT, anchor="middle", weight=400, font=FONT, italic=False):
        lines = s.split("\n")
        for i, line in enumerate(lines):
            st = ' font-style="italic"' if italic else ""
            self.add(f'<text x="{x}" y="{y + i * size * 1.3:.1f}" font-family="{font}" font-size="{size}" '
                     f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}"{st}>{esc(line)}</text>')

    def box(self, x, y, w, h, title, sub=None, color=LINE, fill=PANEL, tsize=16):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{color}" stroke-width="1.5"/>')
        if sub:
            self.text(x + w / 2, y + h / 2 - 4, title, tsize, TXT, weight=600)
            self.text(x + w / 2, y + h / 2 + 16, sub, 12.5, MUTED)
        else:
            self.text(x + w / 2, y + h / 2 + 5, title, tsize, TXT, weight=600)

    def arrow(self, pts, color=MUTED, dash=False, width=1.6):
        d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
        ds = ' stroke-dasharray="6 5"' if dash else ""
        mid = {MUTED: "m", EMBER: "e", WARDEN: "w", DRIFTER: "d", OUTLAW: "o", HEARTH: "h"}.get(color, "m")
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{ds} marker-end="url(#a{mid})"/>')

    def label(self, x, y, s, color=MUTED, size=12, anchor="middle"):
        self.text(x, y, s, size, color, anchor=anchor)

    def save(self, name):
        marks = "".join(
            f'<marker id="a{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M1 1 L9 5 L1 9 Z" fill="{c}"/></marker>'
            for k, c in [("m", MUTED), ("e", EMBER), ("w", WARDEN), ("d", DRIFTER), ("o", OUTLAW), ("h", HEARTH)])
        body = "\n".join(self.items)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img">'
               f'<title>{esc(self.title)}</title><defs>{marks}</defs>'
               f'<rect width="{self.w}" height="{self.h}" rx="14" fill="{BG}"/>\n{body}\n</svg>')
        open(os.path.join(OUT, name), "w").write(svg)


# 1. The stack and the closure ------------------------------------------------
s = SVG(1000, 560, "The XEN hyperstructure and the missing closure")
s.text(500, 46, "The hyperstructure and the missing closure", 24, TXT, font=SERIF)
s.text(500, 74, "Each layer rewards one verb. Nobody rewards keeping XEN for the winter, so NXN closes the loop.", 14, MUTED)
s.box(60, 140, 200, 80, "XEN", "mint: time + network growth", DRIFTER)
s.box(400, 140, 200, 80, "DBXen", "burn XEN, earn DXN", EMBER)
s.box(740, 140, 200, 80, "DXN stakers", "earn ETH fees", EMBER)
s.box(740, 330, 200, 80, "NXD", "compounds DXN fees", EMBER)
s.box(330, 330, 340, 90, "Granary  →  NXN", "store XEN now, burn it after AMP = 1", WARDEN, tsize=18)
s.arrow([(260, 180), (396, 180)], DRIFTER); s.label(328, 170, "XEN burned")
s.arrow([(600, 180), (736, 180)], EMBER); s.label(668, 170, "ETH fees")
s.arrow([(840, 220), (840, 326)], EMBER); s.label(852, 278, "buys + stakes DXN", anchor="start")
s.arrow([(160, 220), (160, 375), (326, 375)], WARDEN); s.label(170, 300, "deposits", anchor="start")
s.arrow([(500, 330), (500, 224)], WARDEN); s.label(512, 280, "release after the floor", anchor="start")
s.add(f'<rect x="60" y="460" width="880" height="64" rx="10" fill="none" stroke="{HEARTH}" stroke-width="1.2" stroke-dasharray="5 5"/>')
s.text(500, 488, "HALF-LIGHT, the game layer", 16, HEARTH, weight=600)
s.text(500, 508, "reads the chain and gives every mint, burn, stake and deposit a meaning: territory, rescues, the Reaping", 13, MUTED)
s.save("stack.svg")

# 2. Model map ------------------------------------------------------------------
s = SVG(1000, 640, "Model of XEN, DBXen, NXD, the Granary and the game")
s.text(500, 44, "The model at a glance", 24, TXT, font=SERIF)
s.box(60, 80, 880, 64, "Chain readings", "gas basefee · TWAP prices of XEN, DXN, NXD · DBXen batches burned · Granary store", MUTED)
s.box(60, 200, 230, 76, "XEN mints", "only when reward × price > gas", DRIFTER)
s.box(385, 200, 230, 76, "XEN supply", "+ mints + 2% stake APY − burns", DRIFTER)
s.box(710, 200, 230, 76, "Game", "steers burns and deposits", HEARTH)
s.box(60, 360, 230, 76, "Granary store", "XEN, DXN, NXD deposits", WARDEN)
s.box(385, 360, 230, 76, "DBXen burns", "B ≈ κ·R·p_d / cost", EMBER)
s.box(710, 360, 230, 76, "DXN stakers", "earn the ETH fees", EMBER)
s.box(60, 520, 230, 76, "Release controller", "more when market burns fall", WARDEN)
s.box(385, 520, 230, 76, "DXN emission", "R = 10,000 · 1.002^−n", EMBER)
s.box(710, 520, 230, 76, "NXD vault", "logistic share of DXN", EMBER)
s.arrow([(175, 144), (175, 196)]); s.arrow([(825, 144), (825, 196)]); s.arrow([(500, 144), (500, 196)])
s.arrow([(290, 238), (381, 238)], DRIFTER)
s.arrow([(500, 276), (500, 356)], DRIFTER)
s.arrow([(430, 276), (430, 318), (175, 318), (175, 356)], WARDEN)
s.arrow([(800, 276), (800, 330), (570, 330), (570, 356)], HEARTH, dash=True)
s.arrow([(175, 436), (175, 516)], WARDEN)
s.arrow([(290, 558), (335, 558), (335, 398), (381, 398)], WARDEN)
s.arrow([(500, 436), (500, 516)], EMBER)
s.arrow([(615, 398), (706, 398)], EMBER)
s.arrow([(800, 436), (800, 516)], EMBER)
s.arrow([(870, 520), (870, 440)], EMBER)
s.label(880, 484, "re-stakes", anchor="start")
s.save("model-map.svg")

# 3. Tribes -------------------------------------------------------------------
s = SVG(1000, 730, "The tribes: three verbs and the market between them")
s.text(500, 44, "Three verbs, one fire", 24, TXT, font=SERIF)
s.text(500, 70, "Each tribe is one action of the hyperstructure. None of them survives alone.", 14, MUTED)
cx, cy, R = 500, 385, 190
s.add(f'<circle cx="{cx}" cy="{cy}" r="{R + 100}" fill="none" stroke="{OUTLAW}" stroke-width="1.2" stroke-dasharray="3 7"/>')
s.text(cx, cy + R + 132, "Outlaws circle outside every tribe: mercenaries, raiders of the cold, free rescuers", 13.5, OUTLAW)
pts = {}
for name, ang, col, verb, line1, line2 in [
    ("Embers", -90, EMBER, "burn", "fire now", "attack · war-burns"),
    ("Wardens", 30, WARDEN, "stake + store", "fire later", "defend · Hearth"),
    ("Drifters", 150, DRIFTER, "mint", "new matter", "rescues · trade")]:
    x = cx + R * math.cos(math.radians(ang)); y = cy + R * math.sin(math.radians(ang))
    pts[name] = (x, y)
    s.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="82" fill="{PANEL}" stroke="{col}" stroke-width="2"/>')
    s.text(x, y - 24, name, 19, col, weight=600)
    s.text(x, y - 2, verb, 13, TXT)
    s.text(x, y + 18, f"“{line1}”", 12.5, MUTED, italic=True)
    s.text(x, y + 42, line2, 12, MUTED)
for a, b in [("Embers", "Wardens"), ("Wardens", "Drifters"), ("Drifters", "Embers")]:
    (x1, y1), (x2, y2) = pts[a], pts[b]
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy)
    s.add(f'<line x1="{x1 + dx / L * 88:.0f}" y1="{y1 + dy / L * 88:.0f}" x2="{x2 - dx / L * 88:.0f}" y2="{y2 - dy / L * 88:.0f}" stroke="{LINE}" stroke-width="1.4"/>')
s.add(f'<circle cx="{cx}" cy="{cy + 10}" r="46" fill="#2a1c12" stroke="{HEARTH}" stroke-width="2"/>')
s.text(cx, cy + 6, "Hearth", 15, HEARTH, weight=600)
s.text(cx, cy + 25, "shared fire", 11.5, MUTED)
s.save("tribes.svg")

# 4. Calendar / AMP -----------------------------------------------------------
gen = dt.date(2022, 10, 8)
s = SVG(1000, 460, "XEN's clock: AMP, eras and key dates")
s.text(500, 44, "XEN's clock", 24, TXT, font=SERIF)
x0, x1, y0, y1 = 80, 940, 360, 100
d_end = 3650
X = lambda d: x0 + (x1 - x0) * d / d_end
Y = lambda a: y0 - (y0 - y1) * a / 3000
s.add(f'<rect x="{X(0):.0f}" y="{y1}" width="{X(2999) - X(0):.0f}" height="{y0 - y1}" fill="{EMBER}" opacity="0.07"/>')
s.add(f'<rect x="{X(2999):.0f}" y="{y1}" width="{X(3470) - X(2999):.0f}" height="{y0 - y1}" fill="{DRIFTER}" opacity="0.10"/>')
s.add(f'<rect x="{X(3470):.0f}" y="{y1}" width="{X(d_end) - X(3470):.0f}" height="{y0 - y1}" fill="{WARDEN}" opacity="0.10"/>')
s.text((X(1472) + X(2999)) / 2, y1 + 22, "Creation", 15, EMBER, weight=600)
s.text((X(2999) + X(3470)) / 2, y1 + 22, "Twilight", 15, DRIFTER, weight=600)
s.text((X(3470) + X(d_end)) / 2, y1 + 22, "Long Fire", 15, WARDEN, weight=600)
s.add(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{LINE}"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="{LINE}"/>')
for a in (0, 1000, 2000, 3000):
    s.text(x0 - 10, Y(a) + 4, f"{a:,}", 11.5, MUTED, anchor="end")
s.text(x0 - 10, y1 - 14, "AMP", 12, MUTED, anchor="end")
for yr in range(2023, 2033):
    d = (dt.date(yr, 1, 1) - gen).days
    s.add(f'<line x1="{X(d):.0f}" y1="{y0}" x2="{X(d):.0f}" y2="{y0 + 5}" stroke="{LINE}"/>')
    s.text(X(d), y0 + 20, str(yr), 11.5, MUTED)
pts_ = " ".join(f"{X(d):.1f},{Y(max(3000 - d, 1)):.1f}" for d in range(0, d_end + 1, 25))
s.add(f'<polyline points="{pts_}" fill="none" stroke="{HEARTH}" stroke-width="2.5"/>')
for d, lab, dy, anc in [(1472, "today\nAMP ≈ 1,530", -50, "start"), (1620, "APY floor 2%\n16 Mar 2027", 30, "end"), (2999, "AMP = 1\n~24 Dec 2030", -60, "start"), (3470, "last stars mature\n~Apr 2032", -104, "end")]:
    a = max(3000 - d, 1)
    s.add(f'<circle cx="{X(d):.1f}" cy="{Y(a):.1f}" r="5" fill="{BG}" stroke="{TXT}" stroke-width="1.6"/>')
    s.text(X(d) + (8 if anc == "start" else -10), Y(a) + dy, lab, 12, TXT, anchor=anc)
s.text(500, 420, "AMP falls by 1 per day from 3,000 at genesis (8 Oct 2022). One game season = one 90-day XEN APY step.", 13, MUTED)
s.save("calendar.svg")

# 5. Day loop + season --------------------------------------------------------
s = SVG(1000, 430, "A day and a season in HALF-LIGHT")
s.text(500, 44, "One day = one DBXen cycle · one season = 90 days", 22, TXT, font=SERIF)
steps = [("Dawn", "the sun cools; the chronicle", ICE), ("Council", "tribes plan and vote", DRIFTER),
         ("Action", "burn, claim, deposit, scout", EMBER), ("Dusk", "warmth counted; cold freezes", WARDEN)]
for i, (t, sub, c) in enumerate(steps):
    x = 60 + i * 230
    s.box(x, 90, 190, 76, t, sub, c)
    if i < 3:
        s.arrow([(x + 190, 128), (x + 226, 128)])
s.add(f'<path d="M 820 166 L 820 196 L 155 196 L 155 170" fill="none" stroke="{MUTED}" stroke-width="1.4" stroke-dasharray="4 4" marker-end="url(#am)"/>')
s.label(488, 214, "next cycle")
bx, bw = 60, 880
s.add(f'<rect x="{bx}" y="270" width="{bw * 80 / 90:.0f}" height="46" rx="8" fill="{PANEL}" stroke="{EMBER}" stroke-width="1.4"/>')
s.add(f'<rect x="{bx + bw * 80 / 90 + 6:.0f}" y="270" width="{bw * 10 / 90 - 6:.0f}" height="46" rx="8" fill="#2a1c12" stroke="{HEARTH}" stroke-width="1.6"/>')
s.text(bx + bw * 40 / 90, 299, "Days 1–80: territory war (war-burns, rescues, feeding the Hearth)", 14, TXT)
s.text(bx + bw * 85 / 90 + 3, 299, "Reaping", 14, HEARTH, weight=600)
s.text(bx + bw * 85 / 90 + 3, 340, "days 81–90", 12, MUTED)
s.text(500, 385, "Season end: titles, the season bonus for the warmest tribe, tribe switching window, outer rings reset.", 13, MUTED)
s.save("day-and-season.svg")

# 6. NXN flows ----------------------------------------------------------------
s = SVG(1000, 520, "Where NXN comes from and where it goes")
s.text(500, 44, "NXN: earned by storing and holding, burned by playing", 22, TXT, font=SERIF)
s.box(390, 80, 220, 70, "NXN emission", "1,000 · 1.001^−n per active cycle", HEARTH)
s.box(140, 210, 240, 70, "Depositors (60%)", "Granary deposits · Wardens", WARDEN)
s.box(620, 210, 240, 70, "Territory (40%)", "tribes by hex yield held", EMBER)
s.arrow([(450, 150), (300, 206)], HEARTH); s.arrow([(550, 150), (700, 206)], HEARTH)
sinks = [("Emergency fuel", "1 NXN = 2 warmth"), ("War-burn call", "5 NXN"), ("Sponsor crate", "1 NXN"),
         ("Council banner", "10 NXN / season"), ("Mercenary bounty", "10% burned")]
for i, (t, sub) in enumerate(sinks):
    x = 60 + i * 180
    s.box(x, 360, 160, 64, t, sub, LINE, tsize=14)
s.arrow([(260, 280), (260, 330), (500, 330), (500, 356)], WARDEN)
s.arrow([(740, 280), (740, 330), (500, 330)], EMBER)
s.text(500, 465, "Every in-game NXN cost is burned. Prices adjust each season by (target ÷ actual)^0.5, at most ±25%.", 13, MUTED)
s.text(500, 486, "Stake income from the Granary also buys and burns NXN (50% of it).", 13, MUTED)
s.save("nxn-flows.svg")

# 7. Hex map ------------------------------------------------------------------
s = SVG(1000, 620, "The 37-hex map")
s.text(500, 44, "The map: the Hearth and 36 provinces in three rings", 22, TXT, font=SERIF)
size = 44
def hex_pts(x, y, r):
    return " ".join(f"{x + r * math.cos(math.radians(60 * k + 30)):.1f},{y + r * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
cxm, cym = 420, 340
cells = []
for q in range(-3, 4):
    for r in range(-3, 4):
        if abs(q + r) <= 3:
            ring = max(abs(q), abs(r), abs(q + r))
            x = cxm + size * math.sqrt(3) * (q + r / 2); y = cym + size * 1.5 * r
            cells.append((ring, x, y, q, r))
tribe_of = lambda q, r: [EMBER, WARDEN, DRIFTER][int(((math.degrees(math.atan2(1.5 * r, math.sqrt(3) * (q + r / 2))) + 360 + 90) % 360) // 120)]
for ring, x, y, q, r in cells:
    if ring == 0:
        s.add(f'<polygon points="{hex_pts(x, y, size - 2)}" fill="#3a2414" stroke="{HEARTH}" stroke-width="2"/>')
        s.text(x, y + 5, "Hearth", 12.5, HEARTH, weight=600)
    else:
        col = tribe_of(q, r)
        op = {1: 0.38, 2: 0.24, 3: 0.12}[ring]
        s.add(f'<polygon points="{hex_pts(x, y, size - 2)}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-opacity="0.7" stroke-width="1.2"/>')
lx = 760
for i, (t, sub) in enumerate([("Ring 1 · inner", "cost θ₀·2·H · yield 1 · safest"), ("Ring 2 · middle", "cost θ₀·3·H · yield 2"), ("Ring 3 · outer", "cost θ₀·4·H · yield 3 · freezes first")]):
    y = 150 + i * 70
    s.add(f'<rect x="{lx - 30}" y="{y - 14}" width="18" height="18" rx="3" fill="{MUTED}" fill-opacity="{[0.38, 0.24, 0.12][i] + 0.2}"/>')
    s.text(lx, y, t, 14, TXT, anchor="start", weight=600)
    s.text(lx, y + 19, sub, 12, MUTED, anchor="start")
for i, (t, c) in enumerate([("Embers home sector", EMBER), ("Wardens home sector", WARDEN), ("Drifters home sector", DRIFTER)]):
    y = 390 + i * 30
    s.add(f'<rect x="{lx - 30}" y="{y - 13}" width="18" height="18" rx="3" fill="{c}" fill-opacity="0.6"/>')
    s.text(lx, y, t, 13, TXT, anchor="start")
s.text(lx - 30, 500, "θ₀ = 10 · H = heat (climate × weather)", 12, MUTED, anchor="start")
s.text(lx - 30, 520, "A hex below θ for 3 dusks freezes.", 12, MUTED, anchor="start")
s.save("hex-map.svg")

# 8. Climate and weather signals ----------------------------------------------
s = SVG(1000, 520, "On-chain signals: climate and weather")
s.text(500, 44, "Climate and weather: five on-chain signals", 22, TXT, font=SERIF)
sig = [("AMP", "the sun · structural", HEARTH), ("DXN reward R", "forge disinflation", HEARTH),
       ("Burns per DXN", "forge crowding · activity", ICE), ("New ranks / day", "births · growth", ICE),
       ("NXD burned", "the Core's pulse", ICE)]
for i, (t, sub, col) in enumerate(sig):
    s.box(60, 80 + i * 80, 230, 60, t, sub, col, tsize=15)
s.box(390, 110, 240, 80, "Climate C", "slow: 1 + ½ln(3000/A) + ½ln(10⁴/R)", HEARTH)
s.box(390, 300, 240, 80, "Weather w", "fast: ln(short ÷ long), mean 0", ICE)
s.box(730, 110, 210, 80, "Game heat", "C × 2^(−w)", EMBER)
s.box(730, 300, 210, 80, "Granary release", "fills dips (burn signal only)", WARDEN)
s.arrow([(290, 110), (340, 110), (340, 140), (386, 140)], HEARTH)
s.arrow([(290, 190), (340, 190), (340, 160), (386, 160)], HEARTH)
s.arrow([(290, 270), (340, 270), (340, 325), (386, 325)])
s.arrow([(290, 350), (386, 350)])
s.arrow([(290, 430), (340, 430), (340, 365), (386, 365)])
s.arrow([(630, 150), (726, 150)], HEARTH)
s.arrow([(630, 320), (680, 320), (680, 170), (726, 170)])
s.arrow([(630, 350), (726, 350)], WARDEN)
s.text(500, 488, "Only costly signals (burns) move money. Cheap ones (rank claims, NXD pulse) only change the game's mood.", 13, MUTED)
s.save("signals.svg")

# 9. Hybrid release ------------------------------------------------------------------
s = SVG(1000, 560, "Hybrid release: allowance, Hearth-lighting auction, small reserve")
s.text(500, 44, "Hybrid release: the market lights the Hearth, a small reserve covers the rest", 20, TXT, font=SERIF)
s.box(60, 90, 260, 80, "Allowance this cycle", "½·gap (any era) + annuity (after floor)", WARDEN)
s.box(370, 90, 260, 80, "Hearth-lighting auction", "caller share rises 10% → 100% in 24 h", HEARTH)
s.box(680, 90, 260, 80, "Caller", "pays DBXen fee, keeps its share of DXN", OUTLAW)
s.box(370, 260, 260, 80, "Unsold lots", "auction found no taker today", LINE)
s.box(60, 260, 260, 80, "Small reserve (escrow)", "ETH from deposit energy fees", ICE)
s.box(370, 430, 260, 80, "DBXen burn", "only on cycles others also burn", EMBER)
s.arrow([(320, 130), (366, 130)], WARDEN)
s.arrow([(630, 130), (676, 130)], HEARTH)
s.arrow([(500, 170), (500, 256)], MUTED)
s.arrow([(366, 300), (324, 300)], MUTED)
s.arrow([(190, 340), (190, 470), (366, 470)], ICE)
s.arrow([(810, 170), (810, 470), (634, 470)], OUTLAW)
s.text(830, 330, "3 lots per cycle", 12.5, MUTED, anchor="start")
s.text(205, 400, "pays only what", 12.5, MUTED, anchor="start")
s.text(205, 418, "the market won't", 12.5, MUTED, anchor="start")
s.text(500, 540, "Before the floor only stake yield can be released; deposits are untouchable. Unsold allowance carries over up to 7 cycles.", 12.5, MUTED)
s.save("release-controller.svg")

print("diagrams ok")

# 8. Charts with matplotlib ------------------------------------------------------
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.facecolor": BG, "figure.facecolor": BG, "axes.edgecolor": LINE, "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TXT, "axes.grid": True,
                     "grid.color": "#2b2420", "grid.linewidth": 0.6, "legend.frameon": False})

# DXN emission and post-floor burns
fig, ax = plt.subplots(figsize=(9, 4.2))
days = np.arange(0, 2200)
n0 = 1150
R = 10000 * 1.002 ** -(n0 + days)
years = np.array([dt.date(2026, 10, 19) + dt.timedelta(int(d)) for d in days])
ax.plot(years, R / R[0], color=EMBER, lw=2.4, label="DXN reward per cycle (daily burns)")
for e, c in [(0.5, HEARTH), (0.7, DRIFTER), (1.0, ICE)]:
    ax.plot(years, (R / R[0]) ** e, color=c, lw=1.4, ls="--", label=f"burn flow if ε = {e}")
floor = dt.date(2030, 12, 24)
ax.axvline(floor, color=MUTED, lw=1, ls=":"); ax.text(floor, 0.55, "  AMP = 1", color=MUTED)
ax.set_ylabel("relative to today"); ax.set_ylim(0, 1.02)
ax.set_title("DBXen after the floor: emission falls ~20×; burns fall by (1/20)^ε", color=TXT, loc="left", fontsize=12.5)
ax.legend(loc="upper right", fontsize=9.5)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "dxn-emission.svg")); plt.close(fig)

# XEN reward per mint vs AMP
fig, ax = plt.subplots(figsize=(9, 4.2))
d = np.arange(0, 3650)
A = np.maximum(3000 - d, 1)
dates = np.array([gen + dt.timedelta(int(x)) for x in d])
ax.semilogy(dates, 19.93 * A * 470, color=DRIFTER, lw=2.2)
ax.axhline(19.93 * 470, color=MUTED, lw=1, ls=":")
ax.text(dates[50], 19.93 * 470 * 1.5, "floor: ~9,400 XEN per max-term mint, forever (paid for waiting + network growth)", color=MUTED, fontsize=9.5)
ax.axvline(dt.date(2026, 10, 19), color=LINE, lw=1, ls=":"); ax.text(dt.date(2026, 10, 19), 3e7, " today", color=MUTED)
ax.set_ylabel("XEN per mint (470 days, Δ = 1M)")
ax.set_title("A max-term XEN mint: ~14M today, ~9,400 after AMP = 1", color=TXT, loc="left", fontsize=12.5)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "xen-mint-reward.svg")); plt.close(fig)
print("charts ok")
