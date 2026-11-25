#!/usr/bin/env python3
"""Build the Love Thy Neighbor site.

    python3 tools/build.py

Reads page bodies from src/pages/ (English) and src/pages/es/ (Spanish), fills in the
values from content/site.json, wraps each one in the shared head, header and footer,
and writes the finished pages at the repository root and in es/.

Each page body starts with one comment line:
    <!-- title: Page title | description: One sentence for search results | nav: programs -->

Tokens a page body can use:
    {{phone}} {{phone_tel}} {{email}} {{address}} {{ein}} {{point_url}} {{give_href}}
    {{root}}                 path back to the site root ("" or "../")
    {{stats}}                the four number blocks
    {{events 3}} {{events all}}   upcoming events, soonest first
    {{seniors}}              the seniors-served progress bar
    {{credit}}               the City of Harlingen credit line, word for word
    {{giving_legal}}         the 501(c)(3) giving sentence, word for word
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "pages"
SITE = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))

CREDIT = ("Funded in part by the City of Harlingen through the "
          "Community Development Block Grant program.")
GIVING_LEGAL = ("Love Thy Neighbor Inc. is a 501(c)(3) nonprofit. Your gift is tax-deductible "
                "to the extent allowed by law. EIN %s." % SITE["ein"])

# slug, English label, Spanish label. Five links, no dropdowns.
NAV = [
    ("programs", "Programs", "Programas"),
    ("get-involved", "Get Involved", "Participa"),
    ("refer", "Refer a Neighbor", "Referir a un vecino"),
    ("give", "Give", "Donar"),
    ("about", "About", "Nosotros"),
]
SPANISH_PAGES = {"index", "refer", "get-involved"}

T = {
    "en": {
        "skip": "Skip to main content",
        "draft": "Design preview. Anything with a dotted underline is sample content, to be replaced before launch.",
        "menu": "Menu", "call": "Call", "volunteer": "Volunteer", "refer": "Refer a Neighbor",
        "home": "Love Thy Neighbor, home", "main_nav": "Main",
        "tagline": "Neighbors helping neighbors in Harlingen, Texas.",
        "contact": "Contact", "explore": "Explore", "follow": "Follow", "language": "Language",
        "spots": "spots open", "signup": "Sign up", "checked": "From our POINT page, checked",
        "as_of": "From POINT, as of", "served": "seniors served toward our goal of",
        "this_year": "this year", "sample": "Sample count",
        "months": ["January", "February", "March", "April", "May", "June", "July", "August",
                   "September", "October", "November", "December"],
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    },
    "es": {
        "skip": "Ir al contenido principal",
        "draft": "Vista previa. Lo que tiene subrayado punteado es contenido de muestra y se reemplazará antes del lanzamiento.",
        "menu": "Menú", "call": "Llame al", "volunteer": "Voluntariado", "refer": "Referir a un vecino",
        "home": "Love Thy Neighbor, inicio", "main_nav": "Principal",
        "tagline": "Vecinos ayudando a vecinos en Harlingen, Texas.",
        "contact": "Contacto", "explore": "Explorar", "follow": "Síguenos", "language": "Idioma",
        "spots": "lugares disponibles", "signup": "Apúntate", "checked": "De nuestra página de POINT, revisada el",
        "as_of": "De POINT, a", "served": "personas mayores atendidas de nuestra meta de",
        "this_year": "este año", "sample": "Cifra de muestra",
        "months": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                   "septiembre", "octubre", "noviembre", "diciembre"],
        "days": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
    },
}

ES_DATES = {"mid-November 2026": "mediados de noviembre de 2026",
            "November 20, 2026": "20 de noviembre de 2026"}


def e(text):
    return html.escape(str(text), quote=True)


def phone_tel():
    return "+1" + re.sub(r"\D", "", SITE["phone"])


def give_href(root):
    return SITE["give_url"] or (root + "give.html#give-online")


def page_href(slug, lang, root):
    """Link to a page, preferring the visitor's language when that page exists in it."""
    if lang == "es" and slug in SPANISH_PAGES:
        return "%s.html" % slug
    return "%s%s.html" % (root, slug)


