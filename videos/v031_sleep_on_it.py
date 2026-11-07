import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Studying till 3 a.m. before the exam?"
WHITE, DARK = (255, 255, 255), (20, 25, 50)
MOON, BOOK1, BOOK2, BOOK3 = (255, 230, 150), (255, 130, 120), (120, 210, 160), (255, 200, 90)
BRAIN = (255, 170, 190)


def clock(d, cx, cy, r, hh, mm, th):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=th["accent"], width=8)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line([(cx + math.sin(a) * r * 0.82, cy - math.cos(a) * r * 0.82),
                (cx + math.sin(a) * r * 0.92, cy - math.cos(a) * r * 0.92)], fill=DARK, width=5)
    ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    am = mm / 60 * 2 * math.pi
    d.line([(cx, cy), (cx + math.sin(ah) * r * 0.5, cy - math.cos(ah) * r * 0.5)], fill=DARK, width=12)
    d.line([(cx, cy), (cx + math.sin(am) * r * 0.75, cy - math.cos(am) * r * 0.75)], fill=DARK, width=7)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=DARK)


def books(d, x, y):
    for i, c in enumerate([BOOK1, BOOK2, BOOK3]):
        d.rounded_rectangle([x + i * 12, y - i * 60, x + 300 + i * 12, y - i * 60 + 55], 10, fill=c)
        d.line([(x + 20 + i * 12, y - i * 60 + 27), (x + 280 + i * 12, y - i * 60 + 27)], fill=(255, 255, 255, 120), width=4)


def moon(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MOON)
    d.ellipse([cx - r + r * 0.55, cy - r - r * 0.2, cx + r + r * 0.55, cy + r - r * 0.2], fill=(25, 45, 90))


def brain(d, cx, cy, s=1.0, col=BRAIN):
    r = 150 * s
    for dx, dy, rr in [(-70, -30, 1.0), (60, -40, 1.0), (-90, 50, 0.85), (80, 50, 0.85), (0, 70, 0.8), (0, -80, 0.8)]:
        rx = r * 0.62 * rr
        d.ellipse([cx + dx * s - rx, cy + dy * s - rx, cx + dx * s + rx, cy + dy * s + rx], fill=col)
    d.line([(cx, cy - 150 * s), (cx, cy + 130 * s)], fill=(200, 110, 140), width=int(6 * s))
    for k in (-1, 1):
        d.arc([cx + k * 40 * s - 60 * s, cy - 60 * s, cx + k * 40 * s + 60 * s, cy + 40 * s], 200, 340,
              fill=(200, 110, 140), width=int(5 * s))


def zzz(d, x, y, t):
    for i in range(3):
        k = (t * 0.8 + i * 0.33) % 1.0
        text_c(d, (x + i * 50 + k * 30, y - k * 120), "z", font(int(50 + 20 * i), "bold"),
               (255, 255, 255, int(255 * (1 - k))))


def s1(img, d, t, T, th):
    moon(d, 860, 360, 60)
    g = pop(prog(t, 0.05, 0.5))
    clock(d, 540, 580, int(200 * g) + 1, 3, 0, th)
    books(d, 380, 1000)
    if t > 1.6:
        g2 = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1150), "3 a.m. before the exam?", font(int(62 * g2) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.5))
    # bed
    d.rounded_rectangle([250, 640, 830, 760], 30, fill=(110, 140, 220))
    d.rounded_rectangle([230, 560, 290, 860], 20, fill=(80, 100, 170))
    d.ellipse([300, 570, 420, 670], fill=(240, 190, 150))
    d.rounded_rectangle([380, 600, 810, 700], 40, fill=(250, 250, 255))
    zzz(d, 430, 540, t)
    if t > 0.5:
        text_c(d, (540, 960), "Sleep is not a break", font(int(62 * g) + 1, "bold"), WHITE)
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([170, 1040, 910, 1150], 40, fill=th["accent"])
        text_c(d, (540, 1095), "It's PART of learning", font(int(58 * g2) + 1, "bold"), DARK)


def s3(img, d, t, T, th):
    brain(d, 540, 560, 1.15)
    # replay loop
    k = (t * 0.6) % 1.0
    a0 = k * 360
    d.arc([300, 330, 780, 790], a0, a0 + 250, fill=th["accent"], width=10)
    ang = math.radians(a0 + 250)
    ex, ey = 540 + 240 * math.cos(ang), 560 + 230 * math.sin(ang)
    d.ellipse([ex - 18, ey - 18, ex + 18, ey + 18], fill=th["accent"])
    labels = ["formulas", "dates", "new words"]
    for i, lb in enumerate(labels):
        st = 0.6 + i * 0.5
        if t > st:
            b = ease(prog(t, st + 0.8, 0.8))
            x = 230 + i * 310
            col = (255, 255, 255, int(110 + 145 * b))
            d.rounded_rectangle([x - 135, 900, x + 135, 990], 26, fill=(255, 255, 255, int(30 + 40 * b)),
                                outline=th["accent"], width=int(3 + 5 * b))
            text_c(d, (x, 945), lb, font(int(38 + 6 * b), "bold"), col)
    if t > 2.2:
        g = pop(prog(t, 2.2, 0.4))
        text_c(d, (540, 1100), "replayed and strengthened", font(int(54 * g) + 1, "bold"), th["accent"])


def s4(img, d, t, T, th):
    brain(d, 540, 540, 0.95, (200, 160, 175))
    # tired eyes on brain
    for ex in (-50, 50):
        d.line([(540 + ex - 25, 560), (540 + ex + 25, 560)], fill=DARK, width=8)
    text_c(d, (540, 820), "No sleep", font(54, "bold"), WHITE)
    # learning bar shrinking
    k = ease(prog(t, 0.6, 1.4))
    full = 700
    d.rounded_rectangle([190, 920, 190 + full, 990], 30, fill=(255, 255, 255, 40))
    d.rounded_rectangle([190, 920, 190 + int(full * (1 - 0.4 * k)), 990], 30, fill=(255, 120, 120))
    text_c(d, (540, 1070), "next-day learning gets harder", font(46, "bold"), th["soft"])


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 360, W - 90, 1060], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (160, 450), "“", font(160, "bold"), th["accent"], anchor="lm")
    text_c(d, (540, 560), "You can't pull an", font(int(62 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 650), "all-nighter and still", font(int(62 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 740), "learn effectively.", font(int(62 * g) + 1, "bold"), th["accent"])
    if t > 0.8:
        text_c(d, (540, 900), "a sleep scientist, in NIH News in Health", font(34, "semi"), th["soft"])


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    books(d, 230, 620)
    text_c(d, (720, 560), "+", font(110, "bold"), WHITE)
    moon(d, 860, 560, 70)
    text_c(d, (540, 820), "Study, then", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 940), "SLEEP ON IT", font(int(86 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Studying till three a.m. the night before the exam? Your brain may need that sleep more.",
         show="Studying till 3 a.m. the night before the exam? Your brain may need that sleep more.", draw=s1),
    dict(say="Sleep isn't a break from learning. It's part of it.", draw=s2),
    dict(say="During sleep, the brain replays what you learned and strengthens those memories.", draw=s3),
    dict(say="Skip sleep, and new learning gets harder the next day.", draw=s4),
    dict(say="One sleep scientist puts it simply: you can't pull an all-nighter and still learn effectively.",
         show="One sleep scientist puts it simply: \"You can't pull an all-nighter and still learn effectively.\"",
         draw=s5),
    dict(say="So study, then sleep on it.", draw=s6),
]
