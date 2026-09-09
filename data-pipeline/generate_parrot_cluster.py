"""
generate_parrot_cluster.py
──────────────────────────
Generates the Parrot Fish (Blood Parrot Cichlid) care cluster under
/guides/parrot-fish-care/, following the betta/koi/discus cluster template
(artlay 2-column with sidebar cluster nav).

Run:  python3 generate_parrot_cluster.py
"""

from pathlib import Path
import json

REPO = Path(__file__).parent.parent
BASE = REPO / "guides" / "parrot-fish-care"

HERO_IMG = "/assets/encyclopedia/real/blood-parrot-cichlid-wikimedia-real.jpg"
DATE = "2026-09-08"

CLUSTER_NAV = [
    ("/guides/parrot-fish-care/",                  "\U0001F41F Parrot Fish Care Guide", "pillar"),
    ("/guides/parrot-fish-care/tank-size/",        "\U0001F5C3️ Tank Size & Setup"),
    ("/guides/parrot-fish-care/water-parameters/", "\U0001F321️ Water & Temperature"),
    ("/guides/parrot-fish-care/food/",             "\U0001F35A Food & Feeding"),
    ("/guides/parrot-fish-care/size-growth/",      "\U0001F4CF Size & Growth"),
    ("/guides/parrot-fish-care/lifespan/",         "⏳ Lifespan"),
    ("/guides/parrot-fish-care/types/",            "\U0001F3A8 Types & Colors"),
    ("/guides/parrot-fish-care/tank-mates/",       "\U0001F420 Tank Mates"),
    ("/guides/parrot-fish-care/breeding/",         "\U0001F95A Breeding & Babies"),
    ("/guides/parrot-fish-care/black-spots/",      "⚫ Black Spots"),
    ("/wiki/blood-parrot-cichlid/",                "\U0001F4D6 Species Profile"),
]

TOOL_LINKS = [
    ("/tools/tank-size-calculator/",       "Tank Size Calculator"),
    ("/tools/water-parameter-checker/",    "Water Parameter Checker"),
    ("/tools/fish-compatibility-checker/", "Compatibility Checker"),
]

CSS = """:root{--p:#1B5E8B;--pl:#2E84C0;--pd:#0F3D5E;--s:#2E9E7D;--a:#F5A623;--bg:#F0F7FF;--tx:#1A2B3C;--mu:#5A7A94;--bd:#D0E4F0;--ok:#27AE60;--wn:#F39C12;--er:#E74C3C}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:linear-gradient(180deg,#E6F7FF 0%,#F7FCFF 36%,#F0F7FF 100%);color:var(--tx);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--p);text-decoration:none}
.con{max-width:1180px;margin:0 auto;padding:0 22px}
h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;line-height:1.2}
h2{font-size:clamp(1.2rem,2.5vw,1.7rem);font-weight:700;line-height:1.25}
h3{font-size:1.1rem;font-weight:700}
p{margin-bottom:.85rem;color:var(--mu)}p:last-child{margin-bottom:0}
.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:8px;font-size:.9rem;font-weight:600;border:none;cursor:pointer;transition:all .18s;white-space:nowrap;text-decoration:none}
.bp{background:var(--p);color:#fff}.bp:hover{background:var(--pl)}
.bo{background:transparent;color:var(--p);border:2px solid var(--p)}.bo:hover{background:var(--p);color:#fff}
.tag{display:inline-block;background:rgba(27,94,139,.1);color:var(--p);padding:3px 11px;border-radius:20px;font-size:.73rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px}
.nb{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid var(--bd);padding:0 22px;height:64px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:8px;font-size:1.2rem;font-weight:800;color:var(--p);text-decoration:none}
.nlinks{display:flex;align-items:center;gap:2px}
.nl{padding:7px 13px;border-radius:8px;font-weight:500;font-size:.86rem;color:var(--mu);text-decoration:none;transition:all .15s}
.nl:hover,.nl.act{color:var(--p);background:rgba(27,94,139,.07)}
.hbg{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:7px;border:none;background:none}
.hbg span{display:block;width:21px;height:2px;background:var(--tx);border-radius:2px}
@media(max-width:760px){.nlinks{display:none;position:absolute;top:64px;left:0;right:0;background:#fff;flex-direction:column;padding:12px;border-bottom:1px solid var(--bd);gap:3px;box-shadow:0 4px 20px rgba(27,94,139,.12)}.nlinks.open{display:flex}.hbg{display:flex}}
.guide-hero{background:#0F3D5E;color:#fff;padding:70px 22px 48px;position:relative;overflow:hidden;min-height:300px;display:flex;align-items:flex-end}
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('/assets/encyclopedia/real/blood-parrot-cichlid-wikimedia-real.jpg') center/cover no-repeat}
.guide-hero::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:90px;background:linear-gradient(0deg,#E6F7FF,rgba(230,247,255,0));pointer-events:none}
.guide-hero .con{position:relative;z-index:1;padding:26px 22px;border-radius:26px;background:linear-gradient(135deg,rgba(255,255,255,.13),rgba(255,255,255,.04));border:1px solid rgba(255,255,255,.18);box-shadow:0 24px 70px rgba(0,0,0,.18);backdrop-filter:blur(7px)}
.guide-hero h1{color:#fff;margin:8px 0 10px;max-width:860px}
.guide-meta{display:flex;gap:14px;flex-wrap:wrap;color:rgba(255,255,255,.78);font-size:.86rem}
.breadcrumb{display:flex;align-items:center;gap:6px;flex-wrap:wrap;font-size:.8rem;color:rgba(255,255,255,.65);margin-bottom:12px}
.breadcrumb a{color:rgba(255,255,255,.75)}.breadcrumb a:hover{color:#fff}
.breadcrumb span{color:rgba(255,255,255,.45)}
.artlay{display:grid;grid-template-columns:1fr 270px;gap:32px;max-width:1180px;margin:32px auto 56px;padding:0 22px}
@media(max-width:900px){.artlay{grid-template-columns:1fr}.sidebar{display:none}}
.artc{background:rgba(255,255,255,.82);border:1px solid rgba(191,228,246,.9);border-radius:24px;padding:34px 40px;box-shadow:0 18px 48px rgba(15,61,110,.1);backdrop-filter:blur(14px)}
.artc h2{font-size:1.25rem;color:var(--pd);margin:28px 0 12px;padding-top:16px;border-top:1.5px solid var(--bd)}
.artc h2:first-child{margin-top:0;padding-top:0;border-top:none}
.artc h3{font-size:1.05rem;color:var(--tx);margin:18px 0 8px}
.artc p{font-size:.96rem;line-height:1.82;color:var(--mu);margin-bottom:13px}
.artc ul,.artc ol{margin:10px 0 14px 20px}
.artc li{font-size:.95rem;line-height:1.72;color:var(--mu);margin-bottom:5px}
.artc strong{color:var(--tx)}
.callout{background:rgba(248,250,254,.85);border:1px solid var(--bd);border-left:4px solid var(--p);border-radius:12px;padding:16px 18px;margin:20px 0}
.callout-warn{background:rgba(255,248,240,.85);border-left-color:var(--wn)}
.callout-ok{background:rgba(240,255,248,.85);border-left-color:var(--s)}
.ptbl{width:100%;border-collapse:collapse;margin:16px 0;font-size:.86rem;border-radius:16px;overflow:hidden;box-shadow:0 12px 30px rgba(15,61,110,.08)}
.ptbl th{background:var(--p);color:#fff;padding:10px 14px;text-align:left}
.ptbl td{padding:10px 14px;border-bottom:1px solid var(--bd);color:var(--mu);vertical-align:top}
.ptbl tr:nth-child(even) td{background:#F8FAFE}
.ptbl tr:last-child td{border-bottom:none}
.ptbl td:first-child{font-weight:600;color:var(--tx)}
.guide-links{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px}
.guide-links a{display:block;background:#fff;border:1px solid var(--bd);border-radius:8px;padding:13px;color:var(--tx);font-weight:700;font-size:.85rem;transition:border-color .15s,background .15s}
.guide-links a:hover{border-color:var(--p);background:#F8FAFE}
@media(max-width:600px){.guide-links{grid-template-columns:1fr}}
.sidebar{display:flex;flex-direction:column;gap:16px}
.toc{background:rgba(255,255,255,.9);border-radius:16px;padding:18px;border:1px solid var(--bd);position:sticky;top:84px;box-shadow:0 4px 18px rgba(27,94,139,.07)}
.toc h4{color:var(--pd);margin-bottom:11px;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.toc a{display:block;padding:5px 0 5px 10px;font-size:.82rem;color:var(--mu);border-left:2px solid transparent;transition:all .15s;line-height:1.4}
.toc a:hover{color:var(--p);border-left-color:var(--p)}
.cluster-nav{background:rgba(255,255,255,.9);border-radius:16px;padding:18px;border:1px solid var(--bd);box-shadow:0 4px 18px rgba(27,94,139,.07)}
.cluster-nav h4{color:var(--pd);margin-bottom:11px;font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.cluster-nav a{display:block;padding:6px 8px;font-size:.82rem;color:var(--mu);border-radius:6px;transition:all .12s;line-height:1.4;margin-bottom:2px}
.cluster-nav a:hover{color:var(--p);background:rgba(27,94,139,.06)}
.cluster-nav a.pillar{color:var(--pd);font-weight:700;border-bottom:1px solid var(--bd);padding-bottom:9px;margin-bottom:7px;display:block}
.cluster-nav a.cur{color:var(--p);background:rgba(27,94,139,.07);font-weight:600}
.tool-card{background:linear-gradient(135deg,rgba(27,94,139,.08),rgba(46,158,125,.06));border-radius:16px;padding:18px;border:1px solid var(--bd)}
.tool-card h4{color:var(--pd);margin-bottom:10px;font-size:.82rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.tool-card a{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-radius:8px;font-size:.84rem;font-weight:600;margin-bottom:7px;background:#fff;border:1px solid var(--bd);color:var(--p);transition:all .15s}
.tool-card a:hover{border-color:var(--p);box-shadow:0 3px 10px rgba(27,94,139,.1)}
.ft{background:#0F3D5E;padding:32px 22px 20px;margin-top:60px}
.ftb{text-align:center;color:rgba(255,255,255,.4);font-size:.76rem}"""


def cluster_nav_html(current_slug: str) -> str:
    items = []
    for entry in CLUSTER_NAV:
        href, label = entry[0], entry[1]
        css_class = entry[2] if len(entry) > 2 else ""
        if current_slug == "":
            is_cur = href == "/guides/parrot-fish-care/"
        else:
            is_cur = href.rstrip("/").endswith("/" + current_slug)
        cls = (css_class + " cur").strip() if is_cur else css_class
        items.append(f'<a href="{href}" class="{cls}">{label}</a>')
    return "\n      ".join(items)


def toc_html(sections):
    return "\n      ".join(f'<a href="#{sid}">{label}</a>' for sid, label in sections)


def tool_links_html():
    return "\n      ".join(
        f'<a href="{href}">{label} <span>&rarr;</span></a>' for href, label in TOOL_LINKS
    )


def faq_json(faqs):
    entities = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": entities}, ensure_ascii=False)


def faq_visible_html(faqs):
    rows = [f"    <h3>{q}</h3>\n    <p>{a}</p>" for q, a in faqs]
    return '    <h2 id="faq">Frequently Asked Questions</h2>\n' + "\n".join(rows)


def related_html(links):
    items = "".join(f'<a href="{href}" title="{label}">{label}</a>' for href, label in links)
    return ('    <h2 id="related">Related Parrot Fish Guides and Tools</h2>\n'
            f'    <div class="guide-links">{items}</div>')


def page(slug, title, meta_desc, h1, hero_tag, hero_meta,
         toc_sections, body_html, faqs, related, date=DATE):
    if slug:
        canonical = f"https://www.fishcareai.com/guides/parrot-fish-care/{slug}/"
        crumb_tail = (
            '<a href="/guides/parrot-fish-care/">Parrot Fish Care Guide</a><span>/</span>\n      '
            f'<span style="color:rgba(255,255,255,.9)">{hero_tag}</span>'
        )
        breadcrumb_items = (
            '{"@type":"ListItem","position":3,"name":"Parrot Fish Care Guide",'
            '"item":"https://www.fishcareai.com/guides/parrot-fish-care/"},'
            f'{{"@type":"ListItem","position":4,"name":{json.dumps(h1)},"item":"{canonical}"}}'
        )
    else:
        canonical = "https://www.fishcareai.com/guides/parrot-fish-care/"
        crumb_tail = f'<span style="color:rgba(255,255,255,.9)">{hero_tag}</span>'
        breadcrumb_items = (
            f'{{"@type":"ListItem","position":3,"name":{json.dumps(h1)},"item":"{canonical}"}}'
        )

    breadcrumb_json = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},'
        '{"@type":"ListItem","position":2,"name":"Guides","item":"https://www.fishcareai.com/guides/"},'
        + breadcrumb_items + "]}"
    )
    article_json = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": meta_desc,
        "datePublished": date, "dateModified": date,
        "image": f"https://www.fishcareai.com{HERO_IMG}",
        "author": {"@type": "Organization", "name": "FishCare AI Editorial Team"},
        "publisher": {"@type": "Organization", "name": "FishCare AI",
                      "url": "https://www.fishcareai.com"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }, ensure_ascii=False)

    full_body = body_html.rstrip() + "\n\n" + faq_visible_html(faqs) + "\n\n" + related_html(related)
    toc = list(toc_sections) + [("faq", "FAQ")]

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{meta_desc}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{canonical}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="FishCare AI"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:image" content="https://www.fishcareai.com{HERO_IMG}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{meta_desc}"/>
<meta name="twitter:image" content="https://www.fishcareai.com{HERO_IMG}"/>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{faq_json(faqs)}</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260908-artc-contrast"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl act" href="/guides/">Guides</a>
    <a class="nl" href="/species">Encyclopedia</a>
    <a class="nl" href="/fish-health/">Fish Health</a>
    <a title="Fish Identification" class="nl" href="https://fish-identification-d558af.anysites.app/" target="_blank" rel="noopener">&#128269; Fish ID</a>
    <a class="nl" href="/#tools">Tools</a>
    <a class="nl" href="/about/">About Us</a>
  </div>
  <button class="hbg" aria-label="Menu" onclick="document.querySelector('.nlinks').classList.toggle('open')">
    <span></span><span></span><span></span>
  </button>
