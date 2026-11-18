from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Can ₹7,371 be split among 9 friends?"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
NOTE, NOTE2 = (140, 210, 150), (90, 160, 105)
GREEN, RED, PINK = (110, 220, 140), (255, 110, 110), (255, 150, 200)
DIGITS = ["7", "3", "7", "1"]


def note(d, x, y, w=150, h=80):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 10, fill=NOTE, outline=NOTE2, width=4)
    d.ellipse([x - 22, y - 22, x + 22, y + 22], outline=NOTE2, width=4)


def friend(d, x, y, r=34, col=PINK):
    d.ellipse([x - r * 0.6, y - r * 1.6, x + r * 0.6, y - r * 0.4], fill=col)
    d.rounded_rectangle([x - r, y - r * 0.3, x + r, y + r], int(r * 0.6), fill=col)


def s1(img, d, t, T, th):
    for i in range(4):
        note(d, 540 + (i - 1.5) * 18, 470 - i * 14)
    g = pop(prog(t, 0.2, 0.4))
    text_c(d, (540, 600), "₹7,371", font(int(110 * g) + 1, "bold"), th["accent"])
    for i in range(9):
        if t > 0.6 + 0.08 * i:
            x = 140 + i * 100
            friend(d, x, 820, 30)
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 1000), "9 friends. Equal shares?", font(int(56 * g2) + 1, "bold"), WHITE)
    if t > 2.0:
        text_c(d, (540, 1110), "Don't divide. Add!", font(52, "bold"), GREEN)


def s2(img, d, t, T, th):
    for i, dg in enumerate(DIGITS):
        x = 240 + i * 200
        g = pop(prog(t, 0.2 + 0.25 * i, 0.35))
        d.rounded_rectangle([x - 75, 400, x + 75, 560], 30, fill=(255, 255, 255, 40), outline=th["accent"], width=5)
        text_c(d, (x, 480), dg, font(int(100 * g) + 1, "bold"), WHITE)
        if i < 3 and t > 0.4 + 0.25 * i:
            text_c(d, (x + 100, 480), "+", font(60, "bold"), th["accent"])
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 690), "= 18", font(int(110 * g) + 1, "bold"), th["accent"])
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        d.rounded_rectangle([170, 830, 910, 970], 50, fill=GREEN)
        text_c(d, (540, 900), "18 = 9 × 2  ✓", font(int(64 * g) + 1, "sym"), DARK)
        text_c(d, (540, 1080), "so 7,371 divides by 9 too", font(46, "semi"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 360), "But why?", font(70, "bold"), th["accent"])
    rows = [("10", "9", "1"), ("100", "99", "1")]
    for i, (a, b, c) in enumerate(rows):
        if t > 0.3 + 0.55 * i:
            g = pop(prog(t, 0.3 + 0.55 * i, 0.4))
            y = 540 + i * 190
            f = font(int(76 * g) + 1, "bold")
            text_c(d, (330, y), a, f, WHITE, anchor="rm")
            text_c(d, (380, y), "=", f, WHITE)
            text_c(d, (640, y), b, f, GREEN, anchor="rm")
            text_c(d, (700, y), "+", f, WHITE)
            text_c(d, (780, y), c, f, th["accent"])


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "7,371 =", font(60, "bold"), WHITE)
    parts = [("7 × 999", "7"), ("3 × 99", "3"), ("7 × 9", "7"), ("", "1")]
    for i, (n, left) in enumerate(parts):
        y = 480 + i * 115
        if t > 0.2 + 0.3 * i:
            if n:
                text_c(d, (420, y), n, font(56, "bold"), GREEN)
                text_c(d, (620, y), "+", font(56, "bold"), WHITE)
            text_c(d, (760, y), left, font(64, "bold"), th["accent"])
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        d.rounded_rectangle([140, 960, 560, 1060], 40, fill=GREEN)
        text_c(d, (350, 1010), "÷ 9 always", font(int(46 * g) + 1, "bold"), DARK)
        d.rounded_rectangle([600, 960, 940, 1060], 40, fill=th["accent"])
        text_c(d, (770, 1010), "digit sum", font(int(46 * g) + 1, "bold"), DARK)
    if t > 2.1:
        text_c(d, (540, 1150), "only the leftovers matter", font(44, "semi"), th["soft"])


def s5(img, d, t, T, th):
    for i in range(9):
        x = 140 + i * 100
        friend(d, x, 600, 30)
        if t > 0.2 + 0.08 * i:
            k = pop(prog(t, 0.2 + 0.08 * i, 0.3))
            note(d, x, 720, int(80 * k) + 1, int(44 * k) + 1)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 880), "₹819 each", font(int(100 * g) + 1, "bold"), th["accent"])
        text_c(d, (540, 1010), "9 × 819 = 7,371", font(50, "semi"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Big number?", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 640), "Add the digits.", font(int(76 * g) + 1, "bold"), th["accent"])
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        text_c(d, (540, 860), "The nines take care", font(int(58 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 940), "of themselves.", font(int(58 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Can seven thousand three hundred seventy one rupees be split equally among nine friends? Add the digits.",
         show="Can ₹7,371 be split equally among 9 friends? Add the digits.", draw=s1),
    dict(say="Seven, three, seven, one. That's eighteen, and eighteen divides by nine.",
         show="7, 3, 7, 1. That's 18, and 18 divides by 9.", draw=s2),
    dict(say="Why? Ten is nine plus one. A hundred is ninety nine plus one.",
         show="Why? 10 is 9 + 1. 100 is 99 + 1.", draw=s3),
    dict(say="The nines always divide. Only the digits are left over.", draw=s4),
    dict(say="So yes: eight hundred nineteen rupees each.", show="So yes: ₹819 each.", draw=s5),
    dict(say="Add the digits. The nines take care of themselves.", draw=s6),
]
