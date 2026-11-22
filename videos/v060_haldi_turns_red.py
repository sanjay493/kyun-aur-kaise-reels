from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a haldi stain turn red with soap?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
HALDI, RED = (245, 190, 30), (200, 40, 50)
SHIRT, SHIRT2 = (245, 248, 252), (200, 205, 215)
SOAP, BUBBLE, LEMON, WATER = (150, 210, 255), (225, 240, 255), (240, 230, 80), (120, 190, 255)
GREEN = (110, 220, 140)


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def shirt(d, x, y, s=1.0):
    w, h = 230 * s, 300 * s
    d.polygon([(x - w, y - h + 60 * s), (x - w * 0.45, y - h), (x + w * 0.45, y - h), (x + w, y - h + 60 * s),
               (x + w * 0.8, y - h + 170 * s), (x + w * 0.55, y - h + 140 * s), (x + w * 0.55, y + h * 0.8),
               (x - w * 0.55, y + h * 0.8), (x - w * 0.55, y - h + 140 * s), (x - w * 0.8, y - h + 170 * s)],
              fill=SHIRT, outline=SHIRT2)
    d.arc([x - 60 * s, y - h - 40 * s, x + 60 * s, y - h + 50 * s], 0, 180, fill=SHIRT2, width=int(8 * s) + 1)


def stain(d, x, y, col, r=55):
    for dx, dy, rr in [(0, 0, r), (-r * 0.7, r * 0.3, r * 0.55), (r * 0.6, -r * 0.4, r * 0.5), (r * 0.3, r * 0.6, r * 0.4)]:
        d.ellipse([x + dx - rr, y + dy - rr, x + dx + rr, y + dy + rr], fill=col)


def bubbles(d, x, y, t, n=7, spread=200):
    for i in range(n):
        bx = x - spread / 2 + (i * 53) % spread
        by = y - ((t * 120 + i * 40) % 160)
        r = 14 + (i * 7) % 16
        d.ellipse([bx - r, by - r, bx + r, by + r], outline=BUBBLE, width=4)


def strip(d, x, y, col, label):
    d.rounded_rectangle([x - 70, y - 200, x + 70, y + 200], 16, fill=col, outline=WHITE, width=4)
    text_c(d, (x, y + 260), label, font(42, "bold"), WHITE)


def s1(img, d, t, T, th):
    shirt(d, 540, 760)
    k = ease(prog(t, 1.4, 0.9))
    stain(d, 560, 720, mix(HALDI, RED, k))
    if t > 0.9:
        bubbles(d, 560, 640, t)
    if t > 2.2:
        g = pop(prog(t, 2.2, 0.4))
        text_c(d, (540, 1130), "Why red?", font(int(76 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 350), "Haldi stain + soap", font(60, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Turmeric is an", font(58, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([210, 420, 870, 560], 50, fill=th["accent"])
    text_c(d, (540, 490), "INDICATOR", font(int(70 * g) + 1, "bold"), DARK)
    if t > 0.9:
        strip(d, 540, 800, HALDI, "")
        text_c(d, (540, 1080), "changes colour to tell you", font(44, "semi"), th["soft"])
        text_c(d, (540, 1140), "what a substance is like", font(44, "semi"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Soap is a BASE", font(64, "bold"), th["accent"])
    k = ease(prog(t, 0.6, 0.8))
    strip(d, 540, 720, mix(HALDI, RED, k), "")
    bubbles(d, 540, 560, t, 6, 180)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([170, 980, 910, 1110], 50, fill=RED)
        text_c(d, (540, 1045), "bases turn it RED", font(int(58 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "Lemon juice? Water?", font(60, "bold"), WHITE)
    for i, (x, lab, col) in enumerate([(330, "lemon", LEMON), (750, "water", WATER)]):
        if t > 0.2 + 0.4 * i:
            g = pop(prog(t, 0.2 + 0.4 * i, 0.4))
            d.ellipse([x - 50 * g, 440, x + 50 * g, 540], fill=col)
            strip(d, x, 760, HALDI, lab)
    if t > 1.3:
        text_c(d, (540, 1130), "both stay yellow", font(56, "bold"), HALDI)


def s5(img, d, t, T, th):
    rows = [("base (soap)", RED, "red"), ("acid (lemon)", HALDI, "yellow"), ("neutral (water)", HALDI, "yellow")]
    for i, (lab, col, word) in enumerate(rows):
        if t > 0.2 + 0.35 * i:
            g = pop(prog(t, 0.2 + 0.35 * i, 0.4))
            y = 460 + i * 170
            d.rounded_rectangle([110, y - 70, 970, y + 70], 40, fill=(255, 255, 255, 30))
            text_c(d, (160, y), lab, font(int(46 * g) + 1, "bold"), WHITE, anchor="lm")
            d.rounded_rectangle([760, y - 45, 920, y + 45], 20, fill=col)
    if t > 1.5:
        text_c(d, (540, 1000), "spots a base, but can't tell", font(46, "bold"), th["accent"])
        text_c(d, (540, 1070), "an acid from water", font(46, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Haldi turned red?", font(int(70 * g) + 1, "bold"), WHITE)
    stain(d, 540, 680, RED, 50)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        d.rounded_rectangle([200, 830, 880, 970], 50, fill=th["accent"])
        text_c(d, (540, 900), "A base is there.", font(int(64 * g2) + 1, "bold"), DARK)


SCENES = [
    dict(say="A haldi stain on your white shirt. Wash it with soap, and it turns red! Why?", draw=s1),
    dict(say="Turmeric is a natural indicator. Its colour shows what kind of substance it touched.", draw=s2),
    dict(say="Soap is a base. And bases turn turmeric red.", draw=s3),
    dict(say="Lemon juice is an acid, but turmeric stays yellow, just like in water.", draw=s4),
    dict(say="So turmeric spots bases, but can't tell an acid from water.", draw=s5),
    dict(say="Haldi turned red? A base is there.", draw=s6),
]
