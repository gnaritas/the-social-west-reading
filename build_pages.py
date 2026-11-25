#!/usr/bin/env python3
"""The Social (West Reading PA) — 9-page pre-opening bar site generator (template v2).
Single source for all pages; pins the -demo Railway host (canonical/OG/sitemap).

Facts ONLY from card t_1358a4a4 sources (re-verified 2026-11-25 dispatch):
- berkscountyeats.com/news/coming-soon/ (Updated 2026-11-21): 'The Social, from the
  team behind Oakbrook Brewing and Taqueria Comalli, will take over the former
  Willow Creek Brewing at 643 Penn Street. According to the health inspection
  report, The Social will only serve drinks with no food service.' Projected
  Opening: December-January. 'No additional information ... is available at this time.'
- Owner tie: thebrewedatpodcast ep.49 'Erik Arizmendi — Owner of Oakbrook Brewing &
  Taqueria Comalli'; palomagazine.com 2025-06-30 profile (acquired Oakbrook).
- Sibling sites live (curl 200 2026-11-25): oakbrookbrewing.com, comallitacos.com.
- Address form: press says '643 Penn Street'; the venue's real street form (predecessor
  listings Yelp/BeerAdvocate/MapQuest + US Census geocoder) is '643 Penn Ave, West
  Reading, PA 19611'. Site NAP uses the verified Penn Ave / 19611 form.
- US Census geocoder: 643 Penn Ave, West Reading PA 19611 -> 40.3358902, -75.9505237.
- Willow Creek Brewing predecessor: '643 Penn Ave, West Reading, PA 19611', closed
  (Yelp 2026).
- Contact: TaqueriaComalli@gmail.com self-published on group FB Page intro
  (facebook.com/TaqueriaComalli, browser 2026-11-25).
No phone published -> none on site. No hours, menu, drinks program, or opening-night
plans announced -> stated as TBD, never invented. Press names carried in the
'sources' box as citations only.
"""
import json, os, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "public")
ORIGIN = "https://the-social-west-reading-demo.up.railway.app"
NAME = "The Social"
CITY = "West Reading"
STATE = "PA"
ZIP = "19611"
ADDR1 = "643 Penn Ave"
NAP = ADDR1 + ", " + CITY + ", " + STATE + " " + ZIP
LAT, LON = 40.3358902, -75.9505237
EMAIL = "TaqueriaComalli@gmail.com"
OAK = "https://oakbrookbrewing.com"
COM = "https://comallitacos.com"
MAPQ = "643+Penn+Ave,+West+Reading,+PA+19611"
MAPSRC = "https://www.google.com/maps?q=" + MAPQ + "&amp;output=embed"
BUILT = "<!-- BUILT-2026-11-25 -->"

def esc(s):
    return H.escape(s, quote=True)

# ------------------------------------------------------------------- JSON-LD
BAR = {
    "@type": "Bar",
    "@id": ORIGIN + "/#bar",
    "name": NAME,
    "image": ORIGIN + "/og.png",
    "url": ORIGIN + "/",
    "description": ("A new drinks-only bar from the owners of Oakbrook Brewing and "
                    "Taqueria Comalli, taking over the old Willow Creek Brewing house "
                    "at 643 Penn Ave, West Reading, PA 19611 — opening December 2026 "
                    "to January 2027. Bar service only, no food service."),
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDR1,
        "addressLocality": CITY,
        "addressRegion": STATE,
        "postalCode": ZIP,
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
}

def graph(nodes):
    return json.dumps({"@context": "https://schema.org", "@graph": nodes},
                      ensure_ascii=True, separators=(",", ":"))

def crumbs(label, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": NAME, "item": ORIGIN + "/"},
        {"@type": "ListItem", "position": 2, "name": label, "item": ORIGIN + path},
    ]}

def faq(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer":
            {"@type": "Answer", "text": a}} for q, a in items]}

def service(name, desc, path):
    return {"@type": "Service", "@id": ORIGIN + path + "#service",
            "name": name, "description": desc,
            "provider": {"@id": ORIGIN + "/#bar"},
            "areaServed": {"@type": "Place", "name": CITY + ", " + STATE}}

