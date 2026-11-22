import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Why does your voice crack?"
WHITE, DARK = (255, 255, 255), (40, 20, 40)
SKIN, SKIN2 = (235, 185, 145), (195, 145, 110)
BOX, WAVE, CRACK = (255, 200, 110), (120, 200, 255), (255, 110, 110)
GREEN = (110, 220, 140)


def head_neck(d, x, y, apple=0.0):
    """Side view: head and neck facing right; `apple` (0-1) grows the bump at the throat."""
    d.ellipse([x - 150, y - 300, x + 150, y], fill=SKIN)
    d.rectangle([x - 70, y - 60, x + 60, y + 260], fill=SKIN)
    d.polygon([(x + 130, y - 120), (x + 175, y - 90), (x + 130, y - 70)], fill=SKIN)  # nose
    d.ellipse([x + 50, y - 200, x + 80, y - 170], fill=DARK)  # eye
    d.chord([x - 160, y - 320, x + 150, y - 120], 180, 360, fill=(45, 30, 30))  # hair
    if apple > 0:
        r = 18 + 22 * apple
        d.ellipse([x + 60 - r * 0.6, y + 90 - r, x + 60 + r * 0.6, y + 90 + r], fill=SKIN, outline=SKIN2, width=3)


def voice_box(d, x, y, s=1.0, col=BOX):
    w, h = 70 * s, 90 * s
    d.rounded_rectangle([x - w, y - h, x + w, y + h], int(26 * s), fill=col, outline=WHITE, width=4)
    for i in range(3):
        yy = y - h * 0.5 + i * h * 0.5
        d.line([(x - w * 0.6, yy), (x + w * 0.6, yy)], fill=(200, 140, 60), width=int(6 * s) + 1)


def wave(d, x0, x1, y, t, amp, freq, col, crack_at=None):
    pts = []
    for i in range(80):
        x = x0 + (x1 - x0) * i / 79
        a = amp
        f = freq
        if crack_at is not None and abs(i / 79 - crack_at) < 0.08:
            a, f = amp * 1.8, freq * 3.2
        pts.append((x, y + a * math.sin(f * i / 79 * 2 * math.pi + t * 8)))
    d.line(pts, fill=col, width=8)


def s1(img, d, t, T, th):
    text_c(d, (540, 350), "Mid-sentence...", font(58, "bold"), WHITE)
    wave(d, 140, 940, 620, t, 40, 4, WAVE, crack_at=0.6 if t > 0.8 else None)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        text_c(d, (640, 500), "SQUEAK!", font(int(70 * g) + 1, "bold"), CRACK)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([200, 860, 880, 1000], 50, fill=th["accent"])
        text_c(d, (540, 930), "What just happened?", font(int(54 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "At puberty", font(60, "bold"), th["accent"])
    g = 0.6 + 0.4 * ease(prog(t, 0.4, 1.4))
    voice_box(d, 540, 680, 1.4 * g)
    if t > 0.8:
        text_c(d, (540, 950), "the voice box grows", font(56, "bold"), WHITE)
        text_c(d, (540, 1040), "(larynx)", font(46, "semi"), th["soft"])


def s3(img, d, t, T, th):
    head_neck(d, 470, 700, ease(prog(t, 0.3, 1.0)))
    if t > 1.0:
        k = ease(prog(t, 1.0, 0.5))
        d.line([(725, 790), (570, 790)], fill=th["accent"], width=8)
        d.polygon([(570, 775), (570, 805), (545, 790)], fill=th["accent"])
        text_c(d, (740, 790), "Adam's apple", font(42, "bold"), th["accent"], anchor="lm")
    text_c(d, (540, 350), "Bigger in boys", font(60, "bold"), WHITE)
    if t > 1.6:
        wave(d, 160, 920, 1060, t, 30, 2, WAVE)
        text_c(d, (540, 1140), "deeper voice", font(40, "semi"), th["soft"])


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "While it grows...", font(58, "bold"), WHITE)
    sh = 6 * math.sin(t * 30)
    voice_box(d, 540 + sh, 600, 1.2)
    wave(d, 140, 940, 880, t, 36, 3, WAVE, crack_at=(t * 0.4) % 1)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([170, 1000, 910, 1120], 50, fill=CRACK)
        text_c(d, (540, 1060), "cracks or sounds hoarse", font(int(50 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Days or weeks", font(62, "bold"), th["accent"])
    k = ease(prog(t, 0.3, 1.4))
    wave(d, 140, 940, 620, t, 34, 3, WAVE, crack_at=None if k > 0.6 else 0.5)
    if k > 0.6:
        g = pop(prog(t, 1.2, 0.4))
        text_c(d, (540, 760), "then it settles", font(int(60 * g) + 1, "bold"), GREEN)
    if t > 1.8:
        text_c(d, (540, 950), "Many boys go through it,", font(46, "bold"), WHITE)
        text_c(d, (540, 1020), "at different ages.", font(46, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Not a flaw.", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 680), "Just a voice box", font(int(66 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 780), "growing up.", font(int(66 * g2) + 1, "bold"), th["accent"])
        voice_box(d, 540, 950, 0.7)


SCENES = [
    dict(say="Your voice suddenly squeaks mid-sentence. What just happened?", draw=s1),
    dict(say="At puberty, your voice box, the larynx, starts to grow.", draw=s2),
    dict(say="In boys it grows bigger, showing as the Adam's apple. Voices get deeper.", draw=s3),
    dict(say="While it grows, its muscles sometimes lose control. The voice cracks or turns hoarse.", draw=s4),
    dict(say="This lasts days or weeks, then settles. Many boys go through it, at different ages.", draw=s5),
    dict(say="Not a flaw. Just a voice box growing up.", draw=s6),
]
