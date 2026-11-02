import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does cutting an onion make you cry?"
WHITE, DARK = (255, 255, 255), (20, 25, 40)
ONION, ONION_D, ONION_L = (190, 110, 160), (140, 70, 120), (235, 205, 225)
CHEM, ENZ, GAS = (255, 210, 80), (110, 200, 255), (200, 255, 150)
STEEL = (210, 215, 230)


def onion(d, x, y, r, cut=False):
    """Whole onion (side view) or a halved onion showing rings."""
    if not cut:
        d.ellipse([x - r, y - r * 0.9, x + r, y + r * 0.95], fill=ONION, outline=ONION_D, width=6)
        d.polygon([(x - r * 0.2, y - r * 0.8), (x, y - r * 1.35), (x + r * 0.2, y - r * 0.8)], fill=ONION_D)
        for k in (-0.5, 0, 0.5):
            d.arc([x - r * (0.9 - abs(k) * 0.6), y - r * 0.85, x + r * (0.9 - abs(k) * 0.6), y + r * 0.9],
                  250 if k <= 0 else 290, 110 if k >= 0 else 70, fill=ONION_D, width=3)
        for k in range(5):
            d.line([(x - 20 + k * 10, y + r * 0.92), (x - 30 + k * 15, y + r * 1.15)], fill=(220, 200, 170), width=4)
    else:
        for k in range(5):
            rr = r * (1 - k * 0.18)
            d.ellipse([x - rr, y - rr * 0.9, x + rr, y + rr * 0.9], fill=ONION_L if k % 2 == 0 else (250, 230, 240),
                      outline=ONION if k == 0 else (210, 160, 195), width=6 if k == 0 else 3)


def knife(d, x, y, s=1.0):
    d.polygon([(x, y), (x + 300 * s, y), (x + 300 * s, y + 20 * s), (x + 40 * s, y + 80 * s)], fill=STEEL,
              outline=WHITE)
    d.rounded_rectangle([x + 290 * s, y - 8 * s, x + 470 * s, y + 34 * s], 14, fill=(120, 70, 40))


def eye(d, x, y, s=1.0, tear=0.0, red=0.0):
    d.ellipse([x - 90 * s, y - 50 * s, x + 90 * s, y + 50 * s], fill=(255, int(255 - 60 * red), int(255 - 60 * red)),
              outline=DARK, width=5)
    d.ellipse([x - 38 * s, y - 38 * s, x + 38 * s, y + 38 * s], fill=(90, 60, 40))
    d.ellipse([x - 18 * s, y - 18 * s, x + 18 * s, y + 18 * s], fill=DARK)
    d.ellipse([x - 12 * s, y - 22 * s, x, y - 10 * s], fill=WHITE)
    if tear > 0:
        ty = y + 50 * s + 160 * s * tear
        d.ellipse([x + 50 * s, ty - 20 * s, x + 80 * s, ty + 20 * s], fill=(120, 190, 255))
        d.polygon([(x + 52 * s, ty - 8 * s), (x + 65 * s, ty - 40 * s), (x + 78 * s, ty - 8 * s)], fill=(120, 190, 255))


def s1(img, d, t, T, th):
    # left: holding an onion (fine). right: cutting (tears)
    d.rounded_rectangle([70, 300, 520, 1010], 40, fill=(255, 255, 255, 25))
    d.rounded_rectangle([560, 300, 1010, 1010], 40, fill=(255, 255, 255, 25))
    onion(d, 295, 620, 120)
    text_c(d, (295, 880), "holding", font(48, "bold"), WHITE)
    text_c(d, (295, 950), "no tears", font(40, "semi"), th["soft"])
    k = ease(prog(t, 0.3, 0.5))
    onion(d, 785, 640, 120, cut=k > 0.5)
    knife(d, 690, 430 + 150 * k + 10 * math.sin(t * 12), 0.6)
    text_c(d, (785, 880), "cutting", font(48, "bold"), WHITE)
    g = pop(prog(t, 1.0, 0.4))
    if g > 0:
        text_c(d, (785, 950), "tears!", font(int(46 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 1110), "Why?", font(int(80 * pop(prog(t, 1.4, 0.4))) + 1, "bold"), th["accent"],
           stroke_width=5, stroke_fill=DARK)


def cell(d, x, y, w, h, broken=0.0):
    if broken <= 0:
        d.rounded_rectangle([x, y, x + w, y + h], 30, outline=WHITE, width=6, fill=(255, 255, 255, 20))
        d.line([(x + w / 2, y + 10), (x + w / 2, y + h - 10)], fill=WHITE, width=6)  # the wall keeping them apart
    else:
        gap = 40 * broken
        d.rounded_rectangle([x - gap, y - gap, x + w + gap, y + h + gap], 30, outline=WHITE + (int(255 * (1 - broken)),),
                            width=6)


def s2(img, d, t, T, th):
    text_c(d, (540, 330), "inside one onion cell", font(46, "semi"), th["soft"])
    x, y, w, h = 160, 420, 760, 520
    cell(d, x, y, w, h)
    import random
    rnd = random.Random(4)
    for j in range(9):
        cx = x + 60 + rnd.random() * (w / 2 - 120); cy = y + 60 + rnd.random() * (h - 120)
        cy += 8 * math.sin(t * 3 + j)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=CHEM)
    for j in range(6):
        cx = x + w / 2 + 60 + rnd.random() * (w / 2 - 120); cy = y + 60 + rnd.random() * (h - 120)
        cy += 8 * math.sin(t * 3 + j * 2)
        d.regular_polygon((cx, cy, 30), 6, fill=ENZ)
    text_c(d, (x + w / 4, y + h + 60), "chemicals", font(44, "bold"), CHEM)
    text_c(d, (x + 3 * w / 4, y + h + 60), "enzyme", font(44, "bold"), ENZ)
    g = pop(prog(t, 0.8, 0.4))
    if g > 0:
        text_c(d, (540, 1120), "kept APART", font(int(64 * g) + 1, "bold"), WHITE, stroke_width=5, stroke_fill=DARK)


