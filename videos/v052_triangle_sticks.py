import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "3 cm, 4 cm, 8 cm: a triangle?"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
A, B, C = (120, 190, 255), (110, 220, 140), (255, 150, 200)
RED = (255, 110, 110)
U = 70  # pixels per cm


def stick(d, p, q, col, w=18):
    d.line([p, q], fill=col, width=w)
    for x, y in (p, q):
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col)


def s1(img, d, t, T, th):
    for i, (L, col) in enumerate([(3, A), (4, B), (8, C)]):
        if t > 0.2 + 0.35 * i:
            k = ease(prog(t, 0.2 + 0.35 * i, 0.4))
            y = 520 + i * 170
            x0 = 540 - 4 * U
            stick(d, (x0, y), (x0 + L * U * k, y), col)
            text_c(d, (x0 + L * U + 90, y), f"{L} cm", font(48, "bold"), col, anchor="lm")
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1060), "A triangle?", font(int(80 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    y = 960
    x0, x1 = 540 - 4 * U, 540 + 4 * U
    stick(d, (x0, y), (x1, y), C)
    k = ease(prog(t, 0.3, 1.2))
    a1 = math.radians(-80 + 40 * k)
    a2 = math.radians(-100 - 40 * k)
    stick(d, (x0, y), (x0 + 3 * U * math.cos(a1), y + 3 * U * math.sin(a1)), A)
    stick(d, (x1, y), (x1 + 4 * U * math.cos(a2), y + 4 * U * math.sin(a2)), B)
    text_c(d, (540, 1060), "8 cm", font(44, "bold"), C)
    text_c(d, (540, 360), "Raise the short ones", font(58, "bold"), WHITE)


def s3(img, d, t, T, th):
    y = 760
    x0, x1 = 540 - 4 * U, 540 + 4 * U
    stick(d, (x0, y), (x1, y), C, 14)
    k = ease(prog(t, 0.1, 0.8))
    stick(d, (x0, y - 60), (x0 + 3 * U * k, y - 60), A)
    stick(d, (x1, y - 60), (x1 - 4 * U * k, y - 60), B)
    if k > 0.95:
        gx0, gx1 = x0 + 3 * U, x1 - 4 * U
        d.rounded_rectangle([gx0 + 8, y - 110, gx1 - 8, y - 10], 12, outline=RED, width=6)
        text_c(d, ((gx0 + gx1) / 2, y - 160), "gap", font(44, "bold"), RED)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 920), "3 + 4 = 7", font(int(80 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 1040), "7 < 8: they can't meet", font(int(56 * g) + 1, "bold"), RED)
    text_c(d, (540, 360), "Even stretched flat...", font(58, "bold"), th["accent"])


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "The rule", font(64, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([110, 450, 970, 720], 50, fill=(255, 255, 255, 35), outline=th["accent"], width=5)
    text_c(d, (540, 540), "any two sides together", font(int(52 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 630), "> the third side", font(int(60 * g) + 1, "sym"), th["accent"])
    if t > 1.0:
        k = ease(prog(t, 1.0, 0.8))
        p, q, r = (300, 1080), (780, 1080), (500, 820)
        stick(d, p, (p[0] + (q[0] - p[0]) * k, p[1]), C)
        if k > 0.5:
            stick(d, p, r, A)
            stick(d, r, q, B)


def s5(img, d, t, T, th):
    text_c(d, (540, 360), "Quick check", font(64, "bold"), th["accent"])
    text_c(d, (540, 450), "add the two shorter sides", font(46, "semi"), th["soft"])
    g = pop(prog(t, 0.3, 0.45))
    text_c(d, (540, 590), "6, 6, 7", font(int(90 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        text_c(d, (540, 730), "6 + 6 = 12 > 7", font(int(70 * g2) + 1, "sym"), th["accent"])
    if t > 1.5:
        p, q, r = (390, 1100), (690, 1100), (540, 820)
        stick(d, p, q, C)
        stick(d, p, r, A)
        stick(d, r, q, B)
        text_c(d, (840, 960), "✓", font(110, "sym"), B)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Short sides", font(int(76 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 630), "too short?", font(int(76 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        d.rounded_rectangle([210, 790, 870, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "No triangle.", font(int(70 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Three sticks: three, four and eight centimetres. Can they make a triangle?",
         show="Three sticks: 3 cm, 4 cm and 8 cm. Can they make a triangle?", draw=s1),
    dict(say="Lay the long one down. Raise the short ones from its ends.", draw=s2),
    dict(say="Even stretched flat, three plus four is only seven. They can't meet.",
         show="Even stretched flat, 3 + 4 is only 7. They can't meet.", draw=s3),
    dict(say="So the rule: any two sides together must be longer than the third.", draw=s4),
    dict(say="Quick check: add the two shorter sides. Six plus six beats seven. Triangle!",
         show="Quick check: add the two shorter sides. 6 + 6 beats 7. Triangle!", draw=s5),
    dict(say="Short sides too short? No triangle.", draw=s6),
]
