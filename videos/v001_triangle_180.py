import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "Why do a triangle's angles always add up to 180°?"
COLS = [(255, 99, 120), (90, 200, 255), (120, 230, 140)]  # A, B, C


def lerp(a, b, k): return a + (b - a) * k
def lp(p, q, k): return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))


def ang(v, p):
    return math.degrees(math.atan2(p[1] - v[1], p[0] - v[0])) % 360


def interior(v, p, q):
    """start angle and extent (clockwise, screen coords) of interior angle at v."""
    a, b = ang(v, p), ang(v, q)
    delta = (b - a) % 360
    if delta > 180: a, delta = b, 360 - delta
    return a, delta


def sector(d, v, start, ext, r, col, label=None):
    d.pieslice([v[0] - r, v[1] - r, v[0] + r, v[1] + r], start, start + ext, fill=col + (235,),
               outline=(255, 255, 255), width=4)
    if label:
        m = math.radians(start + ext / 2)
        text_c(d, (v[0] + math.cos(m) * r * 0.6, v[1] + math.sin(m) * r * 0.6), label, font(44, "bold"), (20, 20, 40))


def tri_angles(P):
    return [interior(P[i], P[(i + 1) % 3], P[(i + 2) % 3]) for i in range(3)]


def triangle(d, P, width=8, col=(255, 255, 255, 255)):
    d.line([P[0], P[1], P[2], P[0]], fill=col, width=width, joint="curve")


# ---- scene 1: morphing triangle with live angle values ----
SHAPES = [[(200, 1000), (880, 1000), (470, 400)],
          [(160, 1000), (900, 1000), (840, 520)],
          [(300, 1000), (780, 1000), (540, 330)],
          [(120, 950), (960, 1020), (300, 620)]]


def s1(img, d, t, T, th):
    n = len(SHAPES); seg = 1.4
    k = (t / seg) % n; i = int(k); f = ease((k - i) * 1.6)
    P = [lp(SHAPES[i][j], SHAPES[(i + 1) % n][j], f) for j in range(3)]
    P = [(x, y - 60) for x, y in P]
    A = tri_angles(P)
    d.polygon(P, fill=(255, 255, 255, 25))
    for (s, e), v, c in zip(A, P, COLS): sector(d, v, s, e, 80, c)
    triangle(d, P)
    vals = [round(e) for _, e in A]
    vals[2] = 180 - vals[0] - vals[1]
    f2 = font(64, "sym")
    parts = [(f"{vals[0]}°", COLS[0]), (" + ", th["ink"]), (f"{vals[1]}°", COLS[1]), (" + ", th["ink"]),
             (f"{vals[2]}°", COLS[2]), (" = ", th["ink"]), ("180°", th["accent"])]
    tw = sum(d.textlength(p, font=f2) for p, _ in parts); x = W / 2 - tw / 2
    for p, c in parts:
        d.text((x, 1060), p, font=f2, fill=c); x += d.textlength(p, font=f2)


# ---- scene 2: three different triangles, all 180 ----
def make_tri(cx, base, a, b, ybase):
    p1, p2 = (cx - base / 2, ybase), (cx + base / 2, ybase)
    L = base * math.sin(math.radians(b)) / math.sin(math.radians(a + b))
    p3 = (p1[0] + L * math.cos(math.radians(a)), p1[1] - L * math.sin(math.radians(a)))
    return [p1, p2, p3]


SMALL = [("Equal", 60, 60), ("Right", 90, 30), ("Wide", 20, 40)]


def s2(img, d, t, T, th):
    rows = [430, 700, 970]
    for k, (name, a, b) in enumerate(SMALL):
        p = pop(prog(t, 0.15 + k * 0.55, 0.45))
        if p <= 0: continue
        y = rows[k]
        P = make_tri(300, 300 * p, a, b, y + 90)
        if k == 2:  # wide triangle is short; scale it up
            P = make_tri(300, 360 * p, a, b, y + 60)
        A = tri_angles(P)
        for (s, e), v, c in zip(A, P, COLS): sector(d, v, s, e, 45 * p, c)
        triangle(d, P, 6)
        c3 = 180 - a - b
        f = font(52, "sym")
        line = f"{a}° + {b}° + {c3}°"
        d.text((520, y - 10), line, font=f, fill=th["ink"])
        d.text((520, y + 55), "= 180°", font=f, fill=th["accent"])


# ---- scenes 3-6: tear corners and line them up ----
BIG = [(200, 800), (880, 800), (430, 330)]
LINE_PT = (540, 1080)
R = 130


def targets():
    A = tri_angles(BIG)
    exts = [e for _, e in A]
    # order on the line: C, A, B  (left to right means clockwise from 180)
    order = [2, 0, 1]; start = 180; tg = {}
    for i in order:
        tg[i] = start; start += exts[i]
    return A, tg


