import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a cold glass 'sweat'?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
STEEL, STEEL_D, STEEL_L = (190, 200, 210), (120, 130, 145), (230, 236, 242)
WATER, DROP, VAP = (120, 190, 240), (170, 220, 255), (200, 230, 255)
RED, GREEN, ICE = (240, 90, 90), (90, 210, 130), (225, 245, 255)

DROPS = [(-0.62, 0.15), (-0.3, 0.42), (0.1, 0.25), (0.45, 0.55), (-0.5, 0.7), (0.3, 0.05), (0.6, 0.3),
         (-0.1, 0.62), (0.05, 0.85), (-0.7, 0.45), (0.55, 0.8), (-0.35, 0.12)]


def tumbler(d, x, y, s=1.0, drops=0.0, fill=True):
    tw, bw, h = 150 * s, 115 * s, 330 * s
    poly = [(x - tw, y - h / 2), (x + tw, y - h / 2), (x + bw, y + h / 2), (x - bw, y + h / 2)]
    d.polygon(poly, fill=STEEL, outline=STEEL_D)
    d.polygon([(x - tw + 25 * s, y - h / 2 + 10 * s), (x - tw + 60 * s, y - h / 2 + 10 * s),
               (x - bw + 50 * s, y + h / 2 - 10 * s), (x - bw + 20 * s, y + h / 2 - 10 * s)], fill=STEEL_L)
    d.ellipse([x - tw, y - h / 2 - 25 * s, x + tw, y - h / 2 + 25 * s], fill=WATER if fill else STEEL_D,
              outline=STEEL_D, width=3)
    if fill:
        for ix in (-60, 20, 70):
            d.rectangle([x + ix * s - 22 * s, y - h / 2 - 18 * s, x + ix * s + 22 * s, y - h / 2 + 10 * s], fill=ICE)
    n = int(len(DROPS) * drops)
    for (u, v) in DROPS[:n]:
        dx = x + u * (tw - 10 * s)
        dy = y - h / 2 + 30 * s + v * (h - 60 * s)
        r = 13 * s
        d.ellipse([dx - r, dy - r, dx + r, dy + r * 1.3], fill=DROP, outline=WHITE, width=2)
    return h


def vapour(d, t, x0, x1, y0, y1, n=26, col=VAP, alpha=170, drift=1.0):
    for i in range(n):
        px = x0 + ((i * 97 + t * 60 * drift) % (x1 - x0))
        py = y0 + ((i * 53 + math.sin(t * 2 + i) * 20) % (y1 - y0))
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col + (alpha,))


def s1(img, d, t, T, th):
    tumbler(d, 540, 700, 1.3, drops=ease(prog(t, 0.8, 1.6)))
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1110), "Leaking?", font(int(70 * g) + 1, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    tumbler(d, 540, 740, 1.1, drops=1.0)
    g = pop(prog(t, 0.1, 0.4))
    text_c(d, (540, 370), "NO", font(int(150 * g) + 1, "bold"), RED, stroke_width=6, stroke_fill=DARK)
    if t > 0.8:
        text_c(d, (540, 1060), "this water was never inside", font(52, "bold"), WHITE)


def s3(img, d, t, T, th):
    vapour(d, t, 100, 980, 320, 1150, n=46, alpha=200)
    g = pop(prog(t, 0.3, 0.4))
    d.rounded_rectangle([150, 600, 930, 860], 40, fill=(10, 40, 30, 200))
    text_c(d, (540, 680), "air holds", font(int(64 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 780), "invisible water vapour", font(int(60 * g) + 1, "bold"), th["accent"])


def s4(img, d, t, T, th):
    h = tumbler(d, 540, 720, 1.2, drops=0.0)
    vapour(d, t, 120, 980, 360, 1100, n=30, alpha=150)
    k = ease(prog(t, 0.3, 1.0))
    # cold zone hugging the glass
    for r in range(4):
        d.rounded_rectangle([540 - 200 - r * 18, 520 - r * 18, 540 + 200 + r * 18, 920 + r * 18], 60,
                            outline=(140, 200, 255, int(160 * k / (r + 1))), width=8)
    if t > 1.0:
        text_c(d, (540, 380), "cold glass cools the air", font(56, "bold"), WHITE)
        text_c(d, (540, 1080), "touching it", font(52, "bold"), th["accent"])


def s5(img, d, t, T, th):
    k = ease(prog(t, 0.2, 1.4))
    tumbler(d, 540, 700, 1.2, drops=k)
    # vapour dots moving in towards the glass
    for i in range(14):
        a = i / 14 * math.pi * 2
        rr = 360 - 170 * clamp(k * 1.2 - (i % 4) * 0.08)
        px, py = 540 + math.cos(a) * rr, 700 + math.sin(a) * rr * 0.9
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=VAP + (200,))
    text_c(d, (540, 360), "vapour turns to liquid drops", font(58, "bold"), WHITE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([200, 1030, 880, 1150], 34, fill=th["accent"])
        text_c(d, (540, 1090), "CONDENSATION", font(int(64 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    # rain clouds: monsoon
    for cx in (300, 760):
        for dx, dy, r in ((-70, 10, 60), (0, -20, 80), (80, 10, 60)):
            d.ellipse([cx + dx - r, 400 + dy - r, cx + dx + r, 400 + dy + r], fill=(200, 210, 225))
    for i in range(18):
        x = 180 + (i * 61) % 720
        y = 500 + ((i * 37 + t * 400) % 200)
        d.line([(x, y), (x - 8, y + 30)], fill=DROP, width=5)
    tumbler(d, 540, 900, 0.8, drops=1.0)
    text_c(d, (540, 1150), "humid air: lots of vapour", font(52, "bold"), th["accent"])


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 540), "The water came", font(int(76 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 650), "from the AIR", font(int(90 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        text_c(d, (540, 840), "not from the glass", font(64, "semi"), th["soft"])


SCENES = [
    dict(say="Pour ice-cold water into a steel glass. Soon the outside is wet. Leaking?",
         draw=s1),
    dict(say="No. That water was never inside the glass.", draw=s2),
    dict(say="The air around us holds water vapour that we cannot see.", draw=s3),
    dict(say="The cold glass cools the air touching it.", draw=s4),
    dict(say="Cooled vapour turns into tiny liquid drops. This is condensation.", draw=s5),
    dict(say="That's why it's so common on humid monsoon days.", draw=s6),
    dict(say="The water came from the air, not from the glass.", draw=s7),
]
