from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Forwarded many times? Pause before you share"
WHITE, DARK, GREY = (255, 255, 255), (20, 30, 40), (120, 130, 140)
BUBBLE, CHAT_BG = (220, 248, 198), (236, 229, 221)
PHONE = (30, 34, 40)


def arrows(d, x, y, col=GREY, n=2, s=1.0):
    """Small forward arrows (double = forwarded many times)."""
    for i in range(n):
        ox = x + i * 22 * s
        d.line([(ox, y + 12 * s), (ox + 10 * s, y), (ox, y - 12 * s)], fill=col, width=int(5 * s))


def bubble(d, x, y, w, many=True, lines=("Free laptops for all", "students! Fill form", "before Sunday!!"), k=1.0):
    h = 90 + 56 * len(lines)
    d.rounded_rectangle([x, y, x + w, y + h], 24, fill=BUBBLE)
    lab = "Forwarded many times" if many else "Forwarded"
    arrows(d, x + 30, y + 40, GREY, 2 if many else 1)
    d.text((x + (80 if many else 58), y + 40), lab, font=font(34, "reg"), fill=GREY, anchor="lm")
    for i, ln in enumerate(lines):
        d.text((x + 30, y + 110 + i * 56), ln, font=font(42, "semi"), fill=DARK, anchor="lm")
    return h


def s1(img, d, t, T, th):
    # phone with a forwarded message
    d.rounded_rectangle([200, 300, 880, 1180], 50, fill=PHONE)
    d.rounded_rectangle([225, 340, 855, 1140], 30, fill=CHAT_BG)
    k = ease(prog(t, 0.2, 0.6))
    bubble(d, 255, 700 - 120 * k, 570)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.5))
        r = 40 * g
        d.ellipse([297 - r, 620 - r, 297 + r, 620 + r], outline=th["accent"], width=6)
        text_c(d, (540, 1060), "Pause!", font(int(80 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 330), "5 or more chats", font(66, "bold"), th["accent"])
    # chain of chats
    xs = [150, 345, 540, 735, 930]
    for i, x in enumerate(xs):
        if t > 0.2 + i * 0.3:
            g = pop(prog(t, 0.2 + i * 0.3, 0.35))
            r = 70 * g
            d.ellipse([x - r, 700 - r, x + r, 700 + r], fill=(255, 255, 255, 50), outline=WHITE, width=5)
            text_c(d, (x, 700), str(i + 1), font(int(60 * g) + 1, "bold"), WHITE)
            if i > 0:
                d.line([(xs[i - 1] + 72, 700), (x - 72, 700)], fill=th["accent"], width=6)
    if t > 1.8:
        arrows(d, 470, 920, th["accent"], 2, 2.2)
        text_c(d, (540, 1050), "then the label appears", font(48, "semi"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 330), "Not from your friend", font(62, "bold"), WHITE)
    # sender -> you, but the origin is unknown further back
    text_c(d, (180, 720), "?", font(160, "bold"), GREY)
    text_c(d, (180, 860), "someone", font(40, "semi"), GREY)
    k = ease(prog(t, 0.2, 0.8))
    d.line([(260, 720), (260 + 160 * k, 720)], fill=GREY, width=6)
    d.ellipse([440, 640, 600, 800], fill=(255, 255, 255, 60), outline=WHITE, width=5)
    text_c(d, (520, 860), "friend", font(40, "semi"), WHITE)
    if t > 0.9:
        k2 = ease(prog(t, 0.9, 0.6))
        d.line([(620, 720), (620 + 160 * k2, 720)], fill=WHITE, width=6)
        d.ellipse([800, 640, 960, 800], fill=(255, 255, 255, 60), outline=th["accent"], width=5)
        text_c(d, (880, 860), "you", font(40, "semi"), th["accent"])
    if t > 1.6:
        text_c(d, (540, 1080), "They just passed it on", font(50, "bold"), th["accent"])


def s4(img, d, t, T, th):
    d.rounded_rectangle([110, 380, 970, 1000], 40, fill=(255, 255, 255, 30), outline=WHITE, width=4)
    text_c(d, (540, 460), "WhatsApp's own advice:", font(46, "semi"), th["soft"])
    g = pop(prog(t, 0.3, 0.5))
    text_c(d, (540, 620), "Shared many times", font(int(62 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.5))
        text_c(d, (540, 740), "doesn't make it", font(int(62 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 870), "TRUE", font(int(100 * g2) + 1, "bold"), th["accent"])


def s5(img, d, t, T, th):
    text_c(d, (540, 330), "Photos & videos can be edited", font(52, "bold"), WHITE)
    # photo frame with edit pencil
    d.rounded_rectangle([170, 450, 590, 800], 20, fill=(255, 255, 255, 50), outline=WHITE, width=5)
    d.polygon([(200, 770), (330, 600), (430, 720), (490, 650), (560, 770)], fill=(120, 200, 160))
    d.ellipse([470, 490, 530, 550], fill=(255, 210, 70))
    k = ease(prog(t, 0.2, 0.6))
    d.line([(560 + 120 * (1 - k), 820 + 60 * (1 - k)), (640 + 120 * (1 - k), 900 + 60 * (1 - k))],
           fill=th["accent"], width=20)
    if t > 1.0:
        d.rounded_rectangle([600, 520, 940, 760], 20, fill=(255, 255, 255, 230))
        text_c(d, (770, 590), "NEWS", font(54, "bold"), DARK)
        for i in range(3):
            d.rectangle([640, 640 + i * 30, 900 - i * 50, 652 + i * 30], fill=GREY)
        text_c(d, (540, 1060), "Check trusted news sites", font(54, "bold"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    arrows(d, 480, 480, th["accent"], 2, int(2 * g) + 0.5 if g > 0 else 0.5)
    text_c(d, (540, 620), "Many forwards", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 720), "≠ more truth", font(int(70 * g2) + 1, "bold"), th["accent"])
    if t > 1.1:
        g3 = pop(prog(t, 1.1, 0.45))
        text_c(d, (540, 920), "Check before you share", font(int(56 * g3) + 1, "bold"), WHITE)


SCENES = [
    dict(say="Seen two arrows and the words, forwarded many times, on a WhatsApp message? Pause.",
         show="Seen two arrows and 'Forwarded many times' on a WhatsApp message? Pause.", draw=s1),
    dict(say="It means the message has passed through a chain of five or more chats.", draw=s2),
    dict(say="It didn't start with whoever sent it to you.", draw=s3),
    dict(say="WhatsApp itself says: being shared many times doesn't make it true.", draw=s4),
    dict(say="Photos and videos can be edited. Check trusted news sites first.", draw=s5),
    dict(say="Many forwards don't mean more truth. Check before you share.", draw=s6),
]
