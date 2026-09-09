"""
generate_koi_cluster.py
───────────────────────
Generates the Koi Fish Care cluster sub-pages under
/guides/koi-fish-care/{slug}/index.html, following the betta/discus
cluster template (artlay 2-column with sidebar cluster nav).

Run:  python3 generate_koi_cluster.py
"""

from pathlib import Path
import json

REPO = Path(__file__).parent.parent
BASE = REPO / "guides" / "koi-fish-care"

HERO_IMG = "/assets/encyclopedia/real/koi-fish-wikimedia-real.jpg"

CLUSTER_NAV = [
    ("/guides/koi-fish-care/",                 "\U0001F41F Koi Fish Care Guide", "pillar"),
    ("/guides/koi-fish-care/pond-setup/",      "\U0001FAA3 Pond Size & Setup"),
    ("/guides/koi-fish-care/water-parameters/", "\U0001F321\uFE0F Water & Temperature"),
    ("/guides/koi-fish-care/feeding/",         "\U0001F35A Feeding & Food"),
    ("/guides/koi-fish-care/size-growth/",     "\U0001F4CF Size & Growth Rate"),
    ("/guides/koi-fish-care/lifespan/",        "\u23F3 Koi Lifespan"),
    ("/guides/koi-fish-care/types/",           "\U0001F3A8 Types & Varieties"),
    ("/guides/koi-fish-care/male-vs-female/",  "\u2640\u2642 Male vs Female"),
    ("/guides/koi-fish-care/breeding/",        "\U0001F95A Breeding & Eggs"),
    ("/guides/koi-fish-care/diseases/",        "\U0001FA7A Diseases & Symptoms"),
    ("/guides/koi-fish-care/tank-mates/",      "\U0001F420 Tank & Pond Mates"),
    ("/guides/koi-fish-tank/",                 "\U0001F5C3\uFE0F Koi Fish Tank Guide"),
]

TOOL_LINKS = [
    ("/calculators/koi-fish-tank-size/",   "Koi Pond Size Calculator"),
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
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('/assets/encyclopedia/real/koi-fish-wikimedia-real.jpg') center/cover no-repeat}
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
        href = entry[0]
        label = entry[1]
        css_class = entry[2] if len(entry) > 2 else ""
        is_cur = href.rstrip("/").endswith("/" + current_slug) and current_slug != ""
        cls = (css_class + " cur").strip() if is_cur else css_class
        items.append(f'<a href="{href}" class="{cls}">{label}</a>')
    return "\n      ".join(items)


def toc_html(sections: list) -> str:
    return "\n      ".join(f'<a href="#{sid}">{label}</a>' for sid, label in sections)


def tool_links_html() -> str:
    return "\n      ".join(
        f'<a href="{href}">{label} <span>&rarr;</span></a>' for href, label in TOOL_LINKS
    )


def faq_json(faqs: list) -> str:
    entities = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                       "mainEntity": entities}, ensure_ascii=False)


def faq_visible_html(faqs: list) -> str:
    rows = []
    for q, a in faqs:
        rows.append(f"    <h3>{q}</h3>\n    <p>{a}</p>")
    return ('    <h2 id="faq">Frequently Asked Questions</h2>\n' + "\n".join(rows))


def related_html(links: list) -> str:
    items = "".join(
        f'<a href="{href}" title="{label}">{label}</a>' for href, label in links
    )
    return ('    <h2 id="related">Related Koi Guides and Tools</h2>\n'
            f'    <div class="guide-links">{items}</div>')


def page(slug, title, meta_desc, h1, hero_tag, hero_meta, date,
         toc_sections, body_html, faqs, related):
    canonical = f"https://www.fishcareai.com/guides/koi-fish-care/{slug}/"
    breadcrumb_json = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},'
        '{"@type":"ListItem","position":2,"name":"Guides","item":"https://www.fishcareai.com/guides/"},'
        '{"@type":"ListItem","position":3,"name":"Koi Fish Care Guide",'
        '"item":"https://www.fishcareai.com/guides/koi-fish-care/"},'
        f'{{"@type":"ListItem","position":4,"name":{json.dumps(h1)},"item":"{canonical}"}}'
        "]}"
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
    toc = toc_sections + [("faq", "FAQ")]

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
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:image" content="https://www.fishcareai.com{HERO_IMG}"/>
<meta name="twitter:card" content="summary_large_image"/>
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
  <button class="hbg" aria-label="Menu" onclick="this.nextElementSibling||0;document.querySelector('.nlinks').classList.toggle('open')">
    <span></span><span></span><span></span>
  </button>
</nav>

<section class="guide-hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="/guides/">Guides</a><span>/</span>
      <a href="/guides/koi-fish-care/">Koi Fish Care Guide</a><span>/</span>
      <span style="color:rgba(255,255,255,.9)">{hero_tag}</span>
    </div>
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">&#127907; Koi Fish Care</div>
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
      <h4>Koi Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc)}
    </div>
    <div class="tool-card">
      <h4>Koi Tools</h4>
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


# ────────────────────────────────────────────────────────────────
# PAGE 1 — Pond Size, Depth & Setup
# ────────────────────────────────────────────────────────────────
POND_SETUP_BODY = """    <p>A koi pond is not a scaled-up goldfish pond. Koi reach 24&ndash;36 inches, live for decades, eat heavily and produce a large ammonia load, so the pond has to be sized for the adult fish you will eventually have &mdash; not the 4-inch juveniles you buy. This page covers koi pond size, koi pond depth, and a build order that gets the water stable before the fish arrive.</p>

    <h2 id="pond-size">Koi Pond Size: How Many Gallons Do Koi Need?</h2>
    <p>The working rule used by most koi clubs is <strong>250 gallons per koi as an absolute minimum and 500 gallons per koi as the target</strong>, with a floor of about 1,000 gallons for any pond that will hold koi permanently. Below roughly 1,000 gallons, temperature and water chemistry swing too fast for a fish that will eventually weigh several pounds.</p>
    <table class="ptbl">
      <tr><th>Pond Volume</th><th>Realistic Koi Stocking</th><th>Notes</th></tr>
      <tr><td>Under 500 gal</td><td>&#10060; Not a koi pond</td><td>Goldfish or juvenile grow-out only</td></tr>
      <tr><td>1,000 gal</td><td>2&ndash;4 koi</td><td>Practical starter pond; needs disciplined filtration</td></tr>
      <tr><td>2,000 gal</td><td>4&ndash;8 koi</td><td>Comfortable for a first serious pond</td></tr>
      <tr><td>3,500 gal</td><td>7&ndash;14 koi</td><td>Stable temperature, room for adult growth</td></tr>
      <tr><td>5,000 gal+</td><td>10&ndash;20 koi</td><td>Show-quality territory; supports jumbo koi</td></tr>
    </table>
    <p>To convert dimensions to volume: <strong>length &times; width &times; average depth (feet) &times; 7.48 = gallons</strong>. A 10 &times; 6 &times; 3 ft pond holds about 1,346 gallons. Our <a href="/calculators/koi-fish-tank-size/">koi pond size calculator</a> does this for you and cross-checks it against your koi count.</p>
    <div class="callout"><strong>Surface area matters as much as volume.</strong> Oxygen enters through the surface, so a wide shallow-ish pond gases better than a narrow deep well of the same volume. Aim for at least 1 square foot of surface per inch of adult koi length before counting on mechanical aeration.</div>

    <h2 id="pond-depth">Koi Pond Depth: 3 Feet Minimum</h2>
    <p>Koi pond depth does three jobs: it buffers temperature, it gives the fish a refuge from herons and raccoons, and it provides an unfrozen layer in winter. The minimum working depth is <strong>3 feet</strong>; 4 feet is the standard recommendation, and 6 feet is worth building where winters are severe or predators are a known problem.</p>
    <table class="ptbl">
      <tr><th>Depth</th><th>Verdict</th><th>What it means in practice</th></tr>
      <tr><td>Under 2 ft</td><td>&#10060; Unsafe</td><td>Freezes or overheats; herons wade straight in</td></tr>
      <tr><td>2&ndash;3 ft</td><td>&#9888;&#65039; Marginal</td><td>Workable only in mild climates with predator netting</td></tr>
      <tr><td>3&ndash;4 ft</td><td>&#9989; Standard</td><td>Stable temperature; koi can hold below heron reach</td></tr>
      <tr><td>4&ndash;6 ft</td><td>&#9989; Best</td><td>Reliable winter refuge; supports jumbo koi growth</td></tr>
    </table>
    <p>A common design compromise is a deep central zone of 4&ndash;5 feet with shallower 2-foot shelves at the edges for plants. Keep the shelves narrow &mdash; a wide shallow ledge is a heron platform.</p>

    <h2 id="setup-steps">Koi Pond Setup, Step by Step</h2>
    <ol>
      <li><strong>Site it.</strong> Partial shade for 4&ndash;6 hours a day limits algae and summer heat. Stay clear of deciduous trees (leaf load) and root systems that will lift a liner. Never site a pond at the bottom of a slope that drains lawn chemicals into it.</li>
      <li><strong>Excavate with the plumbing in mind.</strong> Dig the deep zone first, slope the floor 1&ndash;2 inches per 10 feet toward a bottom drain, and trench for return lines before you line anything.</li>
      <li><strong>Underlay and liner.</strong> Geotextile underlay, then 45-mil EPDM rubber liner. EPDM is fish-safe, flexible in cold, and repairable. Concrete ponds work but must be sealed with a pond-rated coating &mdash; raw concrete leaches lime and drives pH above 9.</li>
      <li><strong>Plumb the filtration.</strong> Bottom drain and skimmer feed the pump; the pump feeds mechanical filtration, then biological media, then back to the pond. Size the plumbing generously &mdash; 2-inch pipe on a 3,000-gallon pond, not 1.5-inch.</li>
      <li><strong>Add aeration.</strong> An air pump with a bottom-mounted diffuser plate runs year-round. It is the single cheapest insurance policy in koi keeping.</li>
      <li><strong>Fill and dechlorinate.</strong> Treat the whole volume for chlorine and chloramine before anything living goes in.</li>
      <li><strong>Cycle the filter for 4&ndash;6 weeks.</strong> Dose ammonia or run a few hardy juveniles, and do not add your main koi until ammonia and nitrite both read 0 ppm. See the <a href="/guides/koi-fish-care/water-parameters/">koi water parameters guide</a>.</li>
      <li><strong>Stock slowly.</strong> Add 2&ndash;3 koi, wait three weeks, test, then add more. Quarantine every new fish for 3&ndash;4 weeks in a separate tank.</li>
    </ol>

    <h2 id="filtration">Filtration and Turnover</h2>
    <p>Koi ponds are filtration projects with fish in them. Target a <strong>full turnover of pond volume every 1&ndash;2 hours</strong> &mdash; a 2,000-gallon pond wants a pump moving 1,000&ndash;2,000 GPH after head loss, not on the box rating.</p>
    <ul>
      <li><strong>Mechanical stage:</strong> settlement chamber, sieve or drum filter. Removes solids before they rot into ammonia. This stage does most of the work in a koi pond.</li>
      <li><strong>Biological stage:</strong> moving-bed media (K1), bioballs or matting. Size for the feed load, not the volume &mdash; heavily fed koi need more biomedia than the pond size alone suggests.</li>
      <li><strong>UV clarifier:</strong> 10 watts per 1,000 gallons controls green water. It does not replace filtration, and it does not treat parasites on the fish.</li>
      <li><strong>Bottom drain:</strong> the difference between a pond you skim and a pond that actually cleans itself. Retrofit is expensive; build it in from the start.</li>
    </ul>

    <h2 id="aeration">Aeration and Oxygen</h2>
    <p>Koi need dissolved oxygen above <strong>6 mg/L</strong>, and warm water holds less of it. Summer nights are the danger window: plants and algae consume oxygen after dark, and a pond that reads fine at noon can hit critical levels at 5 a.m. Run aeration 24 hours a day, and add a second air stone before a heat wave rather than after.</p>
    <p>Signs of low oxygen: koi crowding the waterfall or gasping at the surface in the early morning, listless fish at midday, several fish affected at once.</p>

    <h2 id="winter-predators">Winter and Predator Planning</h2>
    <p>In freezing climates the goal is not a heated pond &mdash; it is a hole in the ice for gas exchange. A floating de-icer plus a relocated air stone at mid-depth (not on the bottom, which would destroy the warm layer koi rest in) keeps the pond safe. Stop feeding entirely below 50&deg;F (10&deg;C).</p>
    <p>For predators: depth plus steep sides defeats herons; netting defeats herons and leaves; a covered cave or length of 8-inch pipe on the pond floor gives koi somewhere to hide when a raccoon visits.</p>

    <h2 id="cost">What a Koi Pond Actually Costs</h2>
    <table class="ptbl">
      <tr><th>Component</th><th>Typical range (2,000 gal pond)</th></tr>
      <tr><td>Excavation</td><td>$0 (DIY) &ndash; $2,000</td></tr>
      <tr><td>Liner + underlay</td><td>$400 &ndash; $900</td></tr>
      <tr><td>Pump</td><td>$150 &ndash; $500</td></tr>
      <tr><td>Filtration system</td><td>$500 &ndash; $2,500</td></tr>
      <tr><td>Aeration + UV</td><td>$150 &ndash; $400</td></tr>
      <tr><td>Plumbing + bottom drain</td><td>$200 &ndash; $700</td></tr>
      <tr><td>Running cost</td><td>$25 &ndash; $70 per month (pump, air, de-icer)</td></tr>
    </table>
"""

