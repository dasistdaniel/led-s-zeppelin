"""LED's'Zeppelin - finales Logo: das Pixel-Luftschiff.

Erzeugt in logo/:
  symbol.svg            Farbversion (transparent)
  symbol-black.svg      einfarbig schwarz
  symbol-white.svg      einfarbig weiß (für dunkle Flächen)
  icon.svg              Farbversion auf dunkler Kachel (Favicon/App-Icon/Avatar)
  lockup-horizontal.svg Symbol + Schriftzug nebeneinander (für dunklen Grund)
  lockup-stacked.svg    Symbol über Schriftzug (für dunklen Grund)
  social-preview.svg    GitHub Social Preview 1280x640
"""
import os, random

HERE = os.path.dirname(os.path.abspath(__file__))

# PICO-8-Farben wie im Spiel
COL = {
    'r': '#ff004d',  # Heckflossen
    'w': '#c2c3c7',  # Hülle oben
    'W': '#fff1e8',  # Glanz
    's': '#83769c',  # Hülle unten (Schatten)
    'b': '#ab5236',  # Gondel
    'c': '#29adff',  # Gondelfenster
}
NAVY, INK, PINK = '#1a1c2c', '#1d2b53', '#ff77a8'

# 16 x 8: das Luftschiff
SYMBOL = [
    '.r....wwwwww....',
    '.rr.wwwWWwwwww..',
    '..rwwwwwwwwwwww.',
    'rrrwwwwwwwwwwwww',
    '..rssssssssssss.',
    '.rr.ssssssssss..',
    '.r....ssssss....',
    '.......bccb.....',
]
SW, SH = 16, 8
VO = (16 - SH) / 2  # senkrecht zentrieren

FONT = {
    'L': '100100100100111', 'E': '111100110100111', 'D': '110101101101110', 'S': '011100010001110',
    'Z': '111001010100111', 'P': '110101110100100', 'I': '111010010010111', 'N': '110101101101101',
    "'": '010010000000000', 'B': '110101110101110', 'R': '110101110101101', 'G': '011100101101011',
    'A': '010101111101101', 'C': '011100100100011', 'H': '101101111101101', 'T': '111010010010010',
    'U': '101101101101111', 'Ü': '101000101101111', 'K': '101101110101101', 'M': '101111111101101',
    'O': '010101101101010', 'W': '101101111111101', 'F': '111100110100100', 'X': '101101010101101',
    'Y': '101101010010010', 'V': '101101101101010', 'J': '001001001101010', 'Q': '010101101110011',
    '.': '000000000000010', '/': '001001010100100', '-': '000000111000000', ':': '000010000010000',
    ' ': '000000000000000', '!': '010010010000010',
}

def runs(pixels, u, ox=0.0, oy=0.0):
    rows = {}
    for x, y in pixels: rows.setdefault(y, []).append(x)
    d = []
    for y in sorted(rows):
        xs = sorted(rows[y]); a = b = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == b + 1: b = x; continue
            d.append(f'M{ox + a * u:g} {oy + y * u:g}h{(b - a + 1) * u:g}v{u:g}h{-(b - a + 1) * u:g}z')
            if x is not None: a = b = x
    return ''.join(d)

def layers(grid, u, ox=0.0, oy=0.0, mono=None):
    """Ein <path> pro Farbe (oder ein einziger für einfarbig)."""
    by = {}
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch != '.': by.setdefault(mono or COL[ch], set()).add((x, y))
    return ''.join(f'<path fill="{c}" d="{runs(px, u, ox, oy)}"/>' for c, px in by.items())

