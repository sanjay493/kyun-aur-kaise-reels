from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Add up odd numbers. Notice anything?"
WHITE, DARK = (255, 255, 255), (20, 20, 50)
LAYER = [(255, 205, 60), (110, 215, 255), (255, 130, 170), (130, 230, 150), (200, 160, 255)]


def dots(d, cx, cy, n_layers, step=70, r=24, show=None, reveal=1.0):
    """Draw an n x n square of dots, each L-shaped layer in its own colour.
    show: number of layers fully drawn; reveal (0-1): how much of the next layer has appeared."""
    n = n_layers
    x0 = cx - (n - 1) * step / 2
    y0 = cy - (n - 1) * step / 2
    full = n if show is None else show
    for i in range(n):
        for j in range(n):
            layer = max(i, j)
            if layer < full:
                g = 1.0
            elif layer == full:
                g = reveal
            else:
                continue
            if g <= 0:
                continue
            rr = r * pop(g)
            x, y = x0 + j * step, y0 + i * step
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=LAYER[layer % 5])


def s1(img, d, t, T, th):
    nums = ["1", "3", "5", "7", "9", "11"]
    for i, s in enumerate(nums):
        g = pop(prog(t, 0.1 + i * 0.18, 0.35))
        if g > 0:
            x = 140 + i * 160
            d.ellipse([x - 65, 520 - 65, x + 65, 520 + 65], fill=LAYER[i % 5])
            text_c(d, (x, 520), s, font(int(64 * g) + 1, "bold"), DARK)
    if t > 1.4:
        text_c(d, (540, 760), "odd numbers", font(70, "bold"), WHITE)
        text_c(d, (540, 870), "keep adding...", font(60, "bold"), th["accent"])


def s2(img, d, t, T, th):
    lines = [("1", "= 1"), ("1 + 3", "= 4"), ("1 + 3 + 5", "= 9"), ("1 + 3 + 5 + 7", "= 16")]
    for i, (a, b) in enumerate(lines):
        g = ease(prog(t, 0.1 + i * 0.55, 0.4))
        if g <= 0:
            continue
        y = 380 + i * 175
        text_c(d, (620, y), a, font(70, "bold"), (255, 255, 255, int(255 * g)), anchor="rm")
        text_c(d, (660, y), b, font(76, "bold"), th["accent"] + (int(255 * g),), anchor="lm")


def s3(img, d, t, T, th):
    for i, (n, x) in enumerate([(1, 160), (2, 380), (3, 640), (4, 920)]):
        g = prog(t, 0.1 + i * 0.3, 0.4)
        if g > 0:
            dots(d, x, 600, n, step=48, r=17, reveal=g, show=None)
            text_c(d, (x, 880), str(n * n), font(80, "bold"), th["accent"])
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 1060), "SQUARE numbers!", font(int(80 * g) + 1, "bold"), WHITE,
               stroke_width=4, stroke_fill=DARK)


def s4(img, d, t, T, th):
    k = prog(t, 0.4, 0.8)
    dots(d, 540, 640, 4, step=95, r=32, show=3, reveal=k)
    if t > 1.2:
        text_c(d, (540, 1060), "each odd number = one L-shaped layer", font(46, "bold"), WHITE)


def s5(img, d, t, T, th):
    # 1 dot -> +3 -> 2x2 -> +5 -> 3x3
    stage1 = prog(t, 0.3, 0.6)
    stage2 = prog(t, 1.6, 0.6)
    if stage2 <= 0:
        dots(d, 540, 620, 2, step=120, r=42, show=1, reveal=stage1)
        if stage1 > 0.2:
            text_c(d, (540, 950), "1 + 3  =  2 × 2", font(76, "bold"), th["accent"])
    else:
        dots(d, 540, 620, 3, step=120, r=42, show=2, reveal=stage2)
        text_c(d, (540, 950), "+ 5  =  3 × 3", font(76, "bold"), th["accent"])


def s6(img, d, t, T, th):
    nums = [str(2 * i + 1) for i in range(10)]
    f = font(52, "bold")
    k = ease(prog(t, 0.1, 1.0))
    shown = int(k * 10 + 0.001)
    row1 = " + ".join(nums[:5])
    row2 = " + ".join(nums[5:])
    if shown > 0:
        text_c(d, (540, 400), " + ".join(nums[:min(5, shown)]), f, WHITE)
    if shown > 5:
        text_c(d, (540, 490), "+ " + " + ".join(nums[5:shown]), f, WHITE)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.45))
        d.rounded_rectangle([170, 620, 910, 800], 40, fill=th["accent"])
        text_c(d, (540, 710), "10 × 10 = 100", font(int(84 * g) + 1, "bold"), DARK)
        text_c(d, (540, 900), "first 10 odd numbers", font(54, "bold"), th["soft"])


def s7(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    k = prog(t, 0.1, 0.9)
    dots(d, 540, 560, 5, step=48, r=17, show=int(k * 5), reveal=(k * 5) % 1 if k < 1 else 1)
    g = pop(prog(t, 0.6, 0.45))
    text_c(d, (540, 860), "Odd numbers", font(int(80 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 970), "build squares", font(int(80 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Add odd numbers, starting from one. Watch the answers.", draw=s1),
    dict(say="One plus three is four. Plus five, nine. Plus seven, sixteen.",
         show="1 + 3 is 4. Plus 5, 9. Plus 7, 16.", draw=s2),
    dict(say="Four, nine, sixteen. All square numbers!", show="4, 9, 16. All square numbers!", draw=s3),
    dict(say="Why? Each odd number adds an L-shaped layer of dots.", draw=s4),
    dict(say="One dot, plus three, makes two by two. Five more make three by three.",
         show="1 dot, plus 3, makes 2 × 2. 5 more make 3 × 3.", draw=s5),
    dict(say="So the first ten odd numbers add up to one hundred.",
         show="So the first 10 odd numbers add up to 100.", draw=s6),
    dict(say="Odd numbers build squares, one layer at a time.", draw=s7),
]