WEBSITE = {"@type": "WebSite", "@id": ORIGIN + "/#website", "name": NAME,
           "url": ORIGIN + "/", "inLanguage": "en"}

# ------------------------------------------------------------------------ FAQ
FAQ_MAIN = [
    ("When does The Social open?",
     "December 2026 to January 2027, as projected. An opening night hasn't been "
     "announced — when the team sets one, this page carries it."),
    ("Where is it?",
     "643 Penn Ave, West Reading, PA 19611 — the old Willow Creek Brewing house. "
     "The map is right below this list."),
    ("Will The Social serve food?",
     "No. The health inspection filing for 643 Penn Ave lists bar service only — "
     "no food service. There's no kitchen, so plan dinner around it; the neighborhood "
     "has plenty."),
    ("Who runs it?",
     "Erik Arizmendi — owner of Oakbrook Brewing and Taqueria Comalli, both in West "
     "Reading. The Social is the same team's first bar of its own."),
    ("What will they pour?",
     "Not announced yet. A bar from a brewing family — the specifics of the drinks "
     "list are still being settled, and we'll post them the day they exist."),
    ("How do I find out about opening night first?",
     "Email " + EMAIL + " or drop a note through the contact form and ask to be "
     "told when the date is set — opening news goes out that way."),
]

FAQ_OPENING = [
    ("Can the December–January window move?",
     "It can — it's a projected window, not a set date. It's what's on record as of "
     "November 2026, and this page gets updated the day that changes."),
    ("Has an opening night been announced?",
     "Not yet. Date, hours, and what's pouring are all still unannounced — email us "
     "and ask to be told when they're set."),
]

FAQ_BAR = [
    ("Why no food?",
     "The health inspection filing for 643 Penn Ave says bar service only, no food "
     "service. This is a drinking room by design and by paperwork."),
    ("So what can I get?",
     "Drinks — the exact list isn't announced. A bar from a brewing family, opened "
     "in West Reading; the details come when the team publishes them."),
]

FAQ_DETAIL_OPEN = [
    ("Is The Social open yet?",
     "Not yet — the bar is projected to open December 2026 to January 2027, and an "
     "opening night hasn't been announced."),
    ("Where exactly is it?",
     "643 Penn Ave, West Reading, PA 19611 — the former Willow Creek Brewing house, "
     "map above."),
    ("Who's behind the new bar?",
     "Erik Arizmendi, owner of Oakbrook Brewing and Taqueria Comalli — a "
     "West Reading team opening its first own-name bar."),
]

FAQ_DETAIL_DRINKS = [
    ("Does a drinks-only bar have a food license?",
     "No — the health inspection filing for 643 Penn Ave lists bar service only, "
     "with no food service."),
    ("Will there be a menu?",
     "No kitchen, so no food menu. The drinks list hasn't been announced yet; "
     "email us and we'll tell you when it's published."),
]

# ------------------------------------------------------------------ fragments
def faq_block(items):
    out = ['<section class="faq"><div class="inner"><h2>Questions people ask</h2>']
    for q, a in items:
        out.append('<details><summary>' + esc(q) + '</summary><p>' + esc(a) + '</p></details>')
    out.append('</div></section>')
    return "\n".join(out)

def mapbox(id_="map"):
    src = ('<section class="mapsec" id="' + id_ + '"><div class="mapgridwrap"><div class="mapwrap">'
           '<iframe title="Map of ' + esc(ADDR1) + ', ' + esc(CITY) + ', ' + esc(STATE) + ' ' + esc(ZIP) + '" '
           'src="' + MAPSRC + '" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
           '</div><div class="mapside"><h2>' + esc(ADDR1) + ', ' + esc(CITY) + '</h2>'
           '<p>' + esc(STATE) + ' ' + esc(ZIP) + ' — the old Willow Creek Brewing house on Penn Avenue. '
           'Same address you drove to for years; new bar inside.</p>'
           '<p class="addrline">' + esc(NAME) + '<br>' + esc(ADDR1) + '<br>' + esc(CITY) + ', ' + esc(STATE) + ' ' + esc(ZIP) + '</p>'
           '<p><a class="btn ghost" href="https://www.google.com/maps?q=' + MAPQ + '" target="_blank" rel="noopener">Open in Maps</a></p>'
           '</div></div></section>')
    return src