def s3(img, d, t, T, th):
    x, y, w, h = 160, 520, 760, 420
    k = ease(prog(t, 0.0, 0.5))
    cell(d, x, y, w, h, broken=k)
    knife(d, 260, 320 + 160 * k, 0.9)
    m = ease(prog(t, 0.5, 1.0))
    import random
    rnd = random.Random(4)
    for j in range(9):
        cx0 = x + 60 + rnd.random() * (w / 2 - 120); cy = y + 60 + rnd.random() * (h - 120)
        cx = cx0 + (540 - cx0) * m * 0.6
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=CHEM)
    for j in range(6):
        cx0 = x + w / 2 + 60 + rnd.random() * (w / 2 - 120); cy = y + 60 + rnd.random() * (h - 120)
        cx = cx0 + (540 - cx0) * m * 0.6
        d.regular_polygon((cx, cy, 26), 6, fill=ENZ)
    # new chemical rises as wisps
    if t > 1.2:
        for j in range(7):
            f = ((t - 1.2) * 0.5 + j / 7) % 1.0
            gx = 300 + j * 80 + 25 * math.sin(f * 8 + j)
            gy = 900 - 520 * f
            a = int(230 * (1 - f))
            d.ellipse([gx - 18, gy - 18, gx + 18, gy + 18], fill=GAS + (a,))
        text_c(d, (540, 1110), "new chemical floats up", font(54, "bold"), GAS, stroke_width=5, stroke_fill=DARK)


def s4(img, d, t, T, th):
    eye(d, 540, 520, 1.6, red=ease(prog(t, 0.6, 0.8)))
    for j in range(8):
        f = ((t * 0.45) + j / 8) % 1.0
        gx = 340 + j * 55 + 20 * math.sin(f * 7 + j)
        gy = 1050 - 430 * f
        d.ellipse([gx - 16, gy - 16, gx + 16, gy + 16], fill=GAS + (int(220 * (1 - f * 0.6)),))
    if t > 0.8:
        for a in (200, 230, 310, 340):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([(540 + ca * 170, 520 + sa * 110), (540 + ca * 230, 520 + sa * 150)], fill=th["accent"], width=8)
        text_c(d, (540, 1110), "irritates eye nerves", font(56, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)


def s5(img, d, t, T, th):
    eye(d, 540, 520, 1.6, tear=(t * 0.6) % 1.0)
    eye(d, 540, 520, 1.6, tear=(t * 0.6 + 0.5) % 1.0)
    g = pop(prog(t, 0.4, 0.4))
    if g > 0:
        d.rounded_rectangle([150, 900, 930, 1070], 40, fill=(120, 190, 255, 230))
        text_c(d, (540, 985), "tears wash it away", font(int(58 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 320, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    onion(d, 540, 540, int(110 * g) + 1, cut=True)
    knife(d, 330, 420 + 20 * math.sin(t * 4), 0.7)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 790), "sharp knife = less spray", font(int(52 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 900), "Tears =", font(int(60 * g2) + 1, "bold"), (120, 190, 255))
        text_c(d, (540, 990), "your eyes protecting", font(int(58 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Why does cutting an onion make you cry, but holding one doesn't?", draw=s1),
    dict(say="Inside the onion, certain chemicals and an enzyme are kept apart.", draw=s2),
    dict(say="Your knife breaks the cells. They mix and form a new chemical that floats into the air.", draw=s3),
    dict(say="When it reaches your eyes, it irritates the nerves there.", draw=s4),
    dict(say="So your eyes make tears to wash it away.", draw=s5),
    dict(say="A sharp knife sprays less. Tears are your eyes protecting themselves.", draw=s6),
]
