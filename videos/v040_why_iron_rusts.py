import math, random
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does an iron gate rust?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
IRON, IRON2 = (150, 160, 175), (100, 110, 125)
RUST, RUST2 = (175, 85, 40), (130, 60, 30)
WATER, AIR, ZINC, PAINT = (110, 190, 255), (200, 235, 255), (205, 215, 225), (60, 150, 90)
GREEN, RED = (110, 220, 140), (255, 110, 110)


def gate(d, x0, y0, w, h, rust=0.0, color=IRON, seed=4):
    # frame + vertical bars; rust patches grow with `rust`
    d.rectangle([x0, y0, x0 + w, y0 + 22], fill=color)
    d.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=color)
    n = 7
    for i in range(n):
        x = x0 + 10 + i * (w - 20) / (n - 1)
        d.rectangle([x - 11, y0, x + 11, y0 + h], fill=color)
    if rust > 0:
        rnd = random.Random(seed)
        for _ in range(int(60 * rust)):
            i = rnd.randrange(n)
            x = x0 + 10 + i * (w - 20) / (n - 1) + rnd.uniform(-8, 8)
            y = rnd.uniform(y0, y0 + h)
            r = rnd.uniform(8, 18)
            d.ellipse([x - r * 0.8, y - r, x + r * 0.8, y + r], fill=RUST if rnd.random() > 0.3 else RUST2)


def drop(d, x, y, s=1.0, col=WATER):
    d.polygon([(x, y - 34 * s), (x - 20 * s, y), (x + 20 * s, y)], fill=col)
    d.ellipse([x - 20 * s, y - 18 * s, x + 20 * s, y + 22 * s], fill=col)


def bar(d, x, y, w=420, rust=0.0, color=IRON):
    d.rounded_rectangle([x - w / 2, y - 40, x + w / 2, y + 40], 14, fill=color)
    if rust > 0:
        rnd = random.Random(9)
        for _ in range(int(30 * rust)):
            px, py = x + rnd.uniform(-w / 2 + 15, w / 2 - 15), y + rnd.uniform(-28, 28)
            r = rnd.uniform(8, 16)
            d.ellipse([px - r, py - r, px + r, py + r], fill=RUST)


def s1(img, d, t, T, th):
    k = ease(prog(t, 0.6, 1.6))
    gate(d, 220, 420, 640, 560, rust=k)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1100), "reddish brown?", font(int(72 * g) + 1, "bold"), WHITE, stroke_width=4, stroke_fill=DARK)
    text_c(d, (540, 340), "old iron gate", font(54, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (290, 380), "iron", font(54, "bold"), WHITE)
    text_c(d, (790, 380), "rust", font(54, "bold"), RUST)
    bar(d, 290, 520, 360)
    bar(d, 790, 520, 360, rust=1.0, color=(150, 110, 90))
    k = ease(prog(t, 0.3, 0.6))
    d.line([(480, 520), (480 + 120 * k, 520)], fill=WHITE, width=10)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([180, 720, 900, 860], 50, fill=th["accent"])
        text_c(d, (540, 790), "a NEW substance", font(int(60 * g) + 1, "bold"), DARK)
    if t > 1.6:
        text_c(d, (540, 960), "iron oxide", font(64, "bold"), WHITE)


def s3(img, d, t, T, th):
    bar(d, 540, 760, 480, rust=ease(prog(t, 1.4, 1.0)))
    k = ease(prog(t, 0.2, 0.8))
    # air arrives from the left, water from the right
    for i in range(3):
        x = 140 + 180 * k + i * 30; y = 520 + i * 60
        d.ellipse([x - 28, y - 28, x + 28, y + 28], fill=AIR, outline=WHITE, width=3)
        text_c(d, (x, y), "O₂", font(26, "sym"), DARK)
    k2 = ease(prog(t, 0.6, 0.8))
    for i in range(3):
        drop(d, 820 - 120 * k2 + i * 40, 520 + i * 60, 0.9)
    text_c(d, (250, 400), "oxygen", font(48, "bold"), WHITE)
    text_c(d, (840, 400), "water", font(48, "bold"), WHITE)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([220, 930, 860, 1060], 50, fill=th["accent"])
        text_c(d, (540, 995), "needs BOTH", font(int(62 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    labels = [("dry air", 0.15), ("humid air", 0.55), ("near the sea", 1.0)]
    for i, (lab, r) in enumerate(labels):
        y = 470 + i * 230
        k = ease(prog(t, 0.3 + 0.35 * i, 0.8))
        bar(d, 640, y, 440, rust=r * k)
        text_c(d, (230, y), lab, font(44, "bold"), WHITE)
        if i >= 1:
            for j in range(2 * i):
                drop(d, 450 + j * 80, y - 70, 0.45)
    if t > 1.8:
        text_c(d, (540, 1140), "salt water: even faster", font(50, "bold"), th["accent"])


def s5(img, d, t, T, th):
    items = [("paint", PAINT), ("grease", (90, 70, 40)), ("zinc coat", ZINC)]
    for i, (lab, col) in enumerate(items):
        x = 230 + i * 310
        g = pop(prog(t, 0.2 + 0.45 * i, 0.4))
        d.rounded_rectangle([x - 50, 440, x + 50, 860], 20, fill=IRON)
        if g > 0:
            d.rounded_rectangle([x - 58, 440, x + 58, 440 + 420 * min(1, g)], 24, fill=col + (220,))
        text_c(d, (x, 930), lab, font(46, "bold"), WHITE)
        if t > 0.6 + 0.45 * i:
            text_c(d, (x, 370), "✓", font(70, "sym"), GREEN)
    if t > 2.0:
        text_c(d, (540, 1060), "zinc coat = galvanisation", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Stop air + water", font(int(70 * g) + 1, "bold"), WHITE)
    bar(d, 540, 720, 460)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 920), "stop the rust", font(int(80 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Why does an old iron gate turn reddish brown?", draw=s1),
    dict(say="That's rust. It's not iron any more. It's a new substance, iron oxide.", draw=s2),
    dict(say="Iron rusts only when it gets both oxygen and water.", draw=s3),
    dict(say="Humid air rusts it faster. Near the sea, salty water makes it even faster.", draw=s4),
    dict(say="So we paint gates, grease chains, or coat iron with zinc.", draw=s5),
    dict(say="Stop air and water, stop the rust.", draw=s6),
]
