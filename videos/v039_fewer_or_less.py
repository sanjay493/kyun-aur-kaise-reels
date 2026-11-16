import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Fewer laddoos or less laddoos?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
LADDOO, LADDOO2 = (250, 175, 60), (215, 135, 35)
WATER, GLASS = (110, 190, 255), (230, 240, 255)
GREEN, RED = (110, 220, 140), (255, 110, 110)


def laddoo(d, x, y, r=48):
    d.ellipse([x - r, y - r, x + r, y + r], fill=LADDOO, outline=LADDOO2, width=5)
    for dx, dy in [(-0.4, -0.3), (0.3, -0.1), (-0.1, 0.4), (0.35, 0.4)]:
        d.ellipse([x + dx * r - 5, y + dy * r - 5, x + dx * r + 5, y + dy * r + 5], fill=LADDOO2)


def plate(d, x, y, w=300):
    d.ellipse([x - w, y - 55, x + w, y + 55], fill=(225, 225, 235), outline=WHITE, width=5)


def glass(d, x, y, level, h=320, w=110):
    top, bot = y - h / 2, y + h / 2
    wl = top + (1 - level) * h
    d.polygon([(x - w + 10, wl), (x + w - 10, wl), (x + w - 25, bot), (x - w + 25, bot)], fill=WATER + (200,))
    d.line([(x - w, top), (x - w + 25, bot), (x + w - 25, bot), (x + w, top)], fill=GLASS, width=8)


def tag(d, xy, s, col, size=64, g=1.0):
    text_c(d, xy, s, font(int(size * g) + 1, "bold"), col)


def s1(img, d, t, T, th):
    plate(d, 540, 700)
    for i, (x, y) in enumerate([(430, 650), (540, 630), (650, 650), (485, 580), (595, 580)]):
        if t > 0.1 * i:
            laddoo(d, x, y, int(48 * pop(prog(t, 0.1 * i, 0.35))) + 1)
    g = pop(prog(t, 0.8, 0.4))
    d.rounded_rectangle([110, 860, 520, 980], 40, fill=(255, 255, 255, 40), outline=th["accent"], width=5)
    d.rounded_rectangle([560, 860, 970, 980], 40, fill=(255, 255, 255, 40), outline=th["accent"], width=5)
    tag(d, (315, 920), "fewer?", WHITE, 64, g)
    tag(d, (765, 920), "less?", WHITE, 64, g)
    if t > 1.6:
        text_c(d, (540, 380), "Which one is right?", font(60, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 360), "Can you count it?", font(60, "bold"), th["accent"])
    for i in range(3):
        x = 300 + i * 240
        if t > 0.3 + 0.4 * i:
            g = pop(prog(t, 0.3 + 0.4 * i, 0.35))
            laddoo(d, x, 620, int(70 * g) + 1)
            text_c(d, (x, 750), str(i + 1), font(int(70 * g) + 1, "bold"), WHITE)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([200, 900, 880, 1040], 50, fill=th["accent"])
        tag(d, (540, 970), "FEWER", DARK, 80, g)
        text_c(d, (540, 1120), "fewer laddoos · fewer mistakes", font(42, "semi"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 360), "Can't count it?", font(60, "bold"), th["accent"])
    lvl = 0.85 - 0.45 * ease(prog(t, 0.3, 1.2))
    glass(d, 540, 640, lvl)
    for i, w in enumerate(["water", "sugar", "time"]):
        if t > 0.5 + 0.3 * i:
            text_c(d, (180 + 360 * i, 860), w, font(48, "semi"), WHITE)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([200, 930, 880, 1070], 50, fill=th["accent"])
        tag(d, (540, 1000), "LESS", DARK, 80, g)
        text_c(d, (540, 1140), "less water · less time", font(42, "semi"), th["soft"])


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "Put a number in front", font(56, "bold"), th["accent"])
    g1 = pop(prog(t, 0.3, 0.4))
    d.rounded_rectangle([110, 470, 970, 650], 40, fill=(255, 255, 255, 35))
    tag(d, (470, 560), "three laddoos", WHITE, 62, g1)
    if t > 0.7:
        text_c(d, (850, 560), "✓", font(int(90 * pop(prog(t, 0.7, 0.4))) + 1, "sym"), GREEN)
    if t > 1.3:
        g2 = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([110, 740, 970, 920], 40, fill=(255, 255, 255, 35))
        tag(d, (470, 830), "three milks", WHITE, 62, g2)
        if t > 1.7:
            text_c(d, (850, 830), "✗", font(int(90 * pop(prog(t, 1.7, 0.4))) + 1, "sym"), RED)


def s5(img, d, t, T, th):
    for i, (a, b) in enumerate([("fewer", "exams"), ("less", "homework")]):
        if t > 0.2 + 0.7 * i:
            g = pop(prog(t, 0.2 + 0.7 * i, 0.4))
            y = 520 + i * 300
            d.rounded_rectangle([130, y - 100, 950, y + 100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=5)
            text_c(d, (540, y), f"{a} {b}", font(int(80 * g) + 1, "bold"), th["accent"] if i == 0 else WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 480), "Count it?", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 590), "FEWER", font(int(100 * g) + 1, "bold"), th["accent"])
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        text_c(d, (540, 800), "Can't count it?", font(int(70 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 910), "LESS", font(int(100 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Fewer laddoos or less laddoos? Most people say less. Here's the rule.", draw=s1),
    dict(say="If you can count it, one, two, three, use fewer. Fewer laddoos, fewer mistakes.", draw=s2),
    dict(say="If you can't count it, like water, sugar or time, use less. Less water, less time.", draw=s3),
    dict(say="Quick test: can you put a number in front? Three laddoos, yes. Three milks, no.", draw=s4),
    dict(say="So: fewer exams, less homework.", draw=s5),
    dict(say="Count it? Fewer. Can't count it? Less.", draw=s6),
]