def draw_pieces(d, k, th, wiggle=0.0, t=0):
    A, tg = targets()
    for i in (0, 1, 2):
        s0, e = A[i]
        ds = ((tg[i] - s0 + 540) % 360) - 180
        kk = ease(clamp(k * 1.25 - i * 0.12))
        v = lp(BIG[i], LINE_PT, kk)
        if wiggle and kk == 0:
            # pull corner slightly out of the triangle as if being torn off
            cx = sum(p[0] for p in BIG) / 3; cy = sum(p[1] for p in BIG) / 3
            dx, dy = BIG[i][0] - cx, BIG[i][1] - cy; L = math.hypot(dx, dy)
            off = 28 * wiggle * (0.6 + 0.4 * math.sin(t * 9 + i))
            v = (v[0] + dx / L * off, v[1] + dy / L * off)
        sector(d, v, s0 + ds * kk, e, R, COLS[i], "abc"[i])


def faint_triangle(d, alpha=255):
    d.polygon(BIG, fill=(255, 255, 255, int(22 * alpha / 255)))
    triangle(d, BIG, 7, (255, 255, 255, alpha))


def s3(img, d, t, T, th):
    faint_triangle(d)
    for i in range(3):  # dashed tear lines
        s, e = tri_angles(BIG)[i]
        v = BIG[i]
        for a in range(int(s), int(s + e), 8):
            d.arc([v[0] - R, v[1] - R, v[0] + R, v[1] + R], a, a + 4, fill=(255, 255, 255), width=5)
    draw_pieces(d, 0, th, wiggle=prog(t, 1.0, 0.6), t=t)
    text_c(d, (W / 2, 1100), "Tear off the 3 corners", font(56, "bold"), th["accent"])


def s4(img, d, t, T, th):
    faint_triangle(d, 110)
    draw_pieces(d, prog(t, 0.1, T * 0.8), th)


def straight_line(d, th, k=1.0):
    x0, x1 = LINE_PT[0] - 330, LINE_PT[0] + 330
    d.line([(x0, LINE_PT[1]), (lerp(x0, x1, k), LINE_PT[1])], fill=th["accent"], width=10)


def s5(img, d, t, T, th):
    faint_triangle(d, 110)
    straight_line(d, th, ease(prog(t, 0.2, 0.7)))
    draw_pieces(d, 1, th)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        text_c(d, (W / 2, 1150), "a  +  b  +  c  =  straight line", font(int(46 * g) + 1, "bold"), th["ink"])


def s6(img, d, t, T, th):
    faint_triangle(d, 80)
    straight_line(d, th)
    draw_pieces(d, 1, th)
    k = ease(prog(t, 0.1, 1.0)); r2 = 230
    d.arc([LINE_PT[0] - r2, LINE_PT[1] - r2, LINE_PT[0] + r2, LINE_PT[1] + r2], 180, 180 + 180 * k,
          fill=th["accent"], width=8)
    for deg in range(0, 181, 15):
        if deg > 180 * k: break
        a = math.radians(180 + deg)
        p1 = (LINE_PT[0] + math.cos(a) * (r2 - 18), LINE_PT[1] + math.sin(a) * (r2 - 18))
        p2 = (LINE_PT[0] + math.cos(a) * (r2 + 4), LINE_PT[1] + math.sin(a) * (r2 + 4))
        d.line([p1, p2], fill=th["accent"], width=5)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.45))
        text_c(d, (W / 2, LINE_PT[1] - r2 - 70), "180°", font(int(110 * g) + 1, "sym"), th["accent"],
               stroke_width=6, stroke_fill=(20, 20, 50))


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.5))
    d.rounded_rectangle([90, 420, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    f = font(int(84 * g) + 1, "sym")
    x = W / 2 - d.textlength("∠a + ∠b + ∠c", font=f) / 2
    for p, c in [("∠a", COLS[0]), (" + ", th["ink"]), ("∠b", COLS[1]), (" + ", th["ink"]), ("∠c", COLS[2])]:
        d.text((x, 560), p, font=f, fill=c); x += d.textlength(p, font=f)
    text_c(d, (W / 2, 760), "= 180°", font(int(130 * g) + 1, "sym"), th["accent"])
    if t > 0.6:
        text_c(d, (W / 2, 950), "Angle Sum Property  ·  Class 7", font(40, "semi"), th["soft"])


SCENES = [
    dict(say="Why do the angles of every triangle add up to exactly one hundred eighty degrees?",
         show="Why do the angles of every triangle add up to exactly 180°?", draw=s1),
    dict(say="Tiny, huge, or stretched, the answer never changes.", draw=s2),
    dict(say="Here's the proof. Tear off the three corners of a paper triangle.", draw=s3),
    dict(say="Now place them side by side, with their tips touching.", draw=s4),
    dict(say="Look! They make a perfect straight line.", draw=s5),
    dict(say="And a straight line measures one hundred eighty degrees.",
         show="And a straight line measures 180°.", draw=s6),
    dict(say="So every triangle's angles add up to one hundred eighty. Try it with notebook paper!",
         show="So every triangle's angles add up to 180. Try it with notebook paper!", draw=s7),
]