def fmt_date(iso, lang):
    d = datetime.date.fromisoformat(iso)
    t = T[lang]
    if lang == "es":
        return "%s %d de %s" % (t["days"][d.weekday()].capitalize(), d.day, t["months"][d.month - 1])
    return "%s, %s %d" % (t["days"][d.weekday()], t["months"][d.month - 1], d.day)


def stats_html(lang):
    t = T[lang]
    as_of = SITE["stats_as_of"]
    if lang == "es":
        as_of = ES_DATES.get(as_of, as_of)
    blocks = []
    for s in SITE["stats"]:
        label = s["label_es"] if lang == "es" else s["label"]
        shown = "%s%s%s" % (s["prefix"], format(s["value"], ","), s["suffix"])
        blocks.append(
            '        <li class="stat"><span class="stat__num" data-count="%d" data-prefix="%s" '
            'data-suffix="%s">%s</span><span class="stat__label">%s</span></li>'
            % (s["value"], e(s["prefix"]), e(s["suffix"]), e(shown), e(label)))
    return ('<ul class="stats" role="list">\n%s\n      </ul>\n'
            '      <p class="fineprint">%s %s.</p>' % ("\n".join(blocks), t["as_of"], e(as_of)))


def seniors_html(lang):
    t = T[lang]
    served, goal = SITE["seniors_served"], SITE["seniors_goal"]
    pct = round(100 * served / goal)
    sample = SITE.get("seniors_served_is_sample")
    num = ('<span data-placeholder title="%s">%d</span>' % (t["sample"], served)) if sample else str(served)
    return ('<div class="progress">\n'
            '        <p class="progress__text"><strong>%s</strong> %s %d %s.</p>\n'
            '        <div class="progress__track" role="img" aria-label="%d / %d"><span style="width:%d%%"></span></div>\n'
            '      </div>' % (num, t["served"], goal, t["this_year"], served, goal, pct))


def events_html(lang, limit):
    t = T[lang]
    today = datetime.date.today().isoformat()
    upcoming = sorted((ev for ev in SITE["events"] if ev["date"] >= today), key=lambda ev: ev["date"])
    if limit:
        upcoming = upcoming[:limit]
    rows = []
    for ev in upcoming:
        d = datetime.date.fromisoformat(ev["date"])
        title = ev["title_es"] if lang == "es" else ev["title"]
        rows.append(
            '        <li class="event">\n'
            '          <p class="event__date"><span class="event__day">%d</span><span class="event__month">%s</span></p>\n'
            '          <div class="event__body">\n'
            '            <h3 class="event__title">%s</h3>\n'
            '            <p class="event__meta">%s, %s · %s</p>\n'
            '            <p class="event__spots">%d %s</p>\n'
            '          </div>\n'
            '          <a class="button button--outline" href="%s" rel="noopener">%s<span class="visually-hidden">: %s, %s</span></a>\n'
            '        </li>'
            % (d.day, e(t["months"][d.month - 1][:3]), e(title), e(fmt_date(ev["date"], lang)),
               e(ev["time"]), e(ev["place"]), ev["open"], t["spots"], e(SITE["point_url"]),
               t["signup"], e(title), e(fmt_date(ev["date"], lang))))
    checked = SITE["events_checked"]
    if lang == "es":
        checked = ES_DATES.get(checked, checked)
    return ('<ul class="events" role="list">\n%s\n      </ul>\n'
            '      <p class="fineprint">%s %s.</p>' % ("\n".join(rows), t["checked"], e(checked)))


