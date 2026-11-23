import math
from engine import font, text_c, ease, pop, prog, clamp, W

SERIES = "safe"
TITLE = "\"Update KYC or your account will be blocked\"?"
WHITE, DARK = (255, 255, 255), (20, 30, 40)
PHONE, SCREEN = (40, 45, 60), (235, 240, 250)
RED, GREEN, BUBBLE, LINK = (255, 95, 95), (90, 210, 120), (225, 230, 240), (40, 110, 220)


def phone(d, x, y, s=1.0):
    d.rounded_rectangle([x - 170 * s, y - 320 * s, x + 170 * s, y + 320 * s], int(40 * s), fill=PHONE)
    d.rounded_rectangle([x - 150 * s, y - 290 * s, x + 150 * s, y + 290 * s], int(28 * s), fill=SCREEN)


def sms(d, x, y, g=1.0):
    d.rounded_rectangle([x - 135, y - 110, x + 135, y + 110], 22, fill=BUBBLE)
    f = font(int(28 * g) + 1, "bold")
    text_c(d, (x, y - 70), "Account will be", f, DARK)
    text_c(d, (x, y - 30), "BLOCKED today.", f, RED)
    text_c(d, (x, y + 10), "Update KYC now:", f, DARK)
    text_c(d, (x, y + 60), "bit.ly/kyc-upd8", font(int(26 * g) + 1, "semi"), LINK)


def lock(d, x, y, s=1.0, col=RED):
    d.arc([x - 50 * s, y - 110 * s, x + 50 * s, y - 10 * s], 180, 360, fill=col, width=int(16 * s) + 1)
    d.line([(x - 50 * s, y - 60 * s), (x - 50 * s, y)], fill=col, width=int(16 * s) + 1)
    d.line([(x + 50 * s, y - 60 * s), (x + 50 * s, y)], fill=col, width=int(16 * s) + 1)
    d.rounded_rectangle([x - 75 * s, y - 10 * s, x + 75 * s, y + 100 * s], int(16 * s) + 1, fill=col)


def s1(img, d, t, T, th):
    sh = 6 * math.sin(t * 40) if t < 0.8 else 0
    phone(d, 540 + sh, 720)
    text_c(d, (540, 470), "SMS", font(30, "semi"), (90, 90, 110))
    if t > 0.3:
        sms(d, 540 + sh, 650, pop(prog(t, 0.3, 0.4)))
    if t > 1.8:
        g = pop(prog(t, 1.8, 0.4))
        d.rounded_rectangle([420, 820, 660, 900], 30, fill=LINK)
        text_c(d, (540, 860), "tap link?", font(int(36 * g) + 1, "bold"), WHITE)
    text_c(d, (540, 330), "Scary message!", font(62, "bold"), WHITE)


def s2(img, d, t, T, th):
    text_c(d, (540, 350), "Reserve Bank of India", font(58, "bold"), WHITE)
    g = pop(prog(t, 0.2, 0.45))
    d.rounded_rectangle([140, 470, 940, 640], 50, fill=th["accent"])
    text_c(d, (540, 555), "warns: KYC fraud", font(int(62 * g) + 1, "bold"), DARK)
    if t > 0.9:
        text_c(d, (540, 760), "calls · SMS · emails", font(52, "bold"), th["soft"])


def s3(img, d, t, T, th):
    text_c(d, (540, 350), "False urgency", font(64, "bold"), RED)
    k = ease(prog(t, 0.2, 1.0))
    lock(d, 540, 600, 1.0 + 0.15 * math.sin(t * 8) * (1 - k * 0.5))
    if t > 0.9:
        text_c(d, (540, 820), "\"freeze\"  \"block\"  \"close\"", font(50, "bold"), WHITE)
    if t > 1.5:
        g = pop(prog(t, 1.5, 0.4))
        d.rounded_rectangle([230, 930, 850, 1060], 50, fill=th["accent"])
        text_c(d, (540, 995), "so you panic", font(int(58 * g) + 1, "bold"), DARK)


def s4(img, d, t, T, th):
    text_c(d, (540, 350), "The link may...", font(60, "bold"), WHITE)
    items = [("install an app", 0.2), ("ask for OTP", 0.6), ("PIN · password", 1.0)]
    for i, (lab, st) in enumerate(items):
        if t > st:
            g = pop(prog(t, st, 0.4))
            y = 520 + i * 180
            d.rounded_rectangle([150, y - 70, 930, y + 70], 40, fill=(255, 255, 255, 30), outline=RED, width=5)
            text_c(d, (540, y), lab, font(int(54 * g) + 1, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 1080), "never share these", font(50, "bold"), RED)


def s5(img, d, t, T, th):
    text_c(d, (540, 350), "Don't click.", font(70, "bold"), RED)
    g = pop(prog(t, 0.4, 0.4))
    d.rounded_rectangle([140, 470, 940, 640], 40, fill=(255, 255, 255, 30), outline=GREEN, width=5)
    text_c(d, (540, 555), "✆ bank's official number", font(int(52 * g) + 1, "sym"), WHITE)
    if t > 1.0:
        g2 = pop(prog(t, 1.0, 0.4))
        d.rounded_rectangle([140, 700, 940, 870], 40, fill=(255, 255, 255, 30), outline=GREEN, width=5)
        text_c(d, (540, 785), "or visit your branch", font(int(52 * g2) + 1, "bold"), WHITE)
    if t > 1.6:
        text_c(d, (540, 990), "number from the bank's own website", font(40, "semi"), th["soft"])


def s6(img, d, t, T, th):
    d.rounded_rectangle([90, 330, W - 90, 1100], 50, fill=(255, 255, 255, 30), outline=th["accent"], width=6)
    g = pop(prog(t, 0.1, 0.45))
    text_c(d, (540, 520), "Panic message?", font(int(76 * g) + 1, "bold"), WHITE)
    if t > 0.5:
        g2 = pop(prog(t, 0.5, 0.45))
        text_c(d, (540, 680), "Pause.", font(int(86 * g2) + 1, "bold"), th["accent"])
    if t > 0.9:
        g3 = pop(prog(t, 0.9, 0.45))
        d.rounded_rectangle([230, 820, 850, 960], 50, fill=th["accent"])
        text_c(d, (540, 890), "Ask your bank.", font(int(64 * g3) + 1, "bold"), DARK)


SCENES = [
    dict(say="S.M.S.: Your bank account will be blocked today. Update K.Y.C. now. Click this link.",
         show="SMS: \"Your bank account will be blocked today. Update KYC now.\" Click this link.", draw=s1),
    dict(say="The Reserve Bank has warned about this fraud.", draw=s2),
    dict(say="Scammers create false urgency and threaten to freeze your account, so you panic.", draw=s3),
    dict(say="The link may install an app or ask for your O.T.P., PIN or password.",
         show="The link may install an app or ask for your OTP, PIN or password.", draw=s4),
    dict(say="Don't click. Call your bank's official number, or visit your branch.", draw=s5),
    dict(say="Panic message? Pause. Ask your bank.", draw=s6),
]
