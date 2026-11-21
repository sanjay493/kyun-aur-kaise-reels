from PIL import Image, ImageDraw
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "science"
TITLE = "Why is AMBULANCE written backwards?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
VAN, VAN2, RED = (245, 245, 245), (190, 195, 205), (230, 60, 60)
MIRROR, CAR = (190, 225, 245), (90, 140, 220)
GREEN = (110, 220, 140)

_cache = {}


def word_img(text, size, col, flip=False):
    """Render `text` to an RGBA image; flip=True mirrors it left-right."""
    key = (text, size, col, flip)
    if key not in _cache:
        f = font(size, "bold")
        tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        w = int(tmp.textlength(text, font=f)) + 20
        im = Image.new("RGBA", (w, size + 30), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 5), text, font=f, fill=col)
        _cache[key] = im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im
    return _cache[key]


def paste_c(img, im, x, y, scale=1.0):
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))))
    img.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))


def van_front(d, x, y, s=1.0):
    d.rounded_rectangle([x - 380 * s, y - 230 * s, x + 380 * s, y + 230 * s], int(50 * s), fill=VAN, outline=VAN2, width=6)
    d.rounded_rectangle([x - 330 * s, y - 190 * s, x + 330 * s, y - 30 * s], int(30 * s), fill=(120, 170, 210))
    d.rectangle([x - 380 * s, y + 20 * s, x + 380 * s, y + 70 * s], fill=RED)
    for dx in (-290, 290):
        d.ellipse([x + (dx - 45) * s, y + 110 * s, x + (dx + 45) * s, y + 200 * s], fill=(255, 230, 120))


def s1(img, d, t, T, th):
    van_front(d, 540, 700)
    g = pop(prog(t, 0.4, 0.5))
    paste_c(img, word_img("AMBULANCE", 76, RED, flip=True), 540, 640 + 0, g * 0.95 + 0.01)
    if t > 1.4:
        g2 = pop(prog(t, 1.4, 0.4))
        text_c(d, (540, 1060), "Backwards. Why?", font(int(72 * g2) + 1, "bold"), th["accent"])
    text_c(d, (540, 360), "Front of an ambulance", font(56, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Hold a word to a mirror", font(56, "bold"), WHITE)
    paste_c(img, word_img("BOOK", 110, WHITE), 540, 520)
    d.rounded_rectangle([170, 640, 910, 900], 30, fill=MIRROR + (90,), outline=WHITE, width=6)
    k = ease(prog(t, 0.4, 0.8))
    if k > 0:
        paste_c(img, word_img("BOOK", 110, (220, 240, 255), flip=True), 540, 770, k)
    if t > 1.4:
        text_c(d, (540, 1020), "left ↔ right", font(64, "sym"), th["accent"])


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "Only the sides swap", font(58, "bold"), th["accent"])
    paste_c(img, word_img("R", 220, WHITE), 330, 680)
    paste_c(img, word_img("R", 220, (220, 240, 255), flip=True), 750, 680)
    d.line([(540, 480), (540, 880)], fill=MIRROR, width=10)
    if t > 0.8:
        g = pop(prog(t, 0.8, 0.4))
        text_c(d, (540, 1000), "not upside down", font(int(60 * g) + 1, "bold"), WHITE)


def s4(img, d, t, T, th):
    # car ahead, driver looking into rear-view mirror; ambulance behind
    d.rounded_rectangle([280, 420, 800, 640], 50, fill=CAR)
    d.rounded_rectangle([330, 360, 750, 460], 40, fill=CAR)
    d.rounded_rectangle([340, 295, 740, 385], 20, fill=MIRROR, outline=WHITE, width=6)
    k = ease(prog(t, 0.6, 0.8))
    paste_c(img, word_img("AMBULANCE", 42, RED), 540, 340, k + 0.01)
    van_front(d, 540, 950, 0.55 + 0.1 * ease(prog(t, 0.0, 1.5)))
    paste_c(img, word_img("AMBULANCE", 44, RED, flip=True), 540, 935)
    if t > 1.4:
        text_c(d, (540, 700), "rear-view mirror ↑", font(44, "sym"), th["accent"])


def s5(img, d, t, T, th):
    paste_c(img, word_img("AMBULANCE", 84, RED, flip=True), 540, 450)
    text_c(d, (540, 560), "↓ mirror flips it ↓", font(48, "sym"), th["soft"])
    k = ease(prog(t, 0.4, 0.6))
    d.rounded_rectangle([110, 620, 970, 820], 30, fill=MIRROR + (90,), outline=WHITE, width=6)
    if k > 0:
        paste_c(img, word_img("AMBULANCE", 84, RED), 540, 720, k)
    if t > 1.2:
        g = pop(prog(t, 1.2, 0.4))
        d.rounded_rectangle([230, 900, 850, 1040], 50, fill=GREEN)
        text_c(d, (540, 970), "Give way!", font(int(66 * g) + 1, "bold"), DARK)


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Written backwards", font(int(70 * g) + 1, "bold"), WHITE)
    if t > 0.7:
        g2 = pop(prog(t, 0.7, 0.45))
        text_c(d, (540, 720), "so a mirror", font(int(70 * g2) + 1, "bold"), th["accent"])
        text_c(d, (540, 820), "reads it forwards.", font(int(70 * g2) + 1, "bold"), th["accent"])


SCENES = [
    dict(say="Why is the word ambulance written backwards on the front of an ambulance?", draw=s1),
    dict(say="Hold a word up to a mirror. Left becomes right, and right becomes left.", draw=s2),
    dict(say="But it's not upside down. Only the sides swap.", draw=s3),
    dict(say="The driver ahead sees the ambulance in the rear-view mirror.", draw=s4),
    dict(say="The mirror flips the letters back, so the driver reads ambulance and gives way.", draw=s5),
    dict(say="Written backwards, so a mirror reads it forwards.", draw=s6),
]
