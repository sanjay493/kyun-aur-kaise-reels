import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Thank-you notes feel better than you think"
WHITE, DARK = (255, 255, 255), (40, 20, 40)
PAPER, LINE, HEART = (250, 245, 235), (190, 180, 170), (255, 110, 140)
GREEN, BLUE, AMBER = (110, 220, 140), (120, 190, 255), (255, 200, 90)


def note(d, x, y, s=1.0, heart=True):
    w, h = 190 * s, 240 * s
    d.rounded_rectangle([x - w, y - h, x + w, y + h], int(20 * s) + 1, fill=PAPER)
    text_c(d, (x, y - h + 60 * s), "Thank you!", font(int(46 * s) + 1, "bold"), DARK)
    for i in range(4):
        yy = y - h + 130 * s + i * 60 * s
        d.line([(x - w + 40 * s, yy), (x + w - 40 * s - (50 * s if i == 3 else 0), yy)], fill=LINE, width=int(6 * s) + 1)
    if heart:
        hx, hy, r = x + w - 60 * s, y + h - 60 * s, 22 * s
        d.ellipse([hx - 2 * r, hy - r, hx, hy + r * 0.6], fill=HEART)
        d.ellipse([hx, hy - r, hx + 2 * r, hy + r * 0.6], fill=HEART)
        d.polygon([(hx - 2 * r, hy), (hx + 2 * r, hy), (hx, hy + 2.2 * r)], fill=HEART)


def face(d, x, y, r, mood=0.0):
    """mood: 0 = unsure (flat mouth), 1 = big smile."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 215, 170))
    for ex in (-0.35, 0.35):
        d.ellipse([x + ex * r - 9, y - 0.2 * r - 9, x + ex * r + 9, y - 0.2 * r + 9], fill=DARK)
    if mood > 0.5:
        d.chord([x - 0.45 * r, y + 0.05 * r, x + 0.45 * r, y + 0.6 * r], 0, 180, fill=(140, 50, 60))
    else:
        d.line([(x - 0.3 * r, y + 0.35 * r), (x + 0.3 * r, y + 0.3 * r)], fill=DARK, width=7)


def bar_pair(d, y, lab, guess, real, k, col):
    text_c(d, (130, y - 75), lab, font(44, "bold"), WHITE, anchor="lm")
    d.rounded_rectangle([130, y - 40, 130 + 760 * guess * k, y], 14, fill=(200, 200, 215))
    d.rounded_rectangle([130, y + 10, 130 + 760 * real * k, y + 50], 14, fill=col)


def s1(img, d, t, T, th):
    face(d, 540, 620, 150, 0.0)
    for i in range(3):
        if t > 0.5 + 0.25 * i:
            text_c(d, (700 + i * 55, 470 - i * 30), "?", font(70, "bold"), AMBER)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([200, 880, 880, 1020], 50, fill=th["accent"])
        text_c(d, (540, 950), "feels awkward...", font(int(58 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "Want to say thanks?", font(60, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "University of Chicago study", font(52, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.45))
    note(d, 540, 720, 0.95 * g + 0.01)
    if t > 1.2:
        text_c(d, (540, 1060), "letters to someone who helped them", font(42, "semi"), WHITE)


def s3(img, d, t, T, th):
    # writer guesses (thought bubble), then the reader answers
    face(d, 290, 760, 110, 0.0)
    text_c(d, (290, 920), "writer", font(44, "bold"), WHITE)
    d.ellipse([170, 430, 420, 600], fill=(255, 255, 255, 50), outline=WHITE, width=4)
    text_c(d, (295, 515), "they'll feel...?", font(34, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        face(d, 790, 760, int(110 * g) + 1, 0.0)
        text_c(d, (790, 920), "reader", font(44, "bold"), WHITE)
        d.rounded_rectangle([640, 450, 940, 590], 30, fill=th["accent"])
        text_c(d, (790, 520), "asked too", font(int(44 * g) + 1, "bold"), DARK)
    text_c(d, (540, 340), "Guess vs real", font(60, "bold"), th["accent"])


def s4(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.9))
    bar_pair(d, 520, "happy", 0.6, 0.85, k, GREEN)
    bar_pair(d, 740, "surprised", 0.45, 0.75, k, BLUE)
    bar_pair(d, 960, "awkward", 0.5, 0.2, k, AMBER)
    text_c(d, (540, 340), "Readers felt:", font(60, "bold"), WHITE)
    if t > 1.0:
        d.rounded_rectangle([140, 1090, 180, 1120], 8, fill=(200, 200, 215))
        text_c(d, (195, 1105), "writer's guess", font(32, "semi"), WHITE, anchor="lm")
        d.rounded_rectangle([560, 1090, 600, 1120], 8, fill=GREEN)
        text_c(d, (615, 1105), "reader's answer", font(32, "semi"), WHITE, anchor="lm")
    if t > 1.6:
        text_c(d, (540, 1170), "(illustration, not exact scores)", font(30, "reg"), th["soft"])


def s5(img, d, t, T, th):
    note(d, 540, 640, 0.75)
    if t > 0.3:
        g = pop(prog(t, 0.3, 0.4))
        d.rounded_rectangle([120, 920, 520, 1040], 40, fill=(255, 255, 255, 35), outline=th["soft"], width=4)
        text_c(d, (320, 980), "right words?", font(int(46 * g) + 1, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([560, 920, 960, 1040], 40, fill=th["accent"])
        text_c(d, (760, 980), "warmth!", font(int(52 * g) + 1, "bold"), DARK)
    text_c(d, (540, 340), "What mattered", font(60, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Don't wait for", font(int(68 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 600), "perfect words.", font(int(68 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        d.rounded_rectangle([200, 780, 880, 920], 50, fill=th["accent"])
        text_c(d, (540, 850), "Say thank you.", font(int(66 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Want to thank someone, but it feels awkward? Here's a surprise.", draw=s1),
    dict(say="In a University of Chicago study, people wrote thank-you letters to someone who helped them.", draw=s2),
    dict(say="Writers guessed how the reader would feel. Then the readers were asked.", draw=s3),
    dict(say="Readers felt happier and more surprised than the writers expected, and less awkward.", draw=s4),
    dict(say="Writers worried about the right words. Readers just felt the warmth.", draw=s5),
    dict(say="Don't wait for perfect words. Say thank you.", draw=s6),
]