def cta_band():
    return ('<section class="ctaband"><div class="inner">'
            '<h2>Don&rsquo;t want to miss opening night?</h2>'
            '<p>The date isn&rsquo;t set yet — email us and ask to be told when it is. '
            'That&rsquo;s the whole ask.</p>'
            '<p class="bandcta"><a class="btn" href="/contact">Tell me when you open</a> '
            '<a class="btn ghost" href="mailto:' + EMAIL + '">' + esc(EMAIL) + '</a></p>'
            '</div></section>')

HEAD_TMPL = """<!DOCTYPE html>
""" + BUILT + """
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Social">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="mast">
  <a class="mark" href="/">The Social<span class="marktag">West Reading · PA</span></a>
  <nav aria-label="Main">
    <a href="/the-bar">The Bar</a>
    <a href="/opening">Opening</a>
    <a href="/contact">Contact</a>
    <a class="btn" href="/contact">Tell me when you open</a>
  </nav>
</header>
<main id="main">
"""

FOOTER = """</main>
<footer class="foot">
  <div class="footgrid">
    <div class="footbrand"><span class="footmark">The Social</span>
      <p>A new drinks-only bar from the owners of Oakbrook Brewing &amp; Taqueria Comalli. Opening December 2026 – January 2027.</p></div>
    <div class="footnap">
      <p class="addrline">The Social<br>643 Penn Ave<br>West Reading, PA 19611</p>
      <p><a href="mailto:TaqueriaComalli@gmail.com">TaqueriaComalli@gmail.com</a></p>
    </div>
    <div class="footlinks">
      <p><a href="/the-bar">The Bar</a> · <a href="/opening">Opening</a> · <a href="/contact">Contact</a> · <a href="/privacy">Privacy</a></p>
      <p class="sibs">Elsewhere from this team: <a href="https://oakbrookbrewing.com" target="_blank" rel="noopener">Oakbrook Brewing</a> · <a href="https://comallitacos.com" target="_blank" rel="noopener">Taqueria Comalli</a></p>
    </div>
  </div>
  <p class="footline">© 2026 The Social · West Reading, Pennsylvania · opening news goes out by email first</p>
</footer>
</body>
</html>
"""

def page(title, desc, path, ld_nodes, body):
    head = HEAD_TMPL.format(
        title=esc(title), desc=esc(desc),
        canon=esc(ORIGIN + path), img=esc(ORIGIN + "/og.png"),
        ld=graph(ld_nodes))
    return head + body + "\n" + FOOTER

def w(fname, text):
    with open(os.path.join(PUBLIC, fname), "w") as f:
        f.write(text)

# ---------------------------------------------------------------------- index
hero = ('<section class="hero"><div class="deco" aria-hidden="true">'
        '<span class="ring r1"></span><span class="ring r2"></span></div>'
        '<div class="heroinner">'
        '<p class="eyebrow">643 Penn Avenue · West Reading, Pennsylvania</p>'
        '<h1 class="bigtype">The Social</h1>'
        '<p class="herosub">A new drinks-only bar from the owners of Oakbrook Brewing &amp; '
        'Taqueria Comalli — going into the old Willow Creek Brewing house on Penn Avenue.</p>'
        '<ul class="chips"><li>Opening Dec 2026 – Jan 2027</li><li>Drinks only — no food service</li>'
        '<li>The old Willow Creek house</li></ul>'
        '<p class="herocta"><a class="btn" href="/contact">Tell me when you open</a> '
        '<a class="btn ghost" href="/the-bar">About the bar</a></p>'
        '</div></section>')

