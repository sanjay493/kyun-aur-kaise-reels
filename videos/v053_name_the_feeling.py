import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Upset? Put it in one word"
WHITE, DARK = (255, 255, 255), (40, 20, 40)
BRAIN, BRAIN2 = (255, 180, 200), (220, 130, 160)
ALARM, CALM, PFC = (255, 90, 90), (120, 200, 255), (255, 220, 90)
GREEN = (110, 220, 140)


def brain(d, cx, cy, s=1.0, alarm=0.0, front=0.0):
    r = 200 * s
    d.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75], fill=BRAIN, outline=BRAIN2, width=6)
    for i in range(-2, 3):
        x = cx + i * r * 0.32
        d.arc([x - r * 0.25, cy - r * 0.5, x + r * 0.25, cy + r * 0.1], 200, 340, fill=BRAIN2, width=6)
    # amygdala: small spot deep in the middle-low part
    ar = r * (0.10 + 0.08 * alarm)
    col = tuple(int(CALM[i] + (ALARM[i] - CALM[i]) * alarm) for i in range(3))
    d.ellipse([cx - ar, cy + r * 0.25 - ar, cx + ar, cy + r * 0.25 + ar], fill=col, outline=WHITE, width=4)
    if front > 0:  # front of the brain on the viewer's left
        d.ellipse([cx - r * 0.98, cy - r * 0.5, cx - r * 0.45, cy + r * 0.2], fill=PFC + (int(80 + 160 * front),),
                  outline=WHITE, width=int(3 + 6 * front))


def face(d, x, y, r, mood):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 215, 170))
    for ex in (-0.35, 0.35):
        d.ellipse([x + ex * r - 10, y - 0.2 * r - 10, x + ex * r + 10, y - 0.2 * r + 10], fill=DARK)
    if mood == "angry":
        d.line([(x - 0.55 * r, y - 0.5 * r), (x - 0.15 * r, y - 0.35 * r)], fill=DARK, width=7)
        d.line([(x + 0.55 * r, y - 0.5 * r), (x + 0.15 * r, y - 0.35 * r)], fill=DARK, width=7)
        d.arc([x - 0.35 * r, y + 0.25 * r, x + 0.35 * r, y + 0.65 * r], 200, 340, fill=DARK, width=7)
    else:
        d.ellipse([x - 0.15 * r, y + 0.25 * r, x + 0.15 * r, y + 0.6 * r], outline=DARK, width=7)
        for ex in (-0.35, 0.35):
            d.arc([x + ex * r - 22, y - 0.6 * r, x + ex * r + 22, y - 0.25 * r], 200, 340, fill=DARK, width=6)


def s1(img, d, t, T, th):
    sh = 5 * math.sin(t * 35) if t < 1.0 else 0
    face(d, 540 + sh, 620, 170, "angry")
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.45))
        d.rounded_rectangle([240, 880, 840, 1020], 50, fill=th["accent"])
        text_c(d, (540, 950), "one word?", font(int(66 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "After a fight...", font(60, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "UCLA brain-scan study", font(56, "bold"), th["accent"])
    for i, (x, m) in enumerate([(320, "angry"), (760, "scared")]):
        if t > 0.3 + 0.4 * i:
            g = pop(prog(t, 0.3 + 0.4 * i, 0.4))
            d.rounded_rectangle([x - 170, 470, x + 170, 840], 30, fill=(255, 255, 255, 40), outline=WHITE, width=4)
            face(d, x, 650, int(120 * g) + 1, m)
    if t > 1.3:
        text_c(d, (540, 960), "photos of emotional faces", font(46, "semi"), WHITE)


def s3(img, d, t, T, th):
    k = ease(prog(t, 0.8, 1.0))
    brain(d, 540, 680, 1.1, alarm=1 - k)
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([330, 360, 750, 470], 40, fill=WHITE)
    text_c(d, (540, 415), "\"angry\"", font(int(58 * g) + 1, "bold"), DARK)
    if t > 1.2:
        text_c(d, (540, 1000), "amygdala: less active", font(52, "bold"), CALM)
        text_c(d, (540, 1080), "(an emotion area)", font(40, "semi"), th["soft"])


def s4(img, d, t, T, th):
    brain(d, 540, 660, 1.1, alarm=0.0, front=0.5 + 0.5 * math.sin(t * 4) ** 2)
    text_c(d, (540, 350), "Behind the forehead", font(58, "bold"), PFC)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 1000), "a thinking area got busier", font(int(50 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    # brake pedal + talk/write icons
    g = pop(prog(t, 0.1, 0.45))
    d.rounded_rectangle([340, 400, 740, 520], 30, fill=ALARM)
    text_c(d, (540, 460), "BRAKES", font(int(62 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 580), "on emotions", font(48, "semi"), WHITE)
    items = [("talk to a friend", 0.9), ("write it down", 1.4)]
    for i, (lab, st) in enumerate(items):
        if t > st:
            g2 = pop(prog(t, st, 0.4))
            y = 760 + i * 170
            d.rounded_rectangle([170, y - 65, 910, y + 65], 40, fill=(255, 255, 255, 35), outline=GREEN, width=5)
            text_c(d, (540, y), lab, font(int(52 * g2) + 1, "bold"), GREEN)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Name it", font(int(96 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 760), "to tame it.", font(int(96 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Angry after a fight? Try putting the feeling into one word.", draw=s1),
    dict(say="In a U.C.L.A. study, people saw photos of angry or scared faces.",
         show="In a UCLA study, people saw photos of angry or scared faces.", draw=s2),
    dict(say="Choosing a word for the feeling lowered activity in the amygdala, an emotion area.", draw=s3),
    dict(say="A thinking area behind the forehead got busier.", draw=s4),
    dict(say="Like hitting the brakes on emotions. Talking or writing it down may help the same way.", draw=s5),
    dict(say="Name it to tame it.", draw=s6),
]