</nav>

<section class="guide-hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="/guides/">Guides</a><span>/</span>
      {crumb_tail}
    </div>
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">&#129412; Parrot Fish Care</div>
    <h1>{h1}</h1>
    <div class="guide-meta">{hero_meta}</div>
  </div>
</section>

<div class="artlay">
  <article class="artc">
{full_body}
  </article>

  <aside class="sidebar">
    <div class="cluster-nav">
      <h4>Parrot Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc)}
    </div>
    <div class="tool-card">
      <h4>Parrot Fish Tools</h4>
      {tool_links_html()}
    </div>
  </aside>
</div>

<footer class="ft">
  <div class="con"><div class="ftb">&copy; 2026 FishCare AI. Practical freshwater fish care guides and tools.</div></div>
  <nav class="legal-links" aria-label="Legal"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


# ════════════════════════════════════════════════════════════════
# PILLAR — Parrot Fish Care Guide
# ════════════════════════════════════════════════════════════════
PILLAR_BODY = """    <p>Search "parrot fish" and you get two completely different animals. In the aquarium hobby it almost always means the <strong>blood parrot cichlid</strong> &mdash; the round, bright orange, permanently smiling hybrid sold in fish stores. In the ocean it means the <strong>marine parrotfish</strong> (family Scaridae), the beaked reef grazer that turns coral into sand. This guide covers the aquarium fish in full, and explains the marine species on the <a href="/guides/parrot-fish-care/types/">types and colors page</a>.</p>

    <h2 id="what-is">What Is a Blood Parrot Fish?</h2>
    <p>The blood parrot cichlid is a <strong>man-made hybrid</strong>, first bred in Taiwan around 1986. It has no scientific name and no wild population, because it does not exist in nature. The parent species are generally accepted to be the midas cichlid (<em>Amphilophus citrinellus</em>) crossed with the redhead cichlid (<em>Paraneetroplus synspilus</em>), though breeders have never published the exact line.</p>
    <p>The hybrid inherited a set of physical quirks that define how you have to keep it:</p>
    <ul>
      <li><strong>A deformed mouth</strong> that only opens into a narrow vertical slit and cannot fully close. Parrot fish cannot bite, tear or chase food properly &mdash; they suck it in from close range.</li>
      <li><strong>A compressed body and shortened spine</strong>, which makes them slow, wobbly swimmers that lose races to the food.</li>
      <li><strong>A reduced swim bladder cavity</strong> in some individuals, making them prone to buoyancy problems if overfed.</li>
      <li><strong>Male sterility.</strong> Almost all male blood parrots are infertile, so pairs lay eggs that never hatch. See <a href="/guides/parrot-fish-care/breeding/">breeding blood parrot fish</a>.</li>
    </ul>
    <p>None of that makes them hard to keep. It makes them a fish with specific requirements &mdash; sinking food, gentle tank mates, and enough space &mdash; and a personality that most cichlid keepers rate as the friendliest in the family.</p>

    <h2 id="quick-facts">Blood Parrot Fish Care at a Glance</h2>
    <table class="ptbl">
      <tr><th>Care factor</th><th>Requirement</th></tr>
      <tr><td>Adult size</td><td>7&ndash;8 inches (18&ndash;20 cm), occasionally 10 inches</td></tr>
      <tr><td>Lifespan</td><td>10&ndash;15 years, up to 20 in good conditions</td></tr>
      <tr><td>Minimum tank</td><td>30 gallons for one; 55&ndash;75 gallons for a pair</td></tr>
      <tr><td>Temperature</td><td>76&ndash;84&deg;F (24&ndash;29&deg;C)</td></tr>
      <tr><td>pH</td><td>6.5&ndash;7.4</td></tr>
      <tr><td>Hardness</td><td>6&ndash;18 dGH</td></tr>
      <tr><td>Ammonia / nitrite</td><td>0 ppm always</td></tr>
      <tr><td>Nitrate</td><td>Under 30 ppm</td></tr>
      <tr><td>Diet</td><td>Omnivore &mdash; sinking cichlid pellets, frozen foods, vegetables</td></tr>
      <tr><td>Temperament</td><td>Semi-aggressive but timid; territorial at spawning time</td></tr>
      <tr><td>Care level</td><td>Beginner to intermediate</td></tr>
    </table>

    <h2 id="tank">Tank Size and Setup</h2>
    <p>A single blood parrot needs <strong>30 gallons minimum</strong>, a pair needs 55&ndash;75 gallons, and a small group needs 100 gallons or more. They are wide-bodied fish that grow to 8 inches and produce a heavy waste load, so a long tank beats a tall one every time.</p>
    <p>Set the tank up around their weaknesses: soft sand or smooth rounded gravel (they dig), plenty of caves and driftwood for hiding, and <strong>moderate flow</strong> &mdash; a poor swimmer pinned against the outflow of an oversized powerhead is a stressed fish. Filtration should be rated for at least 1.5&times; the tank volume, with the return baffled if it is strong. Full detail is on the <a href="/guides/parrot-fish-care/tank-size/">parrot fish tank size guide</a>.</p>
    <div class="callout"><strong>Hiding is normal at first.</strong> Newly added blood parrots often spend two or three weeks wedged behind a rock. Add caves before the fish, keep the lights dim for the first week, and they come out. A parrot fish with nowhere to hide stays skittish permanently.</div>

    <h2 id="water">Water Parameters and Temperature</h2>
    <p>Blood parrots want warm, stable, clean water: <strong>76&ndash;84&deg;F (24&ndash;29&deg;C)</strong>, pH 6.5&ndash;7.4, and nitrate under 30 ppm. They tolerate a wide pH range, but they do not tolerate swings &mdash; a stable 7.6 is better than a pH you keep chasing back to 7.0 with chemicals.</p>
    <p>Change 25&ndash;30% of the water weekly. Their appetite and waste output are high for their size, and nitrate creep is the most common reason a parrot fish loses color. See <a href="/guides/parrot-fish-care/water-parameters/">parrot fish temperature and water parameters</a>.</p>

    <h2 id="food">Food and Feeding</h2>
    <p>Feed <strong>sinking</strong> pellets sized for the mouth &mdash; that mouth cannot chase floating food across the surface, and a parrot fish gulping air at the top is a buoyancy problem waiting to happen. A good weekly rotation:</p>
    <ul>
      <li><strong>Staple:</strong> sinking cichlid pellets with astaxanthin and spirulina for color, twice a day, as much as they finish in 2 minutes.</li>
      <li><strong>Protein:</strong> frozen bloodworms, brine shrimp or mysis 2&ndash;3 times a week.</li>
      <li><strong>Vegetable:</strong> blanched peas (also the fix for constipation), spirulina flake or zucchini once a week.</li>
      <li><strong>Fast:</strong> one no-food day per week keeps the gut working and blood parrots very rarely need more food than that.</li>
    </ul>
    <p>Full feeding schedule and color-food comparison: <a href="/guides/parrot-fish-care/food/">best food for parrot fish</a>.</p>

    <h2 id="mates">Tank Mates</h2>
    <p>Blood parrots are the contradiction of the cichlid world &mdash; territorial enough to chase, too timid and too badly built to fight well. The best tank mates are <strong>calm fish of similar size that are neither aggressive nor bite-sized</strong>: severums, silver dollars, larger tetras such as Congo tetras, giant danios, bristlenose plecos and corydoras.</p>
    <p>Avoid neon tetras and other small fish (they get eaten), tiger barbs and serpae tetras (they nip the slow-moving fins), and genuinely aggressive cichlids such as red devils, jaguars and Jack Dempseys. Oscars are the popular question &mdash; possible in 125 gallons or more, risky below that, and covered on the <a href="/guides/parrot-fish-care/tank-mates/">parrot fish tank mates page</a>.</p>

    <h2 id="colors">Color, Types and Dyed Fish</h2>
    <p>Blood parrots hatch brown-grey and turn orange at around 5&ndash;6 months. Natural colors are <strong>orange, red, yellow and occasionally a calico-style mix</strong>. There is no naturally blue, purple or green blood parrot.</p>
    <div class="callout callout-warn"><strong>Dyed parrot fish.</strong> "Jellybean", "blueberry", "purple" and "grape" parrots are dyed &mdash; the fish are injected with or dipped in dye, which is painful, damages the slime coat and shortens life. Many die within months. The blue and green parrot fish you find in image searches are marine parrotfish, not aquarium fish. Never buy dyed stock; the trade only continues because it sells.</div>
    <p>See <a href="/guides/parrot-fish-care/types/">types of parrot fish and colors</a> for the hybrid varieties (king kong, red mammon, short-body, heart parrot) and the marine parrotfish species.</p>

    <h2 id="health">Common Health Problems</h2>
    <ul>
      <li><strong>Faded or washed-out color</strong> &mdash; almost always stress, poor diet, or nitrate build-up rather than disease.</li>
      <li><strong>Black spots or black patches</strong> &mdash; usually healing ammonia burn or stress marbling, not an infection. Diagnostic walkthrough: <a href="/guides/parrot-fish-care/black-spots/">parrot fish black spots</a>.</li>
      <li><strong>Swim bladder / buoyancy trouble</strong> &mdash; overfeeding or gulped air. Fast 2 days, then feed blanched peas.</li>
      <li><strong>Ich (white spot)</strong> &mdash; white grains like salt; raise temperature to 82&deg;F and treat.</li>
      <li><strong>Hole-in-the-head (HLLE)</strong> &mdash; pitting above the eyes, linked to poor diet and stale nitrate-heavy water.</li>
    </ul>
    <p>Species-specific disease detail: <a href="/aquarium-fish-diseases/blood-parrot-cichlid-diseases/">blood parrot cichlid diseases</a>.</p>

    <h2 id="lifespan">Lifespan and Size</h2>
    <p>A well-kept blood parrot lives <strong>10&ndash;15 years</strong> and reaches 7&ndash;8 inches, with growth largely finished by year three. Fish kept in undersized tanks and fed a flake-only diet commonly die at 3&ndash;5 years, which is why the "5 year lifespan" figure circulates. See <a href="/guides/parrot-fish-care/lifespan/">parrot fish lifespan</a> and <a href="/guides/parrot-fish-care/size-growth/">how big parrot fish get</a>.</p>

    <h2 id="ethics">The Hybrid Question</h2>
    <p>Blood parrots are controversial. Their deformities are the direct result of selective hybrid breeding, and some countries and retailers refuse to stock them. That is a fair debate to have before you buy. What is not debatable is the standard once you own one: a fish with a mouth that barely works and a spine that limits its swimming deserves an appropriately sized tank, sinking food it can actually eat, and tank mates that will not outcompete or bully it.</p>
"""

