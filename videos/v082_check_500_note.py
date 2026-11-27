from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "money"
TITLE = "Look, tilt, touch: checking a ₹500 note"
WHITE, DARK = (255, 255, 255), (25, 30, 40)
NOTE, NOTE2, INK = (196, 196, 190), (170, 172, 168), (90, 95, 100)
GREEN, BLUE = (60, 190, 110), (70, 140, 235)


def mix(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def note(d, cx, cy, s=1.0):
    """A simple schematic of a banknote (not a replica)."""
    w, h = 450 * s, 190 * s
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], int(18 * s), fill=NOTE)
    d.rounded_rectangle([cx - w + 14 * s, cy - h + 14 * s, cx + w - 14 * s, cy + h - 14 * s], int(12 * s),
                        outline=NOTE2, width=max(2, int(4 * s)))
    # portrait area (a plain oval)
    d.ellipse([cx - 60 * s, cy - 110 * s, cx + 90 * s, cy + 110 * s], fill=NOTE2)
    # watermark window (blank area on the right)
    d.ellipse([cx + 180 * s, cy - 100 * s, cx + 330 * s, cy + 100 * s], fill=(214, 214, 208))
    text_c(d, (cx - 300 * s, cy - 110 * s), "₹500", font(int(54 * s) + 1, "bold"), INK)
    return w, h


def thread(d, cx, cy, s, col):
    for i in range(6):
        y0 = cy - 175 * s + i * 60 * s
        d.rectangle([cx + 120 * s, y0, cx + 136 * s, y0 + 34 * s], fill=col)


def s1(img, d, t, T, th):
    g = pop(prog(t, 0.1, 0.5))
    note(d, 540, 680, 1.0 * g + 0.01)
    text_c(d, (540, 360), "3 checks from the RBI", font(60, "bold"), th["accent"])
    if t > 1.0:
        text_c(d, (540, 1000), "LOOK  ·  TILT  ·  TOUCH", font(58, "bold"), WHITE)
    text_c(d, (540, 1150), "simple drawing, not a real note", font(32, "reg"), th["soft"])


def s2(img, d, t, T, th):
    k = ease(prog(t, 0.3, 0.8))
    # glow behind
    r = 300 * k + 1
    d.ellipse([740 - r, 680 - r, 740 + r, 680 + r], fill=(255, 245, 200, 50))
    note(d, 540, 680, 1.0)
    if t > 0.9:
        a = int(200 * ease(prog(t, 0.9, 0.6)))
        # watermark: a faint face outline and "500"
        d.ellipse([765, 600, 845, 700], outline=(120, 120, 115, a), width=5)
        text_c(d, (805, 745), "500", font(34, "bold"), (120, 120, 115, a))
    text_c(d, (540, 340), "1. LOOK: hold it to light", font(56, "bold"), th["accent"])
    if t > 1.4:
        text_c(d, (540, 990), "Gandhiji watermark appears", font(50, "bold"), WHITE)


def s3(img, d, t, T, th):
    text_c(d, (540, 340), "2. TILT it", font(62, "bold"), th["accent"])
    k = clamp((t - 0.4) / 1.4)
    tilt = 0.5 - 0.5 * __import__("math").cos(k * 3.1416)
    sy = 1.0 - 0.25 * tilt
    note(d, 540, 680, 1.0)
    col = mix(GREEN, BLUE, tilt)
    thread(d, 540, 680, 1.0, col)
    text_c(d, (540, 990), "security thread:", font(48, "semi"), WHITE)
    text_c(d, (380, 1080), "green", font(56, "bold"), GREEN)
    text_c(d, (540, 1080), "→", font(56, "sym"), WHITE)
    text_c(d, (700, 1080), "blue", font(56, "bold"), BLUE)


def s4(img, d, t, T, th):
    text_c(d, (540, 340), "Also changes colour:", font(56, "bold"), th["accent"])
    w, h = note(d, 540, 680, 1.0)
    k = clamp((t - 0.4) / 1.2)
    tilt = 0.5 - 0.5 * __import__("math").cos(k * 3.1416)
    col = mix(GREEN, BLUE, tilt)
    text_c(d, (540 + 300, 680 + 120), "₹500", font(64, "bold"), col)
    if t > 0.3:
        d.ellipse([540 + 170, 680 + 60, 540 + 430, 680 + 180], outline=WHITE, width=6)
    text_c(d, (540, 990), "₹500 at the bottom right", font(50, "bold"), WHITE)


def s5(img, d, t, T, th):
    text_c(d, (540, 340), "3. TOUCH the edges", font(58, "bold"), th["accent"])
    note(d, 540, 680, 1.0)
    for side in (-1, 1):
        x = 540 + side * 418
        for i in range(5):
            y = 560 + i * 55
            d.line([(x - 22, y), (x + 22, y - 18)], fill=INK, width=8)
    # finger
    k = (t * 0.8) % 1.0
    fy = 540 + 280 * k
    d.ellipse([90, fy - 30, 150, fy + 30], fill=(240, 190, 150))
    if t > 0.8:
        text_c(d, (540, 990), "5 raised bleed lines each side", font(48, "bold"), WHITE)
    if t > 1.5:
        text_c(d, (540, 1080), "made for visually impaired people", font(42, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    words = [("Look.", WHITE), ("Tilt.", GREEN), ("Touch.", th["accent"])]
    for i, (s, c) in enumerate(words):
        if t > 0.1 + 0.5 * i:
            g = pop(prog(t, 0.1 + 0.5 * i, 0.4))
            text_c(d, (540, 520 + i * 170), s, font(int(96 * g) + 1, "bold"), c)


SCENES = [
    dict(say="Got a five hundred rupee note? Here are three checks the R.B.I. lists.",
         show="Got a ₹500 note? Here are three checks the RBI lists.", draw=s1),
    dict(say="One, look. Hold it against light, and Mahatma Gandhi's watermark appears.", draw=s2),
    dict(say="Two, tilt. The security thread changes from green to blue.", draw=s3),
    dict(say="So does the five hundred, with the rupee sign, at the bottom right.",
         show="So does the ₹500 at the bottom right.", draw=s4),
    dict(say="Three, touch. Five raised bleed lines on the left and right help visually impaired people.", draw=s5),
    dict(say="Look, tilt, touch. Every note, every time.", draw=s6),
]
