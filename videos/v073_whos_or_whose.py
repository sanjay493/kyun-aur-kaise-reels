from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Who's or whose?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GREEN, RED, BLUE = (110, 220, 140), (255, 110, 110), (120, 190, 255)
BAG, BAG2, LADDOO = (230, 120, 60), (180, 85, 40), (250, 175, 60)


def bag(d, x, y, s=1.0):
    d.arc([x - 70 * s, y - 210 * s, x + 70 * s, y - 70 * s], 180, 360, fill=BAG2, width=int(18 * s) + 1)
    d.rounded_rectangle([x - 150 * s, y - 140 * s, x + 150 * s, y + 150 * s], int(40 * s) + 1, fill=BAG)
    d.rounded_rectangle([x - 100 * s, y + 10 * s, x + 100 * s, y + 110 * s], int(20 * s) + 1, fill=BAG2)


def chip(d, x, y, s, col, size=56, g=1.0, w=380):
    d.rounded_rectangle([x - w / 2, y - 60, x + w / 2, y + 60], 40, fill=col)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), DARK)


def mark(d, x, y, ok, g=1.0):
    text_c(d, (x, y), "✓" if ok else "✗", font(int(90 * g) + 1, "sym"), GREEN if ok else RED)


def s1(img, d, t, T, th):
    bag(d, 540, 680)
    text_c(d, (540, 400), "___ bag is this?", font(62, "bold"), WHITE)
    g = pop(prog(t, 0.6, 0.4))
    chip(d, 300, 1000, "Who's?", th["accent"], 58, g, 340)
    chip(d, 780, 1000, "Whose?", th["accent"], 58, g, 340)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 400), "WHO'S", font(int(110 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        chip(d, 540, 560, "= who is / who has", WHITE, 50, g2, 620)
    if t > 1.3:
        d.rounded_rectangle([110, 700, 970, 820], 40, fill=(255, 255, 255, 30))
        text_c(d, (540, 760), "Who's coming?  (who is)", font(48, "bold"), WHITE)
    if t > 2.0:
        d.rounded_rectangle([110, 860, 970, 980], 40, fill=(255, 255, 255, 30))
        text_c(d, (540, 920), "Who's eaten my laddoo?  (who has)", font(42, "bold"), WHITE)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 400), "WHOSE", font(int(110 * g) + 1, "bold"), BLUE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        chip(d, 540, 560, "= belonging to whom", WHITE, 50, g2, 640)
    if t > 1.0:
        bag(d, 540, 850, 0.6)
        text_c(d, (540, 1080), "Whose bag is this?", font(52, "bold"), BLUE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "The test: say \"who is\"", font(56, "bold"), th["accent"])
    g = pop(prog(t, 0.3, 0.4))
    d.rounded_rectangle([90, 450, 990, 610], 40, fill=(255, 255, 255, 30))
    text_c(d, (540, 530), "\"Who is bag is this?\"", font(int(58 * g) + 1, "bold"), WHITE)
    if t > 1.0:
        mark(d, 540, 700, False, pop(prog(t, 1.0, 0.4)))
        text_c(d, (540, 800), "makes no sense", font(48, "semi"), RED)
    if t > 1.6:
        g2 = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([170, 900, 910, 1040], 50, fill=GREEN)
        text_c(d, (540, 970), "so: WHOSE bag", font(int(60 * g2) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "No apostrophe here", font(58, "bold"), WHITE)
    words = ["his", "her", "its", "whose"]
    for i, w in enumerate(words):
        if t > 0.2 + 0.3 * i:
            g = pop(prog(t, 0.2 + 0.3 * i, 0.35))
            x, y = 300 + (i % 2) * 480, 560 + (i // 2) * 220
            col = BLUE if w == "whose" else WHITE
            d.rounded_rectangle([x - 190, y - 80, x + 190, y + 80], 40, fill=(255, 255, 255, 30), outline=col, width=5)
            text_c(d, (x, y), w, font(int(70 * g) + 1, "bold"), col)
    if t > 1.6:
        text_c(d, (540, 1060), "possessives skip the '", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 470), "Can you say \"who is\"?", font(int(58 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 580), "Who's.", font(int(86 * g) + 1, "bold"), th["accent"])
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 780), "Can't?", font(int(62 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 890), "Whose.", font(int(86 * g2) + 1, "bold"), BLUE)


SCENES = [
    dict(say="Whose bag is this? Or who's bag? Only one is right.",
         show="\"Whose bag is this?\" Or \"who's bag\"? Only one is right.", draw=s1),
    dict(say="Who's, with an apostrophe, is short for who is, or who has. Who's coming? Who's eaten my laddoo?", draw=s2),
    dict(say="Whose means belonging to whom. Whose bag is this?", draw=s3),
    dict(say="Test: swap in who is. Who is bag is this? Makes no sense. So, whose.",
         show="Test: swap in \"who is\". \"Who is bag is this?\" Makes no sense. So, whose.", draw=s4),
    dict(say="Like his, her and its, whose has no apostrophe.", draw=s5),
    dict(say="Can you say who is? Who's. Can't? Whose.", show="Can you say \"who is\"? Who's. Can't? Whose.", draw=s6),
]
