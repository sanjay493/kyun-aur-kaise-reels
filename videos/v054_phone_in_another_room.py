from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Face down, on silent, still stealing focus"
WHITE, DARK = (255, 255, 255), (20, 30, 50)
PHONE, SCREEN, DESK = (40, 45, 60), (70, 80, 100), (150, 105, 70)
GREEN, RED, AMBER = (110, 220, 140), (255, 110, 110), (255, 200, 90)


def phone(d, x, y, s=1.0, down=True):
    d.rounded_rectangle([x - 70 * s, y - 130 * s, x + 70 * s, y + 130 * s], int(22 * s), fill=PHONE)
    if not down:
        d.rounded_rectangle([x - 58 * s, y - 115 * s, x + 58 * s, y + 115 * s], int(14 * s), fill=SCREEN)
    else:
        d.ellipse([x - 16 * s, y - 100 * s, x + 16 * s, y - 68 * s], outline=(120, 125, 140), width=4)


def flat_phone(d, x, y, w=260):
    d.rounded_rectangle([x - w / 2, y - 28, x + w / 2, y + 28], 18, fill=PHONE)


def desk(d, y=900):
    d.rectangle([100, y, 980, y + 40], fill=DESK)
    d.rectangle([140, y + 40, 170, y + 250], fill=DESK)
    d.rectangle([910, y + 40, 940, y + 250], fill=DESK)


def mute(d, x, y, r=40):
    d.ellipse([x - r, y - r, x + r, y + r], fill=WHITE)
    d.polygon([(x - 22, y - 10), (x - 8, y - 10), (x + 8, y - 24), (x + 8, y + 24), (x - 8, y + 10), (x - 22, y + 10)],
              fill=DARK)
    d.line([(x - 30, y - 30), (x + 30, y + 30)], fill=RED, width=7)


def s1(img, d, t, T, th):
    desk(d)
    d.rounded_rectangle([200, 760, 520, 900], 10, fill=(240, 240, 230))
    k = ease(prog(t, 0.2, 0.6))
    flat_phone(d, 740, 872 - 200 * (1 - k))
    if t > 0.9:
        mute(d, 740, 700, int(40 * pop(prog(t, 0.9, 0.4))) + 1)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 520), "Harmless?", font(int(84 * g) + 1, "bold"), th["accent"])
    text_c(d, (540, 360), "Face down. On silent.", font(58, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "University of Texas study", font(54, "bold"), th["accent"])
    n = int(clamp((t - 0.2) / 1.2) * 80)
    for i in range(n):
        x, y = 160 + (i % 10) * 85, 470 + (i // 10) * 62
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=WHITE)
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 1060), "~800 people", font(int(70 * g) + 1, "bold"), WHITE)
        text_c(d, (540, 1150), "concentration tests", font(44, "semi"), th["soft"])


SPOTS = [("on the desk", 230), ("pocket or bag", 540), ("another room", 850)]


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Where was the phone?", font(58, "bold"), WHITE)
    for i, (lab, x) in enumerate(SPOTS):
        if t > 0.3 + 0.5 * i:
            g = pop(prog(t, 0.3 + 0.5 * i, 0.4))
            d.rounded_rectangle([x - 140, 470, x + 140, 900], 30, fill=(255, 255, 255, 30), outline=th["soft"], width=4)
            if i == 0:
                phone(d, x, 680, 0.9 * g + 0.01)
            elif i == 1:
                d.rounded_rectangle([x - 90, 600, x + 90, 800], 30, fill=(120, 90, 160))
                d.arc([x - 60, 540, x + 60, 660], 180, 360, fill=(120, 90, 160), width=14)
            else:
                d.rectangle([x - 70, 540, x + 70, 820], outline=WHITE, width=8)
                d.ellipse([x + 35, 670, x + 55, 690], fill=WHITE)
            text_c(d, (x, 960), lab, font(38, "bold"), WHITE)


def s4(img, d, t, T, th):
    res = [("another room", 0.95, GREEN), ("on the desk", 0.65, RED)]
    text_c(d, (540, 350), "Test scores", font(60, "bold"), th["accent"])
    for i, (lab, v, col) in enumerate(res):
        k = ease(prog(t, 0.2 + 0.25 * i, 0.7))
        y = 560 + i * 240
        text_c(d, (130, y - 55), lab, font(40, "bold"), WHITE, anchor="lm")
        d.rounded_rectangle([130, y - 25, 130 + 800 * v * k, y + 35], 20, fill=col)
    if t > 1.4:
        text_c(d, (540, 1110), "(illustration, not exact scores)", font(34, "reg"), th["soft"])


def s5(img, d, t, T, th):
    d.rectangle([100, 960, 980, 1000], fill=DESK)
    flat_phone(d, 540, 932)
    # attention "leaking" from head to phone
    d.ellipse([400, 380, 680, 660], fill=(255, 215, 170))
    for i in range(6):
        k = (t * 0.8 + i / 6) % 1
        x, y = 540, 660 + 240 * k
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=th["accent"])
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        d.rounded_rectangle([140, 1060, 940, 1180], 50, fill=th["accent"])
        text_c(d, (540, 1120), "uses up some attention", font(int(52 * g) + 1, "bold"), DARK)
    text_c(d, (540, 330), "Even silent...", font(56, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Studying?", font(int(80 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 680), "Phone in", font(int(84 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 800), "another room.", font(int(84 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your phone is on the desk, face down, on silent. Harmless, right?", draw=s1),
    dict(say="Researchers in Texas gave nearly eight hundred people concentration tests.",
         show="Researchers in Texas gave nearly 800 people concentration tests.", draw=s2),
    dict(say="Some kept their phones on the desk, some in a pocket or bag, and some in another room.", draw=s3),
    dict(say="The other-room group did best, clearly beating the desk group.", draw=s4),
    dict(say="Even silent, a nearby phone quietly uses up some of your attention.", draw=s5),
    dict(say="Studying? Phone in another room.", draw=s6),
]
