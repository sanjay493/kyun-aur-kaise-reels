import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Fan on, room still hot. Why do you feel cool?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
SKIN, SKIN2 = (225, 170, 130), (185, 130, 95)
SWEAT, VAPOUR, HEAT = (130, 200, 255), (210, 235, 255), (255, 120, 80)
FAN, FAN2 = (220, 225, 235), (150, 160, 175)
GREEN, RED = (110, 220, 140), (255, 110, 110)


def fan(d, cx, cy, t, r=170, spin=True):
    d.line([(cx, 270), (cx, cy - 20)], fill=FAN2, width=10)
    a0 = t * 12 if spin else 0.3
    for k in range(3):
        a = a0 + k * 2 * math.pi / 3
        x, y = cx + r * math.cos(a), cy + 0.35 * r * math.sin(a)
        d.line([(cx, cy), (x, y)], fill=FAN, width=34)
        d.ellipse([x - 26, y - 14, x + 26, y + 14], fill=FAN)
    d.ellipse([cx - 34, cy - 24, cx + 34, cy + 24], fill=FAN2)


def thermo(d, x, y, level, label):
    d.rounded_rectangle([x - 22, y - 170, x + 22, y + 60], 22, fill=WHITE)
    d.ellipse([x - 42, y + 30, x + 42, y + 114], fill=RED)
    d.rounded_rectangle([x - 11, y + 50 - 220 * level, x + 11, y + 60], 11, fill=RED)
    text_c(d, (x, y + 160), label, font(40, "bold"), WHITE)


def skin(d, y0=760, h=260):
    d.rounded_rectangle([110, y0, 970, y0 + h], 40, fill=SKIN, outline=SKIN2, width=5)


def drop(d, x, y, s=1.0, col=SWEAT):
    d.polygon([(x, y - 30 * s), (x - 18 * s, y), (x + 18 * s, y)], fill=col)
    d.ellipse([x - 18 * s, y - 16 * s, x + 18 * s, y + 20 * s], fill=col)


DROPS = [(220, 740), (380, 745), (540, 738), (700, 744), (860, 740)]


def s1(img, d, t, T, th):
    fan(d, 540, 470, t)
    thermo(d, 300, 840, 0.85, "room")
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        text_c(d, (300, 1080), "still hot", font(int(48 * g) + 1, "bold"), RED)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([560, 760, 960, 920], 40, fill=th["accent"])
        text_c(d, (760, 840), "you: cool?", font(int(54 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Hot day: a thin layer", font(56, "bold"), WHITE)
    text_c(d, (540, 430), "of sweat on your skin", font(56, "bold"), th["accent"])
    skin(d)
    for i, (x, y) in enumerate(DROPS):
        if t > 0.3 + 0.15 * i:
            drop(d, x, y, pop(prog(t, 0.3 + 0.15 * i, 0.35)) + 0.01)


def s3(img, d, t, T, th):
    skin(d)
    k = ease(prog(t, 0.2, 1.4))
    for i, (x, y) in enumerate(DROPS):
        drop(d, x, y, max(0.05, 1 - k))
        for j in range(3):
            yy = y - 60 - 260 * ((k + j * 0.33) % 1)
            d.ellipse([x - 14 + j * 8, yy - 14, x + 14 + j * 8, yy + 14], outline=VAPOUR, width=4)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        for x in (330, 750):
            d.line([(x, 1000), (x, 900)], fill=HEAT, width=12)
            d.polygon([(x - 22, 905), (x + 22, 905), (x, 870)], fill=HEAT)
        d.rounded_rectangle([200, 1060, 880, 1180], 50, fill=th["accent"])
        text_c(d, (540, 1120), "takes heat with it", font(int(54 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "Sweat evaporates", font(62, "bold"), WHITE)


def s4(img, d, t, T, th):
    skin(d, 860, 200)
    # wind lines blowing damp air away
    for i in range(5):
        y = 520 + i * 60
        off = (t * 500 + i * 140) % 620
        d.line([(100 + off, y), (260 + off, y)], fill=WHITE, width=8)
    for i in range(6):
        x = 200 + ((t * 420 + i * 150) % 800)
        d.ellipse([x - 16, 780 - i * 25 - 16, x + 16, 780 - i * 25 + 16], outline=VAPOUR, width=4)
    text_c(d, (540, 350), "Fan blows damp air away", font(54, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([170, 1090, 910, 1190], 50, fill=GREEN)
        text_c(d, (540, 1140), "faster evaporation", font(int(52 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Sticky, humid day?", font(60, "bold"), th["accent"])
    d.rounded_rectangle([110, 440, 970, 700], 40, fill=(255, 255, 255, 35))
    for i in range(22):
        x, y = 160 + (i * 97) % 760, 480 + (i * 53) % 190
        d.ellipse([x - 13, y - 13, x + 13, y + 13], outline=VAPOUR, width=4)
    text_c(d, (540, 750), "air already full of moisture", font(44, "semi"), WHITE)
    skin(d, 830, 170)
    for x, y in DROPS:
        drop(d, x, 820, 1.1)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 1110), "fan helps less", font(int(60 * g) + 1, "bold"), RED)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Fans cool", font(int(80 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 640), "people,", font(int(80 * g) + 1, "bold"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 820), "not rooms.", font(int(86 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Fan on, but the room isn't any cooler. So why do you feel cooler?", draw=s1),
    dict(say="On a hot day, your skin has a thin layer of sweat.", draw=s2),
    dict(say="As sweat evaporates, it takes heat from your body.", draw=s3),
    dict(say="The fan blows the damp air away, so sweat evaporates faster.", draw=s4),
    dict(say="On sticky, humid days, the air is already full of moisture, so the fan helps less.", draw=s5),
    dict(say="Fans cool people, not rooms.", draw=s6),
]
