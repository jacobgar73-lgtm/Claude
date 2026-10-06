# Love Thy Neighbor: website redesign

A redesign of [ltntexas.org](https://www.ltntexas.org), built as a static site using the photos, video, logo and copy from the current site.

**Design direction:** Ease Health's structure (split tinted hero panels, a serif headline voice, soft tinted cards, one deep action color), adapted with LTN's heart-red branding and made softer and more inviting: larger rounded corners, a rounded serif (Fraunces "soft"), a friendly sans (Figtree), a warm cream background and gentle shadows.

## Pages
| File | Page |
| --- | --- |
| `index.html` | Home: video hero, partners, programs, volunteering, photo mosaic, referral and donate calls to action |
| `about.html` | Mission, values, team |
| `programs.html` | Restore, Renew & Rebuild; Hearts & Hands Fellowship; Adopt-A-Neighbor |
| `get-involved.html` | Volunteer sign-up and leadership roles |
| `partners.html` | Community partners and sponsors |
| `donate.html` | Amazon wish lists by program |
| `refer.html` | Refer a neighbor form |

## Preview locally
```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Design tokens (`assets/css/styles.css`)
| Token | Value | Use |
| --- | --- | --- |
| `--canvas` | `#fbf5ef` | Page background |
| `--blush` / `--sand` / `--peach` | `#f8ded7` / `#f5e8d6` / `#fde6d2` | Tinted panels |
| `--ink` | `#3b1416` | Headings, footer |
| `--brand` | `#c82828` | LTN logo red (accents) |
| `--brand-deep` | `#8e1d22` | Buttons and main actions |

## Before going live
- **Forms** (volunteer sign-up, referral) currently open the visitor's email app with the answers filled in, addressed to Info@LtnTexas.org. Connect them to a real form service (Formspree, Jotform, Microsoft Forms, or Wix forms) so submissions don't depend on the visitor having an email app.
- **Events page**: left out because the current one is a maintenance page. Add it back once there are events to list.
- **Impact numbers** (homes restored, seniors visited) would strengthen the home page. Add them only once you have real figures.
