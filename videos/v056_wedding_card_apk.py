import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "A wedding card that ends in .apk?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
PHONE, SCREEN = (40, 45, 60), (235, 240, 250)
RED, GREEN, BUBBLE = (255, 95, 95), (90, 210, 120), (220, 248, 200)
CARD, CARD2 = (250, 220, 150), (210, 150, 60)


def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 170 * s, y - 320 * s, x + 170 * s, y + 320 * s], int(40 * s), fill=PHONE)
    d.rounded_rectangle([x - 150 * s, y - 290 * s, x + 150 * s, y + 290 * s], int(28 * s), fill=SCREEN)


def file_chip(d, x, y, name, g=1.0, col=RED):
    d.rounded_rectangle([x - 135, y - 45, x + 135, y + 45], 18, fill=WHITE, outline=col, width=5)
    text_c(d, (x, y), name, font(int(34 * g) + 1, "bold"), col)


def card(d, x, y, s=1.0):
    d.rounded_rectangle([x - 120 * s, y - 160 * s, x + 120 * s, y + 160 * s], int(16 * s), fill=CARD, outline=CARD2, width=6)
    d.ellipse([x - 40 * s, y - 110 * s, x + 40 * s, y - 30 * s], outline=CARD2, width=6)
    for i in range(3):
        yy = y + 20 * s + i * 40 * s
        d.line([(x - 80 * s, yy), (x + 80 * s, yy)], fill=CARD2, width=5)


def s1(img, d, t, T, th):
    phone(d, 540, 720)
    text_c(d, (540, 470), "Unknown number", font(30, "semi"), (90, 90, 110))
    if t > 0.3:
        g = pop(prog(t, 0.3, 0.4))
        d.rounded_rectangle([405, 510, 675, 620], 22, fill=BUBBLE)
        text_c(d, (540, 545), "You're invited!", font(int(30 * g) + 1, "bold"), DARK)
        text_c(d, (540, 590), "Open the card", font(int(28 * g) + 1, "semi"), DARK)
    if t > 1.0:
        file_chip(d, 540, 700, "card.apk", pop(prog(t, 1.0, 0.4)))
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.ellipse([440, 800, 640, 1000], outline=RED, width=10)
        text_c(d, (540, 900), ".apk", font(int(60 * g) + 1, "bold"), RED)
    text_c(d, (540, 340), "Wedding card?", font(64, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), ".apk = an app", font(64, "bold"), th["accent"])
    card(d, 300, 650, 0.9)
    d.line([(160, 470), (440, 830)], fill=RED, width=14)
    d.line([(440, 470), (160, 830)], fill=RED, width=14)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        s = g
        d.rounded_rectangle([700 - 110 * s, 650 - 110 * s, 700 + 110 * s, 650 + 110 * s], int(30 * s) + 1, fill=GREEN)
        text_c(d, (700, 650), "APP", font(int(60 * g) + 1, "bold"), DARK)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([140, 930, 940, 1070], 50, fill=RED)
        text_c(d, (540, 1000), "can take over your phone", font(int(50 * g) + 1, "bold"), WHITE)


def s3(img, d, t, T, th):
    phone(d, 540, 700, 0.9)
    d.rounded_rectangle([420, 480, 660, 580], 20, fill=(220, 225, 240))
    text_c(d, (540, 530), "OTP 4•8•2•9", font(34, "bold"), DARK)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([170, 880, 910, 1010], 50, fill=th["accent"])
        text_c(d, (540, 945), "OTPs → bank account", font(int(54 * g) + 1, "sym"), DARK)
    text_c(d, (540, 340), "They can read your OTPs", font(56, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Then it spreads", font(60, "bold"), th["accent"])
    phone(d, 540, 730, 0.45)
    for i in range(6):
        a = math.radians(-90 + i * 60)
        k = ease(prog(t, 0.3 + 0.12 * i, 0.5))
        x, y = 540 + 290 * k * math.cos(a), 730 + 280 * k * math.sin(a)
        if k > 0.05:
            d.line([(540, 730), (x, y)], fill=(255, 255, 255, 90), width=4)
            file_chip(d, x, y, ".apk", 0.8, RED) if k > 0.9 else None
    if t > 1.6:
        text_c(d, (540, 1130), "same fake invite to your contacts", font(44, "semi"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Real cards come as", font(58, "bold"), WHITE)
    for i, (lab, x) in enumerate([("photo .jpg", 300), ("PDF .pdf", 780)]):
        if t > 0.2 + 0.3 * i:
            g = pop(prog(t, 0.2 + 0.3 * i, 0.4))
            file_chip(d, x, 500, lab, g, GREEN)
    card(d, 540, 700, 0.6)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([140, 900, 940, 1040], 50, fill=th["accent"])
        text_c(d, (540, 970), "Not sure? Call the sender.", font(int(50 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), ".apk", font(int(110 * g) + 1, "bold"), RED)
    text_c(d, (540, 640), "is not an invitation.", font(int(62 * g) + 1, "bold"), WHITE)
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        d.rounded_rectangle([210, 800, 870, 940], 50, fill=th["accent"])
        text_c(d, (540, 870), "Don't install it.", font(int(62 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="WhatsApp: You're invited, open the wedding card. But the file ends in dot A.P.K.",
         show="WhatsApp: \"You're invited, open the wedding card.\" But the file ends in .apk.", draw=s1),
    dict(say="That's an app, not a card. Install it, and scammers can control your phone.", draw=s2),
    dict(say="They can read your O.T.P.s and get into your bank account.",
         show="They can read your OTPs and get into your bank account.", draw=s3),
    dict(say="Some even send the same fake invite to your contacts.", draw=s4),
    dict(say="Real cards come as photos or P.D.F.s. Not sure? Call the sender.",
         show="Real cards come as photos or PDFs. Not sure? Call the sender.", draw=s5),
    dict(say="Dot A.P.K. is not an invitation. Don't install it.",
         show=".apk is not an invitation. Don't install it.", draw=s6),
]
