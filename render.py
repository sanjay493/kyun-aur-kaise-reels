"""Render one or more video scripts to MP4.

Usage:
    python render.py videos/v001_triangle_180.py [videos/v002_....py ...]
    python render.py --all          # every script in videos/
    python render.py --still videos/v001_triangle_180.py   # contact sheet of key frames for checking

Output goes to out/<script name>.mp4 (and out/<script name>_sheet.png for --still).
"""
import glob, importlib.util, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import engine  # noqa: E402


def load(path):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return name, mod


def sheet(name, mod):
    from PIL import Image
    paths = []
    for i in range(len(mod.SCENES)):
        p = os.path.join(ROOT, "work", f"{name}_still{i}.png")
        engine.still(mod, i, 2.5, p)
        paths.append(p)
    ims = [Image.open(p).resize((360, 640)) for p in paths]
    cols = 4
    rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (360 * cols, 640 * rows), "white")
    for k, im in enumerate(ims):
        s.paste(im, ((k % cols) * 360, (k // cols) * 640))
    out = os.path.join(ROOT, "out", f"{name}_sheet.png")
    s.save(out)
    return out


def main(argv):
    still = "--still" in argv
    argv = [a for a in argv if a != "--still"]
    if "--all" in argv:
        argv = sorted(glob.glob(os.path.join(ROOT, "videos", "v*.py")))
    if not argv:
        print(__doc__); return 1
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "work"), exist_ok=True)
    for path in argv:
        name, mod = load(path)
        if still:
            print("sheet:", sheet(name, mod))
        else:
            out = os.path.join(ROOT, "out", f"{name}.mp4")
            dur = engine.render(mod, out, os.path.join(ROOT, "work", name))
            print(f"{out}  {dur:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
