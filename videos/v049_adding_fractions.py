import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "1/3 roti + 1/4 roti = 2/7 roti?"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
ROTI, ROTI2, SPOT = (235, 190, 120), (190, 140, 80), (170, 115, 60)
GREEN, RED, BLUE = (110, 220, 140), (255, 110, 110), (120, 190, 255)


def roti(d, cx, cy, r, parts=0, fill_from=0, fill_n=0, col=None, line=ROTI2):
    """Round roti cut into `parts` slices; slices fill_from..fill_from+fill_n are coloured."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ROTI, outline=ROTI2, width=5)
    for a, b in [(-0.4, -0.3), (0.35, -0.45), (0.1, 0.35), (-0.45, 0.3), (0.5, 0.2)]:
        d.ellipse([cx + a * r - 7, cy + b * r - 5, cx + a * r + 7, cy + b * r + 5], fill=SPOT)
    if parts:
        step = 360 / parts
        for i in range(fill_from, fill_from + fill_n):
            d.pieslice([cx - r, cy - r, cx + r, cy + r], -90 + i * step, -90 + (i + 1) * step,
                       fill=(col or GREEN) + (210,))
        for i in range(parts):
            a = math.radians(-90 + i * step)
            d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=line, width=4)


def frac(d, x, y, n, m, col=WHITE, size=72):
    f = font(size, "bold")
    text_c(d, (x, y - size * 0.6), str(n), f, col)
    d.line([(x - size * 0.55, y), (x + size * 0.55, y)], fill=col, width=6)
    text_c(d, (x, y + size * 0.6), str(m), f, col)


def s1(img, d, t, T, th):
    roti(d, 290, 620, 170, 3, 0, 1, GREEN)
    roti(d, 790, 620, 170, 4, 0, 1, BLUE)
    if t > 0.4:
        text_c(d, (540, 620), "+", font(90, "bold"), WHITE)
    frac(d, 290, 900, 1, 3, GREEN)
    frac(d, 790, 900, 1, 4, BLUE)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([330, 1030, 750, 1170], 40, fill=th["accent"])
        text_c(d, (540, 1100), "= 2/7 ?", font(int(70 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "Add tops, add bottoms?", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Check the size", font(60, "bold"), th["accent"])
    roti(d, 290, 640, 170, 3, 0, 1, GREEN)
    roti(d, 790, 640, 170, 7, 0, 2, RED)
    frac(d, 290, 920, 1, 3, GREEN)
    frac(d, 790, 920, 2, 7, RED)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 660), "<", font(int(110 * g) + 1, "bold"), WHITE)
    if t > 1.4:
        text_c(d, (540, 1110), "Adding made it SMALLER?", font(52, "bold"), RED)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Different-sized pieces", font(56, "bold"), WHITE)
    k = prog(t, 0.6, 0.8)
    parts = 3 if k < 0.5 else 12
    roti(d, 290, 660, 170, parts, 0, 1 if parts == 3 else 4, GREEN)
    roti(d, 790, 660, 170, 4 if k < 0.5 else 12, 0, 1 if k < 0.5 else 3, BLUE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([170, 940, 910, 1080], 50, fill=th["accent"])
        text_c(d, (540, 1010), "cut both into 12ths", font(int(58 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    rows = [(1, 3, 4, GREEN), (1, 4, 3, BLUE)]
    for i, (n, m, k, col) in enumerate(rows):
        if t > 0.2 + 1.0 * i:
            g = pop(prog(t, 0.2 + 1.0 * i, 0.4))
            y = 520 + i * 360
            roti(d, 230, y, 130, 12, 0, k, col)
            frac(d, 480, y, n, m, col, int(64 * g) + 1)
            text_c(d, (590, y), "=", font(70, "bold"), WHITE)
            frac(d, 730, y, k, 12, col, int(64 * g) + 1)


def s5(img, d, t, T, th):
    k = int(clamp((t - 0.2) / 1.2) * 7 + 0.0001)
    roti(d, 540, 620, 230, 12, 0, min(4, k), GREEN)
    if k > 4:
        roti_overlay = k - 4
        step = 30
        for i in range(4, 4 + roti_overlay):
            d.pieslice([540 - 230, 620 - 230, 540 + 230, 620 + 230], -90 + i * step, -90 + (i + 1) * step,
                       fill=BLUE + (210,))
        for i in range(12):
            a = math.radians(-90 + i * step)
            d.line([(540, 620), (540 + 230 * math.cos(a), 620 + 230 * math.sin(a))], fill=ROTI2, width=4)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 950), "4 + 3 = 7 twelfths", font(int(58 * g) + 1, "bold"), WHITE)
        frac(d, 540, 1110, 7, 12, th["accent"], 54)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Same-sized pieces", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "first.", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        d.rounded_rectangle([250, 790, 830, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "Then add.", font(int(72 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="One third of a roti, plus one quarter of a roti. Is that two sevenths?",
         show="1/3 of a roti, plus 1/4 of a roti. Is that 2/7?", draw=s1),
    dict(say="But two sevenths is smaller than one third. Adding can't make it smaller!",
         show="But 2/7 is smaller than 1/3. Adding can't make it smaller!", draw=s2),
    dict(say="The pieces are different sizes. So cut both rotis into twelve equal pieces.", draw=s3),
    dict(say="One third is four twelfths. One quarter is three twelfths.",
         show="1/3 is 4/12. 1/4 is 3/12.", draw=s4),
    dict(say="Four plus three: seven twelfths of a roti.", show="4 + 3: 7/12 of a roti.", draw=s5),
    dict(say="Make the pieces the same size first. Then add.", draw=s6),
]
