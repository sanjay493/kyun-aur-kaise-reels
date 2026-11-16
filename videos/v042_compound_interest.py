from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "₹100 at 10% for 3 years: ₹130?"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
COIN, COIN2 = (250, 200, 70), (200, 150, 40)
SI_COL = (150, 200, 255)

SI = [100, 110, 120, 130]
CI = [100, 110, 121, 133.10]


def coin(d, x, y, r=44, label="₹"):
    d.ellipse([x - r, y - r, x + r, y + r], fill=COIN, outline=COIN2, width=5)
    text_c(d, (x, y), label, font(max(1, int(r * (0.9 if len(label) <= 2 else 1.7 / len(label)))), "bold"), (120, 80, 20))


def money(v):
    return f"₹{v:.2f}".replace(".00", "") if isinstance(v, float) else f"₹{v}"


def bars(d, t, vals, col, x0, label, start=0.3):
    base, top = 1020, 520
    for i, v in enumerate(vals):
        k = ease(prog(t, start + 0.3 * i, 0.4))
        x = x0 + i * 110
        h = (v / 140) * (base - top) * k
        d.rounded_rectangle([x - 40, base - h, x + 40, base], 12, fill=col)
        if k > 0.6:
            text_c(d, (x, base - h - 28), money(v), font(28, "bold"), WHITE)
        text_c(d, (x, base + 32), f"yr {i}", font(28, "semi"), (210, 230, 220))
    text_c(d, (x0 + 165, 440), label, font(44, "bold"), col)


def s1(img, d, t, T, th):
    coin(d, 540, 520, 120, "₹100")
    g = pop(prog(t, 0.6, 0.4))
    d.rounded_rectangle([250, 700, 830, 820], 40, fill=th["accent"])
    text_c(d, (540, 760), "10% a year", font(int(62 * g) + 1, "bold"), DARK)
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 950), "after 3 years...", font(int(56 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 1060), "₹130?", font(int(84 * g2) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "Simple interest", font(60, "bold"), SI_COL)
    for i in range(3):
        if t > 0.3 + 0.4 * i:
            g = pop(prog(t, 0.3 + 0.4 * i, 0.35))
            x = 270 + i * 270
            coin(d, x, 600, int(60 * g) + 1, "+10")
            text_c(d, (x, 710), f"year {i + 1}", font(36, "semi"), WHITE)
    if t > 1.6:
        text_c(d, (540, 880), "on the same ₹100", font(54, "bold"), WHITE)
        text_c(d, (500, 990), "₹130", font(70, "bold"), SI_COL)
        text_c(d, (640, 990), "✓", font(70, "sym"), SI_COL)


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "Compound interest", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.3, 0.4))
    d.rounded_rectangle([160, 450, 920, 600], 40, fill=(255, 255, 255, 35))
    text_c(d, (540, 525), "interest on last year's amount", font(int(42 * g) + 1, "bold"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 700), "Year 2", font(48, "semi"), th["soft"])
        text_c(d, (540, 810), "10% of ₹110 = ₹11", font(int(64 * g2) + 1, "bold"), th["accent"])
        coin(d, 540, 990, 70, "+11")


def s4(img, d, t, T, th):
    bars(d, t, SI, SI_COL, 105, "simple")
    bars(d, t, CI, th["accent"], 645, "compound", 0.6)
    if t > 1.9:
        g = pop(prog(t, 1.9, 0.4))
        text_c(d, (540, 1150), "Year 3: +₹12.10 = ₹133.10", font(int(46 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 340), "₹100 at 10%", font(52, "bold"), WHITE)


def s5(img, d, t, T, th):
    # widening gap: two lines diverging
    k = ease(prog(t, 0.2, 1.6))
    x0, y0, N, top = 160, 1000, 20, 100 * 1.1 ** 20
    si, ci = [], []
    for i in range(41):
        n = i / 40 * N * k
        x = x0 + 760 * (n / N)
        si.append((x, y0 - 480 * (100 + 10 * n) / top))
        ci.append((x, y0 - 480 * (100 * 1.1 ** n) / top))
    d.line(si, fill=SI_COL, width=12)
    d.line(ci, fill=th["accent"], width=12)
    text_c(d, (540, 360), "the longer you wait,", font(54, "bold"), WHITE)
    if t > 1.2:
        text_c(d, (540, 440), "the bigger the gap", font(54, "bold"), th["accent"])
    text_c(d, (540, 1080), "time (years)", font(40, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Interest", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "on interest.", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 860), "Time does the work.", font(int(64 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="One hundred rupees at ten percent a year. After three years, is it one hundred thirty?",
         show="₹100 at 10% a year. After 3 years, is it ₹130?", draw=s1),
    dict(say="Simple interest says yes: ten rupees every year.",
         show="Simple interest says yes: ₹10 every year.", draw=s2),
    dict(say="Compound interest adds interest to interest. Year two: ten percent of one hundred ten is eleven.",
         show="Compound interest adds interest to interest. Year 2: 10% of ₹110 is ₹11.", draw=s3),
    dict(say="Year three: twelve rupees ten paise. Total: one hundred thirty three rupees ten paise.",
         show="Year 3: ₹12.10. Total: ₹133.10.", draw=s4),
    dict(say="The longer you wait, the bigger the gap.", draw=s5),
    dict(say="Interest on interest. Time does the work.", draw=s6),
]
