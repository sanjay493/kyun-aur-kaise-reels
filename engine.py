"""Reel engine: TTS voice + 2D animated scenes + karaoke subtitles -> 1080x1920 MP4.

A video module defines SERIES (theme key) and SCENES: list of dicts
  {"say": text spoken, "show": optional subtitle text (defaults to say), "draw": fn(layer, draw, t, T)}
draw() paints the stage area of an RGBA layer; t = seconds into scene, T = scene length.
"""
import math, os, re, subprocess, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

W, H, FPS = 1080, 1920, 30
HANDLE = "@kyun.aur.kaise"
VOICE, SPEED = "hf_beta", 1.0
HERE = os.path.dirname(os.path.abspath(__file__))

FD = "/usr/share/fonts/truetype/"
def font(size, kind="bold"):
    path = {"bold": FD + "google-fonts/Poppins-Bold.ttf",
            "semi": FD + "google-fonts/Poppins-SemiBold.ttf",
            "reg": FD + "google-fonts/Poppins-Medium.ttf",
            "sym": FD + "dejavu/DejaVuSans-Bold.ttf"}[kind]
    if not os.path.exists(path):
        path = FD + "dejavu/DejaVuSans-Bold.ttf"
    return ImageFont.truetype(path, size)

THEMES = {
    "maths":  dict(name="MATHS WITHOUT FEAR", bg1=(28, 36, 92), bg2=(52, 30, 110), accent=(255, 205, 60),
                   ink=(255, 255, 255), soft=(170, 180, 230), grid=True),
    "safe":   dict(name="SMART & SAFE", bg1=(10, 70, 80), bg2=(20, 40, 70), accent=(255, 140, 60),
                   ink=(255, 255, 255), soft=(160, 215, 215), grid=False),
    "science": dict(name="SCIENCE AROUND US", bg1=(12, 60, 45), bg2=(20, 35, 70), accent=(120, 230, 140),
                    ink=(255, 255, 255), soft=(170, 220, 190), grid=False),
    "teen":   dict(name="TEEN TALK", bg1=(90, 30, 70), bg2=(40, 25, 80), accent=(255, 120, 170),
                   ink=(255, 255, 255), soft=(230, 180, 210), grid=False),
    "study":  dict(name="STUDY SMART", bg1=(20, 55, 95), bg2=(35, 30, 75), accent=(110, 215, 255),
                   ink=(255, 255, 255), soft=(175, 210, 240), grid=False),
    "english": dict(name="ENGLISH MADE EASY", bg1=(105, 48, 28), bg2=(55, 28, 70), accent=(255, 210, 110),
                    ink=(255, 255, 255), soft=(240, 205, 175), grid=False),
}

# ---------- easing ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def pop(x):  # overshoot ease for "pop in"
    x = clamp(x); c = 1.7
    return max(0.0, 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2)
def prog(t, start, dur): return clamp((t - start) / dur)

def text_c(d, xy, s, f, fill, anchor="mm", **kw):
    d.text(xy, s, font=f, fill=fill, anchor=anchor, **kw)

# ---------- background ----------
_bg_cache = {}
def background(theme):
    key = theme["name"]
    if key in _bg_cache: return _bg_cache[key]
    y = np.linspace(0, 1, H)[:, None, None]
    c1, c2 = np.array(theme["bg1"]), np.array(theme["bg2"])
    arr = (c1 * (1 - y) + c2 * y).repeat(W, axis=1).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img, "RGBA")
    if theme["grid"]:
        for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 14), width=2)
        for yy in range(0, H, 60): d.line([(0, yy), (W, yy)], fill=(255, 255, 255, 14), width=2)
    rnd = random.Random(7)
    for _ in range(14):  # soft bokeh dots
        cx, cy, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(30, 110)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 10))
    _bg_cache[key] = img
    return img

# ---------- header / chrome ----------
def chrome(d, theme, frac):
    # progress bar
    d.rounded_rectangle([60, 70, W - 60, 82], 6, fill=(255, 255, 255, 40))
    d.rounded_rectangle([60, 70, 60 + max(12, int((W - 120) * frac)), 82], 6, fill=theme["accent"])
    f = font(34, "semi")
    tw = d.textlength(theme["name"], font=f)
    d.rounded_rectangle([W / 2 - tw / 2 - 30, 115, W / 2 + tw / 2 + 30, 175], 30, fill=theme["accent"])
    text_c(d, (W / 2, 146), theme["name"], f, (25, 25, 40))
    text_c(d, (W / 2, 215), HANDLE, font(30, "reg"), theme["soft"])

