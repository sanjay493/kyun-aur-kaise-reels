from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Is saying no to a friend mean?"
WHITE, DARK = (255, 255, 255), (30, 20, 45)
SKIN2, HAIR2, SHIRT2 = (200, 145, 105), (45, 30, 25), (120, 200, 255)


def friend(d, cx, cy, s=1.0, mood="ask"):
    r = 80 * s
    d.rounded_rectangle([cx - 100 * s, cy + 60 * s, cx + 100 * s, cy + 230 * s], 50 * s, fill=SHIRT2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKIN2)
    d.chord([cx - r - 4 * s, cy - r - 10 * s, cx + r + 4 * s, cy + r * 0.5], 180, 360, fill=HAIR2)
    for ex in (-28, 28):
        x = cx + ex * s
        d.ellipse([x - 9 * s, cy - 6 * s, x + 9 * s, cy + 12 * s], fill=(30, 30, 30))
    if mood == "ask":
        d.arc([cx - 25 * s, cy + 22 * s, cx + 25 * s, cy + 55 * s], 0, 180, fill=(110, 40, 50), width=int(6 * s))
    elif mood == "grumble":
        d.line([(cx - 22 * s, cy + 45 * s), (cx + 22 * s, cy + 40 * s)], fill=(110, 40, 50), width=int(6 * s))
    else:  # ok
        d.chord([cx - 28 * s, cy + 20 * s, cx + 28 * s, cy + 60 * s], 0, 180, fill=(110, 40, 50))


def bubble(d, x, y, w, h, text, f, fill=WHITE, ink=DARK, tail="left"):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 36, fill=fill)
    tx = x - w / 2 + 60 if tail == "left" else x + w / 2 - 60
    d.polygon([(tx - 20, y + h / 2 - 2), (tx + 20, y + h / 2 - 2), (tx, y + h / 2 + 40)], fill=fill)
    text_c(d, (x, y), text, f, ink, align="center")


def notebook(d, cx, cy, s=1.0):
    d.rounded_rectangle([cx - 110 * s, cy - 75 * s, cx + 110 * s, cy + 75 * s], 12, fill=(250, 245, 230),
                        outline=(160, 120, 80), width=5)
    for k in range(4):
        y = cy - 40 * s + k * 26 * s
        d.line([(cx - 85 * s, y), (cx + 85 * s, y)], fill=(120, 150, 220), width=3)
    text_c(d, (cx, cy - 100 * s), "HOMEWORK", font(int(30 * s), "bold"), WHITE)


def s1(img, d, t, T, th):
    friend(d, 300, 720, 1.1)
    g = pop(prog(t, 0.2, 0.4))
    if g > 0:
        bubble(d, 560, 420, 600 * g + 1, 180 * g + 1, "Send me your\nanswers? Again? :)", font(int(48 * g) + 1, "bold"))
    notebook(d, 780, 790, 1.0)
    if t > 1.6:
        g2 = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1110), "Is saying no mean?", font(int(68 * g2) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    g = ease(prog(t, 0.1, 0.5))
    d.rounded_rectangle([110, 400, 510, 760], 40, fill=(255, 255, 255, int(40 * g)), outline=th["accent"], width=5)
    text_c(d, (310, 520), "NO to the", font(52, "bold"), WHITE)
    text_c(d, (310, 620), "request", font(60, "bold"), th["accent"])
    if t > 0.9:
        g2 = ease(prog(t, 0.9, 0.5))
        d.rounded_rectangle([570, 400, 970, 760], 40, fill=(255, 255, 255, int(40 * g2)), outline=th["soft"], width=5)
        text_c(d, (770, 520), "NOT to the", font(52, "bold"), WHITE)
        text_c(d, (770, 620), "friend", font(60, "bold"), th["soft"])
    if t > 1.6:
        text_c(d, (540, 950), "two different things", font(58, "bold"), WHITE)


def s3(img, d, t, T, th):
    friend(d, 840, 820, 0.9)
    g = pop(prog(t, 0.2, 0.4))
    if g > 0:
        bubble(d, 480, 420, 760 * g + 1, 150 * g + 1, "\"I can't share my answers...\"", font(int(46 * g) + 1, "bold"),
               fill=th["accent"], tail="left")
    g2 = pop(prog(t, 1.4, 0.4))
    if g2 > 0:
        bubble(d, 480, 650, 760 * g2 + 1, 150 * g2 + 1, "\"...but I can explain the sum.\"",
               font(int(46 * g2) + 1, "bold"), fill=WHITE, tail="left")
    if t > 2.2:
        text_c(d, (400, 1000), "kind + clear", font(64, "bold"), th["accent"])


def s4(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.6))
    long_txt = ["Actually my mummy said...", "and my tuition sir...", "and also the wifi..."]
    for i, s in enumerate(long_txt):
        y = 400 + i * 110
        d.text((160, y), s, font=font(46, "semi"), fill=(255, 255, 255, int(255 * (1 - 0.6 * k))), anchor="lm")
    if k > 0:
        d.line([(140, 340), (940, 680)], fill=(255, 90, 110), width=int(10 * k) + 1)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([220, 820, 860, 960], 40, fill=th["accent"])
        text_c(d, (540, 890), "short is fine", font(int(64 * g) + 1, "bold"), DARK)


def s5(img, d, t, T, th):
    friend(d, 270, 760, 1.0, mood="grumble")
    text_c(d, (270, 560), "Pleeease?", font(46, "bold"), WHITE)
    for i in range(2):
        g = pop(prog(t, 0.3 + i * 0.9, 0.4))
        if g > 0:
            bubble(d, 700, 430 + i * 210, 520 * g + 1, 130 * g + 1, "\"Sorry, I can't.\"", font(int(46 * g) + 1, "bold"),
                   fill=th["accent"], tail="right")
    if t > 1.8:
        text_c(d, (540, 1110), "same words, same kindness", font(50, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    friend(d, 540, 520, 0.9, mood="ok")
    g = pop(prog(t, 0.3, 0.45))
    text_c(d, (540, 860), "Say no,", font(int(78 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 970), "stay a good friend", font(int(70 * g) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your friend wants to copy your homework, again. Is saying no mean?", draw=s1),
    dict(say="No. Saying no to a request isn't saying no to the friend.", draw=s2),
    dict(say="Try a kind, clear no. I can't share my answers, but I can explain the sum.",
         show="Try a kind, clear no: \"I can't share my answers, but I can explain the sum.\"", draw=s3),
    dict(say="Keep it short. You don't owe a long excuse.", draw=s4),
    dict(say="If they push, repeat it calmly. Same words, same kindness.", draw=s5),
    dict(say="You can say no and still be a good friend.", draw=s6),
]
