# kyun-aur-kaise-reels

Short 2D animated educational Reels for the Instagram channel @kyun.aur.kaise, aimed at CBSE
Class 6–10 students (plus parents and teachers), built entirely in code. About 38 videos so far.
Each video: 1080×1920, 30 fps, 20–32 s, Indian-accent AI voice (Kokoro `hf_beta`), word-by-word
highlighted subtitles, a recurring student character, and a soft generated music bed.

## Quick start

```bash
./setup.sh                                   # packages + voice model (one time)
python render.py --still videos/v001_triangle_180.py   # check layout frames -> out/*_sheet.png
python render.py videos/v001_triangle_180.py           # render -> out/v001_triangle_180.mp4
python render.py --all
```

Needs Python 3.10+ and ffmpeg on PATH (on Windows: `winget install Gyan.FFmpeg`, and run
`./setup.sh` from Git Bash; the renderer uses the fonts in `fonts/`). Voice model files go in
`models/` and rendered MP4s in `out/`; neither is committed.

## How to use it

Making one video, start to finish:

1. **Set up once.** Run `./setup.sh` (installs the Python packages and downloads the voice model
   into `models/`). Make sure `ffmpeg` works in your terminal.
2. **Pick a topic.** Check `docs/topics.csv` so you don't repeat one. Prefer a topic with a strong
   visual and an Indian everyday example. Note 1–3 reliable sources (NCERT, CBSE, government,
   university); never invent facts or numbers.
3. **Write the script.** Copy a script from `videos/` to the next number, e.g.
   `videos/v039_my_topic.py`, and fill in `SERIES`, `TITLE` and `SCENES` (see
   [Script format](#script-format)). Open with a specific question or surprising statement, give
   one central idea, and end with a memorable takeaway.
4. **Check the layout.** Run `python render.py --still videos/v039_my_topic.py` and open
   `out/v039_my_topic_sheet.png`. Fix any overlap, clipped text or wrong numbers, then repeat.
5. **Render.** Run `python render.py videos/v039_my_topic.py`. The video must come out between
   20 and 32 seconds. Pull a few frames with ffmpeg and look at them before accepting it. Confirm
   the maths on screen is correct and nothing important sits below y≈1600, where Instagram's
   caption covers the video.
6. **Log it.** Add a row to `docs/topics.csv` (status `rendered`) and add a `## v039 Title`
   section to `docs/posts/YYYY-MM-DD.md` with the series, class, length, word count, voiceover,
   a caption and the sources. The caption should add something new, not repeat the voiceover,
   and carry 3–5 relevant hashtags.
7. **Get the caption.** Run `python publish/captions.py`. It writes
   `out/v039_my_topic_caption.txt` next to the MP4. The caption is exactly the text between
   `Caption:` and `Sources:` under the `## v039 Title` heading, and must stay under 2,200
   characters and 30 hashtags.
8. **Post.** The account is a personal one, so the Instagram API can't post to it. Upload
   `out/v039_my_topic.mp4` by hand and paste in the caption file.
9. **Commit.** Commit the script, `topics.csv` and the post file, then push to `main`.

Useful commands:

| Command | What it does |
|---|---|
| `python render.py --still <script>` | Layout sheet only, quick to check |
| `python render.py <script>` | Render one video to `out/` |
| `python render.py --all` | Render every video in `videos/` |
| `python publish/captions.py` | Caption files for every rendered MP4 |
| `python publish/captions.py v038` | Print one caption |

## Script format

Each scene is `dict(say=..., show=..., draw=fn)`: `say` is what the voice reads (spell out
numbers and acronyms, e.g. "one hundred eighty", "O.T.P."), `show` is the subtitle text if it
differs, and `draw(layer, d, t, T, theme)` paints the stage between y≈260 and y≈1200 for time `t`
of a scene lasting `T` seconds. Subtitles sit at y≈1240 and the character at the bottom left.
Use 5–7 scenes and 50–70 words of narration in total, with no calls to action.

Series themes (set `SERIES`): `maths`, `science`, `safe`, `teen`, `study`, `english`, `money`,
`family`. Add more in `engine.THEMES`. The channel handle shown on screen is `HANDLE` in
`engine.py`.

## Layout

| Path | What it is |
|---|---|
| `render.py` | Command-line entry point: renders scripts or `--still` layout sheets into `out/` |
| `engine.py` | Renderer: themes, character, subtitles, voice, music, scene encoding |
| `setup.sh`, `requirements.txt` | One-time install of packages and the voice model |
| `videos/vNNN_*.py` | One file per video: `SERIES`, `TITLE`, `SCENES` (spoken line + draw function) |
| `docs/playbook.md` | Content playbook and master prompt |
| `docs/topics.csv` | Every topic made so far, so new videos never repeat one |
| `docs/posts/` | Caption, hashtags and sources for each batch (`YYYY-MM-DD.md`) |
| `publish/captions.py` | Writes `out/vNNN_*_caption.txt` next to each MP4 for copy-paste |
| `fonts/` | Fonts used by the renderer |

## Daily batches

`CLAUDE.md` has the full daily procedure: four new topics from four different series, researched
with sources, scripted, checked with `--still`, rendered, logged in `docs/topics.csv` and
`docs/posts/`, then committed to `main`. On Sundays it also reviews the "Reels tracker" sheet
(shares, saves and watch time per series and hook style) and adds one small visual improvement
to `engine.py`. See `docs/playbook.md` for the content rules and quality checklist.
