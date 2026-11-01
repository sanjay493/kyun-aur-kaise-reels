import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why isn't 1 a prime number?"
GREEN, RED, WHITE, DARK = (90, 215, 140), (240, 90, 90), (255, 255, 255), (25, 25, 50)


def tile(d, x, y, label, col, g=1.0, size=120):
    s = size * g / 2
    d.rounded_rectangle([x - s, y - s, x + s, y + s], int(26 * g) + 1, fill=col, outline=WHITE, width=5)
    text_c(d, (x, y), label, font(int(size * 0.55 * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    items = [(250, "2", GREEN, "prime"), (540, "3", GREEN, "prime"), (830, "1", (200, 200, 220), "?")]
    for k, (x, n, col, lab) in enumerate(items):
        g = pop(prog(t, 0.1 + k * 0.6, 0.35))
        if g <= 0: continue
        tile(d, x, 620, n, col, g, 200)
        c = GREEN if lab == "prime" else th["accent"]
        text_c(d, (x, 800), lab + (" ✓" if lab == "prime" else ""), font(int(56 * g) + 1, "sym"), c)
    if t > 2.0:
        text_c(d, (540, 1020), "Why not 1?", font(84, "bold"), th["accent"], stroke_width=6, stroke_fill=DARK)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.4))
    d.rounded_rectangle([90, 320, W - 90, 640], 40, fill=(255, 255, 255, 235))
    text_c(d, (540, 400), "A PRIME has exactly", font(int(54 * g) + 1, "semi"), DARK)
    text_c(d, (540, 490), "2 factors", font(int(96 * g) + 1, "bold"), (180, 60, 140))
    text_c(d, (540, 580), "1  and  itself", font(int(50 * g) + 1, "semi"), (60, 60, 90))
    g2 = pop(prog(t, 1.2, 0.4))
    if g2 > 0:
        tile(d, 330, 880, "7", th["accent"], g2, 170)
        text_c(d, (555, 880), "→", font(80, "sym"), WHITE)
        tile(d, 690, 880, "1", GREEN, g2, 110)
        tile(d, 840, 880, "7", GREEN, g2, 110)
        text_c(d, (765, 1010), "2 factors ✓", font(int(50 * g2) + 1, "sym"), GREEN)


def s3(img, d, t, T, th):
    tile(d, 540, 560, "1", (200, 200, 220), 1.0, 230)
    g = pop(prog(t, 0.5, 0.4))
    if g > 0:
        text_c(d, (540, 780), "factors:  1", font(int(64 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 870), "only ONE factor", font(int(56 * g) + 1, "bold"), th["accent"])
    g2 = pop(prog(t, 1.4, 0.35))
    if g2 > 0:
        d.rounded_rectangle([290, 960, 790, 1080], 30, fill=RED)
        text_c(d, (540, 1020), "✗ not prime", font(int(60 * g2) + 1, "sym"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 330), "Deeper reason", font(60, "bold"), th["accent"])
    tile(d, 540, 500, "12", WHITE, 1.0, 170)
    k = ease(prog(t, 0.6, 0.6))
    xs = [300, 540, 780]
    labs = ["2", "2", "3"]
    for i in range(3):
        x = 540 + (xs[i] - 540) * k
        y = 500 + 280 * k
        if k > 0:
            d.line([(540, 590), (x, y - 70)], fill=(255, 255, 255, int(150 * k)), width=5)
            tile(d, x, y, labs[i], GREEN, 0.4 + 0.6 * k, 130)
    if k >= 1:
        text_c(d, (420, 780), "×", font(64, "sym"), WHITE)
        text_c(d, (660, 780), "×", font(64, "sym"), WHITE)
        text_c(d, (540, 960), "12 = 2 × 2 × 3", font(76, "sym"), WHITE, stroke_width=5, stroke_fill=DARK)
        text_c(d, (540, 1060), "only ONE way to split into primes", font(44, "semi"), th["soft"])


def s5(img, d, t, T, th):
    text_c(d, (540, 330), "If 1 were prime...", font(64, "bold"), th["accent"])
    lines = ["12 = 2 × 2 × 3", "12 = 2 × 2 × 3 × 1", "12 = 2 × 2 × 3 × 1 × 1", "12 = 2 × 2 × 3 × 1 × 1 × 1"]
    for k, s in enumerate(lines):
        g = pop(prog(t, 0.2 + k * 0.45, 0.3))
        if g > 0:
            text_c(d, (540, 470 + k * 120), s, font(int(60 * g) + 1, "sym"), WHITE if k == 0 else (255, 200, 200))
    if t > 2.2:
        text_c(d, (540, 1000), "...forever!", font(70, "bold"), RED, stroke_width=5, stroke_fill=DARK)
        text_c(d, (540, 1100), "no longer one way", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 340, W - 90, 1060], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    tile(d, 540, 500, "1", (200, 200, 220), g, 150)
    text_c(d, (540, 650), "stays out", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        text_c(d, (540, 820), "Every number keeps", font(int(56 * g2) + 1, "semi"), WHITE)
        text_c(d, (540, 920), "ONE prime recipe", font(int(76 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Two is prime. Three is prime. Why not one?", draw=s1),
    dict(say="A prime has exactly two factors: one and itself. Seven has two.", draw=s2),
    dict(say="But one has only one factor, so it fails.", draw=s3),
    dict(say="Deeper reason: every number splits into primes in only one way. Twelve is two times two times three.",
         show="Deeper reason: every number splits into primes in only one way. 12 = 2 × 2 × 3.", draw=s4),
    dict(say="If one were prime, you could keep adding ones forever.",
         show="If 1 were prime, you could keep adding 1s forever.", draw=s5),
    dict(say="So one stays out, and every number keeps one prime recipe.",
         show="So 1 stays out, and every number keeps one prime recipe.", draw=s6),
]
