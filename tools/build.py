#!/usr/bin/env python3
"""Build the site: wrap each page body in src/pages/ with the shared head, header and footer.

Usage: python3 tools/build.py            (writes every page at the repository root)
       python3 tools/build.py impact     (builds one page)
A page may have its own small stylesheet at css/<page>.css; it is linked automatically.
Each file in src/pages/ starts with one comment line:
    <!-- title: Page title | description: One sentence for search results | nav: get-help -->
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "src" / "pages"

# Remove the data-draft attribute here once every sample figure has been replaced with a real one.
DRAFT = True

NAV = [
    ("get-help", "Get help"),
    ("our-work", "Our work"),
    ("impact", "Impact"),
    ("volunteer", "Volunteer"),
    ("about", "About"),
]

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="icon-person" viewBox="0 0 20 26"><circle cx="10" cy="5" r="4.4"/><path d="M1.5 26v-7.2C1.5 14.5 5.3 11 10 11s8.5 3.5 8.5 7.8V26z"/></symbol>
  <symbol id="icon-house" viewBox="0 0 24 24"><path d="M12 2.2 1.2 11.6h3.1V21.8h6v-6.4h3.4v6.4h6V11.6h3.1z"/></symbol>
</svg>"""


def header(current):
    links = "\n".join(
        '          <li><a class="site-nav__link" href="{0}.html"{2}>{1}</a></li>'.format(
            slug, label, ' aria-current="page"' if slug == current else "")
        for slug, label in NAV)
    return """  <a class="skip-link" href="#main">Skip to main content</a>
  <p class="draft-bar">Design preview. Numbers with a dotted underline are samples, to be replaced with program records.</p>

  <header class="site-header">
    <div class="container site-header__bar">
      <a class="brand" href="index.html" aria-label="Love Thy Neighbor, home">
        <img class="brand__mark" src="assets/img/heart.png" width="600" height="569" alt="">
        <span class="brand__text">
          <span class="brand__name">Love Thy Neighbor</span>
          <span class="brand__tagline">Neighbors Helping Neighbors</span>
        </span>
      </a>

      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>

      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul class="site-nav__list" role="list">
{links}
        </ul>
      </nav>

      <div class="site-header__actions">
        <a class="phone-link" href="tel:+19563203378"><span class="phone-link__label">Call</span> (956) 320-3378</a>
        <a class="button button--outline button--small site-header__help" href="get-help.html">Get help</a>
        <a class="button button--give button--small" href="donate.html">Donate</a>
      </div>
    </div>
  </header>
""".format(links=links)


FOOTER = """  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__grid">
        <div class="site-footer__brand">
          <img class="site-footer__logo" src="assets/img/logo.png" width="519" height="600" alt="Love Thy Neighbor">
          <p class="site-footer__tagline">One neighbor, one heart, one home at a time.</p>
        </div>
        <div>
          <h2 class="site-footer__heading">Contact</h2>
          <ul class="site-footer__list" role="list">
            <li><a href="tel:+19563203378">(956) 320-3378</a></li>
            <li><a href="mailto:Info@LtnTexas.org">Info@LtnTexas.org</a></li>
            <li><a href="https://www.facebook.com/lovethyneighbor">Facebook</a></li>
            <li><a href="https://www.instagram.com/lovethyneighbortx">Instagram</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">Take part</h2>
          <ul class="site-footer__list" role="list">
            <li><a href="get-help.html">Get help</a></li>
            <li><a href="volunteer.html">Volunteer</a></li>
            <li><a href="donate.html">Donate</a></li>
          </ul>
        </div>
        <div>
          <h2 class="site-footer__heading">Learn more</h2>
          <ul class="site-footer__list" role="list">
            <li><a href="our-work.html">Our work</a></li>
            <li><a href="impact.html">Impact</a></li>
            <li><a href="about.html">About</a></li>
          </ul>
        </div>
      </div>
      <div class="site-footer__legal">
        <p>&copy; <span id="year">2026</span> Love Thy Neighbor Inc., Harlingen, Texas. A 501(c)(3) nonprofit, EIN 36-5150765.</p>
        <p>Photographs by Garcia Photography Co. and Love Thy Neighbor volunteers.</p>
      </div>
    </div>
  </footer>
"""

TEMPLATE = """<!doctype html>
<html lang="en"{draft}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#FFFCF8">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="assets/img/r3-crew.jpg">
  <link rel="icon" href="assets/img/heart.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">{page_css}
  <script>document.documentElement.classList.add('js');</script>
</head>
<body>
{sprite}
{header}
  <main id="main">
{body}
  </main>

{footer}
  <script src="main.js"></script>
</body>
</html>
"""


def build(only=None):
    for path in sorted(PAGES.glob("*.html")):
        if only and path.stem not in only:
            continue
        source = path.read_text(encoding="utf-8")
        match = re.match(r"\s*<!--(.*?)-->\s*\n", source, re.S)
        if not match:
            raise SystemExit("{}: missing the first-line comment with title and description".format(path.name))
        meta = dict((k.strip(), v.strip()) for k, v in
                    (part.split(":", 1) for part in match.group(1).split("|") if ":" in part))
        body = source[match.end():].rstrip()
        html = TEMPLATE.format(
            draft=" data-draft" if DRAFT else "",
            title=meta["title"],
            description=meta["description"],
            sprite=SPRITE,
            header=header(meta.get("nav", "")),
            body=body,
            footer=FOOTER,
            page_css=('\n  <link rel="stylesheet" href="css/{}.css">'.format(path.stem)
                      if (ROOT / "css" / (path.stem + ".css")).exists() else ""),
        )
        (ROOT / path.name).write_text(html, encoding="utf-8")
        print("built", path.name)


if __name__ == "__main__":
    import sys
    build(set(sys.argv[1:]) or None)