POND_SETUP = {
    "slug": "pond-setup",
    "title": "Koi Pond Size, Depth & Setup Guide (Gallons per Koi) | FishCare AI",
    "meta_desc": "How big and how deep a koi pond needs to be: 250-500 gallons per koi, 1,000 gallon minimum, 3-4 ft depth. Step-by-step koi pond setup, filtration, aeration and cost.",
    "h1": "Koi Pond Size, Depth and Setup",
    "hero_tag": "Pond Size & Setup",
    "hero_meta": "\U0001F4A7 500 gal per koi &nbsp;|&nbsp; \U0001F4CF 3&ndash;4 ft minimum depth &nbsp;|&nbsp; \U0001F504 1&ndash;2 hour turnover",
    "date": "2026-09-08",
    "toc_sections": [
        ("pond-size", "Koi Pond Size"),
        ("pond-depth", "Koi Pond Depth"),
        ("setup-steps", "Setup Step by Step"),
        ("filtration", "Filtration & Turnover"),
        ("aeration", "Aeration & Oxygen"),
        ("winter-predators", "Winter & Predators"),
        ("cost", "Cost"),
    ],
    "body": POND_SETUP_BODY,
    "faqs": [
        ("How big should a koi pond be?",
         "Allow 250 gallons per koi as an absolute minimum and 500 gallons per koi as the target, with a floor of about 1,000 gallons for any permanent koi pond. A 1,000-gallon pond suits 2-4 koi; 2,000 gallons suits 4-8."),
        ("How deep should a koi pond be?",
         "Three feet is the minimum, 4 feet is the standard recommendation, and 5-6 feet is worth building in cold climates or where herons and raccoons are a problem. Depth stabilises temperature and gives koi a refuge below heron reach."),
        ("Can koi live in a small pond?",
         "Koi reach 24-36 inches and live 25+ years, so a pond under 500 gallons cannot support them long term. Small ponds are suitable for goldfish, or as temporary grow-out space for juvenile koi that will move to a larger pond."),
        ("How many gallons per koi fish?",
         "250 gallons per koi is the working minimum and 500 gallons per koi is the recommended figure. The lower number assumes strong filtration, a bottom drain and constant aeration."),
        ("Do koi ponds need a pump running all the time?",
         "Yes. The pump and the air pump run 24 hours a day year-round. Biological filter bacteria die within hours without flow, and oxygen levels fall fastest overnight when a stopped pump does the most damage."),
    ],
    "related": [
        ("/calculators/koi-fish-tank-size/", "Koi Pond Size Calculator"),
        ("/guides/koi-fish-care/water-parameters/", "Koi Water Parameters"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
        ("/guides/koi-fish-tank/", "Koi Fish Tank Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 2 — Water Parameters & Temperature
# ────────────────────────────────────────────────────────────────
WATER_BODY = """    <p>Koi are hardy across a wide range, but they are hardy to <em>stable</em> conditions. Almost every koi problem traced back to its cause turns out to be water: an uncycled filter, a pH crash after rain, oxygen collapse on a hot night, or a feeding schedule that ignored water temperature. These are the koi water parameters worth testing and the numbers to hold them at.</p>

    <h2 id="target-parameters">Koi Pond Water Parameters at a Glance</h2>
    <table class="ptbl">
      <tr><th>Parameter</th><th>Target</th><th>Act now if</th></tr>
      <tr><td>Temperature</td><td>59&ndash;77&deg;F (15&ndash;25&deg;C)</td><td>Below 39&deg;F or above 86&deg;F</td></tr>
      <tr><td>pH</td><td>7.0&ndash;8.6 (ideal 7.5)</td><td>Below 6.5 or above 9.0</td></tr>
      <tr><td>Ammonia (NH&#8323;)</td><td>0 ppm</td><td>Any reading above 0.02 ppm</td></tr>
      <tr><td>Nitrite (NO&#8322;)</td><td>0 ppm</td><td>Any reading above 0.1 ppm</td></tr>
      <tr><td>Nitrate (NO&#8323;)</td><td>Under 40 ppm (ideally under 20)</td><td>Above 80 ppm</td></tr>
      <tr><td>KH / carbonate hardness</td><td>Above 5 dKH (90 ppm)</td><td>Below 3 dKH (54 ppm)</td></tr>
      <tr><td>GH / general hardness</td><td>4&ndash;12 dGH</td><td>Below 3 dGH</td></tr>
      <tr><td>Dissolved oxygen</td><td>Above 6 mg/L</td><td>Below 5 mg/L</td></tr>
    </table>
    <p>Test ammonia, nitrite and pH weekly on an established pond and daily on a new one. Use a liquid test kit &mdash; paper strips are useful for a quick trend but not accurate enough to make a treatment decision on. The <a href="/tools/water-parameter-checker/">water parameter checker</a> will tell you which reading to fix first.</p>

    <h2 id="temperature">Koi Fish Water Temperature</h2>
    <p>Koi are coldwater fish, not tropical fish, and they do not need a heater in most climates. The comfortable range is <strong>59&ndash;77&deg;F (15&ndash;25&deg;C)</strong>. They survive from just above freezing to the mid-80s, but the extremes are survival, not health: metabolism, immune response and appetite all change with temperature.</p>
    <table class="ptbl">
      <tr><th>Water temperature</th><th>What the koi are doing</th><th>What you should do</th></tr>
      <tr><td>Below 41&deg;F (5&deg;C)</td><td>Torpor; resting on the bottom, barely moving</td><td>No feeding. Keep a hole open in the ice; do not break ice by hitting it</td></tr>
      <tr><td>41&ndash;50&deg;F (5&ndash;10&deg;C)</td><td>Very low activity, digestion nearly stopped</td><td>No feeding. Reduce handling to zero</td></tr>
      <tr><td>50&ndash;59&deg;F (10&ndash;15&deg;C)</td><td>Waking up, light feeding response</td><td>Wheat germ food every other day at most</td></tr>
      <tr><td>59&ndash;68&deg;F (15&ndash;20&deg;C)</td><td>Active, digesting normally</td><td>Feed once or twice daily; parasite risk rises</td></tr>
      <tr><td>68&ndash;77&deg;F (20&ndash;25&deg;C)</td><td>Peak growth and colour development</td><td>Feed 2&ndash;4 times daily; watch oxygen</td></tr>
      <tr><td>Above 82&deg;F (28&deg;C)</td><td>Stressed; oxygen falling</td><td>Add aeration and shade, cut feeding back</td></tr>
    </table>
    <div class="callout callout-warn"><strong>Rate of change matters more than the number.</strong> Koi handle 50&deg;F water they arrived at slowly far better than a 6&deg;F drop in an afternoon. Keep any change under about 2&deg;F per hour when moving fish or doing a large water change, and match top-up water temperature to the pond.</div>
    <p>Koi herpes virus becomes active in the 64&ndash;81&deg;F window, which is one reason new fish should be quarantined at those temperatures rather than introduced straight into a warm summer pond.</p>

    <h2 id="ph">Koi Fish pH</h2>
    <p>Koi tolerate <strong>pH 7.0&ndash;8.6</strong>, with 7.5 as the practical target. Stability beats precision &mdash; a pond steady at 8.2 is healthier than one swinging between 7.0 and 8.4 every day.</p>
    <ul>
      <li><strong>pH falling over weeks</strong> usually means the carbonate buffer is exhausted. Test KH; if it is under 3 dKH, add baking soda (sodium bicarbonate) at roughly 1 teaspoon per 100 gallons to lift KH by about 1 dKH, then retest.</li>
      <li><strong>pH high and climbing</strong> in a new concrete or rendered pond means lime leaching. Seal the concrete or run repeated water changes until it stabilises.</li>
      <li><strong>Daily pH swing</strong> of more than 0.4 points points at a heavy algae or plant load: photosynthesis strips CO&#8322; by day and returns it at night. Aeration flattens the curve.</li>
    </ul>
    <div class="callout"><strong>pH and ammonia interact.</strong> The same total ammonia reading is far more toxic at pH 8.5 than at pH 7.0, because more of it exists as free ammonia. If you have an ammonia reading, do not chase the pH down to fix it &mdash; do a water change and stop feeding.</div>

    <h2 id="cycling">Ammonia, Nitrite and Cycling</h2>
    <p>Koi produce more waste per fish than almost anything else in a garden pond. The biological filter converts ammonia to nitrite and nitrite to nitrate; until that bacterial colony is established, both ammonia and nitrite will spike.</p>
    <ol>
      <li>Run the pump and filter for <strong>4&ndash;6 weeks</strong> before stocking, dosing an ammonia source to feed the bacteria.</li>
      <li>Watch ammonia rise, then fall as nitrite rises, then both settle to 0 ppm with nitrate appearing. That sequence is the cycle completing.</li>
      <li>Stock in stages afterwards &mdash; adding all the koi at once outruns the colony you just built.</li>
    </ol>
    <p>If ammonia or nitrite appears in an established pond: stop feeding for 2&ndash;3 days, do a 25&ndash;30% water change with dechlorinated water, check whether the pump or air supply failed, and check for a dead fish or rotting leaves in the filter. Adding salt at 0.1&ndash;0.3% helps koi tolerate nitrite specifically while the filter recovers.</p>

    <h2 id="oxygen">Dissolved Oxygen</h2>
    <p>Warm water holds less oxygen, and koi demand more of it as they warm up &mdash; the two curves cross badly in midsummer. Hold dissolved oxygen above 6 mg/L. Koi crowding a waterfall at dawn, gasping at the surface, or hanging near the return jets are telling you the pond ran short overnight.</p>

    <h2 id="water-changes">Water Changes and Testing Routine</h2>
    <table class="ptbl">
      <tr><th>Task</th><th>Frequency</th></tr>
      <tr><td>Test ammonia, nitrite, pH</td><td>Weekly (daily on a new pond)</td></tr>
      <tr><td>Test KH and nitrate</td><td>Monthly</td></tr>
      <tr><td>Water change 10&ndash;20%</td><td>Weekly, or 25% every two weeks</td></tr>
      <tr><td>Rinse mechanical media in pond water</td><td>Weekly</td></tr>
      <tr><td>Clean skimmer basket, remove leaves</td><td>Every few days in autumn</td></tr>
      <tr><td>Full filter service</td><td>Spring and autumn</td></tr>
    </table>
    <p>Never rinse biological media under chlorinated tap water &mdash; it kills the colony and restarts the cycle. Always dechlorinate top-up water; chloramine in particular does not gas off on standing.</p>
"""

WATER = {
    "slug": "water-parameters",
    "title": "Koi Water Parameters & Temperature: pH, Ammonia, Oxygen | FishCare AI",
    "meta_desc": "Koi pond water parameters explained: 59-77F temperature, pH 7.0-8.6, 0 ppm ammonia and nitrite, KH above 5 dKH, oxygen above 6 mg/L, plus a testing and water-change routine.",
    "h1": "Koi Water Parameters and Temperature",
    "hero_tag": "Water & Temperature",
    "hero_meta": "\U0001F321️ 59&ndash;77&deg;F ideal &nbsp;|&nbsp; ⚗️ pH 7.0&ndash;8.6 &nbsp;|&nbsp; \U0001F4A8 O&#8322; above 6 mg/L",
    "date": "2026-09-08",
    "toc_sections": [
        ("target-parameters", "Parameters at a Glance"),
        ("temperature", "Water Temperature"),
        ("ph", "Koi Fish pH"),
        ("cycling", "Ammonia & Nitrite"),
        ("oxygen", "Dissolved Oxygen"),
        ("water-changes", "Testing Routine"),
    ],
    "body": WATER_BODY,
    "faqs": [
        ("What water temperature do koi fish need?",
         "Koi are comfortable between 59 and 77F (15-25C). They survive from just above freezing to the mid-80s, but growth, appetite and immune function are best in the 65-75F band. Rate of change matters more than the exact number - keep swings under about 2F per hour."),
        ("What pH do koi fish need?",
         "Koi tolerate pH 7.0-8.6 and do best around 7.5. Stability is more important than the exact value; a pond steady at 8.2 is healthier than one swinging between 7.0 and 8.4 daily. Keep KH above 5 dKH to hold pH steady."),
        ("What are safe ammonia and nitrite levels for koi?",
         "Both should read 0 ppm. Any detectable ammonia above 0.02 ppm or nitrite above 0.1 ppm calls for an immediate 25-30% water change and a feeding stop until the filter catches up."),
        ("Do koi ponds need a heater?",
         "No. Koi are coldwater fish and overwinter safely in a pond deep enough not to freeze solid - 3 feet minimum, 4 feet preferred. A de-icer to keep a gas-exchange hole open in the ice matters far more than heating the water."),
        ("How often should I test koi pond water?",
         "Test ammonia, nitrite and pH weekly on an established pond and daily on a newly filled one. Check KH and nitrate monthly. Use a liquid test kit rather than strips for any reading you plan to act on."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/koi-fish-care/pond-setup/", "Koi Pond Size & Setup"),
        ("/guides/koi-fish-care/diseases/", "Koi Diseases & Symptoms"),
        ("/guides/aquarium-water-parameters/", "Aquarium Water Parameters"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 3 — Feeding & Food
# ────────────────────────────────────────────────────────────────
FEEDING_BODY = """    <p>Koi are omnivores with an appetite that runs on water temperature, not on the clock. The same fish that needs four meals a day in July should get nothing at all in January &mdash; feeding a koi whose digestion has shut down for winter is one of the fastest ways to kill it. This is what to feed koi fish, how much, and how often through the year.</p>

    <h2 id="what-they-eat">What Do Koi Fish Eat?</h2>
    <p>In a pond, koi eat a prepared pellet as the staple and forage for everything else: algae, insect larvae, worms, crustaceans, plant matter and detritus. They are bottom-oriented grazers by nature and will root through substrate all day given the chance. A wild carp diet is roughly 30&ndash;40% animal matter, and koi food formulations reflect that.</p>
    <table class="ptbl">
      <tr><th>Food</th><th>Role</th><th>Notes</th></tr>
      <tr><td>Floating koi pellets</td><td>Staple</td><td>Lets you watch every fish eat &mdash; the best daily health check you get</td></tr>
      <tr><td>Sinking pellets</td><td>Staple in cold or windy conditions</td><td>Easier for older koi; harder to monitor intake</td></tr>
      <tr><td>Wheat germ food</td><td>Spring and autumn staple</td><td>Digestible at low temperatures when protein food is not</td></tr>
      <tr><td>Colour-enhancing food (spirulina, astaxanthin)</td><td>Summer supplement</td><td>Deepens reds and oranges; overuse can yellow white skin</td></tr>
      <tr><td>Vegetables: lettuce, peas, watermelon, orange slices</td><td>Treat, 1&ndash;2&times; weekly</td><td>Shelled peas help with constipation and buoyancy issues</td></tr>
      <tr><td>Live/frozen: earthworms, bloodworms, brine shrimp, silkworm pupae</td><td>Treat / conditioning</td><td>Excellent for growth and pre-spawning conditioning</td></tr>
      <tr><td>Bread, crackers, dog food</td><td>&#10060; Avoid</td><td>No usable nutrition; fouls water and swells in the gut</td></tr>
    </table>

    <h2 id="best-food">Best Food for Koi Fish: Reading the Label</h2>
    <p>The best koi food for your pond is the one matched to the current water temperature and to what you want from the fish &mdash; growth, colour, or simple maintenance.</p>
    <ul>
      <li><strong>Protein 32&ndash;40%:</strong> growth food for summer and for koi under three years old.</li>
      <li><strong>Protein 25&ndash;32%:</strong> maintenance food for adult koi in the main season.</li>
      <li><strong>Wheat germ base, protein under 30%:</strong> spring and autumn food for water between 50 and 60&deg;F.</li>
      <li><strong>Fish meal as the first ingredient</strong> beats a cereal filler first; koi digest marine protein far better than terrestrial grain protein.</li>
      <li><strong>Pellet size</strong> should match mouth size &mdash; 3 mm for koi under 6 inches, 5&ndash;7 mm for adults. Mixed ponds do best with a mixed size so the small fish are not outcompeted.</li>
      <li><strong>Buy small bags.</strong> Fats oxidise; koi food older than about six months loses vitamin C and palatability. Store sealed, cool and dark.</li>
    </ul>

    <h2 id="how-often">How Often to Feed Koi Fish</h2>
    <p>Feed only what the koi finish in about <strong>5 minutes</strong>, and scoop out whatever is left. Frequency comes from the pond thermometer:</p>
    <table class="ptbl">
      <tr><th>Water temperature</th><th>Feeding frequency</th><th>Food type</th></tr>
      <tr><td>Below 50&deg;F (10&deg;C)</td><td>Do not feed at all</td><td>&mdash;</td></tr>
      <tr><td>50&ndash;59&deg;F (10&ndash;15&deg;C)</td><td>Every 2&ndash;3 days, small amounts</td><td>Wheat germ</td></tr>
      <tr><td>59&ndash;65&deg;F (15&ndash;18&deg;C)</td><td>Once daily</td><td>Wheat germ or low-protein staple</td></tr>
      <tr><td>65&ndash;75&deg;F (18&ndash;24&deg;C)</td><td>2&ndash;4 times daily</td><td>Growth or colour food, 32&ndash;40% protein</td></tr>
      <tr><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td><td>2&ndash;3 times daily</td><td>Staple; watch oxygen levels closely</td></tr>
      <tr><td>Above 82&deg;F (28&deg;C)</td><td>Once daily or skip</td><td>Reduce load while oxygen is low</td></tr>
    </table>
    <div class="callout callout-warn"><strong>The 50&deg;F rule is not a guideline.</strong> Below about 50&deg;F a koi's gut stops moving food along. Anything eaten sits and rots internally. Use a pond thermometer at mid-depth, not the air temperature, and stop feeding for the season once the water holds below 50&deg;F for several days.</div>

    <h2 id="feeding-chart">Koi Feeding Chart by Season</h2>
    <table class="ptbl">
      <tr><th>Season</th><th>Typical water temp</th><th>Plan</th></tr>
      <tr><td>Early spring</td><td>45&ndash;55&deg;F</td><td>First feed only once water holds above 50&deg;F. Wheat germ, tiny portions, every other day. Test water &mdash; the filter is waking up more slowly than the fish</td></tr>
      <tr><td>Late spring</td><td>55&ndash;68&deg;F</td><td>Move to once or twice daily; switch to staple food above 60&deg;F. Condition breeders with extra protein</td></tr>
      <tr><td>Summer</td><td>68&ndash;80&deg;F</td><td>Peak feeding: 2&ndash;4 meals daily, growth and colour food. Increase aeration to match</td></tr>
      <tr><td>Early autumn</td><td>68&ndash;58&deg;F</td><td>Step back to once or twice daily; switch back to wheat germ below 60&deg;F to build winter reserves</td></tr>
      <tr><td>Late autumn</td><td>58&ndash;50&deg;F</td><td>Every 2&ndash;3 days, wheat germ only. Stop completely at 50&deg;F</td></tr>
      <tr><td>Winter</td><td>Below 50&deg;F</td><td>No food. Keep a gas-exchange hole open in the ice and leave the fish alone</td></tr>
    </table>

    <h2 id="how-much">How Much to Feed</h2>
    <p>Two methods, both sound. The <strong>5-minute rule</strong> &mdash; feed what disappears in five minutes &mdash; is what most keepers use day to day. The <strong>body-weight method</strong> is more precise for grow-out ponds: feed roughly 1% of total koi body weight per day at 60&deg;F, rising to about 3% at 75&deg;F, split across the day's meals.</p>
    <p>Overfeeding rarely harms the fish directly; it harms the water. Uneaten pellets and the extra waste from overfed koi push ammonia up and oxygen down, which is what actually causes the losses blamed on food.</p>

    <h2 id="not-eating">Koi Not Eating</h2>
    <p>Work through this order before assuming disease:</p>
    <ol>
      <li><strong>Water temperature.</strong> Below 50&deg;F, refusing food is correct behaviour, not a symptom.</li>
      <li><strong>Water quality.</strong> Test ammonia, nitrite and pH. Appetite is the first thing koi drop when ammonia appears.</li>
      <li><strong>Recent change.</strong> New fish, a big water change, or a move &mdash; koi routinely fast for several days after any of these.</li>
      <li><strong>Food age.</strong> Stale food loses palatability. Try a fresh bag or a handful of earthworms; a koi that ignores an earthworm is genuinely unwell.</li>
      <li><strong>Spawning season.</strong> Koi often stop eating for a few days around a spawn.</li>
      <li><strong>Disease.</strong> If water is clean, temperature is right and the fish is still refusing food after 3&ndash;4 days, check for flashing, clamped fins, ulcers or gill movement problems &mdash; see the <a href="/guides/koi-fish-care/diseases/">koi disease guide</a>.</li>
    </ol>
"""

FEEDING = {
    "slug": "feeding",
    "title": "What to Feed Koi Fish: Food Guide & Seasonal Feeding Chart | FishCare AI",
    "meta_desc": "What koi fish eat, the best koi food by protein level, how often to feed by water temperature, and a season-by-season koi feeding chart. Stop feeding below 50F.",
    "h1": "Koi Fish Food and Feeding Chart",
    "hero_tag": "Feeding & Food",
    "hero_meta": "\U0001F35A 5-minute rule &nbsp;|&nbsp; \U0001F321️ Stop below 50&deg;F &nbsp;|&nbsp; \U0001F4C8 2&ndash;4 meals in summer",
    "date": "2026-09-08",
    "toc_sections": [
        ("what-they-eat", "What Koi Eat"),
        ("best-food", "Best Koi Food"),
        ("how-often", "How Often to Feed"),
        ("feeding-chart", "Seasonal Feeding Chart"),
        ("how-much", "How Much to Feed"),
        ("not-eating", "Koi Not Eating"),
    ],
    "body": FEEDING_BODY,
    "faqs": [
        ("What do koi fish eat?",
         "Koi are omnivores. A prepared koi pellet is the staple, supplemented with algae, insect larvae, worms and crustaceans they forage themselves, plus occasional vegetables such as lettuce, shelled peas, watermelon and orange segments."),
        ("How often should I feed koi fish?",
         "Feed by water temperature: 2-4 times daily above 65F, once daily between 59 and 65F, every 2-3 days between 50 and 59F, and not at all below 50F. Offer only what the koi finish in about 5 minutes."),
        ("What is the best food for koi fish?",
         "Use a fish-meal-based pellet sized to the fish: 32-40% protein growth food in summer and for young koi, 25-32% maintenance food for adults, and a wheat germ formula in spring and autumn when water is between 50 and 60F."),
        ("Can koi fish eat bread?",
         "No. Bread has no usable nutrition for koi, swells in the gut, and fouls pond water quickly. Use shelled peas, lettuce or melon if you want a low-cost treat."),
        ("Why is my koi not eating?",
         "Check water temperature first - below 50F, fasting is normal. Then test ammonia, nitrite and pH, since appetite loss is the earliest sign of a water quality problem. Recent moves, spawning and stale food also cause short fasts. A koi that refuses an earthworm in clean, warm water is likely ill."),
    ],
    "related": [
        ("/guides/koi-fish-care/water-parameters/", "Koi Water Parameters"),
        ("/guides/koi-fish-care/size-growth/", "Koi Size & Growth Rate"),
        ("/tools/fish-feeding-calculator/", "Fish Feeding Calculator"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 4 — Size & Growth Rate
# ────────────────────────────────────────────────────────────────
SIZE_BODY = """    <p>The single most common mistake in koi keeping is buying a 4-inch fish and planning for a 4-inch fish. Koi are one of the largest ornamental pond species available to hobbyists, and they get there faster than most people expect &mdash; a well-fed koi can add 6 inches in its first year.</p>

    <h2 id="how-big">How Big Do Koi Fish Get?</h2>
    <p>Adult koi reach <strong>24&ndash;36 inches (60&ndash;90 cm)</strong> depending on bloodline, pond conditions and feeding. Weight at that length runs from about 8 to 35 pounds.</p>
    <table class="ptbl">
      <tr><th>Type</th><th>Typical adult length</th><th>Notes</th></tr>
      <tr><td>Domestic koi (US/EU bred)</td><td>18&ndash;24 in (45&ndash;60 cm)</td><td>The usual garden-centre fish; grows fast, tops out earlier</td></tr>
      <tr><td>Japanese-bred koi</td><td>26&ndash;32 in (65&ndash;80 cm)</td><td>Bloodlines selected over generations for frame and finish</td></tr>
      <tr><td>Jumbo koi (Ogon, Chagoi, Sanke lines)</td><td>32&ndash;36 in (80&ndash;90 cm)</td><td>Requires a deep, large, heavily filtered pond</td></tr>
      <tr><td>Butterfly koi</td><td>24&ndash;36 in (60&ndash;90 cm)</td><td>Body length similar; the long fins make them look larger</td></tr>
      <tr><td>Ghost koi</td><td>24&ndash;30 in (60&ndash;75 cm)</td><td>Hybrid vigour makes them among the fastest growers</td></tr>
    </table>
    <p>The record lengths quoted in the hobby &mdash; koi past 40 inches and 90 pounds &mdash; come from exceptional Japanese fish in mud ponds, not from garden ponds.</p>

    <h2 id="growth-rate">Koi Growth Rate Year by Year</h2>
    <p>Koi grow fastest in their first three years, then slow markedly. These figures assume good water quality, summer temperatures in the 68&ndash;77&deg;F band, and consistent feeding.</p>
    <table class="ptbl">
      <tr><th>Age</th><th>Typical length</th><th>Growth that year</th></tr>
      <tr><td>Hatch (fry)</td><td>0.25 in</td><td>&mdash;</td></tr>
      <tr><td>3 months</td><td>2&ndash;3 in</td><td>Fastest relative growth of the whole life</td></tr>
      <tr><td>1 year</td><td>5&ndash;8 in</td><td>5&ndash;8 in</td></tr>
      <tr><td>2 years</td><td>10&ndash;14 in</td><td>4&ndash;6 in</td></tr>
      <tr><td>3 years</td><td>14&ndash;18 in</td><td>3&ndash;5 in</td></tr>
      <tr><td>4&ndash;5 years</td><td>18&ndash;24 in</td><td>2&ndash;3 in per year</td></tr>
      <tr><td>6&ndash;10 years</td><td>24&ndash;30 in</td><td>0.5&ndash;1.5 in per year</td></tr>
      <tr><td>10 years+</td><td>28&ndash;36 in</td><td>Very slow; frame is essentially set</td></tr>
    </table>
    <p>In a temperate climate the growing season is roughly six months long &mdash; koi put on almost nothing between October and April. Heated indoor systems compress the same growth into a shorter calendar, which is how dealers produce large young fish.</p>

    <h2 id="what-controls-size">What Actually Controls Final Size</h2>
    <ul>
      <li><strong>Genetics.</strong> The strongest single factor. A domestic koi from a small-framed line will not reach jumbo size no matter how it is kept.</li>
      <li><strong>Water volume and quality.</strong> Growth stalls in water carrying nitrate and growth-inhibiting hormones. Regular water changes are a growth technique, not just a health one.</li>
      <li><strong>Temperature and season length.</strong> More days in the 68&ndash;77&deg;F band means more growth days per year.</li>
      <li><strong>Feed quality and frequency.</strong> High-protein food several times a day during the growing season, matched with filtration that can carry the load.</li>
      <li><strong>Stocking density.</strong> Crowded koi grow slowly and unevenly, even with good water readings.</li>
      <li><strong>Oxygen.</strong> Dissolved oxygen below 6 mg/L caps appetite and therefore growth.</li>
    </ul>

    <h2 id="tank-size-myth">Do Koi Only Grow to the Size of Their Tank?</h2>
    <p>No &mdash; this is the most persistent myth in the hobby, and it is dangerous because it is half true. A koi in a small tank does stay smaller, but not because it politely stops growing. Confined water accumulates nitrate and growth-inhibiting pheromones, which suppress the fish's development while its internal organs continue to grow. The result is a stunted koi with a shortened lifespan, not a conveniently small one.</p>
    <div class="callout callout-warn"><strong>Practical consequence:</strong> a 55-gallon aquarium is a nursery for juvenile koi, never a permanent home. Plan the move to a pond of at least 250&ndash;500 gallons per fish before the koi passes about 8 inches. See the <a href="/guides/koi-fish-tank/">koi fish tank guide</a> for the indoor option and its limits.</div>

    <h2 id="measuring">Measuring and Tracking Growth</h2>
    <p>Measure nose to the fork of the tail (or nose to tail tip, but be consistent). Photograph each koi against a marked bowl once a season; growth over a single month is too small to see by eye and easy to imagine. Weigh larger koi in a water-filled bowl on a bathroom scale &mdash; weigh the bowl, add the fish, subtract.</p>
    <p>A koi that stops growing while others in the same pond continue is worth investigating: check for gill flukes, an unnoticed injury, or simple competition at feeding time.</p>
"""

SIZE = {
    "slug": "size-growth",
    "title": "How Big Do Koi Fish Get? Size Chart & Growth Rate by Age | FishCare AI",
    "meta_desc": "Koi fish reach 24-36 inches. Year-by-year koi growth rate chart, what controls final size, typical sizes by type, and why koi do not simply grow to the size of their tank.",
    "h1": "Koi Fish Size and Growth Rate",
    "hero_tag": "Size & Growth",
    "hero_meta": "\U0001F4CF 24&ndash;36 in adult &nbsp;|&nbsp; \U0001F4C8 5&ndash;8 in in year one &nbsp;|&nbsp; \U0001F553 Full size at 6&ndash;10 years",
    "date": "2026-09-08",
    "toc_sections": [
        ("how-big", "How Big Koi Get"),
        ("growth-rate", "Growth Rate by Age"),
        ("what-controls-size", "What Controls Size"),
        ("tank-size-myth", "The Tank Size Myth"),
        ("measuring", "Tracking Growth"),
    ],
    "body": SIZE_BODY,
    "faqs": [
        ("How big do koi fish get?",
         "Adult koi reach 24-36 inches (60-90 cm). Domestic koi commonly top out at 18-24 inches, Japanese-bred koi reach 26-32 inches, and jumbo bloodlines in large ponds can pass 36 inches and 30 pounds."),
        ("How fast do koi fish grow?",
         "Koi grow 5-8 inches in their first year, 4-6 inches in the second, and 3-5 inches in the third, then slow to 1-3 inches a year. Most of a koi's frame is set by age six, with slow growth continuing for years afterwards."),
        ("Do koi only grow to the size of their tank?",
         "No. A koi in a small tank stays smaller because accumulated nitrate and growth-inhibiting hormones suppress development while internal organs keep growing. The fish is stunted and shorter-lived, not naturally sized to the tank."),
        ("How big do koi get in the first year?",
         "A well-fed koi in good water reaches 5-8 inches by its first birthday, having started at about a quarter inch at hatching. Growth is fastest during the summer months and effectively stops below 50F."),
        ("How can I make my koi grow bigger?",
         "Give them volume and clean water first: frequent water changes, dissolved oxygen above 6 mg/L, and low stocking density. Then feed a 32-40% protein food several times a day through the 68-77F growing season. Genetics sets the ceiling."),
    ],
    "related": [
        ("/guides/koi-fish-care/lifespan/", "Koi Fish Lifespan"),
        ("/calculators/koi-fish-tank-size/", "Koi Pond Size Calculator"),
        ("/guides/koi-fish-care/feeding/", "Koi Feeding Chart"),
        ("/guides/koi-fish-tank/", "Koi Fish Tank Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 5 — Lifespan
# ────────────────────────────────────────────────────────────────
LIFESPAN_BODY = """    <p>Koi are a multi-decade commitment. A koi bought as a hand-sized juvenile can reasonably be expected to outlive the pond it was bought for, and in many cases to outlive the keeper's interest in ponds. That is worth knowing before the first fish goes in.</p>

    <h2 id="how-long">How Long Do Koi Fish Live?</h2>
    <p>Well-kept koi live <strong>25&ndash;35 years</strong>. In average garden ponds with variable water quality, 15&ndash;20 years is more typical. Japanese koi from strong bloodlines in mud ponds are regularly documented past 40, and a handful of individual fish have credible records beyond 50.</p>
    <table class="ptbl">
      <tr><th>Conditions</th><th>Typical lifespan</th></tr>
      <tr><td>Small, unfiltered pond; irregular maintenance</td><td>5&ndash;10 years</td></tr>
      <tr><td>Average garden pond; adequate filtration</td><td>15&ndash;20 years</td></tr>
      <tr><td>Well-managed pond; stable water, low density</td><td>25&ndash;35 years</td></tr>
      <tr><td>Japanese bloodlines in optimal conditions</td><td>40&ndash;50+ years</td></tr>
      <tr><td>Indoor aquarium (long-term)</td><td>Usually under 10 years &mdash; stunting shortens life</td></tr>
    </table>
    <p>The famous scarlet koi Hanako, from Gifu Prefecture in Japan, was claimed to have lived 226 years based on growth rings read from a scale in 1966. The figure is widely repeated and cannot be independently verified; treat it as folklore rather than a benchmark.</p>

    <h2 id="what-determines">What Determines Koi Lifespan</h2>
    <ul>
      <li><strong>Water quality above all.</strong> Chronic low-level ammonia and nitrate exposure shortens life without ever producing a visible crisis. Regular water changes are the single highest-value habit.</li>
      <li><strong>Pond volume and depth.</strong> Larger, deeper water swings less in temperature and chemistry. Stunted koi in undersized systems rarely pass 10 years.</li>
      <li><strong>Winter management.</strong> Koi overwinter safely in cold water, but only if oxygen exchange continues and they were not fed into the cold. A single bad winter can end a decade-old fish.</li>
      <li><strong>Genetics.</strong> Japanese bloodlines were selected over generations for longevity as well as pattern; mass-produced fish frequently are not.</li>
      <li><strong>Disease exposure.</strong> One unquarantined new fish carrying koi herpes virus can end an entire pond. A 3&ndash;4 week quarantine is the cheapest life extension available.</li>
      <li><strong>Predation and accidents.</strong> Herons, raccoons, and koi jumping from an uncovered pond account for more losses than disease in many gardens.</li>
    </ul>

    <h2 id="age-signs">Telling a Koi's Age</h2>
    <p>There is no reliable non-invasive way to age a living koi. Size is only a rough proxy because growth rate varies so much with conditions &mdash; an 18-inch koi might be three years old in a well-run pond or eight in a cold, crowded one. Scale growth rings can be read under magnification, the method used for the Hanako claim, but require removing a scale and are interpreted differently by different readers.</p>
    <p>Practical markers of an older koi: colour that has softened or shifted, a thicker body relative to length, slower feeding response, and in females a heavier abdomen year-round. Keep a dated photo record instead &mdash; it is the only age documentation you will ever trust.</p>

    <h2 id="extending-life">Getting the Full 30 Years</h2>
    <ol>
      <li><strong>Build once, correctly.</strong> 500 gallons per adult koi, 4 feet deep, bottom drain, generous biological filtration.</li>
      <li><strong>Change water on a schedule</strong> &mdash; 10&ndash;20% weekly &mdash; rather than in response to problems.</li>
      <li><strong>Quarantine every new fish</strong> for 3&ndash;4 weeks in a separate system at 65&ndash;75&deg;F.</li>
      <li><strong>Feed to the thermometer</strong>, and stop entirely below 50&deg;F.</li>
      <li><strong>Run aeration year-round</strong>, and add capacity before summer heat rather than during it.</li>
      <li><strong>Net or cover the pond</strong> against herons and against koi jumping during spawning season.</li>
      <li><strong>Act on the first symptom.</strong> Flashing, clamped fins or an ulcer treated in week one is routine; the same problem in week four often is not.</li>
    </ol>
"""

LIFESPAN = {
    "slug": "lifespan",
    "title": "How Long Do Koi Fish Live? Koi Lifespan by Conditions | FishCare AI",
    "meta_desc": "Koi fish live 25-35 years in a well-managed pond and 15-20 years in an average one, with Japanese bloodlines passing 40. What determines koi lifespan and how to extend it.",
    "h1": "Koi Fish Lifespan: How Long Do Koi Live?",
    "hero_tag": "Lifespan",
    "hero_meta": "⏳ 25&ndash;35 years typical &nbsp;|&nbsp; \U0001F1EF\U0001F1F5 40+ in Japan &nbsp;|&nbsp; \U0001F4A7 Water quality decides",
    "date": "2026-09-08",
    "toc_sections": [
        ("how-long", "How Long Koi Live"),
        ("what-determines", "What Determines Lifespan"),
        ("age-signs", "Telling a Koi's Age"),
        ("extending-life", "Getting 30 Years"),
    ],
    "body": LIFESPAN_BODY,
    "faqs": [
        ("How long do koi fish live?",
         "Well-kept koi live 25-35 years. In average garden ponds 15-20 years is more typical, while Japanese bloodlines in optimal conditions are regularly documented past 40 years."),
        ("What is the oldest koi fish ever?",
         "A scarlet koi named Hanako, from Gifu Prefecture in Japan, was claimed in 1966 to be 226 years old based on growth rings read from one of her scales. The claim cannot be independently verified and is best treated as folklore."),
        ("How long do koi live in a tank?",
         "Koi kept permanently in an aquarium usually live under 10 years. Confined water accumulates nitrate and growth-inhibiting hormones that stunt the fish while its organs keep developing, which shortens life substantially."),
        ("Why did my koi die suddenly?",
         "The most common causes are an oxygen crash on a warm night, an ammonia or nitrite spike after a filter or pump failure, koi herpes virus introduced by an unquarantined fish, and predation. Test the water immediately - readings change within a day or two of a death."),
        ("How can I tell how old my koi is?",
         "There is no reliable non-invasive method. Size is only a rough guide because growth rate varies enormously with conditions. Scale growth rings can be read under magnification but require removing a scale. Keeping dated photographs is the practical alternative."),
    ],
    "related": [
        ("/guides/koi-fish-care/size-growth/", "Koi Size & Growth Rate"),
        ("/guides/koi-fish-care/diseases/", "Koi Diseases & Symptoms"),
        ("/wiki/koi/", "Koi Species Profile"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 6 — Types, Varieties & Colors
# ────────────────────────────────────────────────────────────────
TYPES_BODY = """    <p>Every koi is the same species &mdash; <em>Cyprinus rubrofuscus</em>, the Amur carp &mdash; and every named type is a selectively bred colour variety, not a separate fish. Japanese breeders group these varieties into about 16 recognised classes, collectively called Nishikigoi. Knowing the class names makes buying far easier, because price tracks pattern quality within a class rather than colour alone.</p>

    <h2 id="gosanke">The Big Three (Gosanke)</h2>
    <p>Three varieties dominate shows and account for most of the koi sold worldwide.</p>
    <table class="ptbl">
      <tr><th>Variety</th><th>Pattern</th><th>What judges look for</th></tr>
      <tr><td>Kohaku</td><td>White body with red (hi) markings</td><td>Snow-white base, deep even red, crisp pattern edges, no red on the head below the eyes</td></tr>
      <tr><td>Taisho Sanke (Sanke)</td><td>White body, red markings, small black (sumi) accents</td><td>Black confined above the lateral line, used sparingly to balance the red</td></tr>
      <tr><td>Showa Sanshoku (Showa)</td><td>Black body with red and white markings</td><td>Wrapping black that runs through the head and into the pectoral fin joints</td></tr>
    </table>
    <p>The quickest way to tell a Sanke from a Showa: Sanke is a white fish with black added, Showa is a black fish with white and red added. Look at the head &mdash; Showa carries black on it, Sanke almost never does.</p>

    <h2 id="main-varieties">Main Koi Varieties</h2>
    <ul>
      <li><strong>Utsurimono</strong> &mdash; black koi with a single second colour: Shiro Utsuri (white), Hi Utsuri (red), Ki Utsuri (yellow).</li>
      <li><strong>Bekko</strong> &mdash; solid base colour with black stepping-stone markings: Shiro, Aka and Ki Bekko.</li>
      <li><strong>Asagi</strong> &mdash; blue-grey net-patterned scales along the back with red on the flanks, belly and fin bases. One of the oldest varieties.</li>
      <li><strong>Shusui</strong> &mdash; the scaleless (Doitsu) version of Asagi, with a single row of dark scales along the dorsal line.</li>
      <li><strong>Tancho</strong> &mdash; any variety with a single red spot on the head and no other red; Tancho Kohaku is the classic.</li>
      <li><strong>Ogon / Hikarimuji</strong> &mdash; single-colour metallic koi: Yamabuki (yellow gold), Platinum (white), Orenji (orange).</li>
      <li><strong>Hikari Moyo</strong> &mdash; multi-coloured metallics, including Kujaku (metallic with net pattern and red markings).</li>
      <li><strong>Kumonryu</strong> &mdash; scaleless black-and-white koi whose pattern shifts with the seasons and can change entirely from year to year.</li>
      <li><strong>Chagoi</strong> &mdash; plain brown or bronze, famously the tamest and fastest-growing variety; often bought deliberately to settle a nervous pond.</li>
      <li><strong>Ochiba Shigure</strong> &mdash; blue-grey body with copper or bronze markings, described as autumn leaves on water.</li>
      <li><strong>Goshiki</strong> &mdash; five-colour koi, a Kohaku pattern over a netted blue-grey base.</li>
      <li><strong>Koromo</strong> &mdash; Kohaku pattern where each red scale carries a blue or black reticulated edge.</li>
      <li><strong>Doitsu</strong> &mdash; not a colour class but a scale type: German mirror carp genetics giving a scaleless body with large scales along the lateral and dorsal lines. Any variety can be Doitsu.</li>
      <li><strong>Ginrin</strong> &mdash; a scale finish, not a colour: individual scales sparkle. Also crosses every variety.</li>
    </ul>

    <h2 id="colors">Koi Fish Colours: Black, White, Blue</h2>
    <p>Searches for a colour usually map onto a specific named variety:</p>
    <table class="ptbl">
      <tr><th>Colour wanted</th><th>Varieties to ask for</th></tr>
      <tr><td>Black koi</td><td>Karasugoi (solid black), Kumonryu (black and white), Shiro Utsuri (black and white), Matsuba (black netting over a base colour)</td></tr>
      <tr><td>White koi</td><td>Platinum Ogon (solid metallic white), Shiro Utsuri, Shiro Bekko</td></tr>
      <tr><td>Blue koi</td><td>Asagi, Shusui, Soragoi (solid blue-grey), Ai Goromo (blue-edged red scales)</td></tr>
      <tr><td>Yellow / gold koi</td><td>Yamabuki Ogon, Ki Utsuri, Ki Bekko</td></tr>
      <tr><td>Orange / red koi</td><td>Orenji Ogon, Benigoi (solid red), Hi Utsuri</td></tr>
      <tr><td>Brown / bronze koi</td><td>Chagoi, Ochiba Shigure</td></tr>
    </table>
    <div class="callout"><strong>Colour is not fixed.</strong> Koi patterns develop for the first three to four years and continue to shift afterwards. Red can spread or recede, black often deepens with age, and metallics dull in poor water. Kumonryu changes pattern seasonally as a matter of course. Buying a young koi is always partly a bet.</div>

    <h2 id="butterfly-koi">Butterfly Koi</h2>
    <p>Butterfly koi &mdash; also called longfin or dragon koi &mdash; are ordinary koi carrying a longfin gene, developed in the United States from a cross with Indonesian longfin carp. Fins, barbels and tail grow long and flowing.</p>
    <ul>
      <li>Same body length as standard koi (24&ndash;36 in), so the same pond requirements apply.</li>
      <li>They are <strong>not recognised in traditional Japanese show classes</strong>, though many Western shows now judge them separately.</li>
      <li>The long fins are more prone to catching on rough hardscape and to fin rot in poor water.</li>
      <li>They read as slower and more graceful in the water, which is why they are popular in viewing ponds.</li>
    </ul>

    <h2 id="ghost-koi">Ghost Koi</h2>
    <p>Ghost koi are a hybrid of a metallic Ogon koi with a wild or mirror carp, first bred in the UK in the 1980s. They show a metallic sheen &mdash; usually silver or gold &mdash; over a darker, plainer body.</p>
    <ul>
      <li><strong>Hardy and fast-growing</strong> thanks to hybrid vigour; often the survivors in a difficult pond.</li>
      <li><strong>Larger appetite and stronger foraging instinct</strong> than most ornamental koi, which can mean uprooted pond plants.</li>
      <li><strong>Not Nishikigoi</strong> and not shown in koi classes; they are also usually far cheaper.</li>
      <li>Sometimes sold as pest fish for large ponds where colour matters less than resilience.</li>
    </ul>

    <h2 id="buying">Choosing a Koi</h2>
    <ol>
      <li><strong>Watch it swim before you look at the pattern.</strong> Body shape, straight spine and confident swimming outrank colour every time.</li>
      <li><strong>Check the skin</strong> for ulcers, raised scales, red streaks in fins, and the gill covers for rapid or one-sided movement.</li>
      <li><strong>Expect the pattern to change.</strong> Buy the koi you like now; do not pay a premium for what a young fish might become.</li>
      <li><strong>Buy from one source where possible</strong> and quarantine everything for 3&ndash;4 weeks regardless of the seller's reputation.</li>
      <li><strong>Add a Chagoi.</strong> They tame quickly and the rest of the pond follows them to the surface at feeding time.</li>
    </ol>
"""

TYPES = {
    "slug": "types",
    "title": "Types of Koi Fish: Varieties, Colors, Butterfly & Ghost Koi | FishCare AI",
    "meta_desc": "A guide to koi fish varieties: Kohaku, Sanke, Showa and the other Nishikigoi classes, which varieties give black, white and blue koi, plus butterfly koi and ghost koi explained.",
    "h1": "Types of Koi Fish: Varieties and Colours",
    "hero_tag": "Types & Varieties",
    "hero_meta": "\U0001F3A8 16 recognised classes &nbsp;|&nbsp; \U0001F947 Gosanke: Kohaku, Sanke, Showa &nbsp;|&nbsp; \U0001F98B Butterfly & ghost koi",
    "date": "2026-09-08",
    "toc_sections": [
        ("gosanke", "The Big Three"),
        ("main-varieties", "Main Varieties"),
        ("colors", "Koi Colours"),
        ("butterfly-koi", "Butterfly Koi"),
        ("ghost-koi", "Ghost Koi"),
        ("buying", "Choosing a Koi"),
    ],
    "body": TYPES_BODY,
    "faqs": [
        ("What are the main types of koi fish?",
         "Japanese breeders recognise about 16 varieties of Nishikigoi. The three most important are the Gosanke: Kohaku (white with red), Taisho Sanke (white with red and black) and Showa Sanshoku (black with red and white). Other common classes include Utsurimono, Bekko, Asagi, Shusui, Tancho, Ogon, Kumonryu and Chagoi."),
        ("What is a butterfly koi?",
         "Butterfly koi, also called longfin or dragon koi, are standard koi carrying a longfin gene developed in the United States from a cross with Indonesian longfin carp. They reach the same 24-36 inch body length as ordinary koi and are not recognised in traditional Japanese show classes."),
        ("What is a ghost koi?",
         "Ghost koi are a hybrid of a metallic Ogon koi with a wild or mirror carp, first bred in the UK in the 1980s. They are hardy, fast-growing and cheaper than Nishikigoi, with a metallic silver or gold sheen over a plainer body, but they are not shown as koi."),
        ("What is a black koi fish called?",
         "A solid black koi is a Karasugoi. Black-and-white varieties include Kumonryu (scaleless, pattern changes with the seasons) and Shiro Utsuri. Matsuba koi carry black netting over a base colour."),
        ("Do koi fish change colour as they grow?",
         "Yes. Koi patterns develop over the first three to four years and keep shifting afterwards - red can spread or recede, black usually deepens with age, and metallic finishes dull in poor water. Kumonryu change pattern seasonally as a matter of course."),
    ],
    "related": [
        ("/wiki/koi/", "Koi Species Profile"),
        ("/guides/koi-fish-care/size-growth/", "Koi Size & Growth Rate"),
        ("/guides/koi-fish-care/male-vs-female/", "Male vs Female Koi"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 7 — Male vs Female
# ────────────────────────────────────────────────────────────────
MVF_BODY = """    <p>Koi show no reliable external sex differences until they are sexually mature &mdash; around <strong>three years old and 10&ndash;12 inches long</strong>. Anyone selling you a sexed 4-inch koi is guessing. Once the fish are mature, four indicators taken together will usually get you there.</p>

    <h2 id="body-shape">Body Shape</h2>
    <p>The clearest everyday indicator. Viewed from above, a mature <strong>female</strong> is noticeably wider through the belly and shoulders, giving a rounded, full outline that becomes pronounced in spring as she fills with eggs. A mature <strong>male</strong> is slimmer and more torpedo-shaped, holding roughly the same width from head to tail.</p>
    <div class="callout"><strong>Caution:</strong> an overfed male can look rounded, and a female outside spawning season can look slim. Always read body shape alongside at least one other indicator, and always look from directly above rather than from the side.</div>

    <h2 id="pectoral-fins">Pectoral Fins</h2>
    <table class="ptbl">
      <tr><th>Feature</th><th>Male</th><th>Female</th></tr>
      <tr><td>Fin shape</td><td>Pointed, triangular, more rigid</td><td>Rounded, softer outline</td></tr>
      <tr><td>Fin colour</td><td>Solid, more opaque and intense</td><td>Often translucent with visible rays</td></tr>
      <tr><td>Fin size relative to body</td><td>Proportionally larger</td><td>Proportionally smaller</td></tr>
    </table>
    <p>Fin shape is more reliable than fin colour, and neither is conclusive alone.</p>

    <h2 id="tubercles">Breeding Tubercles</h2>
    <p>The one genuinely definitive sign, but seasonal. In the run-up to spawning, mature <strong>males</strong> develop small white raised bumps &mdash; breeding tubercles &mdash; on the gill plates and along the leading rays of the pectoral fins. They feel like fine sandpaper.</p>
    <div class="callout callout-warn"><strong>Do not confuse tubercles with ich.</strong> Ich (white spot) appears as scattered white grains across the whole body and fins, on fish of either sex, at any time of year, usually with flashing and clamped fins. Tubercles are confined to gill covers and pectoral fins, appear only on mature males in spring, and come with no other symptoms. See the <a href="/guides/koi-fish-care/diseases/">koi disease guide</a> if in doubt.</div>

    <h2 id="vent">Vent Shape</h2>
    <p>The most accurate indicator outside the breeding season, but it requires handling the fish. With the koi supported in a water-filled bowl or sock net, look at the vent just forward of the anal fin:</p>
    <ul>
      <li><strong>Female:</strong> larger, oval, slightly protruding or convex, and often pinker &mdash; markedly so when gravid.</li>
      <li><strong>Male:</strong> smaller, narrower, flat or slightly concave.</li>
    </ul>
    <p>Handle with wet hands or a soft net, keep the fish in water where possible, support the body fully, and put it back quickly. Do not attempt this on a koi that is already stressed or unwell.</p>

    <h2 id="behaviour">Spawning Behaviour</h2>
    <p>In late spring, once the water passes about 65&deg;F, males chase and nudge females persistently along the flanks, driving them into shallow water and plants. If you have a pond of chasing fish and one or two being chased, the chasers are the males. It is the easiest sexing you will ever do &mdash; and also the point at which females can be injured, so watch for scale damage and provide plant cover or a spawning brush.</p>

    <h2 id="which-to-keep">Does It Matter Which You Keep?</h2>
    <table class="ptbl">
      <tr><th>Consideration</th><th>Practical effect</th></tr>
      <tr><td>Size</td><td>Females typically grow larger and heavier; most jumbo show koi are female</td></tr>
      <tr><td>Show quality</td><td>Females often carry better skin and body volume; males sometimes hold sharper pattern edges</td></tr>
      <tr><td>Spawning disruption</td><td>A mixed pond will spawn most springs: fouled water, exhausted females, and thousands of fry</td></tr>
      <tr><td>All-male pond</td><td>No spawning, no fry, less spring chaos &mdash; but no offspring either</td></tr>
      <tr><td>Ratio if breeding</td><td>Two or three males per female is the usual working ratio</td></tr>
    </table>
    <p>Most keepers end up with whatever they bought and manage the spring spawn rather than sexing their stock. If you want to avoid spawning entirely, buying koi from a single sex is the only reliable route &mdash; and it means buying mature, sexed fish rather than juveniles.</p>
"""

MVF = {
    "slug": "male-vs-female",
    "title": "Male vs Female Koi Fish: How to Tell the Difference | FishCare AI",
    "meta_desc": "How to sex koi fish: body shape, pectoral fin shape, breeding tubercles and vent shape compared. Koi cannot be reliably sexed until about three years old and 10-12 inches.",
    "h1": "Male vs Female Koi Fish",
    "hero_tag": "Male vs Female",
    "hero_meta": "♀♂ Sexable from ~3 years &nbsp;|&nbsp; \U0001F50D 4 indicators &nbsp;|&nbsp; \U0001F338 Tubercles in spring",
    "date": "2026-09-08",
    "toc_sections": [
        ("body-shape", "Body Shape"),
        ("pectoral-fins", "Pectoral Fins"),
        ("tubercles", "Breeding Tubercles"),
        ("vent", "Vent Shape"),
        ("behaviour", "Spawning Behaviour"),
        ("which-to-keep", "Which to Keep"),
    ],
    "body": MVF_BODY,
    "faqs": [
        ("How can you tell if a koi is male or female?",
         "Use four indicators together on a mature fish: females are wider and rounder viewed from above, males have more pointed and solid-coloured pectoral fins, mature males develop white breeding tubercles on the gill plates and pectoral fins in spring, and the female vent is larger, oval and slightly protruding while the male vent is small and flat."),
        ("At what age can you tell a koi's gender?",
         "Not before about three years old and 10-12 inches in length. Juvenile koi show no reliable external sex differences, so any sexing of small fish is guesswork."),
        ("Do male koi have white spots?",
         "Mature male koi develop small white raised bumps called breeding tubercles on the gill covers and pectoral fins during spring spawning season. These are confined to those areas and appear without other symptoms. Ich, by contrast, scatters white grains across the whole body and comes with flashing and clamped fins."),
        ("Do female koi grow bigger than males?",
         "Generally yes. Female koi typically grow longer and heavier than males, and most jumbo show koi are female."),
        ("Should I keep male or female koi?",
         "A single-sex pond avoids the spring spawn, which fouls water, exhausts females and produces thousands of fry. Doing so means buying mature sexed adults rather than juveniles. Most keepers keep a mixed pond and simply manage the spawn."),
    ],
    "related": [
        ("/guides/koi-fish-care/breeding/", "Koi Breeding & Eggs"),
        ("/guides/koi-fish-care/types/", "Types of Koi Fish"),
        ("/guides/koi-fish-care/size-growth/", "Koi Size & Growth"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 8 — Breeding, Eggs & Fry
# ────────────────────────────────────────────────────────────────
BREEDING_BODY = """    <p>Koi will spawn in almost any pond that gets warm enough, whether you planned it or not. The question for most keepers is not how to make it happen but how to manage it &mdash; a spawn dumps enormous amounts of milt and egg protein into the water and can crash the pond in a day.</p>

    <div class="callout"><strong>Koi are not livebearers.</strong> There is no such thing as a pregnant koi fish. A female heavy with eggs is <em>gravid</em> &mdash; she is carrying eggs she will scatter, not developing young. A koi that stays swollen after spawning season, or is swollen with raised scales, has a health problem rather than eggs: see <a href="/guides/koi-fish-care/diseases/">koi diseases</a>.</div>

    <h2 id="when">When Koi Spawn</h2>
    <p>Koi spawn in <strong>late spring to early summer</strong>, triggered by water warming through <strong>65&ndash;75&deg;F (18&ndash;24&deg;C)</strong> and by lengthening daylight. Fish must be sexually mature &mdash; typically three years old and 10&ndash;12 inches. Spawning usually happens at dawn, and the whole event lasts a few hours.</p>
    <p>The signs are unmistakable: males chase a female relentlessly, nudging her flanks and pushing her into shallow water and plant cover; the water turns cloudy and foamy; and eggs appear as tiny sticky beads on plants, brushes and liner walls.</p>

    <h2 id="conditioning">Conditioning Breeders</h2>
    <ul>
      <li>Select healthy adults, at least three years old, with good body shape. Use two or three males per female.</li>
      <li>Raise feeding through spring &mdash; high-protein food two or three times daily once water passes 60&deg;F.</li>
      <li>Keep water quality tight; ammonia and nitrite must read 0 ppm before a spawn, because they will spike after one.</li>
      <li>Provide spawning media: spawning brushes, ropes, or dense soft plants such as hornwort and water hyacinth roots.</li>
    </ul>

    <h2 id="eggs">Koi Fish Eggs</h2>
    <table class="ptbl">
      <tr><th>Detail</th><th>Figure</th></tr>
      <tr><td>Eggs per spawn</td><td>Roughly 50,000&ndash;100,000 for a large female (about 100,000 per kg of body weight)</td></tr>
      <tr><td>Egg size</td><td>1&ndash;2 mm, sticky, translucent amber</td></tr>
      <tr><td>Hatching time</td><td>3&ndash;7 days; about 4 days at 68&deg;F, faster in warmer water</td></tr>
      <tr><td>Fertile vs infertile</td><td>Fertile eggs stay clear or amber; infertile eggs turn opaque white and fungus within 24&ndash;48 hours</td></tr>
      <tr><td>Survival to adulthood</td><td>Very low in a stocked pond &mdash; adults eat most eggs and fry</td></tr>
    </table>
    <p>If you want fry, move the spawning media with eggs attached to a separate tank of pond water within a few hours. Remove white fungused eggs daily; they spread fungus to healthy neighbours. If you do not want fry, leaving the eggs in the pond is usually enough &mdash; the adults will eat them.</p>

    <h2 id="after-spawn">Managing the Pond After a Spawn</h2>
    <p>This is the part that catches people out. A heavy spawn puts a large protein load into the water and strips oxygen at the same time.</p>
    <ol>
      <li><strong>Do a 30&ndash;50% water change</strong> as soon as spawning ends.</li>
      <li><strong>Increase aeration immediately</strong> &mdash; foam on the surface is a sign that oxygen exchange is being blocked.</li>
      <li><strong>Clean skimmers and mechanical media,</strong> which will be loaded with egg debris.</li>
      <li><strong>Test ammonia daily for a week.</strong> Post-spawn ammonia spikes are common even in well-filtered ponds.</li>
      <li><strong>Check females for damage.</strong> Chasing scrapes scales and tears fins; treat injuries and watch for secondary infection.</li>
      <li><strong>Do not feed heavily for a couple of days</strong> while the filter catches up.</li>
    </ol>

    <h2 id="fry">Baby Koi Fish: Raising Fry</h2>
    <table class="ptbl">
      <tr><th>Stage</th><th>Age</th><th>Care</th></tr>
      <tr><td>Hatch</td><td>Day 0</td><td>Fry hang on surfaces absorbing the yolk sac; do not feed</td></tr>
      <tr><td>Free-swimming</td><td>Day 2&ndash;4</td><td>Start feeding: infusoria, liquid fry food, then newly hatched brine shrimp</td></tr>
      <tr><td>Early growth</td><td>Week 2&ndash;6</td><td>Powdered fry food several times daily; gentle sponge filtration only</td></tr>
      <tr><td>Crumble stage</td><td>Month 2&ndash;3</td><td>Move to crushed pellets; fry reach 1&ndash;2 inches</td></tr>
      <tr><td>Colouring up</td><td>Month 6 &ndash; year 3</td><td>Pattern develops gradually; final quality is not clear until year three or four</td></tr>
    </table>
    <p>Two realities worth knowing before you raise a spawn. First, <strong>most fry are brown</strong>. Wild carp colouring is dominant, and typically only a small percentage of any spawn shows worthwhile koi pattern. Second, <strong>culling is part of the practice</strong> &mdash; breeders select repeatedly and cannot keep tens of thousands of fish. If you are not prepared to rehome or humanely cull, do not collect the eggs; let the pond handle it.</p>
    <p>Fry need a sponge filter rather than a powered intake (which will draw them in), 25&ndash;30% water changes several times a week, and generous space &mdash; overcrowded fry stunt permanently.</p>
"""

BREEDING = {
    "slug": "breeding",
    "title": "Koi Breeding: Spawning, Eggs and Raising Baby Koi | FishCare AI",
    "meta_desc": "How koi spawn at 65-75F, how many eggs a female scatters, hatching times, managing the ammonia spike after a spawn, and raising baby koi fry to colouring up.",
    "h1": "Koi Breeding, Eggs and Baby Koi",
    "hero_tag": "Breeding & Eggs",
    "hero_meta": "\U0001F337 Spawns at 65&ndash;75&deg;F &nbsp;|&nbsp; \U0001F95A 50,000&ndash;100,000 eggs &nbsp;|&nbsp; ⏱️ Hatch in 3&ndash;7 days",
    "date": "2026-09-08",
    "toc_sections": [
        ("when", "When Koi Spawn"),
        ("conditioning", "Conditioning Breeders"),
        ("eggs", "Koi Fish Eggs"),
        ("after-spawn", "After the Spawn"),
        ("fry", "Raising Baby Koi"),
    ],
    "body": BREEDING_BODY,
    "faqs": [
        ("Can koi fish get pregnant?",
         "No. Koi are egg scatterers, not livebearers, so there is no pregnant koi. A female swollen in spring is gravid - carrying eggs she will release during spawning. A koi that stays swollen outside spawning season, especially with raised scales, has a health problem such as dropsy."),
        ("When do koi fish spawn?",
         "Koi spawn in late spring to early summer, triggered when water warms through 65-75F (18-24C) and daylight lengthens. Spawning usually happens at dawn and is over within a few hours."),
        ("How many eggs do koi fish lay?",
         "A large female scatters roughly 50,000 to 100,000 eggs in a single spawn, about 100,000 per kilogram of body weight. Survival to adulthood in a stocked pond is very low because the adults eat most eggs and fry."),
        ("How long do koi eggs take to hatch?",
         "Three to seven days depending on temperature - about four days at 68F. Fertile eggs stay clear or amber; infertile ones turn opaque white and fungus within a day or two and should be removed."),
        ("What do baby koi fish eat?",
         "Newly hatched fry live on their yolk sac for two to four days, then take infusoria or liquid fry food, followed by newly hatched brine shrimp and powdered fry food. From about two months they move on to crushed pellets."),
        ("Why are my baby koi brown?",
         "Wild carp colouring is dominant, so most koi fry are brown or grey. Only a small proportion of any spawn develops worthwhile koi pattern, and final quality is not clear until the fish are three or four years old."),
    ],
    "related": [
        ("/guides/koi-fish-care/male-vs-female/", "Male vs Female Koi"),
        ("/guides/koi-fish-care/water-parameters/", "Koi Water Parameters"),
        ("/guides/koi-fish-care/types/", "Types of Koi Fish"),
        ("/guides/koi-fish-care/", "Koi Fish Care Guide"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 9 — Diseases, Parasites & Symptoms
# ────────────────────────────────────────────────────────────────
DISEASES_BODY = """    <p>Almost every koi disease starts with a water quality problem or a fish added without quarantine. Before you treat anything, test ammonia, nitrite, pH and temperature &mdash; a large proportion of the symptoms below resolve on water changes alone, and medicating a pond whose real problem is ammonia makes things worse.</p>
    <div class="callout callout-warn"><strong>This page is an orientation guide, not a substitute for diagnosis.</strong> Persistent ulcers, mass mortality or unexplained deaths warrant a consultation with an aquatic veterinarian, and some conditions (koi herpes virus, spring viraemia of carp) are notifiable in certain countries.</div>

    <h2 id="symptom-index">Symptom Index</h2>
    <table class="ptbl">
      <tr><th>What you see</th><th>Most likely causes</th><th>First action</th></tr>
      <tr><td>Flashing &mdash; rubbing or scraping against the pond floor</td><td>Skin or gill parasites; high ammonia, nitrite or chlorine</td><td>Test water; then scrape/scope for parasites</td></tr>
      <tr><td>White grains over body and fins</td><td>Ich (white spot)</td><td>Salt at 0.3% plus temperature management</td></tr>
      <tr><td>Lying on the bottom, barely moving</td><td>Cold-water torpor (normal); low oxygen; ammonia; parasites; KHV</td><td>Check temperature and oxygen first</td></tr>
      <tr><td>Gasping at the surface, crowding the waterfall</td><td>Low dissolved oxygen; gill damage</td><td>Add aeration immediately, water change</td></tr>
      <tr><td>Not eating</td><td>Water below 50&deg;F (normal); water quality; stress; illness</td><td>Check thermometer, then test water</td></tr>
      <tr><td>Ragged, receding fins with white or red edges</td><td>Fin rot (bacterial, secondary to poor water)</td><td>Water changes; salt; antibacterial if progressing</td></tr>
      <tr><td>Red sores or open ulcers on the flank</td><td>Aeromonas / Pseudomonas ulcer disease</td><td>Isolate, topical treatment, vet consult</td></tr>
      <tr><td>Body swollen, scales sticking out like a pinecone</td><td>Dropsy &mdash; internal organ failure, often terminal</td><td>Isolate; prognosis poor</td></tr>
      <tr><td>Cotton-wool tufts on skin</td><td>Fungus (Saprolegnia), always secondary to injury</td><td>Treat the underlying wound and water quality</td></tr>
      <tr><td>Thread-like growths with two barbs at the attachment</td><td>Anchor worm (Lernaea)</td><td>Manual removal plus a licensed parasiticide</td></tr>
      <tr><td>Flat disc-shaped creature moving on the skin</td><td>Fish louse (Argulus)</td><td>Manual removal plus a licensed parasiticide</td></tr>
      <tr><td>Rapid or one-sided gill movement, gills held open</td><td>Gill flukes; gill damage from ammonia; low oxygen</td><td>Test water; examine gills</td></tr>
    </table>

    <h2 id="parasites">Koi Fish Parasites</h2>
    <p>Parasites are the most common koi health problem, and most are invisible without a microscope. A skin scrape and gill biopsy read at 40&ndash;100&times; is how experienced keepers and vets identify them; treating blind wastes money and stresses fish.</p>
    <ul>
      <li><strong>Ich (<em>Ichthyophthirius multifiliis</em>)</strong> &mdash; visible white grains. Only the free-swimming stage is treatable, so treatment must continue across the full life cycle, which shortens as water warms.</li>
      <li><strong>Skin and gill flukes (<em>Gyrodactylus</em>, <em>Dactylogyrus</em>)</strong> &mdash; the most common koi parasite. Causes flashing, excess mucus, clamped fins and gill irritation. Needs a specific flukicide; salt does not clear them.</li>
      <li><strong>Costia (<em>Ichthyobodo</em>)</strong> &mdash; a fast killer in cool water. Grey-blue film over the skin, lethargy, flashing.</li>
      <li><strong>Chilodonella</strong> and <strong>Trichodina</strong> &mdash; ciliates causing excess mucus and flashing, usually in poor water or crowded conditions.</li>
      <li><strong>Anchor worm (<em>Lernaea</em>)</strong> and <strong>fish lice (<em>Argulus</em>)</strong> &mdash; large enough to see. Remove individually with tweezers, treat the wound, and treat the pond to break the cycle.</li>
    </ul>

    <h2 id="fin-rot">Koi Fin Rot</h2>
    <p>Fin rot is a bacterial infection of tissue already damaged by poor water, fin nipping, or physical injury. Fins fray from the edge inward, often with a white or reddened margin; in advanced cases the erosion reaches the fin base.</p>
    <ol>
      <li><strong>Fix the water.</strong> Test ammonia, nitrite and nitrate; do a 30% water change and repeat every other day.</li>
      <li><strong>Add salt at 0.3%</strong> (about 3 kg per 1,000 litres / 2.5 lb per 100 gallons) for a supportive dip in the healing process, added gradually over 24 hours.</li>
      <li><strong>Check for the cause</strong> &mdash; a sharp rock, a rough net, or a chasing male during spawning season.</li>
      <li><strong>If erosion continues past a week</strong> despite clean water, move to a proprietary antibacterial treatment, or a vet-prescribed antibiotic for a single valuable fish.</li>
    </ol>
    <p>Healed fins regrow with a clear or slightly deformed margin. Regrowth is slow &mdash; weeks to months &mdash; and slower in cold water.</p>

    <h2 id="white-spots">Koi White Spots</h2>
    <p>Not every white spot is ich. Sort them by location and season:</p>
    <table class="ptbl">
      <tr><th>Appearance</th><th>Likely cause</th></tr>
      <tr><td>Fine white grains scattered over body and fins, fish flashing</td><td>Ich (white spot disease)</td></tr>
      <tr><td>White bumps only on gill covers and pectoral fin rays, spring, mature males</td><td>Breeding tubercles &mdash; normal, not a disease</td></tr>
      <tr><td>Waxy white or grey raised patches, cooler months, no other symptoms</td><td>Carp pox &mdash; a herpesvirus growth, usually harmless and seasonal</td></tr>
      <tr><td>Fluffy white tufts on a wound</td><td>Fungus, secondary to injury</td></tr>
      <tr><td>Grey-white film over large areas</td><td>Excess mucus from parasites or chemical irritation</td></tr>
    </table>

    <h2 id="behaviour-signs">Flashing, Lying on the Bottom, Not Eating</h2>
    <p><strong>Flashing</strong> &mdash; rubbing against the pond floor or ornaments &mdash; means irritation. Two causes dominate: parasites, and water chemistry (ammonia, nitrite, chlorine or chloramine in untreated top-up water). Test first, then look for parasites. Occasional single flashes are normal; repeated flashing by several fish is not.</p>
    <p><strong>Koi lying on the bottom</strong> is normal in winter, when koi enter torpor below about 50&deg;F and rest for months. Outside cold weather it points at low oxygen, ammonia poisoning, heavy parasite load, or viral disease. Check dissolved oxygen and ammonia before anything else. A koi lying on its side, rather than resting upright, is a more serious sign &mdash; suspect swim bladder problems or advanced systemic infection.</p>
    <p><strong>Not eating</strong> follows the same triage: temperature, then water quality, then recent changes, then disease. Details are in the <a href="/guides/koi-fish-care/feeding/">koi feeding guide</a>.</p>

    <h2 id="viral">Koi Herpes Virus and Other Viral Disease</h2>
    <p><strong>Koi herpes virus (KHV)</strong> is the disease that ends ponds. It becomes active between roughly 64 and 81&deg;F, kills a high proportion of infected fish within days, and survivors remain lifelong carriers. Signs include sunken eyes, patchy or necrotic gills, lethargy and rapid mortality across the pond. There is no cure. In several countries it is notifiable, and infected stock must not be moved or sold.</p>
    <p><strong>Spring viraemia of carp (SVC)</strong> appears in cool spring water, with haemorrhaging, bloated abdomen and erratic swimming. It is also notifiable in many jurisdictions.</p>
    <p>The only meaningful protection for both is quarantine: keep every new koi in a separate system at 65&ndash;75&deg;F for three to four weeks, watch it, and never add fish straight from a shop bag into the pond.</p>

    <h2 id="prevention">Prevention and the Quarantine Routine</h2>
    <ol>
      <li>Quarantine all new koi for 3&ndash;4 weeks at 65&ndash;75&deg;F in a filtered, aerated tank.</li>
      <li>Test pond water weekly, and always after adding fish or a big rain event.</li>
      <li>Change 10&ndash;20% of the water weekly rather than waiting for a problem.</li>
      <li>Keep stocking density low &mdash; 500 gallons per adult koi.</li>
      <li>Never share nets, bowls or hands between quarantine and main pond without disinfecting.</li>
      <li>Keep a treatment kit ready: pond salt, a dechlorinator, a flukicide, a broad antibacterial, and a liquid test kit.</li>
      <li>Watch feeding time every day. Koi that miss a meal are telling you something days before symptoms show.</li>
    </ol>
"""

DISEASES = {
    "slug": "diseases",
    "title": "Koi Fish Diseases & Parasites: Symptom Chart and Treatment | FishCare AI",
    "meta_desc": "Koi disease symptom chart: flashing, white spots, fin rot, ulcers, lying on the bottom and not eating, plus koi parasites, koi herpes virus and a quarantine routine.",
    "h1": "Koi Fish Diseases, Parasites and Symptoms",
    "hero_tag": "Diseases & Symptoms",
    "hero_meta": "\U0001F50D Test water first &nbsp;|&nbsp; \U0001FA79 Symptom index &nbsp;|&nbsp; \U0001F6E1️ 3&ndash;4 week quarantine",
    "date": "2026-09-08",
    "toc_sections": [
        ("symptom-index", "Symptom Index"),
        ("parasites", "Koi Parasites"),
        ("fin-rot", "Koi Fin Rot"),
        ("white-spots", "Koi White Spots"),
        ("behaviour-signs", "Flashing & Lethargy"),
        ("viral", "Koi Herpes Virus"),
        ("prevention", "Prevention"),
    ],
    "body": DISEASES_BODY,
    "faqs": [
        ("Why is my koi flashing and rubbing on the bottom?",
         "Flashing means skin irritation. The two dominant causes are parasites - usually flukes, costia or trichodina - and water chemistry problems such as ammonia, nitrite, or chlorine in untreated top-up water. Test the water first, then have a skin scrape examined under a microscope."),
        ("What are the white spots on my koi?",
         "Fine white grains scattered over the body and fins with flashing indicate ich. White bumps confined to the gill covers and pectoral fins of a mature male in spring are breeding tubercles and are normal. Waxy grey-white raised patches in cool weather are usually carp pox, which is largely harmless."),
        ("Why is my koi lying on the bottom of the pond?",
         "Below about 50F this is normal winter torpor. In warmer water it points at low dissolved oxygen, ammonia poisoning, a heavy parasite load or viral disease. Check oxygen and ammonia first. A koi lying on its side rather than resting upright is more serious."),
        ("How do I treat koi fin rot?",
         "Fin rot is bacterial and secondary to poor water or injury. Do 30% water changes every other day, add pond salt gradually to 0.3%, and find the physical cause. If the erosion continues after a week in clean water, move to a proprietary antibacterial treatment or ask a vet about antibiotics."),
        ("What is koi herpes virus?",
         "KHV is a viral disease active between roughly 64 and 81F that kills a high proportion of infected koi within days, with survivors remaining lifelong carriers. Signs include sunken eyes, patchy gills and rapid mortality. There is no cure, it is notifiable in several countries, and quarantining new fish is the only real protection."),
        ("Do I need to quarantine new koi?",
         "Yes. Keep every new koi in a separate filtered, aerated system at 65-75F for three to four weeks. Most catastrophic pond losses trace back to a single fish added straight from a shop bag."),
    ],
    "related": [
        ("/aquarium-fish-diseases/koi-diseases/", "Koi Disease Index"),
        ("/guides/koi-fish-care/water-parameters/", "Koi Water Parameters"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/koi-fish-care/feeding/", "Koi Feeding Chart"),
    ],
}

# ────────────────────────────────────────────────────────────────
# PAGE 10 — Tank & Pond Mates
# ────────────────────────────────────────────────────────────────
MATES_BODY = """    <p>Koi are peaceful, but they are large, coldwater, and constantly grazing &mdash; which rules out most of what people ask about. A workable koi tank mate has to survive the same 59&ndash;77&deg;F range, be too big to swallow, and tolerate a pond that is engineered around koi waste. In practice the list is short.</p>

    <h2 id="quick-list">Koi Tank Mates at a Glance</h2>
    <table class="ptbl">
      <tr><th>Species</th><th>Verdict</th><th>Why</th></tr>
      <tr><td>Goldfish (common, comet, shubunkin)</td><td>&#9989; Best match</td><td>Same temperature range, same diet, similar temperament</td></tr>
      <tr><td>Golden orfe (ide)</td><td>&#9989; Good</td><td>Coldwater, fast, active surface shoal; needs high oxygen and a covered pond</td></tr>
      <tr><td>Grass carp</td><td>&#9888;&#65039; Regional</td><td>Compatible but regulated or banned in many jurisdictions &mdash; check local law</td></tr>
      <tr><td>Sterlet / sturgeon</td><td>&#9888;&#65039; Experienced keepers only</td><td>Needs sinking food koi will steal, very high oxygen, and 1,000+ extra gallons</td></tr>
      <tr><td>Fancy goldfish (oranda, ryukin)</td><td>&#9888;&#65039; Not with adult koi</td><td>Too slow to compete for food; koi bump and outcompete them</td></tr>
      <tr><td>Weather loach (dojo)</td><td>&#9989; Good in mild climates</td><td>Coldwater bottom dweller, peaceful, hides in substrate</td></tr>
      <tr><td>Rosy red minnows</td><td>&#9888;&#65039; Feeder fish</td><td>Will be eaten by adult koi; useful only in a heavily planted pond</td></tr>
      <tr><td>Plecos and tropical catfish</td><td>&#10060; No (outdoors)</td><td>Tropical; will not survive pond winters</td></tr>
      <tr><td>Turtles</td><td>&#10060; No</td><td>Bite fins and tails; opportunistic predators of smaller koi</td></tr>
      <tr><td>Tropical community fish (tetras, guppies, gouramis)</td><td>&#10060; No</td><td>Wrong temperature; small enough to be eaten</td></tr>
      <tr><td>Cichlids of any kind</td><td>&#10060; No</td><td>Tropical, territorial, and aggressive toward slow-moving koi</td></tr>
    </table>
    <p>Compare any specific pairing with our <a href="/compatibility/koi/">koi compatibility guides</a>, which score 90 species against koi individually.</p>

    <h2 id="goldfish">Koi and Goldfish Together</h2>
    <p>Goldfish are the standard koi companion and the pairing works well. Both are coldwater cyprinids, both eat the same food, and neither is aggressive.</p>
    <ul>
      <li><strong>Size difference is the main issue.</strong> Adult koi reach 24&ndash;36 inches; common goldfish reach 8&ndash;12 inches. Koi will not hunt goldfish, but very small goldfish can be swallowed accidentally at feeding time. Introduce goldfish at 4 inches or larger.</li>
      <li><strong>Competition at the surface.</strong> Koi feed aggressively and faster. Spread food across the pond so goldfish get their share.</li>
      <li><strong>Avoid fancy varieties</strong> in a koi pond &mdash; orandas, ryukins and bubble-eyes cannot compete for food and are physically knocked about.</li>
      <li><strong>They can hybridise.</strong> Koi &times; goldfish crosses happen in mixed ponds. The offspring are sterile mules with unpredictable, usually plain, colouring.</li>
      <li><strong>Stocking still counts.</strong> Goldfish add to the bio-load; count them in your gallons-per-fish figure. Details in the <a href="/compatibility/goldfish-and-koi/">koi and goldfish compatibility guide</a>.</li>
    </ul>

    <h2 id="turtles">Koi and Turtles</h2>
    <p>Do not keep turtles with koi. Red-eared sliders, painted turtles and snapping turtles are all opportunistic carnivores, and a pond of slow-moving, long-finned fish is exactly what they will act on.</p>
    <ul>
      <li>Turtles bite fins and tails, causing wounds that turn into bacterial ulcers even when the fish survives the bite.</li>
      <li>Snapping turtles will take koi outright, including large ones.</li>
      <li>Turtles are heavy waste producers and add substantially to the filtration load.</li>
      <li>They also eat pond plants down to the roots and bask on anything they can climb, which usually means the pond edge and your plant shelves.</li>
    </ul>
    <p>If you want both, keep them in separate systems. A juvenile turtle in a big pond may coexist for a while &mdash; that is a delay, not compatibility.</p>

    <h2 id="pleco">Koi and Plecos</h2>
    <p>Plecos are tropical South American catfish that need 74&ndash;80&deg;F. In an outdoor koi pond in any temperate climate, a pleco will die over winter, so this pairing is only ever an <strong>indoor, heated aquarium</strong> question &mdash; and an indoor tank is already a poor long-term home for koi.</p>
    <ul>
      <li><strong>Temperature conflict:</strong> koi do best at 59&ndash;77&deg;F, plecos at 74&ndash;80&deg;F. The overlap is narrow and suits neither well.</li>
      <li><strong>Rasping behaviour:</strong> common plecos are known to rasp at the slime coat of large, slow-moving fish. A koi is exactly the target profile, and the resulting wounds invite bacterial infection.</li>
      <li><strong>Better indoor option:</strong> bristlenose pleco, which stays under 5 inches and rarely rasps at fish &mdash; see the <a href="/compatibility/bristlenose-pleco-and-koi/">bristlenose pleco and koi guide</a>. It is still a temperature compromise.</li>
      <li><strong>For pond algae,</strong> use filtration, shade and a UV clarifier rather than a fish. No pond-safe algae eater does the job in a koi pond.</li>
    </ul>

    <h2 id="stocking">Stocking a Mixed Pond</h2>
    <ol>
      <li>Count every fish against the same budget: <strong>250 gallons per koi minimum, 500 recommended</strong>, with goldfish counted at roughly a quarter of a koi each.</li>
      <li>Quarantine everything for 3&ndash;4 weeks &mdash; goldfish carry the same parasites and viruses that will run through a koi pond.</li>
      <li>Introduce new companions when the koi are fed and settled, ideally in the evening.</li>
      <li>Feed in two or three spots so slower fish are not shut out.</li>
      <li>Recheck your stocking every year. The pond that was lightly stocked with 6-inch koi is heavily stocked once they pass 18 inches.</li>
    </ol>
"""

MATES = {
    "slug": "tank-mates",
    "title": "Koi Fish Tank Mates: Goldfish, Turtles, Plecos & What to Avoid | FishCare AI",
    "meta_desc": "Which fish can live with koi: goldfish and orfe work, turtles and plecos do not. Koi tank mate compatibility chart, koi and goldfish together, and mixed-pond stocking.",
    "h1": "Koi Fish Tank Mates and Pond Companions",
    "hero_tag": "Tank & Pond Mates",
    "hero_meta": "\U0001F420 Goldfish are the best match &nbsp;|&nbsp; \U0001F422 Turtles: no &nbsp;|&nbsp; \U0001F321️ Coldwater species only",
    "date": "2026-09-08",
    "toc_sections": [
        ("quick-list", "Compatibility Chart"),
        ("goldfish", "Koi and Goldfish"),
        ("turtles", "Koi and Turtles"),
        ("pleco", "Koi and Plecos"),
        ("stocking", "Mixed Pond Stocking"),
    ],
    "body": MATES_BODY,
    "faqs": [
        ("What fish can live with koi?",
         "Goldfish are the best match, along with golden orfe and weather loaches in mild climates. All share the koi temperature range of 59-77F and are too large to be eaten. Sterlet sturgeon work only for experienced keepers with very large, high-oxygen ponds."),
        ("Can koi and goldfish live together?",
         "Yes. Both are peaceful coldwater cyprinids that eat the same food. Introduce goldfish at 4 inches or larger so adult koi cannot swallow them at feeding time, avoid fancy varieties that cannot compete for food, and count the goldfish in your stocking budget."),
        ("Can koi live with turtles?",
         "No. Red-eared sliders, painted turtles and snapping turtles all bite fins and tails and will take smaller koi outright. They also produce heavy waste and eat pond plants. Keep turtles in a separate system."),
        ("Can a pleco live with koi?",
         "Only in a heated indoor tank, and even then it is a compromise: plecos need 74-80F while koi do best at 59-77F. Common plecos may rasp at the slime coat of large slow fish like koi. A bristlenose pleco is the safer choice, and no pleco survives an outdoor pond winter in a temperate climate."),
        ("Will koi eat smaller fish?",
         "Koi do not hunt, but they are large and will hoover up anything small enough to fit in their mouth during feeding. Fish under about 3 inches, including fry and rosy red minnows, will disappear from a koi pond over time."),
    ],
    "related": [
        ("/compatibility/koi/", "Koi Compatibility Guides"),
        ("/compatibility/goldfish-and-koi/", "Koi and Goldfish"),
        ("/tools/fish-compatibility-checker/", "Compatibility Checker"),
        ("/guides/koi-fish-care/pond-setup/", "Koi Pond Size & Setup"),
    ],
}


PAGES = [POND_SETUP, WATER, FEEDING, SIZE, LIFESPAN, TYPES, MVF, BREEDING, DISEASES, MATES]


def main():
    for pg in PAGES:
        out = BASE / pg["slug"]
        out.mkdir(parents=True, exist_ok=True)
        html = page(
            slug=pg["slug"],
            title=pg["title"],
            meta_desc=pg["meta_desc"],
            h1=pg["h1"],
            hero_tag=pg["hero_tag"],
            hero_meta=pg["hero_meta"],
            date=pg["date"],
            toc_sections=pg["toc_sections"],
            body_html=pg["body"],
            faqs=pg["faqs"],
            related=pg["related"],
        )
        (out / "index.html").write_text(html, encoding="utf-8")
        print(f"✓ /guides/koi-fish-care/{pg['slug']}/  ({len(html):,} bytes)")
    print(f"\nDone — {len(PAGES)} koi cluster pages generated.")


if __name__ == "__main__":
    main()