# ---------- character: "Chintu" ----------
def character(d, cx, cy, mouth, blink, theme, s=1.0, talk=0.0):
    """talk (0-1): how animated Chintu is right now; lifts the eyebrows and nods the head slightly."""
    skin, hair, shirt = (240, 190, 150), (35, 25, 25), (250, 250, 255)
    r = 95 * s
    body_cy = cy
    cy = cy - 6 * s * talk  # small nod up while speaking (body stays put)
    # body / uniform
    by = body_cy
    d.rounded_rectangle([cx - 120 * s, by + 70 * s, cx + 120 * s, by + 260 * s], 60 * s, fill=shirt)
    d.polygon([(cx - 30 * s, by + 80 * s), (cx, by + 135 * s), (cx + 30 * s, by + 80 * s)], fill=theme["accent"])  # tie/collar
    d.rectangle([cx - 22 * s, cy + 60 * s, cx + 22 * s, by + 90 * s], fill=skin)
    # head
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin)
    d.chord([cx - r - 4 * s, cy - r - 12 * s, cx + r + 4 * s, cy + r * 0.55], 180, 360, fill=hair)
    d.ellipse([cx - r - 6 * s, cy - 18 * s, cx - r + 22 * s, cy + 22 * s], fill=skin)  # ears
    d.ellipse([cx + r - 22 * s, cy - 18 * s, cx + r + 6 * s, cy + 22 * s], fill=skin)
    # eyes
    for ex in (-34, 34):
        x = cx + ex * s
        if blink:
            d.line([x - 14 * s, cy + 2 * s, x + 14 * s, cy + 2 * s], fill=(30, 30, 30), width=int(5 * s))
        else:
            d.ellipse([x - 15 * s, cy - 15 * s, x + 15 * s, cy + 17 * s], fill=(255, 255, 255))
            d.ellipse([x - 8 * s, cy - 7 * s, x + 8 * s, cy + 11 * s], fill=(30, 30, 30))
            d.ellipse([x - 3 * s, cy - 5 * s, x + 2 * s, cy], fill=(255, 255, 255))
    # eyebrows: rest low, lift when talking
    lift = 3 * s * talk
    for ex in (-34, 34):
        x = cx + ex * s
        o = -1 if ex < 0 else 1  # outer end sits a touch lower than the inner end
        d.line([(x + 14 * s * o, cy - 17 * s - lift), (x - 14 * s * o, cy - 20 * s - lift)], fill=hair, width=int(5 * s))
    d.ellipse([cx - 62 * s, cy + 22 * s, cx - 42 * s, cy + 36 * s], fill=(245, 150, 140))  # cheeks
    d.ellipse([cx + 42 * s, cy + 22 * s, cx + 62 * s, cy + 36 * s], fill=(245, 150, 140))
    # mouth
    mh = 4 + 26 * mouth
    d.rounded_rectangle([cx - 20 * s, cy + 40 * s, cx + 20 * s, cy + (40 + mh) * s], int(10 * s),
                        fill=(120, 40, 50))

# ---------- subtitles ----------
def words_of(s): return s.split()

def subtitle(d, words, idx, theme, y_top=1240):
    # show the 5-7 word group containing idx
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if len(cur) >= 7 or w.endswith(('.', '?', '!', ',')) and len(cur) >= 3:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    g = next((g for g in groups if idx in g), groups[-1] if idx >= len(words) else groups[0])
    f = font(68, "bold")
    lines, line, wmax = [], [], 950
    for i in g:
        trial = " ".join(words[j] for j in line + [i])
        if line and d.textlength(trial, font=f) > wmax:
            lines.append(line); line = [i]
        else:
            line.append(i)
    lines.append(line)
    y = y_top
    for ln in lines:
        txt = " ".join(words[j] for j in ln)
        x = W / 2 - d.textlength(txt, font=f) / 2
        for j in ln:
            w = words[j] + " "
            col = theme["accent"] if j == idx else theme["ink"]
            d.text((x, y), w, font=f, fill=col, stroke_width=7, stroke_fill=(15, 15, 30))
            x += d.textlength(w, font=f)
        y += 92

# ---------- audio ----------
_kokoro = None
def tts(text, path):
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(os.path.join(HERE, "models/kokoro-v1.0.onnx"), os.path.join(HERE, "models/voices-v1.0.bin"))
    s, sr = _kokoro.create(text, voice=VOICE, speed=SPEED, lang="en-us")
    sf.write(path, s, sr)
    return s, sr

def music_bed(dur, sr=24000):
    t = np.arange(int(dur * sr)) / sr
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    out = np.zeros_like(t)
    beat = 2.0
    for k, ch in enumerate(chords * int(dur / (beat * 4) + 2)):
        a = k * beat
        if a > dur: break
        m = (t >= a) & (t < a + beat + 0.5)
        tt = t[m] - a
        env = np.minimum(tt / 0.3, 1) * np.exp(-tt * 0.6)
        for fq in ch:
            out[m] += env * np.sin(2 * np.pi * fq * tt) * 0.25
        # soft pluck on each half beat
        for p in (0, 1.0):
            m2 = (t >= a + p) & (t < a + p + 0.4)
            tp = t[m2] - a - p
            out[m2] += np.sin(2 * np.pi * ch[(k + int(p)) % 3] * 2 * tp) * np.exp(-tp * 9) * 0.3
    return out / (np.abs(out).max() + 1e-9)