def text(s, u, ox, oy, col, spacing=1):
    px, x = set(), 0
    for ch in s:
        g = FONT[ch]
        for i in range(15):
            if g[i] == '1': px.add((x + i % 3, i // 3))
        x += 3 + spacing
    return f'<path fill="{col}" d="{runs(px, u, ox, oy)}"/>', (x - spacing) * u

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'shape-rendering="crispEdges"><title>{title}</title>{body}</svg>\n')

def save(name, s):
    with open(os.path.join(HERE, name), 'w', encoding='utf-8') as f: f.write(s)

# ---------- Symbol ----------
U = 14; PAD = 16  # 16*14 + 2*16 = 256
save('symbol.svg', svg(256, 256, layers(SYMBOL, U, PAD, PAD + VO * U), "LED's'Zeppelin"))
save('symbol-black.svg', svg(256, 256, layers(SYMBOL, U, PAD, PAD + VO * U, '#000000'), "LED's'Zeppelin"))
save('symbol-white.svg', svg(256, 256, layers(SYMBOL, U, PAD, PAD + VO * U, '#ffffff'), "LED's'Zeppelin"))

# ---------- Icon: Farbversion auf dunkler Kachel (18x18-Raster, 1 Pixel Rand) ----------
IU = 256 / 18
save('icon.svg', svg(256, 256, f'<rect width="256" height="256" fill="{NAVY}"/>' + layers(SYMBOL, IU, IU, IU + VO * IU), "LED's'Zeppelin"))

# ---------- Favicon: 16x16-Raster pixelgenau, ohne Schein ----------
save('favicon.svg', svg(16, 16, f'<rect width="16" height="16" fill="{NAVY}"/>' + layers(SYMBOL, 1, 0, VO), "LED's'Zeppelin"))

# ---------- Schriftzug: LED gelb, 's' nur angedeutet, ZEPPELIN hell ----------
def wordmark(u, ox, oy):
    a, wa = text('LED', u, ox, oy, '#ffec27')
    su = u * 0.6
    b, wb = text("'S'", su, ox + wa + u, oy + 2 * u, '#3a3458')
    c, wc = text('ZEPPELIN', u, ox + wa + u + wb + u, oy, '#fff1e8')
    return a + b + c, wa + u + wb + u + wc

wm, wmw = wordmark(16, 0, 0)
lx = 256 + 32
save('lockup-horizontal.svg', svg(lx + wmw + 16, 256,
     f'<rect width="{lx + wmw + 16}" height="256" fill="{NAVY}"/>' + layers(SYMBOL, U, PAD, PAD + VO * U)
     + wordmark(16, lx, 88)[0], "LED's'Zeppelin"))
sw_ = wmw + 64
save('lockup-stacked.svg', svg(sw_, 336,
     f'<rect width="{sw_}" height="336" fill="{NAVY}"/>' 
     + layers(SYMBOL, U, (sw_ - 256) / 2 + PAD, 48) + wordmark(16, 32, 208)[0], "LED's'Zeppelin"))

# ---------- Social Preview 1280x640 (Pixel = 8 px, Raster 160x80) ----------
P = 8; GW, GH = 160, 80
random.seed(7)
body = []
bands = ['#0e0f1e', '#12142a', '#1a1c2c', '#1d2040', '#1d2b53', '#2b2555', '#3e2456', '#5a2455', '#7e2553']
GROUND = 72
bh = GROUND / len(bands)
for i, c in enumerate(bands):
    body.append(f'<rect x="0" y="{round(i * bh) * P}" width="1280" height="{(round((i + 1) * bh) - round(i * bh)) * P}" fill="{c}"/>')
    if i < len(bands) - 1:  # Dither-Kante
        y0 = round((i + 1) * bh) - 1
        body.append(f'<path fill="{bands[i + 1]}" d="{runs({(x, y0) for x in range(y0 % 2, GW, 2)}, P)}"/>')
stars = {(random.randrange(GW), random.randrange(44)) for _ in range(70)}
body.append(f'<path fill="#83769c" d="{runs(stars, P)}"/>')
body.append(f'<path fill="#fff1e8" d="{runs(set(random.sample(sorted(stars), 18)), P)}"/>')
# Mond
moon = {(x, y) for x in range(GW) for y in range(GH) if (x - 146) ** 2 + (y - 12) ** 2 <= 6.5 ** 2}
body.append(f'<path fill="#fff1e8" fill-opacity=".06" d="{runs({(x, y) for x in range(GW) for y in range(GH) if (x - 146) ** 2 + (y - 12) ** 2 <= 10 ** 2} - moon, P)}"/>')
body.append(f'<path fill="#fff1e8" d="{runs(moon, P)}"/>')
body.append(f'<path fill="#c2c3c7" d="{runs({(143, 10), (144, 10), (143, 11), (148, 14), (149, 14), (145, 16)}, P)}"/>')
# Skyline hinten
far, x = set(), 0
while x < GW:
    w, h = random.randint(5, 12), random.randint(10, 26)
    far |= {(xx, yy) for xx in range(x, x + w) for yy in range(GROUND - h, GROUND)}
    x += w + random.randint(0, 2)
body.append(f'<path fill="#231d45" d="{runs(far, P)}"/>')
# Häuser vorne, einige beleuchtet
x = 0; houses = []
while x < GW:
    w, h = random.randint(8, 14), random.randint(8, 18)
    houses.append((x, w, h, random.random() < 0.55)); x += w + random.randint(1, 3)
for x0, w, h, lit in houses:
    top = GROUND - h
    col = random.choice(['#5f574f', '#83769c', '#7e2553', '#ab5236', '#1d2b53', '#5f281e', '#008751'])
    if lit: body.append(f'<rect x="{(x0 - 2) * P}" y="{(top - 2) * P}" width="{(w + 4) * P}" height="{(h + 2) * P}" fill="#ffc83c" fill-opacity=".12"/>')
    body.append(f'<rect x="{x0 * P}" y="{top * P}" width="{w * P}" height="{h * P}" fill="{col}"/>')
    wins_on, wins_off = set(), set()
    for wy in range(top + 2, GROUND - 2, 3):
        for wx in range(x0 + 2, x0 + w - 2, 3):
            (wins_on if lit and random.random() < 0.85 else wins_off).add((wx, wy)); (wins_on if lit and random.random() < 0.85 else wins_off).add((wx + 1, wy))
    if wins_on: body.append(f'<path fill="#ffec27" d="{runs(wins_on, P)}"/>')
    if wins_off: body.append(f'<path fill="#12131f" d="{runs(wins_off, P)}"/>')
    if not lit: body.append(f'<rect x="{x0 * P}" y="{top * P}" width="{w * P}" height="{h * P}" fill="#080818" fill-opacity=".45"/>')
body.append(f'<rect x="0" y="{GROUND * P}" width="1280" height="{8 * P}" fill="#1a1c2c"/>')
body.append(f'<rect x="0" y="{GROUND * P}" width="1280" height="{P}" fill="#5f574f"/>')
body.append(f'<path fill="#3a3640" d="{runs({(x, GROUND + 4) for s in range(0, GW, 10) for x in range(s, s + 5)}, P)}"/>')
# Logo groß links, Text rechts
SU = 20  # 16*20 = 320 px breit
lx, ly = 64, 128
body.append(layers(SYMBOL, SU, lx, ly))
tx, ty, tu, su = 424, 160, 16, 9
a, wa = text('LED', tu, tx, ty, '#ffec27')
b, wb = text("'S'", su, tx + wa + 12, ty + 3 * tu, '#3a3458')
zx = tx + wa + 12 + wb + 12
c, wc = text('ZEPPELIN', tu, zx, ty, '#fff1e8')
body.append(f'<rect x="{tx - 8}" y="{ty - 8}" width="{wa + 16}" height="{5 * tu + 16}" fill="#ffec27" fill-opacity=".08"/>')
body.append(text('LED', tu, tx + 4, ty + 4, NAVY)[0] + text('ZEPPELIN', tu, zx + 4, ty + 4, NAVY)[0])
body.append(a + b + c)
body.append(text('BRING DAS LICHT ZURÜCK', 8, tx, 288, PINK)[0])
body.append(text("PIXEL-SHOOT'EM'UP IM BROWSER", 5, tx, 344, '#c2c3c7')[0])
save('social-preview.svg', svg(1280, 640, ''.join(body), "LED's'Zeppelin"))
print('ok')
