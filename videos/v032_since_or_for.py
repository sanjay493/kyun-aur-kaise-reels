from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "english"
TITLE = "\"I am living here since 2020\" — spot the mistake"
WHITE, DARK = (255, 255, 255), (30, 20, 30)
RED, GREEN = (235, 80, 80), (80, 200, 120)


def card(d, y, txt, col, th, g=1.0, size=52, outline=None):
    d.rounded_rectangle([90, y - 75, W - 90, y + 75], 36, fill=(255, 255, 255, 235), outline=outline, width=8)
    text_c(d, (540, y), txt, font(int(size * g) + 1, "bold"), col)


def timeline(d, th, y=640):
    d.line([(120, y), (960, y)], fill=WHITE, width=8)
    d.polygon([(960, y - 20), (1000, y), (960, y + 20)], fill=WHITE)
    for x, lb in [(260, "2020"), (900, "now")]:
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=th["accent"])
        text_c(d, (x, y + 60), lb, font(44, "bold"), th["soft"])


def s1(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    card(d, 560, "I am living in Pune since 2020.", DARK, th, g, 50)
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        d.line([(160, 590), (470, 590)], fill=RED, width=8)
        text_c(d, (540, 820), "Spot the mistake?", font(int(70 * g2) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def s2(img, d, t, T, th):
    timeline(d, th)
    k = ease(prog(t, 0.4, 1.4))
    if k > 0:
        d.line([(260, 560), (260 + 640 * k, 560)], fill=th["accent"], width=14)
        text_c(d, (580, 480), "started... still true", font(46, "bold"), th["accent"])
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([170, 900, 910, 1020], 40, fill=th["accent"])
        text_c(d, (540, 960), "PRESENT PERFECT", font(int(62 * g) + 1, "bold"), DARK)
        text_c(d, (540, 1100), "have / has + past participle", font(42, "semi"), th["soft"])


def s3(img, d, t, T, th):
    card(d, 420, "I am living in Pune since 2020.", (150, 140, 150), th, 1.0, 48)
    d.line([(150, 420), (930, 420)], fill=RED, width=7)
    g = pop(prog(t, 0.4, 0.45))
    card(d, 660, "I have lived in Pune since 2020.", DARK, th, g, 48, outline=GREEN)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        d.ellipse([890 - 50 * g2, 820 - 50 * g2, 890 + 50 * g2, 820 + 50 * g2], fill=GREEN)
        text_c(d, (890, 820), "✓", font(int(70 * g2) + 1, "sym"), WHITE)
        text_c(d, (540, 940), "have lived", font(int(74 * g2) + 1, "bold"), th["accent"])


def s4(img, d, t, T, th):
    timeline(d, th, 700)
    g = pop(prog(t, 0.1, 0.45))
    d.rounded_rectangle([340, 330, 740, 450], 40, fill=th["accent"])
    text_c(d, (540, 390), "SINCE", font(int(76 * g) + 1, "bold"), DARK)
    # pointer to starting point
    k = ease(prog(t, 0.6, 0.6))
    d.line([(260, 470), (260, 470 + 190 * k)], fill=th["accent"], width=10)
    if k >= 1:
        d.polygon([(240, 650), (280, 650), (260, 680)], fill=th["accent"])
    text_c(d, (540, 520), "the starting point", font(44, "semi"), WHITE)
    for i, ex in enumerate(["since Monday", "since 2020", "since I was ten"]):
        if t > 1.2 + i * 0.4:
            text_c(d, (540, 900 + i * 90), ex, font(52, "bold"), WHITE)


def s5(img, d, t, T, th):
    timeline(d, th, 700)
    g = pop(prog(t, 0.1, 0.45))
    d.rounded_rectangle([340, 330, 740, 450], 40, fill=(110, 215, 255))
    text_c(d, (540, 390), "FOR", font(int(76 * g) + 1, "bold"), DARK)
    k = ease(prog(t, 0.5, 1.0))
    d.line([(260, 620), (260 + 640 * k, 620)], fill=(110, 215, 255), width=14)
    d.line([(260, 600), (260, 640)], fill=(110, 215, 255), width=8)
    if k >= 1:
        d.line([(900, 600), (900, 640)], fill=(110, 215, 255), width=8)
    text_c(d, (540, 520), "how long", font(44, "semi"), WHITE)
    for i, ex in enumerate(["for three days", "for six years"]):
        if t > 1.2 + i * 0.4:
            text_c(d, (540, 920 + i * 100), ex, font(54, "bold"), WHITE)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 520), "SINCE", font(int(96 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 620), "= the start", font(int(60 * g) + 1, "bold"), WHITE)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.4))
        text_c(d, (540, 800), "FOR", font(int(96 * g2) + 1, "bold"), (110, 215, 255))
        text_c(d, (540, 900), "= how long", font(int(60 * g2) + 1, "bold"), WHITE)


SCENES = [
    dict(say="I am living in Pune since twenty twenty. Spot the mistake?",
         show="\"I am living in Pune since 2020.\" Spot the mistake?", draw=s1),
    dict(say="It started in the past and is still true, so use the present perfect.", draw=s2),
    dict(say="I have lived in Pune since twenty twenty.", show="I have lived in Pune since 2020.", draw=s3),
    dict(say="Since gives the starting point. Since Monday, since twenty twenty.",
         show="Since gives the starting point. Since Monday, since 2020.", draw=s4),
    dict(say="For measures the length of time. For three days, for six years.", draw=s5),
    dict(say="Since is the start. For is how long.", draw=s6),
]
