import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Paid to like videos? It's a trap"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
PHONE, SCREEN = (40, 45, 60), (235, 240, 250)
RED, GREEN, BUBBLE = (255, 95, 95), (90, 210, 120), (220, 248, 200)
COIN, COIN2 = (250, 200, 70), (200, 150, 40)


def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 170 * s, y - 320 * s, x + 170 * s, y + 320 * s], int(40 * s), fill=PHONE)
    d.rounded_rectangle([x - 150 * s, y - 290 * s, x + 150 * s, y + 290 * s], int(28 * s), fill=SCREEN)


def bubble(d, x0, y0, x1, y1, lines, g=1.0, col=BUBBLE, size=34):
    d.rounded_rectangle([x0, y0, x1, y1], 22, fill=col)
    for i, ln in enumerate(lines):
        text_c(d, ((x0 + x1) / 2, y0 + 40 + i * 46), ln, font(int(size * g) + 1, "bold"), DARK)


def coin(d, x, y, r=44, label="₹"):
    d.ellipse([x - r, y - r, x + r, y + r], fill=COIN, outline=COIN2, width=5)
    text_c(d, (x, y), label, font(max(1, int(r * 0.9)), "bold"), (120, 80, 20))


def thumb(d, x, y, s=1.0, col=(80, 150, 255)):
    d.rounded_rectangle([x - 30 * s, y - 10 * s, x + 30 * s, y + 45 * s], int(10 * s), fill=col)
    d.rounded_rectangle([x - 12 * s, y - 50 * s, x + 12 * s, y], int(10 * s), fill=col)


def s1(img, d, t, T, th):
    phone(d, 540, 720)
    text_c(d, (540, 470), "Unknown number", font(30, "semi"), (90, 90, 110))
    if t > 0.3:
        g = pop(prog(t, 0.3, 0.4))
        bubble(d, 410, 510, 680, 650, ["Like 3 videos,", "earn money", "from home!"], g)
    if t > 1.0:
        for i in range(3):
            if t > 1.0 + 0.25 * i:
                thumb(d, 450 + i * 90, 760, pop(prog(t, 1.0 + 0.25 * i, 0.3)) * 0.9 + 0.01)
    if t > 1.9:
        g = pop(prog(t, 1.9, 0.4))
        coin(d, 540, 920, int(60 * g) + 1)
        text_c(d, (540, 1110), "...and they do pay!", font(50, "bold"), th["accent"])
    text_c(d, (540, 330), "Easy money?", font(64, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "The small payment", font(60, "bold"), WHITE)
    # coin on a fishing hook
    k = ease(prog(t, 0.2, 0.8))
    y = 470 + 160 * k
    d.line([(540, 410), (540, y - 60)], fill=(200, 200, 210), width=5)
    d.arc([500, y - 70, 580, y + 10], 0, 180, fill=(200, 200, 210), width=8)
    coin(d, 540, y + 50, 70)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([250, 860, 830, 990], 50, fill=th["accent"])
        text_c(d, (540, 925), "is the BAIT", font(int(64 * g) + 1, "bold"), DARK)
    if t > 1.5:
        text_c(d, (540, 1090), "to win your trust", font(48, "semi"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "Next step:", font(56, "bold"), th["accent"])
    phone(d, 540, 730, 0.95)
    if t > 0.3:
        g = pop(prog(t, 0.3, 0.4))
        bubble(d, 405, 500, 675, 640, ["Pay first for a", "\"prepaid task\"", "More commission!"], g, size=27)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        r = 70 * g + 1
        d.ellipse([540 - r, 820 - r, 540 + r, 820 + r], fill=RED)
        text_c(d, (540, 820), "PAY", font(int(44 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    # stack of coins climbing, then vanishing
    n = int(1 + 6 * ease(prog(t, 0.1, 1.5)))
    gone = ease(prog(t, 2.1, 0.6))
    for i in range(n):
        for j in range(i + 1):
            x = 200 + i * 115
            y = 1000 - j * 55 - 60 * gone * (i + 1)
            if gone < 0.95:
                d.ellipse([x - 48, y - 22, x + 48, y + 22], fill=COIN, outline=COIN2, width=4)
    text_c(d, (540, 350), "You pay more...", font(56, "bold"), WHITE)
    if t > 2.1:
        g = pop(prog(t, 2.1, 0.4))
        d.rounded_rectangle([170, 560, 910, 700], 50, fill=RED)
        text_c(d, (540, 630), "...then they vanish", font(int(58 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    d.rounded_rectangle([110, 380, 970, 620], 50, fill=(255, 255, 255, 35), outline=th["accent"], width=5)
    text_c(d, (540, 450), "Asked to pay", font(int(60 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 545), "to earn?  STOP.", font(int(60 * g) + 1, "bold"), th["accent"])
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        d.rounded_rectangle([260, 740, 820, 900], 50, fill=GREEN)
        text_c(d, (540, 820), "Report: 1930", font(int(64 * g2) + 1, "bold"), DARK)
        text_c(d, (540, 990), "cybercrime.gov.in", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Easy money that", font(int(66 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "wants your money", font(int(66 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        d.rounded_rectangle([250, 790, 830, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "is a trap.", font(int(70 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="A WhatsApp message: like a few videos, earn money from home. And they pay!", draw=s1),
    dict(say="That small payment is bait, to win your trust.", draw=s2),
    dict(say="Next, they ask you to pay for bigger prepaid tasks, promising more commission.", draw=s3),
    dict(say="You pay more. Then the money is stuck, and they vanish.", draw=s4),
    dict(say="Asked to pay before you earn? Stop. Report it on one nine three zero.",
         show="Asked to pay before you earn? Stop. Report it on 1930.", draw=s5),
    dict(say="Easy money that wants your money is a trap.", draw=s6),
]
