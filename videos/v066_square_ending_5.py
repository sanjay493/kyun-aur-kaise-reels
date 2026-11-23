from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "maths"
TITLE = "35 × 35 in your head?"
WHITE, DARK = (255, 255, 255), (25, 25, 60)
GREEN, RED, PINK, BLUE = (110, 220, 140), (255, 110, 110), (255, 150, 200), (120, 190, 255)


def box(d, x, y, s, col, g=1.0, w=200, size=100):
    d.rounded_rectangle([x - w / 2, y - 80, x + w / 2, y + 80], 30, fill=(255, 255, 255, 35), outline=col, width=5)
    text_c(d, (x, y), s, font(int(size * g) + 1, "bold"), col)


def s1(img, d, t, T, th):
    g = pop(prog(t, 0.2, 0.45))
    text_c(d, (540, 560), "35²", font(int(200 * g) + 1, "bold"), WHITE)
    if t > 0.9:
        text_c(d, (540, 780), "= 35 × 35", font(70, "sym"), th["soft"])
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        d.rounded_rectangle([240, 930, 840, 1070], 50, fill=th["accent"])
        text_c(d, (540, 1000), "in your head?", font(int(62 * g2) + 1, "bold"), DARK)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "First digit × next number", font(54, "bold"), th["accent"])
    box(d, 330, 560, "3", PINK, pop(prog(t, 0.2, 0.4)))
    if t > 0.7:
        text_c(d, (540, 560), "×", font(90, "sym"), WHITE)
        box(d, 750, 560, "4", BLUE, pop(prog(t, 0.7, 0.4)))
    if t > 1.4:
        g = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 820), "= 12", font(int(130 * g) + 1, "bold"), GREEN)


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Then put 25 after it", font(56, "bold"), th["accent"])
    box(d, 400, 560, "12", GREEN, 1.0, 230)
    if t > 0.5:
        k = ease(prog(t, 0.5, 0.5))
        box(d, 1000 - 320 * k, 560, "25", th["accent"], 1.0, 230)
    if t > 1.3:
        g = pop(prog(t, 1.3, 0.45))
        text_c(d, (540, 840), "35² = 1225", font(int(110 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Why does it work?", font(60, "bold"), th["accent"])
    g = pop(prog(t, 0.2, 0.4))
    text_c(d, (540, 480), "35 × 35", font(int(80 * g) + 1, "sym"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.4))
        text_c(d, (540, 620), "= 30 × 40 + 5 × 5", font(int(70 * g2) + 1, "sym"), WHITE)
    if t > 1.5:
        g3 = pop(prog(t, 1.5, 0.4))
        text_c(d, (540, 760), "= 1200 + 25", font(int(76 * g3) + 1, "sym"), GREEN)
    if t > 2.1:
        text_c(d, (540, 900), "= 1225", font(80, "bold"), th["accent"])
        text_c(d, (540, 1030), "(3 × 4 = 12 → 1200)", font(44, "sym"), th["soft"])


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Try 85²", font(70, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.4))
    text_c(d, (540, 520), "8 × 9 = 72", font(int(84 * g) + 1, "sym"), GREEN)
    if t > 1.0:
        box(d, 420, 720, "72", GREEN, 1.0, 230)
        k = ease(prog(t, 1.0, 0.5))
        box(d, 1000 - 340 * k, 720, "25", th["accent"], 1.0, 230)
    if t > 1.8:
        g2 = pop(prog(t, 1.8, 0.45))
        text_c(d, (540, 960), "85² = 7225", font(int(100 * g2) + 1, "bold"), WHITE)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 500), "Ends in 5?", font(int(84 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 680), "× the next number,", font(int(62 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 790), "then 25.", font(int(70 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Square thirty five in your head? Try this.", show="Square 35 in your head? Try this.", draw=s1),
    dict(say="Take the first digit, three. Multiply by the next number, four. Twelve.",
         show="Take the first digit, 3. Multiply by the next number, 4. 12.", draw=s2),
    dict(say="Then put twenty five after it: one thousand two hundred twenty five.",
         show="Then put 25 after it: 1225.", draw=s3),
    dict(say="Why? It's thirty times forty, plus five times five: twelve hundred plus twenty five.",
         show="Why? It's 30 × 40, plus 5 × 5: 1200 + 25.", draw=s4),
    dict(say="Try eighty five: eight times nine is seventy two. Seventy two twenty five.",
         show="Try 85: 8 × 9 is 72. 7225.", draw=s5),
    dict(say="Ends in five? Times the next number, then twenty five.",
         show="Ends in 5? Times the next number, then 25.", draw=s6),
]