facts = ('<section class="facts"><div class="inner">'
         '<h2>Three things we know today</h2>'
         '<div class="cards">'
         '<article class="card"><h3>Drinks, full stop</h3><p>The health inspection filing for '
         '643 Penn Ave says it plain: bar service only, no food service. No kitchen, no menu — '
         'a room built for staying with a good drink.</p></article>'
         '<article class="card"><h3>An address West Reading already knows</h3><p>The Social takes '
         'over the Penn Avenue building years of Friday-night traffic knew as Willow Creek Brewing. '
         'Same old house, new purpose: a bar.</p></article>'
         '<article class="card"><h3>The people behind it</h3><p>The Social comes from the team '
         'behind Oakbrook Brewing and Taqueria Comalli — led by Erik Arizmendi, owner of both, '
         'two spots that have spent years serving this town.</p></article>'
         '</div>'
         '<p class="tbd"><b>Still to be announced:</b> hours · what&rsquo;s on tap and behind the '
         'bar · opening night. When the team says it, it lands on this page. Easiest way to hear '
         'it first: <a href="/contact">drop us a note</a>.</p>'
         '</div></section>')

story = ('<section class="story"><div class="inner">'
         '<h2>A drinking room, in a town with a drinking pedigree</h2>'
         '<p>West Reading does bars its own way: a brewery, a beloved taco counter, pub rooms '
         'where the bartender knows your round. The Social is pitched as that kind of '
         'regulars&rsquo; room — walk-up friendly, built for after-dinner and in-between, the '
         'kind of place you find out about from a friend.</p>'
         '<p>Nothing about it is finished yet — that&rsquo;s half the fun. The bones are a house '
         'West Reading already loves, and the people running it have spent years pouring beer '
         'and feeding neighborhoods a block or two away.</p>'
         '<p class="sibsline">In the meantime, the team&rsquo;s other spots are open: '
         '<a href="' + OAK + '" target="_blank" rel="noopener">Oakbrook Brewing</a> · '
         '<a href="' + COM + '" target="_blank" rel="noopener">Taqueria Comalli</a></p>'
         '<div class="srcline"><h3>What&rsquo;s confirmed — and where it came from</h3>'
         '<ul>'
         '<li>Name, address, drinks-only service — Berks County Eats coming-soon column '
         '(updated Nov 21, 2026), citing the county health-inspection report.</li>'
         '<li>Team ties (Oakbrook Brewing, Taqueria Comalli, Erik Arizmendi) — Berks County Eats; '
         'The Brewed At podcast, ep. 49; Paloma magazine (Jun 2025).</li>'
         '<li>Opening window December 2026 – January 2027 — Berks County Eats (projected; '
         'dates can move).</li>'
         '<li>As of Nov 25, 2026 no hours, drinks list, or opening-night details have been '
         'announced.</li>'
         '</ul></div>'
         '</div></section>')

index_body = hero + facts + story + faq_block(FAQ_MAIN) + mapbox() + cta_band()
w("index.html", page(
    "The Social — A New Drinks-Only Bar in West Reading, PA",
    "The Social is a new drinks-only bar from the owners of Oakbrook Brewing and Taqueria Comalli — in the old Willow Creek Brewing house at 643 Penn Ave, West Reading, PA 19611. Opening December 2026 to January 2027.",
    "/", [BAR, WEBSITE, faq(FAQ_MAIN), crumbs("Home", "/")],
    index_body))

