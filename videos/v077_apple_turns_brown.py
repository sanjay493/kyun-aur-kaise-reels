import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a cut apple turn brown?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
RED, FLESH, BROWN, SEED = (210, 40, 50), (250, 240, 200), (170, 110, 50), (90, 55, 30)
O2, ENZ, LEMON = (130, 200, 255), (255, 120, 170), (250, 225, 70)


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def half_apple(d, x, y, s=1.0, brown=0.0):
    r = 220 * s
    d.ellipse([x - r, y - r * 0.92, x + r, y + r * 0.92], fill=RED)
    d.ellipse([x - r + 22 * s, y - r * 0.92 + 22 * s, x + r - 22 * s, y + r * 0.92 - 22 * s],
              fill=mix(FLESH, BROWN, brown))
    for dx, dy in ((-30, -20), (30, -20), (0, 30)):
        d.ellipse([x + dx * s - 12 * s, y + dy * s - 20 * s, x + dx * s + 12 * s, y + dy * s + 20 * s], fill=SEED)
    d.line([(x, y - r * 0.92 - 50 * s), (x + 10 * s, y - r * 0.92 + 10 * s)], fill=SEED, width=int(12 * s))


def s1(img, d, t, T, th):
    b = ease(prog(t, 0.4, 1.8))
    half_apple(d, 540, 700, 1.3, b)
    text_c(d, (540, 320), "fresh" if b < 0.5 else "brown!", font(64, "bold"), th["accent"] if b < 0.5 else BROWN)
    if t > 2.0:
        text_c(d, (540, 1100), "Why?", font(72, "bold"), WHITE)


def cell(d, x, y, r, broken, col=(200, 240, 200)):
    if broken:
        d.arc([x - r, y - r, x + r, y + r], 30, 300, fill=col, width=8)
    else:
        d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=8)


def s2(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.8))
    # knife sweeping down
    kx = 540
    ky = 380 + 360 * k
    d.polygon([(kx - 260, ky - 30), (kx + 200, ky - 30), (kx + 260, ky + 10), (kx - 260, ky + 10)], fill=(210, 215, 225))
    d.rounded_rectangle([kx - 420, ky - 40, kx - 250, ky + 20], 14, fill=(110, 70, 40))
    for i in range(4):
        x = 270 + i * 180
        cell(d, x, 850, 70, k > 0.7)
        if k > 0.7:
            for j in range(3):
                a = t * 2 + j * 2 + i
                text_c(d, (x + 90 + 20 * math.cos(a), 800 + j * 40), "•", font(40, "sym"), ENZ)
    if t > 1.1:
        text_c(d, (540, 1050), "enzyme: polyphenol oxidase", font(46, "semi"), ENZ)
        text_c(d, (540, 1120), "+ oxygen from the air", font(46, "semi"), O2)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.4))
    d.rounded_rectangle([110, 420, 470, 560], 40, fill=ENZ)
    text_c(d, (290, 490), "enzyme", font(int(56 * g) + 1, "bold"), DARK)
    text_c(d, (540, 490), "+", font(70, "sym"), WHITE)
    d.rounded_rectangle([610, 420, 970, 560], 40, fill=O2)
    text_c(d, (790, 490), "oxygen", font(int(56 * g) + 1, "bold"), DARK)
    if t > 0.7:
        text_c(d, (540, 650), "↓", font(90, "sym"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.45))
        d.rounded_rectangle([150, 760, 930, 920], 60, fill=BROWN)
        text_c(d, (540, 840), "brown melanins", font(int(66 * g2) + 1, "bold"), WHITE)
    if t > 1.5:
        text_c(d, (540, 1040), "“enzymatic browning”", font(50, "semi"), th["accent"])


def s4(img, d, t, T, th):
    items = [("banana", (250, 220, 80)), ("potato", (220, 190, 130)), ("brinjal", (110, 60, 130))]
    for i, (name, col) in enumerate(items):
        if t > 0.2 + i * 0.4:
            g = pop(prog(t, 0.2 + i * 0.4, 0.4))
            x = 220 + i * 320
            r = 110 * g + 1
            d.ellipse([x - r, 650 - r, x + r, 650 + r], fill=col)
            b = ease(prog(t, 0.6 + i * 0.4, 1.0))
            ri = r * 0.6
            d.ellipse([x - ri, 650 - ri, x + ri, 650 + ri], fill=mix(FLESH, BROWN, b))
            text_c(d, (x, 830), name, font(48, "bold"), WHITE)
    text_c(d, (540, 340), "Same reaction!", font(64, "bold"), th["accent"])


def s5(img, d, t, T, th):
    half_apple(d, 380, 720, 0.85, 0.05)
    # lemon squeezing drops
    d.ellipse([560, 380, 800, 540], fill=LEMON)
    for i in range(3):
        y = 560 + ((t * 300 + i * 90) % 220)
        d.ellipse([440 + i * 25, y - 12, 460 + i * 25, y + 12], fill=LEMON)
    # fridge
    d.rounded_rectangle([760, 620, 960, 1000], 24, fill=(220, 230, 240))
    d.line([(760, 760), (960, 760)], fill=(150, 160, 175), width=6)
    d.line([(930, 680), (930, 730)], fill=(120, 130, 150), width=10)
    text_c(d, (860, 1060), "fridge", font(44, "semi"), WHITE)
    text_c(d, (640, 330), "lemon juice", font(48, "semi"), LEMON)
    text_c(d, (540, 1150), "slower browning", font(54, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Broken cells", font(int(76 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 690), "+ air", font(int(76 * g2) + 1, "bold"), O2)
    if t > 1.0:
        g3 = pop(prog(t, 1.0, 0.45))
        text_c(d, (540, 850), "= brown", font(int(90 * g3) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Cut an apple and leave it. Soon the white part turns brown. Why?", draw=s1),
    dict(say="The knife breaks open apple cells. An enzyme inside, polyphenol oxidase, meets oxygen from the air.",
         draw=s2),
    dict(say="Their reaction makes brown pigments called melanins. It's called enzymatic browning.", draw=s3),
    dict(say="Bananas, potatoes and brinjals brown the same way.", draw=s4),
    dict(say="To slow it, add lemon juice, or keep the slices in the fridge.", draw=s5),
    dict(say="Broken cells plus air equals brown.", draw=s6),
]
