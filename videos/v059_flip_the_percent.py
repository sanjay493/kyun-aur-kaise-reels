from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "8% of 50? Flip it!"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
GREEN, RED, PINK, BLUE = (110, 220, 140), (255, 110, 110), (255, 150, 200), (120, 190, 255)


def card(d, x, y, s, col, g=1.0, w=420, size=70):
    d.rounded_rectangle([x - w / 2, y - 80, x + w / 2, y + 80], 40, fill=(255, 255, 255, 35), outline=col, width=5)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), col)


def s1(img, d, t, T, th):
    g = pop(prog(t, 0.2, 0.45))
    text_c(d, (540, 360), "Quick!", font(66, "bold"), th["accent"])
    card(d, 540, 560, "8% of 50", WHITE, g, 640, 96)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 760), "= ?", font(int(110 * g2) + 1, "bold"), RED)
    if t > 1.8:
        g3 = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([240, 930, 840, 1070], 50, fill=th["accent"])
        text_c(d, (540, 1000), "Flip it!", font(int(70 * g3) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.8))
    # the two numbers swap places
    xa, xb = 330 + 420 * k, 750 - 420 * k
    text_c(d, (xa, 480), "8", font(110, "bold"), PINK)
    text_c(d, (xb, 480), "50", font(110, "bold"), BLUE)
    text_c(d, (540, 600), "swap!", font(44, "semi"), th["soft"])
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        card(d, 540, 760, "50% of 8", th["accent"], g, 640, 90)
    if t > 1.7:
        g2 = pop(prog(t, 1.7, 0.4))
        text_c(d, (540, 950), "half of 8", font(int(56 * g2) + 1, "semi"), WHITE)
        text_c(d, (540, 1070), "= 4", font(int(100 * g2) + 1, "bold"), GREEN)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Why?", font(70, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    text_c(d, (540, 460), "percent = out of 100", font(int(54 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([110, 570, 970, 730], 40, fill=(255, 255, 255, 30), outline=PINK, width=5)
        text_c(d, (540, 650), "8% of 50 = 8 × 50 ÷ 100", font(int(52 * g2) + 1, "sym"), WHITE)
    if t > 1.6:
        g3 = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([110, 790, 970, 950], 40, fill=(255, 255, 255, 30), outline=BLUE, width=5)
        text_c(d, (540, 870), "50% of 8 = 50 × 8 ÷ 100", font(int(52 * g3) + 1, "sym"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "Order doesn't matter", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    text_c(d, (540, 560), "8 × 50 = 50 × 8", font(int(84 * g) + 1, "sym"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([240, 720, 840, 860], 50, fill=GREEN)
        text_c(d, (540, 790), "= 400", font(int(70 * g2) + 1, "bold"), DARK)
        text_c(d, (540, 960), "400 ÷ 100 = 4", font(int(60 * g2) + 1, "sym"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Try this one", font(62, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    card(d, 540, 520, "4% of 25", WHITE, g, 640, 86)
    if t > 1.0:
        text_c(d, (540, 660), "↓ flip ↓", font(50, "sym"), th["soft"])
        card(d, 540, 800, "25% of 4", th["accent"], pop(prog(t, 1.0, 0.4)), 640, 86)
    if t > 1.8:
        g2 = pop(prog(t, 1.8, 0.4))
        text_c(d, (540, 1020), "= 1", font(int(110 * g2) + 1, "bold"), GREEN)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Stuck on a", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "percentage?", font(int(72 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        d.rounded_rectangle([250, 790, 830, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "Flip it.", font(int(76 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Quick: eight percent of fifty? Hard? Flip it.",
         show="Quick: 8% of 50? Hard? Flip it.", draw=s1),
    dict(say="It's the same as fifty percent of eight. Half of eight: four.",
         show="It's the same as 50% of 8. Half of 8: 4.", draw=s2),
    dict(say="Why? Percent means out of a hundred. Both are eight times fifty, divided by a hundred.",
         show="Why? Percent means out of 100. Both are 8 × 50 ÷ 100.", draw=s3),
    dict(say="And you can multiply in any order. Same answer.", draw=s4),
    dict(say="Try four percent of twenty five. Flip it: twenty five percent of four. One!",
         show="Try 4% of 25. Flip it: 25% of 4. One!", draw=s5),
    dict(say="Stuck on a percentage? Flip it.", draw=s6),
]
