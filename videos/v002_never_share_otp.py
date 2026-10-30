import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "Why should you never share an OTP?"
RED, GREEN, WHITE, DARK = (235, 70, 70), (70, 200, 120), (255, 255, 255), (25, 30, 45)


def phone(d, cx, cy, s=1.0, shake=0.0):
    cx += shake
    w, h = 300 * s, 560 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 46 * s, fill=DARK, outline=(200, 210, 230), width=6)
    d.rounded_rectangle([cx - w / 2 + 16 * s, cy - h / 2 + 40 * s, cx + w / 2 - 16 * s, cy + h / 2 - 40 * s], 26 * s,
                        fill=(235, 240, 250))
    d.rounded_rectangle([cx - 40 * s, cy - h / 2 + 14 * s, cx + 40 * s, cy - h / 2 + 26 * s], 6, fill=(90, 95, 110))
    return cx, cy, w, h


def s1(img, d, t, T, th):
    shake = math.sin(t * 40) * 6 if (t % 1.0) < 0.5 else 0
    cx, cy, w, h = phone(d, 540, 620, 1.0, shake)
    # ringing waves
    for k in range(3):
        r = 190 + ((t * 120 + k * 50) % 150)
        a = int(200 * (1 - (r - 190) / 150))
        d.arc([cx - r - 40, cy - r, cx + r + 40, cy + r], 300, 350, fill=th["accent"] + (a,), width=8)
        d.arc([cx - r - 40, cy - r, cx + r + 40, cy + r], 190, 240, fill=th["accent"] + (a,), width=8)
    d.ellipse([cx - 60, cy - 200, cx + 60, cy - 80], fill=(180, 190, 210))
    text_c(d, (cx, cy - 140), "?", font(80, "bold"), DARK)
    text_c(d, (cx, cy - 30), "\"Bank Helpline\"", font(34, "bold"), DARK)
    text_c(d, (cx, cy + 15), "+91 98XXX XXXXX", font(28, "reg"), (90, 95, 110))
    d.ellipse([cx - 110, cy + 150, cx - 30, cy + 230], fill=RED)
    d.ellipse([cx + 30, cy + 150, cx + 110, cy + 230], fill=GREEN)
    # OTP sms notification pops in
    p = pop(prog(t, 1.6, 0.4))
    if p > 0:
        y = 950
        d.rounded_rectangle([140, y, 940, y + 190 * p], 30, fill=(255, 255, 255, 245), outline=th["accent"], width=5)
        if p > 0.8:
            text_c(d, (180, y + 50), "SMS · YourBank", font(30, "semi"), (90, 95, 110), anchor="lm")
            text_c(d, (180, y + 115), "OTP: 482916. Do NOT share.", font(44, "bold"), DARK, anchor="lm")


def s2(img, d, t, T, th):
    cx, cy, w, h = phone(d, 540, 640, 0.8)
    text_c(d, (cx, cy - 40), "482916", font(56, "bold"), DARK)
    g = pop(prog(t, 0.15, 0.4))
    if g > 0:
        text_c(d, (840, 380), "?", font(int(260 * g) + 1, "bold"), th["accent"], stroke_width=8, stroke_fill=DARK)


def s3(img, d, t, T, th):
    cx, cy, w, h = phone(d, 540, 640, 0.8)
    text_c(d, (cx, cy - 40), "482916", font(56, "bold"), DARK)
    g = pop(prog(t, 0.0, 0.35))
    sz = int(170 * (2.2 - 1.2 * g))
    # stamp
    f = font(max(sz, 10), "bold")
    tw = d.textlength("NEVER", font=f)
    box = [W / 2 - tw / 2 - 40, 600 - sz * 0.65, W / 2 + tw / 2 + 40, 600 + sz * 0.65]
    d.rounded_rectangle(box, 30, outline=RED + (int(255 * clamp(g)),), width=14, fill=(255, 255, 255, int(220 * clamp(g))))
    text_c(d, (W / 2, 600), "NEVER", f, RED + (int(255 * clamp(g)),))


def key(d, x, y, s, col):
    d.ellipse([x - 70 * s, y - 70 * s, x + 70 * s, y + 70 * s], fill=col)
    d.ellipse([x - 28 * s, y - 28 * s, x + 28 * s, y + 28 * s], fill=(0, 0, 0, 0))
    d.rectangle([x + 60 * s, y - 18 * s, x + 260 * s, y + 18 * s], fill=col)
    d.rectangle([x + 200 * s, y + 18 * s, x + 230 * s, y + 65 * s], fill=col)
    d.rectangle([x + 150 * s, y + 18 * s, x + 175 * s, y + 50 * s], fill=col)
    text_c(d, (x + 150 * s, y - 50 * s), "OTP", font(int(46 * s), "bold"), col)


