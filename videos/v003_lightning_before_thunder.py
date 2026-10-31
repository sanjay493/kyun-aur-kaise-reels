import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why do you see lightning before you hear thunder?"
YEL, BLUE, WHITE, DARK = (255, 230, 90), (120, 190, 255), (255, 255, 255), (20, 25, 40)
CLOUD = (120, 130, 160)


def cloud(d, cx, cy, s=1.0, col=CLOUD):
    for dx, dy, r in [(-120, 20, 80), (-40, -30, 105), (70, -10, 95), (150, 30, 70), (10, 45, 90)]:
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s], fill=col)


def bolt(d, x, y, s=1.0, alpha=255):
    pts = [(0, 0), (-45, 120), (5, 120), (-40, 250), (65, 85), (15, 85), (50, 0)]
    d.polygon([(x + px * s, y + py * s) for px, py in pts], fill=YEL + (alpha,), outline=WHITE)


def person(d, x, y, s=1.0, col=(255, 200, 150)):
    d.ellipse([x - 40 * s, y - 150 * s, x + 40 * s, y - 70 * s], fill=col)
    d.rounded_rectangle([x - 50 * s, y - 62 * s, x + 50 * s, y + 60 * s], 26 * s, fill=(90, 170, 255))
    d.ellipse([x - 22 * s, y - 120 * s, x - 10 * s, y - 106 * s], fill=DARK)
    d.ellipse([x + 10 * s, y - 120 * s, x + 22 * s, y - 106 * s], fill=DARK)


def flash_on(t, period=2.4, start=0.3):
    k = (t - start) % period
    return t >= start and k < 0.35


def s1(img, d, t, T, th):
    on = flash_on(t)
    if on:  # soft glow behind the cloud
        for k in range(4):
            r = 260 + k * 70
            d.ellipse([540 - r, 420 - r * 0.7, 540 + r, 420 + r * 0.7], fill=(255, 255, 210, 18))
    cloud(d, 540, 400, 1.3, (200, 205, 225) if on else CLOUD)
    if on:
        bolt(d, 520, 470, 1.4)
    d.line([(80, 1120), (1000, 1120)], fill=(255, 255, 255, 90), width=6)
    person(d, 540, 1060)
    g = pop(prog(t, 0.4, 0.35))
    if g > 0:
        text_c(d, (250, 880), "FLASH!", font(int(80 * g) + 1, "bold"), YEL, stroke_width=6, stroke_fill=DARK)
    g2 = pop(prog(t, 1.7, 0.35))
    if g2 > 0:
        text_c(d, (830, 880), "BOOM!", font(int(80 * g2) + 1, "bold"), BLUE, stroke_width=6, stroke_fill=DARK)
        for k in range(3):
            r = 60 + k * 35
            d.arc([830 - r, 760 - r, 830 + r, 760 + r], 200, 340, fill=BLUE + (200 - k * 50,), width=7)


def lane(d, y, label, col):
    d.rounded_rectangle([80, y - 70, W - 80, y + 70], 35, fill=(255, 255, 255, 25), outline=col, width=4)
    text_c(d, (110, y - 105), label, font(44, "bold"), col, anchor="lm")


