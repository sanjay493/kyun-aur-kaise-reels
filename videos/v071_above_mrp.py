from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Charged more than the MRP?"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
PACK, PACK2, CHIP = (255, 120, 90), (210, 80, 60), (250, 210, 110)
LABEL, GREEN, RED = (250, 250, 240), (110, 220, 140), (255, 110, 110)
SHOP, AWN = (200, 120, 70), (230, 80, 80)


def packet(d, x, y, s=1.0, mrp="₹20"):
    w, h = 150 * s, 210 * s
    d.polygon([(x - w, y - h), (x + w, y - h), (x + w * 0.92, y + h), (x - w * 0.92, y + h)], fill=PACK, outline=PACK2)
    for i in range(6):
        d.line([(x - w + i * w / 3, y - h), (x - w + i * w / 3 + 12 * s, y - h - 14 * s)], fill=PACK2, width=int(5 * s) + 1)
    for dx, dy in [(-0.4, -0.25), (0.3, -0.35), (0.0, 0.05), (-0.3, 0.3), (0.4, 0.15)]:
        r = 30 * s
        d.ellipse([x + dx * w - r, y + dy * h - r * 0.7, x + dx * w + r, y + dy * h + r * 0.7], fill=CHIP)
    d.rounded_rectangle([x - 0.75 * w, y + 0.5 * h, x + 0.75 * w, y + 0.88 * h], int(10 * s) + 1, fill=LABEL)
    text_c(d, (x, y + 0.69 * h), f"MRP {mrp}", font(int(40 * s) + 1, "bold"), DARK)


def shop(d):
    for i in range(8):
        d.rectangle([140 + i * 100, 400, 240 + i * 100, 460], fill=AWN if i % 2 == 0 else WHITE)
    d.rectangle([140, 960, 940, 1100], fill=SHOP)


def s1(img, d, t, T, th):
    shop(d)
    packet(d, 380, 720, 1.0)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        d.rounded_rectangle([600, 560, 960, 700], 40, fill=WHITE)
        text_c(d, (780, 630), "\"₹25, please\"", font(int(48 * g) + 1, "bold"), RED)
    if t > 1.7:
        g = pop(prog(t, 1.7, 0.4))
        text_c(d, (780, 830), "Allowed?", font(int(72 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 1150), "(example prices)", font(36, "reg"), th["soft"])


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "MRP =", font(60, "bold"), WHITE)
    words = [("M", "aximum"), ("R", "etail"), ("P", "rice")]
    for i, (a, b) in enumerate(words):
        if t > 0.2 + 0.3 * i:
            g = pop(prog(t, 0.2 + 0.3 * i, 0.35))
            y = 480 + i * 120
            f = font(int(76 * g) + 1, "bold")
            x0 = 300
            d.text((x0, y), a, font=f, fill=th["accent"], anchor="lm")
            d.text((x0 + d.textlength(a, font=f), y), b, font=f, fill=WHITE, anchor="lm")
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([150, 880, 930, 1020], 50, fill=th["accent"])
        text_c(d, (540, 950), "the HIGHEST price", font(int(60 * g) + 1, "bold"), DARK)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "The rule in India", font(60, "bold"), th["accent"])
    packet(d, 540, 640, 0.85)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        d.rounded_rectangle([110, 900, 970, 1100], 50, fill=(255, 255, 255, 35), outline=RED, width=5)
        text_c(d, (540, 960), "No shop can sell a packed item", font(int(46 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 1040), "ABOVE its MRP", font(int(56 * g) + 1, "bold"), RED)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Below MRP?", font(66, "bold"), WHITE)
    packet(d, 540, 640, 0.85)
    if t > 0.4:
        g = pop(prog(t, 0.4, 0.4))
        d.rounded_rectangle([250, 900, 830, 1040], 50, fill=GREEN)
        text_c(d, (540, 970), "Fine: a discount", font(int(60 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Overcharged?", font(66, "bold"), RED)
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([140, 450, 940, 650], 50, fill=th["accent"])
    text_c(d, (540, 510), "National Consumer Helpline", font(int(44 * g) + 1, "bold"), DARK)
    text_c(d, (540, 590), "✆ 1915", font(int(70 * g) + 1, "sym"), DARK)
    if t > 1.0:
        for i, lab in enumerate(["NCH app", "consumerhelpline.gov.in"]):
            text_c(d, (540, 760 + i * 90), lab, font(48, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 980), "keep the bill or a photo", font(42, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Check before", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "you pay.", font(int(72 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        d.rounded_rectangle([120, 790, 960, 930], 50, fill=th["accent"])
        text_c(d, (540, 860), "Maximum means maximum.", font(int(48 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="A chips packet marked twenty rupees. The shopkeeper asks for twenty five. Allowed?",
         show="A chips packet marked ₹20. The shopkeeper asks for ₹25. Allowed?", draw=s1),
    dict(say="M.R.P. means Maximum Retail Price. The highest price it can be sold for.",
         show="MRP means Maximum Retail Price. The highest price it can be sold for.", draw=s2),
    dict(say="India's packaged goods rules say no shop can sell a packed item above its M.R.P.",
         show="India's packaged goods rules say no shop can sell a packed item above its MRP.", draw=s3),
    dict(say="Below M.R.P.? That's fine. That's a discount.", show="Below MRP? That's fine. That's a discount.", draw=s4),
    dict(say="Overcharged? Call the National Consumer Helpline, one nine one five.",
         show="Overcharged? Call the National Consumer Helpline, 1915.", draw=s5),
    dict(say="Check before you pay. Maximum means maximum.", draw=s6),
]
