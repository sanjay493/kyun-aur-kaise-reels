import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "A perfect right angle from a rope: 3, 4, 5"
WHITE = (255, 255, 255)
ROPE, KNOT = (215, 170, 110), (140, 90, 40)
C3, C4, C5 = (110, 215, 255), (255, 150, 120), (150, 235, 140)
U = 110  # pixels per unit

# right triangle: right angle at A, 4 units along the bottom, 3 units up
A = (300, 1000)
B = (A[0] + 4 * U, A[1])
C = (A[0], A[1] - 3 * U)


def lerp(p, q, k):
    return (p[0] + (q[0] - p[0]) * k, p[1] + (q[1] - p[1]) * k)


def knot(d, p, r=16):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=KNOT, outline=WHITE, width=3)


def right_mark(d, p, s=40, col=(255, 205, 60)):
    d.line([(p[0], p[1] - s), (p[0] + s, p[1] - s), (p[0] + s, p[1])], fill=col, width=6)


def s1(img, d, t, T, th):
    text_c(d, (540, 340), "Just a rope?", font(66, "bold"), WHITE)
    k = ease(prog(t, 0.2, 1.0))
    # wavy rope
    pts = [(120 + i * 8, 530 + 30 * math.sin(i / 6 + t * 2)) for i in range(int(106 * k) + 1)]
    if len(pts) > 1:
        d.line(pts, fill=ROPE, width=12, joint="curve")
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.5))
        right_mark(d, (440, 1010), 120, th["accent"])
        d.line([(440, 1010 - 360 * g), (440, 1010)], fill=WHITE, width=8)
        d.line([(440, 1010), (440 + 360 * g, 1010)], fill=WHITE, width=8)
        text_c(d, (640, 900), "90°", font(int(80 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "Knots at 3, 4 and 5", font(64, "bold"), th["accent"])
    # straight rope, 12 units, knots every unit; big knots at 3 and 7 (3 + 4) and ends
    x0, y = 100, 700
    step = 880 / 12
    k = ease(prog(t, 0.1, 0.8))
    d.line([(x0, y), (x0 + 880 * k, y)], fill=ROPE, width=12)
    for i in range(13):
        if i * step <= 880 * k + 1:
            r = 16 if i in (0, 3, 7, 12) else 7
            knot(d, (x0 + i * step, y), r)
    if t > 1.0:
        for a, b, lab, col in ((0, 3, "3", C3), (3, 7, "4", C4), (7, 12, "5", C5)):
            xa, xb = x0 + a * step, x0 + b * step
            d.line([(xa + 6, y + 60), (xb - 6, y + 60)], fill=col, width=6)
            text_c(d, ((xa + xb) / 2, y + 120), lab, font(70, "bold"), col)
        text_c(d, (540, 1000), "3 + 4 + 5 = 12 equal parts", font(48, "semi"), WHITE)


def triangle(d, k=1.0, labels=True):
    d.line([A, lerp(A, B, k)], fill=C4, width=12)
    d.line([A, lerp(A, C, k)], fill=C3, width=12)
    if k >= 1:
        d.line([C, B], fill=C5, width=12)
        for p in (A, B, C):
            knot(d, p)
        if labels:
            text_c(d, ((A[0] + B[0]) / 2, A[1] + 60), "4", font(66, "bold"), C4)
            text_c(d, (A[0] - 60, (A[1] + C[1]) / 2), "3", font(66, "bold"), C3)
            text_c(d, ((B[0] + C[0]) / 2 + 50, (B[1] + C[1]) / 2 - 40), "5", font(66, "bold"), C5)


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "Pull it into a triangle", font(64, "bold"), WHITE)
    triangle(d, ease(prog(t, 0.2, 0.9)))
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.5))
        right_mark(d, (A[0], A[1]), 50, th["accent"])
        text_c(d, (A[0] + 140, A[1] - 90), "90°", font(int(64 * g) + 1, "bold"), th["accent"])
        text_c(d, (540, 1150), "exactly a right angle", font(54, "bold"), th["accent"])


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Why?", font(70, "bold"), th["accent"])
    f = font(72, "bold")
    rows = [("3² + 4²", WHITE, 0.2), ("= 9 + 16", WHITE, 0.8), ("= 25", th["accent"], 1.4), ("= 5²", C5, 2.0)]
    for i, (txt, col, st) in enumerate(rows):
        if t > st:
            g = pop(prog(t, st, 0.4))
            text_c(d, (540, 520 + i * 140), txt, font(int(80 * g) + 1, "bold"), col)


def s5(img, d, t, T, th):
    triangle(d, 1.0, labels=True)
    right_mark(d, (A[0], A[1]), 50, th["accent"])
    text_c(d, (540, 340), "Two squares add up", font(58, "bold"), WHITE)
    text_c(d, (540, 415), "to the third square?", font(58, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.5))
        text_c(d, (540, 1150), "Right angle, guaranteed", font(int(56 * g) + 1, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 600), "3, 4, 5", font(int(140 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 780), "a right angle", font(int(66 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 870), "from a rope", font(int(66 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="How do you make a perfect right angle with a rope?", draw=s1),
    dict(say="Mark it with knots at three, four and five units.",
         show="Mark it with knots at 3, 4 and 5 units.", draw=s2),
    dict(say="Pull it into a triangle. The corner between three and four: ninety degrees.",
         show="Pull it into a triangle. The corner between 3 and 4: 90°.", draw=s3),
    dict(say="Why? Three squared plus four squared: nine plus sixteen, twenty-five. Five squared!",
         show="Why? 3² + 4²: 9 + 16, 25. 5²!", draw=s4),
    dict(say="If two sides' squares add up to the third's square, it's a right angle.", draw=s5),
    dict(say="Three, four, five: a right angle from a rope.", show="3, 4, 5: a right angle from a rope.", draw=s6),
]
