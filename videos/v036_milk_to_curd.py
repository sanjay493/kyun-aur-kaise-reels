import math, random
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "How does one spoon turn milk into curd?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
MILK, CURD, BOWL, BOWL2 = (250, 248, 238), (245, 240, 215), (200, 120, 70), (160, 90, 50)
BUG, ACID = (120, 230, 140), (255, 225, 90)

BX, BY = 540, 760  # bowl centre (rim line)


def bowl(d, fill=MILK, lumpy=0.0):
    # bowl body (half ellipse) with milk surface on top
    d.chord([BX - 300, BY - 230, BX + 300, BY + 230], 0, 180, fill=BOWL)
    d.ellipse([BX - 300, BY - 60, BX + 300, BY + 60], fill=BOWL2)
    d.ellipse([BX - 275, BY - 48, BX + 275, BY + 48], fill=fill)
    if lumpy > 0:
        rnd = random.Random(3)
        for _ in range(16):
            x = BX + rnd.uniform(-220, 220); y = BY + rnd.uniform(-28, 28)
            r = 14 + 10 * lumpy
            d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(232, 226, 196))


def spoon(d, x, y, a=255):
    d.line([(x, y), (x + 170, y - 170)], fill=(200, 205, 215, a), width=16)
    d.ellipse([x - 55, y - 35, x + 55, y + 35], fill=(200, 205, 215, a))
    d.ellipse([x - 42, y - 24, x + 42, y + 24], fill=CURD + (a,))


def bug(d, x, y, r=16, wob=0.0):
    d.rounded_rectangle([x - r * 1.6, y - r * 0.7 + wob, x + r * 1.6, y + r * 0.7 + wob], int(r * 0.7), fill=BUG,
                        outline=DARK, width=3)


def bug_field(d, t, n, cx, cy, rx, ry, seed=5):
    rnd = random.Random(seed)
    for i in range(n):
        x = cx + rnd.uniform(-rx, rx); y = cy + rnd.uniform(-ry, ry)
        bug(d, x, y, 14, 4 * math.sin(t * 6 + i))


def s1(img, d, t, T, th):
    bowl(d)
    k = ease(prog(t, 0.2, 0.9))
    spoon(d, 760 - 160 * k, 470 + 230 * k)
    text_c(d, (540, 380), "1 spoon", font(56, "bold"), th["accent"])
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1110), "milk to curd?", font(int(76 * g) + 1, "bold"), WHITE, stroke_width=4,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    # magnifier on the spoon showing bacteria, then they multiply
    g = pop(prog(t, 0.1, 0.45))
    r = 260 * g + 1
    d.ellipse([540 - r, 640 - r, 540 + r, 640 + r], fill=CURD, outline=WHITE, width=10)
    d.line([(540 + r * 0.7, 640 + r * 0.7), (540 + r * 1.05, 640 + r * 1.05)], fill=WHITE, width=24)
    n = 3 + int(ease(prog(t, 1.4, 1.6)) * 13)
    if g > 0.9:
        bug_field(d, t, n, 540, 640, 170, 150)
    text_c(d, (540, 330), "Lactobacillus", font(60, "bold"), th["accent"])
    if t > 1.4:
        text_c(d, (540, 1060), "they multiply", font(56, "bold"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "lactose  (milk sugar)", font(50, "bold"), WHITE)
    # lactose blocks travel into a bacterium and come out as acid drops
    bug(d, 540, 640, 60, 6 * math.sin(t * 5))
    for i in range(4):
        p = (t * 0.6 + i * 0.25) % 1.0
        if p < 0.5:
            x, y = 180 + (540 - 180) * (p / 0.5), 640
            d.rounded_rectangle([x - 26, y - 26, x + 26, y + 26], 8, fill=WHITE)
        else:
            x, y = 540 + (900 - 540) * ((p - 0.5) / 0.5), 640
            d.ellipse([x - 22, y - 30, x + 22, y + 22], fill=ACID)
    text_c(d, (180, 760), "sugar", font(42, "semi"), th["soft"])
    text_c(d, (900, 760), "acid", font(42, "semi"), th["soft"])
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([250, 930, 830, 1060], 40, fill=th["accent"])
        text_c(d, (540, 995), "LACTIC ACID", font(int(60 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    # loose protein dots drift together into clumps
    k = ease(prog(t, 0.3, 1.8))
    rnd = random.Random(11)
    centres = [(330, 520), (750, 560), (420, 860), (760, 880)]
    for i in range(36):
        x0, y0 = rnd.uniform(160, 920), rnd.uniform(380, 1000)
        cx, cy = centres[i % 4]
        ox, oy = rnd.uniform(-45, 45), rnd.uniform(-45, 45)
        x = x0 + (cx + ox - x0) * k; y = y0 + (cy + oy - y0) * k
        d.ellipse([x - 20, y - 20, x + 20, y + 20], fill=MILK, outline=(200, 190, 160), width=3)
    text_c(d, (540, 330), "milk proteins", font(54, "bold"), th["accent"])
    if t > 1.8:
        text_c(d, (540, 1110), "runny to thick", font(64, "bold"), WHITE, stroke_width=4, stroke_fill=DARK)


def s5(img, d, t, T, th):
    # three thermometers: cold, warm (tick), very hot
    labels = [("cold", (120, 190, 255), 0.2, False), ("warm", (255, 190, 80), 0.5, True), ("very hot", (255, 90, 90), 0.92, False)]
    for i, (lab, col, lvl, ok) in enumerate(labels):
        x = 240 + i * 300
        d.rounded_rectangle([x - 30, 420, x + 30, 880], 30, fill=(255, 255, 255, 60), outline=WHITE, width=4)
        d.ellipse([x - 55, 850, x + 55, 960], fill=col, outline=WHITE, width=4)
        h = 430 * lvl * ease(prog(t, 0.2 + 0.2 * i, 0.6))
        d.rounded_rectangle([x - 16, 880 - h, x + 16, 885], 16, fill=col)
        text_c(d, (x, 1010), lab, font(44, "bold"), WHITE)
        if t > 1.4:
            g = pop(prog(t, 1.4 + 0.15 * i, 0.4))
            mark = "✓" if ok else "✗"
            text_c(d, (x, 350), mark, font(int(80 * g) + 1, "sym"), (90, 220, 120) if ok else (255, 110, 110))


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    bowl_y = 600
    d.chord([300, bowl_y - 150, 780, bowl_y + 150], 0, 180, fill=BOWL)
    d.ellipse([300, bowl_y - 40, 780, bowl_y + 40], fill=BOWL2)
    d.ellipse([318, bowl_y - 30, 762, bowl_y + 30], fill=CURD)
    text_c(d, (540, 880), "Dahi = milk", font(int(66 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 980), "changed by bacteria", font(int(60 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="How does one spoon of curd turn a whole bowl of milk into curd?", draw=s1),
    dict(say="That spoon carries bacteria called Lactobacillus. In warm milk, they multiply.", draw=s2),
    dict(say="They feed on lactose, the sugar in milk, and turn it into lactic acid.", draw=s3),
    dict(say="The acid makes milk proteins clump together. Runny milk sets thick.", draw=s4),
    dict(say="Too cold or too hot, it won't set well. So we use warm milk.", draw=s5),
    dict(say="Dahi is milk, changed by bacteria.", draw=s6),
]