PILLAR = {
    "slug": "",
    "title": "Parrot Fish Care Guide: Blood Parrot Cichlid Tank, Food & Lifespan",
    "meta_desc": "Complete parrot fish care guide: blood parrot cichlid tank size, water temperature, best food, tank mates, colors, lifespan and health problems explained.",
    "h1": "Parrot Fish Care Guide (Blood Parrot Cichlid)",
    "hero_tag": "Parrot Fish Care Guide",
    "hero_meta": "\U0001F4CF 7&ndash;8 inches &nbsp;|&nbsp; \U0001F5C3️ 30 gal minimum &nbsp;|&nbsp; ⏳ 10&ndash;15 years &nbsp;|&nbsp; \U0001F321️ 76&ndash;84&deg;F",
    "toc_sections": [
        ("what-is", "What Is a Parrot Fish?"),
        ("quick-facts", "Care at a Glance"),
        ("tank", "Tank Size & Setup"),
        ("water", "Water & Temperature"),
        ("food", "Food & Feeding"),
        ("mates", "Tank Mates"),
        ("colors", "Colors & Types"),
        ("health", "Health Problems"),
        ("lifespan", "Lifespan & Size"),
        ("ethics", "The Hybrid Question"),
    ],
    "body": PILLAR_BODY,
    "faqs": [
        ("What is a blood parrot fish?",
         "The blood parrot cichlid is a man-made hybrid first bred in Taiwan around 1986, generally accepted to be a cross between the midas cichlid and the redhead cichlid. It has no scientific name and no wild population, and it inherited a deformed mouth that cannot fully close plus a compressed spine."),
        ("How big do parrot fish get?",
         "Blood parrot cichlids reach 7-8 inches (18-20 cm) at adult size, with exceptional fish hitting 10 inches. Most growth happens in the first 18 months and is essentially finished by year three."),
        ("How long do parrot fish live?",
         "A well-kept blood parrot fish lives 10-15 years, and 20 years is possible. Fish kept in tanks under 30 gallons or fed a flake-only diet commonly die at 3-5 years."),
        ("What size tank does a parrot fish need?",
         "Thirty gallons is the minimum for a single blood parrot, 55-75 gallons suits a pair, and 100 gallons or more is needed for a group or a mixed cichlid community. Length matters more than height for these poor swimmers."),
        ("Are blood parrot fish aggressive?",
         "They are semi-aggressive but unusually timid for cichlids. They will claim a cave and chase intruders away from it, particularly when spawning, but their deformed mouth means they rarely do real damage and they are frequently bullied by more capable fish."),
        ("Are blue and purple parrot fish real?",
         "No. Blood parrot cichlids are naturally orange, red, yellow or calico. Blue, purple and 'jellybean' parrots are artificially dyed, which damages the slime coat and shortens life. The blue and green parrot fish in photos are marine parrotfish from coral reefs, not aquarium fish."),
    ],
    "related": [
        ("/guides/parrot-fish-care/tank-size/", "Parrot Fish Tank Size"),
        ("/guides/parrot-fish-care/tank-mates/", "Parrot Fish Tank Mates"),
        ("/guides/parrot-fish-care/food/", "Best Food for Parrot Fish"),
        ("/wiki/blood-parrot-cichlid/", "Blood Parrot Species Profile"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Tank Size & Setup
# ════════════════════════════════════════════════════════════════
TANK_SIZE_BODY = """    <p>The single most common blood parrot mistake is a 20-gallon tank. These fish reach 7&ndash;8 inches, are as wide as they are tall, dig constantly and produce a waste load closer to an oscar's than a goldfish's. This page covers the parrot fish tank size you actually need, how to lay the aquarium out around their poor swimming, and the equipment that matters.</p>

    <h2 id="minimum">Parrot Fish Tank Size: The Numbers</h2>
    <p><strong>Thirty gallons is the working minimum for one blood parrot fish.</strong> That is a fish reaching 8 inches in a tank 36 inches long &mdash; adequate, not generous. Every parrot fish after the first adds roughly 20&ndash;25 gallons.</p>
    <table class="ptbl">
      <tr><th>Tank size</th><th>Blood parrots</th><th>Verdict</th></tr>
      <tr><td>10&ndash;20 gal</td><td>&#10060; None</td><td>Too small even for a juvenile beyond a few months</td></tr>
      <tr><td>30 gal</td><td>1</td><td>Minimum for a single adult; no room for tank mates</td></tr>
      <tr><td>55 gal</td><td>2</td><td>Comfortable pair, or one parrot plus a small clean-up crew</td></tr>
      <tr><td>75 gal</td><td>2&ndash;3</td><td>The sweet spot &mdash; room for territory and dither fish</td></tr>
      <tr><td>100&ndash;125 gal</td><td>4&ndash;5</td><td>Group or mixed cichlid community; needed for oscars</td></tr>
      <tr><td>150 gal+</td><td>6&ndash;8</td><td>Full community with severums, silver dollars and plecos</td></tr>
    </table>
    <p>Run your own stocking numbers with the <a href="/tools/tank-size-calculator/">tank size calculator</a>.</p>
    <div class="callout"><strong>Footprint beats gallons.</strong> A 40-gallon breeder (36 &times; 18 in) is a far better parrot fish tank than a 40-gallon tall column, because blood parrots swim horizontally and claim floor territory. When two tanks hold the same volume, pick the longer, wider one.</div>

    <h2 id="juveniles">"But Mine Is Tiny"</h2>
    <p>Blood parrots are sold at 1&ndash;2 inches and look absurd in a 30-gallon tank. They will not stay that size: expect 4&ndash;5 inches by the end of year one and near-adult size by year two. Growing a parrot fish out in a small tank does not keep it small &mdash; it stunts the body while the internal organs keep developing, which is a documented cause of early death in cichlids. Buy the adult tank first, or grow-out in a small tank for no more than six months. See <a href="/guides/parrot-fish-care/size-growth/">parrot fish size and growth</a>.</p>

    <h2 id="layout">Parrot Fish Aquarium Layout</h2>
    <p>Design the aquascape around a fish that hides more than most cichlids and swims worse than all of them.</p>
    <ul>
      <li><strong>Substrate:</strong> soft sand or smooth rounded gravel. Blood parrots dig and rearrange, and sharp gravel scratches mouths that already cannot close properly.</li>
      <li><strong>Caves:</strong> at least one cave per fish, plus one spare. Terracotta pots on their side, rock overhangs and PVC pipe all work. This is the single biggest factor in whether a new parrot fish settles in.</li>
      <li><strong>Driftwood:</strong> breaks sightlines so territorial fish cannot see each other constantly.</li>
      <li><strong>Plants:</strong> anything rooted gets dug up. Use anubias, java fern and bucephalandra tied to wood and rock, or accept plastic plants.</li>
      <li><strong>Open swimming lane:</strong> keep the front third of the tank clear. They are clumsy and need room to turn.</li>
      <li><strong>Lid:</strong> essential. Startled cichlids jump.</li>
    </ul>

    <h2 id="filtration">Filtration and Flow</h2>
    <p>Blood parrots are messy eaters with a heavy bioload, so filter for <strong>at least 1.5 times the tank volume</strong> in rated turnover &mdash; a canister rated 350 GPH on a 55-gallon tank, or two HOB filters splitting the load. Over-filtering is nearly impossible; over-flowing is easy.</p>
    <p>Because of the shortened spine and compressed body, a parrot fish pushed around by a strong return spends its day fighting current instead of eating. Baffle the outflow with a spray bar, aim it at the glass, or run a wider, slower filter rather than a narrow jet. You want visible surface movement for gas exchange, not a river.</p>
    <table class="ptbl">
      <tr><th>Equipment</th><th>Specification</th></tr>
      <tr><td>Filter</td><td>1.5&ndash;2&times; tank volume per hour, baffled output</td></tr>
      <tr><td>Heater</td><td>3&ndash;5 watts per gallon, set to 80&deg;F (27&deg;C)</td></tr>
      <tr><td>Thermometer</td><td>Separate from the heater &mdash; heater dials drift</td></tr>
      <tr><td>Air stone</td><td>Optional but useful in warm water above 82&deg;F</td></tr>
      <tr><td>Test kit</td><td>Liquid kit for ammonia, nitrite, nitrate and pH</td></tr>
      <tr><td>Siphon</td><td>Gravel vacuum &mdash; used every water change</td></tr>
    </table>

    <h2 id="cycling">Cycle Before the Fish</h2>
    <p>Blood parrots are not delicate, but they are ammonia-sensitive enough that a fish-in cycle usually shows up later as black burn marks around the head and fins. Cycle the tank for 4&ndash;6 weeks with an ammonia source until it processes 2 ppm of ammonia to 0 ammonia and 0 nitrite within 24 hours, then add fish. If you already have fish in an uncycled tank, do daily 25% water changes and dose a dechlorinator that binds ammonia until the readings settle. See <a href="/guides/parrot-fish-care/black-spots/">parrot fish black spots</a> for what ammonia damage looks like.</p>

    <h2 id="maintenance">Maintenance Schedule</h2>
    <table class="ptbl">
      <tr><th>Frequency</th><th>Task</th></tr>
      <tr><td>Daily</td><td>Feed 1&ndash;2 times, check behaviour, confirm heater temperature</td></tr>
      <tr><td>Weekly</td><td>25&ndash;30% water change with gravel vacuum; test nitrate and pH</td></tr>
      <tr><td>Monthly</td><td>Rinse filter media in old tank water (never tap water); check equipment</td></tr>
      <tr><td>Every 6 months</td><td>Replace worn media, inspect heater and impeller</td></tr>
    </table>
"""

TANK_SIZE = {
    "slug": "tank-size",
    "title": "Blood Parrot Fish Tank Size: How Many Gallons Do They Need?",
    "meta_desc": "Parrot fish tank size explained: 30 gallons minimum for one blood parrot, 55-75 for a pair. Aquarium layout, filtration, flow and maintenance schedule.",
    "h1": "Parrot Fish Tank Size and Aquarium Setup",
    "hero_tag": "Tank Size & Setup",
    "hero_meta": "\U0001F5C3️ 30 gal for one &nbsp;|&nbsp; \U0001F465 55&ndash;75 gal for a pair &nbsp;|&nbsp; \U0001F504 1.5&times; turnover",
    "toc_sections": [
        ("minimum", "Tank Size Numbers"),
        ("juveniles", "But Mine Is Tiny"),
        ("layout", "Aquarium Layout"),
        ("filtration", "Filtration & Flow"),
        ("cycling", "Cycle First"),
        ("maintenance", "Maintenance"),
    ],
    "body": TANK_SIZE_BODY,
    "faqs": [
        ("What size tank do blood parrot fish need?",
         "A single blood parrot cichlid needs 30 gallons minimum. A pair needs 55-75 gallons, and a group or mixed cichlid community needs 100 gallons or more. Each additional parrot fish adds roughly 20-25 gallons."),
        ("Can a blood parrot live in a 20 gallon tank?",
         "Only temporarily, as grow-out space for a juvenile under about 3 inches. An adult reaches 7-8 inches and produces a heavy waste load, and keeping one long term in 20 gallons stunts growth and shortens lifespan."),
        ("How many parrot fish can I keep in a 55 gallon tank?",
         "Two blood parrots comfortably, or one parrot fish plus a few calm tank mates such as corydoras or a bristlenose pleco. Three in a 55 usually leads to one fish being cornered."),
        ("Do parrot fish need a strong filter?",
         "Yes for capacity, no for current. Filter at 1.5-2 times the tank volume per hour, but baffle the output with a spray bar or aim it at the glass. Blood parrots swim poorly and struggle in strong flow."),
        ("Do blood parrot fish need a heater?",
         "Yes. They need 76-84 degrees Fahrenheit year-round, so a heater rated 3-5 watts per gallon set to 80 degrees is required in almost every home aquarium."),
    ],
    "related": [
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
        ("/guides/parrot-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/parrot-fish-care/size-growth/", "Parrot Fish Size & Growth"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Water Parameters & Temperature
# ════════════════════════════════════════════════════════════════
WATER_BODY = """    <p>Blood parrot cichlids are hybrids of Central American species, and they inherited that region's water preferences: warm, moderately hard, near-neutral. They are tolerant of a range, and intolerant of change. This page covers parrot fish temperature, the full parameter set, and the water-change routine that keeps their color bright.</p>

    <h2 id="temperature">Parrot Fish Temperature: 76&ndash;84&deg;F</h2>
    <p>The safe range for blood parrot fish is <strong>76&ndash;84&deg;F (24&ndash;29&deg;C)</strong>, and <strong>80&deg;F (27&deg;C)</strong> is the setting most keepers land on. Warm water raises metabolism, appetite, color development and immune response; cool water does the opposite and is a common trigger for ich.</p>
    <table class="ptbl">
      <tr><th>Temperature</th><th>Effect on blood parrots</th></tr>
      <tr><td>Below 72&deg;F (22&deg;C)</td><td>&#10060; Lethargy, refused food, suppressed immunity, ich risk</td></tr>
      <tr><td>72&ndash;76&deg;F (22&ndash;24&deg;C)</td><td>&#9888;&#65039; Survivable but slow growth and dulled color</td></tr>
      <tr><td>76&ndash;84&deg;F (24&ndash;29&deg;C)</td><td>&#9989; Correct range &mdash; active, feeding, coloring up</td></tr>
      <tr><td>82&ndash;84&deg;F (28&ndash;29&deg;C)</td><td>&#9989; Breeding and ich-treatment range; add aeration</td></tr>
      <tr><td>Above 86&deg;F (30&deg;C)</td><td>&#10060; Oxygen falls, fish gasp at the surface</td></tr>
    </table>
    <p>Use a heater rated 3&ndash;5 watts per gallon and verify with a separate thermometer &mdash; built-in heater dials are routinely off by 2&ndash;4 degrees. In tanks above 55 gallons, two smaller heaters at opposite ends beat one large one: you get even heat, and a failure is half a failure.</p>

    <h2 id="parameters">Full Water Parameters</h2>
    <table class="ptbl">
      <tr><th>Parameter</th><th>Target</th><th>Notes</th></tr>
      <tr><td>Temperature</td><td>76&ndash;84&deg;F (24&ndash;29&deg;C)</td><td>80&deg;F is the practical default</td></tr>
      <tr><td>pH</td><td>6.5&ndash;7.4</td><td>Stability matters more than the exact figure</td></tr>
      <tr><td>Hardness (GH)</td><td>6&ndash;18 dGH</td><td>Tolerant; most tap water is fine</td></tr>
      <tr><td>Carbonate hardness (KH)</td><td>4&ndash;10 dKH</td><td>Buffers against pH crashes</td></tr>
      <tr><td>Ammonia</td><td>0 ppm</td><td>Anything above 0 causes damage</td></tr>
      <tr><td>Nitrite</td><td>0 ppm</td><td>Anything above 0 causes damage</td></tr>
      <tr><td>Nitrate</td><td>Under 30 ppm</td><td>Under 20 ppm for breeding condition</td></tr>
    </table>
    <p>Check your readings against the safe ranges with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="ph">pH: Leave It Alone</h2>
    <p>Blood parrots do best at pH 6.5&ndash;7.4 but live perfectly well at 7.8 or 8.0 if it is steady. The damage in most tanks comes from the owner, not the number &mdash; pH-down products, peat, and driftwood added mid-cycle produce a sawtooth pH that stresses fish far more than a stable "wrong" value.</p>
    <p>If you genuinely need to lower pH, do it slowly with RO water blended into your tap water at water-change time, and never move pH more than 0.2 units in a day. If your KH is below 3 dKH your pH will swing on its own; add crushed coral to the filter to stabilise it.</p>
    <div class="callout callout-warn"><strong>The overnight pH drop.</strong> In a heavily stocked, lightly aerated tank, CO&#8322; builds up at night and pH falls by half a point or more before dawn. If your pH tests differently in the morning than the evening, the fix is aeration and a bigger water change schedule, not a buffer product.</div>

    <h2 id="ammonia">Ammonia, Nitrite and Nitrate</h2>
    <p>Blood parrots eat heavily and are messy, so nitrogen control is the daily work of keeping them. Ammonia and nitrite must read <strong>0 ppm</strong> at all times &mdash; both burn gill tissue and skin, and ammonia burn is the single most common cause of the <a href="/guides/parrot-fish-care/black-spots/">black spots</a> owners panic about.</p>
    <p>Nitrate is the slow one. It climbs between water changes and has no immediate symptom, which is why it wrecks so many tanks. Above roughly 40 ppm, blood parrots fade, stop growing and become HLLE-prone. Keep it under 30 ppm with weekly changes and it is a non-issue.</p>

    <h2 id="water-changes">Water Change Routine</h2>
    <ul>
      <li><strong>Weekly 25&ndash;30%</strong> in a normally stocked tank, gravel-vacuuming as you go.</li>
      <li><strong>Match the temperature</strong> of the new water within about 2&deg;F. Cold-water refills are a classic ich trigger.</li>
      <li><strong>Dechlorinate always.</strong> Chlorine and chloramine kill filter bacteria as well as damaging fish gills.</li>
      <li><strong>Rinse filter media in old tank water</strong>, never under the tap &mdash; tap water sterilises the biofilter.</li>
      <li><strong>After a heavy feed or a lost fish</strong>, do an extra change rather than waiting for the schedule.</li>
    </ul>

    <h2 id="troubleshooting">Water Problem Troubleshooting</h2>
    <table class="ptbl">
      <tr><th>Symptom</th><th>Likely water cause</th><th>Fix</th></tr>
      <tr><td>Gasping at the surface</td><td>Low oxygen or high temperature</td><td>Add aeration, lower temperature toward 78&deg;F</td></tr>
      <tr><td>Faded orange color</td><td>Nitrate build-up or stress</td><td>Larger, more frequent water changes</td></tr>
      <tr><td>Clamped fins, hiding</td><td>Ammonia or nitrite above 0</td><td>Daily 25% changes until readings clear</td></tr>
      <tr><td>Rubbing on decor</td><td>Irritants or parasites</td><td>Test water first, then treat if parameters are clean</td></tr>
      <tr><td>White spots</td><td>Ich, often after a cold water change</td><td>Raise to 82&deg;F and treat</td></tr>
      <tr><td>Cloudy white water</td><td>Bacterial bloom in a new tank</td><td>Stop overfeeding; let the cycle finish</td></tr>
    </table>
"""

WATER = {
    "slug": "water-parameters",
    "title": "Parrot Fish Temperature & Water Parameters (76-84°F Guide)",
    "meta_desc": "Blood parrot fish temperature is 76-84°F with 80°F ideal. Full water parameters, pH, ammonia and nitrate targets, water change routine and troubleshooting.",
    "h1": "Parrot Fish Temperature and Water Parameters",
    "hero_tag": "Water & Temperature",
    "hero_meta": "\U0001F321️ 76&ndash;84&deg;F &nbsp;|&nbsp; ⚗️ pH 6.5&ndash;7.4 &nbsp;|&nbsp; \U0001F4A7 25&ndash;30% weekly",
    "toc_sections": [
        ("temperature", "Temperature Range"),
        ("parameters", "Full Parameters"),
        ("ph", "pH Guidance"),
        ("ammonia", "Ammonia & Nitrate"),
        ("water-changes", "Water Changes"),
        ("troubleshooting", "Troubleshooting"),
    ],
    "body": WATER_BODY,
    "faqs": [
        ("What temperature do blood parrot fish need?",
         "Blood parrot cichlids need 76-84 degrees Fahrenheit (24-29 Celsius), and 80 degrees is the practical default. Below 72 degrees they stop eating and become vulnerable to ich; above 86 degrees oxygen levels fall too far."),
        ("What pH do parrot fish need?",
         "A pH of 6.5-7.4 is ideal, but blood parrots live well at 7.8 or higher as long as it is stable. Chasing a target pH with chemicals causes far more stress than a steady reading slightly outside the ideal range."),
        ("How often should I change the water for parrot fish?",
         "Change 25-30% weekly with a gravel vacuum. Blood parrots eat heavily and produce a lot of waste, so nitrate climbs faster than in a comparably sized community tank."),
        ("Why is my parrot fish losing its color?",
         "The usual causes are nitrate build-up, stress from bullying or a new tank, a diet without carotenoids, or temperature below the correct range. Test nitrate first, then review diet and tank mates before assuming disease."),
        ("Can parrot fish live in cold water?",
         "No. They are tropical hybrids of Central American cichlids and need heated water above 76 degrees Fahrenheit. Unheated room-temperature tanks leave them lethargic, off their food and prone to disease."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/parrot-fish-care/tank-size/", "Parrot Fish Tank Size"),
        ("/guides/parrot-fish-care/black-spots/", "Parrot Fish Black Spots"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Food & Feeding
# ════════════════════════════════════════════════════════════════
FOOD_BODY = """    <p>Blood parrot fish are omnivores with a serious handicap: the hybrid mouth opens into a narrow vertical slit and cannot close fully, so they cannot bite chunks, tear flesh or snap food out of the water column. Everything about parrot fish food comes back to that. This page covers what blood parrot fish eat, the best food for color, how much and how often, and what to avoid.</p>

    <h2 id="what-they-eat">What Do Blood Parrot Fish Eat?</h2>
    <p>In practical terms a blood parrot eats <strong>small sinking pellets, frozen meaty foods and soft vegetables</strong>. They are opportunistic omnivores by inheritance &mdash; the midas and redhead cichlids that produced them eat insect larvae, small crustaceans, plant matter and detritus &mdash; so a mixed diet suits them better than any single food.</p>
    <p>Two rules govern every choice:</p>
    <ul>
      <li><strong>Sinking, not floating.</strong> A parrot fish chasing floating pellets gulps air, and gulped air is the leading cause of the buoyancy problems these fish are known for. Sinking food also lets them feed the way their mouth actually works &mdash; hovering over it and sucking it in.</li>
      <li><strong>Small, not large.</strong> Pellets around 1&ndash;3 mm for juveniles and 3&ndash;5 mm for adults. A pellet too big for the mouth slit gets mouthed, spat out, and left to rot.</li>
    </ul>

    <h2 id="best-food">Best Food for Parrot Fish</h2>
    <table class="ptbl">
      <tr><th>Food type</th><th>Role</th><th>How often</th></tr>
      <tr><td>Sinking cichlid pellets (color formula)</td><td>Staple &mdash; 60&ndash;70% of the diet</td><td>Daily</td></tr>
      <tr><td>Frozen bloodworms</td><td>Protein and conditioning; highly palatable</td><td>2&ndash;3&times; weekly</td></tr>
      <tr><td>Frozen brine shrimp / mysis</td><td>Protein plus natural carotenoids</td><td>2&ndash;3&times; weekly</td></tr>
      <tr><td>Blanched peas (shelled)</td><td>Fibre; the standard constipation fix</td><td>Weekly</td></tr>
      <tr><td>Spirulina flake or wafer</td><td>Plant matter and color support</td><td>Weekly</td></tr>
      <tr><td>Blanched zucchini or spinach</td><td>Vegetable variety</td><td>Occasional</td></tr>
      <tr><td>Live blackworms</td><td>Treat; stimulates a fussy eater</td><td>Occasional</td></tr>
    </table>
    <p>For the staple, look for a sinking cichlid pellet listing <strong>astaxanthin, spirulina, krill or shrimp meal</strong> in the first several ingredients &mdash; those are the carotenoid sources that maintain the orange. Whole fish meal or krill meal as the first ingredient beats "fish derivatives" or wheat flour.</p>

    <h2 id="color">Feeding for Color</h2>
    <p>Blood parrot orange is <strong>pigment-dependent</strong>. The fish cannot synthesise carotenoids and has to eat them, so a parrot fish on a cheap wheat-based flake will fade over months regardless of how clean the water is. Colour-enhancing foods are not a gimmick for this species; they are maintenance.</p>
    <ul>
      <li><strong>Astaxanthin</strong> &mdash; the strongest red/orange enhancer, found in krill, shrimp and dedicated colour pellets.</li>
      <li><strong>Spirulina</strong> &mdash; supports colour and provides plant matter in one food.</li>
      <li><strong>Frozen krill and brine shrimp</strong> &mdash; natural carotenoid sources, and blood parrots take them enthusiastically.</li>
    </ul>
    <div class="callout callout-warn"><strong>Colour food will not fix a stress problem.</strong> If a parrot fish faded in days rather than months, the cause is water quality, bullying or temperature &mdash; not diet. Test nitrate and check the <a href="/guides/parrot-fish-care/tank-mates/">tank mate list</a> before buying a new food.</div>

    <h2 id="how-much">How Much and How Often</h2>
    <p>Feed adults <strong>twice a day, only what they finish in about two minutes</strong>. Juveniles under 3 inches can take three smaller meals a day while they are growing. One fasting day per week is good practice &mdash; blood parrots are prone to constipation and buoyancy trouble, and a day without food lets the gut clear.</p>
    <table class="ptbl">
      <tr><th>Age / size</th><th>Feedings per day</th><th>Portion</th></tr>
      <tr><td>Juvenile, under 3 in</td><td>2&ndash;3</td><td>What is eaten in 1&ndash;2 minutes</td></tr>
      <tr><td>Adult, 4&ndash;8 in</td><td>2</td><td>What is eaten in 2 minutes</td></tr>
      <tr><td>Any age, fast day</td><td>0</td><td>One day per week</td></tr>
    </table>
    <p>Overfeeding is the more common error by a wide margin. Blood parrots beg constantly, learn to recognise their owner, and look convincingly starved. Uneaten food fuels nitrate, and an overfed parrot develops the bloated, tilting profile that gets mistaken for swim bladder disease.</p>

    <h2 id="fussy">The Fish That Will Not Eat</h2>
    <p>Newly bought blood parrots often refuse food for the first several days. That is normal &mdash; they are timid, and a fish still hiding behind a rock will not come out to eat. Steps that work, in order:</p>
    <ol>
      <li>Confirm the temperature is at least 78&deg;F. Cold fish do not eat.</li>
      <li>Test ammonia, nitrite and nitrate. A fish in bad water shuts its appetite down first.</li>
      <li>Dim the lights and feed sinking food near the cave rather than at the surface.</li>
      <li>Offer frozen bloodworms &mdash; almost nothing refuses them &mdash; then mix pellets in gradually.</li>
      <li>Check for bullying. A parrot fish being chased off the food eats nothing and hides more.</li>
    </ol>
    <p>A fish that still refuses food after a week in clean, warm water with no aggression needs a health check, not a new food.</p>

    <h2 id="avoid">What Not to Feed</h2>
    <ul>
      <li><strong>Floating pellets and sticks</strong> &mdash; cause air gulping and buoyancy problems.</li>
      <li><strong>Large pellets</strong> &mdash; the mouth cannot handle them; they get spat out and rot.</li>
      <li><strong>Feeder goldfish</strong> &mdash; a genuine disease and thiaminase risk, and blood parrots are poor hunters anyway.</li>
      <li><strong>Mammal meat</strong> (beef heart as a staple) &mdash; the fat is not digestible for cichlids at aquarium temperatures.</li>
      <li><strong>Bread and human snacks</strong> &mdash; no nutritional value, fouls the water.</li>
      <li><strong>Freeze-dried food fed dry</strong> &mdash; expands in the gut. Soak it in tank water first.</li>
    </ul>
"""

FOOD = {
    "slug": "food",
    "title": "Best Food for Parrot Fish: What Blood Parrots Eat & How Much",
    "meta_desc": "Best food for blood parrot fish: sinking colour-enhancing cichlid pellets, frozen bloodworms and vegetables. Feeding schedule, portions and foods to avoid.",
    "h1": "Best Food for Parrot Fish and How to Feed Them",
    "hero_tag": "Food & Feeding",
    "hero_meta": "\U0001F35A Sinking pellets &nbsp;|&nbsp; \U0001F551 2&times; daily &nbsp;|&nbsp; \U0001F49A 1 fast day weekly",
    "toc_sections": [
        ("what-they-eat", "What They Eat"),
        ("best-food", "Best Foods"),
        ("color", "Feeding for Colour"),
        ("how-much", "How Much & How Often"),
        ("fussy", "Fish That Won't Eat"),
        ("avoid", "What Not to Feed"),
    ],
    "body": FOOD_BODY,
    "faqs": [
        ("What do blood parrot fish eat?",
         "Blood parrot fish are omnivores that eat small sinking cichlid pellets as a staple, plus frozen bloodworms, brine shrimp and mysis for protein, and blanched peas, spirulina and zucchini for plant matter. Food must sink and be small enough for their deformed mouth."),
        ("What is the best food for parrot fish colour?",
         "A sinking cichlid pellet listing astaxanthin, spirulina, krill or shrimp meal near the top of the ingredients, supplemented with frozen krill and brine shrimp. Blood parrots cannot make carotenoids themselves, so orange colour depends directly on diet."),
        ("How often should I feed my blood parrot fish?",
         "Twice a day for adults, giving only what they finish in about two minutes, and two to three smaller meals a day for juveniles under 3 inches. Include one fasting day per week to prevent constipation and buoyancy problems."),
        ("Why won't my blood parrot fish eat?",
         "Most often the fish is newly added and still settling, the water is too cold, ammonia or nitrite is above zero, or a tank mate is chasing it off the food. Check temperature and water parameters first, then tempt it with frozen bloodworms near its cave."),
        ("Can parrot fish eat flake food?",
         "They can eat spirulina flake as a supplement, but flake is a poor staple. It floats, which encourages air gulping, and most flakes lack the carotenoid content blood parrots need to keep their orange colour."),
        ("Can blood parrot fish eat goldfish?",
         "Feeder goldfish should not be used. They carry parasites and disease, contain thiaminase that interferes with vitamin B1 absorption, and blood parrots are poor hunters that rarely catch them anyway."),
    ],
    "related": [
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
        ("/guides/parrot-fish-care/size-growth/", "Parrot Fish Size & Growth"),
        ("/guides/parrot-fish-care/water-parameters/", "Water & Temperature"),
        ("/tools/fish-feeding-calculator/", "Fish Feeding Calculator"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Tank Mates
# ════════════════════════════════════════════════════════════════
MATES_BODY = """    <p>Blood parrot cichlids sit in an awkward spot: too territorial for a nano community, too timid and too poorly built to hold their own against real cichlid aggression, and big enough to swallow anything under two inches. Good blood parrot fish tank mates are <strong>calm, similar-sized fish that neither bully nor nip</strong>. This page lists what works, what does not, and settles the two questions everyone asks &mdash; oscars and other cichlids.</p>

    <h2 id="temperament">Understanding Parrot Fish Temperament</h2>
    <p>A blood parrot will claim a cave, flare at intruders and defend a corner of the tank, especially while spawning. It will also be the fish hiding behind the filter when a Jack Dempsey moves in. The deformed mouth means it cannot lock jaws or deliver a real bite, so its aggression is mostly display &mdash; and its defence is mostly running away.</p>
    <p>The practical consequence: pick tank mates by <strong>behaviour, not just size</strong>. A 4-inch convict cichlid is far more dangerous to a blood parrot than a 6-inch silver dollar.</p>

    <h2 id="good">Best Blood Parrot Fish Tank Mates</h2>
    <table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Why it works</th></tr>
      <tr><td>Severum</td><td>8 in</td><td>Similar size, similar temperament, same water</td></tr>
      <tr><td>Silver dollar</td><td>6 in</td><td>Peaceful shoaler, too big to eat, occupies mid-water</td></tr>
      <tr><td>Congo tetra</td><td>3 in</td><td>Large enough to be safe, adds movement</td></tr>
      <tr><td>Giant danio</td><td>4 in</td><td>Fast dither fish that draws shy parrots out</td></tr>
      <tr><td>Bristlenose pleco</td><td>5 in</td><td>Bottom cleaner, armoured, minds its own business</td></tr>
      <tr><td>Corydoras (larger species)</td><td>2&ndash;3 in</td><td>Bottom dwellers the parrot ignores; keep 6+</td></tr>
      <tr><td>Rainbowfish</td><td>4 in</td><td>Active, peaceful, colourful mid-water fish</td></tr>
      <tr><td>Keyhole cichlid</td><td>4 in</td><td>One of the few genuinely peaceful cichlids</td></tr>
      <tr><td>Firemouth cichlid</td><td>6 in</td><td>Mostly bluff; workable in 75 gallons or more</td></tr>
      <tr><td>Clown loach</td><td>8&ndash;12 in</td><td>Peaceful and robust, but needs a big tank and a group</td></tr>
      <tr><td>Other blood parrots</td><td>8 in</td><td>The safest choice &mdash; matched pace and temperament</td></tr>
    </table>
    <div class="callout callout-ok"><strong>Dither fish work.</strong> A shoal of giant danios or silver dollars swimming calmly in open water signals "no predators here" and pulls a hiding blood parrot out of its cave faster than anything else you can do.</div>

    <h2 id="avoid">Fish to Avoid</h2>
    <table class="ptbl">
      <tr><th>Avoid</th><th>Reason</th></tr>
      <tr><td>Neon tetras, guppies, endlers</td><td>Small enough to be eaten, even by a bad hunter</td></tr>
      <tr><td>Tiger barbs, serpae tetras</td><td>Fin nippers; a slow parrot fish cannot escape them</td></tr>
      <tr><td>Red devil, jaguar, Midas cichlid</td><td>Genuinely aggressive; will injure or kill a parrot fish</td></tr>
      <tr><td>Jack Dempsey, green terror</td><td>Out-fight blood parrots and dominate the food</td></tr>
      <tr><td>Convict cichlid</td><td>Small but relentlessly aggressive, especially when breeding</td></tr>
      <tr><td>Flowerhorn</td><td>Highly aggressive; keep single-species</td></tr>
      <tr><td>African cichlids (mbuna)</td><td>Wrong water chemistry and far too aggressive</td></tr>
      <tr><td>Common pleco</td><td>Grows to 18 in and rasps at slime coats at night</td></tr>
      <tr><td>Goldfish</td><td>Cold-water fish; incompatible temperature needs</td></tr>
      <tr><td>Shrimp and small snails</td><td>Treated as food</td></tr>
    </table>

    <h2 id="oscar">Parrot Fish and Oscar: Can They Live Together?</h2>
    <p>This is the most-asked blood parrot compatibility question, and the honest answer is <strong>sometimes, in a big enough tank, with a close eye on feeding</strong>.</p>
    <p>The case for it: oscars and blood parrots want the same temperature and pH, and plenty of keepers run the combination successfully for years. The case against it:</p>
    <ul>
      <li>An oscar reaches 12&ndash;14 inches against the parrot's 8, and grows faster.</li>
      <li>Oscars are aggressive feeders with a normal mouth. A blood parrot with a slit mouth loses every race to the food and can slowly starve in plain sight.</li>
      <li>Oscars are boisterous. A timid parrot fish that hides permanently is not a fish that is coping.</li>
    </ul>
    <p><strong>Minimum requirements if you try it:</strong> 125 gallons or more, both fish introduced young at similar sizes, multiple caves and sightline breaks, and target-feeding the parrot fish at the opposite end of the tank. Below 100 gallons, do not. See our <a href="/tools/fish-compatibility-checker/">fish compatibility checker</a> and the <a href="/guides/oscar-fish-care/">oscar fish care guide</a>.</p>

    <h2 id="cichlids">Parrot Fish and Other Cichlids</h2>
    <p>Blood parrots are South and Central American in origin, so pair them with New World cichlids that share their water preferences and stay calm:</p>
    <ul>
      <li><strong>Reliable:</strong> severum, keyhole cichlid, other blood parrots, electric blue acara (in a large tank).</li>
      <li><strong>Workable with space:</strong> firemouth, angelfish (watch the fins), rainbow cichlid, geophagus species in 100 gallons plus.</li>
      <li><strong>Not recommended:</strong> convict, Jack Dempsey, green terror, red devil, jaguar, flowerhorn, all African mbuna.</li>
    </ul>
    <p>African cichlids are the mistake to avoid outright &mdash; they need harder, more alkaline water, and mbuna aggression is far more than a blood parrot can absorb.</p>

    <h2 id="introducing">How to Introduce New Tank Mates</h2>
    <ol>
      <li><strong>Quarantine for 2&ndash;4 weeks</strong> in a separate tank. Every disease that reaches an established tank arrives on a new fish.</li>
      <li><strong>Rearrange the decor</strong> before adding anyone. Breaking up existing territories resets the aggression map.</li>
      <li><strong>Add at lights-out</strong> so the new fish gets a night to find hiding spots before it is noticed.</li>
      <li><strong>Add in groups</strong> where the species is a shoaler, so aggression is spread rather than focused on one fish.</li>
      <li><strong>Watch feeding time for a week.</strong> Chasing at the food bowl is the earliest reliable sign a pairing will not work.</li>
      <li><strong>Have a plan B</strong> &mdash; a spare tank or a divider &mdash; before you introduce anything semi-aggressive.</li>
    </ol>
"""

MATES = {
    "slug": "tank-mates",
    "title": "Blood Parrot Fish Tank Mates: Best & Worst Companions",
    "meta_desc": "Blood parrot cichlid tank mates that work: severums, silver dollars, plecos and giant danios. Fish to avoid, plus whether parrot fish and oscars can share a tank.",
    "h1": "Blood Parrot Fish Tank Mates",
    "hero_tag": "Tank Mates",
    "hero_meta": "\U0001F420 Calm, similar-sized fish &nbsp;|&nbsp; \U0001F6AB No nippers or bullies &nbsp;|&nbsp; \U0001F5C3️ 75 gal+ for a community",
    "toc_sections": [
        ("temperament", "Parrot Fish Temperament"),
        ("good", "Best Tank Mates"),
        ("avoid", "Fish to Avoid"),
        ("oscar", "Parrot Fish and Oscar"),
        ("cichlids", "Parrot Fish and Cichlids"),
        ("introducing", "Introducing New Fish"),
    ],
    "body": MATES_BODY,
    "faqs": [
        ("What are the best tank mates for blood parrot cichlids?",
         "Severums, silver dollars, Congo tetras, giant danios, bristlenose plecos, larger corydoras, rainbowfish and other blood parrots. The rule is calm fish of similar size that will neither bully a timid parrot fish nor fit in its mouth."),
        ("Can blood parrot fish live with oscars?",
         "It can work in 125 gallons or more with both fish raised together from a young age, but it is risky. Oscars reach 12-14 inches, grow faster and outcompete a blood parrot at feeding time because the parrot's deformed mouth makes it a slow eater."),
        ("Are blood parrot fish aggressive to other fish?",
         "They are semi-aggressive but mostly bluff. A blood parrot will defend a cave and chase intruders, especially when spawning, but its deformed mouth cannot deliver a serious bite and it is more often the victim than the aggressor."),
        ("Can parrot fish live with African cichlids?",
         "No. African mbuna need harder, more alkaline water than blood parrots prefer, and their aggression level is far beyond what a slow, poorly armed hybrid can cope with."),
        ("Can I keep just one blood parrot fish?",
         "Yes. Blood parrots do not need a group and a single fish in a 30-gallon tank does fine, often becoming noticeably interactive with its owner. They also do well in pairs or groups given enough space and caves."),
        ("Will blood parrot fish eat neon tetras?",
         "Yes, eventually. Anything under about two inches is a potential meal. Keep tank mates at three inches or larger, or expect to lose small fish one at a time."),
    ],
    "related": [
        ("/tools/fish-compatibility-checker/", "Fish Compatibility Checker"),
        ("/guides/parrot-fish-care/tank-size/", "Parrot Fish Tank Size"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Size & Growth
# ════════════════════════════════════════════════════════════════
SIZE_BODY = """    <p>Blood parrot cichlids are sold at 1&ndash;2 inches and end up as fish the size of a grapefruit. Knowing how big parrot fish get &mdash; and how fast &mdash; is the difference between buying the right tank once and rehoming a stunted fish in two years. This page covers blood parrot fish size, the growth timeline, and what makes one fish reach 8 inches while another stalls at 4.</p>

    <h2 id="how-big">How Big Do Parrot Fish Get?</h2>
    <p>Adult blood parrot cichlids reach <strong>7&ndash;8 inches (18&ndash;20 cm)</strong> in length. Exceptional individuals in large tanks reach 10 inches, and king kong parrot variants can exceed that. Because the body is deep and rounded rather than streamlined, an 8-inch blood parrot looks and stocks like a much larger fish &mdash; the body depth is often 5&ndash;6 inches.</p>
    <table class="ptbl">
      <tr><th>Variety</th><th>Typical adult size</th></tr>
      <tr><td>Standard blood parrot</td><td>7&ndash;8 in (18&ndash;20 cm)</td></tr>
      <tr><td>Large / well-grown specimens</td><td>Up to 10 in (25 cm)</td></tr>
      <tr><td>King kong parrot</td><td>10&ndash;12 in (25&ndash;30 cm)</td></tr>
      <tr><td>Short-body / balloon parrot</td><td>4&ndash;6 in (10&ndash;15 cm)</td></tr>
      <tr><td>Marine parrotfish (for comparison)</td><td>1&ndash;4 ft depending on species</td></tr>
    </table>
    <p>Note the last row: if you arrived here after reading that parrot fish grow to four feet, that is the <strong>marine parrotfish</strong> of coral reefs, a completely different animal. See <a href="/guides/parrot-fish-care/types/">types of parrot fish</a>.</p>

    <h2 id="growth-rate">Growth Rate Timeline</h2>
    <p>Blood parrots grow quickly for the first year, slow through the second, and are essentially finished by year three.</p>
    <table class="ptbl">
      <tr><th>Age</th><th>Typical size</th><th>Stage</th></tr>
      <tr><td>Hatch to 2 months</td><td>0.5&ndash;1 in</td><td>Fry; drab brown-grey</td></tr>
      <tr><td>3&ndash;6 months</td><td>1.5&ndash;3 in</td><td>Sale size; colour starts turning orange</td></tr>
      <tr><td>6&ndash;12 months</td><td>3&ndash;5 in</td><td>Fastest growth phase; needs full-size tank</td></tr>
      <tr><td>1&ndash;2 years</td><td>5&ndash;7 in</td><td>Body deepens; adult shape appears</td></tr>
      <tr><td>2&ndash;3 years</td><td>7&ndash;8 in</td><td>Adult size reached; growth mostly stops</td></tr>
      <tr><td>3+ years</td><td>8 in+</td><td>Marginal gains only</td></tr>
    </table>
    <p>A rough working figure is <strong>about an inch every two months through the first year</strong>, tapering sharply afterwards. A fish that has not grown at all in six months during year one has a husbandry problem, not a genetic one.</p>

    <h2 id="factors">What Controls Final Size</h2>
    <ul>
      <li><strong>Tank size.</strong> The strongest single factor. A blood parrot in a 20-gallon tank will not reach 8 inches, and the shortfall is not cosmetic &mdash; stunted cichlids have internal organs that keep growing against a body that does not.</li>
      <li><strong>Water quality.</strong> Chronic nitrate above 40 ppm suppresses growth hormone response. Weekly water changes do more for size than any food.</li>
      <li><strong>Diet.</strong> Protein-adequate sinking pellets plus frozen foods through the first year. Underfeeding during months 6&ndash;12 costs size permanently.</li>
      <li><strong>Temperature.</strong> Growth is metabolic. At 76&deg;F fish grow noticeably slower than at 80&ndash;82&deg;F.</li>
      <li><strong>Competition.</strong> A parrot fish outcompeted for food by an oscar or a severum grows slowly no matter what you put in the tank.</li>
      <li><strong>Genetics.</strong> Hybrid stock is variable. Some lines simply top out smaller, and short-body variants are bred to.</li>
    </ul>
    <div class="callout callout-warn"><strong>Stunting is not "keeping it small".</strong> The idea that a fish grows to the size of its tank is a myth in the form it is usually told. Blood parrots in undersized tanks show suppressed external growth with continued internal growth, spinal curvature and dramatically shortened lifespan. Size the tank for the adult from the start &mdash; see <a href="/guides/parrot-fish-care/tank-size/">parrot fish tank size</a>.</div>

    <h2 id="body-shape">Why the Body Shape Matters for Stocking</h2>
    <p>Standard stocking rules built around slim community fish underestimate blood parrots badly. An 8-inch parrot fish has roughly the body mass of a 12-inch slim-bodied fish and eats accordingly, which is why the tank guidance is 30 gallons for one fish rather than the 20 an "inch per gallon" rule would suggest. Plug your numbers into the <a href="/tools/tank-size-calculator/">tank size calculator</a> rather than counting inches.</p>

    <h2 id="growing-out">Growing Out a Healthy Parrot Fish</h2>
    <ol>
      <li><strong>Full-size tank by six months.</strong> Grow-out in something smaller is fine only for the first few months.</li>
      <li><strong>Feed 2&ndash;3 small meals daily through year one</strong>, dropping to twice daily after that. See the <a href="/guides/parrot-fish-care/food/">feeding guide</a>.</li>
      <li><strong>Hold temperature at 80&ndash;82&deg;F</strong> during the growth phase.</li>
      <li><strong>Change 25&ndash;30% weekly</strong> without exception; nitrate is the invisible brake on growth.</li>
      <li><strong>Keep competition mild</strong> so the slow-mouthed parrot actually gets its share.</li>
      <li><strong>Measure every few months</strong> against the timeline above so a problem shows up early.</li>
    </ol>
"""

SIZE = {
    "slug": "size-growth",
    "title": "How Big Do Parrot Fish Get? Blood Parrot Size & Growth Rate",
    "meta_desc": "Blood parrot fish size explained: adults reach 7-8 inches, up to 10. Growth rate timeline by age, what limits final size and how to grow out a healthy fish.",
    "h1": "How Big Do Parrot Fish Get? Size and Growth",
    "hero_tag": "Size & Growth",
    "hero_meta": "\U0001F4CF 7&ndash;8 in adult &nbsp;|&nbsp; \U0001F4C8 ~1 in per 2 months (year 1) &nbsp;|&nbsp; \U0001F3C1 Full size by year 3",
    "toc_sections": [
        ("how-big", "How Big They Get"),
        ("growth-rate", "Growth Timeline"),
        ("factors", "What Controls Size"),
        ("body-shape", "Body Shape & Stocking"),
        ("growing-out", "Growing Out"),
    ],
    "body": SIZE_BODY,
    "faqs": [
        ("How big do blood parrot fish get?",
         "Blood parrot cichlids reach 7-8 inches (18-20 cm) as adults, with exceptional fish reaching 10 inches. King kong parrot variants can reach 10-12 inches, while short-body or balloon parrots stay at 4-6 inches."),
        ("How fast do blood parrot fish grow?",
         "Roughly one inch every two months through the first year, reaching 3-5 inches by 12 months and 5-7 inches by two years. Growth slows sharply after year two and is essentially finished by year three."),
        ("Do parrot fish only grow to the size of their tank?",
         "No. A blood parrot in an undersized tank shows suppressed external growth while its internal organs keep developing, which causes spinal problems and a much shorter life. Size the tank for an 8-inch adult from the start."),
        ("Why is my blood parrot fish not growing?",
         "The usual causes are a tank that is too small, nitrate above 40 ppm, underfeeding during the first year, water below 78 degrees Fahrenheit, or a tank mate outcompeting it at feeding time."),
        ("How big is a parrot fish in the ocean?",
         "Marine parrotfish, a different animal entirely, range from about 1 foot for princess parrotfish to over 4 feet for the bumphead parrotfish. They are reef grazers and not suitable for home aquariums."),
    ],
    "related": [
        ("/guides/parrot-fish-care/tank-size/", "Parrot Fish Tank Size"),
        ("/guides/parrot-fish-care/lifespan/", "Parrot Fish Lifespan"),
        ("/guides/parrot-fish-care/food/", "Best Food for Parrot Fish"),
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Lifespan
# ════════════════════════════════════════════════════════════════
LIFESPAN_BODY = """    <p>Blood parrot cichlids are long-lived fish that are frequently killed young. The species is capable of 10&ndash;15 years and sometimes 20, yet a large share die at three to five &mdash; almost always for reasons the owner could have changed. This page covers how long parrot fish live, what shortens the number, and the ageing signs worth knowing.</p>

    <h2 id="how-long">How Long Do Parrot Fish Live?</h2>
    <p>A well-kept blood parrot fish lives <strong>10&ndash;15 years</strong>, with 20 years documented in exceptional cases. That puts them alongside oscars and other medium Central American cichlids, and well ahead of most community fish.</p>
    <table class="ptbl">
      <tr><th>Conditions</th><th>Typical lifespan</th></tr>
      <tr><td>Dyed fish ("jellybean", "blueberry")</td><td>Months to 2 years</td></tr>
      <tr><td>Small tank, flake-only diet, irregular water changes</td><td>3&ndash;5 years</td></tr>
      <tr><td>Adequate tank, mixed diet, weekly changes</td><td>8&ndash;12 years</td></tr>
      <tr><td>Large tank, varied diet, stable warm water</td><td>10&ndash;15 years</td></tr>
      <tr><td>Best recorded</td><td>Around 20 years</td></tr>
    </table>
    <p>If you are comparing with the ocean species: marine parrotfish live around 5&ndash;7 years for the smaller species, and up to about 40 years for the bumphead parrotfish. They are a different family entirely &mdash; see <a href="/guides/parrot-fish-care/types/">types of parrot fish</a>.</p>

    <h2 id="what-shortens">What Shortens a Parrot Fish's Life</h2>
    <ul>
      <li><strong>An undersized tank.</strong> The most common cause. Stunting brings organ crowding, spinal deformity and chronic stress; fish rarely pass five years.</li>
      <li><strong>Chronic nitrate.</strong> Nitrate above 40 ppm week after week is a slow poison. It has no dramatic symptom, which is exactly why it kills so many fish.</li>
      <li><strong>Cold water.</strong> Long-term keeping below 76&deg;F suppresses immunity and invites repeat ich and bacterial infections.</li>
      <li><strong>A poor diet.</strong> Flake-only or cheap filler-heavy pellets produce fading colour, HLLE and fatty liver disease.</li>
      <li><strong>Persistent bullying.</strong> A fish that hides all day is a fish with permanently elevated stress hormones and a suppressed immune system.</li>
      <li><strong>Dyeing.</strong> Injected and dipped colour destroys the slime coat and a large share of dyed fish die within a year of sale.</li>
      <li><strong>Overfeeding.</strong> Buoyancy problems, constipation and fatty deposits, all avoidable with a weekly fast day.</li>
    </ul>
    <div class="callout callout-ok"><strong>The five things that add years:</strong> a tank of 30+ gallons per fish, weekly 25&ndash;30% water changes, a stable 80&deg;F, a varied sinking diet with one fast day a week, and tank mates that leave the fish alone. Nothing exotic is required.</div>

    <h2 id="life-stages">Life Stages</h2>
    <table class="ptbl">
      <tr><th>Stage</th><th>Age</th><th>What to expect</th></tr>
      <tr><td>Juvenile</td><td>0&ndash;12 months</td><td>Fast growth, colour change from grey-brown to orange, timid</td></tr>
      <tr><td>Young adult</td><td>1&ndash;3 years</td><td>Adult size and colour, territorial behaviour, possible spawning</td></tr>
      <tr><td>Mature adult</td><td>3&ndash;8 years</td><td>Stable size, peak colour, most interactive with owners</td></tr>
      <tr><td>Senior</td><td>8&ndash;15 years</td><td>Slower, colour may soften, less inclined to spawn</td></tr>
    </table>

    <h2 id="ageing">Signs of an Ageing Parrot Fish</h2>
    <p>Old blood parrots slow down rather than fall apart. Expect gradually reduced activity, a slightly softer or paler orange, less interest in defending territory, a slower approach to food, and occasional cloudiness in the eyes. These arrive over months. Anything that appears in <strong>days</strong> &mdash; sudden fading, clamped fins, gasping, tilting &mdash; is illness or water quality, not age. Start with a water test and the <a href="/aquarium-fish-diseases/blood-parrot-cichlid-diseases/">blood parrot disease guide</a>.</p>

    <h2 id="maximise">A Longevity Checklist</h2>
    <ol>
      <li>Buy undyed stock from a tank with no visible dead or gasping fish.</li>
      <li>Quarantine new arrivals for 2&ndash;4 weeks before they meet your other fish.</li>
      <li>Keep 30 gallons per adult parrot fish, more if you can.</li>
      <li>Hold 80&deg;F with a reliable heater and an independent thermometer.</li>
      <li>Change 25&ndash;30% of the water weekly and keep nitrate under 30 ppm.</li>
      <li>Feed a varied sinking diet twice daily with a weekly fast day.</li>
      <li>Test the water monthly even when nothing looks wrong.</li>
      <li>Fix aggression early &mdash; rehome the aggressor rather than hoping it settles.</li>
    </ol>
"""

LIFESPAN = {
    "slug": "lifespan",
    "title": "How Long Do Parrot Fish Live? Blood Parrot Lifespan Explained",
    "meta_desc": "Blood parrot fish lifespan is 10-15 years and up to 20 in good conditions. What shortens it, life stages by age, signs of ageing and a longevity checklist.",
    "h1": "Parrot Fish Lifespan: How Long Do They Live?",
    "hero_tag": "Lifespan",
    "hero_meta": "⏳ 10&ndash;15 years typical &nbsp;|&nbsp; \U0001F3C6 20 years possible &nbsp;|&nbsp; ⚠️ 3&ndash;5 years if kept poorly",
    "toc_sections": [
        ("how-long", "How Long They Live"),
        ("what-shortens", "What Shortens Life"),
        ("life-stages", "Life Stages"),
        ("ageing", "Signs of Ageing"),
        ("maximise", "Longevity Checklist"),
    ],
    "body": LIFESPAN_BODY,
    "faqs": [
        ("How long do blood parrot fish live?",
         "Blood parrot cichlids live 10-15 years in good conditions, and around 20 years in exceptional cases. Fish kept in small tanks with irregular water changes and a flake-only diet commonly die at 3-5 years."),
        ("Why did my blood parrot fish die so young?",
         "The most common causes are an undersized tank, chronic nitrate above 40 ppm, water kept below 76 degrees Fahrenheit, a poor diet, persistent bullying by tank mates, or the fish having been artificially dyed before sale."),
        ("How long do dyed jellybean parrot fish live?",
         "Dyed parrot fish often survive only months to about two years. The dyeing process damages the slime coat and immune defences, and mortality in the weeks after treatment is high before the fish even reaches a shop."),
        ("How can I tell how old my parrot fish is?",
         "Size is the best guide. Under 3 inches is roughly under six months, 3-5 inches is around a year, 5-7 inches is one to two years, and a full 7-8 inch adult is at least two to three years old."),
        ("How long do parrot fish live in the ocean?",
         "Marine parrotfish, an unrelated reef family, live about 5-7 years for smaller species and up to roughly 40 years for the bumphead parrotfish. This has no bearing on aquarium blood parrot cichlids."),
    ],
    "related": [
        ("/guides/parrot-fish-care/size-growth/", "Parrot Fish Size & Growth"),
        ("/aquarium-fish-diseases/blood-parrot-cichlid-diseases/", "Blood Parrot Diseases"),
        ("/guides/parrot-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Types & Colors
# ════════════════════════════════════════════════════════════════
TYPES_BODY = """    <p>"Types of parrot fish" covers two unrelated groups of animals. In the aquarium trade it means the <strong>hybrid varieties of the blood parrot cichlid</strong> &mdash; king kong, red mammon, short-body, heart parrot. On a coral reef it means the <strong>marine parrotfish family (Scaridae)</strong>, which is where the blue, green and rainbow parrot fish photos come from. This page covers both, and explains which colours are real and which are dye.</p>

    <h2 id="aquarium-types">Types of Blood Parrot Cichlid</h2>
    <table class="ptbl">
      <tr><th>Variety</th><th>Description</th><th>Adult size</th></tr>
      <tr><td>Standard blood parrot</td><td>The common orange fish; round body, beak-like mouth</td><td>7&ndash;8 in</td></tr>
      <tr><td>King kong parrot</td><td>Bigger, blockier, often deeper red; premium priced</td><td>10&ndash;12 in</td></tr>
      <tr><td>Red mammon</td><td>King kong line selected for solid deep red colour</td><td>10&ndash;12 in</td></tr>
      <tr><td>Short-body / balloon parrot</td><td>Further-shortened spine; compact and slower-swimming</td><td>4&ndash;6 in</td></tr>
      <tr><td>Heart parrot / love heart</td><td>Tail cut so the body reads as a heart shape &mdash; a cosmetic mutilation, not a variety</td><td>6&ndash;8 in</td></tr>
      <tr><td>Polar blue parrot</td><td>A separate convict-cichlid hybrid, white-blue with dark bars</td><td>3&ndash;4 in</td></tr>
      <tr><td>Purple / jellybean / blueberry</td><td>Artificially dyed fish, not a genetic variety</td><td>Varies</td></tr>
    </table>
    <p>All of these share the same care requirements as the standard fish &mdash; see the <a href="/guides/parrot-fish-care/">parrot fish care guide</a>. Short-body variants swim even worse than standard blood parrots, so keep flow gentle and tank mates calm.</p>

    <h2 id="colors">Parrot Fish Colors: What's Real</h2>
    <p>Naturally occurring blood parrot colours are <strong>orange, red, yellow, and occasionally a calico or marbled mix</strong>. Juveniles hatch brown-grey and shift to orange at around 5&ndash;6 months. Colour intensity is diet-driven, because the fish cannot manufacture carotenoids &mdash; see <a href="/guides/parrot-fish-care/food/">feeding for colour</a>.</p>
    <table class="ptbl">
      <tr><th>Colour</th><th>Real?</th><th>Notes</th></tr>
      <tr><td>Orange</td><td>&#9989; Natural</td><td>The standard blood parrot colour</td></tr>
      <tr><td>Red</td><td>&#9989; Natural</td><td>Selectively bred; deepest in king kong lines</td></tr>
      <tr><td>Yellow</td><td>&#9989; Natural</td><td>Less common; sometimes a juvenile or diet effect</td></tr>
      <tr><td>Calico / marbled</td><td>&#9989; Natural</td><td>Orange with black or white patches</td></tr>
      <tr><td>Grey / brown</td><td>&#9989; Natural</td><td>Juvenile colour, or a faded stressed adult</td></tr>
      <tr><td>Blue, purple, pink, green</td><td>&#10060; Dyed</td><td>Injected or dipped; painful and life-shortening</td></tr>
    </table>
    <div class="callout callout-warn"><strong>How to spot a dyed parrot fish.</strong> The colour looks painted rather than graded, often with pale patches around the mouth and the fin bases where dye did not take. Sale names to avoid: jellybean, blueberry, grape, bubblegum, strawberry parrot. Dyed fish frequently arrive with damaged slime coats and secondary infections, and the practice continues only because the fish sell.</div>

    <h2 id="marine">Marine Parrotfish (Scaridae)</h2>
    <p>The reef parrotfish is a real, wild family of about 95 species. They are named for a <strong>beak</strong> formed by fused teeth, which they use to scrape algae off coral rock. In the process they grind up calcium carbonate and excrete it as sand &mdash; a large parrotfish can produce hundreds of pounds of white sand a year, and a substantial share of tropical beach sand comes from them.</p>
    <p>Two features explain why parrotfish colours are so confusing:</p>
    <ul>
      <li><strong>They change sex and colour.</strong> Most parrotfish are protogynous hermaphrodites: they begin as drab red-brown females (initial phase) and some later become vivid blue-green males (terminal phase). The "blue parrot fish" and the "red parrot fish" in reef photos are often the same species at different life stages.</li>
      <li><strong>They sleep in mucus cocoons.</strong> Many species secrete a mucus envelope at night that masks their scent from predators and parasites.</li>
    </ul>
    <table class="ptbl">
      <tr><th>Species</th><th>Common name</th><th>Adult size</th></tr>
      <tr><td><em>Scarus coeruleus</em></td><td>Blue parrotfish</td><td>Up to 4 ft</td></tr>
      <tr><td><em>Scarus guacamaia</em></td><td>Rainbow parrotfish</td><td>Up to 4 ft; largest Atlantic herbivorous fish</td></tr>
      <tr><td><em>Sparisoma viride</em></td><td>Stoplight parrotfish</td><td>Up to 2 ft</td></tr>
      <tr><td><em>Scarus taeniopterus</em></td><td>Princess parrotfish</td><td>Up to 14 in</td></tr>
      <tr><td><em>Scarus vetula</em></td><td>Queen parrotfish</td><td>Up to 2 ft</td></tr>
      <tr><td><em>Bolbometopon muricatum</em></td><td>Bumphead parrotfish</td><td>Up to 4.3 ft, 100 lb</td></tr>
      <tr><td><em>Chlorurus</em> species</td><td>Green parrotfish (various)</td><td>1&ndash;2 ft</td></tr>
    </table>
    <div class="callout"><strong>Can you keep marine parrotfish in an aquarium?</strong> Realistically, no. They reach 1&ndash;4 feet, graze continuously on live rock, and need enormous systems &mdash; they are public-aquarium animals. Several species are also protected or fishery-restricted because of their role in reef health. If you want a reef-safe fish with similar colour, look at tangs or wrasses instead: see the <a href="/guides/blue-tang-care-guide/">blue tang</a> and <a href="/guides/yellow-tang-care-guide/">yellow tang</a> guides.</div>

    <h2 id="blue-green">"Blue Parrot Fish" and "Green Parrot Fish"</h2>
    <p>If you searched for a blue or green parrot fish, one of three things is true:</p>
    <ol>
      <li>You are looking at a <strong>marine parrotfish</strong> &mdash; a wild reef species, not an aquarium fish.</li>
      <li>You are looking at a <strong>dyed blood parrot</strong> &mdash; do not buy it.</li>
      <li>You are looking at a <strong>polar blue parrot cichlid</strong>, a separate convict hybrid that is genuinely white-blue but is a different, smaller fish with a normal mouth.</li>
    </ol>
    <p>There is no naturally blue or green blood parrot cichlid, and no amount of feeding will produce one.</p>

    <h2 id="choosing">Choosing a Healthy Parrot Fish</h2>
    <ul>
      <li>Even, graded colour &mdash; not blotchy paint-like colour with pale mouth and fin bases.</li>
      <li>Both eyes clear and equal; no cloudiness or bulging.</li>
      <li>Fins intact and held open, not clamped against the body.</li>
      <li>Active and reacting to movement, not sitting on the bottom breathing hard.</li>
      <li>No white spots, cotton-like patches, red streaks or open sores.</li>
      <li>A shop tank with no dead or gasping fish in it.</li>
      <li>An intact tail &mdash; a "heart" shape means the tail was cut.</li>
    </ul>
"""

TYPES = {
    "slug": "types",
    "title": "Types of Parrot Fish & Colors: Blood Parrot vs Marine Parrotfish",
    "meta_desc": "Types of parrot fish explained: blood parrot cichlid varieties, real colours vs dyed jellybean fish, and the blue, green and rainbow marine parrotfish species.",
    "h1": "Types of Parrot Fish and Their Colors",
    "hero_tag": "Types & Colors",
    "hero_meta": "\U0001F3A8 Orange, red, yellow are natural &nbsp;|&nbsp; \U0001F6AB Blue &amp; purple are dyed &nbsp;|&nbsp; \U0001F30A 95 marine species",
    "toc_sections": [
        ("aquarium-types", "Blood Parrot Varieties"),
        ("colors", "Real vs Dyed Colours"),
        ("marine", "Marine Parrotfish"),
        ("blue-green", "Blue & Green Parrot Fish"),
        ("choosing", "Choosing a Healthy Fish"),
    ],
    "body": TYPES_BODY,
    "faqs": [
        ("What are the different types of parrot fish?",
         "In aquariums: standard blood parrot, king kong parrot, red mammon, short-body or balloon parrot, heart parrot, and the separate polar blue parrot cichlid. On coral reefs: about 95 marine parrotfish species including blue, rainbow, stoplight, queen and bumphead parrotfish."),
        ("Are blue parrot fish real?",
         "The blue parrotfish (Scarus coeruleus) is a real marine reef species that reaches four feet. A blue or purple blood parrot cichlid in an aquarium shop is artificially dyed, not a natural colour variety."),
        ("What colours do blood parrot fish come in?",
         "Naturally orange, red, yellow, and sometimes calico or marbled. Juveniles start brown-grey and turn orange at around five to six months. Blue, purple, pink and green fish are dyed."),
        ("Are jellybean parrot fish dyed?",
         "Yes. Jellybean, blueberry, grape and similar names are dyed blood parrot cichlids. The dyeing process damages the slime coat and immune system, and many dyed fish die within months."),
        ("Can you keep a marine parrotfish in a home aquarium?",
         "No, realistically. Marine parrotfish reach one to four feet, graze continuously on live rock, and require enormous systems. They are public-aquarium animals, and several species are protected because of their role in reef health."),
        ("Why do marine parrotfish change colour?",
         "Most parrotfish are protogynous hermaphrodites. They begin life as drab red-brown females in the initial phase, and some later become vivid blue-green terminal-phase males. The same species can look like two entirely different fish."),
    ],
    "related": [
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
        ("/guides/parrot-fish-care/food/", "Feeding for Colour"),
        ("/wiki/blood-parrot-cichlid/", "Blood Parrot Species Profile"),
        ("/guides/blue-tang-care-guide/", "Blue Tang Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Breeding & Babies
# ════════════════════════════════════════════════════════════════
BREEDING_BODY = """    <p>Blood parrot cichlids pair up, dig pits, lay eggs and guard them like textbook cichlid parents &mdash; and then almost nothing hatches. The reason is hybrid sterility, and understanding it saves a lot of disappointment. This page covers blood parrot fish breeding, why the eggs usually fail, what a viable cross looks like, and how to raise baby blood parrot fish if you do get fry.</p>

    <h2 id="sterility">Why Blood Parrot Breeding Usually Fails</h2>
    <p><strong>Almost all male blood parrots are sterile.</strong> They are hybrids, and hybrid males in this cross generally have non-functional or absent milt-producing tissue. Females are usually fertile and lay perfectly good eggs; there is simply nothing to fertilise them.</p>
    <p>What you see in a home tank is therefore very common: a pair forms, cleans a flat rock or digs a pit, the female lays 200&ndash;400 eggs, both fish fan and guard them &mdash; and within 48&ndash;72 hours the eggs turn opaque white with fungus and the parents eat them. That is unfertilised eggs going off, not bad parenting.</p>
    <div class="callout"><strong>Infertile spawning is still a good sign.</strong> Fish only spawn when they are healthy, well fed and settled in stable water. If your blood parrots are laying eggs, your husbandry is working &mdash; even though nothing will hatch.</div>

    <h2 id="viable">When Fry Are Actually Possible</h2>
    <p>Viable blood parrot fry come from one of three routes, and commercial breeders use all of them:</p>
    <ul>
      <li><strong>Female blood parrot &times; male of a parent-type species</strong> &mdash; a midas, redhead or convict cichlid male. This is the common backcross and it does produce fry, though the young often look less "parrot" than the mother.</li>
      <li><strong>A rare fertile male blood parrot.</strong> A small percentage exist. If a spawn in an all-parrot tank produces fry, you have one.</li>
      <li><strong>Commercial hormone or hand-stripping methods</strong>, used in production hatcheries and not practical or advisable at home.</li>
    </ul>
    <p>Fry from a backcross are legitimate fish, but be clear with anyone you give them to about what they are &mdash; hybrids of hybrids are exactly how the trade produced fish with mouths that do not close.</p>

    <h2 id="sexing">Sexing Blood Parrot Fish</h2>
    <p>Sexing is genuinely difficult and no single feature is reliable. Working indicators:</p>
    <table class="ptbl">
      <tr><th>Feature</th><th>Male</th><th>Female</th></tr>
      <tr><td>Size</td><td>Usually slightly larger</td><td>Usually slightly smaller</td></tr>
      <tr><td>Fin shape</td><td>Dorsal and anal fins more pointed</td><td>Fins more rounded</td></tr>
      <tr><td>Venting (at spawning)</td><td>Narrow, pointed papilla</td><td>Wider, blunter ovipositor</td></tr>
      <tr><td>Behaviour</td><td>More display and territory patrolling</td><td>Cleans and inspects the spawning site</td></tr>
    </table>
    <p>The dependable method is behavioural: whichever fish lays the eggs is female. Venting is only readable in the days around a spawn.</p>

    <h2 id="conditioning">Setting Up for a Spawn</h2>
    <ol>
      <li><strong>Let a pair form naturally.</strong> Grow out 5&ndash;6 juveniles in a 75&ndash;100 gallon tank and let two pick each other &mdash; forced pairings usually end in one fish being beaten.</li>
      <li><strong>Move the pair to their own tank</strong> of 55 gallons or more if you can. Spawning blood parrots become genuinely territorial and will harass tank mates.</li>
      <li><strong>Provide spawning sites:</strong> flat slate, a large smooth rock, or a terracotta pot on its side.</li>
      <li><strong>Raise the temperature to 82&ndash;84&deg;F</strong> and hold pH near 7.0.</li>
      <li><strong>Condition with protein</strong> &mdash; frozen bloodworms, mysis and brine shrimp for two to three weeks. See the <a href="/guides/parrot-fish-care/food/">feeding guide</a>.</li>
      <li><strong>Trigger with a water change</strong> &mdash; a 30% change with slightly cooler water often prompts spawning within days.</li>
    </ol>

    <h2 id="eggs">Eggs and Timeline</h2>
    <table class="ptbl">
      <tr><th>Stage</th><th>Timing</th><th>What you see</th></tr>
      <tr><td>Spawning</td><td>Day 0</td><td>200&ndash;400 amber eggs on a cleaned flat surface</td></tr>
      <tr><td>Fertile eggs</td><td>Day 1&ndash;3</td><td>Stay amber/translucent; parents fan constantly</td></tr>
      <tr><td>Infertile eggs</td><td>Day 1&ndash;3</td><td>Turn opaque white, then fuzzy with fungus</td></tr>
      <tr><td>Hatching</td><td>Day 3&ndash;5</td><td>Wrigglers in a pit, still attached to yolk sacs</td></tr>
      <tr><td>Free swimming</td><td>Day 7&ndash;9</td><td>Fry leave the pit as a cloud around the parents</td></tr>
      <tr><td>First colour</td><td>Month 5&ndash;6</td><td>Grey-brown juveniles begin turning orange</td></tr>
    </table>
    <p>Blood parrots are good parents when they have something to parent &mdash; they fan the eggs, move wrigglers between pits, and herd free-swimming fry. Leaving the fry with the parents is usually fine, and safer than moving eggs to a bare tank.</p>

    <h2 id="fry">Raising Baby Blood Parrot Fish</h2>
    <ul>
      <li><strong>First foods:</strong> newly hatched brine shrimp, microworms or a quality powdered fry food, 3&ndash;4 times a day.</li>
      <li><strong>Water:</strong> small daily changes of 10&ndash;15% with a sponge filter only &mdash; fry get pulled into hang-on and canister intakes.</li>
      <li><strong>Temperature:</strong> hold 82&deg;F for the first few weeks.</li>
      <li><strong>Grading:</strong> separate fast growers from slow ones by week four; blood parrot fry cannibalise size differences.</li>
      <li><strong>Move to crushed pellets</strong> around week six, then small sinking pellets.</li>
      <li><strong>Expect the colour change</strong> at 5&ndash;6 months. Grey-brown fry are normal, not failed fish.</li>
      <li><strong>Cull expectations:</strong> a share of blood parrot fry carry deformities incompatible with life. Decide in advance how you will handle it.</li>
    </ul>
    <p>Growth and size expectations for the juveniles are on the <a href="/guides/parrot-fish-care/size-growth/">size and growth page</a>.</p>
"""

BREEDING = {
    "slug": "breeding",
    "title": "Blood Parrot Fish Breeding: Why Eggs Fail & Raising Babies",
    "meta_desc": "Blood parrot fish breeding explained: male hybrids are sterile so most eggs never hatch. Sexing, spawning setup, egg timeline and how to raise baby blood parrots.",
    "h1": "Blood Parrot Fish Breeding and Baby Parrot Fish",
    "hero_tag": "Breeding & Babies",
    "hero_meta": "\U0001F95A 200&ndash;400 eggs &nbsp;|&nbsp; ♂️ Males usually sterile &nbsp;|&nbsp; \U0001F321️ 82&ndash;84&deg;F to spawn",
    "toc_sections": [
        ("sterility", "Why Breeding Fails"),
        ("viable", "When Fry Are Possible"),
        ("sexing", "Sexing Parrot Fish"),
        ("conditioning", "Setting Up a Spawn"),
        ("eggs", "Eggs & Timeline"),
        ("fry", "Raising Baby Parrots"),
    ],
    "body": BREEDING_BODY,
    "faqs": [
        ("Can blood parrot fish breed?",
         "Females are fertile and lay 200-400 eggs, but almost all male blood parrots are sterile because they are hybrids. Pairs spawn and guard the eggs normally, then the unfertilised eggs turn white and fungus over within two to three days."),
        ("Why are my blood parrot eggs turning white?",
         "White, opaque eggs are unfertilised. This is the normal outcome in an all-blood-parrot tank because the males are sterile. Fertile eggs stay amber and translucent and hatch in three to five days."),
        ("How do you get baby blood parrot fish?",
         "The reliable route is crossing a female blood parrot with a male of a parent-type species such as a midas, redhead or convict cichlid. A small percentage of male blood parrots are fertile, so an all-parrot spawn occasionally produces fry."),
        ("How can you tell if a blood parrot fish is male or female?",
         "There is no reliable external test. Males tend to be slightly larger with more pointed dorsal and anal fins; females are rounder-finned and show a wider ovipositor at spawning time. In practice, the fish that lays the eggs is the female."),
        ("What do baby blood parrot fish look like?",
         "Fry and juveniles are grey-brown with no orange at all. The colour change happens at around five to six months, so a drab juvenile is normal rather than a sign of poor health."),
        ("How many eggs do blood parrot fish lay?",
         "A spawn is typically 200-400 eggs laid on a cleaned flat rock, slate or the floor of a pit the pair digs. Both parents fan and guard them."),
    ],
    "related": [
        ("/guides/parrot-fish-care/size-growth/", "Parrot Fish Size & Growth"),
        ("/guides/parrot-fish-care/tank-mates/", "Parrot Fish Tank Mates"),
        ("/guides/parrot-fish-care/food/", "Best Food for Parrot Fish"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PAGE — Black Spots
# ════════════════════════════════════════════════════════════════
BLACK_BODY = """    <p>Black spots on a blood parrot fish look alarming and are usually not an infection. In the large majority of cases they are <strong>melanin marks left by healing chemical burns from ammonia or nitrite</strong>, or ordinary stress marbling. This page works through the causes in order of likelihood, what each one looks like, and what to do.</p>

    <div class="callout"><strong>Start here.</strong> Before treating anything, test ammonia, nitrite and nitrate. If ammonia or nitrite is above 0 ppm, or nitrate is above 40 ppm, you have almost certainly found your answer &mdash; and adding medication to bad water makes things worse.</div>

    <h2 id="causes">Causes of Black Spots, Most Likely First</h2>
    <table class="ptbl">
      <tr><th>Cause</th><th>Appearance</th><th>How common</th></tr>
      <tr><td>Ammonia or nitrite burn (healing)</td><td>Irregular black patches, often on head, fins, flanks; appear after a water-quality problem</td><td>Most common</td></tr>
      <tr><td>Stress marbling</td><td>Smudgy grey-black shading that comes and goes with mood or lighting</td><td>Common</td></tr>
      <tr><td>Genetic pigment</td><td>Stable black markings present from a young age; a calico trait</td><td>Common</td></tr>
      <tr><td>Age and maturity</td><td>Gradual dark speckling as an adult fish ages</td><td>Occasional</td></tr>
      <tr><td>Black spot disease (flukes)</td><td>Distinct raised pinhead-sized black dots, evenly scattered like pepper grains</td><td>Rare in aquaria</td></tr>
      <tr><td>Injury healing</td><td>Dark scar tissue at a specific damaged site</td><td>Occasional</td></tr>
    </table>

    <h2 id="ammonia">Ammonia Burn: The Usual Answer</h2>
    <p>Ammonia and nitrite chemically burn skin and gill tissue. As the tissue heals, the fish deposits melanin over it &mdash; so <strong>the black marks appear as the fish gets better, not while it is getting worse</strong>. That timing confuses a lot of owners into thinking a new disease has started.</p>
    <p>Typical pattern: a new tank, a filter change, a dead fish left in the tank, or a skipped run of water changes; then clamped fins and hiding; then, a week or two later, black patches spreading across the head and fins.</p>
    <p><strong>What to do:</strong></p>
    <ol>
      <li>Test ammonia, nitrite and nitrate with a liquid kit.</li>
      <li>Do a 25&ndash;30% water change immediately, then daily changes until ammonia and nitrite both read 0.</li>
      <li>Use a dechlorinator that detoxifies ammonia while the biofilter catches up.</li>
      <li>Stop feeding for a day or two &mdash; less food means less ammonia.</li>
      <li>Do not change or rinse the filter media in tap water; the bacteria you need are living in it.</li>
      <li>Keep temperature stable at 80&deg;F and leave the fish alone.</li>
    </ol>
    <p>The marks fade over <strong>weeks to a few months</strong> once the water is clean. Some fish keep a faint permanent shadow, which is cosmetic. Full parameter targets are on the <a href="/guides/parrot-fish-care/water-parameters/">water parameters page</a>.</p>

    <h2 id="stress">Stress Marbling and Genetics</h2>
    <p>Blood parrots also darken from plain stress &mdash; bullying, a new tank, a light that is too bright, a tank in a high-traffic room. Stress marbling is smudgier than burn marks and often changes within hours. Fix the stressor and the colour returns: add caves, dim the lighting, and check the <a href="/guides/parrot-fish-care/tank-mates/">tank mate list</a> for an aggressor.</p>
    <p>Genetic black markings are different again: they are stable, present from a young age, and do not spread. Calico and marbled blood parrots are a recognised natural pattern, not a health problem.</p>

    <h2 id="disease">Black Spot Disease (Rare)</h2>
    <p>True black spot disease is caused by encysted digenean fluke larvae, and it needs snails plus fish-eating birds to complete its life cycle &mdash; which is why it turns up in ponds and wild-caught fish and almost never in a closed indoor aquarium.</p>
    <p>Tell it apart by the shape: black spot disease produces <strong>distinct, evenly sized, slightly raised dots like ground pepper</strong>, scattered uniformly. Ammonia burn produces irregular patches of varying size. If you genuinely have flukes, treat with praziquantel and remove snails to break the cycle.</p>

    <h2 id="diagnose">Quick Diagnostic Walkthrough</h2>
    <ol>
      <li><strong>Are ammonia or nitrite above 0?</strong> &rarr; Chemical burn. Water changes, not medication.</li>
      <li><strong>Is nitrate above 40 ppm?</strong> &rarr; Chronic stress and burn. Increase water change volume and frequency.</li>
      <li><strong>Are the marks irregular patches?</strong> &rarr; Burn or stress marbling.</li>
      <li><strong>Are they uniform raised dots?</strong> &rarr; Possible flukes; treat with praziquantel.</li>
      <li><strong>Have they been there since the fish was small?</strong> &rarr; Genetics; no action needed.</li>
      <li><strong>Is the fish eating and swimming normally?</strong> &rarr; Cosmetic. Fix the water and wait.</li>
      <li><strong>Is it also gasping, clamped, or refusing food?</strong> &rarr; Treat that first; the spots are secondary. See <a href="/aquarium-fish-diseases/blood-parrot-cichlid-diseases/">blood parrot diseases</a>.</li>
    </ol>

    <h2 id="prevent">Preventing Black Spots</h2>
    <ul>
      <li>Cycle the tank fully before adding fish, and never fish-in cycle a blood parrot if you can avoid it.</li>
      <li>Change 25&ndash;30% of the water weekly and keep nitrate under 30 ppm.</li>
      <li>Do not overfeed; uneaten food is the most common ammonia source in a stocked tank.</li>
      <li>Rinse filter media in old tank water only.</li>
      <li>Keep at least one cave per fish so a stressed parrot has somewhere to go.</li>
      <li>Quarantine new fish for 2&ndash;4 weeks before they meet the display tank.</li>
      <li>Test monthly even when everything looks fine &mdash; the point is to catch the problem before the fish shows it.</li>
    </ul>
"""

BLACK = {
    "slug": "black-spots",
    "title": "Parrot Fish Black Spots: Causes, Treatment & When to Worry",
    "meta_desc": "Black spots on blood parrot fish are usually healing ammonia burn or stress marbling, not disease. How to tell the causes apart, treat them and prevent recurrence.",
    "h1": "Parrot Fish Black Spots: Causes and Treatment",
    "hero_tag": "Black Spots",
    "hero_meta": "\U0001F9EA Test water first &nbsp;|&nbsp; ⚫ Usually healing burn &nbsp;|&nbsp; \U0001F4C5 Fades over weeks",
    "toc_sections": [
        ("causes", "Causes Ranked"),
        ("ammonia", "Ammonia Burn"),
        ("stress", "Stress & Genetics"),
        ("disease", "Black Spot Disease"),
        ("diagnose", "Diagnostic Walkthrough"),
        ("prevent", "Prevention"),
    ],
    "body": BLACK_BODY,
    "faqs": [
        ("Why does my blood parrot fish have black spots?",
         "The most common cause is melanin left behind as ammonia or nitrite burns heal, which is why the marks often appear after a water quality problem has already passed. Stress marbling and natural calico genetics account for most of the rest."),
        ("Will black spots on my parrot fish go away?",
         "Ammonia burn marks usually fade over several weeks to a few months once ammonia and nitrite read 0 ppm and nitrate stays under 30 ppm. Some fish keep a faint permanent shadow, which is cosmetic only."),
        ("Are black spots on parrot fish contagious?",
         "Burn marks, stress marbling and genetic markings are not contagious. True black spot disease from digenean flukes is contagious but very rare in closed aquariums, because it needs snails and fish-eating birds to complete its life cycle."),
        ("How do I treat black spots on a blood parrot?",
         "Test the water first. If ammonia or nitrite is above 0, do daily 25-30% water changes until they clear rather than medicating. Only uniform, raised, pepper-like dots suggest flukes, which are treated with praziquantel."),
        ("Is black colour on a blood parrot normal?",
         "It can be. Calico and marbled blood parrots naturally carry black patches, and these are stable from a young age and do not spread. New black marks that appear on an adult fish point to water quality or stress instead."),
    ],
    "related": [
        ("/guides/parrot-fish-care/water-parameters/", "Water & Temperature"),
        ("/aquarium-fish-diseases/blood-parrot-cichlid-diseases/", "Blood Parrot Diseases"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/parrot-fish-care/", "Parrot Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
PAGES = [PILLAR, TANK_SIZE, WATER, FOOD, MATES, SIZE, LIFESPAN, TYPES, BREEDING, BLACK]


def main():
    for spec in PAGES:
        html = page(
            slug=spec["slug"], title=spec["title"], meta_desc=spec["meta_desc"],
            h1=spec["h1"], hero_tag=spec["hero_tag"], hero_meta=spec["hero_meta"],
            toc_sections=spec["toc_sections"], body_html=spec["body"],
            faqs=spec["faqs"], related=spec["related"],
        )
        out_dir = BASE / spec["slug"] if spec["slug"] else BASE
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        out_file.write_text(html, encoding="utf-8")
        url = f"/guides/parrot-fish-care/{spec['slug']}/" if spec["slug"] else "/guides/parrot-fish-care/"
        print(f"  {url:<48} {len(html):>7,} bytes")
    print(f"\n{len(PAGES)} pages written to {BASE}")


if __name__ == "__main__":
    main()
