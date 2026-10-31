import math, random
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Do you need your UPI PIN to receive money?"
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)


def phone(d, cx, cy, s=1.0):
    w, h = 300 * s, 560 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 46 * s, fill=DARK, outline=(200, 210, 230), width=6)
    d.rounded_rectangle([cx - w / 2 + 16 * s, cy - h / 2 + 40 * s, cx + w / 2 - 16 * s, cy + h / 2 - 40 * s], 26 * s,
                        fill=(235, 240, 250))
    d.rounded_rectangle([cx - 40 * s, cy - h / 2 + 14 * s, cx + 40 * s, cy - h / 2 + 26 * s], 6, fill=(90, 95, 110))


def qr(d, cx, cy, size):
    rnd = random.Random(3)
    n = 13; c = size / n; x0, y0 = cx - size / 2, cy - size / 2
    d.rectangle([x0 - 10, y0 - 10, x0 + size + 10, y0 + size + 10], fill=WHITE)
    for i in range(n):
        for j in range(n):
            corner = (i < 4 and j < 4) or (i > 8 and j < 4) or (i < 4 and j > 8)
            if not corner and rnd.random() < 0.5:
                d.rectangle([x0 + i * c, y0 + j * c, x0 + (i + 1) * c - 1, y0 + (j + 1) * c - 1], fill=DARK)
    for fi, fj in [(0, 0), (10, 0), (0, 10)]:  # finder squares (3x3 cells)
        fx, fy = x0 + fi * c, y0 + fj * c
        d.rectangle([fx, fy, fx + 3 * c, fy + 3 * c], outline=DARK, width=int(c * 0.7))
        d.rectangle([fx + c, fy + c, fx + 2 * c, fy + 2 * c], fill=DARK)


def cycle(d, x, y, s=1.0, col=(255, 200, 80)):
    r = 75 * s
    for wx in (x - 110 * s, x + 110 * s):
        d.ellipse([wx - r, y - r, wx + r, y + r], outline=WHITE, width=int(10 * s))
    d.line([(x - 110 * s, y), (x - 20 * s, y - 110 * s), (x + 80 * s, y - 110 * s), (x + 110 * s, y)], fill=col, width=int(12 * s))
    d.line([(x - 110 * s, y), (x + 10 * s, y), (x + 80 * s, y - 110 * s)], fill=col, width=int(12 * s))
    d.line([(x - 20 * s, y - 110 * s), (x - 30 * s, y - 150 * s)], fill=col, width=int(12 * s))
    d.line([(x - 60 * s, y - 155 * s), (x + 0 * s, y - 155 * s)], fill=WHITE, width=int(12 * s))


def s1(img, d, t, T, th):
    cycle(d, 280, 620, 1.0)
    d.rounded_rectangle([140, 720, 420, 800], 20, fill=th["accent"])
    text_c(d, (280, 760), "FOR SALE", font(40, "bold"), DARK)
    g = pop(prog(t, 0.6, 0.4))
    if g > 0:
        phone(d, 790, 640, 0.95 * g)
        if g > 0.9:
            text_c(d, (790, 450), "Buyer", font(34, "bold"), DARK)
            qr(d, 790, 640, 200)
            text_c(d, (790, 800), "Scan to receive", font(28, "bold"), RED)
            text_c(d, (790, 840), "₹2,500", font(40, "sym"), DARK)


