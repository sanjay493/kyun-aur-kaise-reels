from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why is a triangle's area HALF?"
WHITE, DARK = (255, 255, 255), (20, 20, 50)
TRI, LEFT, RIGHT = (255, 205, 60), (110, 215, 255), (255, 130, 170)

# triangle: base from (A) to (B), apex P above the base
AX, BX, BY, TOP = 200, 880, 900, 450
PX = 420


def lerp(a, b, k): return a + (b - a) * k


def rect(d, a=255, width=6):
    d.rectangle([AX, TOP, BX, BY], outline=(255, 255, 255, a), width=width)


def triangle(d, fill=TRI, a=255):
    d.polygon([(AX, BY), (BX, BY), (PX, TOP)], fill=fill + (a,))


def labels(d, th):
    text_c(d, ((AX + BX) / 2, BY + 55), "base", font(48, "bold"), th["accent"])
    d.line([(BX + 30, TOP), (BX + 30, BY)], fill=th["soft"], width=4)
    d.line([(BX + 18, TOP), (BX + 42, TOP)], fill=th["soft"], width=4)
    d.line([(BX + 18, BY), (BX + 42, BY)], fill=th["soft"], width=4)
    text_c(d, (BX + 50, (TOP + BY) / 2), "height", font(36, "bold"), th["soft"], anchor="lm")


def s1(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.5))
    if g > 0:
        cx, cy = 540, 670
        pts = [(cx + (x - 540) * g, cy + (y - 675) * g) for x, y in [(AX, BY), (BX, BY), (PX, TOP)]]
        d.polygon(pts, fill=TRI)
    if t > 0.9:
        text_c(d, (540, 1040), "Area = ½ × base × height", font(60, "bold"), WHITE)
    if t > 1.8:
        g2 = pop(prog(t, 1.8, 0.4))
        text_c(d, (540, 1140), "Why HALF?", font(int(70 * g2) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    triangle(d)
    k = ease(prog(t, 0.3, 1.0))
    if k > 0:
        rect(d, int(255 * k))
    if t > 1.0:
        labels(d, th)


def s3(img, d, t, T, th):
    if t > 1.2:
        g = ease(prog(t, 1.2, 0.5))
        d.rectangle([AX, TOP, PX, BY], fill=LEFT + (int(70 * g),))
        d.rectangle([PX, TOP, BX, BY], fill=RIGHT + (int(70 * g),))
    triangle(d)
    rect(d)
    k = ease(prog(t, 0.3, 0.8))
    if k > 0:
        d.line([(PX, TOP), (PX, lerp(TOP, BY, k))], fill=WHITE, width=6)
    if t > 1.2:
        text_c(d, (540, 1080), "two rectangles", font(60, "bold"), th["accent"])


def s4(img, d, t, T, th):
    rect(d)
    d.line([(PX, TOP), (PX, BY)], fill=WHITE, width=6)
    # left rectangle: inside piece (part of triangle) and outside piece
    k = ease(prog(t, 0.2, 0.6))
    d.polygon([(AX, BY), (PX, BY), (PX, TOP)], fill=LEFT)                          # in
    d.polygon([(AX, BY), (AX, TOP), (PX, TOP)], fill=LEFT + (int(255 * (1 - 0.7 * k)),))  # out
    k2 = ease(prog(t, 0.9, 0.6))
    d.polygon([(PX, BY), (BX, BY), (PX, TOP)], fill=RIGHT)
    d.polygon([(PX, TOP), (BX, TOP), (BX, BY)], fill=RIGHT + (int(255 * (1 - 0.7 * k2)),))
    d.line([(AX, BY), (PX, TOP), (BX, BY)], fill=DARK, width=6)
    if t > 1.6:
        text_c(d, (540, 1080), "each one cut in HALF", font(60, "bold"), th["accent"])


def s5(img, d, t, T, th):
    rect(d)
    triangle(d)
    k = ease(prog(t, 0.2, 0.6))
    d.polygon([(AX, BY), (AX, TOP), (PX, TOP)], fill=(255, 255, 255, int(45 * k)))
    d.polygon([(PX, TOP), (BX, TOP), (BX, BY)], fill=(255, 255, 255, int(45 * k)))
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        d.rounded_rectangle([150, 1010, 930, 1130], 36, fill=th["accent"])
        text_c(d, (540, 1070), "triangle = ½ rectangle", font(int(58 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    # 8 x 5 grid, triangle on it
    step, x0, y0 = 90, 180, 420
    for i in range(9):
        d.line([(x0 + i * step, y0), (x0 + i * step, y0 + 5 * step)], fill=(255, 255, 255, 60), width=2)
    for j in range(6):
        d.line([(x0, y0 + j * step), (x0 + 8 * step, y0 + j * step)], fill=(255, 255, 255, 60), width=2)
    d.polygon([(x0, y0 + 5 * step), (x0 + 8 * step, y0 + 5 * step), (x0 + 3 * step, y0)], fill=TRI + (220,))
    text_c(d, (x0 + 4 * step, y0 + 5 * step + 45), "base 8", font(42, "bold"), th["accent"])
    text_c(d, (x0 + 8 * step + 70, y0 + 2.5 * step), "height 5", font(36, "bold"), th["soft"])
    if t > 0.6:
        text_c(d, (540, 1000), "8 × 5 = 40", font(64, "bold"), WHITE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 1110), "½ of 40 = 20", font(int(72 * g) + 1, "bold"), th["accent"])


def s7(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.05, 0.45))
    d.rectangle([300, 420, 780, 720], outline=WHITE, width=6)
    d.polygon([(300, 720), (780, 720), (480, 420)], fill=TRI)
    text_c(d, (540, 850), "Every triangle is", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 960), "half a rectangle", font(int(74 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="A triangle's area is half of base times height. Why half?", draw=s1),
    dict(say="Draw a rectangle around it, same base, same height.", draw=s2),
    dict(say="A line from the top corner straight down splits it into two rectangles.", draw=s3),
    dict(say="Each one is cut in half by a side of the triangle.", draw=s4),
    dict(say="So the triangle is exactly half the rectangle.", draw=s5),
    dict(say="Base eight, height five? That makes forty, and half is twenty.",
         show="Base 8, height 5? That makes 40, and half is 20.", draw=s6),
    dict(say="Every triangle is half a rectangle.", draw=s7),
]
