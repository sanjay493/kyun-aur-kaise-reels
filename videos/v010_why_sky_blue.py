import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "If sunlight is white, why is the sky blue?"
WHITE, DARK = (255, 255, 255), (20, 25, 40)
SUN = (255, 225, 110)
RAINBOW = [(235, 70, 70), (255, 150, 60), (255, 225, 80), (90, 200, 110), (70, 140, 255), (110, 80, 200),
           (170, 90, 220)]
BLUE = (70, 140, 255)


def sun(d, x, y, r, col=SUN):
    for k in range(3):
        rr = r + 25 + k * 22
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (30,))
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def s1(img, d, t, T, th):
    sun(d, 260, 420, 90)
    k = ease(prog(t, 0.2, 0.6))
    d.line([(340, 470), (340 + 420 * k, 470 + 250 * k)], fill=WHITE, width=14)
    if k >= 1:
        text_c(d, (720, 650), "white light", font(46, "semi"), WHITE, anchor="lm")
    g = pop(prog(t, 0.9, 0.4))
    if g > 0:
        d.rounded_rectangle([140, 820, 940, 1000], 40, fill=BLUE, outline=WHITE, width=5)
        text_c(d, (540, 910), "but the sky is BLUE?", font(int(66 * g) + 1, "bold"), WHITE, stroke_width=5,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    sun(d, 170, 640, 75)
    d.line([(250, 640), (470, 640)], fill=WHITE, width=16)
    # prism
    d.polygon([(470, 470), (380, 790), (600, 790)], fill=(220, 240, 255, 90), outline=WHITE)
    k = ease(prog(t, 0.3, 0.7))
    for i, c in enumerate(RAINBOW):
        y1 = 520 + i * 40
        d.line([(530, 640), (530 + 450 * k, 640 + (y1 - 640) * 1.6 * k)], fill=c, width=12)
    g = pop(prog(t, 1.2, 0.4))
    if g > 0:
        text_c(d, (540, 1020), "White = all colours mixed", font(int(56 * g) + 1, "bold"), th["accent"],
               stroke_width=5, stroke_fill=DARK)


def wave(d, x0, x1, y, wl, col, amp=30, width=8):
    pts = []
    for x in range(int(x0), int(x1), 6):
        pts.append((x, y + amp * math.sin((x - x0) / wl * 2 * math.pi)))
    if len(pts) > 1:
        d.line(pts, fill=col, width=width)


def s3(img, d, t, T, th):
    # tiny air particle in the middle, red wave passes, blue wave bounces everywhere
    px, py = 540, 640
    text_c(d, (540, 320), "tiny air particles", font(46, "semi"), th["soft"])
    k = ease(prog(t, 0.1, 0.9))
    wave(d, 80, 80 + 920 * k, 470, 180, RAINBOW[0], 30)  # red: long wavelength, mostly passes
    text_c(d, (90, 410), "red", font(40, "bold"), RAINBOW[0], anchor="lm")
    wave(d, 80, 80 + (px - 80) * k, 760, 70, BLUE, 30)  # blue: short wavelength, hits particle
    text_c(d, (90, 700), "blue", font(40, "bold"), BLUE, anchor="lm")
    for qx, qy in [(px, py), (px + 130, 560), (px - 40, 850), (px + 260, 760)]:
        d.ellipse([qx - 16, qy - 16, qx + 16, qy + 16], fill=(230, 235, 255), outline=WHITE, width=3)
    if k >= 0.6:
        g = ease(prog(t, 0.8, 0.8))
        for a in range(0, 360, 30):
            r0, r1 = 40, 40 + 220 * g
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([(px + ca * r0, 760 + sa * r0), (px + ca * r1, 760 + sa * r1)], fill=BLUE + (220,), width=7)
    if t > 1.8:
        text_c(d, (540, 1100), "Blue scatters far more than red", font(50, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def kid(d, x, y, s=1.0):
    d.ellipse([x - 40 * s, y - 150 * s, x + 40 * s, y - 70 * s], fill=(240, 190, 150))
    d.rounded_rectangle([x - 50 * s, y - 62 * s, x + 50 * s, y + 60 * s], 26 * s, fill=(255, 170, 90))
    d.ellipse([x - 22 * s, y - 128 * s, x - 10 * s, y - 114 * s], fill=DARK)
    d.ellipse([x + 10 * s, y - 128 * s, x + 22 * s, y - 114 * s], fill=DARK)


def s4(img, d, t, T, th):
    k = ease(prog(t, 0.1, 1.2))
    # sky fills with blue
    d.rounded_rectangle([80, 290, W - 80, 1000], 40, fill=(70, 140, 255, int(200 * k)))
    d.ellipse([810, 340, 930, 460], fill=SUN)
    kx, ky = 540, 1100
    d.line([(80, 1160), (1000, 1160)], fill=(120, 200, 120), width=10)
    kid(d, kx, ky + 50, 0.9)
    import random
    rnd = random.Random(3)
    for j in range(14):
        sx, sy = rnd.randint(140, 940), rnd.randint(330, 900)
        f = clamp((t * 1.2 - j * 0.07) % 1.0)
        x = sx + (kx - sx) * f
        y = sy + (ky - 70 - sy) * f
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(200, 225, 255))
    if t > 1.0:
        text_c(d, (540, 600), "blue from every direction", font(54, "bold"), WHITE, stroke_width=5, stroke_fill=DARK)


def s5(img, d, t, T, th):
    # sunset: low sun, long path through air
    d.rounded_rectangle([80, 290, W - 80, 1000], 40, fill=(255, 140, 70, 90))
    d.pieslice([140, 700, 380, 940], 180, 360, fill=(255, 120, 60))
    d.line([(80, 820), (1000, 820)], fill=(255, 255, 255, 120), width=4)
    kid(d, 880, 900, 0.8)
    k = ease(prog(t, 0.2, 1.0))
    d.line([(380, 790), (380 + 440 * k, 790)], fill=(255, 150, 70), width=12)
    for j in range(5):
        x = 420 + j * 85
        if x < 380 + 440 * k:
            d.line([(x, 780), (x - 20, 700 - j * 10)], fill=BLUE + (200,), width=6)
    if k >= 1:
        text_c(d, (560, 430), "long path through air", font(50, "semi"), WHITE)
        text_c(d, (560, 520), "blue scattered away", font(52, "bold"), (150, 195, 255), stroke_width=5, stroke_fill=DARK)
    if t > 1.8:
        text_c(d, (540, 1090), "orange & red reach you", font(56, "bold"), (255, 170, 90), stroke_width=5,
               stroke_fill=DARK)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 340, W - 90, 1060], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    sun(d, 540, 520, int(80 * g) + 1)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "Blue sky =", font(int(70 * g2) + 1, "bold"), BLUE)
        text_c(d, (540, 870), "sunlight, scattered", font(int(66 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 970), "by air", font(int(50 * g2) + 1, "semi"), WHITE)


SCENES = [
    dict(say="Sunlight looks white. So why is the sky blue?", draw=s1),
    dict(say="White light is a mix of all the rainbow colours.", draw=s2),
    dict(say="Tiny air particles scatter blue light far more than red.", draw=s3),
    dict(say="So scattered blue reaches your eyes from every part of the sky.", draw=s4),
    dict(say="At sunset, light crosses more air. Blue gets scattered away, leaving orange and red.", draw=s5),
    dict(say="A blue sky is just sunlight, bouncing off air.", draw=s6),
]