def s2(img, d, t, T, th):
    phone(d, 540, 680, 1.1)
    text_c(d, (540, 450), "Enter UPI PIN", font(40, "bold"), DARK)
    n = min(6, int(t * 3))
    for k in range(6):
        x = 540 - 125 + k * 50
        if k < n:
            d.ellipse([x - 14, 520, x + 14, 548], fill=DARK)
        else:
            d.line([(x - 16, 550), (x + 16, 550)], fill=DARK, width=5)
    for r in range(4):
        for c in range(3):
            x, y = 540 - 90 + c * 90, 640 + r * 80
            d.ellipse([x - 32, y - 32, x + 32, y + 32], fill=(210, 215, 230))
            lab = "123456789 0 "[r * 3 + c]
            text_c(d, (x, y), lab, font(36, "bold"), DARK)
    g = pop(prog(t, 0.8, 0.4))
    if g > 0:
        d.rounded_rectangle([200, 1030, 880, 1130], 30, fill=(255, 255, 255, 240))
        text_c(d, (540, 1080), "...to RECEIVE money?", font(int(50 * g) + 1, "bold"), RED)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.0, 0.35))
    cx, cy, r = 540, 660, 260 * g
    pts = [(cx + r * math.cos(math.radians(22.5 + 45 * k)), cy + r * math.sin(math.radians(22.5 + 45 * k))) for k in range(8)]
    d.polygon(pts, fill=RED, outline=WHITE)
    text_c(d, (cx, cy), "STOP", font(int(130 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        text_c(d, (W / 2, 1060), "It's a trap", font(64, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)


def arrow(d, x0, x1, y, col, w=18):
    d.line([(x0, y), (x1, y)], fill=col, width=w)
    sgn = 1 if x1 > x0 else -1
    d.polygon([(x1 + sgn * 40, y), (x1, y - 32), (x1, y + 32)], fill=col)


def varrow(d, x, y0, y1, col, w=20):
    d.line([(x, y0), (x, y1)], fill=col, width=w)
    sgn = 1 if y1 > y0 else -1
    d.polygon([(x, y1 + sgn * 40), (x - 34, y1), (x + 34, y1)], fill=col)


def s4(img, d, t, T, th):
    d.rounded_rectangle([300, 340, 780, 580], 36, fill=(240, 240, 250))
    text_c(d, (540, 410), "YOUR ACCOUNT", font(44, "bold"), DARK)
    text_c(d, (540, 500), "₹", font(70, "sym"), GREEN)
    g1 = ease(prog(t, 0.2, 0.6))
    if g1 > 0:  # money OUT: arrow leaves the box downwards
        varrow(d, 700, 600, 600 + 260 * g1, RED)
        text_c(d, (760, 960), "Money OUT", font(46, "bold"), WHITE)
        text_c(d, (760, 1030), "PIN needed", font(46, "bold"), th["accent"])
    g2 = ease(prog(t, 1.2, 0.6))
    if g2 > 0:  # money IN: arrow comes up into the box
        varrow(d, 380, 900, 900 - 260 * g2, GREEN)
        text_c(d, (330, 960), "Money IN", font(46, "bold"), WHITE)
        text_c(d, (330, 1030), "NO PIN", font(46, "bold"), GREEN)


def coin(d, x, y, col=(255, 205, 60)):
    d.ellipse([x - 42, y - 42, x + 42, y + 42], fill=col, outline=(160, 120, 20), width=5)
    text_c(d, (x, y), "₹", font(44, "sym"), (120, 85, 10))


def s5(img, d, t, T, th):
    for x, lab, col in [(220, "YOU", (90, 170, 255)), (860, "SCAMMER", RED)]:
        d.ellipse([x - 70, 480, x + 70, 620], fill=(250, 205, 165))
        d.rounded_rectangle([x - 90, 630, x + 90, 820], 40, fill=col)
        text_c(d, (x, 880), lab, font(42, "bold"), WHITE)
    for j in range(4):
        p = clamp((t - 0.3 - j * 0.35) / 1.0)
        if p <= 0 or p >= 1: continue
        x = 300 + 480 * ease(p); y = 640 - 200 * math.sin(math.pi * p)
        coin(d, x, y)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (W / 2, 1040), "− ₹2,500", font(int(96 * g) + 1, "sym"), RED, stroke_width=6, stroke_fill=DARK)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([100, 340, W - 100, 760], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (W / 2, 460), "PIN  =  Paying", font(int(100 * g) + 1, "bold"), th["accent"])
    for k in range(6):
        x = 540 - 150 + k * 60
        d.ellipse([x - 16, 590, x + 16, 622], fill=WHITE)
    if t > 0.8:
        text_c(d, (W / 2, 880), "Receiving money:", font(50, "bold"), WHITE)
        text_c(d, (W / 2, 950), "no scan, no PIN", font(56, "bold"), GREEN)
    if t > 1.6:
        d.rounded_rectangle([110, 1090, 970, 1170], 24, fill=(255, 255, 255, 235))
        text_c(d, (540, 1130), "Cyber fraud helpline: 1930  ·  cybercrime.gov.in", font(34, "bold"), DARK)


SCENES = [
    dict(say="Someone wants to buy your old cycle online. They send a Q.R. code to pay you.",
         show="Someone wants to buy your old cycle online. They send a QR code to pay you.", draw=s1),
    dict(say="Scan it and enter your U.P.I. pin to receive the money, they say.",
         show="\"Scan it and enter your UPI PIN to receive the money,\" they say.", draw=s2),
    dict(say="Stop. That's a trap.", draw=s3),
    dict(say="Your U.P.I. pin is needed only when money leaves your account.",
         show="Your UPI PIN is needed only when money leaves your account.", draw=s4),
    dict(say="Enter it there, and the money goes from you to them.", draw=s5),
    dict(say="To receive money, you never scan or enter a pin. Remember: pin means paying.",
         show="To receive money, you never scan or enter a PIN. Remember: PIN means paying.", draw=s6),
]
