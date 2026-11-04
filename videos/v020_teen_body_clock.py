import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Why can't you sleep early anymore?"
WHITE, DARK = (255, 255, 255), (30, 20, 45)
MOON, SUN, BLUE = (250, 240, 190), (255, 200, 80), (120, 180, 255)


def clock(d, x, y, r, hour, minute=0, col=WHITE):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 235), outline=col, width=8)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        d.line([(x + math.sin(a) * r * 0.82, y - math.cos(a) * r * 0.82),
                (x + math.sin(a) * r * 0.92, y - math.cos(a) * r * 0.92)], fill=DARK, width=6)
    ah = ((hour % 12) + minute / 60) / 12 * 2 * math.pi
    am = minute / 60 * 2 * math.pi
    d.line([(x, y), (x + math.sin(ah) * r * 0.5, y - math.cos(ah) * r * 0.5)], fill=DARK, width=12)
    d.line([(x, y), (x + math.sin(am) * r * 0.75, y - math.cos(am) * r * 0.75)], fill=DARK, width=7)
    d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=DARK)


def moon(d, x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=MOON)
    d.ellipse([x - r + r * 0.5, y - r - r * 0.2, x + r + r * 0.5, y + r - r * 0.2], fill=(70, 30, 75))


def s1(img, d, t, T, th):
    moon(d, 280, 430, 80)
    clock(d, 280, 760, 150, 11, 0)
    text_c(d, (280, 980), "11 PM", font(60, "bold"), th["accent"])
    text_c(d, (280, 1070), "wide awake", font(46, "semi"), WHITE)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.ellipse([800 - 80 * g, 430 - 80 * g, 800 + 80 * g, 430 + 80 * g], fill=SUN)
        clock(d, 800, 760, 150, 7, 0)
        text_c(d, (800, 980), "7 AM", font(60, "bold"), th["accent"])
        text_c(d, (800, 1070), "zombie mode", font(46, "semi"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 360), "During puberty", font(64, "bold"), WHITE)
    k = ease(prog(t, 0.6, 1.4))
    h = 9 + 2 * k
    clock(d, 540, 720, 230, int(h), int((h % 1) * 60), col=th["accent"])
    # arc showing the shift
    d.arc([540 - 280, 720 - 280, 540 + 280, 720 + 280], 180, 180 + 60 * k, fill=th["accent"], width=14)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([230, 1020, 850, 1140], 34, fill=th["accent"])
        text_c(d, (540, 1080), "~2 hours later", font(int(62 * g) + 1, "bold"), DARK)


def s3(img, d, t, T, th):
    moon(d, 540, 420, 90)
    text_c(d, (540, 590), "MELATONIN", font(86, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)
    text_c(d, (540, 690), "the sleepy hormone", font(50, "semi"), th["soft"])
    # timeline: release dot slides later
    x0, x1, y = 160, 920, 900
    d.line([(x0, y), (x1, y)], fill=WHITE, width=6)
    for i, lb in enumerate(["8 PM", "10 PM", "12 AM"]):
        x = x0 + i * (x1 - x0) / 2
        d.line([(x, y - 18), (x, y + 18)], fill=WHITE, width=6)
        text_c(d, (x, y + 60), lb, font(40, "bold"), WHITE)
    k = ease(prog(t, 0.8, 1.4))
    px = x0 + (x1 - x0) * (0.3 + 0.35 * k)
    d.ellipse([px - 30, y - 30, px + 30, y + 30], fill=th["accent"])
    if t > 1.6:
        text_c(d, (540, 1060), "released later at night", font(52, "bold"), WHITE)


def s4(img, d, t, T, th):
    # school bus + sleep need
    d.rounded_rectangle([170, 380, 650, 600], 40, fill=SUN)
    for i in range(4):
        d.rounded_rectangle([200 + i * 105, 410, 285 + i * 105, 490], 12, fill=BLUE)
    for wx in (260, 560):
        d.ellipse([wx - 45, 560, wx + 45, 650], fill=DARK, outline=WHITE, width=5)
    text_c(d, (840, 490), "early", font(60, "bold"), WHITE)
    text_c(d, (840, 560), "school", font(60, "bold"), WHITE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 790), "teens need", font(int(56 * g) + 1, "semi"), th["soft"])
        text_c(d, (540, 920), "8–10 hours", font(int(120 * g) + 1, "bold"), th["accent"], stroke_width=6,
               stroke_fill=DARK)
        text_c(d, (540, 1050), "of sleep a night", font(int(52 * g) + 1, "semi"), WHITE)


def phone_glow(d, x, y, s, a):
    for r in range(5, 0, -1):
        d.ellipse([x - 160 * r * s / 2, y - 200 * r * s / 2, x + 160 * r * s / 2, y + 200 * r * s / 2],
                  fill=BLUE + (int(18 * a),))
    d.rounded_rectangle([x - 110 * s, y - 200 * s, x + 110 * s, y + 200 * s], 30 * s, fill=DARK,
                        outline=WHITE, width=5)
    d.rounded_rectangle([x - 95 * s, y - 175 * s, x + 95 * s, y + 175 * s], 20 * s, fill=(190, 220, 255))


def s5(img, d, t, T, th):
    phone_glow(d, 540, 680, 1.1, 1.0)
    if t > 1.0:
        text_c(d, (540, 1060), "bright light = 'stay awake'", font(54, "bold"), th["accent"], stroke_width=4,
               stroke_fill=DARK)


def s6(img, d, t, T, th):
    k = ease(prog(t, 0.2, 1.0))
    phone_glow(d, 540, 640, 1.0, 1 - k)
    d.rounded_rectangle([430, 440, 650, 840], 30, fill=(20, 20, 30, int(230 * k)))
    moon(d, 540, 640, int(60 * k) + 1)
    if t > 1.0:
        text_c(d, (540, 1000), "dim screens well before bed", font(54, "bold"), WHITE)


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 540), "You're not lazy.", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        text_c(d, (540, 720), "Your body clock", font(68, "semi"), th["soft"])
        text_c(d, (540, 830), "runs LATE", font(92, "bold"), th["accent"])


SCENES = [
    dict(say="Wide awake at eleven at night, but a zombie at seven in the morning?",
         show="Wide awake at 11 at night, but a zombie at 7 in the morning?", draw=s1),
    dict(say="During puberty, your body clock shifts about two hours later.", draw=s2),
    dict(say="Melatonin, the sleepy hormone, is released later at night.", draw=s3),
    dict(say="But school starts early, and teens need eight to ten hours of sleep.",
         show="But school starts early, and teens need 8 to 10 hours of sleep.", draw=s4),
    dict(say="Bright screens at night keep your brain awake.", draw=s5),
    dict(say="So dim the screens well before bed.", draw=s6),
    dict(say="You're not lazy. Your body clock just runs late.", draw=s7),
]
