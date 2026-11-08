from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Is 0.999... less than 1?"
WHITE, DARK = (255, 255, 255), (20, 24, 50)
RED, GREEN = (240, 90, 90), (90, 210, 130)


def card(d, x0, y0, x1, y1, th, a=40):
    d.rounded_rectangle([x0, y0, x1, y1], 40, fill=(255, 255, 255, a), outline=th["accent"], width=5)


def nines(t, start, n_max=9, rate=6.0):
    """0.9, 0.99, ... grows while the scene runs, ending in an ellipsis."""
    n = 1 + int(clamp((t - start) * rate / n_max) * (n_max - 1))
    return "9" * n


def s1(img, d, t, T, th):
    k = nines(t, 0.1)
    text_c(d, (540, 520), "0." + k + "...", font(96, "bold"), th["accent"])
    text_c(d, (540, 640), "nines forever", font(44, "semi"), th["soft"])
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (330, 880), "0.999...", font(int(80 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 880), "<", font(int(90 * g) + 1, "bold"), RED)
        text_c(d, (720, 880), "1", font(int(96 * g) + 1, "bold"), WHITE)
        text_c(d, (850, 880), "?", font(int(90 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    card(d, 120, 380, 960, 1120, th)
    text_c(d, (540, 520), "x = 0.999...", font(78, "bold"), WHITE)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        text_c(d, (540, 650), "× 10", font(int(50 * g) + 1, "semi"), th["soft"])
        text_c(d, (540, 800), "10x = 9.999...", font(int(78 * g) + 1, "bold"), th["accent"])
    if t > 1.8:
        text_c(d, (540, 960), "still nines forever", font(46, "semi"), WHITE)


def s3(img, d, t, T, th):
    card(d, 120, 360, 960, 1140, th)
    text_c(d, (540, 470), "10x = 9.999...", font(70, "bold"), WHITE)
    text_c(d, (540, 590), "-  x = 0.999...", font(70, "bold"), WHITE)
    k = ease(prog(t, 0.6, 0.6))
    if k > 0:
        # strike the matching endless tails
        d.line([(640, 470), (640 + 200 * k, 470)], fill=RED, width=8)
        d.line([(640, 590), (640 + 200 * k, 590)], fill=RED, width=8)
    d.line([(200, 670), (880, 670)], fill=WHITE, width=5)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 790), "9x = 9", font(int(96 * g) + 1, "bold"), th["accent"])
    if t > 2.0:
        text_c(d, (540, 960), "the nines cancel", font(48, "semi"), th["soft"])


def s4(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "x = 1", font(int(150 * g) + 1, "bold"), th["accent"], stroke_width=4, stroke_fill=DARK)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([250, 820, 830, 950], 40, fill=GREEN)
        text_c(d, (540, 885), "exactly, not almost", font(int(54 * g2) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    card(d, 100, 360, 980, 1150, th)
    text_c(d, (540, 470), "1/3 = 0.333...", font(76, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 630), "× 3", font(int(50 * g) + 1, "semi"), th["soft"])
        text_c(d, (540, 770), "3/3 = 0.999...", font(int(76 * g) + 1, "bold"), WHITE)
    if t > 2.0:
        g2 = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 960), "and 3/3 = 1", font(int(76 * g2) + 1, "bold"), th["accent"])


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    card(d, 90, 360, W - 90, 1100, th, 30)
    text_c(d, (540, 560), "0.999...  =  1", font(int(96 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 760), "two ways to write", font(int(60 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 860), "the same number", font(int(60 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Point nine nine nine, with nines forever. Is it just less than one?",
         show="0.999..., with nines forever. Is it just less than 1?", draw=s1),
    dict(say="Call it x. Ten x is nine point nine nine nine, forever.",
         show="Call it x. 10x is 9.999..., forever.", draw=s2),
    dict(say="Subtract x. The endless nines cancel, so nine x is nine.",
         show="Subtract x. The endless nines cancel, so 9x = 9.", draw=s3),
    dict(say="So x is exactly one. Not almost.", show="So x is exactly 1. Not almost.", draw=s4),
    dict(say="Check: one third is point three three three, forever. Times three: point nine nine nine. And three thirds is one.",
         show="Check: 1/3 is 0.333..., forever. Times 3: 0.999... And three thirds is 1.", draw=s5),
    dict(say="Two ways to write the same number.", draw=s6),
]
