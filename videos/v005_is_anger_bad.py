import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Is getting angry always bad?"
RED, GREEN, WHITE, DARK = (235, 80, 80), (80, 205, 130), (255, 255, 255), (30, 25, 45)


def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def face(d, cx, cy, r, heat, frown):
    col = mix((255, 215, 120), (240, 90, 80), heat)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=WHITE, width=6)
    for ex in (-0.35, 0.35):
        x = cx + ex * r
        d.ellipse([x - r * 0.1, cy - r * 0.2, x + r * 0.1, cy + r * 0.02], fill=DARK)
        # eyebrows tilt with frown
        d.line([(x - r * 0.18, cy - r * 0.32 - (ex < 0) * frown * r * 0.12 + (ex > 0) * frown * r * 0.0),
                (x + r * 0.18, cy - r * 0.32 - (ex > 0) * frown * r * 0.12)], fill=DARK, width=int(r * 0.07))
    # mouth: smile -> frown
    mw = r * 0.4
    if frown < 0.5:
        d.arc([cx - mw, cy + r * 0.05, cx + mw, cy + r * 0.55], 20, 160, fill=DARK, width=int(r * 0.07))
    else:
        d.arc([cx - mw, cy + r * 0.35, cx + mw, cy + r * 0.85], 200, 340, fill=DARK, width=int(r * 0.07))


def steam(d, cx, cy, r, t, k):
    if k <= 0: return
    for sx in (-1, 1):
        for j in range(3):
            y = cy - r + 10 - ((t * 90 + j * 30) % 90)
            x = cx + sx * (r * 0.75) + math.sin(t * 6 + j) * 10
            d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(255, 255, 255, int(150 * k)))


def phone_icon(d, x, y, s=1.0):
    d.rounded_rectangle([x - 50 * s, y - 90 * s, x + 50 * s, y + 90 * s], 18 * s, fill=DARK, outline=WHITE, width=4)
    d.rounded_rectangle([x - 38 * s, y - 70 * s, x + 38 * s, y + 70 * s], 10 * s, fill=(120, 180, 255))


def s1(img, d, t, T, th):
    heat = ease(prog(t, 1.0, 1.6))
    face(d, 540, 640, 200, heat, heat)
    steam(d, 540, 640, 200, t, heat)
    k = ease(prog(t, 0.2, 0.9))
    px = 760 + 260 * k
    phone_icon(d, px, 1010, 0.9)
    if k > 0.3:
        d.line([(px - 140, 990), (px - 70, 990)], fill=WHITE, width=6)
        d.line([(px - 160, 1030), (px - 80, 1030)], fill=WHITE, width=6)
    if t > 1.2:
        text_c(d, (300, 1040), "Hey!", font(80, "bold"), th["accent"], stroke_width=6, stroke_fill=DARK)


def s2(img, d, t, T, th):
    face(d, 540, 520, 170, 0.6, 0.6)
    g = pop(prog(t, 0.3, 0.45))
    if g > 0:
        d.rounded_rectangle([110, 770, W - 110, 1100], 40, fill=(255, 255, 255, 235))
        text_c(d, (W / 2, 850), "Anger is a", font(int(54 * g) + 1, "semi"), DARK)
        text_c(d, (W / 2, 935), "NORMAL emotion", font(int(70 * g) + 1, "bold"), (190, 50, 110))
        text_c(d, (W / 2, 1025), "✓ usually healthy", font(int(48 * g) + 1, "sym"), (40, 150, 90))


def s3(img, d, t, T, th):
    # warning light
    cx, cy = 540, 600
    blink = (t % 0.8) < 0.5
    d.rounded_rectangle([cx - 120, cy - 260, cx + 120, cy + 260], 60, fill=(40, 40, 55), outline=WHITE, width=6)
    for k, col in enumerate([(255, 80, 80), (255, 200, 60), (90, 210, 120)]):
        y = cy - 160 + k * 160
        on = (k == 0 and blink) or (k != 0 and False)
        c = col if on or k != 0 else mix(col, (60, 60, 70), 0.6)
        if k != 0: c = mix(col, (60, 60, 70), 0.7)
        d.ellipse([cx - 70, y - 70, cx + 70, y + 70], fill=c)
    if t > 0.5:
        text_c(d, (W / 2, 1000), "A signal:", font(52, "semi"), WHITE)
        text_c(d, (W / 2, 1080), "\"something feels unfair\"", font(56, "bold"), th["accent"])


