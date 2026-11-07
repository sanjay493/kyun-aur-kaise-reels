from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why does a straw look broken in water?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
WATER, STRAW, RAY, GHOST = (120, 200, 255), (255, 110, 110), (255, 230, 90), (255, 255, 255)

# glass and water
GX0, GX1, GTOP, GBOT, WY = 300, 760, 420, 1080, 700
# real straw: a straight line from bottom-left to top-right
SA, SB = (400, 1040), (840, 300)


def on_straw(y):
    k = (y - SA[1]) / (SB[1] - SA[1])
    return SA[0] + (SB[0] - SA[0]) * k


SURF_X = on_straw(WY)
SHIFT = 70  # how far the underwater part appears displaced (schematic)


def glass(d, water_alpha=150):
    d.rectangle([GX0, WY, GX1, GBOT], fill=WATER + (water_alpha,))
    d.line([(GX0, WY), (GX1, WY)], fill=(200, 235, 255), width=5)
    d.line([(GX0, GTOP), (GX0 + 20, GBOT)], fill=WHITE, width=6)
    d.line([(GX1, GTOP), (GX1 - 20, GBOT)], fill=WHITE, width=6)
    d.line([(GX0 + 20, GBOT), (GX1 - 20, GBOT)], fill=WHITE, width=6)
    # lemon slice
    d.ellipse([GX0 + 40, WY - 30, GX0 + 140, WY + 30], fill=(250, 230, 90), outline=(200, 190, 40), width=4)


def straw_above(d, a=255):
    d.line([(SURF_X, WY), SB], fill=STRAW + (a,), width=26)


def straw_real_below(d, a=255):
    d.line([SA, (SURF_X, WY)], fill=STRAW + (a,), width=26)


RATIO = 0.7  # schematic: the underwater part is seen raised


def raised(pt):
    return (pt[0], WY + (pt[1] - WY) * RATIO)


def straw_seen_below(d, a=255):
    # apparent underwater part: each point seen raised towards the surface (schematic)
    d.line([raised(SA), (SURF_X, WY)], fill=STRAW + (a,), width=30)


def eye(d, x, y):
    d.ellipse([x - 60, y - 35, x + 60, y + 35], fill=WHITE, outline=DARK, width=5)
    d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=(60, 120, 80))
    d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=DARK)


P0 = (on_straw(950), 950)
Q0 = (P0[0] - 120, WY)
_A = raised(P0)
EYE = (Q0[0] + 1.4 * (Q0[0] - _A[0]), Q0[1] + 1.4 * (Q0[1] - _A[1]))


def s1(img, d, t, T, th):
    glass(d)
    straw_above(d)
    straw_seen_below(d)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1160), "Broken?", font(int(76 * g) + 1, "bold"), th["accent"], stroke_width=4,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    glass(d)
    straw_above(d)
    k = ease(prog(t, 0.3, 0.8))
    straw_seen_below(d, int(255 * (1 - 0.75 * k)))
    straw_real_below(d, int(255 * k))
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 1160), "the straw is straight", font(int(58 * g) + 1, "bold"), WHITE)


def s3(img, d, t, T, th):
    glass(d)
    straw_above(d, 120)
    straw_real_below(d)
    # ray from a point on the underwater straw up to the surface, bends, goes to the eye
    P, Q = P0, Q0
    k1 = ease(prog(t, 0.2, 0.7))
    d.line([P, (P[0] + (Q[0] - P[0]) * k1, P[1] + (Q[1] - P[1]) * k1)], fill=RAY, width=8)
    if t > 0.9:
        k2 = ease(prog(t, 0.9, 0.7))
        d.line([Q, (Q[0] + (EYE[0] - Q[0]) * k2, Q[1] + (EYE[1] - Q[1]) * k2)], fill=RAY, width=8)
        g = pop(prog(t, 0.9, 0.4))
        d.ellipse([Q[0] - 22 * g, Q[1] - 22 * g, Q[0] + 22 * g, Q[1] + 22 * g], outline=WHITE, width=5)
        text_c(d, (Q[0] - 30, Q[1] + 60), "bends here", font(36, "bold"), RAY, anchor="rm")
    eye(d, *EYE)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([290, 1110, 790, 1200], 36, fill=th["accent"])
        text_c(d, (540, 1155), "REFRACTION", font(int(56 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    glass(d)
    straw_above(d, 120)
    straw_real_below(d, 140)
    P, Q = P0, Q0
    d.line([P, Q], fill=RAY, width=8)
    d.line([Q, EYE], fill=RAY, width=8)
    eye(d, *EYE)
    # brain extends the last straight line backwards (dashed)
    k = ease(prog(t, 0.5, 1.0))
    dx, dy = _A[0] - Q[0], _A[1] - Q[1]
    L = k
    n = 10
    for i in range(n):
        a, b = i / n, (i + 0.5) / n
        if a > L: break
        b = min(b, L)
        d.line([(Q[0] + dx * a, Q[1] + dy * a), (Q[0] + dx * b, Q[1] + dy * b)], fill=WHITE, width=6)
    text_c(d, (540, 1160), "brain: \"light came straight\"", font(48, "bold"), WHITE)


def s5(img, d, t, T, th):
    glass(d)
    straw_above(d)
    straw_real_below(d, 70)
    k = ease(prog(t, 0.3, 0.8))
    straw_seen_below(d, int(255 * k))
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        text_c(d, (285, raised(SA)[1]), "seen here", font(int(40 * g) + 1, "bold"), WHITE, anchor="rm")
        text_c(d, (285, SA[1]), "really here", font(int(40 * g) + 1, "bold"), th["soft"], anchor="rm")
    if t > 1.6:
        text_c(d, (540, 1160), "a place it isn't", font(58, "bold"), th["accent"])


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    d.line([(360, 640), (720, 420)], fill=STRAW, width=26)
    text_c(d, (540, 800), "The straw stays straight.", font(int(58 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 930), "Its LIGHT takes a turn.", font(int(64 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Put a straw in a glass of nimbu paani. Why does it look broken?", draw=s1),
    dict(say="The straw isn't bent. The light coming from it is.", draw=s2),
    dict(say="Light bends when it crosses from water into air. That's called refraction.", draw=s3),
    dict(say="Your eyes and brain assume light came in a straight line.", draw=s4),
    dict(say="So they place the underwater part of the straw somewhere it isn't.", draw=s5),
    dict(say="The straw stays straight. Its light takes a turn.", draw=s6),
]
