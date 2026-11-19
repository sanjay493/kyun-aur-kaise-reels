from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Buy 2 get 1 free: half price?"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
SHIRT, SHIRT2, FREE = (110, 170, 255), (70, 120, 210), (255, 140, 170)
GREEN, RED = (110, 220, 140), (255, 110, 110)


def tshirt(d, x, y, s=1.0, col=SHIRT, label=None):
    w, h = 110 * s, 150 * s
    d.polygon([(x - w, y - h + 30 * s), (x - w * 0.45, y - h), (x + w * 0.45, y - h), (x + w, y - h + 30 * s),
               (x + w * 0.8, y - h + 90 * s), (x + w * 0.55, y - h + 70 * s), (x + w * 0.55, y + h * 0.7),
               (x - w * 0.55, y + h * 0.7), (x - w * 0.55, y - h + 70 * s), (x - w * 0.8, y - h + 90 * s)],
              fill=col)
    d.arc([x - 30 * s, y - h - 20 * s, x + 30 * s, y - h + 25 * s], 0, 180, fill=SHIRT2, width=int(6 * s) + 1)
    if label:
        text_c(d, (x, y), label, font(int(40 * s) + 1, "bold"), DARK)


def tag(d, x, y, s, col, size=48, g=1.0, w=300):
    d.rounded_rectangle([x - w / 2, y - 45, x + w / 2, y + 45], 30, fill=col)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    for i in range(3):
        if t > 0.1 + 0.25 * i:
            g = pop(prog(t, 0.1 + 0.25 * i, 0.35))
            tshirt(d, 240 + i * 300, 640, 0.9 * g + 0.01, FREE if i == 2 else SHIRT)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        tag(d, 840, 860, "FREE", FREE, 50, g, 220)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 1050), "Half price?", font(int(80 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 350), "Buy 2, get 1 free", font(64, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "₹100 each", font(60, "bold"), th["accent"])
    for i in range(3):
        tshirt(d, 240 + i * 300, 600, 0.8, FREE if i == 2 else SHIRT, "₹100" if i < 2 else "₹0")
    if t > 0.7:
        g = pop(prog(t, 0.7, 0.4))
        d.rounded_rectangle([110, 830, 520, 980], 40, fill=(255, 255, 255, 35), outline=RED, width=5)
        text_c(d, (315, 880), "you pay", font(40, "semi"), WHITE)
        text_c(d, (315, 940), "₹200", font(int(60 * g) + 1, "bold"), RED)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([560, 830, 970, 980], 40, fill=(255, 255, 255, 35), outline=GREEN, width=5)
        text_c(d, (765, 880), "you get", font(40, "semi"), WHITE)
        text_c(d, (765, 940), "3 shirts", font(int(60 * g) + 1, "bold"), GREEN)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.2, 0.45))
    text_c(d, (540, 430), "₹200 ÷ 3", font(int(96 * g) + 1, "sym"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        text_c(d, (540, 600), "= ₹66.67 each", font(int(80 * g2) + 1, "bold"), th["accent"])
    if t > 1.5:
        for i in range(3):
            tshirt(d, 300 + i * 240, 880, 0.6, SHIRT)
            text_c(d, (300 + i * 240, 1010), "₹66.67", font(40, "bold"), WHITE)


def s4(img, d, t, T, th):
    # bar: what you'd pay vs what you pay
    text_c(d, (540, 340), "Saved ₹100 of ₹300", font(56, "bold"), WHITE)
    k = ease(prog(t, 0.2, 0.8))
    x0, x1, y = 130, 950, 560
    d.rounded_rectangle([x0, y - 50, x1, y + 50], 25, fill=(255, 255, 255, 40))
    seg = (x1 - x0) / 3
    for i in range(3):
        col = GREEN if i == 2 else SHIRT
        d.rounded_rectangle([x0 + seg * i + 6, y - 44, x0 + seg * i + 6 + (seg - 12) * k, y + 44], 20, fill=col)
    text_c(d, (x0 + seg * 2.5, y + 100), "free", font(40, "bold"), GREEN)
    if t > 1.1:
        g = pop(prog(t, 1.1, 0.4))
        d.rounded_rectangle([190, 780, 890, 930], 50, fill=th["accent"])
        text_c(d, (540, 855), "1/3 off ≈ 33%", font(int(66 * g) + 1, "sym"), DARK)
    if t > 1.8:
        text_c(d, (540, 1030), "not 50%", font(60, "bold"), RED)


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "Buy 1, get 1 free", font(60, "bold"), th["accent"])
    tshirt(d, 370, 640, 0.9, SHIRT, "₹100")
    tshirt(d, 710, 640, 0.9, FREE, "₹0")
    if t > 0.7:
        g = pop(prog(t, 0.7, 0.4))
        d.rounded_rectangle([250, 880, 830, 1020], 50, fill=GREEN)
        text_c(d, (540, 950), "that's 50% off", font(int(62 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "What you pay", font(int(70 * g) + 1, "bold"), WHITE)
    d.line([(250, 580), (830, 580)], fill=WHITE, width=8)
    text_c(d, (540, 660), "What you get", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        d.rounded_rectangle([200, 820, 880, 960], 50, fill=th["accent"])
        text_c(d, (540, 890), "= the real price", font(int(62 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Buy two, get one free. Sounds like half price, right?", draw=s1),
    dict(say="Each T-shirt costs one hundred rupees. You pay two hundred and take home three.",
         show="Each T-shirt costs ₹100. You pay ₹200 and take home three.", draw=s2),
    dict(say="So each one costs about sixty six rupees sixty seven paise.",
         show="So each one costs about ₹66.67.", draw=s3),
    dict(say="You saved one third, about thirty three percent. Not half.",
         show="You saved one third, about 33%. Not half.", draw=s4),
    dict(say="Buy one, get one free? That one really is fifty percent off.",
         show="Buy one, get one free? That one really is 50% off.", draw=s5),
    dict(say="Divide what you pay by what you get. That's the real price.", draw=s6),
]
