from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Guess first, then learn"
WHITE, DARK = (255, 255, 255), (20, 30, 50)
PAPER, LINE = (245, 245, 238), (175, 180, 195)
GREEN, RED, AMBER, BLUE = (110, 220, 140), (255, 110, 110), (255, 200, 90), (120, 190, 255)


def page(d, x0, y0, w, h, rows=7):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 20, fill=PAPER)
    for i in range(rows):
        y = y0 + 60 + i * (h - 100) / (rows - 1)
        ln = w - 80 - (60 if i % 3 == 2 else 0)
        d.line([(x0 + 40, y), (x0 + 40 + ln, y)], fill=LINE, width=8)


def qcard(d, x, y, g=1.0, mark=None):
    d.rounded_rectangle([x - 120 * g, y - 70 * g, x + 120 * g, y + 70 * g], 24, fill=WHITE)
    text_c(d, (x - 40, y), "Q?", font(int(50 * g) + 1, "bold"), DARK)
    if mark is not None and g > 0.9:
        text_c(d, (x + 60, y), "✗" if mark is False else "✓", font(60, "sym"), RED if mark is False else GREEN)


def s1(img, d, t, T, th):
    text_c(d, (540, 350), "New chapter tomorrow?", font(58, "bold"), WHITE)
    page(d, 300, 450, 480, 520)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        d.rounded_rectangle([170, 1020, 910, 1150], 50, fill=th["accent"])
        text_c(d, (540, 1085), "Try its questions first", font(int(52 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "An experiment", font(62, "bold"), th["accent"])
    page(d, 300, 460, 480, 500)
    g = pop(prog(t, 0.3, 0.4))
    # an eye drawn on the page
    d.ellipse([440 - 60 * g, 600, 640 + 60 * g, 720], fill=WHITE, outline=DARK, width=6)
    d.ellipse([505, 625, 575, 695], fill=BLUE)
    d.ellipse([525, 645, 555, 675], fill=DARK)
    if t > 0.9:
        text_c(d, (540, 1060), "college students read an essay about vision", font(40, "semi"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Group 1: test first", font(58, "bold"), th["accent"])
    for i in range(4):
        if t > 0.2 + 0.25 * i:
            g = pop(prog(t, 0.2 + 0.25 * i, 0.35))
            qcard(d, 300 + (i % 2) * 480, 560 + (i // 2) * 220, g, mark=False if t > 1.4 else None)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([170, 960, 910, 1090], 50, fill=RED)
        text_c(d, (540, 1025), "almost all wrong!", font(int(56 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Group 2: just study", font(58, "bold"), BLUE)
    page(d, 300, 450, 480, 520)
    k = ease(prog(t, 0.2, 1.2))
    d.rounded_rectangle([300, 1020, 780, 1060], 20, fill=(255, 255, 255, 40))
    d.rounded_rectangle([300, 1020, 300 + 480 * k, 1060], 20, fill=BLUE)
    text_c(d, (540, 1120), "same extra time", font(40, "semi"), th["soft"])


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Final test", font(62, "bold"), WHITE)
    rows = [("guessed first", 0.75, th["accent"]), ("just studied", 0.56, BLUE)]
    for i, (lab, v, col) in enumerate(rows):
        k = ease(prog(t, 0.2 + 0.3 * i, 0.8))
        y = 560 + i * 260
        text_c(d, (130, y - 70), lab, font(46, "bold"), WHITE, anchor="lm")
        d.rounded_rectangle([130, y - 30, 130 + 820 * v * k, y + 40], 20, fill=col)
        if k > 0.8:
            text_c(d, (150 + 820 * v * k, y + 5), f"{int(v * 100)}%", font(48, "bold"), col, anchor="lm")
    if t > 1.6:
        text_c(d, (540, 1110), "Experiment 1 scores", font(36, "reg"), th["soft"])


def s6(img, d, t, T, th):
    text_c(d, (540, 350), "The key step", font(62, "bold"), th["accent"])
    qcard(d, 330, 620, 1.0, mark=False)
    k = ease(prog(t, 0.3, 0.6))
    d.line([(470, 620), (470 + 140 * k, 620)], fill=WHITE, width=10)
    if k > 0.95:
        d.polygon([(610, 598), (610, 642), (645, 620)], fill=WHITE)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        d.rounded_rectangle([660, 540, 960, 700], 30, fill=GREEN)
        text_c(d, (810, 620), "answer", font(int(52 * g) + 1, "bold"), DARK)
        text_c(d, (540, 900), "check the right answer", font(54, "bold"), WHITE)
        text_c(d, (540, 980), "straight after", font(54, "bold"), WHITE)


def s7(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Guess first.", font(int(90 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 760), "Then learn.", font(int(90 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Before reading a chapter, try its questions. Even if you get them wrong.", draw=s1),
    dict(say="In one experiment, college students read an essay about vision.", draw=s2),
    dict(say="Some first tried test questions on it. They got almost all of them wrong.", draw=s3),
    dict(say="Others just spent that time studying.", draw=s4),
    dict(say="On the final test, the guessers did better: seventy five percent versus fifty six.",
         show="On the final test, the guessers did better: 75% versus 56%.", draw=s5),
    dict(say="The key: check the right answers straight after.", draw=s6),
    dict(say="Guess first. Then learn.", draw=s7),
]
