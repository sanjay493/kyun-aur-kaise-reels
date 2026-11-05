from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "One of my friend or one of my friends?"
WHITE, DARK = (255, 255, 255), (30, 22, 40)
RED, GREEN = (240, 90, 90), (90, 210, 130)
SKINS = [(240, 190, 150), (200, 140, 100), (225, 170, 125), (180, 120, 85), (235, 180, 140)]
SHIRTS = [(110, 170, 255), (255, 150, 120), (150, 220, 140), (230, 150, 230), (255, 210, 110)]


def kid(d, x, y, i, s=1.0, glow=False):
    if glow:
        d.ellipse([x - 95 * s, y - 115 * s, x + 95 * s, y + 175 * s], fill=(255, 210, 110, 70))
    d.rounded_rectangle([x - 55 * s, y + 25 * s, x + 55 * s, y + 150 * s], 30 * s, fill=SHIRTS[i % 5])
    d.ellipse([x - 45 * s, y - 70 * s, x + 45 * s, y + 20 * s], fill=SKINS[i % 5])
    d.chord([x - 48 * s, y - 78 * s, x + 48 * s, y - 5 * s], 180, 360, fill=(35, 25, 25))
    for ex in (-16, 16):
        d.ellipse([x + ex * s - 6 * s, y - 32 * s, x + ex * s + 6 * s, y - 20 * s], fill=DARK)
    d.arc([x - 18 * s, y - 15 * s, x + 18 * s, y + 5 * s], 20, 160, fill=DARK, width=int(4 * s))


def group(d, t, glow_idx=None, y=560, show_until=5):
    xs = [180, 360, 540, 720, 900]
    for i, x in enumerate(xs[:show_until]):
        g = pop(prog(t, 0.1 + i * 0.15, 0.35))
        if g > 0:
            kid(d, x, y, i, 0.95 * g, glow=(i == glow_idx))


def s1(img, d, t, T, th):
    group(d, t, y=480)
    d.rounded_rectangle([80, 780, W - 80, 920], 34, fill=(255, 255, 255, 240))
    f = font(56, "bold")
    full = "One of my friend is coming."
    text_c(d, (540, 850), full, f, DARK)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        x0 = 540 - d.textlength(full, font=f) / 2 + d.textlength("One of my ", font=f)
        x1 = x0 + d.textlength("friend", font=f)
        d.ellipse([x0 - 8, 805, x1 + 8, 895], outline=RED, width=int(8 * g) + 1)
        text_c(d, (540, 1060), "Sounds right? Look again.", font(int(60 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "\"one of\"", font(110, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)
    group(d, t, glow_idx=2 if t > 1.0 else None, y=640)
    k = ease(prog(t, 0.9, 0.5))
    if k > 0:
        d.rounded_rectangle([120, 950, 960, 1090], 34, fill=(255, 255, 255, int(45 * k)))
        text_c(d, (540, 1020), "= one FROM a group", font(60, "bold"), WHITE)


def s3(img, d, t, T, th):
    group(d, t, y=430)
    text_c(d, (540, 700), "a group = MANY", font(64, "bold"), WHITE)
    g = pop(prog(t, 0.9, 0.45))
    if g > 0:
        d.rounded_rectangle([170, 820, 910, 1000], 40, fill=GREEN)
        text_c(d, (540, 910), "friends", font(int(110 * g) + 1, "bold"), DARK)
    if t > 1.6:
        text_c(d, (540, 1100), "plural noun", font(52, "bold"), th["soft"])


def s4(img, d, t, T, th):
    kid(d, 540, 470, 2, 1.4, glow=True)
    text_c(d, (540, 760), "talking about ONE person", font(56, "bold"), WHITE)
    g = pop(prog(t, 1.0, 0.45))
    if g > 0:
        d.rounded_rectangle([290, 850, 790, 1020], 40, fill=th["accent"])
        text_c(d, (540, 935), "is", font(int(120 * g) + 1, "bold"), DARK)
    if t > 1.7:
        text_c(d, (540, 1110), "singular verb", font(52, "bold"), th["soft"])


def s5(img, d, t, T, th):
    rows = [("One of my ", "friends", " is", " coming."), ("One of the ", "boys", " is", " late.")]
    f = font(58, "bold")
    for r, (a, n, v, e) in enumerate(rows):
        g = ease(prog(t, 0.2 + r * 1.2, 0.5))
        if g <= 0:
            continue
        y = 470 + r * 330
        d.rounded_rectangle([70, y - 90, W - 70, y + 90], 34, fill=(255, 255, 255, int(235 * g)))
        full = a + n + v + e
        x = 540 - d.textlength(full, font=f) / 2
        for part, col in ((a, DARK), (n, (40, 150, 80)), (v, (200, 120, 0)), (e, DARK)):
            d.text((x, y), part, font=f, fill=col, anchor="lm")
            x += d.textlength(part, font=f)
    if t > 2.6:
        text_c(d, (540, 1110), "plural noun  +  singular verb", font(48, "bold"), th["accent"])


def s6(img, d, t, T, th):
    group(d, t, glow_idx=None, y=430)
    text_c(d, (540, 670), "1. picture the group", font(56, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        kid(d, 540, 860, 1, 1.0 * g, glow=True)
        text_c(d, (540, 1110), "2. pick ONE from it", font(56, "bold"), th["accent"])


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 480), "One of", font(int(110 * g) + 1, "bold"), WHITE)
    if t > 0.4:
        g2 = pop(prog(t, 0.4, 0.4))
        text_c(d, (540, 690), "many friends,", font(int(100 * g2) + 1, "bold"), GREEN)
    if t > 0.9:
        g3 = pop(prog(t, 0.9, 0.4))
        text_c(d, (540, 900), "one is.", font(int(120 * g3) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="One of my friend is coming. Sounds right? Look again.", draw=s1),
    dict(say="One of means one from a group.", show="\"One of\" means one from a group.", draw=s2),
    dict(say="A group has many friends, so the noun is plural. Friends.",
         show="A group has many friends, so the noun is plural: friends.", draw=s3),
    dict(say="But you're talking about just one person, so the verb stays singular. Is.",
         show="But you're talking about just one person, so the verb stays singular: is.", draw=s4),
    dict(say="One of my friends is coming. One of the boys is late.", draw=s5),
    dict(say="Picture the group first, then pick one from it.", draw=s6),
    dict(say="One of many friends, one is.", show="One of many friends... one is.", draw=s7),
]
