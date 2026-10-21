# PrizeBond Check · প্রাইজবন্ড চেক

Free checker for Bangladesh 100 Taka prize bonds. Visitors paste, upload (Excel/CSV) or
photograph their bonds and check them against the last 8 Bangladesh Bank draws.
Everything runs in the visitor's browser; no server, no data leaves their device.

## How it's put together

| Path | What it is |
|---|---|
| `draws.json` | Winning numbers for each draw (the only file that changes after a draw) |
| `template.html` | Page design, text (English + Bangla) and all the checker logic |
| `build.py` | Turns the two files above into the website in `site/` |
| `vendor/` | Third-party libraries: SheetJS (Excel), tesseract.js (camera scan) |
| `site/` | The finished website. **Cloudflare publishes this folder.** Don't edit by hand. |

## Hosting

Cloudflare Pages, connected to this repository:
build command **none**, build output directory **`site`**. Every push to `main` goes live.

## After a new draw

1. Add the draw to `draws.json` (all 46 numbers, verified in at least two sources).
   Keep only the last 8 draws: delete the oldest when adding a new one.
2. In `template.html`, set `NEXT_DRAW` to the following draw (number and date).
3. Run `python3 build.py` (needs Python 3 and Pillow: `pip install pillow`).
4. Commit and push, including `site/`.

A scheduled task does these steps automatically after each draw and only publishes when
every number matches across sources.

## Settings

In `build.py`, set `SITE_URL` to the live address (e.g. `https://example.com`) to switch on
canonical links and `sitemap.xml`.
