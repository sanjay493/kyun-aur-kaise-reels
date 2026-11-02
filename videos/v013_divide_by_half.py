import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why is 6 ÷ ½ not 3?"
WHITE, DARK = (255, 255, 255), (20, 22, 50)
ROTI, ROTI_D, BURN = (235, 190, 120), (200, 150, 85), (170, 110, 60)
RED, GREEN = (240, 90, 90), (90, 210, 130)


def roti(d, x, y, r, half=None, gap=0):
    """Whole roti, or half='l'/'r' to draw just one half, nudged apart by gap."""
    box = [x - r, y - r, x + r, y + r]
    if half is None:
        d.ellipse(box, fill=ROTI, outline=ROTI_D, width=4)
        spots = [(-0.4, -0.2), (0.3, 0.35), (0.1, -0.45), (-0.2, 0.4), (0.45, -0.1)]
    else:
        dx = -gap if half == "l" else gap
        box = [x - r + dx, y - r, x + r + dx, y + r]
        a0, a1 = (90, 270) if half == "l" else (270, 90)
        d.pieslice(box, a0, a1, fill=ROTI, outline=ROTI_D, width=4)
        spots = [(-0.4, -0.2), (-0.2, 0.4)] if half == "l" else [(0.3, 0.35), (0.45, -0.1)]
        x += dx
    for sx, sy in spots:
        d.ellipse([x + sx * r - r * 0.09, y + sy * r - r * 0.07, x + sx * r + r * 0.09, y + sy * r + r * 0.07],
                  fill=BURN)


def s1(img, d, t, T, th):
    text_c(d, (540, 470), "6 ÷ ½ = ?", font(130, "bold"), WHITE)
    g = pop(prog(t, 0.6, 0.4))
    if g > 0:
        text_c(d, (330, 760), "3", font(int(150 * g) + 1, "bold"), RED)
        d.line([(260, 690), (400, 830)], fill=RED, width=14)
        d.line([(400, 690), (260, 830)], fill=RED, width=14)
    g2 = pop(prog(t, 1.4, 0.4))
    if g2 > 0:
        text_c(d, (750, 760), "12", font(int(170 * g2) + 1, "bold"), th["accent"], stroke_width=6, stroke_fill=DARK)
        d.ellipse([620, 640, 880, 880], outline=GREEN, width=10)
    if t > 2.0:
        text_c(d, (540, 1060), "How?", font(84, "bold"), th["accent"])


def s2(img, d, t, T, th):
    # a box, and pieces fitting into it
    text_c(d, (540, 360), "Division asks:", font(56, "semi"), th["soft"])
    g = pop(prog(t, 0.2, 0.45))
    if g > 0:
        text_c(d, (540, 500), "how many of THESE", font(int(64 * g) + 1, "bold"), th["accent"])
        text_c(d, (540, 590), "fit inside THAT?", font(int(64 * g) + 1, "bold"), WHITE)
    d.rounded_rectangle([200, 700, 880, 1000], 30, outline=WHITE, width=6)
    k = ease(prog(t, 0.8, 1.2))
    n = int(k * 4 + 0.001)
    for i in range(4):
        x = 230 + i * 162
        if i < n:
            d.rounded_rectangle([x, 730, x + 140, 970], 20, fill=th["accent"])
    if n >= 4:
        text_c(d, (540, 1100), "12 ÷ 3 = 4  (four 3s fit in 12)", font(46, "bold"), WHITE)


ROWS = [(250, 460), (540, 460), (830, 460), (250, 760), (540, 760), (830, 760)]


def s3(img, d, t, T, th):
    for i, (x, y) in enumerate(ROWS):
        g = pop(prog(t, 0.05 + i * 0.12, 0.3))
        if g > 0:
            roti(d, x, y, int(110 * g) + 1)
    text_c(d, (540, 320), "6 rotis", font(60, "bold"), th["accent"])
    k = ease(prog(t, 1.2, 0.6))
    if k > 0:
        for (x, y) in ROWS:
            d.line([(x, y - 125), (x, y - 125 + 250 * k)], fill=WHITE, width=6)
        text_c(d, (540, 1000), "cut each into halves", font(54, "bold"), WHITE)


