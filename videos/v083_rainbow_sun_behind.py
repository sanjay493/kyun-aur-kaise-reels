import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why is a rainbow always opposite the Sun?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
SUN, SKIN = (255, 210, 70), (240, 190, 150)
DROP = (150, 210, 255)
VIBGYOR = [(148, 0, 211), (75, 0, 130), (40, 90, 255), (40, 200, 80), (255, 235, 0), (255, 140, 0), (255, 40, 40)]


def sun(d, x, y, r=60, k=1.0):
    for i in range(12):
        a = i * math.pi / 6
        d.line([(x + math.cos(a) * (r + 10), y + math.sin(a) * (r + 10)),
                (x + math.cos(a) * (r + 10 + 30 * k), y + math.sin(a) * (r + 10 + 30 * k))], fill=SUN, width=7)
    d.ellipse([x - r, y - r, x + r, y + r], fill=SUN)


def person(d, x, y, s=1.0):
    """Small figure seen from behind, standing with feet at y."""
    d.ellipse([x - 28 * s, y - 230 * s, x + 28 * s, y - 174 * s], fill=(35, 25, 25))
    d.rounded_rectangle([x - 40 * s, y - 170 * s, x + 40 * s, y - 70 * s], 18 * s, fill=(90, 160, 240))
    d.rectangle([x - 32 * s, y - 72 * s, x - 6 * s, y], fill=(50, 50, 80))
    d.rectangle([x + 6 * s, y - 72 * s, x + 32 * s, y], fill=(50, 50, 80))


def rainbow(d, cx, cy, r, k=1.0, band=22, alpha=230):
    """Arc with red outside, violet inside. k = fraction drawn (left to right)."""
    end = 180 + 180 * k
    for i, col in enumerate(VIBGYOR):  # violet innermost
        rr = r + i * band
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, end, fill=col + (alpha,), width=band + 1)


def raindrops(d, t, x0, x1, y0, y1, n=40, seed=3):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.uniform(x0, x1)
        y = y0 + ((rnd.uniform(0, 1) * (y1 - y0) + t * 260) % (y1 - y0))
        d.line([(x, y), (x - 6, y + 26)], fill=DROP + (200,), width=5)


def s1(img, d, t, T, th):
    # sun behind the person (right), rainbow in front (left)
    sun(d, 920, 420, 55)
    d.rectangle([60, 1060, W - 60, 1072], fill=(255, 255, 255, 60))
    person(d, 700, 1060, 1.1)
    k = ease(prog(t, 0.4, 1.2))
    rainbow(d, 330, 1060, 150, k)
    text_c(d, (540, 330), "Sun behind you", font(60, "bold"), SUN)
    if t > 1.4:
        text_c(d, (330, 1120), "rainbow in front", font(42, "semi"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 330), "After rain", font(60, "bold"), WHITE)
    raindrops(d, t, 120, 960, 420, 1080, n=55)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.5))
        r = 70 * g
        d.ellipse([540 - r, 760 - r * 1.15, 540 + r, 760 + r], fill=DROP + (230,))
        text_c(d, (540, 1140), "tiny drops in the air", font(48, "semi"), th["accent"])


def droplet(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 210, 255, 90), outline=DROP, width=6)


def s3(img, d, t, T, th):
    text_c(d, (540, 330), "Each drop = a tiny prism", font(58, "bold"), th["accent"])
    # prism on left, drop on right
    d.polygon([(270, 560), (130, 860), (410, 860)], fill=(255, 255, 255, 60), outline=WHITE)
    k = ease(prog(t, 0.3, 0.8))
    d.line([(40, 760), (40 + 150 * k, 740)], fill=WHITE, width=7)
    if k >= 1:
        k2 = ease(prog(t, 1.1, 0.6))
        for i, col in enumerate(VIBGYOR[::-1]):
            d.line([(330, 730), (330 + 150 * k2, 760 + i * 18 + 40 * k2)], fill=col, width=6)
    droplet(d, 790, 720, 150)
    text_c(d, (270, 950), "glass prism", font(40, "semi"), WHITE)
    text_c(d, (790, 950), "water drop", font(40, "semi"), WHITE)
    text_c(d, (540, 1110), "splits white light into colours", font(44, "semi"), WHITE)


