import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "teen"
TITLE = "Did the whole class really notice?"
WHITE, DARK = (255, 255, 255), (25, 20, 40)
SKIN = [(240, 190, 150), (205, 150, 110), (225, 170, 130), (180, 125, 90)]
SHIRTS = [(120, 170, 255), (255, 200, 90), (140, 220, 160), (250, 250, 255), (200, 150, 255)]
CHAI = (170, 110, 60)


def person(d, x, y, s=1.0, skin=SKIN[0], shirt=SHIRTS[0], look=0, eyes=True, hair=(35, 25, 25)):
    d.rounded_rectangle([x - 55 * s, y + 40 * s, x + 55 * s, y + 170 * s], 30 * s, fill=shirt)
    d.ellipse([x - 45 * s, y - 50 * s, x + 45 * s, y + 40 * s], fill=skin)
    d.chord([x - 47 * s, y - 56 * s, x + 47 * s, y + 20 * s], 180, 360, fill=hair)
    if eyes:
        for ex in (-16, 16):
            d.ellipse([x + (ex - 6 + look) * s, y - 8 * s, x + (ex + 6 + look) * s, y + 6 * s], fill=DARK)


def spotlight(d, x, top, bottom, width, a=60):
    d.polygon([(x - 40, top), (x + 40, top), (x + width, bottom), (x - width, bottom)], fill=(255, 245, 200, a))


def s1(img, d, t, T, th):
    # Chintu-like student with a chai stain, imagined eyes everywhere
    spotlight(d, 540, 280, 1000, 260, 50 + int(30 * math.sin(t * 3)))
    person(d, 540, 680, 2.0, shirt=(250, 250, 255))
    k = ease(prog(t, 0.2, 0.5))
    d.ellipse([500, 820, 500 + 90 * k + 1, 820 + 70 * k + 1], fill=CHAI)
    if t > 0.9:
        import random
        rnd = random.Random(2)
        for j in range(8):
            g = pop(prog(t, 0.9 + j * 0.08, 0.3))
            ex = rnd.choice([rnd.randint(120, 300), rnd.randint(780, 960)])
            ey = rnd.randint(330, 980)
            r = int(38 * g) + 1
            d.ellipse([ex - r, ey - r * 0.6, ex + r, ey + r * 0.6], fill=WHITE, outline=DARK, width=3)
            d.ellipse([ex - r * 0.35, ey - r * 0.35, ex + r * 0.35, ey + r * 0.35], fill=DARK)
    if t > 1.8:
        text_c(d, (540, 1110), "Everyone noticed... right?", font(56, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s2(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    spotlight(d, 540, 280, 1000, int(300 * g) + 1, 80)
    person(d, 540, 760, 1.6, shirt=(250, 250, 255))
    d.ellipse([505, 870, 575, 925], fill=CHAI)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.4))
        d.rounded_rectangle([130, 1030, 950, 1170], 40, fill=th["accent"])
        text_c(d, (540, 1100), "the SPOTLIGHT EFFECT", font(int(58 * g2) + 1, "bold"), DARK)


def tshirt(d, x, y, s=1.0):
    d.polygon([(x - 80 * s, y), (x - 140 * s, y + 50 * s), (x - 110 * s, y + 100 * s), (x - 80 * s, y + 80 * s),
               (x - 80 * s, y + 220 * s), (x + 80 * s, y + 220 * s), (x + 80 * s, y + 80 * s),
               (x + 110 * s, y + 100 * s), (x + 140 * s, y + 50 * s), (x + 80 * s, y)], fill=(255, 150, 60))
    d.ellipse([x - 45 * s, y + 70 * s, x + 45 * s, y + 160 * s], fill=(255, 225, 120))
    text_c(d, (x, y + 115 * s), ":-/", font(int(40 * s), "bold"), DARK)


def s3(img, d, t, T, th):
    text_c(d, (540, 330), "a real study, 2000", font(44, "semi"), th["soft"])
    tshirt(d, 540, 430, 1.6)
    g = pop(prog(t, 0.6, 0.4))
    if g > 0:
        d.rounded_rectangle([200, 860, 880, 960], 30, fill=(255, 255, 255, 40))
        text_c(d, (540, 910), "embarrassing T-shirt", font(int(54 * g) + 1, "bold"), WHITE)
    if t > 1.2:
        text_c(d, (540, 1080), "worn into a room of students", font(46, "semi"), th["soft"])


def bar(d, x, label, val, col, k, th):
    base, hmax = 1010, 560
    h = hmax * val * k
    d.rounded_rectangle([x - 110, base - h, x + 110, base], 20, fill=col)
    text_c(d, (x, base - h - 50), f"{int(round(val * 100 * k))}%", font(64, "bold"), WHITE, stroke_width=4,
           stroke_fill=DARK)
    text_c(d, (x, base + 50), label, font(44, "bold"), WHITE)


def s4(img, d, t, T, th):
    d.line([(120, 1010), (960, 1010)], fill=WHITE, width=5)
    bar(d, 330, "guessed", 0.5, th["soft"], ease(prog(t, 0.1, 0.8)), th)
    bar(d, 750, "actually", 0.25, th["accent"], ease(prog(t, 1.4, 0.8)), th)
    text_c(d, (540, 320), "who noticed the shirt?", font(48, "semi"), WHITE)
    text_c(d, (540, 1130), "Gilovich et al., 2000", font(32, "reg"), th["soft"])


def s5(img, d, t, T, th):
    xs = [190, 430, 670, 900]
    for i, x in enumerate(xs):
        y = 760 + (i % 2) * 40
        person(d, x, y, 1.1, skin=SKIN[i], shirt=SHIRTS[i], look=-6 if i % 2 else 6)
        g = pop(prog(t, 0.2 + i * 0.25, 0.35))
        if g > 0:
            bx, by = x, y - 230
            r = int(100 * g) + 1
            d.ellipse([bx - r, by - r * 0.75, bx + r, by + r * 0.75], fill=WHITE)
            icon = ["exam", "homework", "lunch", "cricket"][i]
            text_c(d, (bx, by), icon, font(int(28 * g) + 1, "bold"), DARK)
    if t > 1.4:
        text_c(d, (540, 1110), "busy with their own day", font(56, "bold"), th["accent"], stroke_width=5,
               stroke_fill=DARK)


def s6(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.45))
    d.rounded_rectangle([90, 320, W - 90, 1080], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    spotlight(d, 540, 340, 760, int(60 * (1 - ease(prog(t, 0.2, 1.2)))) + 120, 40)
    person(d, 540, 520, 1.2 * g + 0.01, shirt=(250, 250, 255))
    if t > 0.6:
        g2 = pop(prog(t, 0.6, 0.45))
        text_c(d, (540, 820), "Your spotlight is", font(int(56 * g2) + 1, "bold"), WHITE)
        text_c(d, (540, 920), "smaller than you think", font(int(60 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Spilled chai on your shirt? Feels like the whole class noticed. Did they?", draw=s1),
    dict(say="Psychologists call this the spotlight effect.", draw=s2),
    dict(say="In one study, students wore an embarrassing T-shirt into a room.", draw=s3),
    dict(say="They guessed about half the people noticed it. Only about a quarter actually did.", draw=s4),
    dict(say="Most people are busy thinking about their own day.", draw=s5),
    dict(say="So next time, relax a little. Most people notice your slips less than you think.", draw=s6),
]
