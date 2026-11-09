"""Write the Instagram caption for each rendered video next to its MP4, for manual upload.

    python publish/captions.py            # every out/vNNN_*.mp4 -> out/vNNN_*_caption.txt
    python publish/captions.py v038       # print one caption

The caption is the text between 'Caption:' and 'Sources:' under '## vNNN Title' in docs/posts/*.md.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def caption_for(vid):
    """Find '## vNNN ...' in docs/posts/*.md and return the text between 'Caption:' and 'Sources:'."""
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "posts", "*.md")), reverse=True):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        m = re.search(rf"^## {re.escape(vid)}\b.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not m:
            continue
        c = re.search(r"^Caption:\s*\n(.*?)(?=^Sources?:|\Z)", m.group(1), re.M | re.S)
        if not c:
            return None
        cap = c.group(1).strip()
        tags = re.findall(r"#\w+", cap)
        if len(tags) > 30:
            raise ValueError(f"{vid}: caption has {len(tags)} hashtags; Instagram allows 30")
        if len(cap) > 2200:
            raise ValueError(f"{vid}: caption is {len(cap)} characters; Instagram allows 2200")
        return cap
    return None


def main(argv):
    if argv:
        cap = caption_for(argv[0])
        print(cap if cap else f"No caption found for {argv[0]}")
        return 0 if cap else 1
    missing = []
    for mp4 in sorted(glob.glob(os.path.join(ROOT, "out", "v*.mp4"))):
        name = os.path.splitext(os.path.basename(mp4))[0]
        cap = caption_for(name.split("_")[0])
        if not cap:
            missing.append(name)
            continue
        with open(os.path.join(ROOT, "out", f"{name}_caption.txt"), "w", encoding="utf-8") as f:
            f.write(cap + "\n")
    print("captions written" + (f"; missing: {', '.join(missing)}" if missing else ""))
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
