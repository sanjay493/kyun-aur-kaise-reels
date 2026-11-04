import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why do stars twinkle?"
WHITE, DARK = (255, 255, 255), (15, 25, 40)
STAR, AIR1, AIR2 = (255, 245, 200), (120, 200, 255), (160, 230, 200)
RED = (240, 90, 90)


def star(d, x, y, r, a=255):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    d.polygon(pts, fill=STAR + (a,))


def eye(d, x, y, s=1.0):
    d.ellipse([x - 90 * s, y - 45 * s, x + 90 * s, y + 45 * s], fill=WHITE, outline=DARK, width=4)
    d.ellipse([x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s], fill=(70, 50, 30))
    d.ellipse([x - 13 * s, y - 13 * s, x + 13 * s, y + 13 * s], fill=DARK)


def air_layers(d, t, y0, y1, n=5):
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 0.5) / n
        pts = [(x, y + math.sin(x / 90 + t * 2.2 + i * 1.3) * 18) for x in range(80, 1001, 20)]
        d.line(pts, fill=(AIR1 if i % 2 else AIR2) + (150,), width=10)


def twinkle(t, i):
    return 0.55 + 0.45 * math.sin(t * 9 + i * 2.1) * math.sin(t * 5.3 + i)


def s1(img, d, t, T, th):
    for i, (x, y) in enumerate([(220, 380), (560, 330), (860, 450), (380, 620), (720, 700), (180, 860),
                                (900, 880), (540, 1000)]):
        k = twinkle(t, i)
        star(d, x, y, 30 + 18 * k, int(140 + 115 * k))
    if t > 2.0:
        g = pop(prog(t, 2.0, 0.4))
        text_c(d, (540, 1140), "Is the star flickering?", font(int(60 * g) + 1, "bold"), th["accent"],
               stroke_width=5, stroke_fill=DARK)


def s2(img, d, t, T, th):
    star(d, 540, 420, 90)
    text_c(d, (540, 580), "very, very far away", font(54, "bold"), WHITE)
    k = ease(prog(t, 0.6, 1.2))
    r = 90 * (1 - k) + 8 * k
    star(d, 540, 820, r) if r > 12 else d.ellipse([532, 812, 548, 828], fill=STAR)
    if t > 1.6:
        text_c(d, (540, 1000), "looks like a tiny POINT", font(58, "bold"), th["accent"])


def s3(img, d, t, T, th):
    d.ellipse([532, 302, 548, 318], fill=STAR)
    air_layers(d, t, 450, 950)
    k = ease(prog(t, 0.3, 1.6))
    d.line([(540, 320), (540, 320 + 700 * k)], fill=STAR, width=6)
    eye(d, 540, 1080, 0.9)
    text_c(d, (850, 400), "moving air", font(46, "bold"), AIR1)


def s4(img, d, t, T, th):
    d.ellipse([532, 302, 548, 318], fill=STAR)
    air_layers(d, t, 450, 950)
    # bent, wobbling ray through the layers
    pts, x = [(540, 320)], 540
    for i in range(6):
        y = 450 + i * 100
        x += math.sin(t * 3 + i * 1.7) * 35
        pts.append((x, y))
    pts.append((540, 1040))
    d.line(pts, fill=STAR, width=6)
    if t > 0.8:
        text_c(d, (540, 1150), "each layer bends the light", font(52, "bold"), WHITE)


def s5(img, d, t, T, th):
    k = twinkle(t * 1.2, 3)
    dx = math.sin(t * 7) * 18
    star(d, 540 + dx, 600, 70 + 60 * k, int(120 + 135 * k))
    labels = ["brighter", "dimmer", "wobbles"]
    for i, lb in enumerate(labels):
        if t > 0.5 + i * 0.6:
            text_c(d, (220 + i * 320, 960), lb, font(56, "bold"), th["accent"] if i != 1 else th["soft"])


def s6(img, d, t, T, th):
    # curved sky dome over the Earth
    d.ellipse([-300, 1000, 1380, 2200], fill=(40, 90, 70))
    d.arc([-450, 560, 1530, 2400], 180, 360, fill=AIR1 + (180,), width=14)
    eye(d, 540, 1040, 0.6)
    # overhead star: short path; horizon star: long path
    d.line([(540, 330), (540, 1010)], fill=STAR, width=5)
    star(d, 540, 320, 30)
    d.line([(110, 900), (500, 1030)], fill=STAR, width=5)
    k = twinkle(t, 1)
    star(d, 110, 890, 26 + 18 * k, int(140 + 115 * k))
    if t > 0.8:
        text_c(d, (575, 690), "near the horizon:", font(40, "bold"), WHITE, anchor="lm")
        text_c(d, (575, 750), "more air, more twinkle", font(40, "bold"), th["accent"], anchor="lm")


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 540), "The twinkle isn't", font(int(74 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 650), "in the star", font(int(74 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        text_c(d, (540, 850), "it's in our AIR", font(88, "bold"), th["accent"])


SCENES = [
    dict(say="On a clear night, stars twinkle. Is the star flickering?", draw=s1),
    dict(say="Stars are so far away, each looks like a tiny point.", draw=s2),
    dict(say="That light passes through moving air to reach your eye.", draw=s3),
    dict(say="Warm and cool air bend the light differently, and keep shifting.", draw=s4),
    dict(say="So the starlight wobbles, brighter, then dimmer.", draw=s5),
    dict(say="Near the horizon, light crosses more air, so stars twinkle more.", draw=s6),
    dict(say="The twinkle isn't in the star. It's in our air.", draw=s7),
]