# --------------------------------------------------------------------- the-bar
bar_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">The Bar</p>'
    '<h1>Drinks, full stop.</h1>'
    '<p class="lede">This is the sentence every part of The Social is built around: the health '
    'inspection filing for 643 Penn Ave lists bar service only — no food service. Not a '
    'restaurant with a bar attached. A bar.</p></div></section>'
    '<section class="prose"><div class="inner">'
    '<h2>What &ldquo;drinks only&rdquo; actually means for a night out</h2>'
    '<p>Eat before, or send out for something once you&rsquo;re parked at the room — but don&rsquo;t '
    'come hunting for a kitchen, because there isn&rsquo;t one. The whole visit is the drink order, '
    'the seat you settle into, and however long you feel like staying.</p>'
    '<p>&ldquo;Drinks only&rdquo; isn&rsquo;t a restriction — it&rsquo;s a design decision, filed on '
    'paper with the county and backed by the people making it. A brewery family opening its own '
    'bar, in a house built for drinking, with no kitchen in the plans. That&rsquo;s the concept, '
    'end to end.</p>'
    '<h2>What&rsquo;s on the lists</h2>'
    '<p>Nothing announced yet — not the taps, not the cocktail program, not the prices. But this '
    'is a bar from a brewing family, opened in a town that already queues for their taps; '
    'expect the beer side to be taken seriously, and expect the rest to arrive as a done idea, '
    'not a guess. When the drinks list exists, it lands here first.</p>'
    '<h2>The room</h2>'
    '<p>The house is the old Willow Creek Brewing building on Penn Avenue — if you&rsquo;ve spent '
    'a Friday night on that block in the last decade, you&rsquo;ve already sat in it. What changes '
    'inside hasn&rsquo;t been announced. What won&rsquo;t change: it&rsquo;s still the same familiar '
    'front door at 643.</p>'
    '<h2>Hours</h2>'
    '<p>To be announced before opening. Ask us to tell you when they&rsquo;re set — that&rsquo;s '
    'exactly what the contact form is for.</p>'
    '<p class="moreline">More: <a href="/bar-opening-west-reading">the opening details</a> · '
    '<a href="/drinks-only-bar-west-reading">the drinks-only side</a> · <a href="/opening">when it opens</a></p>'
    '</div></section>'
    + faq_block(FAQ_BAR) + mapbox() + cta_band())
w("the-bar.html", page(
    "The Bar — Drinks Only, The Social, West Reading PA",
    "Bar service only, no food service — that's the health filing for The Social, the new drinks-only bar at 643 Penn Ave, West Reading PA. What that means for a night out, in plain terms.",
    "/the-bar", [BAR, crumbs("The Bar", "/the-bar")],
    bar_body))

# --------------------------------------------------------------------- opening
open_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">Opening</p>'
    '<h1>December 2026 – January 2027</h1>'
    '<p class="lede">That&rsquo;s the projected window, per the coming-soon column covering the '
    'building (updated Nov 21, 2026). It&rsquo;s a window, not a nailed date — this page gets '
    'updated the day that changes.</p></div></section>'
    '<section class="prose"><div class="inner">'
    '<h2>Where things stand</h2>'
    '<ol class="timeline">'
    '<li><b>Nov 2026 — the name is on the street.</b> The Social shows up on the county&rsquo;s '
    'most-read food column&rsquo;s coming-soon list, and the health-inspection paperwork is '
    'already done: drinks only, no food service.</li>'
    '<li><b>Now — the in-between.</b> The house is between lives: closed as Willow Creek '
    'Brewing, becoming a bar. Hours, drinks program, and opening night are all yet to be '
    'announced.</li>'
    '<li><b>Dec 2026 – Jan 2027 — the projected window.</b> Openings in a former brewery '
    'space land when the work says so, not when a press release does. When a date is set, '
    'it&rsquo;s posted here and emailed to everyone who asked.</li>'
    '</ol>'
    '<h2>How to hear it first</h2>'
    '<p>Email <a href="mailto:' + EMAIL + '">' + esc(EMAIL) + '</a> or use the contact form '
    'and ask to be told when opening night and hours are set. Opening news goes out that '
    'way — this site updates the day announcements exist.</p>'
    '</div></section>'
    + faq_block(FAQ_OPENING) + mapbox() + cta_band())
w("opening.html", page(
    "Opening December 2026 – January 2027 — The Social, West Reading PA",
    "The Social, the new drinks-only bar at 643 Penn Ave in West Reading PA, is projected to open December 2026 to January 2027. Confirmed facts, what's TBD, and how to hear opening news first.",
    "/opening", [BAR, faq(FAQ_OPENING), crumbs("Opening", "/opening")],
    open_body))

