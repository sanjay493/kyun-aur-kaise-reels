import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Nervous before speaking? Try this"
WHITE, DARK = (255, 255, 255), (30, 20, 45)
RED, BLUE, GOLD = (255, 95, 120), (120, 190, 255), (255, 205, 90)


def heart(d, x, y, s):
    d.ellipse([x - 60 * s, y - 50 * s, x + 4 * s, y + 14 * s], fill=RED)
    d.ellipse([x - 4 * s, y - 50 * s, x + 60 * s, y + 14 * s], fill=RED)
    d.polygon([(x - 58 * s, y - 6 * s), (x + 58 * s, y - 6 * s), (x, y + 70 * s)], fill=RED)


def mic(d, x, y):
    d.rounded_rectangle([x - 40, y - 90, x + 40, y + 30], 40, fill=(200, 205, 220), outline=WHITE, width=4)
    d.line([(x, y + 30), (x, y + 200)], fill=(200, 205, 220), width=12)
    d.line([(x - 70, y + 200), (x + 70, y + 200)], fill=(200, 205, 220), width=12)


def bubble(d, x, y, w, h, text, f, fill=WHITE, ink=DARK):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 36, fill=fill)
    d.polygon([(x - 20, y + h / 2 - 2), (x + 20, y + h / 2 - 2), (x - 40, y + h / 2 + 40)], fill=fill)
    text_c(d, (x, y), text, f, ink, align="center")


def s1(img, d, t, T, th):
    # stage: mic, beating heart
    d.rounded_rectangle([140, 960, 940, 1010], 20, fill=(255, 255, 255, 50))
    mic(d, 700, 700)
    beat = 1 + 0.12 * abs(math.sin(t * 7))
    heart(d, 340, 560, beat)
    text_c(d, (340, 400), "ASSEMBLY", font(44, "bold"), th["soft"])
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        bubble(d, 540, 1050, 520 * g + 1, 100 * g + 1, "\"Calm down!\"", font(int(54 * g) + 1, "bold"))


def s2(img, d, t, T, th):
    for i, (lab, col) in enumerate([("NERVOUS", BLUE), ("EXCITED", GOLD)]):
        x = 300 + i * 480
        g = pop(prog(t, 0.1 + 0.6 * i, 0.4))
        d.rounded_rectangle([x - 200, 380, x + 200, 900], 40, fill=(255, 255, 255, 35), outline=col, width=6)
        text_c(d, (x, 450), lab, font(int(54 * g) + 1, "bold"), col)
        heart(d, x, 600, (1 + 0.12 * abs(math.sin(t * 7))) * g)
        text_c(d, (x, 780), "fast heartbeat", font(36, "semi"), WHITE)
        text_c(d, (x, 830), "high energy", font(36, "semi"), WHITE)
    if t > 1.6:
        text_c(d, (540, 1040), "feel alike", font(68, "bold"), th["accent"])


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "HARVARD STUDY", font(46, "bold"), th["soft"])
    for i, (said, col) in enumerate([("\"I'm calm\"", BLUE), ("\"I'm excited\"", GOLD)]):
        x = 300 + i * 480
        g = pop(prog(t, 0.2 + 0.5 * i, 0.4))
        d.rounded_rectangle([x - 210, 420, x + 210, 820], 40, fill=(255, 255, 255, 35), outline=col, width=6)
        mic(d, x, 600) if g > 0.5 else None
        text_c(d, (x, 470), said, font(int(46 * g) + 1, "bold"), col)
    if t > 1.8:
        g2 = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([560, 860, 1000, 980], 40, fill=GOLD)
        text_c(d, (780, 920), "more persuasive", font(int(46 * g2) + 1, "bold"), DARK)
        text_c(d, (540, 1060), "speeches judged by raters", font(40, "semi"), WHITE)


def s4(img, d, t, T, th):
    # an arrow from NERVOUS to EXCITED is short; to CALM is long and uphill
    d.rounded_rectangle([110, 460, 450, 580], 40, fill=BLUE)
    text_c(d, (280, 520), "nervous", font(52, "bold"), DARK)
    k = ease(prog(t, 0.3, 0.7))
    d.rounded_rectangle([630, 460, 970, 580], 40, fill=(GOLD[0], GOLD[1], GOLD[2], int(255 * k)))
    text_c(d, (800, 520), "excited", font(52, "bold"), DARK)
    d.line([(460, 520), (460 + 160 * k, 520)], fill=WHITE, width=10)
    if t > 1.2:
        g = ease(prog(t, 1.2, 0.6))
        d.rounded_rectangle([370, 840, 710, 960], 40, fill=(255, 255, 255, int(120 * g)))
        text_c(d, (540, 900), "calm", font(52, "bold"), DARK)
        for i in range(8):  # long dashed path down to "calm"
            a, b = i / 8, (i + 0.5) / 8
            d.line([(280 + (540 - 280) * a, 590 + (830 - 590) * a), (280 + (540 - 280) * b, 590 + (830 - 590) * b)],
                   fill=th["soft"], width=6)
        text_c(d, (540, 1050), "excited may be the easier switch", font(46, "bold"), th["accent"])


def s5(img, d, t, T, th):
    mic(d, 300, 720)
    g = pop(prog(t, 0.6, 0.45))
    if g > 0:
        bubble(d, 680, 520, 520 * g + 1, 170 * g + 1, "\"I'm\nexcited!\"", font(int(66 * g) + 1, "bold"), fill=GOLD)
    if t > 1.4:
        text_c(d, (680, 900), "say it out loud", font(52, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    heart(d, 540, 540, 1.3 + 0.12 * abs(math.sin(t * 7)))
    g = pop(prog(t, 0.3, 0.45))
    text_c(d, (540, 820), "Same racing heart.", font(int(64 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 930), "New name.", font(int(76 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Heart racing before you speak in assembly? Everyone says, calm down.",
         show="Heart racing before you speak in assembly? Everyone says, \"Calm down.\"", draw=s1),
    dict(say="But nervousness and excitement feel alike: fast heartbeat, high energy.", draw=s2),
    dict(say="In a Harvard study, people who said I'm excited before a speech were rated more persuasive than those who said I'm calm.",
         show="In a Harvard study, people who said \"I'm excited\" before a speech were rated more persuasive than those who said \"I'm calm\".",
         draw=s3),
    dict(say="Turning nerves into excitement may be easier than forcing calm.", draw=s4),
    dict(say="So next time, say it out loud: I'm excited.", show="So next time, say it out loud: \"I'm excited.\"", draw=s5),
    dict(say="Same racing heart, new name.", draw=s6),
]
