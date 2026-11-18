import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Your brain is still under construction"
WHITE, DARK = (255, 255, 255), (40, 20, 40)
BRAIN, BRAIN2 = (255, 180, 200), (220, 130, 160)
PFC, CONE, GREEN = (255, 220, 90), (255, 150, 60), (110, 220, 140)


def brain(d, cx, cy, s=1.0, glow=0.0):
    r = 200 * s
    d.ellipse([cx - r, cy - r * 0.75, cx + r, cy + r * 0.75], fill=BRAIN, outline=BRAIN2, width=6)
    for i in range(-2, 3):
        x = cx + i * r * 0.32
        d.arc([x - r * 0.25, cy - r * 0.5, x + r * 0.25, cy + r * 0.1], 200, 340, fill=BRAIN2, width=6)
        d.arc([x - r * 0.22, cy, x + r * 0.22, cy + r * 0.5], 20, 160, fill=BRAIN2, width=6)
    if glow > 0:  # front part (the viewer's left)
        w = int(4 + 8 * glow)
        d.ellipse([cx - r * 1.0, cy - r * 0.55, cx - r * 0.4, cy + r * 0.35], fill=PFC, outline=WHITE, width=w)


def cone(d, x, y, s=1.0):
    d.polygon([(x, y - 90 * s), (x - 45 * s, y), (x + 45 * s, y)], fill=CONE)
    d.rectangle([x - 32 * s, y - 40 * s, x + 32 * s, y - 28 * s], fill=WHITE)
    d.rectangle([x - 60 * s, y, x + 60 * s, y + 14 * s], fill=CONE)


def s1(img, d, t, T, th):
    brain(d, 540, 640)
    for i, x in enumerate([330, 750]):
        if t > 0.5 + 0.3 * i:
            cone(d, x, 940, pop(prog(t, 0.5 + 0.3 * i, 0.4)))
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 1100), "mid-to-late 20s", font(int(70 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 360), "still developing", font(58, "bold"), WHITE)


def s2(img, d, t, T, th):
    brain(d, 600, 620, 1.0, glow=0.5 + 0.5 * math.sin(t * 4) ** 2)
    text_c(d, (540, 350), "prefrontal cortex", font(58, "bold"), PFC)
    for i, w in enumerate(["plan", "prioritise", "decide"]):
        if t > 0.8 + 0.35 * i:
            g = pop(prog(t, 0.8 + 0.35 * i, 0.4))
            x = 230 + i * 310
            d.rounded_rectangle([x - 135, 900, x + 135, 1000], 40, fill=(255, 255, 255, 40), outline=PFC, width=4)
            text_c(d, (x, 950), w, font(int(46 * g) + 1, "bold"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 360), "Stress can feel different", font(54, "bold"), WHITE)
    # a stress meter swinging
    ang = math.radians(200 + 120 * (0.5 + 0.5 * math.sin(t * 3)))
    cx, cy, r = 540, 800, 240
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=th["soft"], width=24)
    d.line([(cx, cy), (cx + r * 0.85 * math.cos(ang), cy + r * 0.85 * math.sin(ang))], fill=th["accent"], width=14)
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=th["accent"])
    if t > 1.0:
        text_c(d, (540, 940), "brain still developing", font(50, "bold"), th["accent"])


def s4(img, d, t, T, th):
    brain(d, 540, 560, 0.8)
    items = ["a tough subject", "a sport", "music or art"]
    for i, w in enumerate(items):
        if t > 0.5 + 0.35 * i:
            g = pop(prog(t, 0.5 + 0.35 * i, 0.4))
            y = 820 + i * 100
            text_c(d, (540, y), "+ " + w, font(int(52 * g) + 1, "bold"), GREEN)
    text_c(d, (540, 330), "ready to learn & adapt", font(54, "bold"), WHITE)


def s5(img, d, t, T, th):
    steps = [("1", "notice what set it off"), ("2", "try what calms you")]
    for i, (n, lab) in enumerate(steps):
        if t > 0.2 + 0.7 * i:
            g = pop(prog(t, 0.2 + 0.7 * i, 0.4))
            y = 520 + i * 260
            d.rounded_rectangle([110, y - 100, 970, y + 100], 50, fill=(255, 255, 255, 35), outline=th["accent"], width=5)
            d.ellipse([150, y - 55, 260, y + 55], fill=th["accent"])
            text_c(d, (205, y), n, font(60, "bold"), DARK)
            text_c(d, (600, y), lab, font(int(48 * g) + 1, "bold"), WHITE)
    if t > 1.7:
        text_c(d, (540, 1080), "your own way", font(46, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Under construction", font(int(68 * g) + 1, "bold"), WHITE)
    cone(d, 540, 700, 0.9)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 900), "Build it well.", font(int(80 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Surprise: your brain keeps developing till your mid to late twenties.", draw=s1),
    dict(say="The prefrontal cortex, behind your forehead, is one of the last to mature. It helps you plan and decide.", draw=s2),
    dict(say="So teens may respond to stress differently from adults.", draw=s3),
    dict(say="But a growing brain is ready to learn. Tough subjects, sport and music strengthen it.", draw=s4),
    dict(say="Stressed? Notice what set it off, then try what calms you.", draw=s5),
    dict(say="Under construction. Build it well.", draw=s6),
]
