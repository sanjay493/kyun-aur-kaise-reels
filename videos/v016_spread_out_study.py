from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Does studying all night work?"
WHITE, DARK = (255, 255, 255), (20, 25, 50)
RED, GREEN, MOON = (240, 90, 90), (90, 210, 130), (250, 235, 170)
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


def book(d, x, y, s=1.0, col=(110, 215, 255)):
    d.rounded_rectangle([x - 70 * s, y - 50 * s, x + 70 * s, y + 50 * s], 10, fill=col, outline=DARK, width=3)
    d.line([(x, y - 50 * s), (x, y + 50 * s)], fill=DARK, width=3)


def calendar(d, th, top=600):
    for i, dn in enumerate(DAYS):
        x = 140 + i * 200
        d.rounded_rectangle([x - 85, top, x + 85, top + 260], 22, fill=(255, 255, 255, 40), outline=th["soft"], width=3)
        text_c(d, (x, top + 40), dn, font(40, "bold"), th["soft"])


def s1(img, d, t, T, th):
    d.ellipse([760, 320, 900, 460], fill=MOON)
    d.ellipse([800, 300, 930, 430], fill=(35, 32, 78))  # crescent
    for i in range(5):
        g = pop(prog(t, 0.1 + i * 0.15, 0.3))
        if g > 0:
            book(d, 540, 1000 - i * 90, g, [th["accent"], (255, 200, 90), (240, 130, 160)][i % 3])
    text_c(d, (330, 420), "2 a.m.", font(80, "bold"), WHITE)
    if t > 1.2:
        text_c(d, (540, 1130), "Does it stick?", font(76, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 360), "CRAMMING", font(96, "bold"), th["accent"])
    # memory bar rises fast then drains
    k1 = ease(prog(t, 0.3, 0.6))
    k2 = ease(prog(t, 1.4, 1.0))
    lvl = k1 * (1 - 0.75 * k2)
    d.rounded_rectangle([400, 480, 680, 1000], 30, outline=WHITE, width=6)
    h = 500 * lvl
    if h > 4:
        d.rounded_rectangle([412, 990 - h, 668, 990], 22, fill=RED if k2 > 0.3 else GREEN)
    text_c(d, (540, 1080), "learnt fast… fades fast" if t > 1.4 else "feels like learning", font(54, "bold"), WHITE)


def s3(img, d, t, T, th):
    calendar(d, th)
    text_c(d, (540, 400), "same hours,", font(66, "bold"), WHITE)
    text_c(d, (540, 490), "split across days", font(66, "bold"), th["accent"])
    for j, i in enumerate((0, 2, 4)):
        g = pop(prog(t, 0.4 + j * 0.35, 0.35))
        if g > 0:
            book(d, 140 + i * 200, 760, 0.8 * g + 0.01)
    if t > 1.6:
        text_c(d, (540, 1000), "instead of one long night", font(48, "semi"), th["soft"])


def s4(img, d, t, T, th):
    # two curves: crammed vs spaced memory over time
    x0, x1, y0, y1 = 150, 930, 1020, 420
    d.line([(x0, y1 - 20), (x0, y0)], fill=WHITE, width=5)
    d.line([(x0, y0), (x1, y0)], fill=WHITE, width=5)
    text_c(d, (x0 + 10, y1 - 50), "remembered", font(38, "semi"), th["soft"], anchor="lm")
    text_c(d, (x1, y0 + 45), "time passing", font(38, "semi"), th["soft"], anchor="rm")
    k = ease(prog(t, 0.2, 1.4))
    n = int(60 * k)
    cram, spaced = [], []
    for i in range(n + 1):
        u = i / 60
        cram.append((x0 + u * (x1 - x0), y0 - (y0 - y1) * (0.85 * (1 - u) ** 2.4 + 0.08)))
        spaced.append((x0 + u * (x1 - x0), y0 - (y0 - y1) * (0.85 - 0.25 * u)))
    if n > 1:
        d.line(cram, fill=RED, width=10)
        d.line(spaced, fill=GREEN, width=10)
    if k > 0.95:
        text_c(d, (x1 - 10, cram[-1][1] - 60), "crammed", font(44, "bold"), RED, anchor="rm")
        text_c(d, (x1 - 10, spaced[-1][1] - 70), "spread out", font(44, "bold"), GREEN, anchor="rm")
    if t > 1.8:
        text_c(d, (540, 1120), "same total time", font(50, "bold"), th["accent"])


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "A big review of study methods:", font(48, "semi"), th["soft"])
    picks = [("Spacing it out", True), ("Testing yourself", True), ("Rereading", False), ("Highlighting", False)]
    for i, (lb, top) in enumerate(picks):
        g = pop(prog(t, 0.3 + i * 0.3, 0.35))
        if g > 0:
            y = 470 + i * 150
            d.rounded_rectangle([150, y - 55, 930, y + 55], 30, fill=th["accent"] if top else (255, 255, 255, 40))
            col = DARK if top else th["soft"]
            text_c(d, (210, y), "★" if top else "•", font(int(50 * g) + 1, "sym"), col)
            text_c(d, (280, y), lb, font(int(52 * g) + 1, "bold"), col, anchor="lm")
    if t > 1.7:
        text_c(d, (540, 1100), "top two", font(60, "bold"), GREEN)


def s6(img, d, t, T, th):
    text_c(d, (540, 360), "Try this week:", font(64, "bold"), WHITE)
    calendar(d, th, top=480)
    for j, i in enumerate((1, 3)):
        g = pop(prog(t, 0.3 + j * 0.5, 0.35))
        if g > 0:
            x = 140 + i * 200
            d.rounded_rectangle([x - 70, 580, x + 70, 700], 20, fill=th["accent"])
            text_c(d, (x, 640), "short", font(int(36 * g) + 1, "bold"), DARK)
    if t > 1.4:
        text_c(d, (540, 880), "2 short sessions", font(70, "bold"), th["accent"], stroke_width=5, stroke_fill=DARK)
        text_c(d, (540, 980), "not 1 long night", font(56, "semi"), WHITE)


def s7(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 600), "Spread it out,", font(int(90 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 780), "it stays.", font(int(110 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Studying all night before an exam feels productive. Does it stick?", draw=s1),
    dict(say="That's cramming. It feels like learning, but it often fades fast.", draw=s2),
    dict(say="Now split the same hours across a few days.", draw=s3),
    dict(say="Spread-out study is remembered longer, even with the same total time.", draw=s4),
    dict(say="A big review rated spacing one of the two best study techniques.", draw=s5),
    dict(say="Try two short sessions this week, not one long night.", draw=s6),
    dict(say="Spread it out, and it stays.", draw=s7),
]
