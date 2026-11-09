"""Render new videos and publish them to Instagram as Reels.

Used by .github/workflows/instagram.yml; can also be run by hand.

    python publish/instagram.py queue          # render scripts not yet in the queue, upload MP4s, add rows
    python publish/instagram.py post           # publish the oldest queued video
    python publish/instagram.py caption v038   # print the caption that would be posted (no network)
    python publish/instagram.py status         # show the queue

State lives in docs/instagram.csv (id, file, status, attempts, media_id, permalink, posted_at, note).
Status: queued -> posted, or failed after MAX_ATTEMPTS. "skip" rows are never posted.
To re-post or retry something, set its status back to "queued" (and attempts to 0).

Environment (post):
    IG_ACCESS_TOKEN   long-lived Instagram User access token (Instagram API with Instagram Login)
    GITHUB_REPOSITORY owner/repo, used to build the public video URL (set automatically in Actions)
    IG_API_VERSION    optional, default v24.0
Environment (queue):
    GH_TOKEN          token the gh CLI uses to upload release assets (set in the workflow)
"""
import csv, datetime as dt, glob, json, os, re, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "docs", "instagram.csv")
FIELDS = ["id", "file", "status", "attempts", "media_id", "permalink", "posted_at", "note"]
RELEASE_TAG = "reels"          # one rolling GitHub Release holds every MP4
MAX_ATTEMPTS = 3
API = "https://graph.instagram.com/" + os.environ.get("IG_API_VERSION", "v24.0")


# ---------- state ----------

def load_state():
    if not os.path.exists(STATE):
        return []
    with open(STATE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_state(rows):
    rows.sort(key=lambda r: r["id"])
    with open(STATE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


# ---------- captions ----------

def caption_for(vid):
    """Find '## vNNN ...' in docs/posts/*.md and return the text between 'Caption:' and 'Sources:'."""
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "posts", "*.md")), reverse=True):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        m = re.search(rf"^## {re.escape(vid)}\b.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
        if not m:
            continue
        sec = m.group(1)
        c = re.search(r"^Caption:\s*\n(.*?)(?=^Sources?:|\Z)", sec, re.M | re.S)
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


# ---------- queue ----------

def sh(*cmd, check=True):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True, capture_output=True)


def ensure_release():
    if sh("gh", "release", "view", RELEASE_TAG, check=False).returncode != 0:
        sh("gh", "release", "create", RELEASE_TAG, "--title", "Rendered Reels",
           "--notes", "MP4s published to Instagram by the Instagram workflow. Do not delete: "
                      "Instagram downloads videos from these URLs.", "--latest=false")


def cmd_queue():
    rows = load_state()
    known = {r["id"] for r in rows}
    todo = []
    for path in sorted(glob.glob(os.path.join(ROOT, "videos", "v*.py"))):
        name = os.path.splitext(os.path.basename(path))[0]
        vid = name.split("_")[0]
        if vid not in known:
            todo.append((vid, name, path))
    if not todo:
        print("Nothing new to render.")
        return 0
    ensure_release()
    failed = 0
    for vid, name, path in todo:
        try:
            r = sh(sys.executable, "render.py", os.path.relpath(path, ROOT))
            print(r.stdout.strip())
            mp4 = os.path.join(ROOT, "out", name + ".mp4")
            sh("gh", "release", "upload", RELEASE_TAG, mp4, "--clobber")
        except subprocess.CalledProcessError as e:
            print(f"!! {vid} failed: {e.stderr or e.stdout}", file=sys.stderr)
            failed += 1
            continue          # not added to state, so the next run retries it
        rows.append({"id": vid, "file": name + ".mp4", "status": "queued", "attempts": "0"})
        save_state(rows)      # save after each one so a later failure doesn't lose work
        print(f"queued {vid}")
    return 1 if failed else 0


# ---------- Instagram API ----------

def api(method, path, **params):
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"{method} {path} -> HTTP {e.code}: {body}") from None


def publish_reel(video_url, caption):
    me = api("GET", "me", fields="user_id,username")
    ig_id = me["user_id"]
    print(f"Posting as @{me.get('username')}")
    container = api("POST", f"{ig_id}/media", media_type="REELS", video_url=video_url,
                    caption=caption, share_to_feed="true")["id"]
    # Instagram downloads and processes the video; wait until it is ready (up to ~10 min).
    for _ in range(60):
        st = api("GET", container, fields="status_code,status")
        code = st.get("status_code")
        print("container status:", code)
        if code == "FINISHED":
            break
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram could not process the video: {st}")
        time.sleep(10)
    else:
        raise RuntimeError("Timed out waiting for Instagram to process the video")
    media_id = api("POST", f"{ig_id}/media_publish", creation_id=container)["id"]
    try:
        link = api("GET", media_id, fields="permalink").get("permalink", "")
    except RuntimeError:
        link = ""
    return media_id, link


def cmd_post():
    if not os.environ.get("IG_ACCESS_TOKEN"):
        print("IG_ACCESS_TOKEN is not set; add it as a repository secret.", file=sys.stderr)
        return 1
    repo = os.environ["GITHUB_REPOSITORY"]
    rows = load_state()
    for row in rows:
        if row["status"] != "queued":
            continue
        try:
            cap = caption_for(row["id"])
        except ValueError as e:
            row["status"], row["note"] = "failed", str(e)
            save_state(rows)
            print(e, file=sys.stderr)
            return 1
        if cap is None:
            print(f"{row['id']}: no caption in docs/posts yet, skipping for now")
            continue
        url = f"https://github.com/{repo}/releases/download/{RELEASE_TAG}/{row['file']}"
        print(f"Publishing {row['id']} from {url}")
        row["attempts"] = str(int(row.get("attempts") or 0) + 1)
        try:
            media_id, link = publish_reel(url, cap)
        except Exception as e:  # noqa: BLE001 - record any failure in the state file
            row["note"] = str(e)[:300].replace("\n", " ")
            if int(row["attempts"]) >= MAX_ATTEMPTS:
                row["status"] = "failed"
            save_state(rows)
            print(f"!! {row['id']}: {e}", file=sys.stderr)
            return 1
        row.update(status="posted", media_id=media_id, permalink=link, note="",
                   posted_at=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
        save_state(rows)
        print(f"Posted {row['id']}: {link or media_id}")
        return 0
    print("Queue is empty: nothing to post.")
    return 0


def cmd_status():
    for r in load_state():
        if r["status"] != "skip":
            print(f"{r['id']}  {r['status']:<7} {r.get('posted_at', '')}  {r.get('permalink') or r.get('note', '')}")
    return 0


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # captions contain emoji; Windows consoles default to cp1252
    if not argv:
        print(__doc__); return 1
    if argv[0] == "caption":
        cap = caption_for(argv[1])
        print(cap if cap is not None else f"No caption found for {argv[1]}")
        return 0 if cap else 1
    return {"queue": cmd_queue, "post": cmd_post, "status": cmd_status}[argv[0]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
