# Love Thy Neighbor website

The site for Love Thy Neighbor Inc., Harlingen, Texas, built to the LTN Website Brief (November 24, 2026).

It has one job: inform visitors, collect referrals for seniors, and turn visitors into volunteers.

## Pages

| Page | File | Main action |
| --- | --- | --- |
| Home | `index.html` | Refer a Neighbor, Volunteer |
| Programs | `programs.html` | Volunteer |
| Get Involved | `get-involved.html` | Sign up on POINT |
| Refer a Neighbor | `refer.html` | Submit the form |
| Give | `give.html` | Give or contact us |
| About | `about.html` | Contact us |

Spanish versions of Home, Refer a Neighbor and Get Involved are in `es/`. The language switch is in the footer.

## Change a number, an event or the phone number

Everything that changes often is in one file: `content/site.json`.

- The four numbers on Home (`stats`) and their date (`stats_as_of`)
- Seniors served and the goal (`seniors_served`, `seniors_goal`)
- Upcoming events (`events`). Past dates drop off by themselves at the next build.
- Phone, email, address, Instagram, POINT link
- The seasonal banner on Home (`campaign`). Set `enabled` to `false` when the campaign ends.

Then rebuild:

```bash
python3 tools/build.py
```

```bash
python3 -m http.server 8000
```

Open http://localhost:8000 to preview.

## How it is put together

```
content/site.json     numbers, events, contact details, links
src/pages/*.html      English page bodies (edit these, not the files at the root)
src/pages/es/*.html   Spanish page bodies
tools/build.py        adds the shared head, header and footer, fills in site.json
styles.css            the whole look: colors and type first, then components
main.js               menu, counting numbers, before/after slider, giving picker, form
assets/img/           photographs and the logo
```

The logo (`assets/img/ltn-logo.png`) is the supplied artwork, unchanged. It was only trimmed and given a transparent background.

## Sample content

Anything invented is wrapped in `data-placeholder` and shows a dotted underline while `"draft": true` in `content/site.json`. Find every one with:

```bash
grep -rn "data-placeholder" src/pages/
```

Set `"draft": false` only when that search comes back empty.

The four POINT numbers (438+ hours, 20 events, 31 volunteers, $15,370 in volunteer time) are real, as of mid-November 2026.

## Before launch

1. **Referral form.** Set `form_endpoint` in `content/site.json` to a form service. Until then the form opens the visitor's email app, which is not good enough for launch.
2. **Giving.** Set `give_url` once the board chooses a giving tool. Until then the Give button starts an email.
3. **Events.** The list is typed by hand in `site.json`. Replace it with the POINT embed on Get Involved if POINT provides one.
4. **Open decisions from the brief.** Mission statement, phone number, Instagram handle, public address, seniors served so far.
5. **Photos.** A matched before and after pair, a GoodWorks Market photo, and signed releases for any photo that shows a senior. No senior appears on the site today.
6. **Partners.** Names are shown as text. Add logos only with written permission.
7. **Spanish.** Have a native speaker from the Valley read the three Spanish pages.
8. **Visit tracking.** Set `analytics_domain` to turn on Plausible, or add the tracker of your choice in `tools/build.py`.
9. **Facebook link.** `facebook_url` is a placeholder.

## Photography

Restore Day photographs: Garcia Photography Co. Other photographs: Love Thy Neighbor volunteers. No stock images.
