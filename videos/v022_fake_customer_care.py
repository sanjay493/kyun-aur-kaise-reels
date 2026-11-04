from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Googled a helpline number? Careful."
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)
SCREEN, GREY = (235, 240, 250), (120, 130, 150)


def phone(d, cx, cy, s=1.0, screen=SCREEN):
    w, h = 420 * s, 740 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 50 * s, fill=DARK, outline=(200, 210, 230),
                        width=6)
    d.rounded_rectangle([cx - w / 2 + 18 * s, cy - h / 2 + 44 * s, cx + w / 2 - 18 * s, cy + h / 2 - 44 * s],
                        28 * s, fill=screen)
    return cx - w / 2 + 40 * s, cy - h / 2 + 70 * s


def search_results(d, x, y, s, flag=0.0):
    d.rounded_rectangle([x, y, x + 340 * s, y + 60 * s], 30 * s, fill=WHITE, outline=GREY, width=3)
    text_c(d, (x + 20 * s, y + 30 * s), "refund customer care", font(int(24 * s), "semi"), DARK, anchor="lm")
    for i in range(3):
        yy = y + 100 * s + i * 150 * s
        bad = i == 0
        col = RED if (bad and flag > 0) else (40, 90, 200)
        d.rounded_rectangle([x - 6 * s, yy - 10 * s, x + 346 * s, yy + 120 * s], 16 * s,
                            outline=RED if (bad and flag > 0) else SCREEN, width=int(3 + 5 * flag))
        text_c(d, (x, yy + 15 * s), "Helpline 24x7" if bad else "Result", font(int(28 * s), "bold"), col,
               anchor="lm")
        text_c(d, (x, yy + 60 * s), "Call 98XXX XXXXX" if bad else "...", font(int(26 * s), "semi"), DARK,
               anchor="lm")


def s1(img, d, t, T, th):
    x, y = phone(d, 540, 690, 1.0)
    search_results(d, x, y, 1.0)
    if t > 1.6:
        g = pop(prog(t, 1.6, 0.4))
        text_c(d, (540, 1150), "Careful!", font(int(72 * g) + 1, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    x, y = phone(d, 540, 690, 1.0)
    search_results(d, x, y, 1.0, flag=ease(prog(t, 0.4, 0.5)))
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([240, 1095, 840, 1190], 30, fill=RED)
        text_c(d, (540, 1142), "FAKE NUMBER", font(int(60 * g) + 1, "bold"), WHITE)


def s3(img, d, t, T, th):
    # caller bubble with asks
    d.ellipse([420, 330, 660, 570], fill=(90, 100, 130))
    d.ellipse([490, 360, 590, 460], fill=(200, 170, 140))
    d.chord([450, 450, 630, 640], 180, 360, fill=(60, 70, 100))
    text_c(d, (540, 620), "\"I'm from customer care\"", font(46, "semi"), th["soft"])
    asks = ["install this screen-sharing app", "tell me the O.T.P."]
    shows = ["Install this screen-sharing app", "Tell me the OTP"]
    for i, lb in enumerate(shows):
        if t > 0.9 + i * 1.6:
            g = pop(prog(t, 0.9 + i * 1.6, 0.4))
            yy = 780 + i * 170
            d.rounded_rectangle([110, yy - 60, 970, yy + 60], 30, fill=WHITE)
            text_c(d, (540, yy), lb, font(int(48 * g) + 1, "bold"), RED)


def s4(img, d, t, T, th):
    text_c(d, (540, 380), "Real banks NEVER ask for", font(56, "bold"), WHITE)
    for i, lb in enumerate(["OTP", "PIN", "PASSWORD"]):
        if t > 0.4 + i * 0.5:
            g = pop(prog(t, 0.4 + i * 0.5, 0.4))
            yy = 560 + i * 190
            d.rounded_rectangle([260, yy - 70, 820, yy + 70], 36, fill=(255, 255, 255, 40), outline=RED, width=6)
            text_c(d, (540, yy), lb, font(int(70 * g) + 1, "bold"), WHITE)
            d.line([(300, yy + 40), (780, yy - 40)], fill=RED, width=10)


def s5(img, d, t, T, th):
    x, y = phone(d, 540, 700, 1.0)
    d.rounded_rectangle([x, y, x + 340, y + 70], 16, fill=GREEN)
    text_c(d, (x + 170, y + 35), "Official website / app", font(24, "bold"), WHITE)
    text_c(d, (x + 170, y + 170), "Contact us", font(40, "bold"), DARK)
    text_c(d, (x + 170, y + 250), "Customer care:", font(28, "semi"), GREY)
    text_c(d, (x + 170, y + 300), "1800 XXX XXXX", font(34, "bold"), (40, 90, 200))
    if t > 1.0:
        g = pop(prog(t, 1.0, 0.4))
        d.ellipse([850 - 70 * g, 560 - 70 * g, 850 + 70 * g, 560 + 70 * g], fill=GREEN, outline=WHITE, width=5)
        text_c(d, (850, 560), "✓", font(int(90 * g) + 1, "sym"), WHITE)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 500), "Don't trust the", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 600), "search result", font(int(70 * g) + 1, "bold"), RED)
    if t > 0.7:
        text_c(d, (540, 800), "Trust the", font(64, "semi"), th["soft"])
        text_c(d, (540, 910), "OFFICIAL SOURCE", font(80, "bold"), th["accent"])


SCENES = [
    dict(say="Refund stuck, so you search online for the helpline number? Careful.", draw=s1),
    dict(say="The R.B.I. warns these numbers are often fakes put up by fraudsters.",
         show="The RBI warns these numbers are often fakes put up by fraudsters.", draw=s2),
    dict(say="The fake agent sounds helpful, then asks you to install a screen-sharing app or share an O.T.P.",
         show="The fake agent sounds helpful, then asks you to install a screen-sharing app or share an OTP.",
         draw=s3),
    dict(say="Real banks never ask for your O.T.P., PIN or password.",
         show="Real banks never ask for your OTP, PIN or password.", draw=s4),
    dict(say="Take the number only from the official website or app.", draw=s5),
    dict(say="Don't trust the search result. Trust the official source.", draw=s6),
]
