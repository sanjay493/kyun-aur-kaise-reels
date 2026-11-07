from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "\"Electricity will be cut tonight\" — real?"
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)
SCREEN, GREY, BULB = (235, 240, 250), (120, 130, 150), (255, 220, 90)


def phone(d, cx, cy, s=1.0, screen=SCREEN):
    w, h = 440 * s, 760 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 50 * s, fill=DARK, outline=(200, 210, 230),
                        width=6)
    d.rounded_rectangle([cx - w / 2 + 18 * s, cy - h / 2 + 44 * s, cx + w / 2 - 18 * s, cy + h / 2 - 44 * s],
                        28 * s, fill=screen)
    return cx - w / 2 + 36 * s, cy - h / 2 + 70 * s


def sms(d, x, y, s=1.0, flag=0.0):
    lines = ["Dear customer, your", "electricity will be", "DISCONNECTED", "tonight at 9 PM.", "Bill not updated.",
             "Call officer:", "98XXX XXXXX"]
    d.rounded_rectangle([x - 6, y - 6, x + 360 * s, y + 470 * s], 24, fill=WHITE,
                        outline=RED if flag > 0 else GREY, width=int(3 + 6 * flag))
    for i, ln in enumerate(lines):
        col = RED if ln in ("DISCONNECTED", "98XXX XXXXX") else DARK
        text_c(d, (x + 20, y + 40 + i * 62), ln, font(int(28 * s), "bold" if col == RED else "semi"), col, anchor="lm")


def bulb(d, cx, cy, on=True):
    d.ellipse([cx - 60, cy - 70, cx + 60, cy + 50], fill=BULB if on else (90, 90, 100))
    d.rectangle([cx - 30, cy + 45, cx + 30, cy + 85], fill=(180, 180, 190))


def s1(img, d, t, T, th):
    x, y = phone(d, 540, 700, 1.0)
    sms(d, x, y)
    bulb(d, 900, 380, on=int(t * 4) % 2 == 0 or t < 1.0)
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1150), "Real?", font(int(80 * g) + 1, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    x, y = phone(d, 540, 680, 1.0)
    sms(d, x, y, flag=ease(prog(t, 0.3, 0.4)))
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        d.rounded_rectangle([230, 1000, 850, 1100], 30, fill=RED)
        text_c(d, (540, 1050), "PIB FACT CHECK: SCAM", font(int(50 * g) + 1, "bold"), WHITE)
    if t > 1.8:
        text_c(d, (540, 1160), "not sent by the Ministry of Power", font(36, "semi"), th["soft"])


def s3(img, d, t, T, th):
    d.ellipse([420, 320, 660, 560], fill=(90, 100, 130))
    d.ellipse([490, 350, 590, 450], fill=(200, 170, 140))
    d.chord([450, 440, 630, 630], 180, 360, fill=(60, 70, 100))
    text_c(d, (540, 610), "\"I'm the electricity officer\"", font(44, "semi"), th["soft"])
    asks = ["Share your bank details", "Install this remote-access app"]
    for i, lb in enumerate(asks):
        st = 0.8 + i * 1.2
        if t > st:
            g = pop(prog(t, st, 0.4))
            yy = 780 + i * 170
            d.rounded_rectangle([90, yy - 60, 990, yy + 60], 30, fill=WHITE)
            text_c(d, (540, yy), lb, font(int(46 * g) + 1, "bold"), RED)


def s4(img, d, t, T, th):
    x, y = phone(d, 540, 680, 0.9, screen=(60, 60, 80))
    k = ease(prog(t, 0.2, 0.8))
    # remote cursor wandering over the screen
    cx, cy = 420 + 200 * k, 520 + 260 * k
    d.polygon([(cx, cy), (cx, cy + 60), (cx + 16, cy + 46), (cx + 30, cy + 76), (cx + 42, cy + 70),
               (cx + 28, cy + 40), (cx + 48, cy + 40)], fill=WHITE, outline=DARK)
    text_c(d, (540, 450), "Remote control ON", font(34, "bold"), RED)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([170, 1060, 910, 1170], 36, fill=RED)
        text_c(d, (540, 1115), "They control your phone", font(int(50 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    x, y = phone(d, 540, 680, 1.0)
    d.rounded_rectangle([x, y, x + 368, y + 80], 16, fill=GREEN)
    text_c(d, (x + 184, y + 40), "Official website / app", font(28, "bold"), WHITE)
    text_c(d, (x + 184, y + 180), "Your electricity", font(36, "bold"), DARK)
    text_c(d, (x + 184, y + 230), "company", font(36, "bold"), DARK)
    text_c(d, (x + 184, y + 320), "Bill status: check here", font(28, "semi"), GREY)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.ellipse([870 - 70 * g, 520 - 70 * g, 870 + 70 * g, 520 + 70 * g], fill=GREEN, outline=WHITE, width=5)
        text_c(d, (870, 520), "✓", font(int(90 * g) + 1, "sym"), WHITE)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 540), "Panic is", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 640), "THEIR tool.", font(int(78 * g) + 1, "bold"), RED)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 820), "Pause is", font(int(72 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 920), "YOURS.", font(int(84 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your electricity will be cut tonight at nine p.m. Call our officer now. Real?",
         show="\"Your electricity will be cut tonight at 9 PM. Call our officer now.\" Real?", draw=s1),
    dict(say="P.I.B. Fact Check called this message a scam. The Ministry of Power never sent it.",
         show="PIB Fact Check called this message a scam. The Ministry of Power never sent it.", draw=s2),
    dict(say="Call, and the fake officer asks for bank details or a remote-access app.", draw=s3),
    dict(say="That app can hand them control of your phone.", draw=s4),
    dict(say="Check only through your electricity company's official website or app.", draw=s5),
    dict(say="Panic is their tool. Pause is yours.", draw=s6),
]
