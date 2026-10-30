# kyun-aur-kaise-reels

Short 2D animated educational Reels / YouTube Shorts for CBSE Class 6–10 students, built in code.
Each video: 1080×1920, 30 fps, 20–30 s, Indian-accent AI voice (Kokoro `hf_beta`), word-by-word
highlighted subtitles, a recurring student character, and a soft generated music bed.

## Quick start

```bash
./setup.sh                                   # packages + voice model (one time)
python render.py --still videos/v001_triangle_180.py   # check layout frames -> out/*_sheet.png
python render.py videos/v001_triangle_180.py           # render -> out/v001_triangle_180.mp4
python render.py --all
```

Needs Python 3.10+ and ffmpeg.

## Layout

| Path | What it is |
|---|---|
| `engine.py` | Renderer: themes, character, subtitles, voice, music, scene encoding |
| `videos/vNNN_*.py` | One file per video: `SERIES`, `TITLE`, `SCENES` (spoken line + draw function) |
| `docs/playbook.md` | Content playbook and master prompt |
| `docs/topics.csv` | Every topic made so far, so new videos never repeat one |
| `docs/posts/` | Caption, hashtags and sources for each batch |

## Writing a new video

Copy an existing script in `videos/`. Each scene is
`dict(say=..., show=..., draw=fn)`: `say` is what the voice reads (spell out numbers and
acronyms, e.g. "one hundred eighty", "O.T.P."), `show` is the subtitle text if it differs,
and `draw(layer, d, t, T, theme)` paints the stage between y≈260 and y≈1200 for time `t`
of a scene lasting `T` seconds. Keep narration 50–70 words.

Series themes (set `SERIES`): `maths`, `science`, `safe`, `teen`. Add more in `engine.THEMES`.

## Checks before posting

Run `--still`, look at the sheet, render, then confirm: facts checked with sources, on-screen
maths correct, nothing important hidden behind Instagram's bottom caption area (below y≈1600).