def fill(body, lang, root):
    simple = {
        "phone": e(SITE["phone"]), "phone_tel": phone_tel(), "email": e(SITE["email"]),
        "address": e(SITE["address"]), "ein": e(SITE["ein"]), "point_url": e(SITE["point_url"]),
        "give_href": e(give_href(root)), "root": root, "credit": CREDIT,
        "giving_legal": GIVING_LEGAL, "instagram_handle": e(SITE["instagram_handle"]),
        "instagram_url": e(SITE["instagram_url"]), "facebook_url": e(SITE["facebook_url"]),
        "form_endpoint": e(SITE["form_endpoint"]),
        "stats": stats_html(lang), "seniors": seniors_html(lang),
        "seniors_goal": str(SITE["seniors_goal"]),
    }

    def sub(match):
        key = match.group(1).strip()
        if key.startswith("events"):
            arg = key.split()[1] if " " in key else "all"
            return events_html(lang, None if arg == "all" else int(arg))
        if key not in simple:
            raise SystemExit("Unknown token {{%s}}" % key)
        return simple[key]

    return re.sub(r"\{\{([^}]+)\}\}", sub, body)


def header(current, lang, root):
    t = T[lang]
    home = "index.html" if lang == "es" else root + "index.html"
    links = "\n".join(
        '          <li><a class="site-nav__link" href="%s"%s>%s</a></li>'
        % (page_href(slug, lang, root), ' aria-current="page"' if slug == current else "",
           es if lang == "es" else en)
        for slug, en, es in NAV)
    campaign = ""
    c = SITE.get("campaign", {})
    if c.get("enabled") and current == "index":
        campaign = ('  <p class="campaign-bar">%s <a href="%s" rel="noopener">%s</a></p>\n'
                    % (e(c["text_es" if lang == "es" else "text"]), e(c["url"]),
                       e(c["link_text_es" if lang == "es" else "link_text"])))
    draft = '  <p class="draft-bar">%s</p>\n' % t["draft"] if SITE.get("draft") else ""
    return """  <a class="skip-link" href="#main">{skip}</a>
{draft}  <header class="site-header">
    <div class="container site-header__bar">
      <a class="brand" href="{home}" aria-label="{home_label}">
        <img class="brand__logo" src="{root}assets/img/ltn-logo.png" width="640" height="640" alt="Love Thy Neighbor">
      </a>
      <nav class="site-nav" id="site-nav" aria-label="{main_nav}">
        <ul class="site-nav__list" role="list">
{links}
        </ul>
      </nav>
      <div class="site-header__actions">
        <a class="phone-link" href="tel:{tel}"><span class="phone-link__label">{call}</span> {phone}</a>
        <a class="button button--primary button--small site-header__cta" href="{point}" rel="noopener">{volunteer}</a>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">{menu}</button>
      </div>
    </div>
  </header>
{campaign}""".format(skip=t["skip"], draft=draft, home=home, home_label=t["home"], root=root,
                    main_nav=t["main_nav"], links=links, tel=phone_tel(), call=t["call"],
                    phone=e(SITE["phone"]), point=e(SITE["point_url"]), volunteer=t["volunteer"],
                    menu=t["menu"], campaign=campaign)


