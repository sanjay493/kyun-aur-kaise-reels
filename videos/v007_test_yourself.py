import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Does rereading your chapter actually work?"
BLUE, ORANGE, WHITE, DARK = (110, 215, 255), (255, 170, 80), (255, 255, 255), (25, 30, 50)


def book(d, cx, cy, s=1.0, col=(255, 120, 120), open_=True):
    if open_:
        d.polygon([(cx, cy - 10 * s), (cx - 170 * s, cy - 40 * s), (cx - 170 * s, cy + 110 * s), (cx, cy + 140 * s)],
                  fill=(250, 250, 245), outline=col)
        d.polygon([(cx, cy - 10 * s), (cx + 170 * s, cy - 40 * s), (cx + 170 * s, cy + 110 * s), (cx, cy + 140 * s)],
                  fill=(240, 240, 235), outline=col)
        for k in range(4):
            y = cy + (5 + k * 28) * s
            d.line([(cx - 145 * s, y - 20 * s), (cx - 25 * s, y)], fill=(170, 175, 190), width=int(5 * s) + 1)
            d.line([(cx + 25 * s, y), (cx + 145 * s, y - 20 * s)], fill=(170, 175, 190), width=int(5 * s) + 1)
        d.line([(cx, cy - 10 * s), (cx, cy + 140 * s)], fill=col, width=int(6 * s) + 1)
    else:
        d.rounded_rectangle([cx - 120 * s, cy - 90 * s, cx + 120 * s, cy + 90 * s], int(14 * s), fill=col,
                            outline=WHITE, width=5)
        d.rectangle([cx - 120 * s, cy + 60 * s, cx + 120 * s, cy + 75 * s], fill=(250, 250, 245))


def s1(img, d, t, T, th):
    book(d, 540, 560, 1.5)
    # eyes sweeping over pages again and again
    k = (t * 1.2) % 1.0
    x = 330 + 420 * k
    d.ellipse([x - 22, 500, x + 22, 544], fill=(255, 255, 255, 200), outline=BLUE, width=5)
    n = min(3, 1 + int(t / 0.9))
    text_c(d, (540, 900), " → ".join(["READ"] + ["again"] * (n - 1)), font(60, "sym"), WHITE,
           stroke_width=5, stroke_fill=DARK)
    g = pop(prog(t, 2.2, 0.4))
    if g > 0:
        text_c(d, (540, 1060), "Does it work?", font(int(80 * g) + 1, "bold"), th["accent"], stroke_width=6,
               stroke_fill=DARK)


