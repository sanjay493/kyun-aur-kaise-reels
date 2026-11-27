from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why is a pinhole camera's image upside down?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
WAX, FLAME, CORE = (245, 240, 225), (255, 170, 50), (255, 235, 120)
TOPC, BOTC = (255, 120, 120), (120, 190, 255)
BOX, SCREEN = (70, 60, 55), (235, 225, 200)

HOLE = (560, 700)


def candle(d, x, base, s=1.0, flip=False, alpha=255):
    """Candle standing on base (or hanging from base when flipped). Total height about 360*s."""
    sgn = -1 if not flip else 1
    wax_top = base + sgn * 220 * s
    y0, y1 = sorted([base, wax_top])
    d.rectangle([x - 40 * s, y0, x + 40 * s, y1], fill=WAX + (alpha,))
    tip = wax_top + sgn * 140 * s
    mid = wax_top + sgn * 60 * s
    d.polygon([(x - 34 * s, mid), (x, tip), (x + 34 * s, mid), (x, wax_top)], fill=FLAME + (alpha,))
    d.ellipse([x - 16 * s, mid - 24 * s, x + 16 * s, mid + 24 * s], fill=CORE + (alpha,))
    return tip


def setup(d, show_screen=True):
    # pinhole wall
    d.rectangle([HOLE[0] - 14, 380, HOLE[0] + 14, HOLE[1] - 12], fill=BOX)
    d.rectangle([HOLE[0] - 14, HOLE[1] + 12, HOLE[0] + 14, 1020], fill=BOX)
    if show_screen:
        d.rectangle([900, 460, 930, 940], fill=SCREEN)
        text_c(d, (915, 990), "screen", font(36, "semi"), WHITE)
    text_c(d, (HOLE[0], 1060), "pinhole", font(36, "semi"), WHITE)


def s1(img, d, t, T, th):
    setup(d)
    tip = candle(d, 220, 900, 1.0)
    if t > 0.8:
        k = ease(prog(t, 0.8, 0.8))
        a = int(255 * k)
        candle(d, 860, 580, 0.6, flip=True, alpha=a)
    if t > 1.6:
        text_c(d, (540, 330), "Upside down! Why?", font(64, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 340), "Light travels in", font(62, "bold"), WHITE)
    text_c(d, (540, 420), "straight lines", font(70, "bold"), th["accent"])
    k = ease(prog(t, 0.3, 1.2))
    for i in range(5):
        y = 600 + i * 110
        d.line([(140, y), (140 + 800 * k, y)], fill=CORE, width=8)
        if k > 0.98:
            x = 940
            d.polygon([(x, y - 18), (x + 30, y), (x, y + 18)], fill=CORE)


def ray(d, p0, p1, col, k):
    x = p0[0] + (p1[0] - p0[0]) * k
    y = p0[1] + (p1[1] - p0[1]) * k
    d.line([p0, (x, y)], fill=col, width=7)


def through(p, hole, xs):
    # continue straight line p -> hole until x = xs
    m = (hole[1] - p[1]) / (hole[0] - p[0])
    return (xs, hole[1] + m * (xs - hole[0]))


def s3(img, d, t, T, th):
    setup(d)
    tip = candle(d, 220, 900, 1.0)
    top = (220, tip)
    end = through(top, HOLE, 900)
    k1 = ease(prog(t, 0.2, 0.6))
    ray(d, top, HOLE, TOPC, k1)
    if k1 >= 1:
        k2 = ease(prog(t, 0.8, 0.6))
        ray(d, HOLE, end, TOPC, k2)
        if k2 >= 1:
            d.ellipse([end[0] - 16, end[1] - 16, end[0] + 16, end[1] + 16], fill=TOPC)
    text_c(d, (540, 330), "top of flame", font(52, "bold"), TOPC)
    if t > 1.5:
        text_c(d, (540, 1150), "lands at the bottom", font(52, "bold"), TOPC)


def s4(img, d, t, T, th):
    setup(d)
    tip = candle(d, 220, 900, 1.0)
    top, bot = (220, tip), (220, 900)
    et, eb = through(top, HOLE, 900), through(bot, HOLE, 900)
    ray(d, top, HOLE, TOPC, 1)
    ray(d, HOLE, et, TOPC, 1)
    k = ease(prog(t, 0.1, 0.8))
    ray(d, bot, HOLE, BOTC, k)
    if k >= 1:
        k2 = ease(prog(t, 0.9, 0.6))
        ray(d, HOLE, eb, BOTC, k2)
    if t > 1.5:
        # flipped image on screen, scaled to fit between eb (top) and et (bottom)
        hgt = et[1] - eb[1]
        candle(d, 860, eb[1], hgt / 360, flip=True)
        text_c(d, (540, 330), "bottom goes to the top", font(52, "bold"), BOTC)
        text_c(d, (540, 1150), "The picture flips!", font(56, "bold"), th["accent"])
    else:
        text_c(d, (540, 330), "bottom of flame", font(52, "bold"), BOTC)


def s5(img, d, t, T, th):
    text_c(d, (540, 330), "Hole too big?", font(64, "bold"), th["accent"])
    # sharp vs blurry
    d.rounded_rectangle([110, 440, 510, 960], 30, fill=(255, 255, 255, 25))
    d.rounded_rectangle([570, 440, 970, 960], 30, fill=(255, 255, 255, 25))
    candle(d, 310, 560, 0.85, flip=True)
    text_c(d, (310, 1010), "tiny hole", font(42, "semi"), WHITE)
    g = ease(prog(t, 0.4, 0.8))
    if t > 0.4:
        for dx, dy in ((-24, -10), (24, 10), (-10, 22), (12, -22), (0, 0)):
            candle(d, 770 + dx * g, 560 + dy * g, 0.85, flip=True, alpha=70)
        text_c(d, (770, 1010), "big hole: blurry", font(42, "semi"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Straight lines", font(int(74 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 650), "cross at the hole", font(int(64 * g2) + 1, "bold"), CORE)
    if t > 1.1:
        g3 = pop(prog(t, 1.1, 0.45))
        text_c(d, (540, 830), "= upside down", font(int(80 * g3) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Point a pinhole camera at a candle. The flame appears upside down. Why?", draw=s1),
    dict(say="Because light travels in straight lines.", draw=s2),
    dict(say="Light from the flame's top goes straight through the tiny hole, to the screen's bottom.", draw=s3),
    dict(say="Light from the bottom goes up to the top. So the whole picture flips.", draw=s4),
    dict(say="Make the hole too big, and the image turns blurry.", draw=s5),
    dict(say="Straight lines crossing at one hole: an upside down image.", draw=s6),
]