def s4(img, d, t, T, th):
    cx, cy, r = 600, 740, 260
    droplet(d, cx, cy, r)
    # sunlight enters from right (sun side)
    p_in = (cx + 150, cy - 212)
    p_back = (cx - 240, cy - 20)
    k1 = ease(prog(t, 0.1, 0.6))
    d.line([(1060, p_in[1]), (1060 + (p_in[0] - 1060) * k1, p_in[1])], fill=WHITE, width=8)
    text_c(d, (540, 330), "bends going in", font(58, "bold"), th["accent"])
    if k1 >= 1:
        k2 = ease(prog(t, 0.7, 0.6))
        for i, col in enumerate(VIBGYOR):
            tgt = (p_back[0], p_back[1] + (i - 3) * 14)
            d.line([p_in, (p_in[0] + (tgt[0] - p_in[0]) * k2, p_in[1] + (tgt[1] - p_in[1]) * k2)], fill=col, width=5)
        if k2 >= 1:
            text_c(d, (540, 410), "reflects off the back", font(48, "semi"), WHITE)
            k3 = ease(prog(t, 1.3, 0.6))
            for i, col in enumerate(VIBGYOR):
                a = (p_back[0], p_back[1] + (i - 3) * 14)
                b = (cx + 120 + i * 12, cy + 222 - i * 6)
                d.line([a, (a[0] + (b[0] - a[0]) * k3, a[1] + (b[1] - a[1]) * k3)], fill=col, width=5)
                if k3 >= 1:
                    k4 = ease(prog(t, 1.9, 0.5))
                    c = (b[0] + (110 + i * 10) * k4, b[1] + (70 - i * 5) * k4)
                    d.line([b, c], fill=col, width=5)
            if t > 2.0:
                text_c(d, (540, 1150), "and bends again coming out", font(44, "semi"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 330), "Colours come back", font(58, "bold"), WHITE)
    text_c(d, (540, 405), "towards the Sun's side", font(58, "bold"), SUN)
    sun(d, 960, 560, 45)
    person(d, 760, 1060, 1.0)
    d.rectangle([60, 1060, W - 60, 1072], fill=(255, 255, 255, 60))
    raindrops(d, t, 80, 520, 520, 1040, n=30)
    k = ease(prog(t, 0.3, 0.8))
    for i, col in enumerate(VIBGYOR):
        a = (420 - i * 8, 760 + i * 10)
        d.line([a, (a[0] + (740 - a[0]) * k, a[1] + (880 - a[1]) * k)], fill=col, width=5)
    if t > 1.2:
        text_c(d, (300, 1130), "so they reach you", font(42, "semi"), th["accent"])


def s6(img, d, t, T, th):
    rainbow(d, 540, 980, 250, 1.0, band=24)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 360), "Sun behind you,", font(int(66 * g) + 1, "bold"), SUN)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 450), "rain in front", font(int(66 * g2) + 1, "bold"), DROP)
    if t > 1.0:
        g3 = pop(prog(t, 1.0, 0.45))
        text_c(d, (540, 1060), "= rainbow", font(int(84 * g3) + 1, "bold"), th["accent"])
    text_c(d, (540, 1150), "red outside, violet inside", font(40, "semi"), WHITE)


SCENES = [
    dict(say="Want to see a rainbow? Turn your back to the Sun.", draw=s1),
    dict(say="After rain, tiny water droplets float in the air.", draw=s2),
    dict(say="Each droplet acts like a small prism, splitting sunlight into colours.", draw=s3),
    dict(say="Light bends going in, reflects off the back, and bends again coming out.", draw=s4),
    dict(say="So the colours head back towards the Sun's side, where you stand.", draw=s5),
    dict(say="A rainbow is always opposite the Sun. Sun behind, rain in front.", draw=s6),
]