# ------------------------------------------- detail 1: new bar opening (SEO)
d1_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">New bar opening</p>'
    '<h1>A new bar is opening in West Reading: The Social, 643 Penn Avenue</h1>'
    '<p class="lede">A new bar is coming to West Reading, Pennsylvania. The Social — a '
    'drinks-only bar from the team behind Oakbrook Brewing and Taqueria Comalli — takes over '
    'the former Willow Creek Brewing house, with a projected opening of December 2026 to '
    'January 2027.</p></div></section>'
    '<section class="prose"><div class="inner">'
    '<h2>The short version</h2>'
    '<ul class="factslist">'
    '<li><b>What:</b> The Social — a drinks-only bar (bar service only, per the county '
    'health-inspection report).</li>'
    '<li><b>Where:</b> ' + esc(NAP) + ' — the former Willow Creek Brewing house on Penn Avenue.</li>'
    '<li><b>When:</b> projected December 2026 to January 2027; opening night not yet '
    'announced.</li>'
    '<li><b>Who:</b> Erik Arizmendi — owner of Oakbrook Brewing and Taqueria Comalli, both '
    'West Reading businesses. The Social is the team&rsquo;s first own-name bar.</li>'
    '<li><b>Contact:</b> <a href="mailto:' + EMAIL + '">' + esc(EMAIL) + '</a> — the bar '
    'isn&rsquo;t open yet, and this inbox is monitored.</li>'
    '</ul>'
    '<h2>Why the address matters</h2>'
    '<p>643 Penn Avenue is not a blank spot on a map — for years it was Willow Creek '
    'Brewing, one of the places West Reading built its Friday nights around. The new bar '
    'keeps the house and changes what happens inside it: no kitchen, no food service, just '
    'the drinking end of a night out, run by people this town already drinks with.</p>'
    '<h2>Following the opening</h2>'
    '<p>No hours, drinks list, or opening-night plans have been announced as of November '
    '2026. This site is where the confirmed news lands, and emailed readers hear it '
    'first. <a href="/contact">Ask us to keep you posted.</a></p>'
    '</div></section>'
    + faq_block(FAQ_DETAIL_OPEN) + mapbox() + cta_band())
w("bar-opening-west-reading.html", page(
    "New Bar Opening in West Reading PA — The Social, 643 Penn Ave",
    "A new bar is opening in West Reading, PA: The Social, a drinks-only bar from the owners of Oakbrook Brewing & Taqueria Comalli, in the former Willow Creek Brewing house at 643 Penn Ave. Projected Dec 2026 – Jan 2027.",
    "/bar-opening-west-reading",
    [BAR, service("New bar opening — The Social",
                  "A new drinks-only bar at 643 Penn Ave, West Reading PA, projected to open December 2026 to January 2027.",
                  "/bar-opening-west-reading"),
     faq(FAQ_DETAIL_OPEN), crumbs("New Bar Opening", "/bar-opening-west-reading")],
    d1_body))

# ------------------------------------------- detail 2: drinks-only bar (SEO)
d2_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">Drinks only</p>'
    '<h1>A drinks-only bar for West Reading</h1>'
    '<p class="lede">&ldquo;Drinks only&rdquo; isn&rsquo;t marketing copy here — it&rsquo;s the '
    'health inspection filing. The county report on 643 Penn Ave lists bar service with no '
    'food service, and The Social is being built to exactly that brief.</p></div></section>'
    '<section class="prose"><div class="inner">'
    '<h2>A bar the paperwork agrees on</h2>'
    '<p>No kitchen means no food menu, no grill tickets, no &ldquo;we&rsquo;ll bring it out '
    'when it&rsquo;s ready.&rdquo; Order a drink, settle in, and the only thing between you and '
    'another round is asking for it. Dinner happens somewhere else in the neighborhood — '
    'which, on Penn Avenue and the blocks around it, is not a hardship.</p>'
    '<h2>Who to trust with a drinks-only room</h2>'
    '<p>The Social comes from Erik Arizmendi — owner of Oakbrook Brewing, a West Reading '
    'brewery, and Taqueria Comalli, a West Reading taqueria. A brewery family opening a '
    'room with nothing but drinks on the bill is a bet the town can live with; the drinks '
    'program itself hasn&rsquo;t been announced, and it&rsquo;ll be posted here when '
    'it&rsquo;s real.</p>'
    '<h2>By the numbers so far</h2>'
    '<ul class="factslist">'
    '<li><b>Service:</b> bar only — no food service (county health inspection report, '
    'via Berks County Eats, Nov 2026).</li>'
    '<li><b>Address:</b> ' + esc(NAP) + '.</li>'
    '<li><b>Opening:</b> projected December 2026 – January 2027.</li>'
    '<li><b>Hours / drinks list / opening night:</b> to be announced.</li>'
    '</ul>'
    '</div></section>'
    + faq_block(FAQ_DETAIL_DRINKS) + mapbox() + cta_band())
