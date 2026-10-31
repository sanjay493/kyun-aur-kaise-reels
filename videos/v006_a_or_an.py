import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Why 'an hour' but 'a university'?"
WHITE, DARK, BLUE, PINK, GREY = (255, 255, 255), (35, 25, 30), (110, 180, 255), (255, 130, 160), (160, 150, 160)


def card(d, cx, cy, art, word, g, art_col, hi=None, w=820, h=200):
    """Word card: article + word; hi = (index, colour) of the letter to highlight."""
    if g <= 0: return
    d.rounded_rectangle([cx - w / 2 * g, cy - h / 2 * g, cx + w / 2 * g, cy + h / 2 * g], int(40 * g) + 1,
                        fill=(255, 250, 240))
    if g < 0.9: return
    f = font(92, "bold")
    parts = ([(art + " ", art_col)] if art else [("", art_col)]) + [(ch, DARK) for ch in word]
    if hi: parts[1 + hi[0]] = (word[hi[0]], hi[1])
    tw = sum(d.textlength(p, font=f) for p, _ in parts); x = cx - tw / 2
    span = None
    for k, (p, c) in enumerate(parts):
        if hi and k == 1 + hi[0]: span = (x, x + d.textlength(p, font=f))
        d.text((x, cy), p, font=f, fill=c, anchor="lm"); x += d.textlength(p, font=f)
    return span


def ear(d, cx, cy, s, col):
    d.ellipse([cx - 90 * s, cy - 130 * s, cx + 90 * s, cy + 130 * s], fill=col)
    d.ellipse([cx - 40 * s, cy - 70 * s, cx + 50 * s, cy + 60 * s], fill=(200, 130, 110))
    d.ellipse([cx - 10 * s, cy - 30 * s, cx + 30 * s, cy + 20 * s], fill=col)
    for k in range(3):
        r = (150 + k * 45) * s
        d.arc([cx + 60 * s - r, cy - r, cx + 60 * s + r, cy + r], 330, 30, fill=WHITE + (220 - 60 * k,), width=int(8 * s) + 1)


def s1(img, d, t, T, th):
    card(d, W / 2, 470, "an", "hour", pop(prog(t, 0.1, 0.4)), th["accent"], (0, PINK))
    card(d, W / 2, 760, "a", "university", pop(prog(t, 0.9, 0.4)), th["accent"], (0, BLUE))
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (W / 2, 1020), "H = consonant?  U = vowel?", font(int(52 * g) + 1, "bold"), WHITE,
               stroke_width=4, stroke_fill=DARK)
        text_c(d, (W / 2, 1110), "?", font(int(90 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    ear(d, W / 2, 560, 1.0, (240, 175, 150))
    g = pop(prog(t, 0.4, 0.4))
    if g > 0:
        d.rounded_rectangle([130, 860, W - 130, 1120], 40, fill=(255, 255, 255, 235))
        text_c(d, (W / 2, 935), "first SOUND", font(int(70 * g) + 1, "bold"), (60, 140, 90))
        text_c(d, (W / 2, 1040), "not first letter", font(int(54 * g) + 1, "semi"), (200, 60, 70))
        if g > 0.9:
            d.line([(W / 2 - 220, 1042), (W / 2 + 220, 1042)], fill=(200, 60, 70), width=6)


def s3(img, d, t, T, th):
    span = card(d, W / 2, 450, "", "hour", 1.0, th["accent"], (0, (210, 200, 205)), w=600)
    k = ease(prog(t, 0.3, 0.6))
    if k > 0 and span:  # cross out silent h
        x0, x1 = span[0] - 8, span[1] + 8
        d.line([(x0, 490), (x0 + (x1 - x0) * k, 490 - 90 * k)], fill=(220, 60, 70), width=10)
    if t > 0.8:
        text_c(d, (W / 2, 610), "silent H, sounds like \"our\"", font(46, "semi"), WHITE)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (W / 2, 760), "vowel sound", font(int(60 * g) + 1, "bold"), PINK)
        card(d, W / 2, 960, "an", "hour", g, th["accent"], w=600)


def s4(img, d, t, T, th):
    card(d, W / 2, 450, "", "university", 1.0, th["accent"], (0, BLUE), w=760)
    if t > 0.5:
        g = pop(prog(t, 0.5, 0.4))
        text_c(d, (W / 2, 610), "starts like \"you\"", font(int(56 * g) + 1, "bold"), WHITE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (W / 2, 760), "consonant sound", font(int(60 * g) + 1, "bold"), BLUE)
        card(d, W / 2, 960, "a", "university", g, th["accent"], w=760)


def s5(img, d, t, T, th):
    g1 = pop(prog(t, 0.1, 0.4))
    card(d, W / 2, 450, "an", "MLA", g1, th["accent"], (0, PINK), w=600)
    if g1 > 0.9:
        text_c(d, (W / 2, 590), "\"em-el-ay\"", font(48, "semi"), PINK)
    g2 = pop(prog(t, 1.1, 0.4))
    card(d, W / 2, 790, "a", "one-rupee coin", g2, th["accent"], (0, BLUE), w=900)
    if g2 > 0.9:
        text_c(d, (W / 2, 930), "\"wun\"", font(48, "semi"), BLUE)
        cx, cy = 880, 1080
        d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(205, 205, 215), outline=(140, 140, 150), width=6)
        text_c(d, (cx, cy), "₹1", font(52, "sym"), (80, 80, 95))


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    ear(d, W / 2, 560, 0.9 * g + 0.01, (240, 175, 150))
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        text_c(d, (W / 2, 900), "Don't trust the letter.", font(int(58 * g2) + 1, "bold"), WHITE)
        text_c(d, (W / 2, 1010), "Trust your ears.", font(int(76 * g2) + 1, "bold"), th["accent"],
               stroke_width=5, stroke_fill=DARK)


SCENES = [
    dict(say="Why do we say an hour, but a university?",
         show="Why do we say 'an hour', but 'a university'?", draw=s1),
    dict(say="Here's the secret. A and an follow the first sound, not the first letter.",
         show="Here's the secret. 'A' and 'an' follow the first sound, not the first letter.", draw=s2),
    dict(say="Hour has a silent H. It starts with a vowel sound, so: an hour.",
         show="'Hour' has a silent H. It starts with a vowel sound, so: an hour.", draw=s3),
    dict(say="University starts with a you sound. That's a consonant sound, so: a university.",
         show="'University' starts with a 'you' sound. That's a consonant sound, so: a university.", draw=s4),
    dict(say="That's why it's an M.L.A., but a one rupee coin.",
         show="That's why it's an MLA, but a one-rupee coin.", draw=s5),
    dict(say="Don't trust the letter. Trust your ears.", draw=s6),
]