def s4(img, d, t, T, th):
    # shouting + door, both leading to "worse"
    # mouth with !!!
    d.ellipse([140, 440, 440, 740], fill=(240, 120, 100), outline=WHITE, width=6)
    d.ellipse([230, 600, 350, 700], fill=DARK)
    text_c(d, (290, 520), "!!!", font(70, "bold"), WHITE)
    # door
    a = math.sin(t * 8) * 6 if t < 1.2 else 0
    d.rectangle([660, 400, 900, 780], fill=(150, 95, 60), outline=WHITE, width=6)
    d.ellipse([850, 590, 875, 615], fill=(255, 210, 90))
    if 0.3 < t < 1.4:
        for j in range(3):
            d.line([(630 - j * 25, 450 + j * 120), (600 - j * 25, 440 + j * 120)], fill=WHITE, width=6)
    g = pop(prog(t, 1.0, 0.4))
    if g > 0:
        arrow_y = 900
        d.line([(540, 800), (540, arrow_y)], fill=WHITE, width=10)
        d.polygon([(510, arrow_y), (570, arrow_y), (540, arrow_y + 40)], fill=WHITE)
        text_c(d, (W / 2, 1040), "usually makes it worse", font(int(60 * g) + 1, "bold"), RED, stroke_width=5,
               stroke_fill=DARK)


def step(d, x, y, n, title, g, th):
    d.rounded_rectangle([x - 150 * g, y - 150 * g, x + 150 * g, y + 150 * g], int(36 * g) + 1, fill=(255, 255, 255, 235))
    d.ellipse([x - 40 * g, y - 190 * g, x + 40 * g, y - 110 * g], fill=th["accent"])
    text_c(d, (x, y - 150 * g), str(n), font(int(48 * g) + 1, "bold"), DARK)
    text_c(d, (x, y + 95 * g), title, font(int(38 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    xs = [190, 540, 890]
    titles = ["PAUSE", "BREATHE", "NAME IT"]
    for k in range(3):
        g = pop(prog(t, 0.2 + k * 0.7, 0.4))
        if g <= 0: continue
        x, y = xs[k], 600
        step(d, x, y, k + 1, titles[k], g, th)
        if g > 0.9:
            if k == 0:
                d.rectangle([x - 40, y - 70, x - 12, y + 30], fill=DARK)
                d.rectangle([x + 12, y - 70, x + 40, y + 30], fill=DARK)
            elif k == 1:
                r = 40 + 25 * (0.5 + 0.5 * math.sin(t * 2.5))
                d.ellipse([x - r, y - 20 - r, x + r, y - 20 + r], outline=(90, 170, 255), width=8)
            else:
                d.rounded_rectangle([x - 70, y - 80, x + 70, y + 10], 20, fill=(255, 140, 170))
                d.polygon([(x - 30, y + 5), (x - 50, y + 40), (x, y + 8)], fill=(255, 140, 170))
                text_c(d, (x, y - 35), "...", font(50, "bold"), WHITE)
    if t > 2.3:
        d.rounded_rectangle([110, 900, W - 110, 1010], 30, fill=(255, 255, 255, 40), outline=th["accent"], width=4)
        text_c(d, (W / 2, 955), "\"I feel angry because...\"", font(50, "bold"), WHITE)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 380, W - 90, 1060], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (W / 2, 500), "Feeling angry", font(int(64 * g) + 1, "bold"), WHITE)
    text_c(d, (W / 2, 590), "✓ OK", font(int(80 * g) + 1, "sym"), GREEN)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        text_c(d, (W / 2, 780), "What you do next", font(int(64 * g2) + 1, "bold"), WHITE)
        text_c(d, (W / 2, 880), "your choice", font(int(80 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your brother grabs your phone without asking, and your face goes hot. Is that anger bad?", draw=s1),
    dict(say="Not really. Psychologists call anger a normal, usually healthy emotion.", draw=s2),
    dict(say="It's a signal that something feels unfair.", draw=s3),
    dict(say="But shouting or slamming doors usually makes things worse.", draw=s4),
    dict(say="Try this: pause, take one slow breath, and name it. I feel angry because...",
         show="Try this: pause, take one slow breath, and name it. \"I feel angry because...\"", draw=s5),
    dict(say="Anger is okay. What you do with it is your choice.", draw=s6),
]
