from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Shared your WhatsApp code by mistake?"
WHITE, DARK = (255, 255, 255), (20, 25, 40)
GREEN, RED, GREY = (60, 200, 110), (240, 80, 80), (150, 155, 170)


def phone(d, x, y, w=380, h=620, screen=(240, 244, 246)):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 46, fill=(25, 28, 38), outline=(95, 100, 120),
                        width=6)
    d.rounded_rectangle([x - w / 2 + 20, y - h / 2 + 36, x + w / 2 - 20, y + h / 2 - 36], 28, fill=screen)


def code_boxes(d, cx, cy, digits, box=62, gap=12, fill=WHITE, ink=DARK, n=6):
    total = n * box + (n - 1) * gap
    x0 = cx - total / 2
    for i in range(n):
        x = x0 + i * (box + gap)
        d.rounded_rectangle([x, cy - box * 0.6, x + box, cy + box * 0.6], 12, fill=fill, outline=GREY, width=3)
        if i < len(digits):
            text_c(d, (x + box / 2, cy), digits[i], font(int(box * 0.62), "bold"), ink)


def lock(d, cx, cy, s=1.0, col=None, open_=0.0):
    col = col or (255, 140, 60)
    d.arc([cx - 45 * s, cy - 110 * s - 40 * s * open_, cx + 45 * s, cy - 20 * s - 40 * s * open_], 180, 360,
          fill=col, width=int(16 * s))
    d.line([(cx - 45 * s, cy - 65 * s - 40 * s * open_), (cx - 45 * s, cy - 30 * s)], fill=col, width=int(16 * s))
    d.line([(cx + 45 * s, cy - 65 * s - 40 * s * open_), (cx + 45 * s, cy - 30 * s)], fill=col, width=int(16 * s))
    d.rounded_rectangle([cx - 75 * s, cy - 40 * s, cx + 75 * s, cy + 70 * s], int(18 * s), fill=col)
    d.ellipse([cx - 13 * s, cy - 2 * s, cx + 13 * s, cy + 24 * s], fill=DARK)


def s1(img, d, t, T, th):
    phone(d, 540, 640)
    text_c(d, (540, 430), "WhatsApp code", font(36, "bold"), DARK)
    k = ease(prog(t, 0.2, 0.9))
    code_boxes(d, 540, 520, "482915"[:int(k * 6 + 0.001)], box=50, gap=4)
    text_c(d, (540, 620), "Don't share this code", font(26, "semi"), GREY)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([380, 700, 700, 790], 24, fill=(220, 248, 200))
        text_c(d, (540, 745), "Sent: 482915", font(int(36 * g) + 1, "bold"), DARK)
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1080), "Account gone?", font(int(76 * g) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    phone(d, 290, 640, 300, 500)
    phone(d, 790, 640, 300, 500, screen=(255, 225, 225))
    text_c(d, (290, 640), "YOUR\nphone", font(44, "bold"), DARK, align="center")
    text_c(d, (790, 560), "scammer's", font(36, "bold"), RED)
    text_c(d, (790, 620), "phone", font(36, "bold"), RED)
    k = ease(prog(t, 0.4, 1.0))
    bx = 290 + 500 * k
    d.rounded_rectangle([bx - 70, 820, bx + 70, 900], 20, fill=GREEN)
    text_c(d, (bx, 860), "chats", font(34, "bold"), WHITE)
    if k > 0.95:
        text_c(d, (790, 700), "your number", font(32, "semi"), DARK)
    if t > 1.5:
        text_c(d, (540, 1060), "code alone = enough", font(62, "bold"), th["accent"])


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    lock(d, 540, 560, 1.6 * g + 0.01)
    if t > 0.8:
        text_c(d, (540, 800), "Two-step verification", font(64, "bold"), WHITE)
    if t > 1.4:
        k = ease(prog(t, 1.4, 0.7))
        code_boxes(d, 540, 950, "******"[:int(k * 6 + 0.001)], fill=(255, 255, 255, 40), ink=th["accent"])
        text_c(d, (540, 1060), "6-digit PIN only YOU know", font(46, "bold"), th["soft"])


def s4(img, d, t, T, th):
    phone(d, 540, 620, 420, 640, screen=(255, 235, 235))
    text_c(d, (540, 380), "New phone?", font(40, "bold"), DARK)
    text_c(d, (540, 450), "SMS code", font(30, "semi"), GREY)
    code_boxes(d, 540, 510, "482915", box=54, gap=6)
    d.line([(450, 560), (480, 590), (530, 540)], fill=GREEN, width=8)
    text_c(d, (540, 640), "Enter your PIN", font(34, "bold"), DARK)
    code_boxes(d, 540, 710, "??????", box=54, gap=6, ink=RED)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([290, 820, 790, 900], 26, fill=RED)
        text_c(d, (540, 860), "BLOCKED", font(int(48 * g) + 1, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 1060), "code + PIN needed", font(62, "bold"), th["accent"])


def s5(img, d, t, T, th):
    steps = ["Settings", "Account", "Two-step verification", "Set a 6-digit PIN"]
    for i, s in enumerate(steps):
        g = ease(prog(t, 0.15 + i * 0.4, 0.35))
        if g <= 0:
            continue
        y = 400 + i * 170
        d.rounded_rectangle([170, y - 60, 910, y + 60], 30, fill=(255, 255, 255, int(40 * g)),
                            outline=th["accent"] + (int(255 * g),), width=4)
        text_c(d, (540, y), s, font(54, "bold"), (255, 255, 255, int(255 * g)))
        if i < 3:
            d.polygon([(520, y + 74), (560, y + 74), (540, y + 98)], fill=th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.05, 0.45))
    lock(d, 540, 580, 1.3 * g + 0.01)
    g2 = pop(prog(t, 0.5, 0.45))
    text_c(d, (540, 820), "Codes get stolen.", font(int(70 * g2) + 1, "bold"), WHITE)
    text_c(d, (540, 930), "Add a PIN lock.", font(int(70 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Someone tricks you into sharing your WhatsApp code. Is your account gone?", draw=s1),
    dict(say="It could be. With only that code, they can move your account to their phone.", draw=s2),
    dict(say="Add a second lock: two-step verification, a six-digit PIN only you know.",
         show="Add a second lock: two-step verification, a 6-digit PIN only you know.", draw=s3),
    dict(say="Then a new phone needs your PIN too, not just the S.M.S. code.",
         show="Then a new phone needs your PIN too, not just the SMS code.", draw=s4),
    dict(say="Turn it on in Settings, Account, Two-step verification.",
         show="Turn it on in Settings > Account > Two-step verification.", draw=s5),
    dict(say="Codes can be stolen. Add a lock only you know.", draw=s6),
]
