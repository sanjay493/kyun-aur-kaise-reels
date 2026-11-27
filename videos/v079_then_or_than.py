from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Then or than?"
WHITE, DARK = (255, 255, 255), (30, 20, 20)
GREEN, RED, BLUE = (110, 220, 140), (255, 110, 110), (120, 190, 255)
SKIN, HAIR, TOP1, TOP2 = (240, 190, 150), (35, 25, 25), (255, 140, 170), (120, 190, 255)


def kid(d, x, foot, h, col):
    """Simple standing figure; h = total height in px."""
    r = h * 0.13
    hy = foot - h + r
    d.ellipse([x - r, hy - r, x + r, hy + r], fill=SKIN)
    d.pieslice([x - r, hy - r, x + r, hy + r], 180, 360, fill=HAIR)
    d.rounded_rectangle([x - r * 1.1, hy + r * 1.1, x + r * 1.1, foot - h * 0.32], int(r * 0.5), fill=col)
    d.rounded_rectangle([x - r * 0.8, foot - h * 0.34, x - r * 0.15, foot], int(r * 0.2), fill=(60, 60, 90))
    d.rounded_rectangle([x + r * 0.15, foot - h * 0.34, x + r * 0.8, foot], int(r * 0.2), fill=(60, 60, 90))


def chip(d, x, y, s, col, size=56, g=1.0, w=380):
    d.rounded_rectangle([x - w / 2, y - 60, x + w / 2, y + 60], 40, fill=col)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), DARK)


def s1(img, d, t, T, th):
    kid(d, 380, 900, 520, TOP1)
    kid(d, 700, 900, 400, TOP2)
    text_c(d, (380, 960), "Didi", font(46, "semi"), WHITE)
    text_c(d, (700, 960), "me", font(46, "semi"), WHITE)
    text_c(d, (540, 330), "Didi is taller ___ me.", font(58, "bold"), WHITE)
    g = pop(prog(t, 0.5, 0.4))
    chip(d, 300, 1100, "then?", th["accent"], 58, g, 320)
    chip(d, 780, 1100, "than?", th["accent"], 58, g, 320)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 380), "THAN", font(int(120 * g) + 1, "bold"), th["accent"])
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        chip(d, 540, 540, "with an A: for comparing", WHITE, 46, g2, 720)
    rows = ["taller than me", "more than ₹50", "rather than walk"]
    for i, r in enumerate(rows):
        if t > 1.0 + 0.4 * i:
            y = 700 + i * 150
            d.rounded_rectangle([140, y - 60, 940, y + 60], 40, fill=(255, 255, 255, 30))
            text_c(d, (540, y), r, font(50, "bold"), WHITE)


def s3(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 380), "THEN", font(int(120 * g) + 1, "bold"), BLUE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        chip(d, 540, 540, "with an E: for time", WHITE, 46, g2, 640)
    if t > 1.0:
        # timeline: brush -> then -> sleep
        k = ease(prog(t, 1.0, 0.8))
        d.line([(180, 780), (180 + 720 * k, 780)], fill=BLUE, width=10)
        d.ellipse([150, 750, 210, 810], fill=BLUE)
        text_c(d, (180, 870), "brush", font(46, "bold"), WHITE)
        if k > 0.95:
            d.ellipse([870, 750, 930, 810], fill=BLUE)
            text_c(d, (900, 870), "sleep", font(46, "bold"), WHITE)
            text_c(d, (540, 730), "then", font(50, "semi"), BLUE)
    if t > 1.9:
        text_c(d, (540, 1040), "First brush, then sleep.", font(52, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "Also: if ... then", font(62, "bold"), BLUE)
    g = pop(prog(t, 0.3, 0.4))
    d.rounded_rectangle([90, 470, 990, 640], 40, fill=(255, 255, 255, 30))
    text_c(d, (540, 555), "If it rains, then", font(int(60 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([90, 680, 990, 850], 40, fill=(255, 255, 255, 30))
        text_c(d, (540, 765), "take an umbrella.", font(int(60 * g2) + 1, "bold"), WHITE)
    if t > 1.4:
        # umbrella
        cx, cy = 540, 1060
        d.pieslice([cx - 150, cy - 110, cx + 150, cy + 110], 180, 360, fill=BLUE)
        d.line([(cx, cy), (cx, cy + 110)], fill=WHITE, width=10)
        d.arc([cx - 40, cy + 80, cx, cy + 130], 0, 180, fill=WHITE, width=10)


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "Spelling tip", font(60, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([110, 430, 970, 640], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=5)
    text_c(d, (540, 495), "compAre & thAn", font(int(66 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 585), "both have an A", font(44, "semi"), WHITE)
    if t > 1.2:
        g2 = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([110, 720, 970, 930], 50, fill=(255, 255, 255, 30), outline=BLUE, width=5)
        text_c(d, (540, 785), "whEn & thEn", font(int(66 * g2) + 1, "bold"), BLUE)
        text_c(d, (540, 875), "both end in -en", font(44, "semi"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 470), "Comparing?", font(int(62 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 580), "Than.", font(int(90 * g) + 1, "bold"), th["accent"])
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 780), "Time?", font(int(62 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 890), "Then.", font(int(90 * g2) + 1, "bold"), BLUE)


SCENES = [
    dict(say="Didi is taller then me, or taller than me? One letter makes the difference.",
         show="\"Didi is taller then me\" or \"taller than me\"? One letter makes the difference.", draw=s1),
    dict(say="Than, with an A, is for comparing. Taller than me. More than fifty rupees. Rather than.",
         show="Than, with an A, is for comparing. Taller than me. More than ₹50. Rather than.", draw=s2),
    dict(say="Then, with an E, is about time. First brush, then sleep.", draw=s3),
    dict(say="Also: if it rains, then take an umbrella.", draw=s4),
    dict(say="Tip: compare and than both have an A. When and then both end in E N.",
         show="Tip: compare and than both have an A. When and then both end in -en.", draw=s5),
    dict(say="Comparing? Than. Time? Then.", draw=s6),
]