def s4(img, d, t, T, th):
    gap = 18 * ease(prog(t, 0.0, 0.4))
    shown = int(clamp((t - 0.4) / 1.6) * 12 + 0.001)
    c = 0
    for (x, y) in ROWS:
        for h in ("l", "r"):
            roti(d, x, y, 105, half=h, gap=gap)
            c += 1
            if c <= shown:
                px = x - 50 - gap if h == "l" else x + 50 + gap
                d.ellipse([px - 30, y - 30, px + 30, y + 30], fill=th["accent"])
                text_c(d, (px, y), str(c), font(34, "bold"), DARK)
    text_c(d, (540, 320), "2 halves per roti", font(52, "semi"), th["soft"])
    if shown >= 12:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1020), "12 halves", font(int(90 * g) + 1, "bold"), th["accent"], stroke_width=6,
               stroke_fill=DARK)


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    text_c(d, (540, 470), "6 ÷ ½", font(int(120 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "=", font(110, "bold"), th["soft"])
    g2 = pop(prog(t, 0.6, 0.4))
    if g2 > 0:
        text_c(d, (540, 780), "6 × 2", font(int(120 * g2) + 1, "bold"), th["accent"])
    if t > 1.3:
        text_c(d, (540, 960), "= 12", font(110, "bold"), GREEN, stroke_width=5, stroke_fill=DARK)


def s6(img, d, t, T, th):
    text_c(d, (540, 340), "Same with a third:", font(54, "semi"), th["soft"])
    # one roti cut into thirds
    k = ease(prog(t, 0.2, 0.6))
    r = 140
    for j, a in enumerate((90, 210, 330)):
        off = 18 * k
        ca, sa = math.cos(math.radians(a + 60)), math.sin(math.radians(a + 60))
        d.pieslice([540 - r + ca * off, 600 - r + sa * off, 540 + r + ca * off, 600 + r + sa * off], a, a + 120,
                   fill=ROTI, outline=ROTI_D, width=4)
    text_c(d, (540, 800), "3 pieces per roti", font(48, "bold"), WHITE)
    g = pop(prog(t, 1.0, 0.4))
    if g > 0:
        text_c(d, (540, 940), "6 ÷ 1/3 = 6 × 3 = 18", font(int(70 * g) + 1, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    for i, s in enumerate((70, 50, 34)):
        x = 300 + i * 240
        n = [1, 2, 3][i]
        for j in range(n):
            roti(d, x + (j - (n - 1) / 2) * s * 0.9, 560, int(s * g) + 1)
    if t > 0.4:
        g2 = pop(prog(t, 0.4, 0.45))
        text_c(d, (540, 780), "Smaller pieces,", font(int(70 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 890), "more of them fit", font(int(70 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Six divided by a half is not three. It's twelve. How?", show="6 ÷ ½ is not 3. It's 12. How?", draw=s1),
    dict(say="Division asks: how many of these fit inside that?", draw=s2),
    dict(say="Take six rotis. Cut each roti into halves.", show="Take 6 rotis. Cut each roti into halves.", draw=s3),
    dict(say="Each roti gives two halves. So six rotis give twelve halves.",
         show="Each roti gives 2 halves. So 6 rotis give 12 halves.", draw=s4),
    dict(say="That's why dividing by a half is the same as multiplying by two.",
         show="That's why dividing by ½ is the same as multiplying by 2.", draw=s5),
    dict(say="Same with a third: six divided by one third is eighteen.", show="Same with a third: 6 ÷ 1/3 is 18.",
         draw=s6),
    dict(say="Smaller pieces, more of them fit.", draw=s7),
]
