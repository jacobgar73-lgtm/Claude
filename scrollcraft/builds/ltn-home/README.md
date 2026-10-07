# Love Thy Neighbor home page (scroll-craft build)

A preview of the redesigned home page. The rest of the site is unchanged and is
linked from here. The brief, journey and feeling curve are in `BRIEF.md`.

## Preview

```bash
python3 -m http.server 8000      # from the repository root
# open http://localhost:8000/scrollcraft/builds/ltn-home/
```

It must be served over HTTP; opening the file directly blocks the film.

## Before launch

- **Replace the two placeholder figures** (seniors visited, volunteer hours) in
  chapter IV. They are marked with a red `TK` tag. When the real numbers are in,
  delete `data-draft` from the `<html>` tag and the tags disappear.
- **Promote it**: copy this page to the site root as `index.html`, change the
  `../../../` links to plain file names, and point the asset paths at the right
  folder.
- **Test the film on a real iPhone.** The headless checks cannot reproduce iOS
  video. If it freezes, deploy `.claude/skills/scroll-craft/references/device-diag.html`
  next to the page and send a screenshot from the phone.

## Files

- `index.html`: the page, including its own CSS and the signature hands script.
- `scrollcraft.js` / `scrollcraft.css`: the unmodified scroll-craft engine.
- `assets/`: web-optimised copies of the site's own photos, the story film
  encoded for scrubbing (MP4, with a WebM fallback for browsers without H.264),
  and the two halves of the heart-and-hands mark.