def s2(img, d, t, T, th):
    y = 560
    lane(d, y, "LIGHT", YEL)
    k = ease(prog(t, 0.2, 0.18))
    x1 = 120 + (W - 240) * k
    d.rounded_rectangle([120, y - 22, x1, y + 22], 22, fill=YEL)
    if k >= 1:
        for j in range(4):  # glow
            d.rounded_rectangle([120, y - 22 - j * 8, x1, y + 22 + j * 8], 30, outline=YEL + (90 - j * 20,), width=4)
    g = pop(prog(t, 0.6, 0.4))
    if g > 0:
        text_c(d, (W / 2, 800), "≈ 3,00,000 km", font(int(96 * g) + 1, "sym"), YEL, stroke_width=5, stroke_fill=DARK)
        text_c(d, (W / 2, 900), "every second", font(int(56 * g) + 1, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (W / 2, 1060), "That's ~7.5 trips around Earth!", font(46, "semi"), th["soft"])


def speaker(d, x, y, col):
    d.rectangle([x - 40, y - 30, x, y + 30], fill=col)
    d.polygon([(x, y - 30), (x + 50, y - 70), (x + 50, y + 70), (x, y + 30)], fill=col)


def s3(img, d, t, T, th):
    y = 560
    lane(d, y, "SOUND", BLUE)
    speaker(d, 170, y, BLUE)
    front = 240 + 90 * t
    for k in range(5):
        x = front - k * 45
        if x < 240: continue
        d.arc([x - 50, y - 50, x + 50, y + 50], 300, 60, fill=BLUE + (255 - k * 45,), width=8)
    # snail for fun
    sx = min(front + 70, W - 160)
    d.ellipse([sx - 45, y - 50, sx + 35, y + 30], fill=(240, 170, 90), outline=WHITE, width=3)
    d.rounded_rectangle([sx - 60, y + 10, sx + 75, y + 40], 15, fill=(250, 210, 150))
    g = pop(prog(t, 0.5, 0.4))
    if g > 0:
        text_c(d, (W / 2, 800), "≈ 340 m", font(int(110 * g) + 1, "sym"), BLUE, stroke_width=5, stroke_fill=DARK)
        text_c(d, (W / 2, 910), "every second", font(int(56 * g) + 1, "bold"), WHITE)
    if t > 1.5:
        text_c(d, (W / 2, 1060), "Nearly 9 lakh times slower", font(46, "semi"), th["soft"])


def s4(img, d, t, T, th):
    cx, cy = 280, 380
    cloud(d, cx, cy, 0.9)
    bolt(d, cx - 20, cy + 50, 0.9)
    px, py = 830, 1080
    person(d, px, py, 0.9)
    eye = (px, py - 102)
    k = ease(prog(t, 0.1, 0.15))
    src = (cx, cy + 200)
    d.line([src, (src[0] + (eye[0] - src[0]) * k, src[1] + (eye[1] - src[1]) * k)], fill=YEL, width=8)
    if k >= 1:
        text_c(d, (px, py - 210), "Seen!", font(48, "bold"), YEL, stroke_width=5, stroke_fill=DARK)
    R = 80 + 110 * t
    for j in range(3):
        r = R - j * 60
        if r <= 30: continue
        d.arc([src[0] - r, src[1] - r, src[0] + r, src[1] + r], 0, 90, fill=BLUE + (230 - j * 60,), width=8)
    if t > 0.8:
        text_c(d, (300, 1140), "rumble on its way...", font(42, "semi"), BLUE, stroke_width=4, stroke_fill=DARK)


def s5(img, d, t, T, th):
    cx, cy, r = 540, 640, 230
    n = int(9 * prog(t, 0.2, T * 0.7))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 248, 255), outline=WHITE, width=10)
    d.rounded_rectangle([cx - 40, cy - r - 60, cx + 40, cy - r - 10], 12, fill=(200, 205, 225))
    for k in range(12):
        a = math.radians(k * 30 - 90)
        d.line([(cx + math.cos(a) * (r - 30), cy + math.sin(a) * (r - 30)),
                (cx + math.cos(a) * (r - 8), cy + math.sin(a) * (r - 8))], fill=DARK, width=6)
    a = math.radians(-90 + 360 * (n / 12))
    d.line([(cx, cy), (cx + math.cos(a) * (r - 50), cy + math.sin(a) * (r - 50))], fill=(235, 70, 70), width=10)
    text_c(d, (cx, cy + 90), f"{n} s", font(80, "bold"), DARK)
    bolt(d, 130, 400, 0.6)
    text_c(d, (930, 470), "BOOM", font(46, "bold"), BLUE)
    g = pop(prog(t, 1.2, 0.4))
    if g > 0:
        text_c(d, (W / 2, 1020), "seconds  ÷  3", font(int(84 * g) + 1, "sym"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 640], 40, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (W / 2, 430), "9 s  ÷  3", font(int(90 * g) + 1, "sym"), WHITE)
    text_c(d, (W / 2, 550), "≈ 3 km away", font(int(90 * g) + 1, "sym"), th["accent"])
    # distance diagram
    y = 950
    cloud(d, 210, y - 120, 0.55)
    bolt(d, 200, y - 85, 0.5)
    person(d, 880, y + 100, 0.7)
    k = ease(prog(t, 0.5, 0.8))
    x0, x1 = 230, 230 + (820 - 230) * k
    d.line([(x0, y + 150), (x1, y + 150)], fill=th["accent"], width=8)
    d.line([(x0, y + 125), (x0, y + 175)], fill=th["accent"], width=8)
    if k >= 1:
        d.line([(820, y + 125), (820, y + 175)], fill=th["accent"], width=8)
        text_c(d, (525, y + 105), "≈ 3 km", font(52, "sym"), WHITE)


SCENES = [
    dict(say="Lightning and thunder happen together. So why do you see the flash first?", draw=s1),
    dict(say="Light is super fast, about three lakh kilometres every second.",
         show="Light is super fast, about 3 lakh km every second.", draw=s2),
    dict(say="Sound is much slower, about three hundred forty metres a second.",
         show="Sound is much slower, about 340 metres a second.", draw=s3),
    dict(say="The flash reaches you instantly. The rumble is still on its way.", draw=s4),
    dict(say="Count the seconds between flash and thunder, then divide by three.", draw=s5),
    dict(say="Nine seconds? The storm is about three kilometres away.",
         show="9 seconds? The storm is about 3 km away.", draw=s6),
]
