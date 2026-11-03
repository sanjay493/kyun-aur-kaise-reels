from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "Its or it's?"
WHITE, DARK = (255, 255, 255), (30, 22, 40)
RED, GREEN = (240, 90, 90), (90, 210, 130)
FUR, FUR_D = (215, 160, 95), (160, 110, 60)


def dog(d, x, y, s=1.0, wag=0.0):
    # tail (wagging)
    tx = x + 150 * s
    d.line([(tx, y + 10 * s), (tx + 70 * s, y - 70 * s + wag * 30 * s)], fill=FUR_D, width=int(22 * s))
    d.ellipse([x - 150 * s, y - 60 * s, x + 160 * s, y + 90 * s], fill=FUR, outline=FUR_D, width=4)  # body
    for lx in (-110, -40, 60, 120):
        d.rounded_rectangle([x + lx * s - 14 * s, y + 60 * s, x + lx * s + 14 * s, y + 150 * s], 10, fill=FUR_D)
    hx, hy = x - 170 * s, y - 70 * s
    d.ellipse([hx - 80 * s, hy - 75 * s, hx + 80 * s, hy + 75 * s], fill=FUR, outline=FUR_D, width=4)  # head
    d.ellipse([hx - 95 * s, hy - 60 * s, hx - 50 * s, hy + 30 * s], fill=FUR_D)  # ear
    d.ellipse([hx - 30 * s, hy - 25 * s, hx - 10 * s, hy - 5 * s], fill=DARK)  # eye
    d.ellipse([hx - 90 * s, hy + 5 * s, hx - 60 * s, hy + 30 * s], fill=DARK)  # nose
    d.arc([hx - 70 * s, hy + 10 * s, hx - 20 * s, hy + 50 * s], 20, 160, fill=DARK, width=int(5 * s))


def s1(img, d, t, T, th):
    import math
    dog(d, 560, 560, 1.0, math.sin(t * 12))
    d.rounded_rectangle([90, 860, W - 90, 1040], 34, fill=(255, 255, 255, 240))
    text_c(d, (540, 950), "The dog wagged it's tail.", font(58, "bold"), DARK)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        f = font(58, "bold")
        full = "The dog wagged it's tail."
        x0 = 540 - d.textlength(full, font=f) / 2 + d.textlength("The dog wagged ", font=f)
        x1 = x0 + d.textlength("it's", font=f)
        d.ellipse([x0 - 18, 895, x1 + 18, 1005], outline=RED, width=int(8 * g) + 1)
        text_c(d, (540, 1130), "Spot the mistake?", font(int(64 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    text_c(d, (540, 430), "it's", font(int(170 * g) + 1, "bold"), th["accent"], stroke_width=6, stroke_fill=DARK)
    k = ease(prog(t, 0.6, 0.5))
    if k > 0:
        text_c(d, (540, 650), "=", font(100, "bold"), th["soft"])
        d.rounded_rectangle([200, 740, 880, 860], 30, fill=(255, 255, 255, int(50 * k)))
        text_c(d, (540, 800), "it is", font(80, "bold"), WHITE)
    if t > 1.4:
        d.rounded_rectangle([200, 900, 880, 1020], 30, fill=(255, 255, 255, 50))
        text_c(d, (540, 960), "it has", font(80, "bold"), WHITE)


def s3(img, d, t, T, th):
    # "it is" -> the i of "is" flies away, apostrophe drops in
    f = font(130, "bold")
    k = ease(prog(t, 0.4, 0.8))
    text_c(d, (330, 560), "it", f, WHITE)
    text_c(d, (730, 560), "s", f, WHITE)
    # the missing "i"
    text_c(d, (620, 560 - 260 * k), "i", f, (255, 255, 255, int(255 * (1 - k))))
    if k > 0.5:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 520), "'", font(int(200 * g) + 1, "bold"), th["accent"])
    if t > 1.4:
        text_c(d, (540, 850), "apostrophe = missing letters", font(54, "bold"), th["accent"])
        text_c(d, (540, 960), "it is  =  it's", font(64, "bold"), WHITE)


def s4(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    text_c(d, (540, 380), "its", font(int(150 * g) + 1, "bold"), GREEN, stroke_width=6, stroke_fill=DARK)
    text_c(d, (540, 520), "= belonging to it", font(58, "bold"), WHITE)
    words = ["his", "her", "its"]
    for i, w in enumerate(words):
        g2 = pop(prog(t, 0.8 + i * 0.35, 0.35))
        if g2 > 0:
            x = 230 + i * 310
            d.rounded_rectangle([x - 120, 660, x + 120, 800], 30, fill=(255, 255, 255, 50),
                                outline=GREEN if i == 2 else th["soft"], width=5)
            text_c(d, (x, 730), w, font(int(76 * g2) + 1, "bold"), WHITE)
    if t > 2.0:
        text_c(d, (540, 920), "no apostrophe", font(64, "bold"), th["accent"])


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "Quick test:", font(60, "bold"), th["soft"])
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([140, 430, 940, 600], 40, fill=th["accent"])
    text_c(d, (540, 515), "say \"it is\"", font(int(80 * g) + 1, "bold"), DARK)
    if t > 1.0:
        text_c(d, (540, 740), "still makes sense?", font(60, "bold"), WHITE)
        text_c(d, (540, 870), "Yes? Write it's", font(70, "bold"), GREEN)


def s6(img, d, t, T, th):
    import math
    dog(d, 560, 470, 0.7, math.sin(t * 12))
    d.rounded_rectangle([70, 700, W - 70, 830], 30, fill=(255, 255, 255, 230))
    text_c(d, (540, 765), "The dog wagged it is tail?", font(50, "bold"), DARK)
    if t > 0.9:
        d.line([(110, 765), (W - 110, 765)], fill=RED, width=8)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        d.rounded_rectangle([70, 900, W - 70, 1040], 30, fill=GREEN)
        text_c(d, (540, 970), "The dog wagged its tail.", font(int(52 * g) + 1, "bold"), DARK)


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 520), "it's", font(int(150 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 690), "=", font(int(90 * g) + 1, "bold"), th["soft"])
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 860), "it is", font(int(140 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="The dog wagged it's tail. Spot the mistake?", draw=s1),
    dict(say="It's, with an apostrophe, means it is, or it has.", draw=s2),
    dict(say="The apostrophe stands in for missing letters.", draw=s3),
    dict(say="Its, without one, means belonging to it. Like his and her, no apostrophe.", draw=s4),
    dict(say="Quick test: say it is. If the sentence still makes sense, write it's.",
         show="Quick test: say \"it is\". If the sentence still makes sense, write it's.", draw=s5),
    dict(say="The dog wagged it is tail? No. So it's its tail.", draw=s6),
    dict(say="Read it's as it is, every time.", show="Read it's as \"it is\", every time.", draw=s7),
]
