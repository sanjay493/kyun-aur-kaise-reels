import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why is a circle's area πr²?"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
CRUST, CHEESE, SAUCE = (215, 150, 70), (255, 215, 110), (225, 90, 60)
GREEN, PINK, BLUE = (110, 220, 140), (255, 150, 200), (120, 190, 255)
N = 12


def pizza(d, cx, cy, r, cuts=0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CRUST)
    ri = r * 0.88
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=CHEESE)
    for a, b in [(-0.4, -0.3), (0.35, -0.45), (0.1, 0.35), (-0.45, 0.3), (0.5, 0.2), (0.0, -0.05)]:
        d.ellipse([cx + a * r - 18, cy + b * r - 18, cx + a * r + 18, cy + b * r + 18], fill=SAUCE)
    for i in range(cuts):
        a = 2 * math.pi * i / N - math.pi / 2
        d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], fill=DARK, width=5)


def wedge(d, tip, ang, r, up=True):
    """Pizza slice with its tip at `tip`, opening downward (up=True) or upward."""
    x, y = tip
    half = math.pi / N
    base = math.pi / 2 if up else -math.pi / 2
    pts = [(x, y)]
    for j in range(9):
        a = base - half + 2 * half * j / 8
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    d.polygon(pts, fill=CHEESE, outline=DARK)
    # crust on the curved edge
    d.line(pts[1:], fill=CRUST, width=12)


def strip(d, k, r, y0, x_mid=540):
    """Slices arranged tips-up, tips-down; k (0-1) squeezes them together."""
    w = 2 * r * math.sin(math.pi / N)  # chord width of one slice
    step = w / 2 * (1 + 0.6 * (1 - k))
    n = N
    total = step * (n - 1)
    for i in range(n):
        x = x_mid - total / 2 + i * step
        if i % 2 == 0:
            wedge(d, (x, y0), 0, r, up=True)      # tip at top, crust at bottom
        else:
            wedge(d, (x, y0 + r), 0, r, up=False)  # tip at bottom, crust at top


def s1(img, d, t, T, th):
    pizza(d, 540, 680, 250)
    g = pop(prog(t, 0.6, 0.45))
    text_c(d, (540, 360), "Area = πr²", font(int(90 * g) + 1, "sym"), WHITE)
    if t > 1.4:
        text_c(d, (540, 1030), "but why?", font(64, "bold"), th["accent"])


def s2(img, d, t, T, th):
    cuts = int(clamp(t / 0.9) * N)
    if t < 1.3:
        pizza(d, 540, 640, 230, cuts)
        text_c(d, (540, 350), "12 equal slices", font(60, "bold"), WHITE)
    else:
        strip(d, 0.0, 200, 560)
        text_c(d, (540, 350), "tips up, tips down", font(60, "bold"), WHITE)


def s3(img, d, t, T, th):
    k = ease(prog(t, 0.1, 1.0))
    strip(d, k, 200, 560)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([160, 940, 920, 1070], 50, fill=th["accent"])
        text_c(d, (540, 1005), "almost a rectangle!", font(int(58 * g) + 1, "bold"), DARK)
    text_c(d, (540, 350), "Push them together", font(58, "bold"), WHITE)


def s4(img, d, t, T, th):
    strip(d, 1.0, 200, 520)
    w = 2 * 200 * math.sin(math.pi / N)
    L = w / 2 * (N - 1) + w / 2
    x0, x1 = 540 - L / 2, 540 + L / 2
    if t > 0.2:
        g = pop(prog(t, 0.2, 0.4))
        d.line([(x0 - 40, 520), (x0 - 40, 720)], fill=PINK, width=8)
        text_c(d, (x0 - 80, 620), "r", font(int(64 * g) + 1, "bold"), PINK)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.line([(x0, 770), (x1, 770)], fill=BLUE, width=8)
        text_c(d, (540, 840), "half the crust", font(int(50 * g) + 1, "bold"), BLUE)
        text_c(d, (540, 930), "½ × 2πr = πr", font(int(64 * g) + 1, "sym"), WHITE)
    text_c(d, (540, 350), "Measure it", font(60, "bold"), th["accent"])


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Rectangle area", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([200, 460, 880, 700], 10, fill=CHEESE, outline=CRUST, width=12)
    text_c(d, (540, 740), "πr", font(int(56 * g) + 1, "sym"), BLUE)
    text_c(d, (160, 580), "r", font(int(56 * g) + 1, "bold"), PINK)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.4))
        text_c(d, (540, 900), "length × height", font(int(56 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 1010), "πr × r", font(int(80 * g2) + 1, "sym"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "= πr²", font(int(120 * g) + 1, "sym"), th["accent"])
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "Every circle hides", font(int(64 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 860), "a rectangle.", font(int(64 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Why is a circle's area pi r squared? Cut a pizza and find out.",
         show="Why is a circle's area πr²? Cut a pizza and find out.", draw=s1),
    dict(say="Slice it into many equal pieces, and lay them tips up, tips down.", draw=s2),
    dict(say="It looks almost like a rectangle. The more slices, the straighter it gets.", draw=s3),
    dict(say="Height: the radius, r. Length: half the crust, which is pi r.",
         show="Height: the radius, r. Length: half the crust, which is πr.", draw=s4),
    dict(say="Rectangle area: length times height. Pi r times r.",
         show="Rectangle area: length × height. πr × r.", draw=s5),
    dict(say="Pi r squared. Every circle hides a rectangle.", show="πr². Every circle hides a rectangle.", draw=s6),
]
