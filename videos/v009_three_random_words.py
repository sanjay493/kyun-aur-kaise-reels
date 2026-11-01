import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Which password is really stronger?"
GREEN, RED, WHITE, DARK = (90, 215, 140), (240, 90, 90), (255, 255, 255), (20, 30, 40)


def field(d, cx, cy, text, col, w=860, g=1.0, fsize=60):
    hw = w / 2 * g
    d.rounded_rectangle([cx - hw, cy - 70 * g, cx + hw, cy + 70 * g], int(30 * g) + 1, fill=(255, 255, 255, 240),
                        outline=col, width=6)
    text_c(d, (cx, cy), text, font(int(fsize * g) + 1, "sym"), DARK)


def lock(d, x, y, s=1.0, col=(255, 140, 60), open_=False):
    d.arc([x - 50 * s, y - 120 * s - (30 * s if open_ else 0), x + 50 * s, y - 20 * s - (30 * s if open_ else 0)],
          180, 360, fill=WHITE, width=int(16 * s))
    d.rounded_rectangle([x - 75 * s, y - 70 * s, x + 75 * s, y + 60 * s], int(20 * s), fill=col)
    d.ellipse([x - 14 * s, y - 25 * s, x + 14 * s, y + 3 * s], fill=DARK)


def s1(img, d, t, T, th):
    g1 = pop(prog(t, 0.1, 0.4))
    if g1 > 0:
        field(d, 540, 450, "Pa55word!", th["accent"], 700, g1, 72)
    g = pop(prog(t, 0.8, 0.3))
    if g > 0:
        text_c(d, (540, 620), "or", font(int(60 * g) + 1, "bold"), WHITE)
    g2 = pop(prog(t, 1.2, 0.4))
    if g2 > 0:
        field(d, 540, 790, "chai kite monsoon", th["accent"], 860, g2, 64)
    if t > 2.0:
        text_c(d, (540, 1020), "Which is stronger?", font(76, "bold"), th["accent"], stroke_width=6, stroke_fill=DARK)


def s2(img, d, t, T, th):
    steps = [("password", None), ("Pa55word", "a→A   s→5"), ("Pa55word!", "+ ! at the end")]
    for k, (s, note) in enumerate(steps):
        g = pop(prog(t, 0.1 + k * 0.7, 0.35))
        if g <= 0: continue
        y = 400 + k * 230
        field(d, 540, y, s, (160, 215, 215), 640, g, 66)
        if note:
            text_c(d, (540, y - 105), note, font(40, "sym"), th["accent"])
    if t > 2.2:
        text_c(d, (540, 1110), "looks \"complex\"...", font(50, "semi"), th["soft"])


def s3(img, d, t, T, th):
    field(d, 540, 420, "Pa55word!", RED, 640, 1.0, 72)
    # guess list scrolling
    guesses = ["password ✗", "Password1 ✗", "P@ssword ✗", "Pa55word ✗", "Pa55word! ✓"]
    n = min(len(guesses), int(t / 0.4) + 1)
    for k in range(n):
        last = k == len(guesses) - 1
        text_c(d, (540, 590 + k * 80), guesses[k], font(48, "sym"), RED if last else (200, 210, 220))
    if n == len(guesses):
        d.rounded_rectangle([230, 1040, 850, 1150], 30, fill=RED)
        text_c(d, (540, 1095), "EASY TO GUESS", font(60, "bold"), WHITE)


def s4(img, d, t, T, th):
    words = ["chai", "kite", "monsoon"]
    cols = [(255, 190, 120), (130, 200, 255), (150, 225, 160)]
    for k, w in enumerate(words):
        g = pop(prog(t, 0.1 + k * 0.45, 0.35))
        if g <= 0: continue
        x = 230 + k * 310
        d.rounded_rectangle([x - 140 * g, 420 - 70 * g, x + 140 * g, 420 + 70 * g], int(30 * g) + 1, fill=cols[k])
        text_c(d, (x, 420), w, font(int(48 * g) + 1, "bold"), DARK)
    tags = [("LONG", GREEN), ("ODD", GREEN), ("EASY TO REMEMBER", GREEN)]
    for k, (tg, c) in enumerate(tags):
        g = pop(prog(t, 1.6 + k * 0.4, 0.3))
        if g > 0:
            text_c(d, (540, 640 + k * 110), "✓ " + tg, font(int(58 * g) + 1, "sym"), c)
    if t > 2.6:
        text_c(d, (540, 1050), "(make your own - not this one!)", font(40, "reg"), th["soft"])


def s5(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.8))
    text_c(d, (540, 340), "LENGTH", font(80, "bold"), GREEN)
    text_c(d, (540, 430), "beats tricks", font(60, "semi"), WHITE)
    # length bars
    d.rounded_rectangle([140, 540, 140 + 330 * k, 600], 30, fill=RED)
    text_c(d, (140, 510), "Pa55word!", font(38, "sym"), (255, 200, 200), anchor="lm")
    d.rounded_rectangle([140, 690, 140 + 800 * k, 750], 30, fill=GREEN)
    text_c(d, (140, 660), "chai kite monsoon", font(38, "sym"), (200, 255, 210), anchor="lm")
    g = pop(prog(t, 1.4, 0.4))
    if g > 0:
        d.rounded_rectangle([110, 860, W - 110, 1100], 40, fill=(255, 255, 255, 235))
        text_c(d, (540, 930), "Recommended by the UK's", font(int(44 * g) + 1, "semi"), DARK)
        text_c(d, (540, 1010), "National Cyber Security Centre", font(int(46 * g) + 1, "bold"), (20, 110, 120))


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 340, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 450), "3 random words", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 560), "+", font(int(70 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 660), "a different set for", font(int(56 * g2) + 1, "semi"), WHITE)
        text_c(d, (540, 750), "every account", font(int(72 * g2) + 1, "bold"), th["accent"])
        for k in range(3):
            lock(d, 300 + k * 240, 960, 0.7, th["accent"])


SCENES = [
    dict(say="Which password is stronger? One full of symbols, or three random words?", draw=s1),
    dict(say="People swap letters for numbers and add a symbol at the end.", draw=s2),
    dict(say="Hackers know these tricks, so such passwords are easy to guess.", draw=s3),
    dict(say="Now try three random words: chai, kite, monsoon. Long, odd, and easy to remember.", draw=s4),
    dict(say="Length beats tricks. Britain's National Cyber Security Centre recommends it.", draw=s5),
    dict(say="Three random words, and a different set for every account.", draw=s6),
]
