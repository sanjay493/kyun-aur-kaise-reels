import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Lose or loose?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GREEN, RED, BLUE, PINK = (110, 220, 140), (255, 110, 110), (120, 190, 255), (255, 150, 200)
PHONE, SCREEN, SHIRT = (40, 45, 60), (90, 110, 150), (120, 190, 255)


def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 70 * s, y - 130 * s, x + 70 * s, y + 130 * s], int(22 * s) + 1, fill=PHONE)
    d.rounded_rectangle([x - 58 * s, y - 115 * s, x + 58 * s, y + 115 * s], int(14 * s) + 1, fill=SCREEN)


def shirt(d, x, y, s=1.0, col=SHIRT):
    w, h = 150 * s, 190 * s
    d.polygon([(x - w, y - h + 40 * s), (x - w * 0.45, y - h), (x + w * 0.45, y - h), (x + w, y - h + 40 * s),
               (x + w * 0.8, y - h + 120 * s), (x + w * 0.6, y - h + 100 * s), (x + w * 0.6, y + h * 0.8),
               (x - w * 0.6, y + h * 0.8), (x - w * 0.6, y - h + 100 * s), (x - w * 0.8, y - h + 120 * s)], fill=col)


def word(d, x, y, stem, mid, tail, col, size=110):
    f = font(size, "bold")
    full = stem + mid + tail
    x0 = x - d.textlength(full, font=f) / 2
    d.text((x0, y), stem, font=f, fill=WHITE, anchor="lm")
    x1 = x0 + d.textlength(stem, font=f)
    d.text((x1, y), mid, font=f, fill=col, anchor="lm")
    d.text((x1 + d.textlength(mid, font=f), y), tail, font=f, fill=WHITE, anchor="lm")


def s1(img, d, t, T, th):
    phone(d, 540, 620)
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([90, 840, 990, 980], 40, fill=(255, 255, 255, 35))
    text_c(d, (540, 910), "\"Don't loose your phone!\"", font(int(54 * g) + 1, "bold"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 1080), "Spot the mistake?", font(int(56 * g2) + 1, "bold"), th["accent"])
    text_c(d, (540, 350), "Read this:", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    word(d, 540, 420, "l", "o", "se", th["accent"], int(120 * g) + 1)
    text_c(d, (540, 540), "one O · a VERB", font(50, "bold"), th["accent"])
    if t > 0.8:
        phone(d, 330, 800, 0.7)
        text_c(d, (330, 1000), "lose your phone", font(40, "bold"), WHITE)
    if t > 1.4:
        d.rounded_rectangle([620, 720, 900, 880], 30, fill=(255, 255, 255, 35))
        text_c(d, (760, 800), "2 – 3", font(70, "bold"), RED)
        text_c(d, (760, 1000), "lose a match", font(40, "bold"), WHITE)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    word(d, 540, 420, "l", "oo", "se", BLUE, int(120 * g) + 1)
    text_c(d, (540, 540), "two Os · not tight", font(50, "bold"), BLUE)
    if t > 0.8:
        k = ease(prog(t, 0.8, 0.6))
        shirt(d, 330, 820, 0.7 + 0.25 * k)
        text_c(d, (330, 1060), "a loose shirt", font(40, "bold"), WHITE)
    if t > 1.4:
        d.rounded_rectangle([640, 880, 880, 940], 30, fill=(230, 120, 130))  # gum
        tx = 760 + 10 * math.sin(t * 12)  # wobbling tooth
        d.rounded_rectangle([tx - 60, 700, tx + 60, 820], 40, fill=WHITE)
        d.polygon([(tx - 55, 790), (tx - 40, 900), (tx - 10, 900), (tx, 830), (tx + 10, 900), (tx + 40, 900), (tx + 55, 790)], fill=WHITE)
        for sx in (-1, 1):
            d.arc([tx + sx * 90 - 30, 720, tx + sx * 90 + 30, 800], 120 if sx < 0 else -60, 240 if sx < 0 else 60, fill=th["accent"], width=6)
        text_c(d, (760, 1060), "a loose tooth", font(40, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "They sound different", font(58, "bold"), WHITE)
    rows = [("lose", "rhymes with choose", th["accent"]), ("loose", "rhymes with goose", BLUE)]
    for i, (w, r, col) in enumerate(rows):
        if t > 0.3 + 0.8 * i:
            g = pop(prog(t, 0.3 + 0.8 * i, 0.4))
            y = 560 + i * 280
            d.rounded_rectangle([110, y - 110, 970, y + 110], 50, fill=(255, 255, 255, 30), outline=col, width=5)
            text_c(d, (540, y - 40), w, font(int(76 * g) + 1, "bold"), col)
            text_c(d, (540, y + 50), r, font(int(46 * g) + 1, "semi"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Memory trick", font(62, "bold"), th["accent"])
    k = ease(prog(t, 0.3, 0.8))
    shirt(d, 540, 640, 0.7 + 0.25 * k)
    word(d, 540, 890, "l", "oo", "se", th["accent"], 100)
    if t > 1.1:
        g = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([150, 980, 930, 1110], 50, fill=th["accent"])
        text_c(d, (540, 1045), "extra O = extra room", font(int(56 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 480), "Lost something?", font(int(66 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 580), "One O: lose", font(int(72 * g) + 1, "bold"), th["accent"])
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 800), "Not tight?", font(int(66 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 900), "Two Os: loose", font(int(72 * g2) + 1, "bold"), BLUE)


SCENES = [
    dict(say="Don't loose your phone. Spot the mistake?", show="\"Don't loose your phone.\" Spot the mistake?", draw=s1),
    dict(say="Lose, with one O, is a verb. To lose your phone, or lose a match.", draw=s2),
    dict(say="Loose, with two O's, usually means not tight. A loose shirt, a loose tooth.",
         show="Loose, with two Os, usually means not tight. A loose shirt, a loose tooth.", draw=s3),
    dict(say="They sound different too. Lose rhymes with choose. Loose rhymes with goose.", draw=s4),
    dict(say="Trick: loose has an extra O, like the extra room in a loose shirt.", draw=s5),
    dict(say="Lost something? One O. Not tight? Two O's.", show="Lost something? One O. Not tight? Two Os.", draw=s6),
]
