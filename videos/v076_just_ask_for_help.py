import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Scared to ask for help?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
SKIN, HAIR = (240, 190, 150), (40, 30, 30)
RED, GREEN, BLUE = (255, 110, 120), (110, 220, 140), (120, 190, 255)


def kid(d, x, y, s=1.0, shirt=BLUE, arm_up=0.0):
    r = 70 * s
    d.rounded_rectangle([x - 90 * s, y + 70 * s, x + 90 * s, y + 260 * s], int(45 * s), fill=shirt)
    if arm_up > 0:
        ax = x + 80 * s
        d.line([(ax, y + 110 * s), (ax + 40 * s, y + 110 * s - 200 * s * arm_up)], fill=SKIN, width=int(26 * s))
    d.ellipse([x - r, y - r, x + r, y + r], fill=SKIN)
    d.chord([x - r - 3, y - r - 8 * s, x + r + 3, y + r * 0.5], 180, 360, fill=HAIR)
    for ex in (-24, 24):
        d.ellipse([x + ex * s - 8 * s, y - 6 * s, x + ex * s + 8 * s, y + 12 * s], fill=DARK)


def bubble(d, x, y, w, h, col, tail=(0, 1)):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 40, fill=col)
    tx, ty = x + tail[0] * w * 0.3, y + h / 2
    d.polygon([(tx - 25, ty - 2), (tx + 25, ty - 2), (tx - 10 * tail[1], ty + 50)], fill=col)


def s1(img, d, t, T, th):
    kid(d, 300, 820, 1.3)
    for i, (bx, by) in enumerate(((680, 520), (820, 720), (640, 880))):
        if t > 0.3 + i * 0.4:
            g = pop(prog(t, 0.3 + i * 0.4, 0.35))
            d.ellipse([bx - 110 * g, by - 70 * g, bx + 110 * g, by + 70 * g], fill=(255, 255, 255, 200))
            text_c(d, (bx, by), "No?", font(int(56 * g) + 1, "bold"), RED)
    text_c(d, (540, 320), "Scared to ask?", font(64, "bold"), WHITE)


def phone_icon(d, x, y, s=1.0):
    d.rounded_rectangle([x - 60 * s, y - 110 * s, x + 60 * s, y + 110 * s], int(20 * s), fill=(40, 45, 60))
    d.rounded_rectangle([x - 50 * s, y - 95 * s, x + 50 * s, y + 90 * s], int(12 * s), fill=(220, 235, 250))


def form_icon(d, x, y, s=1.0):
    d.rounded_rectangle([x - 85 * s, y - 115 * s, x + 85 * s, y + 115 * s], int(14 * s), fill=(245, 245, 235))
    for i in range(5):
        yy = y - 70 * s + i * 36 * s
        d.rectangle([x - 60 * s, yy - 8 * s, x - 40 * s, yy + 8 * s], outline=DARK, width=3)
        d.line([(x - 25 * s, yy), (x + 60 * s, yy)], fill=(150, 150, 160), width=5)


def s2(img, d, t, T, th):
    text_c(d, (540, 320), "Stanford studies", font(60, "bold"), th["accent"])
    g1 = pop(prog(t, 0.2, 0.4))
    phone_icon(d, 330, 640, 1.2 * g1 + 0.01)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.4))
        form_icon(d, 750, 640, 1.2 * g2 + 0.01)
    if t > 1.2:
        text_c(d, (330, 880), "lend a phone?", font(44, "semi"), WHITE)
        text_c(d, (750, 880), "fill in a form?", font(44, "semi"), WHITE)
        text_c(d, (540, 1020), "asking strangers", font(46, "semi"), th["soft"])


def s3(img, d, t, T, th):
    base = 1000
    k = ease(prog(t, 0.2, 1.0))
    # illustration: guessed 15 people, needed 10 (50% more)
    for i, (lab, val, col) in enumerate((("guessed", 15, RED), ("needed", 10, GREEN))):
        x = 360 + i * 360
        h = val * 36 * k
        d.rounded_rectangle([x - 100, base - h, x + 100, base], 20, fill=col)
        text_c(d, (x, base + 50), lab, font(48, "bold"), WHITE)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([170, 300, 910, 420], 50, fill=th["accent"])
        text_c(d, (540, 360), "about 50% too many", font(int(56 * g) + 1, "bold"), DARK)
    text_c(d, (540, 1120), "illustration", font(36, "reg"), th["soft"])


def s4(img, d, t, T, th):
    kid(d, 300, 690, 1.2, BLUE)
    kid(d, 780, 690, 1.2, (250, 200, 90))
    if t > 0.4:
        g = pop(prog(t, 0.4, 0.4))
        bubble(d, 780, 420, 360 * g + 1, 140 * g + 1, (255, 255, 255, 220))
        text_c(d, (780, 420), "Saying no...", font(int(50 * g) + 1, "bold"), DARK)
    if t > 1.1:
        g = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([170, 1050, 910, 1170], 50, fill=th["accent"])
        text_c(d, (540, 1110), "is harder than we think", font(int(54 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    up = ease(prog(t, 0.3, 0.6))
    kid(d, 340, 760, 1.3, BLUE, arm_up=up)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        bubble(d, 720, 520, 420 * g + 1, 170 * g + 1, (255, 255, 255, 230), tail=(-1, -1))
        text_c(d, (720, 495), "Can you help me", font(int(44 * g) + 1, "bold"), DARK)
        text_c(d, (720, 550), "with this sum?", font(int(44 * g) + 1, "bold"), DARK)
    text_c(d, (540, 320), "Ask clearly", font(64, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "More people say", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 700), "YES", font(int(130 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 850), "than you think.", font(int(70 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Scared to ask for help? You might think people will say no.", draw=s1),
    dict(say="In Stanford studies, people asked strangers to lend a phone or fill in a form.", draw=s2),
    dict(say="They guessed they'd need to ask about fifty percent more people than needed.",
         show="They guessed they'd need to ask about 50% more people than needed.", draw=s3),
    dict(say="Why? For the person asked, saying no is harder than we think.", draw=s4),
    dict(say="Stuck on a sum? Ask your friend or teacher, clearly.", draw=s5),
    dict(say="More people say yes than you think.", draw=s6),
]
