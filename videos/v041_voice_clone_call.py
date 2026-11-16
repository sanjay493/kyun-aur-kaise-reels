import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Is that really your uncle calling?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
PHONE, SCREEN = (40, 45, 60), (235, 240, 250)
RED, GREEN, BLUE = (255, 95, 95), (90, 210, 120), (100, 170, 255)


def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 170 * s, y - 320 * s, x + 170 * s, y + 320 * s], int(40 * s), fill=PHONE)
    d.rounded_rectangle([x - 150 * s, y - 290 * s, x + 150 * s, y + 290 * s], int(28 * s), fill=SCREEN)


def wave(d, x, y, w, t, amp=40, col=BLUE, n=24):
    for i in range(n):
        h = amp * (0.3 + 0.7 * abs(math.sin(t * 6 + i * 0.7)))
        xx = x - w / 2 + i * w / (n - 1)
        d.rounded_rectangle([xx - 6, y - h, xx + 6, y + h], 6, fill=col)


def s1(img, d, t, T, th):
    sh = 6 * math.sin(t * 40) if t < 1.2 else 0
    phone(d, 540 + sh, 700)
    text_c(d, (540, 520), "New number", font(34, "semi"), (90, 90, 110))
    text_c(d, (540, 580), "+91 9xxxx xxxxx", font(34, "reg"), (120, 120, 140))
    wave(d, 540, 720, 220, t, 36, RED)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([170, 860 - 10, 910, 990], 30, fill=(255, 255, 255))
        text_c(d, (540, 885), "\"Accident! Send money", font(int(42 * g) + 1, "bold"), DARK)
        text_c(d, (540, 945), "RIGHT NOW!\"", font(int(42 * g) + 1, "bold"), RED)
    text_c(d, (540, 330), "uncle's voice...", font(54, "bold"), th["accent"])


def s2(img, d, t, T, th):
    # social media video -> AI box -> copied voice
    d.rounded_rectangle([90, 470, 330, 750], 24, fill=SCREEN)
    d.polygon([(185, 560), (185, 660), (260, 610)], fill=RED)
    text_c(d, (210, 800), "video clip", font(38, "semi"), WHITE)
    k = ease(prog(t, 0.3, 0.6))
    d.line([(350, 610), (350 + 70 * k, 610)], fill=WHITE, width=8)
    g = pop(prog(t, 0.6, 0.4))
    d.rounded_rectangle([440, 520, 640, 700], 30, fill=th["accent"])
    text_c(d, (540, 610), "A.I.", font(int(64 * g) + 1, "bold"), DARK)
    k2 = ease(prog(t, 1.0, 0.6))
    d.line([(660, 610), (660 + 70 * k2, 610)], fill=WHITE, width=8)
    if t > 1.4:
        wave(d, 870, 610, 200, t, 50, BLUE, 12)
        text_c(d, (870, 800), "copied voice", font(38, "semi"), WHITE)
    text_c(d, (540, 360), "Voices can be copied", font(58, "bold"), WHITE)
    if t > 1.9:
        text_c(d, (540, 1000), "from social media clips", font(48, "bold"), th["accent"])


def s3(img, d, t, T, th):
    # panic meter rising
    text_c(d, (540, 360), "PANIC", font(80, "bold"), RED)
    k = ease(prog(t, 0.2, 1.2))
    d.rounded_rectangle([200, 520, 880, 600], 40, fill=(255, 255, 255, 40))
    d.rounded_rectangle([200, 520, 200 + max(80, 680 * k), 600], 40, fill=RED)
    for i, w in enumerate(["hurry", "now", "don't tell anyone"]):
        if t > 0.4 + 0.35 * i:
            text_c(d, (540, 720 + i * 90), w, font(48, "semi"), WHITE)
    if t > 1.8:
        text_c(d, (540, 1100), "so you don't stop to think", font(46, "bold"), th["accent"])


def s4(img, d, t, T, th):
    phone(d, 540, 700, 0.95)
    if t < 1.0:
        g = pop(prog(t, 0.1, 0.4))
        r = 80 * g + 1
        d.ellipse([540 - r, 700 - r, 540 + r, 700 + r], fill=RED)
        text_c(d, (540, 700), "✆", font(int(80 * g) + 1, "sym"), WHITE)
        text_c(d, (540, 520), "hang up", font(50, "bold"), DARK)
    else:
        text_c(d, (540, 500), "Saved contacts", font(28, "semi"), (90, 90, 110))
        d.rounded_rectangle([420, 560, 660, 640], 20, fill=(220, 225, 240))
        text_c(d, (540, 600), "Chacha", font(44, "bold"), DARK)
        g = pop(prog(t, 1.0, 0.4))
        r = 80 * g + 1
        d.ellipse([540 - r, 780 - r, 540 + r, 780 + r], fill=GREEN)
        text_c(d, (540, 780), "✆", font(int(80 * g) + 1, "sym"), WHITE)
    text_c(d, (540, 1130), "call back on the saved number", font(46, "bold"), th["accent"])


def s5(img, d, t, T, th):
    text_c(d, (540, 360), "family code word", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.3, 0.45))
    d.rounded_rectangle([200, 520, 880, 760], 50, fill=(255, 255, 255, 40), outline=WHITE, width=5)
    text_c(d, (540, 640), "★ ★ ★ ★ ★", font(int(70 * g) + 1, "sym"), WHITE)
    if t > 1.0:
        text_c(d, (540, 880), "only your family knows it", font(48, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "A familiar voice", font(int(66 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "isn't proof.", font(int(66 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        d.rounded_rectangle([200, 790, 880, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "Call back first", font(int(66 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Your uncle calls from a new number, crying. There's been an accident. Send money now!", draw=s1),
    dict(say="But scammers can now copy a voice with A.I., using clips from social media videos.",
         show="But scammers can now copy a voice with AI, using clips from social media videos.", draw=s2),
    dict(say="They create panic so you don't stop to think.", draw=s3),
    dict(say="So hang up. Call back on the number you've saved for him.", draw=s4),
    dict(say="Families can also agree on a secret code word for emergencies.", draw=s5),
    dict(say="A familiar voice isn't proof. Call back first.", draw=s6),
]
