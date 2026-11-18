from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Your page is all yellow. Did you learn it?"
WHITE, DARK = (255, 255, 255), (20, 30, 50)
PAPER, LINE = (245, 245, 238), (175, 180, 195)
HL, GREEN, RED = (255, 235, 70), (110, 220, 140), (255, 110, 110)


def page(d, x0, y0, w, h, hl=0.0, rows=9):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 20, fill=PAPER)
    for i in range(rows):
        y = y0 + 60 + i * (h - 100) / (rows - 1)
        ln = w - 80 - (60 if i % 3 == 2 else 0)
        if hl > 0:
            d.rectangle([x0 + 35, y - 16, x0 + 35 + ln * clamp(hl * rows - i), y + 16], fill=HL)
        d.line([(x0 + 40, y), (x0 + 40 + ln, y)], fill=LINE, width=8)


def pen(d, x, y):
    d.polygon([(x, y), (x + 30, y - 30), (x + 150, y - 150), (x + 120, y - 180), (x, y - 60)], fill=HL)
    d.polygon([(x, y), (x - 25, y + 25), (x + 10, y - 20)], fill=(200, 180, 40))


def s1(img, d, t, T, th):
    k = ease(prog(t, 0.1, 2.0))
    page(d, 240, 420, 600, 640, hl=k)
    pen(d, 760, 420 + 640 * k * 0.9)
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        text_c(d, (540, 1140), "learnt it?", font(int(70 * g) + 1, "bold"), th["accent"])


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "10 study techniques reviewed", font(48, "bold"), WHITE)
    for i in range(10):
        if t > 0.2 + 0.08 * i:
            x, y = 210 + (i % 5) * 165, 520 + (i // 5) * 170
            d.rounded_rectangle([x - 65, y - 65, x + 65, y + 65], 24, fill=(255, 255, 255, 40), outline=th["soft"], width=3)
            text_c(d, (x, y), str(i + 1), font(52, "bold"), WHITE)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.4))
        d.rounded_rectangle([160, 860, 920, 1000], 50, fill=HL)
        text_c(d, (540, 930), "highlighting: LOW", font(int(60 * g) + 1, "bold"), DARK)
        text_c(d, (540, 1090), "rereading: low too", font(44, "semi"), th["soft"])


def s3(img, d, t, T, th):
    page(d, 140, 420, 380, 460, hl=1.0, rows=7)
    text_c(d, (330, 940), "feels busy", font(50, "bold"), HL)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (760, 650), "≠", font(int(150 * g) + 1, "sym"), WHITE)
    if t > 1.2:
        text_c(d, (760, 940), "learning", font(50, "bold"), GREEN)


def s4(img, d, t, T, th):
    text_c(d, (540, 360), "Rated highest", font(60, "bold"), th["accent"])
    items = [("test yourself", "?"), ("spread it over days", "1  2  3")]
    for i, (lab, icon) in enumerate(items):
        if t > 0.3 + 0.6 * i:
            g = pop(prog(t, 0.3 + 0.6 * i, 0.4))
            y = 560 + i * 280
            d.rounded_rectangle([120, y - 110, 960, y + 110], 50, fill=(255, 255, 255, 35), outline=GREEN, width=5)
            text_c(d, (250, y), icon, font(int(64 * g) + 1, "bold"), GREEN)
            text_c(d, (620, y), lab, font(int(54 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    k = ease(prog(t, 0.2, 0.7))
    # book closes
    w = 600 * (1 - 0.55 * k)
    page(d, 540 - w / 2, 420, w, 520, hl=0.4, rows=6)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.4))
        d.rounded_rectangle([140, 1000, 940, 1130], 50, fill=th["accent"])
        text_c(d, (540, 1065), "explain it from memory", font(int(50 * g) + 1, "bold"), DARK)
    if t > 0.6:
        text_c(d, (540, 360), "book closed", font(54, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Colour less.", font(int(86 * g) + 1, "bold"), HL)
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 760), "Recall more.", font(int(86 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Your whole page is yellow with highlighter. But did you actually learn it?", draw=s1),
    dict(say="Researchers reviewed ten popular study techniques. Highlighting was rated low. So was rereading.", draw=s2),
    dict(say="It feels busy, but students got little benefit from it.", draw=s3),
    dict(say="The top two? Testing yourself, and spreading study over several days.", draw=s4),
    dict(say="So after highlighting, close the book and explain each point from memory.", draw=s5),
    dict(say="Colour less. Recall more.", draw=s6),
]
