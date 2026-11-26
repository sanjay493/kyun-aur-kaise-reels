import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Can you spot the fake link?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
RED, GREEN, BAR = (255, 95, 95), (90, 210, 120), (235, 240, 250)
REAL, FAKE = "mybank.co.in", "rnybank.co.in"


def urlbar(d, y, txt, col=DARK, size=62, outline=None):
    d.rounded_rectangle([110, y - 70, W - 110, y + 70], 35, fill=BAR, outline=outline, width=8)
    text_c(d, (W / 2, y), txt, font(size, "bold"), col)


def s1(img, d, t, T, th):
    text_c(d, (540, 330), "Which one is fake?", font(62, "bold"), th["accent"])
    g1 = pop(prog(t, 0.2, 0.4))
    if g1 > 0:
        urlbar(d, 560, REAL, size=int(62 * g1) + 1)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.4))
        urlbar(d, 800, FAKE, size=int(62 * g2) + 1)
    text_c(d, (540, 1100), "made-up example", font(36, "reg"), th["soft"])


def s2(img, d, t, T, th):
    urlbar(d, 560, REAL, GREEN, outline=GREEN)
    urlbar(d, 800, FAKE, RED, outline=RED)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        # zoom on "rn" vs "m"
        d.rounded_rectangle([170, 940, 510, 1140], 40, fill=(255, 255, 255, 40), outline=RED, width=6)
        text_c(d, (340, 1040), "r n", font(int(110 * g) + 1, "bold"), RED)
        text_c(d, (590, 1040), "≈", font(90, "sym"), WHITE)
        d.rounded_rectangle([670, 940, 910, 1140], 40, fill=(255, 255, 255, 40), outline=GREEN, width=6)
        text_c(d, (790, 1040), "m", font(int(110 * g) + 1, "bold"), GREEN)
    text_c(d, (540, 330), "Look letter by letter", font(58, "bold"), WHITE)


def s3(img, d, t, T, th):
    # fake login page
    d.rounded_rectangle([230, 360, 850, 900], 40, fill=BAR)
    d.rounded_rectangle([230, 360, 850, 450], 40, fill=RED)
    text_c(d, (540, 405), FAKE, font(44, "bold"), WHITE)
    for i, lab in enumerate(("User ID", "Password")):
        y = 540 + i * 130
        d.rounded_rectangle([290, y - 45, 790, y + 45], 20, fill=WHITE, outline=(170, 175, 190), width=4)
        text_c(d, (540, y), lab, font(40, "semi"), (130, 135, 150))
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 830), "STEALS LOGINS", font(int(54 * g) + 1, "bold"), RED)
    if t > 1.3:
        d.rounded_rectangle([140, 980, 940, 1160], 50, fill=th["accent"])
        text_c(d, (540, 1035), "CERT-In: check spellings", font(46, "bold"), DARK)
        text_c(d, (540, 1105), "and domain names", font(46, "bold"), DARK)


def s4(img, d, t, T, th):
    # SMS with a link, crossed out
    d.rounded_rectangle([150, 380, 760, 620], 40, fill=(255, 255, 255, 220))
    text_c(d, (455, 450), "Your account is", font(42, "semi"), DARK)
    text_c(d, (455, 510), "blocked! Click:", font(42, "semi"), DARK)
    text_c(d, (455, 570), "rnybank-kyc.xyz", font(40, "bold"), (60, 110, 220))
    if t > 0.5:
        k = ease(prog(t, 0.5, 0.4))
        d.line([(150, 380), (150 + 610 * k, 380 + 240 * k)], fill=RED, width=14)
        d.line([(760, 380), (760 - 610 * k, 380 + 240 * k)], fill=RED, width=14)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        # official app icon
        d.rounded_rectangle([420, 760, 660, 1000], 50, fill=GREEN)
        text_c(d, (540, 880), "✓", font(int(130 * g) + 1, "sym"), WHITE)
        text_c(d, (540, 1080), "official app or website", font(50, "bold"), th["accent"])


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 360), "Money lost?", font(64, "bold"), WHITE)
    d.rounded_rectangle([290, 470, 790, 680], 60, fill=th["accent"])
    text_c(d, (540, 575), "1930", font(int(130 * g) + 1, "bold"), DARK)
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 790), "or report at", font(48, "semi"), th["soft"])
        urlbar(d, 920, "cybercrime.gov.in", DARK, int(56 * g2) + 1)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 580), "Read the link,", font(int(76 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "letter by letter.", font(int(76 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Two website links. One is fake. Can you spot it?", draw=s1),
    dict(say="In the second, r and n sit together, like an m.", draw=s2),
    dict(say="Fake sites steal logins. India's cyber agency, C.E.R.T. In, says: check the spelling in every link.",
         show="Fake sites steal logins. India's cyber agency, CERT-In, says: check the spelling in every link.",
         draw=s3),
    dict(say="Don't tap unknown links in messages. Use the official app or website.", draw=s4),
    dict(say="Lost money? Call one nine three zero, or report at cybercrime dot gov dot in.",
         show="Lost money? Call 1930, or report at cybercrime.gov.in", draw=s5),
    dict(say="Read the link, letter by letter.", draw=s6),
]
