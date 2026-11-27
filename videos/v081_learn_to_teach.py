from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "study"
TITLE = "Study as if you'll teach it"
WHITE, DARK = (255, 255, 255), (20, 25, 45)
TEST, TEACH, GOLD = (255, 150, 120), (130, 230, 160), (255, 210, 90)
SKIN, HAIR = (240, 190, 150), (35, 25, 25)


def person(d, x, y, col, s=1.0):
    r = 50 * s
    d.ellipse([x - r, y - r, x + r, y + r], fill=SKIN)
    d.pieslice([x - r, y - r, x + r, y + r], 180, 360, fill=HAIR)
    d.rounded_rectangle([x - 70 * s, y + 60 * s, x + 70 * s, y + 200 * s], int(30 * s), fill=col)


def book(d, x, y, s=1.0):
    d.polygon([(x, y), (x - 130 * s, y - 30 * s), (x - 130 * s, y + 120 * s), (x, y + 150 * s)], fill=(250, 250, 255))
    d.polygon([(x, y), (x + 130 * s, y - 30 * s), (x + 130 * s, y + 120 * s), (x, y + 150 * s)], fill=(225, 230, 245))
    for i in range(4):
        yy = y + 10 * s + i * 28 * s
        d.line([(x - 110 * s, yy - 20 * s), (x - 20 * s, yy)], fill=(160, 170, 200), width=4)
        d.line([(x + 20 * s, yy), (x + 110 * s, yy - 20 * s)], fill=(160, 170, 200), width=4)


def s1(img, d, t, T, th):
    book(d, 540, 520, 1.3)
    text_c(d, (540, 360), "Remember a chapter better?", font(54, "bold"), WHITE)
    if t > 0.9:
        g = pop(prog(t, 0.9, 0.45))
        d.rounded_rectangle([140, 860, 940, 1020], 50, fill=th["accent"])
        text_c(d, (540, 940), "Study as if you'll teach it", font(int(50 * g) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 330), "A 2014 study", font(58, "bold"), WHITE)
    book(d, 540, 420, 0.7)
    g = pop(prog(t, 0.5, 0.4))
    person(d, 300, 700, TEST, g)
    if t > 0.5:
        d.rounded_rectangle([150, 960, 450, 1060], 40, fill=TEST)
        text_c(d, (300, 1010), "expect a test", font(38, "bold"), DARK)
    if t > 1.2:
        g2 = pop(prog(t, 1.2, 0.4))
        person(d, 780, 700, TEACH, g2)
        d.rounded_rectangle([600, 960, 960, 1060], 40, fill=TEACH)
        text_c(d, (780, 1010), "expect to teach", font(38, "bold"), DARK)


def s3(img, d, t, T, th):
    text_c(d, (540, 380), "The twist:", font(62, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([120, 520, 960, 700], 50, fill=(255, 255, 255, 30))
    text_c(d, (540, 610), "nobody actually taught", font(int(54 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        g2 = pop(prog(t, 0.9, 0.45))
        d.rounded_rectangle([120, 760, 960, 940], 50, fill=(255, 255, 255, 30))
        text_c(d, (540, 850), "everyone took the test", font(int(54 * g2) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Expecting to teach:", font(58, "bold"), TEACH)
    items = ["remembered more", "especially main points", "better organised"]
    for i, s in enumerate(items):
        if t > 0.3 + 0.45 * i:
            g = pop(prog(t, 0.3 + 0.45 * i, 0.4))
            y = 520 + i * 190
            d.rounded_rectangle([120, y - 70, 960, y + 70], 40, fill=(255, 255, 255, 30), outline=TEACH, width=5)
            text_c(d, (200, y), "✓", font(int(64 * g) + 1, "sym"), TEACH)
            text_c(d, (580, y), s, font(int(50 * g) + 1, "bold"), WHITE)


def s5(img, d, t, T, th):
    person(d, 260, 560, TEACH, 1.1)
    # whiteboard
    d.rounded_rectangle([430, 380, 980, 900], 24, fill=(245, 248, 255))
    text_c(d, (705, 440), "Key points", font(44, "bold"), DARK)
    for i in range(3):
        if t > 0.4 + 0.4 * i:
            y = 540 + i * 110
            text_c(d, (500, y), f"{i + 1}.", font(44, "bold"), (60, 90, 160))
            k = ease(prog(t, 0.4 + 0.4 * i, 0.4))
            d.line([(550, y), (550 + 360 * k, y)], fill=(120, 140, 190), width=12)
    if t > 1.7:
        text_c(d, (540, 1060), "find the key points, put them in order", font(42, "semi"), th["accent"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 560), "Study like", font(int(70 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 670), "a teacher", font(int(90 * g) + 1, "bold"), th["accent"])
    if t > 0.8:
        g2 = pop(prog(t, 0.8, 0.45))
        text_c(d, (540, 860), "not just a student", font(int(56 * g2) + 1, "semi"), WHITE)


SCENES = [
    dict(say="Want to remember a chapter better? Study it like you'll teach it.", draw=s1),
    dict(say="In a twenty fourteen study, students read a passage. Some expected a test, others to teach it.",
         show="In a 2014 study, students read a passage. Some expected a test, others to teach it.", draw=s2),
    dict(say="Twist: nobody actually taught. Everyone took the test.", draw=s3),
    dict(say="Those expecting to teach remembered more, especially main points, and organised it better.", draw=s4),
    dict(say="Preparing to teach makes you find key points and order them.", draw=s5),
    dict(say="Study like a teacher, not just a student.", draw=s6),
]
