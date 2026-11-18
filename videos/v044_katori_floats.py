import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a steel katori float?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
STEEL, STEEL2 = (200, 208, 220), (140, 150, 165)
WATER, WATER2 = (80, 160, 230), (60, 130, 200)
SHIP, SHIP2 = (170, 180, 195), (110, 120, 135)
GREEN, RED, UP = (110, 220, 140), (255, 110, 110), (255, 220, 90)


def bucket(d, x0, x1, top, bot, level):
    d.rectangle([x0, level, x1, bot], fill=WATER + (190,))
    d.line([(x0, top), (x0, bot), (x1, bot), (x1, top)], fill=WHITE, width=8)
    d.line([(x0, level), (x1, level)], fill=(170, 215, 255), width=4)


def spoon(d, x, y, ang=0.0):
    d.ellipse([x - 30, y - 20, x + 30, y + 20], fill=STEEL, outline=STEEL2, width=3)
    d.rounded_rectangle([x + 25, y - 6, x + 140, y + 6], 6, fill=STEEL)


def katori(d, x, y, w=120, h=60):
    d.chord([x - w, y - h, x + w, y + h], 0, 180, fill=STEEL, outline=STEEL2, width=4)
    d.line([(x - w, y), (x + w, y)], fill=STEEL2, width=6)


def arrow_up(d, x, y, L=90, col=UP):
    d.line([(x, y), (x, y - L)], fill=col, width=10)
    d.polygon([(x - 18, y - L + 6), (x + 18, y - L + 6), (x, y - L - 24)], fill=col)


def s1(img, d, t, T, th):
    bucket(d, 140, 940, 420, 1120, 620)
    sy = 560 + 460 * ease(prog(t, 0.3, 1.2))
    spoon(d, 300, sy)
    k = ease(prog(t, 0.8, 0.6))
    katori(d, 720, 380 + 230 * k if k < 1 else 610)
    if t > 1.6:
        text_c(d, (330, 360), "sinks", font(52, "bold"), RED)
        text_c(d, (720, 360), "floats!", font(52, "bold"), GREEN)


def s2(img, d, t, T, th):
    text_c(d, (540, 360), "Same steel. Why?", font(62, "bold"), th["accent"])
    katori(d, 330, 640)
    spoon(d, 640, 640)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 850), "= steel", font(int(60 * g) + 1, "bold"), WHITE)
    if t > 1.2:
        text_c(d, (540, 1000), "...and so is a ship", font(54, "bold"), th["soft"])


def s3(img, d, t, T, th):
    bucket(d, 140, 940, 420, 1120, 650)
    katori(d, 540, 640)
    for i, x in enumerate([440, 540, 640]):
        if t > 0.3 + 0.2 * i:
            k = ease(prog(t, 0.3 + 0.2 * i, 0.5))
            arrow_up(d, x, 860, 120 * k + 1)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([220, 930, 860, 1060], 50, fill=th["accent"])
        text_c(d, (540, 995), "upthrust", font(int(64 * g) + 1, "bold"), DARK)
    text_c(d, (540, 360), "Water pushes up", font(60, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Archimedes:", font(56, "bold"), th["accent"])
    text_c(d, (540, 420), "push = weight of water", font(50, "bold"), WHITE)
    text_c(d, (540, 490), "pushed aside", font(50, "bold"), WHITE)
    # spoon: little water pushed aside
    bucket(d, 110, 500, 600, 1050, 720)
    spoon(d, 250, 1000)
    # katori: lots of water pushed aside
    rise = 70 * ease(prog(t, 0.6, 0.8))
    bucket(d, 580, 970, 600, 1050, 760 - rise)
    katori(d, 775, 750 - rise)
    if t > 1.4:
        text_c(d, (305, 1120), "a little", font(44, "bold"), RED)
        text_c(d, (775, 1120), "a lot", font(44, "bold"), GREEN)


def s5(img, d, t, T, th):
    # ship hull, hollow, full of air
    k = ease(prog(t, 0.2, 0.8))
    y = 600 + 40 * k
    d.rectangle([90, 760, 990, 1120], fill=WATER + (190,))
    d.line([(90, 760), (990, 760)], fill=(170, 215, 255), width=4)
    d.polygon([(200, y), (880, y), (800, y + 220), (280, y + 220)], fill=SHIP, outline=SHIP2)
    d.polygon([(240, y + 20), (840, y + 20), (775, y + 190), (305, y + 190)], fill=(235, 245, 255))
    if t > 0.8:
        text_c(d, (540, y + 90), "air", font(56, "bold"), (120, 160, 200))
    if t > 1.3:
        text_c(d, (540, 380), "Hollow shape", font(62, "bold"), th["accent"])
        text_c(d, (540, 460), "pushes aside lots of water", font(46, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Same steel.", font(int(72 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 680), "Shape decides.", font(int(80 * g2) + 1, "bold"), th["accent"])
        katori(d, 540, 880, 110, 55)


SCENES = [
    dict(say="Drop a steel spoon in a bucket, and it sinks. But a steel katori floats. Why?", draw=s1),
    dict(say="Same steel. Giant ships are made of steel too.", draw=s2),
    dict(say="Water pushes up on everything in it. That push is called upthrust.", draw=s3),
    dict(say="Archimedes found it equals the weight of the water pushed aside.", draw=s4),
    dict(say="A hollow katori or ship pushes aside lots of water, enough to hold up its weight.", draw=s5),
    dict(say="Same steel. Shape decides.", draw=s6),
]