def s4(img, d, t, T, th):
    # vault/account box on the right
    vx, vy = 700, 660
    d.rounded_rectangle([vx - 170, vy - 230, vx + 170, vy + 230], 36, fill=(240, 240, 250), outline=WHITE, width=6)
    text_c(d, (vx, vy - 170), "YOUR ACCOUNT", font(32, "bold"), DARK)
    opened = t > 2.0
    # lock
    ly = vy + 50
    if opened:
        d.arc([vx - 60, ly - 150, vx + 60, ly - 30], 180, 300, fill=(120, 120, 140), width=22)
    else:
        d.arc([vx - 60, ly - 120, vx + 60, ly], 180, 360, fill=(120, 120, 140), width=22)
    d.rounded_rectangle([vx - 90, ly - 60, vx + 90, ly + 80], 18, fill=th["accent"])
    d.ellipse([vx - 16, ly - 10, vx + 16, ly + 22], fill=DARK)
    # key slides in
    k = ease(prog(t, 0.3, 1.6))
    kx = -260 + (vx - 330 + 260) * k
    key(d, kx, ly + 10, 1.0, th["accent"] if not opened else GREEN)
    if opened:
        for j in range(3):  # money flying out
            p = clamp((t - 2.1 - j * 0.35) / 1.2)
            if p <= 0: continue
            x, y = vx + 60 + 170 * p, vy + 140 - 300 * p + 120 * p * p
            d.rounded_rectangle([x - 70, y - 38, x + 70, y + 38], 10, fill=(130, 210, 140), outline=(40, 110, 60), width=4)
            text_c(d, (x, y), "₹", font(48, "sym"), (40, 110, 60))
        g = pop(prog(t, 2.2, 0.4))
        text_c(d, (W / 2, 1060), "Payment approved. Not by you!", font(int(50 * g) + 1, "bold"), RED,
               stroke_width=5, stroke_fill=DARK)


def icon_call(d, x, y):
    d.rounded_rectangle([x - 70, y - 70, x + 70, y + 70], 30, fill=(90, 160, 255))
    d.arc([x - 40, y - 40, x + 40, y + 40], 110, 250, fill=WHITE, width=22)


def icon_sms(d, x, y):
    d.rounded_rectangle([x - 70, y - 70, x + 70, y + 70], 30, fill=(255, 190, 70))
    d.rounded_rectangle([x - 45, y - 35, x + 45, y + 25], 14, fill=WHITE)
    d.polygon([(x - 20, y + 20), (x - 30, y + 45), (x + 2, y + 22)], fill=WHITE)


def icon_wa(d, x, y):
    d.rounded_rectangle([x - 70, y - 70, x + 70, y + 70], 30, fill=(60, 200, 110))
    d.ellipse([x - 42, y - 42, x + 42, y + 42], outline=WHITE, width=10)
    d.polygon([(x - 38, y + 22), (x - 50, y + 52), (x - 18, y + 40)], fill=WHITE)


def cross(d, x, y, k):
    if k <= 0: return
    r = 80 * k
    d.line([(x - r, y - r), (x + r, y + r)], fill=RED, width=16)
    d.line([(x - r, y + r), (x + r, y - r)], fill=RED, width=16)


def s5(img, d, t, T, th):
    g = pop(prog(t, 0.05, 0.4))
    # shield
    cx, cy, s = 540, 560, g
    pts = [(cx, cy - 230 * s), (cx + 190 * s, cy - 150 * s), (cx + 170 * s, cy + 90 * s), (cx, cy + 230 * s),
           (cx - 170 * s, cy + 90 * s), (cx - 190 * s, cy - 150 * s)]
    d.polygon(pts, fill=(240, 245, 255), outline=WHITE)
    text_c(d, (cx, cy - 60 * s), "BANKS", font(int(52 * s) + 1, "bold"), DARK)
    text_c(d, (cx, cy + 5 * s), "& RBI", font(int(52 * s) + 1, "bold"), DARK)
    text_c(d, (cx, cy + 80 * s), "never ask", font(int(40 * s) + 1, "semi"), RED)
    xs = [260, 540, 820]
    for j, (fn, x) in enumerate(zip([icon_call, icon_sms, icon_wa], xs)):
        if t < 1.5 + j * 0.45: continue
        fn(d, x, 1000)
        cross(d, x, 1000, pop(prog(t, 1.6 + j * 0.45, 0.3)))


def s6(img, d, t, T, th):
    # hang-up button
    g = pop(prog(t, 0.05, 0.4))
    d.ellipse([540 - 130 * g, 470 - 130 * g, 540 + 130 * g, 470 + 130 * g], fill=RED)
    d.arc([540 - 70 * g, 450 - 40 * g, 540 + 70 * g, 450 + 60 * g], 200, 340, fill=WHITE, width=int(26 * g) + 1)
    text_c(d, (540, 650), "Hang up", font(60, "bold"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        # parent + child icons
        for x, r, col in [(470, 70, (250, 200, 160)), (610, 52, (240, 190, 150))]:
            rr = r * g2
            d.ellipse([x - rr, 760 - rr * 1.6 + 80, x + rr, 760 + 80 + rr * 0.4], fill=col)
            d.rounded_rectangle([x - rr * 1.2, 760 + 110, x + rr * 1.2, 760 + 110 + rr * 2], int(rr * 0.6) + 1, fill=th["accent"])
        text_c(d, (540, 1050), "Tell a parent", font(56, "bold"), WHITE)
    if t > 1.8:
        d.rounded_rectangle([110, 1110, 970, 1190], 24, fill=(255, 255, 255, 235))
        text_c(d, (540, 1150), "Cyber fraud helpline: 1930  ·  cybercrime.gov.in", font(34, "bold"), DARK)


SCENES = [
    dict(say="Someone calls saying they're from your bank, and asks for the O.T.P. you just got.",
         show="Someone calls saying they're from your bank, and asks for the OTP you just got.", draw=s1),
    dict(say="Should you share it?", draw=s2),
    dict(say="Never.", draw=s3),
    dict(say="An O.T.P. is like a one-time key. Whoever has it can approve a payment, or log in as you.",
         show="An OTP is like a one-time key. Whoever has it can approve a payment, or log in as you.", draw=s4),
    dict(say="Real banks and the R.B.I. never ask for your O.T.P. Not by call, S.M.S., or WhatsApp.",
         show="Real banks and the RBI never ask for your OTP. Not by call, SMS, or WhatsApp.", draw=s5),
    dict(say="If anyone asks, it's a scam. Hang up, and tell a parent.", draw=s6),
]
