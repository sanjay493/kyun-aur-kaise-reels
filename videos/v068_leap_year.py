import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does February get a 29th day?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
SUN, SUN2, EARTH, LAND = (255, 200, 60), (255, 150, 40), (80, 150, 255), (90, 200, 110)
CAL, CALTOP, RED, GREEN = (250, 250, 245), (230, 80, 80), (255, 110, 110), (110, 220, 140)


def sun(d, x, y, r=90):
    for i in range(12):
        a = i * math.pi / 6
        d.line([(x + r * 1.15 * math.cos(a), y + r * 1.15 * math.sin(a)),
                (x + r * 1.45 * math.cos(a), y + r * 1.45 * math.sin(a))], fill=SUN2, width=10)
    d.ellipse([x - r, y - r, x + r, y + r], fill=SUN)


def earth(d, x, y, r=40):
    d.ellipse([x - r, y - r, x + r, y + r], fill=EARTH)
    d.ellipse([x - r * 0.5, y - r * 0.5, x + r * 0.1, y + r * 0.1], fill=LAND)
    d.ellipse([x + r * 0.1, y + r * 0.1, x + r * 0.6, y + r * 0.55], fill=LAND)


def calendar(d, x, y, big, small="FEB", s=1.0, col=DARK):
    w, h = 170 * s, 190 * s
    d.rounded_rectangle([x - w, y - h, x + w, y + h], int(24 * s) + 1, fill=CAL)
    d.rounded_rectangle([x - w, y - h, x + w, y - h + 90 * s], int(24 * s) + 1, fill=CALTOP)
    d.rectangle([x - w, y - h + 50 * s, x + w, y - h + 90 * s], fill=CALTOP)
    text_c(d, (x, y - h + 45 * s), small, font(int(48 * s) + 1, "bold"), WHITE)
    text_c(d, (x, y + 45 * s), big, font(int(150 * s) + 1, "bold"), col)


def s1(img, d, t, T, th):
    k = ease(prog(t, 0.5, 0.8))
    calendar(d, 540, 680, "29" if k > 0.5 else "28", "FEB", 1.0 + 0.05 * math.sin(k * math.pi), RED if k > 0.5 else DARK)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 1020), "only sometimes. Why?", font(int(58 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 350), "February 29?", font(64, "bold"), WHITE)


def s2(img, d, t, T, th):
    cx, cy, rx, ry = 540, 700, 380, 230
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=(255, 255, 255, 120), width=4)
    sun(d, cx, cy, 80)
    a = -math.pi / 2 + 2 * math.pi * ease(prog(t, 0.2, 2.2))
    earth(d, cx + rx * math.cos(a), cy + ry * math.sin(a))
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([220, 1000, 860, 1130], 50, fill=th["accent"])
        text_c(d, (540, 1065), "365¼ days", font(int(66 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "One trip around the Sun", font(56, "bold"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Calendar year", font(60, "bold"), WHITE)
    calendar(d, 330, 640, "365", "DAYS", 0.75)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (560, 640), "+", font(90, "bold"), th["accent"])
        d.rounded_rectangle([630, 560, 950, 720], 40, fill=(255, 255, 255, 35), outline=th["accent"], width=5)
        text_c(d, (790, 640), "6 hours", font(int(60 * g) + 1, "bold"), th["accent"])
    if t > 1.5:
        text_c(d, (540, 950), "left over every year", font(54, "bold"), th["soft"])


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Save them up", font(60, "bold"), th["accent"])
    for i in range(4):
        if t > 0.2 + 0.3 * i:
            g = pop(prog(t, 0.2 + 0.3 * i, 0.35))
            x = 210 + i * 220
            d.rounded_rectangle([x - 90, 480, x + 90, 640], 30, fill=(255, 255, 255, 35), outline=WHITE, width=4)
            text_c(d, (x, 540), f"year {i + 1}", font(32, "semi"), th["soft"])
            text_c(d, (x, 595), "6 h", font(int(52 * g) + 1, "bold"), WHITE)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 760), "6 × 4 = 24 hours", font(int(70 * g) + 1, "sym"), WHITE)
        d.rounded_rectangle([250, 870, 830, 1000], 50, fill=GREEN)
        text_c(d, (540, 935), "= 1 whole day", font(int(60 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    calendar(d, 540, 640, "29", "FEB", 0.9, RED)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        d.rounded_rectangle([170, 920, 910, 1050], 50, fill=th["accent"])
        text_c(d, (540, 985), "366 days: LEAP YEAR", font(int(56 * g) + 1, "bold"), DARK)
    text_c(d, (540, 340), "Every 4th year", font(60, "bold"), WHITE)
    if t > 1.4:
        text_c(d, (540, 1130), "next one: 2028", font(44, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "6 hours a year,", font(int(72 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 660), "saved up into", font(int(66 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 770), "one extra day.", font(int(72 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Why does February sometimes get a twenty ninth day?", show="Why does February sometimes get a 29th day?", draw=s1),
    dict(say="Earth takes about three hundred sixty five and a quarter days to circle the Sun.",
         show="Earth takes about 365¼ days to circle the Sun.", draw=s2),
    dict(say="Our calendar year has three hundred sixty five, so six hours are left over.",
         show="Our calendar year has 365, so 6 hours are left over.", draw=s3),
    dict(say="In four years, that's twenty four hours. One whole day.",
         show="In 4 years, that's 24 hours. One whole day.", draw=s4),
    dict(say="So every fourth year, February gets day twenty nine. A leap year.",
         show="So every 4th year, February gets day 29. A leap year.", draw=s5),
    dict(say="Six hours a year, saved up into one day.", show="6 hours a year, saved up into one day.", draw=s6),
]
