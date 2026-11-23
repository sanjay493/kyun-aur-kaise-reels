from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Practice or practise?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GREEN, RED, BLUE, ICE = (110, 220, 140), (255, 110, 110), (120, 190, 255), (200, 235, 255)


def bat(d, x, y, s=1.0):
    d.rounded_rectangle([x - 28 * s, y - 160 * s, x + 28 * s, y + 60 * s], int(18 * s), fill=(235, 205, 150))
    d.rounded_rectangle([x - 10 * s, y + 55 * s, x + 10 * s, y + 140 * s], int(6 * s), fill=(120, 80, 50))


def ball(d, x, y, r=34):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(220, 50, 50))
    d.arc([x - r * 0.6, y - r, x + r * 0.6, y + r], 100, 260, fill=WHITE, width=3)


def chip(d, x, y, s, col, size=60, g=1.0, w=420):
    d.rounded_rectangle([x - w / 2, y - 60, x + w / 2, y + 60], 40, fill=col)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), DARK)


def word(d, x, y, stem, letter, tail, col, size=96):
    """Draw stem+letter+tail centred, with `letter` coloured."""
    f = font(size, "bold")
    full = stem + letter + tail
    w = d.textlength(full, font=f)
    x0 = x - w / 2
    d.text((x0, y), stem, font=f, fill=WHITE, anchor="lm")
    x1 = x0 + d.textlength(stem, font=f)
    d.text((x1, y), letter, font=f, fill=col, anchor="lm")
    d.text((x1 + d.textlength(letter, font=f), y), tail, font=f, fill=WHITE, anchor="lm")


def s1(img, d, t, T, th):
    bat(d, 420, 640)
    ball(d, 650, 560)
    g = pop(prog(t, 0.5, 0.4))
    chip(d, 300, 940, "practice", th["accent"], 56, g, 380)
    chip(d, 780, 940, "practise", th["accent"], 56, g, 380)
    if t > 1.3:
        text_c(d, (540, 1090), "both are real words!", font(50, "bold"), GREEN)
    text_c(d, (540, 350), "Cricket ___?", font(62, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "British English", font(54, "bold"), th["soft"])
    g = pop(prog(t, 0.1, 0.4))
    word(d, 540, 490, "practi", "c", "e", th["accent"], int(100 * g) + 1)
    if t > 0.6:
        chip(d, 540, 650, "NOUN: a thing", WHITE, 54, pop(prog(t, 0.6, 0.4)), 520)
    if t > 1.2:
        text_c(d, (540, 820), "cricket practice", font(54, "semi"), WHITE)
        text_c(d, (540, 910), "piano practice", font(54, "semi"), WHITE)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.4))
    word(d, 540, 460, "practi", "s", "e", BLUE, int(100 * g) + 1)
    if t > 0.6:
        chip(d, 540, 620, "VERB: doing it", WHITE, 54, pop(prog(t, 0.6, 0.4)), 520)
    if t > 1.1:
        g2 = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([110, 780, 970, 940], 40, fill=(255, 255, 255, 30), outline=BLUE, width=5)
        text_c(d, (540, 860), "I practise every day.", font(int(58 * g2) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Same pattern", font(62, "bold"), th["accent"])
    rows = [("advi", "c", "e", "noun", th["accent"]), ("advi", "s", "e", "verb", BLUE)]
    for i, (a, b, c, lab, col) in enumerate(rows):
        if t > 0.3 + 0.6 * i:
            g = pop(prog(t, 0.3 + 0.6 * i, 0.4))
            y = 560 + i * 240
            d.rounded_rectangle([140, y - 90, 940, y + 90], 40, fill=(255, 255, 255, 30), outline=col, width=5)
            word(d, 420, y, a, b, c, col, int(84 * g) + 1)
            text_c(d, (780, y), lab, font(int(56 * g) + 1, "bold"), col)
    if t > 1.6:
        text_c(d, (540, 1060), "Good advice. I advise you.", font(46, "semi"), th["soft"])


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Easy trick", font(62, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    # an ice cube
    s = 1.0 * g
    d.rounded_rectangle([540 - 110 * s, 470, 540 + 110 * s, 470 + 220 * s], int(30 * s) + 1, fill=ICE, outline=WHITE, width=5)
    text_c(d, (540, 470 + 110 * s), "ICE", font(int(64 * g) + 1, "bold"), DARK)
    if t > 0.7:
        text_c(d, (540, 790), "ICE is a noun", font(60, "bold"), WHITE)
    if t > 1.3:
        word(d, 540, 920, "advi", "ce", "", ICE, 64)
        word(d, 540, 1030, "practi", "ce", "", ICE, 64)


def s6(img, d, t, T, th):
    text_c(d, (540, 350), "American English?", font(60, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.45))
    word(d, 540, 560, "practi", "c", "e", th["accent"], int(100 * g) + 1)
    if t > 0.7:
        text_c(d, (540, 720), "for both noun and verb", font(52, "bold"), th["soft"])


def s7(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 540), "A thing? C.", font(int(86 * g) + 1, "bold"), th["accent"])
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 760), "Doing it? S.", font(int(86 * g2) + 1, "bold"), BLUE)


SCENES = [
    dict(say="Cricket practice or cricket practise? Both are real words.", draw=s1),
    dict(say="In British English, practice with a C is the noun, like cricket practice.", draw=s2),
    dict(say="Practise with an S is the verb. I practise every day.", draw=s3),
    dict(say="Same pattern as advice and advise. Advice is the noun, advise is the verb.", draw=s4),
    dict(say="Easy trick: ice is a noun. Advice and practice are nouns.", draw=s5),
    dict(say="American English uses practice for both.", draw=s6),
    dict(say="A thing? C. Doing it? S.", draw=s7),
]
