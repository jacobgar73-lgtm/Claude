# Love Thy Neighbor: website redesign

A redesign of [ltntexas.org](https://www.ltntexas.org) as a small static site: seven pages, one stylesheet, no framework.

**Direction:** clean and minimal, led by data and by real photographs of the crews at work. Warm paper tones, one typeface (Archivo), and Love Thy Neighbor red kept for two jobs: giving, and the bar that is the point of a chart.

## Pages

| Page | What it is for |
| --- | --- |
| `index.html` | Who we are, why the work is needed (charts), where we are today (timeline), the programs, and three ways in |
| `get-help.html` | For seniors, families and referrers: the phone number, what is offered today, the referral form, Spanish help |
| `our-work.html` | The three programs, mostly in photographs and diagrams |
| `impact.html` | The data page: the need in Cameron County, what has been done, the activity log |
| `volunteer.html` | Open dates, ways to serve, what to expect, sign-up |
| `about.html` | The story, the mission, the team, partners, contact |
| `donate.html` | What a gift does, wish lists, other ways to give |

## How it is put together

```
src/pages/*.html   page bodies (edit these)
tools/build.py     wraps each body in the shared head, header and footer
styles.css         the whole design system: tokens first, then components
main.js            menu, chart animation, tooltips, form hand-off
css/<page>.css     optional small page-specific styles
assets/img/        photographs and logos
```

Build and preview:

```bash
python3 tools/build.py          # writes the pages at the repository root
python3 -m http.server 8000     # then open http://localhost:8000
```

## Sample content

The client asked for sample figures while the design is settled. Every invented number, quote or amount is wrapped in `data-placeholder`, so it can be found with one search:

```bash
grep -rn "data-placeholder" src/pages/
```

While `DRAFT = True` in `tools/build.py`, sample content gets a dotted underline and each section shows a small note. Set `DRAFT = False` once the real records are in.

The statistics about the need are real. Each was reproduced from its primary source on November 20, 2026 (U.S. Census Bureau American Community Survey 2020 to 2024, the U.S. Surgeon General's 2023 advisory, the National Academies, CDC and AARP) and carries its source link on the page.

## Before going live

- Replace every sample figure with program records, then turn draft mode off.
- Connect the two forms (referral, volunteer) to a real form service. They currently open the visitor's email app.
- Confirm captions: the clean-up photographs are captioned "Harlingen, 2026".
- Have a native speaker review the Spanish on the Get help page.
- Confirm the lines marked "to confirm" on the About page (everyone is a volunteer; help is offered regardless of faith).

## Photography

Restore, Renew & Rebuild clean-up photographs: Garcia Photography Co. Fellowship photographs: Love Thy Neighbor volunteers. The hero video from the old site is not used.
