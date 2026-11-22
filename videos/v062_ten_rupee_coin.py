from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "\"This ₹10 coin is fake\"? Not so fast"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
RING, RING2, CORE, CORE2 = (230, 190, 90), (180, 140, 50), (205, 210, 220), (150, 155, 170)
SHOP, AWN = (200, 120, 70), (230, 80, 80)
GREEN, RED = (110, 220, 140), (255, 110, 110)


def coin(d, x, y, r=110, style=0):
    """Two-colour ₹10 coin: golden outer ring, silver centre. `style` varies the centre pattern."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=RING, outline=RING2, width=max(2, int(r * 0.05)))
    ri = r * 0.68
    d.ellipse([x - ri, y - ri, x + ri, y + ri], fill=CORE, outline=CORE2, width=max(2, int(r * 0.03)))
    if style % 3 == 0:
        text_c(d, (x, y), "₹10", font(max(8, int(r * 0.42)), "bold"), (90, 95, 110))
    elif style % 3 == 1:
        text_c(d, (x, y - ri * 0.1), "10", font(max(8, int(r * 0.45)), "bold"), (90, 95, 110))
        d.line([(x - ri * 0.5, y + ri * 0.45), (x + ri * 0.5, y + ri * 0.45)], fill=(90, 95, 110), width=max(2, int(r * 0.04)))
    else:
        text_c(d, (x, y - ri * 0.2), "₹", font(max(8, int(r * 0.4)), "bold"), (90, 95, 110))
        text_c(d, (x, y + ri * 0.35), "10", font(max(8, int(r * 0.3)), "bold"), (90, 95, 110))


def s1(img, d, t, T, th):
    # shop counter
    d.rectangle([140, 900, 940, 1060], fill=SHOP)
    for i in range(8):
        d.rectangle([140 + i * 100, 420, 240 + i * 100, 480], fill=AWN if i % 2 == 0 else WHITE)
    coin(d, 540, 760, 110)
    if t > 0.6:
        g = pop(prog(t, 0.6, 0.4))
        d.rounded_rectangle([200, 520, 880, 630], 40, fill=WHITE)
        text_c(d, (540, 575), "\"Fake! Won't take it.\"", font(int(46 * g) + 1, "bold"), DARK)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        text_c(d, (540, 1140), "Is he right?", font(int(64 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 350), "At the shop...", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Many designs", font(62, "bold"), th["accent"])
    for i in range(14):
        if t > 0.2 + 0.08 * i:
            g = pop(prog(t, 0.2 + 0.08 * i, 0.3))
            x, y = 190 + (i % 5) * 175, 500 + (i // 5) * 190
            coin(d, x, y, int(70 * g) + 1, i)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([160, 1050, 920, 1170], 50, fill=th["accent"])
        text_c(d, (540, 1110), "14 designs by 2018", font(int(54 * g) + 1, "bold"), DARK)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Why so many?", font(60, "bold"), WHITE)
    coin(d, 330, 600, 120, 0)
    coin(d, 750, 600, 120, 2)
    if t > 0.5:
        text_c(d, (540, 800), "new themes keep coming", font(48, "bold"), th["accent"])
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 930), "coins last for years,", font(int(50 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 1010), "so old + new circulate together", font(int(44 * g) + 1, "semi"), th["soft"])


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Reserve Bank of India:", font(54, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([140, 440, 940, 620], 50, fill=GREEN)
    text_c(d, (540, 530), "ALL are legal tender", font(int(60 * g) + 1, "bold"), DARK)
    for i in range(3):
        coin(d, 300 + i * 240, 790, 85, i)
    if t > 1.0:
        text_c(d, (540, 970), "can be accepted for", font(48, "bold"), WHITE)
        text_c(d, (540, 1040), "any payment", font(48, "bold"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "And banks?", font(62, "bold"), th["accent"])
    # bank building
    d.polygon([(260, 560), (540, 430), (820, 560)], fill=WHITE)
    for i in range(5):
        x = 300 + i * 120
        d.rectangle([x, 580, x + 40, 820], fill=WHITE)
    d.rectangle([250, 830, 830, 870], fill=WHITE)
    if t > 0.7:
        g = pop(prog(t, 0.7, 0.4))
        d.rounded_rectangle([160, 940, 920, 1070], 50, fill=GREEN)
        text_c(d, (540, 1005), "told to accept them", font(int(56 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 480), "New design", font(int(72 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 580), "isn't fake.", font(int(72 * g) + 1, "bold"), WHITE)
    coin(d, 540, 760, 90, 1)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        d.rounded_rectangle([170, 900, 910, 1040], 50, fill=th["accent"])
        text_c(d, (540, 970), "₹10 is still ₹10.", font(int(64 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="Shopkeeper: this ten rupee coin is fake, I won't take it. Is he right?",
         show="Shopkeeper: \"This ₹10 coin is fake, I won't take it.\" Is he right?", draw=s1),
    dict(say="Ten rupee coins come in many designs. By twenty eighteen, fourteen.",
         show="₹10 coins come in many designs. By 2018, 14 of them.", draw=s2),
    dict(say="New themes keep coming, and coins last years, so old and new circulate together.", draw=s3),
    dict(say="The Reserve Bank says all are legal tender, and can be accepted for payments.", draw=s4),
    dict(say="Banks were told to accept them too.", draw=s5),
    dict(say="New design isn't fake. Ten rupees is still ten rupees.",
         show="New design isn't fake. ₹10 is still ₹10.", draw=s6),
]