w("drinks-only-bar-west-reading.html", page(
    "Drinks-Only Bar in West Reading PA — The Social",
    "The Social is a drinks-only bar — bar service with no food service, per its county health filing — at 643 Penn Ave, West Reading PA 19611, from the owners of Oakbrook Brewing & Taqueria Comalli. Opening Dec 2026 – Jan 2027.",
    "/drinks-only-bar-west-reading",
    [BAR, service("Drinks-only bar — The Social",
                  "A bar serving drinks only, with no food service, at 643 Penn Ave, West Reading PA — opening December 2026 to January 2027.",
                  "/drinks-only-bar-west-reading"),
     faq(FAQ_DETAIL_DRINKS), crumbs("Drinks-Only Bar", "/drinks-only-bar-west-reading")],
    d2_body))

# --------------------------------------------------------------------- contact
contact_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">Contact</p>'
    '<h1>Talk to The Social before opening night</h1>'
    '<p class="lede">The bar hasn&rsquo;t opened — which makes now the easiest time to reach '
    'the people who run it. Opening-night questions, the address, what you&rsquo;d want in a '
    'drinks-only room on Penn Avenue: all fair game.</p></div></section>'
    '<section class="formsec"><div class="innerish"><div class="formwrap">'
    '<form method="post" action="/contact">'
    '<label>Your name*<input type="text" name="name" maxlength="120" required></label>'
    '<label>Phone<input type="tel" name="phone" maxlength="60"></label>'
    '<label>Email<input type="email" name="email" maxlength="120"></label>'
    '<label>Message*<textarea name="message" rows="5" maxlength="4000" required placeholder="Questions, requests — or just put me on the list for opening news"></textarea></label>'
    '<button class="btn" type="submit">Send it</button>'
    '</form>'
    '<p class="formnote">* required. Prefer email? <a href="mailto:' + EMAIL + '">' + esc(EMAIL) + '</a> — '
    'same crew, same bar.</p>'
    '</div>'
    '<div class="formaside"><h2>The Social</h2>'
    '<p class="addrline">' + esc(ADDR1) + '<br>' + esc(CITY) + ', ' + esc(STATE) + ' ' + esc(ZIP) + '</p>'
    '<p>Not open yet. Opening news: <a href="/opening">where things stand</a>. '
    '<a href="mailto:' + EMAIL + '">Email us</a> anytime.</p></div>'
    '</div></section>' + mapbox() + (
    '<section class="prose"><div class="inner"><h2>Good to know</h2>'
    '<p>This inbox also belongs to the team&rsquo;s other West Reading spots — Oakbrook '
    'Brewing and Taqueria Comalli — so if a reply comes signed with the Comalli name, '
    'it&rsquo;s the same crew answering for the bar. Expect answers about the bar through '
    'here while it&rsquo;s still pre-opening.</p></div></section>') + cta_band())
w("contact.html", page(
    "Contact — The Social, West Reading PA",
    "Not open yet, already reachable: contact The Social — the new drinks-only bar at 643 Penn Ave, West Reading PA — about opening night, the address, or anything else.",
    "/contact", [BAR, crumbs("Contact", "/contact")],
    contact_body))

