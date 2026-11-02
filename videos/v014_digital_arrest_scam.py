import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Can police arrest you on a video call?"
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)
KHAKI = (190, 165, 110)


def phone(d, cx, cy, s=1.0, shake=0.0, screen=(235, 240, 250)):
    cx += shake
    w, h = 340 * s, 620 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 46 * s, fill=DARK, outline=(200, 210, 230),
                        width=6)
    d.rounded_rectangle([cx - w / 2 + 16 * s, cy - h / 2 + 40 * s, cx + w / 2 - 16 * s, cy + h / 2 - 40 * s], 26 * s,
                        fill=screen)
    return cx, cy, w, h


def fake_cop(d, x, y, s=1.0, grin=False):
    d.rounded_rectangle([x - 80 * s, y + 60 * s, x + 80 * s, y + 190 * s], 30 * s, fill=KHAKI)
    d.ellipse([x - 55 * s, y - 50 * s, x + 55 * s, y + 60 * s], fill=(215, 165, 125))
    d.rectangle([x - 62 * s, y - 70 * s, x + 62 * s, y - 35 * s], fill=(60, 70, 110))  # cap
    d.rectangle([x - 75 * s, y - 40 * s, x + 75 * s, y - 30 * s], fill=(40, 45, 80))
    d.ellipse([x - 10 * s, y - 64 * s, x + 10 * s, y - 44 * s], fill=(255, 210, 80))
    for ex in (-20, 20):
        d.line([x + (ex - 10) * s, y - 4 * s, x + (ex + 10) * s, y + 2 * s], fill=DARK, width=int(5 * s))
    if grin:
        d.arc([x - 25 * s, y + 10 * s, x + 25 * s, y + 40 * s], 10, 170, fill=DARK, width=int(5 * s))
    else:
        d.line([x - 22 * s, y + 30 * s, x + 22 * s, y + 30 * s], fill=DARK, width=int(5 * s))


def s1(img, d, t, T, th):
    shake = math.sin(t * 40) * 6 if (t % 1.2) < 0.5 else 0
    cx, cy, w, h = phone(d, 540, 640, 1.0, shake, screen=(40, 50, 70))
    fake_cop(d, cx, cy - 60, 1.2)
    d.ellipse([cx + 110, cy - 270, cx + 130, cy - 250], fill=RED)  # recording dot
    text_c(d, (cx, cy + 210), "VIDEO CALL", font(30, "bold"), WHITE)
    g = pop(prog(t, 0.9, 0.4))
    if g > 0:
        d.rounded_rectangle([110, 990, 970, 1130], 30, fill=(255, 255, 255, 245), outline=RED, width=6)
        text_c(d, (540, 1060), "\"You are under DIGITAL ARREST\"", font(int(44 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.0, 0.35))
    sz = int(200 * (2.0 - 1.0 * g))
    f = font(max(sz, 10), "bold")
    tw = d.textlength("NO", font=f)
    d.rounded_rectangle([W / 2 - tw / 2 - 60, 520 - sz * 0.6, W / 2 + tw / 2 + 60, 520 + sz * 0.6], 30,
                        outline=RED, width=14)
    text_c(d, (540, 520), "NO", f, RED)
    if t > 0.6:
        text_c(d, (540, 820), "no such thing as", font(58, "semi"), WHITE)
        text_c(d, (540, 920), "\"digital arrest\"", font(70, "bold"), th["accent"])
        text_c(d, (540, 1020), "in Indian law", font(58, "semi"), WHITE)


def s3(img, d, t, T, th):
    labels = ["\"POLICE\"", "\"CBI\"", "\"CUSTOMS\""]
    for i, lb in enumerate(labels):
        g = pop(prog(t, 0.1 + i * 0.3, 0.35))
        if g > 0:
            x = 230 + i * 310
            fake_cop(d, x, 520, 0.9 * g + 0.01, grin=t > 1.8)
            text_c(d, (x, 380), lb, font(int(40 * g) + 1, "bold"), th["accent"])
    k = ease(prog(t, 1.2, 0.6))
    if k > 0:
        # a mask slipping to show it's a costume
        d.rounded_rectangle([160, 800, 920, 900], 30, fill=(255, 255, 255, int(40 * k)))
        text_c(d, (540, 850), "really: scammers in costume", font(48, "bold"), WHITE)
        cx, cy, w, h = phone(d, 330, 1040, 0.25, screen=(40, 50, 70))
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED)
        text_c(d, (420, 1040), "\"stay on camera\"", font(40, "semi"), th["soft"], anchor="lm")


def s4(img, d, t, T, th):
    cx, cy, w, h = phone(d, 540, 620, 0.9, screen=(40, 50, 70))
    fake_cop(d, cx, cy - 80, 1.0, grin=False)
    g = pop(prog(t, 0.2, 0.4))
    if g > 0:
        d.rounded_rectangle([cx - 140, cy + 90, cx + 140, cy + 200], 20, fill=RED)
        text_c(d, (cx, cy + 145), "PAY ₹₹₹", font(int(52 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        text_c(d, (540, 1080), "scare first, then money", font(66, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    d.rounded_rectangle([90, 300, W - 90, 680], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 400), "Real officers", font(int(60 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 490), "NEVER arrest", font(int(64 * g) + 1, "bold"), RED)
    text_c(d, (540, 580), "on a video call", font(int(60 * g) + 1, "bold"), WHITE)
    steps = [("✂", "Cut the call"), ("👪", "Tell an adult"), ("1930", "Report it")]
    for i, (ic, lb) in enumerate(steps):
        g2 = pop(prog(t, 0.9 + i * 0.6, 0.35))
        if g2 > 0:
            y = 760 + i * 130
            d.rounded_rectangle([170, y - 52, 910, y + 52], 30, fill=th["accent"] if i == 2 else (255, 255, 255, 50))
            col = DARK if i == 2 else WHITE
            text_c(d, (240, y), str(i + 1), font(int(54 * g2) + 1, "bold"), col)
            text_c(d, (310, y), lb + (" on 1930" if i == 2 else ""), font(int(50 * g2) + 1, "bold"), col, anchor="lm")


SCENES = [
    dict(say="A 'police officer' on a video call says you're under digital arrest. Real?",
         show="A \"police officer\" on a video call says you're under digital arrest. Real?", draw=s1),
    dict(say="No. There is no such thing as a digital arrest in Indian law.", draw=s2),
    dict(say="Scammers pose as police, C.B.I. or customs officers and keep you on camera.",
         show="Scammers pose as police, CBI or customs officers and keep you on camera.", draw=s3),
    dict(say="They scare you, then demand money.", draw=s4),
    dict(say="Real officers never arrest anyone on video calls. Cut the call, tell an adult, report it on one nine three zero.",
         show="Real officers never arrest anyone on video calls. Cut the call, tell an adult, report it on 1930.",
         draw=s5),
]