def footer(current, lang, root):
    t = T[lang]
    links = "\n".join(
        '          <li><a href="%s">%s</a></li>' % (page_href(slug, lang, root), es if lang == "es" else en)
        for slug, en, es in NAV)
    # Language switch: point at the same page in the other language when it exists.
    if lang == "es":
        switch = '<a href="../%s.html" lang="en" hreflang="en">English</a> · <span aria-current="true">Español</span>' % current
    elif current in SPANISH_PAGES:
        switch = '<span aria-current="true">English</span> · <a href="es/%s.html" lang="es" hreflang="es">Español</a>' % current
    else:
        switch = '<span aria-current="true">English</span> · <a href="es/index.html" lang="es" hreflang="es">Español</a>'
    return """  <footer class="site-footer">
    <div class="container site-footer__grid">
      <div class="site-footer__brand">
        <img src="{root}assets/img/ltn-logo.png" width="640" height="640" alt="Love Thy Neighbor" loading="lazy">
        <p>{tagline}</p>
      </div>
      <div>
        <h2 class="site-footer__title">{contact}</h2>
        <ul role="list">
          <li><a href="tel:{tel}">{phone}</a></li>
          <li><a href="mailto:{email}">{email}</a></li>
          <li>{address}</li>
        </ul>
      </div>
      <div>
        <h2 class="site-footer__title">{explore}</h2>
        <ul role="list">
{links}
        </ul>
      </div>
      <div>
        <h2 class="site-footer__title">{follow}</h2>
        <ul role="list">
          <li><a href="{ig}" rel="noopener">Instagram @{handle}</a></li>
          <li><a href="{fb}" rel="noopener">Facebook</a></li>
        </ul>
        <h2 class="site-footer__title site-footer__title--gap">{language}</h2>
        <p class="lang-switch">{switch}</p>
      </div>
    </div>
    <div class="container site-footer__legal">
      <p>{legal}</p>
    </div>
  </footer>

  <nav class="action-bar" aria-label="{refer} / {volunteer}">
    <a class="button button--primary" href="{refer_href}">{refer}</a>
    <a class="button button--dark" href="{point}" rel="noopener">{volunteer}</a>
  </nav>
""".format(root=root, tagline=t["tagline"], contact=t["contact"], tel=phone_tel(),
           phone=e(SITE["phone"]), email=e(SITE["email"]), address=e(SITE["address"]),
           explore=t["explore"], links=links, follow=t["follow"], ig=e(SITE["instagram_url"]),
           handle=e(SITE["instagram_handle"]), fb=e(SITE["facebook_url"]), language=t["language"],
           switch=switch, legal=GIVING_LEGAL, refer=t["refer"], volunteer=t["volunteer"],
           refer_href=page_href("refer", lang, root), point=e(SITE["point_url"]))


def build(path, lang):
    slug = path.stem
    root = "../" if lang == "es" else ""
    raw = path.read_text(encoding="utf-8")
    meta = re.match(r"<!--(.*?)-->\s*", raw, re.S)
    if not meta:
        raise SystemExit("%s needs a first-line comment with title and description" % path)
    # Titles may contain "|", so split only where a known field name starts.
    parts = re.split(r"\s*\|?\s*\b(title|description|nav):", meta.group(1))[1:]
    fields = {k: v.strip() for k, v in zip(parts[0::2], parts[1::2])}
    body = fill(raw[meta.end():], lang, root)
    title, desc = e(fields["title"]), e(fields["description"])

    alternate = ""
    if slug in SPANISH_PAGES:
        other = ("../%s.html" % slug, "en") if lang == "es" else ("es/%s.html" % slug, "es")
        alternate = '  <link rel="alternate" hreflang="%s" href="%s">\n' % (other[1], other[0])
    analytics = ""
    if SITE.get("analytics_domain"):
        analytics = ('  <script defer data-domain="%s" src="https://plausible.io/js/script.js"></script>\n'
                     % e(SITE["analytics_domain"]))

    page = """<!doctype html>
<html lang="{lang}"{draft}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#F6F0E4">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{root}assets/img/r3-clearing-brush.jpg">
{alternate}  <link rel="icon" href="{root}assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}styles.css">
{analytics}</head>
<body>
{header}
  <main id="main">
{body}
  </main>

{footer}
  <script src="{root}main.js" defer></script>
</body>
</html>
""".format(lang=lang, draft=" data-draft" if SITE.get("draft") else "", title=title, desc=desc,
           root=root, alternate=alternate, analytics=analytics,
           header=header(fields.get("nav", slug), lang, root), body=body.rstrip(),
           footer=footer(slug, lang, root))

    out = (ROOT / "es" / path.name) if lang == "es" else (ROOT / path.name)
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out.relative_to(ROOT)


if __name__ == "__main__":
    for p in sorted(SRC.glob("*.html")):
        print("built", build(p, "en"))
    for p in sorted((SRC / "es").glob("*.html")):
        print("built", build(p, "es"))