# --------------------------------------------------------------------- privacy
priv_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">Privacy</p>'
    '<h1>Privacy</h1>'
    '<p class="lede">A bar website should not be a surveillance operation. Here&rsquo;s '
    'everything this site does with your information.</p></div></section>'
    '<section class="prose"><div class="inner">'
    '<h2>What gets collected</h2>'
    '<p>Only what you type into the contact form: your name, optionally a phone number and '
    'email, and your message. It&rsquo;s sent to the people who run The Social so they can '
    'answer you — opening news, questions, requests. It isn&rsquo;t sold, and it '
    'isn&rsquo;t added to some marketing machine behind your back.</p>'
    '<h2>Cookies and trackers</h2>'
    '<p>This site sets no cookies of its own, loads no third-party scripts, and shows no '
    'ads. The one exception is the map: the embedded Google map loads from Google, and '
    'Google may set cookies inside that map frame under its own policy.</p>'
    '<h2>Hosting</h2>'
    '<p>The site is hosted for The Social on standard, ad-free web hosting. Messages are '
    'delivered through an email provider that processes them to deliver them — nothing '
    'more.</p>'
    '<h2>Questions?</h2>'
    '<p>Email <a href="mailto:' + EMAIL + '">' + esc(EMAIL) + '</a> and ask.</p>'
    '</div></section>')
w("privacy.html", page(
    "Privacy — The Social, West Reading PA",
    "How The Social's website handles your contact-form message: collected to answer you, never sold, no cookies of its own, no third-party scripts, no ads.",
    "/privacy", [BAR, crumbs("Privacy", "/privacy")],
    priv_body))

# ------------------------------------------------------------------------ 404
e404_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">404</p>'
    '<h1>This page isn&rsquo;t on the menu</h1>'
    '<p class="lede">The bar isn&rsquo;t open yet either — but when it is, this is the '
    'address: 643 Penn Ave, West Reading, PA 19611.</p>'
    '<p class="herocta"><a class="btn" href="/">Back to the front page</a> '
    '<a class="btn ghost" href="/contact">Contact us</a></p></div></section>')
w("404.html", page(
    "Page Not Found — The Social, West Reading PA",
    "That page isn't here. The Social is — a new drinks-only bar at 643 Penn Ave, West Reading PA 19611, opening December 2026 to January 2027.",
    "/404", [BAR, crumbs("Page Not Found", "/404")],
    e404_body))

# ----------------------------------------------------------------------- thanks
thanks_body = (
    '<section class="pagehero"><div class="inner"><p class="eyebrow">Message sent</p>'
    '<h1>Message sent</h1>'
    '<p class="lede">It&rsquo;s with the people who run The Social. Opening news goes out to '
    'everyone who emailed — this page is where confirmed announcements land.</p>'
    '<p class="herocta"><a class="btn" href="/">Back to the front page</a> '
    '<a class="btn ghost" href="/opening">Where the opening stands</a></p></div></section>')
w("thanks.html", page(
    "Message Sent — The Social, West Reading PA",
    "Your message is with the people who run The Social — opening news goes out to email readers first.",
    "/thanks", [BAR, crumbs("Message Sent", "/thanks")],
    thanks_body))

# -------------------------------------------------------------- css / robots / sitemap
import shutil
css_src = os.path.join(HERE, "style.css")
shutil.copyfile(css_src, os.path.join(PUBLIC, "style.css"))

sitemap_urls = ["", "/the-bar", "/opening", "/bar-opening-west-reading",
                "/drinks-only-bar-west-reading", "/contact", "/privacy", "/thanks"]
with open(os.path.join(PUBLIC, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in sitemap_urls:
        f.write('<url><loc>' + ORIGIN + (u if u else "/") + '</loc></url>\n')
    f.write('</urlset>\n')

with open(os.path.join(PUBLIC, "robots.txt"), "w") as f:
    f.write('User-agent: *\nAllow: /\nDisallow: /open\n\nSitemap: ' + ORIGIN + '/sitemap.xml\n')

print("generated", len(os.listdir(PUBLIC)), "files into", PUBLIC)
