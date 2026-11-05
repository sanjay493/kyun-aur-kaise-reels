import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Seen, but no reply?"
WHITE, DARK = (255, 255, 255), (30, 20, 45)
BUBBLE, TICK = (220, 248, 200), (80, 160, 255)
GREY = (150, 150, 165)


def phone(d, x, y, w=460, h=700):
    d.rounded_rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], 50, fill=(25, 25, 35), outline=(90, 90, 110),
                        width=6)
    d.rounded_rectangle([x - w / 2 + 22, y - h / 2 + 40, x + w / 2 - 22, y + h / 2 - 40], 30, fill=(240, 236, 228))


def msg(d, x, y, text, seen=True):
    f = font(36, "semi")
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw - 90, y - 40, x, y + 40], 22, fill=BUBBLE)
    d.text((x - tw - 60, y), text, font=f, fill=DARK, anchor="lm")
    col = TICK if seen else GREY
    for dx in (0, 14):
        bx = x - 46 + dx
        d.line([(bx - 10, y + 10), (bx - 3, y + 18), (bx + 10, y)], fill=col, width=4)


def s1(img, d, t, T, th):
    phone(d, 540, 640)
    msg(d, 730, 470, "Free to talk?")
    if t > 0.8:
        text_c(d, (540, 470 + 70), "Seen", font(28, "semi"), GREY)
    k = prog(t, 1.0, 1.5)
    hrs = 1 + int(k * 3)
    if t > 1.0:
        text_c(d, (540, 760), f"{hrs} hours later...", font(44, "bold"), DARK)
    if t > 2.2:
        g = pop(prog(t, 2.2, 0.4))
        text_c(d, (540, 1110), "Are they angry with me?", font(int(60 * g) + 1, "bold"), th["accent"],
               stroke_width=4, stroke_fill=DARK)


def thought(d, x, y, w, h, a=255):
    d.ellipse([x - w / 2, y - h / 2, x + w / 2, y + h / 2], fill=(255, 255, 255, a))
    d.ellipse([x - 40 - w / 4, y + h / 2 + 10, x + 0 - w / 4, y + h / 2 + 50], fill=(255, 255, 255, a))
    d.ellipse([x - 70 - w / 4, y + h / 2 + 60, x - 50 - w / 4, y + h / 2 + 80], fill=(255, 255, 255, a))


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.45))
    thought(d, 560, 560, 760 * g + 1, 420 * g + 1, 235)
    if g > 0.8:
        text_c(d, (560, 500), "\"They hate me.\"", font(56, "bold"), DARK)
        text_c(d, (560, 600), "\"I said something wrong.\"", font(46, "bold"), (120, 60, 90))
    if t > 1.2:
        text_c(d, (540, 1000), "the WORST story", font(64, "bold"), th["accent"])


def s3(img, d, t, T, th):
    items = [("phone died", "🔋"), ("in class", "📚"), ("helping at home", "🏠"), ("just forgot", "💭")]
    text_c(d, (540, 320), "Other reasons?", font(60, "bold"), WHITE)
    for i, (lab, _) in enumerate(items):
        g = pop(prog(t, 0.3 + i * 0.7, 0.4))
        if g <= 0:
            continue
        y = 450 + i * 175
        d.rounded_rectangle([150, y - 65, 930, y + 65], 34, fill=(255, 255, 255, int(45 + 10 * g)),
                            outline=th["accent"], width=4)
        text_c(d, (540, y), lab, font(int(60 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    phone(d, 540, 560, 420, 500)
    msg(d, 715, 470, "Free to talk?")
    g = pop(prog(t, 0.3, 0.4))
    d.ellipse([676 - 55 * g, 478 - 55 * g, 676 + 55 * g, 478 + 55 * g], outline=th["accent"], width=7)
    if t > 0.9:
        text_c(d, (540, 900), "\"Seen\" = opened", font(64, "bold"), WHITE)
        text_c(d, (540, 1010), "not how they feel", font(58, "bold"), th["accent"])


def s5(img, d, t, T, th):
    phone(d, 540, 640)
    msg(d, 730, 450, "Free to talk?")
    k = ease(prog(t, 0.3, 0.6))
    if k > 0:
        msg(d, 730, 560, "All okay?", seen=False)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([320, 660, 640, 740], 22, fill=(255, 255, 255))
        d.text((345, 700), "Yes! Phone died", font=font(32, "semi"), fill=DARK, anchor="lm")
    if t > 0.6:
        text_c(d, (540, 1110), "ask kindly", font(60, "bold"), th["accent"])


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    text_c(d, (540, 520), "Silence", font(int(84 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 630), "isn't anger.", font(int(84 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 840), "Ask,", font(int(96 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 960), "don't assume.", font(int(96 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your message shows seen, but no reply for hours. Are they angry with you?",
         show="Your message shows \"seen\", but no reply for hours. Are they angry with you?", draw=s1),
    dict(say="It's easy to jump to the worst story.", draw=s2),
    dict(say="But think of other reasons. Their phone died. They're in class. They're helping at home. Or they just forgot.",
         draw=s3),
    dict(say="Seen only means the message was opened, not what they feel.",
         show="\"Seen\" only means the message was opened, not what they feel.", draw=s4),
    dict(say="If it still bothers you, ask kindly. All okay?",
         show="If it still bothers you, ask kindly: \"All okay?\"", draw=s5),
    dict(say="Don't read silence as anger. Ask, don't assume.", draw=s6),
]
