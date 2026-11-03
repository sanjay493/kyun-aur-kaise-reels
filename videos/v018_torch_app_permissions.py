import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Why does a torch app want your contacts?"
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)
BEAM = (255, 240, 170)


def phone(d, cx, cy, s=1.0, screen=(235, 240, 250)):
    w, h = 400 * s, 720 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 50 * s, fill=DARK, outline=(200, 210, 230),
                        width=6)
    d.rounded_rectangle([cx - w / 2 + 18 * s, cy - h / 2 + 44 * s, cx + w / 2 - 18 * s, cy + h / 2 - 44 * s],
                        28 * s, fill=screen)
    return w, h


def torch_icon(d, x, y, s=1.0, on=True):
    if on:
        d.polygon([(x - 30 * s, y - 60 * s), (x + 30 * s, y - 60 * s), (x + 110 * s, y - 230 * s),
                   (x - 110 * s, y - 230 * s)], fill=BEAM + (150,))
    d.rounded_rectangle([x - 40 * s, y - 70 * s, x + 40 * s, y - 40 * s], 8, fill=(250, 200, 60))
    d.rounded_rectangle([x - 28 * s, y - 45 * s, x + 28 * s, y + 80 * s], 12, fill=(80, 90, 110))
    d.ellipse([x - 10 * s, y + 5 * s, x + 10 * s, y + 25 * s], fill=RED)


def dialog(d, cx, cy, s, msg, th, glow=0.0):
    d.rounded_rectangle([cx - 195 * s, cy - 120 * s, cx + 195 * s, cy + 120 * s], 26 * s, fill=WHITE,
                        outline=th["accent"] if glow else (200, 205, 215), width=int(4 + 4 * glow))
    for i, line in enumerate(msg):
        text_c(d, (cx, cy - 70 * s + i * 40 * s), line, font(int(30 * s), "bold"), DARK)
    for j, (lb, col) in enumerate((("Don't allow", (90, 100, 120)), ("Allow", (40, 120, 220)))):
        bx = cx - 95 * s + j * 190 * s
        text_c(d, (bx, cy + 75 * s), lb, font(int(28 * s), "bold"), col)


def s1(img, d, t, T, th):
    w, h = phone(d, 540, 720, 1.1, screen=(30, 36, 55))
    torch_icon(d, 540, 900, 1.2, on=True)
    g = pop(prog(t, 0.5, 0.4))
    if g > 0:
        dialog(d, 540, 560, 1.05 * g + 0.01, ["Allow TORCH to", "access your", "contacts?"], th, glow=1.0)
    if t > 1.6:
        text_c(d, (540, 1160), "Why would a torch need that?", font(54, "bold"), th["accent"], stroke_width=4,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.0, 0.35))
    text_c(d, (540, 440), "It doesn't.", font(int(120 * g) + 1, "bold"), RED, stroke_width=6, stroke_fill=DARK)
    torch_icon(d, 360, 900, 1.0, on=True)
    text_c(d, (620, 800), "light: yes", font(60, "bold"), GREEN, anchor="lm")
    if t > 0.8:
        text_c(d, (620, 920), "contacts: no", font(60, "bold"), RED, anchor="lm")


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "Mumbai cyber police warn:", font(52, "bold"), th["soft"])
    asks = [("📇", "contacts"), ("🎤", "microphone"), ("📍", "location"), ("🗂", "storage")]
    torch_icon(d, 200, 760, 1.0, on=False)
    for i, (ic, lb) in enumerate(asks):
        g = pop(prog(t, 0.3 + i * 0.3, 0.35))
        if g > 0:
            y = 500 + i * 140
            d.rounded_rectangle([330, y - 50, 930, y + 50], 26, fill=(255, 255, 255, 45), outline=RED, width=4)
            text_c(d, (370, y), lb, font(int(50 * g) + 1, "bold"), WHITE, anchor="lm")
            text_c(d, (890, y), "?", font(int(56 * g) + 1, "bold"), RED)
    if t > 1.7:
        text_c(d, (540, 1110), "apps asking for what they don't need", font(42, "bold"), th["accent"])


def s4(img, d, t, T, th):
    phone(d, 540, 720, 0.95, screen=(30, 36, 55))
    dialog(d, 540, 700, 1.0, ["Allow APP to", "access your", "photos?"], th)
    # thumb tapping Allow repeatedly
    tap = (t * 2.2) % 1.0
    tx, ty = 625, 790 + 30 * abs(math.sin(tap * math.pi))
    d.ellipse([tx - 45, ty, tx + 45, ty + 120], fill=(210, 160, 120), outline=(160, 110, 80), width=3)
    text_c(d, (540, 1150), "tap, tap, ALLOW…", font(56, "bold"), th["accent"])


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    d.rounded_rectangle([90, 320, W - 90, 640], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 420), "Before you tap Allow, ask:", font(int(48 * g) + 1, "semi"), th["soft"])
    text_c(d, (540, 530), "Does it NEED this?", font(int(70 * g) + 1, "bold"), WHITE)
    rows = [("light for the torch: YES", True), ("your contacts: NO", False)]
    for i, (lb, ok) in enumerate(rows):
        g2 = pop(prog(t, 0.8 + i * 0.5, 0.35))
        if g2 > 0:
            y = 780 + i * 150
            d.rounded_rectangle([130, y - 55, 950, y + 55], 30, fill=GREEN if ok else RED)
            text_c(d, (540, y), lb, font(int(48 * g2) + 1, "bold"), WHITE)


def s6(img, d, t, T, th):
    text_c(d, (540, 340), "Settings › Apps › Permissions", font(46, "bold"), th["soft"])
    items = ["Contacts", "Location", "Microphone"]
    for i, lb in enumerate(items):
        y = 500 + i * 150
        d.rounded_rectangle([150, y - 55, 930, y + 55], 28, fill=(255, 255, 255, 40))
        text_c(d, (200, y), lb, font(50, "bold"), WHITE, anchor="lm")
        k = ease(prog(t, 0.4 + i * 0.4, 0.3))
        kx = 800 + 70 * (1 - k)
        d.rounded_rectangle([760, y - 30, 900, y + 30], 30, fill=tuple(int(a * (1 - k) + b * k) for a, b in
                                                                         zip(GREEN, (110, 115, 130))))
        d.ellipse([kx - 26, y - 26, kx + 26, y + 26], fill=WHITE)
    if t > 1.8:
        text_c(d, (540, 1000), "Don't allow", font(70, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)
        text_c(d, (540, 1100), "change it anytime", font(48, "semi"), WHITE)


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 580), "Your data,", font(int(100 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 760), "your permission.", font(int(90 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="A torch app asks to read your contacts. Why would a torch need that?", draw=s1),
    dict(say="It doesn't. Contacts have nothing to do with light.", draw=s2),
    dict(say="Mumbai cyber police have warned about apps asking for permissions they don't need.", draw=s3),
    dict(say="Many of us just tap Allow without reading.", draw=s4),
    dict(say="Before you allow, ask: does this app need it?", draw=s5),
    dict(say="If not, tap Don't allow. You can change it anytime in Settings.", draw=s6),
    dict(say="Your data, your permission.", draw=s7),
]
