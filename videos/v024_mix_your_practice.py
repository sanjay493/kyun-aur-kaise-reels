from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Same type of sum, 20 times in a row?"
WHITE, DARK = (255, 255, 255), (20, 25, 45)
TYPES = [("A", "area", (255, 170, 90)), ("B", "%", (130, 220, 150)), ("C", "ratio", (200, 150, 255)),
         ("D", "angles", (255, 120, 150))]


def card(d, x, y, k, s=1.0, a=255):
    lab, name, col = TYPES[k]
    d.rounded_rectangle([x - 70 * s, y - 45 * s, x + 70 * s, y + 45 * s], int(18 * s), fill=col + (a,),
                        outline=DARK + (a,), width=3)
    text_c(d, (x, y), name, font(max(1, int(34 * s)), "bold"), DARK + (a,))


def grid(d, t, seq, y0=380, cols=5, start=0.1, step=0.06):
    for i, k in enumerate(seq):
        g = pop(prog(t, start + i * step, 0.3))
        if g > 0:
            x = 140 + (i % cols) * 200
            y = y0 + (i // cols) * 120
            card(d, x, y, k, g)


def s1(img, d, t, T, th):
    grid(d, t, [0] * 20, y0=360)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 900), "20 × same type", font(int(70 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 1020), "feels easy...", font(int(62 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 330), "BLOCKED practice", font(64, "bold"), th["accent"])
    for i in range(5):
        card(d, 140 + i * 200, 470, 0)
    # arrow repeating the same method
    d.rounded_rectangle([170, 600, 910, 720], 30, fill=(255, 255, 255, 40))
    text_c(d, (540, 660), "method: same as last one", font(48, "bold"), WHITE)
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        text_c(d, (540, 880), "no deciding needed", font(int(64 * g) + 1, "bold"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 330), "INTERLEAVED practice", font(62, "bold"), th["accent"])
    seq = [2, 0, 3, 1, 0]
    for i, k in enumerate(seq):
        g = pop(prog(t, 0.1 + i * 0.12, 0.3))
        if g > 0:
            card(d, 140 + i * 200, 470, k, g)
    if t > 0.9:
        for i in range(5):
            x = 140 + i * 200
            g = pop(prog(t, 0.9 + i * 0.15, 0.3))
            text_c(d, (x, 600), "?", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 1.7:
        text_c(d, (540, 800), "which method THIS time?", font(56, "bold"), WHITE)
        text_c(d, (540, 920), "you choose, every time", font(56, "bold"), th["accent"])


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "One study:", font(58, "bold"), th["soft"])
    g = pop(prog(t, 0.2, 0.4))
    d.rounded_rectangle([140, 450, 940, 620], 40, fill=th["accent"])
    text_c(d, (540, 535), "Class 7 students", font(int(68 * g) + 1, "bold"), DARK)
    k = ease(prog(t, 0.8, 1.2))
    # 9-week calendar strip
    for i in range(9):
        x = 150 + i * 98
        on = k * 9 > i
        d.rounded_rectangle([x - 40, 720, x + 40, 800], 14, fill=(255, 255, 255, 220 if on else 50))
        text_c(d, (x, 760), f"W{i + 1}", font(30, "bold"), DARK if on else WHITE)
    if t > 1.5:
        text_c(d, (540, 920), "9 weeks of maths practice", font(54, "bold"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 330), "Surprise test", font(60, "bold"), WHITE)
    base, top = 1090, 470
    k = ease(prog(t, 0.3, 1.4))
    for x, val, lab, col in ((330, 72, "mixed", th["accent"]), (750, 38, "blocked", th["soft"])):
        h = (base - top) * val / 100 * k
        d.rounded_rectangle([x - 110, base - h, x + 110, base], 20, fill=col)
        if k > 0.9:
            text_c(d, (x, base - h - 55), f"{val}%", font(72, "bold"), WHITE)
        text_c(d, (x, base + 55), lab, font(52, "bold"), WHITE)
    d.line([(160, base), (920, base)], fill=WHITE, width=5)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 520), "Don't just practise", font(int(68 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 620), "the method.", font(int(68 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 820), "Practise", font(int(90 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 930), "CHOOSING it.", font(int(90 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Twenty sums of one type in a row feels easy. That might be the problem.",
         show="20 sums of one type in a row feels easy. That might be the problem.", draw=s1),
    dict(say="With blocked practice, you never decide which method to use.", draw=s2),
    dict(say="Mixing types makes you choose each time. That's called interleaving.", draw=s3),
    dict(say="In one study, seventh graders practised maths for nine weeks.",
         show="In one study, Class 7 students practised maths for 9 weeks.", draw=s4),
    dict(say="On a surprise test, mixed topics scored seventy-two percent. Blocked topics, thirty-eight.",
         show="On a surprise test, mixed topics scored 72%. Blocked topics, 38%.", draw=s5),
    dict(say="Don't just practise the method. Practise choosing it.", draw=s6),
]