def pop_sfx(sr=24000):
    t = np.arange(int(0.18 * sr)) / sr
    f = 900 - 3000 * t
    return np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t * 28)

# ---------- render ----------
def render(module, out_path, workdir):
    os.makedirs(workdir, exist_ok=True)
    theme = THEMES[module.SERIES]
    scenes = module.SCENES
    sr = 24000
    voice_parts, timing = [], []
    PAD_HEAD, PAD_TAIL = 0.15, 0.35
    for i, sc in enumerate(scenes):
        s, sr = tts(sc["say"], os.path.join(workdir, f"v{i}.wav"))
        # trim near-silence at ends for tighter sync
        nz = np.where(np.abs(s) > 0.01)[0]
        s = s[max(0, nz[0] - 600): nz[-1] + 1200] if len(nz) else s
        seg = np.concatenate([np.zeros(int(PAD_HEAD * sr)), s, np.zeros(int(PAD_TAIL * sr))])
        voice_parts.append(seg)
        timing.append(dict(T=len(seg) / sr, speech0=PAD_HEAD, speech1=PAD_HEAD + len(s) / sr, audio=seg))
    total = sum(x["T"] for x in timing)

    # audio mix
    voice = np.concatenate(voice_parts)
    mix = voice * 0.95 + music_bed(len(voice) / sr, sr)[:len(voice)] * 0.06
    sfx, pos = pop_sfx(sr), 0
    for tm in timing:
        p = int(pos * sr); mix[p:p + len(sfx)] += sfx[:len(mix) - p] * 0.25
        pos += tm["T"]
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    sf.write(os.path.join(workdir, "mix.wav"), mix.astype(np.float32), sr)

    bg = background(theme)
    elapsed, files = 0.0, []
    for i, (sc, tm) in enumerate(zip(scenes, timing)):
        words = words_of(sc.get("show", sc["say"]))
        aud = tm["audio"]
        nfr = int(round(tm["T"] * FPS))
        cw = np.cumsum([len(w) + 1 for w in words]); cw = cw / cw[-1]
        tmp = os.path.join(workdir, f"s{i}.tmp.mp4"); fin = os.path.join(workdir, f"s{i}.mp4")
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset",
                                 "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for fi in range(nfr):
            t = fi / FPS
            gt = elapsed + t
            frame = bg.copy()
            # stage layer
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sd = ImageDraw.Draw(layer, "RGBA")
            sc["draw"](layer, sd, t, tm["T"], theme)
            a = ease(t / 0.22)
            if a < 1:
                alpha = layer.getchannel("A").point(lambda v: int(v * a))
                layer.putalpha(alpha)
                layer = layer.transform(layer.size, Image.AFFINE, (1, 0, 0, 0, 1, -40 * (1 - a)))
            frame.paste(layer, (0, 0), layer)
            d = ImageDraw.Draw(frame, "RGBA")
            chrome(d, theme, gt / total)
            # word index from speech progress
            sp = (t - tm["speech0"]) / (tm["speech1"] - tm["speech0"])
            idx = int(np.searchsorted(cw, sp)) if sp >= 0 else 0
            if sp > 1.02: idx = len(words)  # finished: no highlight
            subtitle(d, words, min(idx, len(words)) if sp <= 1.02 else -1, theme)
            # mouth from loudness
            c = int(t * sr); seg = aud[max(0, c - 600): c + 600]
            loud = float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0
            blink = (gt % 3.3) < 0.12
            c2 = int(max(0, t - 0.25) * sr); seg2 = aud[max(0, c2 - 3000): c2 + 3000]  # slower envelope
            talk = clamp(float(np.sqrt(np.mean(seg2 ** 2))) * 7) if len(seg2) else 0
            character(d, 170, 1640, clamp(loud * 9), blink, theme, 0.85, talk)
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait() != 0: raise RuntimeError("ffmpeg failed on scene %d" % i)
        os.replace(tmp, fin); files.append(fin)
        elapsed += tm["T"]

    lst = os.path.join(workdir, "list.txt")
    with open(lst, "w") as f:
        for p in files: f.write(f"file '{os.path.abspath(p)}'\n")
    silent = os.path.join(workdir, "silent.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    tmp = out_path[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", os.path.join(workdir, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out_path)
    return total


def still(module, sc_index, t, out_png):
    """Draw a single frame for checking (no audio)."""
    theme = THEMES[module.SERIES]
    sc = module.SCENES[sc_index]
    frame = background(theme).copy()
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sc["draw"](layer, ImageDraw.Draw(layer, "RGBA"), t, 5.0, theme)
    frame.paste(layer, (0, 0), layer)
    d = ImageDraw.Draw(frame, "RGBA")
    chrome(d, theme, 0.4)
    words = words_of(sc.get("show", sc["say"]))
    subtitle(d, words, 2, theme)
    character(d, 170, 1640, 0.5, False, theme, 0.85, 1.0)
    frame.save(out_png)
