from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Is the big pack always cheaper?"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
PACK_S, PACK_B, PACK2 = (255, 150, 90), (120, 180, 255), (255, 255, 255)
BIS, BIS2 = (225, 175, 100), (180, 130, 60)
GREEN, RED = (110, 220, 140), (255, 110, 110)

# example prices (an illustration, not real brands)
SMALL = dict(g=200, rs=40)   # ₹20 per 100 g
BIG = dict(g=500, rs=110)    # ₹22 per 100 g


def pack(d, x, y, w, h, col, label, price, g=1.0):
    w, h = w * g, h * g
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 24, fill=col, outline=PACK2, width=5)
    for i in range(3):
        cx = x - w / 4 + i * w / 4
        r = min(w, h) * 0.12
        d.ellipse([cx - r, y - r, cx + r, y + r], fill=BIS, outline=BIS2, width=3)
    if g > 0.6:
        text_c(d, (x, y - h / 2 + 50), label, font(int(46 * g) + 1, "bold"), DARK)
        text_c(d, (x, y + h / 2 - 50), price, font(int(50 * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    pack(d, 300, 680, 260, 330, PACK_S, "200 g", "₹40", pop(prog(t, 0.2, 0.4)))
    if t > 0.8:
        pack(d, 760, 640, 360, 440, PACK_B, "500 g", "₹110", pop(prog(t, 0.8, 0.4)))
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        text_c(d, (540, 1000), "Big = cheaper?", font(int(76 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 360), "Same biscuits", font(58, "bold"), WHITE)
    text_c(d, (540, 1120), "(example prices)", font(36, "reg"), th["soft"])


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Compare the same amount", font(54, "bold"), WHITE)
    text_c(d, (540, 430), "price for 100 g", font(48, "semi"), th["soft"])
    pack(d, 300, 690, 260, 330, PACK_S, "200 g", "₹40")
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        text_c(d, (760, 640), "₹40 ÷ 2", font(int(64 * g) + 1, "sym"), WHITE)
        d.rounded_rectangle([590, 720, 930, 830], 40, fill=GREEN)
        text_c(d, (760, 775), "₹20", font(int(64 * g) + 1, "bold"), DARK)
        text_c(d, (760, 890), "per 100 g", font(40, "semi"), WHITE)


def s3(img, d, t, T, th):
    pack(d, 300, 690, 300, 380, PACK_B, "500 g", "₹110")
    if t > 0.5:
        g = pop(prog(t, 0.5, 0.4))
        text_c(d, (770, 640), "₹110 ÷ 5", font(int(64 * g) + 1, "sym"), WHITE)
        d.rounded_rectangle([600, 720, 940, 830], 40, fill=RED)
        text_c(d, (770, 775), "₹22", font(int(64 * g) + 1, "bold"), DARK)
        text_c(d, (770, 890), "per 100 g", font(40, "semi"), WHITE)
    if t > 1.5:
        text_c(d, (540, 1060), "the BIG pack costs more!", font(54, "bold"), th["accent"])
    text_c(d, (540, 350), "Big pack", font(58, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "On the label", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([170, 440, 910, 860], 30, fill=(250, 250, 240))
    for i, (k, v) in enumerate([("Net qty", "500 g"), ("MRP", "₹110")]):
        y = 510 + i * 90
        text_c(d, (230, y), k, font(44, "semi"), (90, 90, 100), anchor="lm")
        text_c(d, (850, y), v, font(44, "bold"), DARK, anchor="rm")
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.4))
        d.rounded_rectangle([200, 700, 880, 820], 30, outline=RED, width=7)
        text_c(d, (540, 760), "Unit sale price", font(int(50 * g2) + 1, "bold"), DARK)
    if t > 1.3:
        text_c(d, (540, 960), "required on packs in India", font(46, "bold"), WHITE)
        text_c(d, (540, 1040), "since 2022", font(42, "semi"), th["soft"])


def s5(img, d, t, T, th):
    rows = [("small pack", "₹20 / 100 g", GREEN), ("big pack", "₹22 / 100 g", RED)]
    for i, (lab, v, col) in enumerate(rows):
        if t > 0.2 + 0.5 * i:
            g = pop(prog(t, 0.2 + 0.5 * i, 0.4))
            y = 520 + i * 230
            d.rounded_rectangle([110, y - 90, 970, y + 90], 40, fill=(255, 255, 255, 30), outline=col, width=5)
            text_c(d, (160, y), lab, font(int(50 * g) + 1, "bold"), WHITE, anchor="lm")
            text_c(d, (920, y), v, font(int(54 * g) + 1, "bold"), col, anchor="rm")
    if t > 1.4:
        text_c(d, (540, 1020), "Bigger isn't always cheaper", font(52, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Compare the", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "same amount.", font(int(72 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        d.rounded_rectangle([230, 790, 850, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "Then decide.", font(int(66 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Biscuits: two hundred grams for forty rupees, or five hundred grams for one hundred ten. Big pack's cheaper, right?",
         show="Biscuits: 200 g for ₹40, or 500 g for ₹110. Big pack's cheaper, right?", draw=s1),
    dict(say="Compare the same amount. Small pack: twenty rupees per hundred grams.",
         show="Compare the same amount. Small pack: ₹20 per 100 g.", draw=s2),
    dict(say="Big pack: twenty two rupees per hundred grams. It costs more!",
         show="Big pack: ₹22 per 100 g. It costs more!", draw=s3),
    dict(say="Since twenty twenty two, packs in India must show a unit sale price, to make comparing easier.",
         show="Since 2022, packs in India must show a unit sale price, to make comparing easier.", draw=s4),
    dict(say="Bigger isn't always cheaper.", draw=s5),
    dict(say="Compare the same amount. Then decide.", draw=s6),
]
