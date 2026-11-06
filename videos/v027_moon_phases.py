import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Does the Moon really change shape?"
WHITE, DARK = (255, 255, 255), (15, 20, 40)
MOON, NIGHT = (245, 240, 215), (55, 60, 80)
SUN, EARTH = (255, 200, 60), (70, 150, 255)


def moon_phase(d, cx, cy, r, p, n=60):
    """Draw the Moon as seen from Earth. p: 0 = new, 0.25 = first quarter, 0.5 = full, 0.75 = last quarter."""
    p %= 1.0
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NIGHT)
    side = 1 if p <= 0.5 else -1          # waxing: lit on the right; waning: lit on the left
    c = math.cos(2 * math.pi * p)
    limb, term = [], []
    for i in range(n + 1):
        th = math.pi * i / n
        y = cy - r * math.cos(th)
        limb.append((cx + side * r * math.sin(th), y))
        term.append((cx + side * c * r * math.sin(th), y))
    poly = limb + term[::-1]
    if p > 0.005:
        d.polygon(poly, fill=MOON)


def stars(d, seed=3, a=160):
    import random
    rnd = random.Random(seed)
    for _ in range(40):
        x, y, s = rnd.randint(40, W - 40), rnd.randint(270, 1180), rnd.randint(2, 5)
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, a))


def s1(img, d, t, T, th):
    stars(d)
    g1 = pop(prog(t, 0.1, 0.45))
    if g1 > 0:
        moon_phase(d, 300, 600, 150 * g1 + 1, 0.5)
        text_c(d, (300, 820), "Monday", font(46, "bold"), th["soft"])
    g2 = pop(prog(t, 1.2, 0.45))
    if g2 > 0:
        moon_phase(d, 780, 600, 150 * g2 + 1, 0.92)
        text_c(d, (780, 820), "a week later", font(46, "bold"), th["soft"])
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1040), "Did it change shape?", font(int(70 * g) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    # Sun on the left, rays to a Moon that is half lit
    g = pop(prog(t, 0.05, 0.45))
    d.ellipse([-150, 470 - 150 * g, 150 * g, 470 + 150 * g], fill=SUN)
    k = ease(prog(t, 0.4, 0.8))
    for i, y in enumerate((370, 470, 570)):
        x1 = 170 + 420 * k
        if k > 0:
            d.line([(170, y), (x1, y)], fill=SUN + (200,), width=8)
            if k > 0.95:
                d.polygon([(x1 + 22, y), (x1 - 8, y - 16), (x1 - 8, y + 16)], fill=SUN)
    cx, cy, r = 790, 470, 150
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NIGHT)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=MOON)
    if t > 1.0:
        text_c(d, (540, 760), "No light of its own", font(60, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 870), "Half is ALWAYS lit", font(66, "bold"), th["accent"])
        text_c(d, (540, 960), "(the half facing the Sun)", font(44, "semi"), th["soft"])


def orbit_scene(d, t, th, a):
    """Sun light from the left, Earth in the middle, Moon at angle a (0 = right of Earth = full moon)."""
    ex, ey, R = 600, 590, 260
    for y in (330, 450, 590, 730, 850):
        d.line([(40, y), (150, y)], fill=SUN + (190,), width=7)
        d.polygon([(170, y), (145, y - 13), (145, y + 13)], fill=SUN)
    text_c(d, (95, 280), "sunlight", font(36, "semi"), SUN)
    d.ellipse([ex - R, ey - R, ex + R, ey + R], outline=(255, 255, 255, 70), width=3)
    d.ellipse([ex - 70, ey - 70, ex + 70, ey + 70], fill=EARTH)
    d.pieslice([ex - 70, ey - 70, ex + 70, ey + 70], 270, 450, fill=(30, 70, 140))  # night side of Earth
    text_c(d, (ex, ey), "Earth", font(30, "bold"), WHITE)
    mx, my = ex + R * math.cos(a), ey - R * math.sin(a)
    r = 48
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=NIGHT)
    d.pieslice([mx - r, my - r, mx + r, my + r], 90, 270, fill=MOON)  # lit half faces the Sun
    return (a / (2 * math.pi) + 0.5) % 1.0


def s3(img, d, t, T, th):
    a = math.pi + 2 * math.pi * prog(t, 0.2, max(1.0, T - 0.5))  # one lap, starting at new moon
    p = orbit_scene(d, t, th, a)
    d.rounded_rectangle([330, 920, 750, 1180], 30, fill=(0, 0, 0, 90), outline=th["accent"], width=4)
    text_c(d, (540, 955), "what we see", font(34, "semi"), th["soft"])
    moon_phase(d, 540, 1065, 85, p)
    if p < 0.03 or p > 0.97:
        d.ellipse([455, 980, 625, 1150], outline=(140, 145, 170), width=3)


def s4(img, d, t, T, th):
    stars(d, 5, 120)
    g1 = pop(prog(t, 0.1, 0.4))
    if g1 > 0:
        moon_phase(d, 300, 560, 140 * g1 + 1, 0.5)
        text_c(d, (300, 770), "FULL moon", font(54, "bold"), th["accent"])
        text_c(d, (300, 850), "lit side faces us", font(40, "semi"), WHITE)
    g2 = pop(prog(t, 1.4, 0.4))
    if g2 > 0:
        moon_phase(d, 780, 560, 140 * g2 + 1, 0.0)
        d.ellipse([780 - 140, 560 - 140, 780 + 140, 560 + 140], outline=(140, 145, 170), width=3)
        text_c(d, (780, 770), "NEW moon", font(54, "bold"), th["accent"])
        text_c(d, (780, 850), "lit side faces away", font(40, "semi"), WHITE)


def s5(img, d, t, T, th):
    phases = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
    for i, p in enumerate(phases):
        g = pop(prog(t, 0.1 + i * 0.18, 0.35))
        if g <= 0:
            continue
        cx = 150 + (i % 4) * 260
        cy = 470 + (i // 4) * 250
        moon_phase(d, cx, cy, 85 * g + 1, p)
        if p == 0.0:
            d.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], outline=(140, 145, 170), width=3)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([200, 930, 880, 1090], 40, fill=th["accent"])
        text_c(d, (540, 1010), "about 29.5 days", font(int(76 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    k = (t / 2.5) % 1.0
    moon_phase(d, 540, 560, 130, k)
    if k < 0.06 or k > 0.94:
        d.ellipse([540 - 130, 560 - 130, 540 + 130, 560 + 130], outline=(140, 145, 170), width=3)
    g = pop(prog(t, 0.4, 0.45))
    text_c(d, (540, 820), "Shape: same", font(int(78 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 930), "View: changes", font(int(78 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Round one night, a thin smile a week later. Does the Moon really change shape?", draw=s1),
    dict(say="No. The Moon shines by reflecting sunlight, and half of it is always lit.", draw=s2),
    dict(say="As it circles the Earth, we see different amounts of that lit half.", draw=s3),
    dict(say="Lit side facing us? Full moon. Facing away? New moon.", draw=s4),
    dict(say="One full cycle takes about twenty-nine and a half days.",
         show="One full cycle takes about 29.5 days.", draw=s5),
    dict(say="The shape never changes. Only our view does.", draw=s6),
]
