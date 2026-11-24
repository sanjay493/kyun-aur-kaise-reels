import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a rubbed refill pick up paper?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
REFILL, TIP = (120, 190, 255), (230, 230, 240)
BAL1, BAL2, PAPER = (255, 110, 140), (255, 190, 80), (245, 245, 235)
POLY, PLUS, MINUS = (220, 235, 245), (255, 120, 120), (120, 200, 255)
GREEN = (110, 220, 140)


def refill(d, x, y, ang=0.0, L=420):
    dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
    d.line([(x - dx, y - dy), (x + dx, y + dy)], fill=REFILL, width=22)
    d.ellipse([x + dx - 14, y + dy - 14, x + dx + 14, y + dy + 14], fill=TIP)


def balloon(d, x, y, col, s=1.0, sign=None):
    r = 95 * s
    d.ellipse([x - r * 0.85, y - r, x + r * 0.85, y + r], fill=col)
    d.polygon([(x - 14 * s, y + r + 16 * s), (x + 14 * s, y + r + 16 * s), (x, y + r - 4 * s)], fill=col)
    d.line([(x, y + r + 16 * s), (x, y + r + 120 * s)], fill=WHITE, width=3)
    if sign:
        for i in range(3):
            text_c(d, (x + (i - 1) * r * 0.45, y), sign, font(int(48 * s) + 1, "sym"), WHITE)


def bits(d, cx, y, t, lift=0.0, n=9):
    for i in range(n):
        x = cx - 200 + i * 50
        yy = max(y - lift * (60 + (i * 37) % 80) * (1 - abs(i - n / 2) / n), 745)
        d.rectangle([x - 12, yy - 8, x + 12, yy + 8], fill=PAPER)


def s1(img, d, t, T, th):
    if t < 1.3:
        rub = math.sin(t * 18) * 60
        refill(d, 540, 620, 0.0)
        d.rounded_rectangle([440 + rub, 570, 640 + rub, 670], 20, fill=POLY + (170,))
        text_c(d, (540, 360), "refill + polythene", font(56, "bold"), WHITE)
    else:
        lift = ease(prog(t, 1.4, 0.8))
        refill(d, 540, 720, 0.0, 440)
        bits(d, 540, 1000, t, lift * 2.2)
        text_c(d, (540, 360), "It picks up paper!" if t < 2.2 else "How?", font(64, "bold"), th["accent"])


def s2(img, d, t, T, th):
    refill(d, 540, 560, 0.0, 520)
    n = int(clamp(t / 1.2) * 8)
    for i in range(n):
        text_c(d, (330 + i * 60, 500), "+", font(46, "sym"), PLUS)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([170, 720, 910, 860], 50, fill=th["accent"])
        text_c(d, (540, 790), "electric charge", font(int(62 * g) + 1, "bold"), DARK)
        text_c(d, (540, 960), "made by rubbing = static charge", font(46, "semi"), WHITE)
    text_c(d, (540, 360), "Rubbing gives it", font(60, "bold"), WHITE)


def s3(img, d, t, T, th):
    k = ease(prog(t, 0.4, 0.8))
    balloon(d, 470 - 110 * k, 560, BAL1, 1.0, "−" if t > 0.3 else None)
    balloon(d, 610 + 110 * k, 560, BAL2, 1.0, "−" if t > 0.3 else None)
    d.line([(470 - 110 * k, 300), (470 - 110 * k, 560 - 95)], fill=WHITE, width=3)
    d.line([(610 + 110 * k, 300), (610 + 110 * k, 560 - 95)], fill=WHITE, width=3)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([200, 900, 880, 1040], 50, fill=th["accent"])
        text_c(d, (540, 970), "Like charges REPEL", font(int(58 * g) + 1, "bold"), DARK)
    text_c(d, (540, 1120), "both rubbed with wool", font(40, "semi"), th["soft"])


def s4(img, d, t, T, th):
    k = ease(prog(t, 0.3, 0.9))
    balloon(d, 380 + 60 * k, 560, BAL1, 1.0, "−")
    x = 820 - 160 * k
    refill(d, x, 560, math.pi / 2, 360)
    for i in range(3):
        text_c(d, (x + 40, 470 + i * 80), "+", font(42, "sym"), PLUS)
    if t > 1.1:
        g = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([170, 900, 910, 1040], 50, fill=GREEN)
        text_c(d, (540, 970), "Unlike charges ATTRACT", font(int(54 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    # head with hair rising as the sweater comes off
    k = ease(prog(t, 0.2, 1.0))
    cx, cy = 540, 700
    for i in range(11):
        a = math.radians(200 + i * 14)
        L = 40 + 110 * k
        x0, y0 = cx + 150 * math.cos(a), cy + 150 * math.sin(a)
        d.line([(x0, y0), (x0 + L * math.cos(a), y0 + L * math.sin(a))], fill=(40, 30, 30), width=10)
    d.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], fill=(240, 195, 155))
    for ex in (-50, 50):
        d.ellipse([cx + ex - 14, cy - 20, cx + ex + 14, cy + 8], fill=DARK)
    d.ellipse([cx - 30, cy + 50, cx + 30, cy + 90], fill=(140, 50, 60))
    sy = 900 + 80 * k
    d.rounded_rectangle([280, sy, 800, sy + 110], 40, fill=(90, 140, 220))
    if t > 1.0:
        text_c(d, (540, 360), "static charge again!", font(58, "bold"), th["accent"])
    else:
        text_c(d, (540, 360), "pulling off a sweater...", font(56, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 540), "Like charges push.", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "Unlike charges pull.", font(int(70 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Rub a pen refill with polythene. Now it picks up bits of paper! How?", draw=s1),
    dict(say="Rubbing gives it a small electric charge, called a static charge.", draw=s2),
    dict(say="Rub two balloons with wool, and they push apart. Like charges repel.", draw=s3),
    dict(say="A charged balloon pulls a charged refill. Unlike charges attract.", draw=s4),
    dict(say="Hair standing up when you pull off a sweater? Static charge again.", draw=s5),
    dict(say="Like charges push. Unlike charges pull.", draw=s6),
]
