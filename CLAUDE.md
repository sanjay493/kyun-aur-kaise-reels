# Daily Reels procedure

This repo makes 2D animated educational Reels for the Instagram channel (working handle
@kyun.aur.kaise; set `HANDLE` in `engine.py` when it changes). Audience: CBSE Class 6–10
students in India, plus parents and teachers. Read `docs/playbook.md` for the full content
rules and quality checklist; the rules below are the ones that matter most.

## Each daily batch (4 videos)

1. `./setup.sh`, then read `docs/topics.csv` and the last two files in `docs/posts/`.
2. Pick 4 topics that are not in `topics.csv` (no repeats, no slight variations).
   Use 4 different series in a batch and don't open with the series that opened yesterday.
   Mix school concepts (maths, science, English, Hindi, social science) with life topics
   (teen talk, study habits, digital safety, family, money). Prefer topics with a strong
   visual and an Indian everyday example.
3. Research each one with web search; prefer NCERT, CBSE, government, university and
   established science sources. Never invent facts or numbers. Note 1–3 source links.
4. Write `videos/vNNN_slug.py` (next number after the highest in `topics.csv`), copying the
   structure of the existing scripts:
   - Narration 50–70 words total, 5–7 scenes, opens with a specific question or surprising
     statement (never "Did you know"), one central idea, ends with a memorable takeaway,
     no calls to action in the narration.
   - `say` is for the voice: spell out numbers ("one hundred eighty") and acronyms with
     dots ("O.T.P."). `show` is the subtitle text when it differs.
   - Draw only between y≈260 and y≈1200; subtitles sit at y≈1240, the character bottom-left.
   - Psychology and parenting topics: balanced, no diagnosing, no shaming.
5. `python render.py --still videos/vNNN_slug.py`, open the sheet image and fix any overlap,
   clipped text or wrong numbers. Then render. Each video must be 20–32 s. Pull 3–4 frames
   from the MP4 with ffmpeg and look at them before accepting it.
6. Append the topics to `docs/topics.csv` (status `rendered`), write
   `docs/posts/YYYY-MM-DD.md` with title, series, class, length, word count, voiceover,
   caption (adds value, doesn't repeat the voiceover; 3–5 relevant hashtags) and sources.
   Commit and push to `main`.

## Improving over time

- Sundays: read the "Reels tracker" Google Sheet in the Drive folder "kyun.aur.kaise Reels".
  Where metrics have been filled in, favour the series and hook styles with the best
  shares, saves and watch time, and note what changed in that day's post file.
- Sundays: also make one small visual improvement to `engine.py` (a transition, an
  expression for the character, a new series theme), re-render one existing video's still
  sheet to confirm nothing broke, and describe it in the commit message.
- Keep the overall look consistent: same character, voice (`hf_beta`), subtitle style.

## Sizes and limits

Voice model files live in `models/` and are not committed. Rendered MP4s go in `out/` and are
not committed either; they are delivered to the person directly.
