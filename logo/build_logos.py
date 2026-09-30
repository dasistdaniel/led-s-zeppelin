"""Erzeugt die Pixel-Logo-Konzepte für LED's'Zeppelin als saubere SVGs (ein <path> aus Pixel-Läufen)."""
import math, os

OUT = os.path.join(os.path.dirname(__file__), 'concepts')
os.makedirs(OUT, exist_ok=True)

FONT = {
    'L': '100100100100111', 'E': '111100110100111', 'D': '110101101101110', 'S': '011100010001110',
    'Z': '111001010100111', 'P': '110101110100100', 'I': '111010010010111', 'N': '110101101101101',
    "'": '010010000000000',
}

def runs_path(pixels, u, ox=0, oy=0):
    """pixels: set of (x, y) -> one path from horizontal runs."""
    d = []
    rows = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    for y in sorted(rows):
        xs = sorted(rows[y]); start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x; continue
            d.append(f'M{ox + start * u:g} {oy + y * u:g}h{(prev - start + 1) * u:g}v{u:g}h{-(prev - start + 1) * u:g}z')
            if x is not None: start = prev = x
    return ''.join(d)

def grid(rows):
    return {(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == '#'}

def text_pixels(s, spacing=1):
    px, x = set(), 0
    for ch in s:
        g = FONT[ch]
        for b in range(15):
            if g[b] == '1': px.add((x + b % 3, b // 3))
        x += 3 + spacing
    return px, x - spacing

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" '
            f'shape-rendering="crispEdges"><title>{title}</title>{body}</svg>\n')

def save(name, content):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f: f.write(content)

# ---------- A: LED-Zeppelin — eine liegende LED ist zugleich das Luftschiff ----------
A = set()
for y in range(1, 11):  # Körper: flaches Heck links, runde Kuppel rechts
    for x in range(6, 20):
        if x <= 13 or (x - 13) ** 2 + (y - 5.5) ** 2 <= 5.6 ** 2: A.add((x, y))
for y in range(0, 12): A.add((5, y))          # Sockelrand der LED
for x in range(0, 5): A.add((x, 3))           # langes Bein (Anode)
for x in range(1, 5): A.add((x, 8))           # kurzes Bein (Kathode)
A -= {(15, 3), (16, 3), (16, 4)}              # Glanzlicht in der Kuppel
A |= {(10, 11), (11, 11)} | {(x, 12) for x in range(8, 14)}  # Gondel
A_W, A_H = 20, 13

# ---------- B: Pixel-Wortmarke "LED" mit Glühfaden-Punkt ----------
B, bw = text_pixels('LED')          # 11 x 5
# ---------- C: Abwurf — Luftschiff oben, eine LED fällt, darunter ein Haus mit Licht ----------
C = {(x, y) for y in range(16) for x in range(16) if ((x - 8.5) / 6.6) ** 2 + ((y - 3) / 2.6) ** 2 <= 1}
C |= {(1, 0), (2, 0), (2, 1), (1, 6), (2, 6), (2, 5)}      # Heckflossen
C |= {(8, 6), (9, 6)}                                       # Gondel
C |= {(8, 8), (9, 8)}                                         # fallende LED
roof = {(x, y) for y in range(11, 13) for x in range(16) if abs(x - 8.5) <= (y - 10) * 2.5 + 0.5}
C |= roof | {(x, y) for y in range(13, 16) for x in range(4, 13)}
C -= {(7, 14), (8, 14), (10, 14)}                           # Fenster (leuchtet in Farbe)
C -= {(x, 12) for x in range(16) if abs(x - 8.5) > 3.6}     # Dachkante sauber

U = 16  # 16x16-Raster auf 256er-Canvas
def symbol(name, px, cols, rows, title):
    u = 256 / max(cols, rows) * 0.86
    ox = (256 - cols * u) / 2; oy = (256 - rows * u) / 2
    save(name, svg(256, 256, f'<path fill="#000" d="{runs_path(px, u, ox, oy)}"/>', title))

symbol('a-symbol.svg', A, A_W, A_H, 'LED-Zeppelin')
symbol('b-symbol.svg', B, bw, 5, 'LED Wortmarke')
symbol('c-symbol.svg', C, 16, 16, 'Mond-Emblem')

def lockup(name, px, cols, rows, title):
    u = 256 / 16
    su = 256 / max(cols, rows) * 0.86
    sw = cols * su
    sym = runs_path(px, su, 0, (256 - rows * su) / 2)
    led, lw = text_pixels('LED')
    s_, sw2 = text_pixels("'S'")
    zep_, zw = text_pixels('ZEPPELIN')
    tu = 14; ty = (256 - 5 * tu) / 2
    x0 = sw + 40
    p1 = runs_path(led, tu, x0, ty)
    x1 = x0 + (lw + 1) * tu
    p2 = runs_path(s_, tu * 0.6, x1, ty + 2 * tu)
    x2 = x1 + (sw2 + 1.5) * tu * 0.6
    p3 = runs_path(zep_, tu, x2, ty)
    w = x2 + zw * tu
    body = (f'<path fill="#000" d="{sym}{p1}{p3}"/><path fill="#000" fill-opacity=".25" d="{p2}"/>')
    save(name, svg(w, 256, body, title))

lockup('a-lockup.svg', A, A_W, A_H, "LED's'Zeppelin")
lockup('b-lockup.svg', B, bw, 5, "LED's'Zeppelin")
lockup('c-lockup.svg', C, 16, 16, "LED's'Zeppelin")
print('ok')
