from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Why ₹199 feels so much cheaper than ₹200"
WHITE, DARK, GREY = (255, 255, 255), (20, 30, 40), (150, 160, 170)
TAG, RED, GREEN = (255, 245, 220), (255, 110, 110), (120, 230, 140)


def tag(d, cx, cy, txt, s=1.0, fill=TAG, ink=DARK):
    w, h = 300 * s, 150 * s
    d.polygon([(cx - w / 2, cy - h / 2), (cx + w / 2 - 40 * s, cy - h / 2), (cx + w / 2, cy),
               (cx + w / 2 - 40 * s, cy + h / 2), (cx - w / 2, cy + h / 2)], fill=fill)
    d.ellipse([cx + w / 2 - 62 * s, cy - 12 * s, cx + w / 2 - 38 * s, cy + 12 * s], fill=(60, 60, 70))
    text_c(d, (cx - 20 * s, cy), txt, font(max(1, int(70 * s)), "bold"), ink)


def s1(img, d, t, T, th):
    g1 = pop(prog(t, 0.1, 0.5))
    tag(d, 290, 620, "₹199", max(0.01, g1))
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.5))
        tag(d, 790, 620, "₹200", max(0.01, g2))
    if t > 1.2:
        text_c(d, (290, 780), "feels cheap", font(46, "semi"), GREEN)
        text_c(d, (790, 780), "feels costly", font(46, "semi"), RED)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.5))
        text_c(d, (540, 1000), "Difference: ₹1", font(int(70 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 340), "Which feels cheaper?", font(62, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "We read left to right", font(62, "bold"), WHITE)
    k = ease(prog(t, 0.2, 0.9))
    d.line([(200, 470), (200 + 680 * k, 470)], fill=th["accent"], width=8)
    if k >= 1:
        d.polygon([(880, 450), (920, 470), (880, 490)], fill=th["accent"])
    f = font(150, "bold")
    for i, (num, y) in enumerate((("199", 680), ("200", 900))):
        first, rest = num[0], num[1:]
        x0 = 540 - d.textlength("₹" + num, font=f) / 2
        d.text((x0, y), "₹", font=f, fill=GREY, anchor="lm")
        x1 = x0 + d.textlength("₹", font=f)
        hl = t > 1.0
        d.text((x1, y), first, font=f, fill=th["accent"] if hl else WHITE, anchor="lm")
        x2 = x1 + d.textlength(first, font=f)
        d.text((x2, y), rest, font=f, fill=(255, 255, 255, 90) if hl else WHITE, anchor="lm")
    if t > 1.4:
        text_c(d, (540, 1110), "1 vs 2 lands first", font(52, "bold"), th["accent"])


def s3(img, d, t, T, th):
    d.rounded_rectangle([110, 400, 970, 1000], 40, fill=(255, 255, 255, 30), outline=WHITE, width=4)
    text_c(d, (540, 490), "2005 study", font(48, "semi"), th["soft"])
    text_c(d, (540, 560), "Thomas & Morwitz", font(42, "reg"), th["soft"])
    g = pop(prog(t, 0.3, 0.5))
    text_c(d, (540, 730), "The left-digit", font(int(76 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 840), "effect", font(int(90 * g) + 1, "bold"), th["accent"])


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Only when the first", font(60, "bold"), WHITE)
    text_c(d, (540, 415), "digit changes", font(60, "bold"), th["accent"])
    rows = [("$2.99 vs $3.00", "✓", GREEN, 0.3), ("$3.59 vs $3.60", "✗", RED, 1.0)]
    for i, (txt, mark, col, st) in enumerate(rows):
        if t > st:
            g = pop(prog(t, st, 0.4))
            y = 620 + i * 200
            d.rounded_rectangle([120, y - 75, 960, y + 75], 30, fill=(255, 255, 255, 35))
            text_c(d, (480, y), txt, font(int(66 * g) + 1, "bold"), WHITE)
            text_c(d, (870, y), mark, font(int(90 * g) + 1, "sym"), col)
    if t > 1.5:
        text_c(d, (540, 1120), "(the study used US prices)", font(36, "reg"), th["soft"])


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "Round up in your head", font(62, "bold"), th["accent"])
    for i, (a, b) in enumerate((("₹499", "₹500"), ("₹999", "₹1000"))):
        y = 600 + i * 260
        tag(d, 300, y, a, 0.9)
        k = ease(prog(t, 0.4 + i * 0.5, 0.5))
        if k > 0:
            d.line([(480, y), (480 + 120 * k, y)], fill=WHITE, width=8)
            if k >= 1:
                d.polygon([(600, y - 20), (630, y), (600, y + 20)], fill=WHITE)
                text_c(d, (820, y), b, font(76, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "₹199 is ₹200", font(int(90 * g) + 1, "bold"), th["accent"])
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 720), "Read the whole price,", font(int(58 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 810), "not just the first digit", font(int(58 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Why does one hundred ninety-nine rupees feel so much cheaper than two hundred? It's just one rupee less.",
         show="Why does ₹199 feel so much cheaper than ₹200? It's just one rupee less.", draw=s1),
    dict(say="We read left to right, so the first digit hits first: one versus two.", draw=s2),
    dict(say="A two thousand and five study named this the left-digit effect.",
         show="A 2005 study named this the left-digit effect.", draw=s3),
    dict(say="It only worked when the first digit changed.", draw=s4),
    dict(say="So when you see four ninety-nine or nine ninety-nine, round up in your head.",
         show="So when you see ₹499 or ₹999, round up in your head.", draw=s5),
    dict(say="One ninety-nine is really two hundred. Read the whole price, not just the first digit.",
         show="₹199 is really ₹200. Read the whole price, not just the first digit.", draw=s6),
]
