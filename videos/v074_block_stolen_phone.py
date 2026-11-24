import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Phone stolen? Block it"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
PHONE, SCREEN = (40, 45, 60), (235, 240, 250)
RED, GREEN, BLUE, PAPER = (255, 95, 95), (90, 210, 120), (100, 170, 255), (245, 245, 235)


def phone(d, x, y, s=1.0, scr=SCREEN):
    d.rounded_rectangle([x - 170 * s, y - 320 * s, x + 170 * s, y + 320 * s], int(40 * s) + 1, fill=PHONE)
    d.rounded_rectangle([x - 150 * s, y - 290 * s, x + 150 * s, y + 290 * s], int(28 * s) + 1, fill=scr)


def tower(d, x, y, s=1.0, col=WHITE):
    d.polygon([(x, y - 160 * s), (x - 60 * s, y + 60 * s), (x + 60 * s, y + 60 * s)], outline=col, width=int(6 * s) + 1)
    d.line([(x, y - 160 * s), (x, y + 60 * s)], fill=col, width=int(5 * s) + 1)
    for r in (40, 70):
        d.arc([x - r * s, y - 160 * s - r * s, x + r * s, y - 160 * s + r * s], 200, 340, fill=col, width=int(5 * s) + 1)


def s1(img, d, t, T, th):
    k = ease(prog(t, 0.3, 0.8))
    phone(d, 540 + 500 * k, 680, 0.8)
    if t > 0.5:
        # hand grabbing from the right
        d.rounded_rectangle([760 + 500 * k, 600, 980 + 500 * k, 760], 50, fill=(200, 150, 110))
    if t > 1.1:
        g = pop(prog(t, 1.1, 0.4))
        text_c(d, (540, 650), "STOLEN!", font(int(100 * g) + 1, "bold"), RED)
    if t > 1.8:
        g = pop(prog(t,1.8, 0.4))
        d.rounded_rectangle([200, 900, 880, 1040], 50, fill=th["accent"])
        text_c(d, (540, 970), "You can block it", font(int(58 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    phone(d, 540, 700, 0.9)
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([420, 470, 660, 560], 20, fill=(255, 150, 60))
    text_c(d, (540, 515), "GOVT", font(int(40 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 640), "Sanchar", font(int(52 * g) + 1, "bold"), DARK)
    text_c(d, (540, 710), "Saathi", font(int(52 * g) + 1, "bold"), DARK)
    text_c(d, (540, 820), "portal or app", font(34, "semi"), (90, 90, 110))
    text_c(d, (540, 1110), "sancharsaathi.gov.in", font(46, "bold"), th["accent"])


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "You'll need", font(62, "bold"), th["accent"])
    items = ["police complaint copy", "phone's IMEI number", "a number for the OTP"]
    for i, lab in enumerate(items):
        if t > 0.3 + 0.6 * i:
            g = pop(prog(t, 0.3 + 0.6 * i, 0.4))
            y = 520 + i * 190
            d.rounded_rectangle([110, y - 75, 970, y + 75], 40, fill=(255, 255, 255, 30), outline=WHITE, width=4)
            d.ellipse([140, y - 45, 230, y + 45], fill=th["accent"])
            text_c(d, (185, y), str(i + 1), font(54, "bold"), DARK)
            text_c(d, (600, y), lab, font(int(50 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    for i, x in enumerate([220, 540, 860]):
        tower(d, x, 620, 0.9)
        if t > 0.4 + 0.25 * i:
            g = pop(prog(t, 0.4 + 0.25 * i, 0.35))
            r = 50 * g + 1
            d.ellipse([x - r, 470 - r, x + r, 470 + r], outline=RED, width=10)
            d.line([(x - r * 0.7, 470 + r * 0.7), (x + r * 0.7, 470 - r * 0.7)], fill=RED, width=10)
    text_c(d, (540, 350), "Blocked on all Indian networks", font(50, "bold"), WHITE)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([170, 860, 910, 990], 50, fill=th["accent"])
        text_c(d, (540, 925), "and police can trace it", font(int(54 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Found it later?", font(62, "bold"), WHITE)
    phone(d, 540, 720, 0.7)
    g = pop(prog(t, 0.4, 0.45))
    r = 80 * g + 1
    d.ellipse([540 - r, 720 - r, 540 + r, 720 + r], fill=GREEN)
    text_c(d, (540, 720), "✓", font(int(90 * g) + 1, "sym"), WHITE)
    if t > 0.9:
        text_c(d, (540, 1020), "unblock it on the same portal", font(48, "bold"), GREEN)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Lost phone?", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 700), "Report it.", font(int(76 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 820), "Then block it.", font(int(76 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your phone is stolen. Scared someone will misuse it? You can block it.", draw=s1),
    dict(say="Use the government's Sanchar Saathi portal or app.", draw=s2),
    dict(say="You'll need a police complaint copy, your phone's I.M.E.I. number, and a mobile number for the O.T.P.",
         show="You'll need a police complaint copy, your phone's IMEI number, and a mobile number for the OTP.", draw=s3),
    dict(say="Then it's blocked on all Indian networks, and police can trace it.", draw=s4),
    dict(say="Found it later? Unblock it on the same portal.", draw=s5),
    dict(say="Lost phone? Report it, then block it.", draw=s6),
]
