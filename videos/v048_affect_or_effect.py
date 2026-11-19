import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Rain will affect or effect the match?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GRASS, PITCH = (70, 160, 80), (215, 190, 130)
CLOUD, RAIN = (200, 210, 225), (120, 190, 255)
GREEN, RED, BLUE = (110, 220, 140), (255, 110, 110), (120, 190, 255)


def cloud(d, x, y, s=1.0):
    for dx, dy, r in [(-70, 10, 55), (0, -20, 75), (75, 10, 55), (0, 25, 60)]:
        d.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s], fill=CLOUD)


def rain(d, x0, x1, y0, y1, t, n=14):
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        y = y0 + ((t * 600 + i * 97) % (y1 - y0))
        d.line([(x, y), (x - 8, y + 30)], fill=RAIN, width=5)


def ground(d, y=880):
    d.ellipse([140, y - 120, 940, y + 160], fill=GRASS)
    d.rounded_rectangle([480, y - 90, 600, y + 120], 10, fill=PITCH)
    for dx in (-18, 0, 18):
        d.line([(540 + dx, y - 80), (540 + dx, y - 30)], fill=WHITE, width=6)


def chip(d, xy, s, col, size=60, g=1.0, w=360):
    x, y = xy
    d.rounded_rectangle([x - w / 2, y - 60, x + w / 2, y + 60], 40, fill=col)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    ground(d)
    cloud(d, 540, 560)
    if t > 0.4:
        rain(d, 420, 660, 620, 820, t)
    g = pop(prog(t, 0.9, 0.4))
    chip(d, (300, 1080), "affect?", th["accent"], 58, g, 340)
    chip(d, (780, 1080), "effect?", th["accent"], 58, g, 340)
    text_c(d, (540, 360), "Rain will ___ the match", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 380), "AFFECT", font(int(110 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        chip(d, (540, 560), "usually a VERB", WHITE, 54, g2, 560)
    if t > 1.2:
        # rain (doer) -> arrow -> match (changed): the action
        cloud(d, 260, 780, 0.8)
        rain(d, 200, 320, 830, 930, t, 5)
        k = ease(prog(t, 1.2, 0.6))
        d.line([(420, 820), (420 + 220 * k, 820)], fill=th["accent"], width=12)
        if k > 0.95:
            d.polygon([(640, 795), (640, 845), (680, 820)], fill=th["accent"])
        for dx in (-22, 0, 22):
            d.line([(800 + dx, 740), (800 + dx, 900)], fill=WHITE, width=10)
        d.line([(770, 735), (830, 735)], fill=WHITE, width=8)
        text_c(d, (540, 1060), "the action: to change something", font(42, "semi"), th["soft"])


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 380), "EFFECT", font(int(110 * g) + 1, "bold"), BLUE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        chip(d, (540, 560), "usually a NOUN", WHITE, 54, g2, 560)
    if t > 1.1:
        g3 = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([230, 690, 850, 940], 30, fill=(255, 255, 255, 35), outline=BLUE, width=5)
        text_c(d, (540, 770), "the result", font(int(64 * g3) + 1, "bold"), WHITE)
        text_c(d, (540, 865), "of the change", font(int(50 * g3) + 1, "semi"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Quick trick", font(62, "bold"), WHITE)
    rows = [("A", "Action", "Affect", th["accent"]), ("E", "End result", "Effect", BLUE)]
    for i, (letter, word, term, col) in enumerate(rows):
        if t > 0.3 + 0.9 * i:
            g = pop(prog(t, 0.3 + 0.9 * i, 0.4))
            y = 560 + i * 280
            d.rounded_rectangle([110, y - 110, 970, y + 110], 50, fill=(255, 255, 255, 30), outline=col, width=5)
            d.ellipse([140, y - 75, 290, y + 75], fill=col)
            text_c(d, (215, y), letter, font(int(90 * g) + 1, "bold"), DARK)
            text_c(d, (620, y - 35), word, font(int(56 * g) + 1, "bold"), WHITE)
            text_c(d, (620, y + 45), "→ " + term, font(int(48 * g) + 1, "sym"), col)


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.4))
    d.rounded_rectangle([90, 400, 990, 600], 40, fill=(255, 255, 255, 30))
    text_c(d, (540, 500), "Rain affects the match.", font(int(58 * g) + 1, "bold"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([90, 700, 990, 900], 40, fill=(255, 255, 255, 30))
        text_c(d, (540, 800), "The effect? No match!", font(int(58 * g2) + 1, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 1000), "affects = verb   ·   effect = noun", font(40, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Affect does.", font(int(84 * g) + 1, "bold"), th["accent"])
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 720), "Effect is what", font(int(70 * g2) + 1, "bold"), BLUE)
        text_c(d, (540, 820), "you get.", font(int(70 * g2) + 1, "bold"), BLUE)


SCENES = [
    dict(say="Rain will affect the match. Or is it effect? Lots of people mix these two up.", draw=s1),
    dict(say="Affect is usually a verb. It's the action, to change something.", draw=s2),
    dict(say="Effect is usually a noun. It's the result of that change.", draw=s3),
    dict(say="Quick trick: A for action, affect. E for end result, effect.", draw=s4),
    dict(say="So, rain affects the match. And the effect? No match today.", draw=s5),
    dict(say="Affect does. Effect is what you get.", draw=s6),
]
