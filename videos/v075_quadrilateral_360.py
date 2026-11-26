import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why do a quadrilateral's angles add up to 360°?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
T1, T2, T3 = (120, 200, 255), (255, 140, 170), (130, 230, 150)
# a crooked four-sided shape (A, B, C, D)
Q = [(250, 470), (820, 400), (900, 980), (330, 900)]
# a five-sided shape
P5 = [(540, 380), (880, 600), (760, 1000), (320, 1000), (200, 600)]


def angle_arc(d, pts, i, col, r=60, w=8):
    """Arc inside the polygon at vertex i."""
    x, y = pts[i]
    a = pts[i - 1]; b = pts[(i + 1) % len(pts)]
    a1 = math.degrees(math.atan2(a[1] - y, a[0] - x))
    a2 = math.degrees(math.atan2(b[1] - y, b[0] - x))
    # choose the sweep that is smaller than 180 (convex shapes)
    s, e = (a1, a2) if (a2 - a1) % 360 < 180 else (a2, a1)
    d.arc([x - r, y - r, x + r, y + r], s, s + (e - s) % 360, fill=col, width=w)


def outline(d, pts, col=WHITE, w=8):
    d.line(pts + [pts[0]], fill=col, width=w, joint="curve")


def s1(img, d, t, T, th):
    k = ease(prog(t, 0.0, 0.8))
    pts = [(540 + (x - 540) * k, 690 + (y - 690) * k) for x, y in Q]
    d.polygon(pts, fill=(255, 255, 255, 25))
    outline(d, pts)
    if t > 0.8:
        for i in range(4):
            angle_arc(d, Q, i, th["accent"])
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([210, 1040, 870, 1170], 50, fill=th["accent"])
        text_c(d, (540, 1105), "4 angles = 360°", font(int(62 * g) + 1, "bold"), DARK)
    text_c(d, (540, 320), "Any four-sided shape", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.9))
    A, C = Q[0], Q[2]
    if t > 1.0:
        d.polygon([Q[0], Q[1], Q[2]], fill=T1 + (90,))
        d.polygon([Q[0], Q[2], Q[3]], fill=T2 + (90,))
    outline(d, Q)
    d.line([A, (A[0] + (C[0] - A[0]) * k, A[1] + (C[1] - A[1]) * k)], fill=th["accent"], width=8)
    text_c(d, (540, 320), "Draw one diagonal", font(60, "bold"), WHITE)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 1100), "= 2 triangles", font(int(70 * g) + 1, "bold"), th["accent"])


def s3(img, d, t, T, th):
    gap = 60 * ease(prog(t, 0.1, 0.7))
    up = [(x, y - gap) for x, y in (Q[0], Q[1], Q[2])]
    dn = [(x - gap, y + gap * 0.3) for x, y in (Q[0], Q[2], Q[3])]
    d.polygon(up, fill=T1 + (120,), outline=WHITE)
    d.polygon(dn, fill=T2 + (120,), outline=WHITE)
    for i in range(3):
        angle_arc(d, up, i, WHITE, 50, 6)
        angle_arc(d, dn, i, WHITE, 50, 6)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        text_c(d, (700, 560), "180°", font(int(64 * g) + 1, "bold"), DARK)
        text_c(d, (460, 860), "180°", font(int(64 * g) + 1, "bold"), DARK)
    text_c(d, (540, 320), "Each triangle: 180°", font(60, "bold"), WHITE)


def s4(img, d, t, T, th):
    g1 = pop(prog(t, 0.1, 0.4))
    d.rounded_rectangle([140, 450, 480, 600], 40, fill=T1)
    text_c(d, (310, 525), "180°", font(int(76 * g1) + 1, "bold"), DARK)
    text_c(d, (540, 525), "+", font(80, "sym"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        d.rounded_rectangle([600, 450, 940, 600], 40, fill=T2)
        text_c(d, (770, 525), "180°", font(int(76 * g2) + 1, "bold"), DARK)
    if t > 1.1:
        g3 = pop(prog(t, 1.1, 0.45))
        d.rounded_rectangle([190, 760, 890, 960], 60, fill=th["accent"])
        text_c(d, (540, 860), "= 360°", font(int(120 * g3) + 1, "bold"), DARK)
    text_c(d, (540, 320), "Two triangles", font(60, "bold"), WHITE)


def s5(img, d, t, T, th):
    outline(d, P5)
    k = ease(prog(t, 0.2, 0.8))
    for j, col in ((2, T1), (3, T2)):
        e = P5[j]
        d.line([P5[0], (P5[0][0] + (e[0] - P5[0][0]) * k, P5[0][1] + (e[1] - P5[0][1]) * k)],
               fill=th["accent"], width=7)
    if t > 1.0:
        for tri, col in (((0, 1, 2), T1), ((0, 2, 3), T2), ((0, 3, 4), T3)):
            d.polygon([P5[i] for i in tri], fill=col + (90,))
        outline(d, P5)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([130, 1060, 950, 1180], 50, fill=th["accent"])
        text_c(d, (540, 1120), "3 × 180° = 540°", font(int(64 * g) + 1, "bold"), DARK)
    text_c(d, (540, 300), "Five sides? 3 triangles", font(56, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Stuck on a shape?", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "Cut it into", font(int(76 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 870), "triangles!", font(int(76 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Draw any four-sided shape, even a crooked one. Its angles always add up to three hundred sixty degrees. Why?",
         show="Draw any four-sided shape, even a crooked one. Its angles always add up to 360°. Why?", draw=s1),
    dict(say="Draw one diagonal, corner to corner. Now you have two triangles.", draw=s2),
    dict(say="Each triangle's angles add up to one hundred eighty degrees.",
         show="Each triangle's angles add up to 180°.", draw=s3),
    dict(say="Two triangles: one hundred eighty plus one hundred eighty. Three hundred sixty!",
         show="Two triangles: 180° + 180°. 360°!", draw=s4),
    dict(say="A five-sided shape? Three triangles, five hundred forty degrees.",
         show="A five-sided shape? Three triangles, 540°.", draw=s5),
    dict(say="Stuck on a shape? Cut it into triangles.", draw=s6),
]