def chip(d, x, y, label, col, g=1.0):
    w = 110 * g
    d.rounded_rectangle([x - w, y - 42 * g, x + w, y + 42 * g], int(22 * g) + 1, fill=col)
    text_c(d, (x, y), label, font(int(40 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    cols = [(300, "GROUP A", ["READ", "READ", "READ", "READ"]), (780, "GROUP B", ["READ", "TEST", "TEST", "TEST"])]
    for ci, (x, name, steps) in enumerate(cols):
        g0 = pop(prog(t, 0.1 + ci * 0.4, 0.35))
        if g0 <= 0: continue
        text_c(d, (x, 330), name, font(int(52 * g0) + 1, "bold"), WHITE)
        for k, st in enumerate(steps):
            g = pop(prog(t, 0.4 + ci * 0.4 + k * 0.35, 0.3))
            if g > 0:
                chip(d, x, 450 + k * 120, st, BLUE if st == "READ" else ORANGE, g)
    if t > 2.6:
        text_c(d, (540, 1000), "rereading", font(48, "semi"), BLUE, anchor="rm")
        text_c(d, (560, 1000), "vs", font(40, "semi"), th["soft"], anchor="lm")
        text_c(d, (640, 1000), "self-testing", font(48, "semi"), ORANGE, anchor="lm")
    text_c(d, (540, 1100), "a famous memory experiment", font(38, "reg"), th["soft"])


def bars(d, t, a_h, b_h, label, th):
    base = 1000
    text_c(d, (540, 330), label, font(70, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)
    text_c(d, (540, 410), "how much they remembered", font(38, "reg"), th["soft"])
    d.line([(160, base), (920, base)], fill=WHITE, width=6)
    k = ease(prog(t, 0.2, 0.8))
    for x, h, col, name in [(360, a_h, BLUE, "Rereaders"), (720, b_h, ORANGE, "Self-testers")]:
        d.rounded_rectangle([x - 110, base - h * k, x + 110, base], 24, fill=col)
        text_c(d, (x, base + 55), name, font(42, "bold"), WHITE)
    text_c(d, (540, 1140), "(bar heights not to scale)", font(30, "reg"), th["soft"])


def crown(d, x, y):
    d.polygon([(x - 50, y + 30), (x - 50, y - 20), (x - 25, y + 5), (x, y - 35), (x + 25, y + 5), (x + 50, y - 20),
               (x + 50, y + 30)], fill=(255, 215, 70), outline=DARK)


def s3(img, d, t, T, th):
    bars(d, t, 460, 380, "5 minutes later", th)
    if t > 1.1:
        crown(d, 360, 1000 - 460 - 60)


def s4(img, d, t, T, th):
    bars(d, t, 260, 420, "1 week later", th)
    if t > 1.1:
        crown(d, 720, 1000 - 420 - 60)


def s5(img, d, t, T, th):
    # memory path gets thicker each time you pull it out
    cx, cy = 540, 600
    d.ellipse([cx - 230, cy - 190, cx + 230, cy + 190], fill=(255, 170, 200), outline=WHITE, width=6)
    d.arc([cx - 150, cy - 110, cx + 10, cy + 60], 200, 340, fill=(220, 120, 160), width=8)
    d.arc([cx - 20, cy - 40, cx + 160, cy + 120], 190, 330, fill=(220, 120, 160), width=8)
    reps = min(3, int(t / 0.8) + 1)
    wd = 6 + reps * 8
    pts = [(cx - 160, cy + 60), (cx - 60, cy - 30), (cx + 40, cy + 40), (cx + 160, cy - 60)]
    d.line(pts, fill=(255, 230, 90), width=wd, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - wd, p[1] - wd, p[0] + wd, p[1] + wd], fill=(255, 230, 90))
    text_c(d, (540, 880), "Recall it  →  stronger", font(60, "sym"), WHITE, stroke_width=5, stroke_fill=DARK)
    if t > 1.6:
        text_c(d, (540, 990), "Rereading just feels familiar", font(48, "semi"), th["soft"])


def s6(img, d, t, T, th):
    k = ease(prog(t, 0.1, 0.4))
    book(d, 330, 560, 1.0, open_=False)
    if k < 1:
        d.line([(330, 470), (330, 650)], fill=WHITE, width=4)
    g = pop(prog(t, 0.6, 0.45))
    if g > 0:
        x, y = 720, 520
        d.rounded_rectangle([x - 240 * g, y - 130 * g, x + 240 * g, y + 130 * g], int(40 * g) + 1,
                            fill=(255, 255, 255, 240))
        d.polygon([(x - 160 * g, y + 110 * g), (x - 250 * g, y + 190 * g), (x - 90 * g, y + 125 * g)],
                  fill=(255, 255, 255, 240))
        text_c(d, (x, y - 40 * g), "What do I", font(int(52 * g) + 1, "bold"), DARK)
        text_c(d, (x, y + 30 * g), "remember?", font(int(60 * g) + 1, "bold"), (30, 120, 200))
    if t > 1.4:
        d.rounded_rectangle([110, 880, W - 110, 1060], 40, fill=(255, 255, 255, 30), outline=th["accent"], width=5)
        text_c(d, (540, 935), "Test yourself.", font(62, "bold"), th["accent"])
        text_c(d, (540, 1010), "Don't just reread.", font(52, "semi"), WHITE)


SCENES = [
    dict(say="Reading a chapter again and again feels like studying. But does it work?", draw=s1),
    dict(say="In a famous experiment, students learned a short passage. Some kept rereading. Others read once, then tested themselves.", draw=s2),
    dict(say="Five minutes later, the rereaders did better.", draw=s3),
    dict(say="But one week later, the self-testers remembered more.", draw=s4),
    dict(say="Pulling an answer out of memory makes it stronger. Rereading just feels familiar.", draw=s5),
    dict(say="So close the book and ask: what do I remember?", draw=s6),
]
