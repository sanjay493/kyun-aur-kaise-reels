from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Is ₹100 in your gullak still ₹100?"
WHITE, DARK = (255, 255, 255), (20, 30, 35)
NOTE, NOTE2, POT, POT2 = (190, 150, 210), (150, 110, 175), (200, 110, 60), (160, 80, 40)
RED, GREEN = (255, 105, 105), (110, 220, 140)


def note(d, x, y, s=1.0, a=255):
    d.rounded_rectangle([x - 150 * s, y - 70 * s, x + 150 * s, y + 70 * s], 14 * s, fill=NOTE + (a,),
                        outline=(255, 255, 255, a), width=4)
    d.ellipse([x + 40 * s, y - 45 * s, x + 130 * s, y + 45 * s], outline=NOTE2 + (a,), width=int(5 * s) + 1)
    text_c(d, (x - 50 * s, y), "₹100", font(max(1, int(60 * s)), "bold"), (60, 30, 80, a))


def gullak(d, x, y, s=1.0):
    d.ellipse([x - 170 * s, y - 150 * s, x + 170 * s, y + 160 * s], fill=POT)
    d.ellipse([x - 70 * s, y - 185 * s, x + 70 * s, y - 135 * s], fill=POT2)
    d.rounded_rectangle([x - 60 * s, y - 70 * s, x + 60 * s, y - 52 * s], 8, fill=(70, 35, 20))
    d.arc([x - 120 * s, y - 60 * s, x + 120 * s, y + 140 * s], 20, 160, fill=POT2, width=int(6 * s))


def basket(d, x, y, n, s=1.0):
    d.polygon([(x - 160 * s, y - 40 * s), (x + 160 * s, y - 40 * s), (x + 120 * s, y + 110 * s),
               (x - 120 * s, y + 110 * s)], fill=(215, 170, 100), outline=WHITE)
    cols = [(255, 120, 90), (255, 210, 80), (130, 210, 110), (240, 240, 230), (255, 160, 60)]
    for i in range(n):
        cx = x - 110 * s + (i % 5) * 55 * s
        cy = y - 60 * s - (i // 5) * 45 * s
        d.ellipse([cx - 28 * s, cy - 28 * s, cx + 28 * s, cy + 28 * s], fill=cols[i % 5])


def s1(img, d, t, T, th):
    gullak(d, 540, 760)
    k = ease(prog(t, 0.2, 0.9))
    note(d, 540, 420 + 180 * k, 0.8, int(255 * (1 - 0.8 * clamp((t - 1.0) / 0.3))))
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 1050), "10 years later...", font(int(60 * g) + 1, "bold"), th["accent"])
        text_c(d, (540, 1140), "still worth ₹100?", font(int(56 * g) + 1, "bold"), WHITE)


def s2(img, d, t, T, th):
    note(d, 540, 460, 1.0)
    text_c(d, (540, 600), "still says ₹100", font(46, "semi"), th["soft"])
    # price tag climbing
    for i, (yr, p) in enumerate([("Year 1", "₹100"), ("Year 2", "₹106"), ("Year 3", "₹112")]):
        if t > 0.8 + 0.5 * i:
            g = pop(prog(t, 0.8 + 0.5 * i, 0.35))
            x = 240 + i * 300; y = 900 - i * 70
            d.rounded_rectangle([x - 120, y - 60, x + 120, y + 60], 20, fill=(255, 240, 210))
            text_c(d, (x, y - 18), yr, font(int(30 * g) + 1, "semi"), (90, 70, 50))
            text_c(d, (x, y + 22), p, font(int(46 * g) + 1, "bold"), DARK)
    if t > 2.2:
        text_c(d, (540, 1120), "same basket, rising price", font(40, "semi"), th["soft"])


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    k = ease(prog(t, 0.2, 1.4))
    # an arrow that climbs
    d.line([(200, 960), (200 + 680 * k, 960 - 420 * k)], fill=RED, width=16)
    if k > 0.95:
        d.polygon([(880, 540), (830, 545), (865, 585)], fill=RED)
    d.rounded_rectangle([250, 340, 830, 470], 50, fill=th["accent"])
    text_c(d, (540, 405), "INFLATION", font(int(72 * g) + 1, "bold"), DARK)
    text_c(d, (540, 1060), "prices rising over time", font(50, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (290, 380), "Earlier", font(48, "bold"), th["soft"])
    text_c(d, (790, 380), "Later", font(48, "bold"), th["soft"])
    note(d, 290, 500, 0.7); note(d, 790, 500, 0.7)
    basket(d, 290, 770, 10, 0.9)
    k = ease(prog(t, 0.6, 1.0))
    basket(d, 790, 770, 10 - int(4 * k), 0.9)
    d.line([(540, 400), (540, 900)], fill=(255, 255, 255, 60), width=4)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        d.rounded_rectangle([170, 980, 910, 1100], 40, fill=th["accent"])
        text_c(d, (540, 1040), "less purchasing power", font(int(54 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    text_c(d, (540, 360), "if prices rise 6% a year", font(50, "bold"), WHITE)
    vals = [(0, 100), (3, 119), (6, 142), (9, 169), (12, 201)]
    base_y, top = 1000, 470
    for i, (yr, v) in enumerate(vals):
        k = ease(prog(t, 0.4 + 0.3 * i, 0.4))
        x = 200 + i * 170
        h = (v / 201) * (base_y - top) * k
        col = th["accent"] if i == 4 else (255, 255, 255, 140)
        d.rounded_rectangle([x - 55, base_y - h, x + 55, base_y], 14, fill=col)
        if k > 0.5:
            text_c(d, (x, base_y - h - 34), f"₹{v}", font(36, "bold"), WHITE)
        text_c(d, (x, base_y + 40), f"yr {yr}", font(32, "semi"), th["soft"])
    if t > 2.2:
        text_c(d, (540, 1140), "about double in 12 years", font(52, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    note(d, 540, 540, 0.9)
    g = pop(prog(t, 0.3, 0.45))
    text_c(d, (540, 790), "Money kept still", font(int(64 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 880), "doesn't grow.", font(int(64 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        text_c(d, (540, 1000), "Prices do.", font(int(80 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Keep a hundred rupee note in your gullak for ten years. Is it still worth a hundred?",
         show="Keep a ₹100 note in your gullak for 10 years. Is it still worth ₹100?", draw=s1),
    dict(say="The note still says one hundred. But prices usually rise every year.",
         show="The note still says ₹100. But prices usually rise every year.", draw=s2),
    dict(say="That rise in prices over time is called inflation.", draw=s3),
    dict(say="So the same note buys less. That's called losing purchasing power.", draw=s4),
    dict(say="If prices rise six percent a year, they about double in twelve years.",
         show="If prices rise 6% a year, they about double in 12 years.", draw=s5),
    dict(say="Money kept still doesn't grow. Prices do.", draw=s6),
]
