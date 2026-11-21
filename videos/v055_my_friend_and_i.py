from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "My friend and I, or my friend and me?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GREEN, RED, PINK, BLUE = (110, 220, 140), (255, 110, 110), (255, 150, 200), (120, 190, 255)


def kid(d, x, y, col, s=1.0):
    r = 40 * s
    d.ellipse([x - r, y - 2.6 * r, x + r, y - 0.6 * r], fill=(255, 215, 170))
    d.rounded_rectangle([x - 1.2 * r, y - 0.5 * r, x + 1.2 * r, y + 1.6 * r], int(0.6 * r), fill=col)


def line_box(d, y, words, g=1.0, strike=None, col=WHITE, size=54):
    """Sentence in a soft box; `strike` = substring drawn crossed out (removed)."""
    d.rounded_rectangle([70, y - 75, W - 70, y + 75], 40, fill=(255, 255, 255, 30))
    f = font(int(size * g) + 1, "bold")
    text_c(d, (540, y), words, f, col)
    if strike and g > 0.9:
        full = d.textlength(words, font=f)
        x0 = 540 - full / 2 + d.textlength(words.split(strike)[0], font=f)
        x1 = x0 + d.textlength(strike, font=f)
        d.line([(x0, y), (x1, y)], fill=RED, width=8)


def mark(d, x, y, ok, g=1.0):
    text_c(d, (x, y), "✓" if ok else "✗", font(int(90 * g) + 1, "sym"), GREEN if ok else RED)


def s1(img, d, t, T, th):
    kid(d, 420, 700, PINK)
    kid(d, 660, 700, BLUE)
    g = pop(prog(t, 0.6, 0.4))
    d.rounded_rectangle([110, 860, 520, 980], 40, fill=(255, 255, 255, 40), outline=th["accent"], width=5)
    d.rounded_rectangle([560, 860, 970, 980], 40, fill=(255, 255, 255, 40), outline=th["accent"], width=5)
    text_c(d, (315, 920), "...and I?", font(int(58 * g) + 1, "bold"), WHITE)
    text_c(d, (765, 920), "...and me?", font(int(58 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 360), "Me and my friend went out...", font(54, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Take the friend out", font(60, "bold"), th["accent"])
    line_box(d, 520, "Me went out.", pop(prog(t, 0.3, 0.4)))
    if t > 0.8:
        mark(d, 540, 650, False, pop(prog(t, 0.8, 0.4)))
    if t > 1.3:
        line_box(d, 820, "I went out.", pop(prog(t, 1.3, 0.4)))
        mark(d, 540, 950, True, pop(prog(t, 1.6, 0.4)))
    if t > 2.0:
        text_c(d, (540, 1110), "My friend and I went.", font(54, "bold"), GREEN)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Now this one", font(60, "bold"), th["accent"])
    line_box(d, 520, "Mummy called my friend and I.", pop(prog(t, 0.2, 0.4)), size=48)
    if t > 0.9:
        line_box(d, 760, "Mummy called I?", pop(prog(t, 0.9, 0.4)))
        mark(d, 540, 890, False, pop(prog(t, 1.2, 0.4)))
    if t > 1.7:
        g = pop(prog(t, 1.7, 0.4))
        d.rounded_rectangle([200, 1000, 880, 1130], 50, fill=GREEN)
        text_c(d, (540, 1065), "Mummy called me.", font(int(56 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([70, 450, W - 70, 650], 40, fill=(255, 255, 255, 30), outline=GREEN, width=5)
    text_c(d, (540, 550), "Mummy called my friend and me.", font(int(46 * g) + 1, "bold"), WHITE)
    if t > 0.8:
        mark(d, 540, 760, True, pop(prog(t, 0.8, 0.4)))
    if t > 1.2:
        text_c(d, (540, 920), "I = does the action", font(50, "bold"), th["accent"])
        text_c(d, (540, 1010), "me = gets the action", font(50, "bold"), BLUE)


def s5(img, d, t, T, th):
    text_c(d, (540, 360), "Polite order", font(62, "bold"), th["accent"])
    kid(d, 380, 720, BLUE, 1.2)
    kid(d, 700, 720, PINK, 1.2)
    if t > 0.5:
        g = pop(prog(t, 0.5, 0.4))
        text_c(d, (380, 900), "1st: friend", font(int(46 * g) + 1, "bold"), WHITE)
        text_c(d, (700, 900), "2nd: me / I", font(int(46 * g) + 1, "bold"), WHITE)
    if t > 1.2:
        text_c(d, (540, 1060), "name the other person first", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Remove the friend.", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 740), "What sounds right", font(int(66 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 840), "stays right.", font(int(66 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Me and my friend went out. Or is it my friend and I?", draw=s1),
    dict(say="Take your friend out. Me went? No. I went. So, my friend and I went.", draw=s2),
    dict(say="Now: Mummy called my friend and I. Remove the friend. Mummy called I? No. Mummy called me.", draw=s3),
    dict(say="So, Mummy called my friend and me.", draw=s4),
    dict(say="And to be polite, name the other person first.", draw=s5),
    dict(say="Remove the friend. What sounds right stays right.", draw=s6),
]
