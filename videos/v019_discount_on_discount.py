from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Is 50% + 20% off really 70% off?"
WHITE, DARK = (255, 255, 255), (20, 24, 50)
RED, GREEN, TAG = (240, 90, 90), (90, 210, 130), (255, 235, 200)
SHIRT = (90, 170, 240)


def shirt(d, x, y, s=1.0):
    p = [(x - 70 * s, y - 120 * s), (x - 25 * s, y - 135 * s), (x, y - 110 * s), (x + 25 * s, y - 135 * s),
         (x + 70 * s, y - 120 * s), (x + 140 * s, y - 60 * s), (x + 105 * s, y - 15 * s), (x + 70 * s, y - 45 * s),
         (x + 70 * s, y + 130 * s), (x - 70 * s, y + 130 * s), (x - 70 * s, y - 45 * s), (x - 105 * s, y - 15 * s),
         (x - 140 * s, y - 60 * s)]
    d.polygon(p, fill=SHIRT, outline=WHITE)
    d.line([(x, y - 110 * s), (x, y + 130 * s)], fill=(60, 130, 200), width=int(4 * s))


def price_tag(d, x, y, txt, col=DARK, s=1.0, strike=False):
    d.rounded_rectangle([x - 150 * s, y - 55 * s, x + 150 * s, y + 55 * s], 22 * s, fill=TAG, outline=WHITE, width=4)
    f = font(max(1, int(64 * s)), "bold")
    text_c(d, (x, y), txt, f, col)
    if strike:
        d.line([(x - 120 * s, y + 5 * s), (x + 120 * s, y - 5 * s)], fill=RED, width=int(8 * s))


def badge(d, x, y, txt, col, g=1.0):
    r = 140 * g
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=WHITE, width=5)
    a, b = txt.split(" ")
    text_c(d, (x, y - 28 * g), a, font(int(62 * g) + 1, "bold"), DARK)
    text_c(d, (x, y + 34 * g), b, font(int(46 * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    badge(d, 330, 520, "50% OFF", RED, pop(prog(t, 0.2, 0.4)))
    if t > 1.2:
        badge(d, 750, 520, "+20% OFF", th["accent"], pop(prog(t, 1.2, 0.4)))
    if t > 2.6:
        g = pop(prog(t, 2.6, 0.4))
        text_c(d, (540, 820), "= 70% off?", font(int(110 * g) + 1, "bold"), WHITE, stroke_width=6,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    shirt(d, 540, 640, 1.6)
    g = pop(prog(t, 0.4, 0.4))
    if g > 0:
        price_tag(d, 540, 1000, "₹1000", s=g + 0.01)


def s3(img, d, t, T, th):
    shirt(d, 300, 620, 1.0)
    price_tag(d, 300, 900, "₹1000", s=0.8, strike=t > 0.6)
    k = ease(prog(t, 0.6, 0.6))
    d.line([(470, 760), (470 + 140 * k, 760)], fill=WHITE, width=8)
    if k >= 1:
        d.polygon([(620, 760), (595, 740), (595, 780)], fill=WHITE)
        text_c(d, (540, 400), "50% off", font(64, "bold"), RED)
        price_tag(d, 800, 760, "₹500", col=DARK, s=0.9)


def s4(img, d, t, T, th):
    price_tag(d, 540, 400, "₹500", s=1.0)
    text_c(d, (540, 540), "20% of ₹500", font(72, "bold"), th["accent"])
    # bar of 500 split in 5 parts, one part removed
    x0, x1, y0, y1 = 140, 940, 640, 760
    seg = (x1 - x0) / 5
    k = ease(prog(t, 1.4, 0.6))
    for i in range(5):
        dx = (40 * k) if i == 4 else 0
        dy = (60 * k) if i == 4 else 0
        col = RED if (i == 4 and t > 1.4) else (120, 140, 230)
        d.rounded_rectangle([x0 + i * seg + 6 + dx, y0 + dy, x0 + (i + 1) * seg - 6 + dx, y1 + dy], 14, fill=col)
        text_c(d, (x0 + i * seg + seg / 2 + dx, (y0 + y1) / 2 + dy), "₹100", font(40, "bold"), WHITE)
    if t > 2.2:
        text_c(d, (540, 960), "not 20% of ₹1000", font(56, "semi"), th["soft"])
        text_c(d, (540, 1070), "only ₹100 off", font(64, "bold"), RED)


def s5(img, d, t, T, th):
    shirt(d, 540, 520, 1.0)
    g = pop(prog(t, 0.2, 0.4))
    price_tag(d, 540, 790, "₹400", col=DARK, s=1.1 * g + 0.01)
    if t > 1.3:
        text_c(d, (540, 960), "60% off", font(110, "bold"), GREEN, stroke_width=6, stroke_fill=DARK)
    if t > 2.2:
        text_c(d, (540, 1100), "not 70%", font(70, "bold"), RED)
        d.line([(400, 1105), (680, 1095)], fill=RED, width=8)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 470), "Discount on discount?", font(int(62 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 640), "0.5 × 0.8 = 0.4", font(int(84 * g) + 1, "bold"), th["accent"])
    if t > 0.8:
        text_c(d, (540, 820), "they MULTIPLY", font(78, "bold"), GREEN)
        text_c(d, (540, 940), "they don't add", font(60, "semi"), th["soft"])


SCENES = [
    dict(say="A shop says fifty percent off, plus an extra twenty percent off. Is that seventy percent off?",
         show="A shop says 50% off, plus an extra 20% off. Is that 70% off?", draw=s1),
    dict(say="Let's check with a shirt that costs one thousand rupees.",
         show="Let's check with a shirt that costs ₹1000.", draw=s2),
    dict(say="Fifty percent off brings it to five hundred.", show="50% off brings it to ₹500.", draw=s3),
    dict(say="Now the extra twenty percent is taken from five hundred, not one thousand. That's only one hundred off.",
         show="Now the extra 20% is taken from ₹500, not ₹1000. That's only ₹100 off.", draw=s4),
    dict(say="You pay four hundred. That's sixty percent off, not seventy.",
         show="You pay ₹400. That's 60% off, not 70.", draw=s5),
    dict(say="Discounts on discounts multiply. They don't add up.", draw=s6),
]
