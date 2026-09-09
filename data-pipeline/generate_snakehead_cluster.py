"""
generate_snakehead_cluster.py
─────────────────────────────
Generates the Snakehead Fish (Channa) care cluster under
/guides/snakehead-fish-care/, following the betta/koi/parrot cluster template
(artlay 2-column with sidebar cluster nav).

Run:  python3 generate_snakehead_cluster.py
"""

from pathlib import Path
import json

REPO = Path(__file__).parent.parent
BASE = REPO / "guides" / "snakehead-fish-care"

HERO_IMG = "/assets/encyclopedia/real/snakehead-fish-wikimedia-real.jpg"
DATE = "2026-09-09"

CLUSTER_NAV = [
    ("/guides/snakehead-fish-care/",                  "\U0001F41F Snakehead Fish Care Guide", "pillar"),
    ("/guides/snakehead-fish-care/types/",            "\U0001F3A8 Types & Species"),
    ("/guides/snakehead-fish-care/tank-size/",        "\U0001F5C3\uFE0F Tank Size & Setup"),
    ("/guides/snakehead-fish-care/water-parameters/", "\U0001F321\uFE0F Water & Temperature"),
    ("/guides/snakehead-fish-care/feeding/",          "\U0001F35A Food & Feeding"),
    ("/guides/snakehead-fish-care/size-growth/",      "\U0001F4CF Size & Growth"),
    ("/guides/snakehead-fish-care/lifespan/",         "\u23F3 Lifespan"),
    ("/guides/snakehead-fish-care/male-vs-female/",   "\u2640\u2642 Male vs Female"),
    ("/guides/snakehead-fish-care/breeding/",         "\U0001F95A Breeding & Fry"),
    ("/guides/snakehead-fish-care/diseases/",         "\U0001FA7A Diseases & Symptoms"),
    ("/guides/snakehead-fish-care/tank-mates/",       "\U0001F420 Tank Mates"),
    ("/wiki/snakehead-fish/",                         "\U0001F4D6 Species Profile"),
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
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('/assets/encyclopedia/real/snakehead-fish-wikimedia-real.jpg') center/cover no-repeat}
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
.fig{margin:18px 0;border-radius:16px;overflow:hidden;border:1px solid rgba(128,160,190,.35);background:transparent;box-shadow:0 12px 30px rgba(15,61,110,.08)}
.fig img{display:block;width:100%;height:auto;object-fit:cover;background:rgba(128,160,190,.14)}
.fig figcaption{padding:10px 14px;font-size:.8rem;color:inherit;opacity:.82;background:rgba(128,160,190,.12);border-top:1px solid rgba(128,160,190,.28);line-height:1.5}
.fig figcaption em{color:inherit;font-style:italic}
.figgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:18px 0}
.figgrid .fig{margin:0}
@media(max-width:600px){.figgrid{grid-template-columns:1fr}}
.ft{background:#0F3D5E;padding:32px 22px 20px;margin-top:60px}
.ftb{text-align:center;color:rgba(255,255,255,.4);font-size:.76rem}"""


def cluster_nav_html(current_slug: str) -> str:
    items = []
    for entry in CLUSTER_NAV:
        href, label = entry[0], entry[1]
        css_class = entry[2] if len(entry) > 2 else ""
        if current_slug == "":
            is_cur = href == "/guides/snakehead-fish-care/"
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
    return ('    <h2 id="related">Related Snakehead Guides and Tools</h2>\n'
            f'    <div class="guide-links">{items}</div>')


def page(slug, title, meta_desc, h1, hero_tag, hero_meta,
         toc_sections, body_html, faqs, related, date=DATE):
    if slug:
        canonical = f"https://www.fishcareai.com/guides/snakehead-fish-care/{slug}/"
        crumb_tail = (
            '<a href="/guides/snakehead-fish-care/">Snakehead Fish Care Guide</a><span>/</span>\n      '
            f'<span style="color:rgba(255,255,255,.9)">{hero_tag}</span>'
        )
        breadcrumb_items = (
            '{"@type":"ListItem","position":3,"name":"Snakehead Fish Care Guide",'
            '"item":"https://www.fishcareai.com/guides/snakehead-fish-care/"},'
            f'{{"@type":"ListItem","position":4,"name":{json.dumps(h1)},"item":"{canonical}"}}'
        )
    else:
        canonical = "https://www.fishcareai.com/guides/snakehead-fish-care/"
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
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">&#128013; Snakehead Fish Care</div>
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
      <h4>Snakehead Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc)}
    </div>
    <div class="tool-card">
      <h4>Snakehead Tools</h4>
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
# PILLAR — Snakehead Fish Care Guide
# ════════════════════════════════════════════════════════════════
PILLAR_BODY = """    <p>Snakeheads (family Channidae) are air-breathing ambush predators from Asia and Africa. In the aquarium trade they are usually sold under the genus name <strong><em>Channa</em></strong> &mdash; a group of more than 50 described species that runs from 4-inch dwarfs suited to a 30-gallon tank all the way up to the 4-foot giant snakehead. That range is why almost every generic &ldquo;snakehead fish care&rdquo; answer online is wrong for the fish actually in front of you: the correct tank size, temperature and diet depend entirely on which <em>Channa</em> you have.</p>
    <p>This guide covers what all snakeheads share, then points you to the species-specific numbers. Read the legal section first &mdash; in the United States, snakeheads are federally restricted, and that is not a formality.</p>

    <div class="callout callout-warn"><strong>Legal status first.</strong> All <em>Channa</em> and <em>Parachanna</em> species are listed as <strong>injurious wildlife under the US Lacey Act</strong>, and many states ban possession outright. Check the <a href="#legality">legality section</a> before you buy, import or rehome one.</div>

    <h2 id="what-is">What Is a Snakehead Fish?</h2>
    <p>Snakeheads get their name from the flattened, scaled head and the long cylindrical body &mdash; the profile genuinely looks like a snake when the fish hangs motionless under a leaf. Two genera make up the family:</p>
    <ul>
      <li><strong><em>Channa</em></strong> &mdash; roughly 50+ species across South, Southeast and East Asia. This is what &ldquo;channa fish&rdquo; means in the hobby.</li>
      <li><strong><em>Parachanna</em></strong> &mdash; three African species, rarely seen in the trade.</li>
    </ul>
    <p>Three traits define how you have to keep them, and every care decision on this site follows from these:</p>
    <ol>
      <li><strong>They are obligate air-breathers.</strong> A snakehead has a suprabranchial chamber above the gills that works like a primitive lung. It <em>must</em> surface every few minutes to gulp atmospheric air. A snakehead sealed under a tight lid with no air gap, or trapped under d&eacute;cor, will drown &mdash; in fully oxygenated water.</li>
      <li><strong>They are ambush piscivores.</strong> They sit still for hours and then strike. Anything that fits in the mouth is food, and the mouth is larger than it looks.</li>
      <li><strong>They are escape artists.</strong> Snakeheads jump, push at lids and squeeze through filter cutouts. A weighted, fully sealed cover is not optional equipment; it is the single most common cause of death in captivity.</li>
    </ol>
    <p>What they are <em>not</em> is the tabloid monster of the &ldquo;Frankenfish&rdquo; headlines. They do not hunt people, they do not stalk across dry land for miles, and most species cannot survive out of water for more than a short period in damp conditions. The real concern is ecological, not personal &mdash; see <a href="#legality">legality and invasive status</a>.</p>

    <h2 id="legality">Are Snakehead Fish Legal? Invasive Status Explained</h2>
    <p>This is the most important question on the page, and the honest answer for most US readers is <strong>no</strong>.</p>
    <h3>United States</h3>
    <p>In 2002 the US Fish and Wildlife Service added all species of <em>Channa</em> and <em>Parachanna</em> to the <strong>injurious wildlife</strong> list under the Lacey Act. In practice that means:</p>
    <ul>
      <li><strong>Import into the US is prohibited</strong>, as is transport across state lines.</li>
      <li><strong>Possession is governed by state law</strong>, and a large majority of states prohibit it outright &mdash; including California, Florida, Texas, New York, Washington, Massachusetts, Maine and Wisconsin. A handful of states have narrower rules or permit systems.</li>
      <li>Because interstate transport is federally banned, even in a state with no explicit possession ban there is usually no lawful way to obtain one.</li>
    </ul>
    <p>Penalties are real: fines, confiscation and in some jurisdictions criminal charges. If you already own a snakehead, contact your state wildlife agency &mdash; <strong>never release it into local water and never flush it</strong>.</p>
    <h3>United Kingdom and European Union</h3>
    <p>The northern snakehead (<em>Channa argus</em>) is listed as an <strong>Invasive Alien Species of Union Concern</strong>, which bans keeping, breeding, selling and releasing it across the EU, and it carries equivalent restrictions in the UK. Other <em>Channa</em> species are generally legal to keep in the UK and much of the EU, but rules change &mdash; verify before buying.</p>
    <h3>Elsewhere</h3>
    <p>Canada bans snakeheads in several provinces including Ontario. Australia prohibits them nationally. In much of Asia they are native, farmed as food fish, and completely unrestricted.</p>
    <h3>Why they are restricted</h3>
    <p><em>Channa argus</em> became established in the Potomac River after a 2002 discovery in a Maryland pond, and the bullseye snakehead (<em>C. marulius</em>) is established in southeast Florida. Air-breathing lets them survive waters that would kill other predators, and they guard their fry aggressively, so populations establish easily. Field studies since have found the ecological damage less catastrophic than early coverage predicted, but the precautionary listing stands.</p>
    <div class="callout callout-warn"><strong>Are snakehead fish dangerous to humans?</strong> There are no verified records of unprovoked attacks on people. A large snakehead guarding fry will charge and can bite a hand placed in the nest, and a 3-foot <em>C. micropeltes</em> has teeth that warrant respect during maintenance &mdash; but they are not a danger to swimmers.</div>

    <h2 id="quick-facts">Snakehead Fish Care at a Glance</h2>
    <p>These are the ranges across commonly kept aquarium species. Species-specific numbers are on the <a href="/guides/snakehead-fish-care/types/">types and species page</a>.</p>
    <table class="ptbl">
      <tr><th>Care factor</th><th>Requirement</th></tr>
      <tr><td>Family / genus</td><td>Channidae &mdash; <em>Channa</em> (Asia), <em>Parachanna</em> (Africa)</td></tr>
      <tr><td>Adult size</td><td>4 in (<em>C. andrao</em>) to 4 ft (<em>C. micropeltes</em>)</td></tr>
      <tr><td>Lifespan</td><td>8&ndash;15 years typical; 20+ for large species</td></tr>
      <tr><td>Minimum tank</td><td>30 gal for a dwarf pair; 300&ndash;1,000+ gal for large species</td></tr>
      <tr><td>Temperature</td><td>Species-dependent: 60&ndash;79&deg;F subtropical, 75&ndash;82&deg;F tropical</td></tr>
      <tr><td>pH</td><td>6.0&ndash;7.5</td></tr>
      <tr><td>Hardness</td><td>2&ndash;15 dGH</td></tr>
      <tr><td>Ammonia / nitrite</td><td>0 ppm always</td></tr>
      <tr><td>Nitrate</td><td>Under 30 ppm</td></tr>
      <tr><td>Diet</td><td>Carnivore &mdash; frozen seafood, insects, worms, weaned carnivore pellets</td></tr>
      <tr><td>Temperament</td><td>Predatory; territorial to highly aggressive by species</td></tr>
      <tr><td>Air access</td><td>Mandatory &mdash; 2&ndash;4 in humid air gap under a sealed lid</td></tr>
      <tr><td>Care level</td><td>Intermediate to advanced</td></tr>
    </table>

    <h2 id="types">Snakehead Species: Dwarf to Giant</h2>
    <p>Pick the species before you pick the tank. The trade names are inconsistent &mdash; &ldquo;dwarf snakehead&rdquo; is applied to at least six different fish &mdash; so buy on the scientific name.</p>
    <table class="ptbl">
      <tr><th>Group</th><th>Examples</th><th>Adult size</th><th>Realistic tank</th></tr>
      <tr><td>Dwarf</td><td><em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em>, <em>C. limbata</em></td><td>4&ndash;8 in</td><td>30&ndash;55 gal</td></tr>
      <tr><td>Medium</td><td><em>C. pulchra</em>, <em>C. stewartii</em>, <em>C. asiatica</em>, <em>C. aurantimaculata</em></td><td>12&ndash;16 in</td><td>75&ndash;125 gal</td></tr>
      <tr><td>Large</td><td><em>C. marulioides</em>, <em>C. striata</em>, <em>C. lucius</em>, <em>C. barca</em></td><td>2&ndash;3 ft</td><td>250&ndash;400 gal</td></tr>
      <tr><td>Giant</td><td><em>C. micropeltes</em>, <em>C. marulius</em>, <em>C. argus</em></td><td>3&ndash;4 ft</td><td>1,000+ gal / indoor pond</td></tr>
    </table>
    <p>Full profiles, common trade names (red, rainbow, blue, golden, emperor, bullseye, giant, northern) and photographs are on the <a href="/guides/snakehead-fish-care/types/">snakehead types and species guide</a>.</p>

    <h2 id="tank">Tank Size and Setup</h2>
    <p>The working rule is <strong>tank length at least 3&times; adult body length and width at least 1.5&times;</strong>. A 5-inch <em>C. andrao</em> therefore wants a 30-inch tank &mdash; a standard 30-gallon breeder is a good pair tank. A 30-inch <em>C. marulioides</em> wants an 8-foot tank, which is why so few people should own one.</p>
    <p>Setup priorities, in order:</p>
    <ul>
      <li><strong>A weighted, gap-free lid</strong> with a 2&ndash;4 inch humid air gap above the water. Block every filter and heater cutout. Snakeheads breathe warm humid air; an open-topped tank in a cold room stresses the breathing organ even if the fish does not jump out.</li>
      <li><strong>Footprint over height.</strong> They are bottom-and-mid ambushers that need floor area, not depth.</li>
      <li><strong>Low flow.</strong> Wild habitat is sluggish streams, swamps and paddy fields. Baffle strong returns.</li>
      <li><strong>Heavy cover.</strong> Caves, driftwood tangles, leaf litter and dense floating plants. A snakehead with nowhere to hide stays skittish and jumps.</li>
      <li><strong>Oversized filtration.</strong> A predator fed whole seafood produces a heavy waste load. Rate the filter for at least 1.5&times; tank volume and change 30&ndash;50% of the water weekly.</li>
    </ul>
    <p>Full dimensions by species and a lid checklist: <a href="/guides/snakehead-fish-care/tank-size/">snakehead fish tank size guide</a>. Our <a href="/tools/tank-size-calculator/">tank size calculator</a> converts dimensions to gallons.</p>

    <h2 id="water">Water Parameters and Temperature</h2>
    <p>There is no single &ldquo;snakehead fish temperature&rdquo;. The genus spans the tropics to temperate China, and keeping a subtropical species at tropical temperatures year-round is one of the commonest slow-killers in the hobby.</p>
    <table class="ptbl">
      <tr><th>Group</th><th>Temperature</th><th>Winter cooldown</th></tr>
      <tr><td>Tropical lowland (<em>micropeltes</em>, <em>striata</em>, <em>lucius</em>, <em>marulioides</em>)</td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td><td>Not required</td></tr>
      <tr><td>Subtropical / highland (<em>andrao</em>, <em>bleheri</em>, <em>gachua</em>, <em>aurantimaculata</em>, <em>stewartii</em>)</td><td>64&ndash;79&deg;F (18&ndash;26&deg;C)</td><td>Yes &mdash; 8&ndash;12 weeks at 59&ndash;68&deg;F</td></tr>
      <tr><td>Temperate (<em>C. argus</em>, <em>C. asiatica</em>)</td><td>50&ndash;79&deg;F (10&ndash;26&deg;C)</td><td>Yes &mdash; a genuine cold season</td></tr>
    </table>
    <p>Across all of them: pH 6.0&ndash;7.5, hardness 2&ndash;15 dGH, ammonia and nitrite at 0 ppm, nitrate under 30 ppm. Detail and a seasonal schedule: <a href="/guides/snakehead-fish-care/water-parameters/">snakehead water parameters and temperature</a>. Check a reading against safe ranges with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="food">Food and Feeding</h2>
    <p>Snakeheads are carnivores, but <strong>a diet of live feeder fish is the wrong way to feed one</strong>. Goldfish and rosy red minnows contain thiaminase, which destroys vitamin B1 and causes neurological damage over months, and feeders are the most reliable way to introduce disease into a tank.</p>
    <p>Feed instead a rotation of thawed frozen and fresh foods: shell-on shrimp and prawn, mussel, krill, silversides, white fish fillet, earthworms, and for dwarf species bloodworm, mysis and insects such as crickets and dubia roaches. Most <em>Channa</em> can be weaned onto quality carnivore pellets, which makes long-term nutrition far easier.</p>
    <p>Feed juveniles daily; adults <strong>2&ndash;3 times a week</strong> is plenty. Obesity and fatty liver disease are far more common in captive snakeheads than starvation. Full schedule, portion sizes and a pellet-weaning method: <a href="/guides/snakehead-fish-care/feeding/">what snakehead fish eat</a>.</p>

    <h2 id="behavior">Behaviour, Aggression and Normal Weirdness</h2>
    <p>New snakehead keepers panic about behaviour that is entirely normal for an ambush predator:</p>
    <ul>
      <li><strong>Lying motionless on the bottom for hours</strong> is normal. It is how the fish hunts.</li>
      <li><strong>Rising to the surface to gulp air</strong> every few minutes is normal and mandatory. It is not gasping. Distress looks different &mdash; the fish stays at the surface with rapid gill movement instead of returning to its station.</li>
      <li><strong>Hiding for two to four weeks after import</strong> is normal. Dim the lights, add cover, stop staring at it.</li>
      <li><strong>Darkening or losing colour</strong> is often a mood and dominance signal in <em>Channa</em> and can change within hours.</li>
    </ul>
    <p>Aggression is real and species-specific. <em>C. bleheri</em> and <em>C. andrao</em> are comparatively mild; <em>C. micropeltes</em>, <em>C. marulius</em> and <em>C. argus</em> are seriously aggressive and every species becomes far worse when spawning. The most dangerous tank mate for a snakehead is another snakehead.</p>

    <h2 id="mates">Tank Mates</h2>
    <p>The realistic answer is that <strong>most snakeheads are best kept alone or as a proven pair</strong>. Where tank mates work at all, they follow three rules: nothing small enough to swallow, nothing slow with trailing fins, and nothing that competes for the same floor space.</p>
    <p>Dwarf species in a large, heavily planted tank can sometimes live with fast mid-water dithers such as rosy barbs, tiger barbs or larger rasboras. Big species realistically get bichirs, large plecos or nothing. Oscars, arowanas and African cichlids are all common suggestions that mostly end badly &mdash; the reasons are broken down on the <a href="/guides/snakehead-fish-care/tank-mates/">snakehead tank mates guide</a>, and you can sanity-check a pairing with the <a href="/tools/fish-compatibility-checker/">compatibility checker</a>.</p>

    <h2 id="health">Common Health Problems</h2>
    <p>Snakeheads are hardy fish that mostly get sick for three reasons: wild-caught parasite loads, injuries from jumping or fighting, and diet.</p>
    <ul>
      <li><strong>Not eating</strong> &mdash; usually settling stress in a new fish, wrong temperature for the species, or a natural seasonal fast. Weeks of refusal in an otherwise bright, alert fish is common and rarely an emergency.</li>
      <li><strong>Internal parasites</strong> &mdash; wild-caught imports frequently carry nematodes and tapeworms. Quarantine 4&ndash;6 weeks and treat before the fish goes in the display.</li>
      <li><strong>Bloating</strong> &mdash; overfeeding first, dropsy second. Pineconed scales change the diagnosis.</li>
      <li><strong>Ulcers, cloudy eye and fin damage</strong> &mdash; nearly always secondary to a jumping impact, a bite, or nitrate creep.</li>
    </ul>
    <p>Symptom-by-symptom diagnosis, including white spots, turning black, swimming sideways and true gasping: <a href="/guides/snakehead-fish-care/diseases/">snakehead fish diseases and symptoms</a>.</p>

    <h2 id="breeding">Breeding</h2>
    <p><em>Channa</em> split into two reproductive strategies. The dwarf <em>gachua</em>-group species &mdash; including <em>C. andrao</em>, <em>C. bleheri</em> and <em>C. pulchra</em> &mdash; are <strong>paternal mouthbrooders</strong>: the pair spawns in an embrace near the surface, the male collects the floating eggs and incubates them for several days, then guards the free-swimming fry. Large species such as <em>C. striata</em>, <em>C. argus</em> and <em>C. micropeltes</em> are <strong>nest guarders</strong> that produce a floating raft of eggs and defend the fry as a pair, sometimes for months.</p>
    <p>Both routes need an established, well-fed pair, cover, and in subtropical species a cool period followed by warming and soft-water changes. Step-by-step conditioning, spawning and fry raising: <a href="/guides/snakehead-fish-care/breeding/">breeding snakehead fish</a>. Telling the sexes apart first: <a href="/guides/snakehead-fish-care/male-vs-female/">male vs female snakehead</a>.</p>

    <h2 id="verdict">Should You Keep a Snakehead?</h2>
    <p>If you are in the US, the answer is almost certainly no, on legal grounds alone. Where they are legal, a dwarf <em>Channa</em> in a 40-gallon planted tank with a locked lid is a genuinely rewarding fish &mdash; intelligent, interactive, and one of the few aquarium species that will watch you back. A giant snakehead in a home aquarium is a mistake that takes three years to become obvious.</p>
"""

PILLAR = {
    "slug": "",
    "title": "Snakehead Fish Care Guide (Channa): Tank, Food, Types & Legality",
    "meta_desc": "Complete snakehead fish care guide: Channa tank size, temperature, food, species from dwarf to giant, breeding - and where snakeheads are legal.",
    "h1": "Snakehead Fish Care Guide (Channa)",
    "hero_tag": "Snakehead Fish Care Guide",
    "hero_meta": "\U0001F41F 50+ <em>Channa</em> species &nbsp;|&nbsp; \U0001F4CF 4 in to 4 ft &nbsp;|&nbsp; \U0001FAC1 Obligate air-breather &nbsp;|&nbsp; ⚖️ Restricted in the US",
    "toc_sections": [
        ("what-is", "What Is a Snakehead?"),
        ("legality", "Legality & Invasive Status"),
        ("quick-facts", "Care at a Glance"),
        ("types", "Species & Types"),
        ("tank", "Tank Size & Setup"),
        ("water", "Water & Temperature"),
        ("food", "Food & Feeding"),
        ("behavior", "Behaviour & Aggression"),
        ("mates", "Tank Mates"),
        ("health", "Health Problems"),
        ("breeding", "Breeding"),
        ("verdict", "Should You Keep One?"),
    ],
    "body": PILLAR_BODY,
    "faqs": [
        ("Are snakehead fish illegal?",
         "In the United States all Channa and Parachanna species are listed as injurious wildlife under the Lacey Act, so import and interstate transport are federally banned and most states prohibit possession outright. Channa argus is banned across the EU and UK as an Invasive Alien Species of Union Concern, while other Channa species are generally legal in the UK. Always check your state or national rules before buying."),
        ("Can you keep snakehead fish as pets?",
         "Where it is legal, yes - dwarf species such as Channa andrao and Channa bleheri do well in a 30-55 gallon tank with a sealed lid, low flow and heavy cover. Large species reaching 2-4 feet are not realistic home aquarium fish. In most of the United States keeping any snakehead is prohibited."),
        ("How big do snakehead fish get?",
         "It depends entirely on species. Dwarf snakeheads such as Channa andrao stay around 4-5 inches, mid-sized species like Channa aurantimaculata reach 12-16 inches, and the giant snakehead Channa micropeltes can exceed 4 feet."),
        ("Are snakehead fish dangerous?",
         "Not to people. There are no verified records of unprovoked snakehead attacks on humans. A large adult guarding fry will charge and can bite a hand placed into the nest, so use care during maintenance, but they pose no threat to swimmers."),
        ("Do snakehead fish need to breathe air?",
         "Yes. Snakeheads are obligate air-breathers with a suprabranchial chamber above the gills and must surface every few minutes to gulp atmospheric air. A snakehead denied surface access will drown even in fully oxygenated water, so the tank needs a 2-4 inch humid air gap under a secure lid."),
        ("Are snakehead fish aggressive?",
         "Most are, to varying degrees. Channa bleheri and Channa andrao are comparatively mild, while Channa micropeltes, Channa marulius and Channa argus are seriously aggressive. Every species becomes far more aggressive when spawning, and conspecific aggression between snakeheads is the leading cause of death in mixed setups."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/types/", "Snakehead Types & Species"),
        ("/guides/snakehead-fish-care/tank-size/", "Snakehead Tank Size"),
        ("/guides/snakehead-fish-care/feeding/", "What Snakeheads Eat"),
        ("/wiki/snakehead-fish/", "Snakehead Species Profile"),
    ],
}

# ════════════════════════════════════════════════════════════════
# TYPES — Snakehead Types & Species
# ════════════════════════════════════════════════════════════════
TYPES_BODY = """    <p>&ldquo;Snakehead&rdquo; covers more than 50 described <em>Channa</em> species plus three African <em>Parachanna</em>, and the trade names attached to them are a mess. &ldquo;Dwarf snakehead&rdquo; has been used for at least six different fish, &ldquo;red snakehead&rdquo; usually means a juvenile of a species that grows to four feet, and &ldquo;blue snakehead&rdquo; is a colour morph label rather than a species. <strong>Buy on the scientific name.</strong> The difference between <em>Channa andrao</em> and <em>Channa micropeltes</em> is the difference between a 30-gallon tank and a swimming pool.</p>

    <h2 id="trade-names">Trade Names Decoded</h2>
    <table class="ptbl">
      <tr><th>Common name in shops</th><th>Usually means</th><th>Adult size</th></tr>
      <tr><td>Dwarf snakehead</td><td><em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em>, <em>C. limbata</em></td><td>4&ndash;8 in</td></tr>
      <tr><td>Blue snakehead / blue bleheri</td><td><em>C. andrao</em></td><td>4&ndash;5 in</td></tr>
      <tr><td>Rainbow snakehead</td><td><em>C. bleheri</em></td><td>6&ndash;7 in</td></tr>
      <tr><td>Peacock snakehead</td><td><em>C. pulchra</em></td><td>10&ndash;12 in</td></tr>
      <tr><td>Golden cobra snakehead</td><td><em>C. aurantimaculata</em></td><td>14&ndash;16 in</td></tr>
      <tr><td>Golden snakehead</td><td><em>C. stewartii</em> (sometimes <em>C. aurantimaculata</em>)</td><td>10&ndash;12 in</td></tr>
      <tr><td>Emperor snakehead</td><td><em>C. marulioides</em></td><td>24&ndash;26 in</td></tr>
      <tr><td>Bullseye / great snakehead</td><td><em>C. marulius</em></td><td>3&ndash;4 ft</td></tr>
      <tr><td>Red snakehead / toman</td><td><em>C. micropeltes</em> juvenile</td><td>3&ndash;4 ft as an adult</td></tr>
      <tr><td>Giant snakehead</td><td><em>C. micropeltes</em></td><td>3&ndash;4 ft</td></tr>
      <tr><td>Striped / chevron snakehead</td><td><em>C. striata</em></td><td>2&ndash;3 ft</td></tr>
      <tr><td>Northern snakehead</td><td><em>C. argus</em></td><td>2&ndash;3 ft</td></tr>
      <tr><td>Chinese snakehead</td><td><em>C. asiatica</em></td><td>12&ndash;13 in</td></tr>
    </table>
    <div class="callout"><strong>The red snakehead trap.</strong> Juvenile <em>C. micropeltes</em> are sold at 3 inches with brilliant red and black stripes. Those colours disappear by 8 inches, the fish grows about an inch a month, and it ends up over three feet long. This is the single most regretted purchase in the snakehead hobby.</div>

    <h2 id="dwarf">Dwarf Snakeheads (4&ndash;8 inches)</h2>
    <p>These are the only <em>Channa</em> that belong in a normal aquarium. All are from the <em>gachua</em> group, all are paternal mouthbrooders, and all prefer cooler, softer water than most tropical fish.</p>

    <h3>Channa andrao &mdash; Blue Snakehead / Dwarf Channa</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-andrao-wikimedia-real.jpg" alt="Channa andrao dwarf snakehead in a planted aquarium showing blue and red fin edging" width="800" height="533" loading="lazy"/>
      <figcaption><em>Channa andrao</em> &mdash; the blue dwarf snakehead, the most aquarium-suitable species in the genus. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <ul>
      <li><strong>Size:</strong> 4&ndash;5 in (10&ndash;13 cm) &mdash; the smallest snakehead in the trade</li>
      <li><strong>Origin:</strong> Lefraguri swamp, West Bengal, India</li>
      <li><strong>Temperature:</strong> 64&ndash;79&deg;F (18&ndash;26&deg;C), with a winter cooldown</li>
      <li><strong>Tank:</strong> 30 gallons for a pair</li>
      <li><strong>Temperament:</strong> Mildest of the genus; pairs bond strongly</li>
    </ul>
    <p>Described only in 2013 and separated from <em>C. bleheri</em>, which is why it is still sold as &ldquo;blue bleheri&rdquo;. Deep blue-black body, red-and-white fin margins that intensify with age. If you want one snakehead and you can legally have it, this is the one.</p>

    <h3>Channa bleheri &mdash; Rainbow Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-bleheri-wikimedia-real.jpg" alt="Channa bleheri rainbow snakehead showing orange and red mottled markings" width="670" height="510" loading="lazy"/>
      <figcaption><em>Channa bleheri</em> &mdash; the rainbow snakehead from the Brahmaputra basin. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <ul>
      <li><strong>Size:</strong> 6&ndash;7 in (15&ndash;18 cm)</li>
      <li><strong>Origin:</strong> Brahmaputra basin, Assam, India</li>
      <li><strong>Temperature:</strong> 68&ndash;79&deg;F (20&ndash;26&deg;C)</li>
      <li><strong>Tank:</strong> 40&ndash;55 gallons for a pair</li>
      <li><strong>Notable:</strong> Lacks pelvic fins, like <em>C. asiatica</em></li>
    </ul>
    <p>Orange, red and cream mottling over a warm brown base. Sociable by snakehead standards and one of the few species sometimes kept as a small group in a large tank of grown-together juveniles.</p>

    <h3>Channa gachua and Channa limbata &mdash; Dwarf / Brown Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-gachua-wikimedia-real.jpg" alt="Male Channa gachua dwarf snakehead showing blue-edged fins" width="800" height="447" loading="lazy"/>
      <figcaption><em>Channa gachua</em> &mdash; a species complex rather than a single fish. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p><em>C. gachua</em> is best understood as a species complex spread from Iran to Indonesia. Many regional populations have been split off into separate species &mdash; <em>C. limbata</em>, <em>C. harcourtbutleri</em>, <em>C. burmanica</em> and others &mdash; and shop stock labelled &ldquo;gachua&rdquo; may be any of them. Expect 6&ndash;8 inches, 55 gallons, 68&ndash;79&deg;F, and considerable variation in temperament between populations.</p>

    <h2 id="medium">Medium Snakeheads (10&ndash;16 inches)</h2>

    <h3>Channa pulchra &mdash; Peacock Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-pulchra-wikimedia-real.jpg" alt="Channa pulchra peacock snakehead with blue-green spotted flanks" width="540" height="360" loading="lazy"/>
      <figcaption><em>Channa pulchra</em> &mdash; the peacock snakehead from Myanmar. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>10&ndash;12 inches, from the Rakhine Yoma range of Myanmar. Blue-green iridescent spotting over a bronze base. Wants 75 gallons minimum, 68&ndash;79&deg;F and a distinct cool season. More territorial than the true dwarfs but manageable as a single fish or bonded pair.</p>

    <h3>Channa aurantimaculata &mdash; Golden Cobra Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-aurantimaculata-wikimedia-real.jpg" alt="Channa aurantimaculata golden cobra snakehead with orange bars on a dark body" width="800" height="533" loading="lazy"/>
      <figcaption><em>Channa aurantimaculata</em> &mdash; golden cobra snakehead, Assam. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>14&ndash;16 inches of black body slashed with orange bars, from the Dibrugarh district of Assam. Spectacular and expensive. Needs 125 gallons, 61&ndash;79&deg;F and a genuine winter cooldown &mdash; kept warm year-round it declines within a few years. Aggressive to conspecifics outside of a bonded pair.</p>

    <h3>Channa asiatica &mdash; Chinese Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-asiatica-wikimedia-real.jpg" alt="Red-form Channa asiatica Chinese snakehead" width="800" height="533" loading="lazy"/>
      <figcaption><em>Channa asiatica</em> &mdash; subtropical, pelvic-finless, and cold-tolerant. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>12&ndash;13 inches, native to southern China and Taiwan. Subtropical: comfortable from the low 50s&deg;F to the upper 70s&deg;F, so it can be kept unheated in many homes. Lacks pelvic fins. A confident, personable fish that learns to take food from tongs quickly.</p>

    <h2 id="large">Large and Giant Snakeheads (2&ndash;4 feet)</h2>
    <div class="callout callout-warn"><strong>Reality check.</strong> Everything in this section outgrows a standard aquarium. A 3-foot fish needs a tank roughly 9 feet long and 4 feet wide &mdash; 800&ndash;1,000+ gallons. If you cannot build that room, do not buy the juvenile.</div>

    <h3>Channa micropeltes &mdash; Giant / Red Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-micropeltes-wikimedia-real.jpg" alt="Adult Channa micropeltes giant snakehead showing blue-grey adult coloration" width="800" height="400" loading="lazy"/>
      <figcaption><em>Channa micropeltes</em> &mdash; the giant snakehead, sold as a 3-inch red juvenile. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>The largest commonly traded species, reaching 3&ndash;4 ft (up to about 130 cm). Juveniles are red and black; adults are blue-grey with a pale belly. Fast-growing, powerfully built and the most aggressive snakehead in the trade &mdash; adults will strike at hands during maintenance. Tropical: 75&ndash;82&deg;F. Public aquarium territory.</p>

    <h3>Channa marulius &mdash; Bullseye Snakehead</h3>
    <p>3&ndash;4 ft, native from India through Southeast Asia and established as an invasive population in Broward County, Florida. Named for the black eyespot ringed in orange on the caudal peduncle, which is retained into adulthood. Tropical, 75&ndash;82&deg;F.</p>

    <h3>Channa marulioides &mdash; Emperor Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-marulioides-wikimedia-real.jpg" alt="Channa marulioides emperor snakehead showing yellow-edged scale pattern" width="640" height="426" loading="lazy"/>
      <figcaption><em>Channa marulioides</em> &mdash; the emperor snakehead of Borneo and Malaysia. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>24&ndash;26 inches, from Borneo, Sumatra and peninsular Malaysia. Often considered the most beautiful of the large species: a bold scale-edge pattern in gold and black with a caudal eyespot. Needs 250&ndash;400 gallons and 75&ndash;82&deg;F.</p>

    <h3>Channa striata &mdash; Striped / Chevron Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-striata-wikimedia-real.jpg" alt="Channa striata striped snakehead showing chevron flank markings" width="640" height="426" loading="lazy"/>
      <figcaption><em>Channa striata</em> &mdash; the striped snakehead, farmed as food across Southeast Asia. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>2&ndash;3 ft. The most widely farmed snakehead in Asia and a staple food fish, which is why it is cheap and frequently exported. Extremely hardy, extremely adaptable, and correspondingly the species most likely to establish itself if released. Tropical, 75&ndash;82&deg;F.</p>

    <h3>Channa argus &mdash; Northern Snakehead</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-argus-wikimedia-real.jpg" alt="Channa argus northern snakehead showing mottled brown temperate coloration" width="800" height="467" loading="lazy"/>
      <figcaption><em>Channa argus</em> &mdash; the northern snakehead, the invasive species behind the US and EU bans. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p>2&ndash;3 ft, native to China, Korea and eastern Russia. Genuinely temperate &mdash; it survives under ice and tolerates 50&ndash;79&deg;F &mdash; which is exactly why it established in the Potomac River after 2002 and why it is banned across the EU and UK as well as the US. Not an aquarium fish under any circumstances.</p>

    <h3>Channa lucius and Channa barca</h3>
    <figure class="fig">
      <img src="/assets/encyclopedia/real/channa-lucius-wikimedia-real.jpg" alt="Channa lucius forest snakehead showing barred flanks" width="640" height="426" loading="lazy"/>
      <figcaption><em>Channa lucius</em> &mdash; the forest or splendid snakehead. Photo via Wikimedia Commons.</figcaption>
    </figure>
    <p><em>C. lucius</em> reaches about 16&ndash;20 inches and is a slender, heavily barred forest-stream species from Southeast Asia. <em>C. barca</em>, from a small area of the Brahmaputra in Assam, reaches roughly 3 ft, lives in burrows dug into riverbanks, and is one of the most expensive freshwater aquarium fish in the world &mdash; individual specimens have sold for thousands of dollars. Both are advanced-keeper fish at best.</p>

    <h2 id="picking">Picking the Right Species</h2>
    <table class="ptbl">
      <tr><th>If you have&hellip;</th><th>Realistic options</th></tr>
      <tr><td>30&ndash;40 gallons</td><td><em>C. andrao</em> (single or bonded pair)</td></tr>
      <tr><td>55 gallons</td><td><em>C. bleheri</em>, <em>C. gachua</em>, <em>C. limbata</em></td></tr>
      <tr><td>75&ndash;125 gallons</td><td><em>C. pulchra</em>, <em>C. asiatica</em>, <em>C. stewartii</em>, <em>C. aurantimaculata</em></td></tr>
      <tr><td>250&ndash;400 gallons</td><td><em>C. marulioides</em>, <em>C. lucius</em></td></tr>
      <tr><td>Under 30 gallons</td><td>No snakehead. Consider a <a href="/guides/betta-care-guide/">betta</a> or <a href="/guides/german-blue-ram-care-guide/">dwarf cichlid</a> instead.</td></tr>
    </table>
    <p>Once you have chosen, size the tank properly on the <a href="/guides/snakehead-fish-care/tank-size/">snakehead tank size guide</a> and set the temperature from the <a href="/guides/snakehead-fish-care/water-parameters/">water parameters guide</a> &mdash; the subtropical species are the ones most often killed by kindness in a heated tropical tank.</p>
"""

TYPES = {
    "slug": "types",
    "title": "Types of Snakehead Fish: 13 Channa Species Compared (With Photos)",
    "meta_desc": "Snakehead fish species compared: dwarf Channa andrao and bleheri, peacock, golden cobra, emperor, bullseye, giant red and northern - size and tank needs.",
    "h1": "Types of Snakehead Fish (Channa Species)",
    "hero_tag": "Types & Species",
    "hero_meta": "\U0001F3A8 50+ species &nbsp;|&nbsp; \U0001F4CF 4 in to 4 ft &nbsp;|&nbsp; \U0001F50D Buy on the scientific name",
    "toc_sections": [
        ("trade-names", "Trade Names Decoded"),
        ("dwarf", "Dwarf Snakeheads"),
        ("medium", "Medium Snakeheads"),
        ("large", "Large & Giant Snakeheads"),
        ("picking", "Picking a Species"),
    ],
    "body": TYPES_BODY,
    "faqs": [
        ("What is the smallest snakehead fish?",
         "Channa andrao, the blue dwarf snakehead from West Bengal, is the smallest species in the trade at 4-5 inches. Channa bleheri, the rainbow snakehead, is next at 6-7 inches. Both can be kept in a 30-55 gallon tank with a sealed lid."),
        ("What is a red snakehead fish?",
         "Red snakehead is a trade name for juvenile Channa micropeltes, the giant snakehead. The red and black striping fades by about 8 inches and the fish grows roughly an inch a month to over 3 feet, so it is not a home aquarium species despite being sold at 3 inches."),
        ("What is the difference between Channa andrao and Channa bleheri?",
         "Channa andrao was split from Channa bleheri in 2013 and is still sold as blue bleheri. Andrao stays smaller at 4-5 inches with a deep blue-black body and red-and-white fin margins, while bleheri reaches 6-7 inches with orange and cream mottling on a warm brown base."),
        ("Which snakehead is best for a home aquarium?",
         "Channa andrao is the best choice where snakeheads are legal: 4-5 inches, the mildest temperament in the genus, and comfortable in a 30-gallon tank. Channa bleheri and Channa asiatica are good second choices for 55 and 75 gallon tanks respectively."),
        ("How big does a northern snakehead get?",
         "Channa argus reaches 2-3 feet (roughly 60-100 cm). It is a temperate species that tolerates 50-79F and survives under ice, which is why it established in the Potomac River and is banned across the US, UK and EU."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
        ("/guides/snakehead-fish-care/tank-size/", "Snakehead Tank Size"),
        ("/guides/snakehead-fish-care/size-growth/", "Size & Growth Rate"),
        ("/wiki/snakehead-fish/", "Snakehead Species Profile"),
    ],
}

# ════════════════════════════════════════════════════════════════
# TANK SIZE — Tank Size & Setup
# ════════════════════════════════════════════════════════════════
TANK_BODY = """    <p>There is no single snakehead fish tank size, because the genus spans 4-inch dwarfs and 4-foot giants. What every species shares is the shape of the requirement: <strong>floor area over water volume, a locked lid over everything else</strong>. A snakehead in a tall tank with a loose cover is a snakehead on the carpet.</p>

    <h2 id="rule">The Sizing Rule</h2>
    <p>Ambush predators need room to turn, not room to swim laps. Size the footprint first:</p>
    <div class="callout"><strong>Tank length &ge; 3&times; adult body length. Tank width &ge; 1.5&times; adult body length.</strong> Height is almost irrelevant &mdash; 18&ndash;24 inches is plenty for any species, and a shallower tank makes the mandatory trip to the surface for air easier.</div>
    <p>Work from the <em>adult</em> size of your species, not the fish in the bag. Snakeheads do not stop growing to fit the tank; a stunted snakehead is a deformed one with a shortened life. Check adult sizes on the <a href="/guides/snakehead-fish-care/types/">types and species page</a> and confirm your gallons with the <a href="/tools/tank-size-calculator/">tank size calculator</a>.</p>

    <h2 id="by-species">Snakehead Tank Size by Species</h2>
    <table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Minimum footprint</th><th>Minimum volume</th></tr>
      <tr><td><em>C. andrao</em> (blue dwarf)</td><td>4&ndash;5 in</td><td>30 &times; 12 in</td><td>30 gal (pair)</td></tr>
      <tr><td><em>C. bleheri</em> (rainbow)</td><td>6&ndash;7 in</td><td>36 &times; 15 in</td><td>40&ndash;55 gal</td></tr>
      <tr><td><em>C. gachua</em> / <em>C. limbata</em></td><td>6&ndash;8 in</td><td>36 &times; 18 in</td><td>55 gal</td></tr>
      <tr><td><em>C. pulchra</em> (peacock)</td><td>10&ndash;12 in</td><td>48 &times; 18 in</td><td>75 gal</td></tr>
      <tr><td><em>C. asiatica</em> (Chinese)</td><td>12&ndash;13 in</td><td>48 &times; 18 in</td><td>75 gal</td></tr>
      <tr><td><em>C. aurantimaculata</em> (golden cobra)</td><td>14&ndash;16 in</td><td>60 &times; 24 in</td><td>125 gal</td></tr>
      <tr><td><em>C. lucius</em> (forest)</td><td>16&ndash;20 in</td><td>72 &times; 24 in</td><td>180 gal</td></tr>
      <tr><td><em>C. marulioides</em> (emperor)</td><td>24&ndash;26 in</td><td>84 &times; 30 in</td><td>300 gal</td></tr>
      <tr><td><em>C. striata</em> / <em>C. argus</em></td><td>24&ndash;36 in</td><td>108 &times; 36 in</td><td>500+ gal</td></tr>
      <tr><td><em>C. micropeltes</em> (giant)</td><td>36&ndash;48 in</td><td>144 &times; 48 in</td><td>1,000+ gal</td></tr>
    </table>
    <p>The bottom three rows are indoor-pond or public-aquarium projects. If a shop is selling you one of those as a 3-inch juvenile for a 55-gallon tank, they are selling you a problem you will meet in about eighteen months. See <a href="/guides/snakehead-fish-care/size-growth/">snakehead growth rate</a> for how fast that happens.</p>

    <h2 id="lid">The Lid: The Most Important Piece of Equipment</h2>
    <p>More captive snakeheads die on the floor than from any disease. They are strong, deliberate jumpers, they push at loose covers with the flat of the head, and they will find a 1-inch gap around a filter pipe. Build the lid properly:</p>
    <ul>
      <li><strong>Full coverage, no open corners.</strong> Glass or rigid plastic, cut to the tank, with cutouts sealed around hoses using mesh or foam.</li>
      <li><strong>Weighted or latched.</strong> A large snakehead can lift an unsecured glass lid. Books, clamps or latches &mdash; something positive.</li>
      <li><strong>Leave a 2&ndash;4 inch air gap</strong> between the water surface and the lid. This is not optional. Snakeheads breathe atmospheric air and the air they breathe should be warm and humid; a lid resting on the water surface denies them air, and an open tank in a cold room chills the breathing organ.</li>
      <li><strong>Mind the water level.</strong> Top up so the gap stays in range &mdash; evaporation that widens the gap is fine, but a tank filled to the rim is a drowning risk.</li>
      <li><strong>Check after every water change.</strong> The lid left ajar for ten minutes is the classic loss.</li>
    </ul>
    <div class="callout callout-warn"><strong>Do not use a mesh screen alone.</strong> Screen tops that work for cichlids let the humid air layer escape. Snakeheads need a solid cover that traps warm moist air above the water.</div>

    <h2 id="layout">Aquascape and Layout</h2>
    <p>Wild <em>Channa</em> live in sluggish, shaded, structure-rich water &mdash; swamps, paddy field margins, forest streams. Reproduce that and the fish stops hiding:</p>
    <ul>
      <li><strong>Dense cover:</strong> driftwood tangles, caves, terracotta pipe, dried leaf litter (Indian almond, oak). A snakehead with three hiding places is calm; one with none stays wedged in a corner permanently.</li>
      <li><strong>Floating plants:</strong> water lettuce, frogbit or salvinia. Dim overhead light is the single fastest way to bring out natural colour and reduce skittishness &mdash; but leave clear patches so the fish can reach the surface for air.</li>
      <li><strong>Soft substrate:</strong> sand or fine gravel. Several species dig.</li>
      <li><strong>Open floor space:</strong> keep the front third clear so the fish has somewhere to sit and watch the room.</li>
    </ul>

    <h2 id="equipment">Filtration, Flow and Heating</h2>
    <table class="ptbl">
      <tr><th>Equipment</th><th>Specification</th><th>Why</th></tr>
      <tr><td>Filtration</td><td>Rated 1.5&ndash;2&times; tank volume</td><td>Whole-seafood diet produces a heavy waste load</td></tr>
      <tr><td>Flow</td><td>Low &mdash; baffle strong returns</td><td>Native habitat is nearly still water</td></tr>
      <tr><td>Heater</td><td>Guarded, and only if the species needs it</td><td>Subtropical species often need no heater at all</td></tr>
      <tr><td>Lighting</td><td>Dim, or heavily shaded by floaters</td><td>Bright light causes hiding and washed-out colour</td></tr>
      <tr><td>Water changes</td><td>30&ndash;50% weekly</td><td>Keeps nitrate under 30 ppm</td></tr>
    </table>
    <p>Canister filters are the usual choice because the intake and return can be sealed cleanly through the lid. Whatever you use, secure the intake &mdash; a curious snakehead will investigate an unguarded strainer, and a juvenile can be pinned to it.</p>

    <h2 id="quarantine">Quarantine Tank</h2>
    <p>Most snakeheads in the trade are wild-caught and arrive with internal parasites. Run a bare-bottom quarantine tank of at least 20 gallons &mdash; with its own sealed lid &mdash; for <strong>4&ndash;6 weeks</strong> before the fish enters a display tank. It is far easier to dose and observe a fish in a bare tank than to medicate a planted display later. See <a href="/guides/snakehead-fish-care/diseases/">snakehead diseases</a> for what to treat for.</p>

    <h2 id="mistakes">Common Setup Mistakes</h2>
    <ul>
      <li><strong>Buying the tank for the juvenile.</strong> The fish you bought at 3 inches is not the fish you will own in a year.</li>
      <li><strong>A tall tank instead of a long one.</strong> Height adds gallons on the receipt and nothing the fish can use.</li>
      <li><strong>No air gap.</strong> Filling to the rim under a tight lid is a drowning hazard for an obligate air-breather.</li>
      <li><strong>Strong flow.</strong> A powerhead aimed across the tank keeps an ambush predator permanently unsettled.</li>
      <li><strong>Bright light and a bare tank.</strong> Produces a pale, hidden, jumpy fish and then a dead one behind the cabinet.</li>
    </ul>
"""

TANK = {
    "slug": "tank-size",
    "title": "Snakehead Fish Tank Size: Minimum Gallons by Channa Species",
    "meta_desc": "Snakehead fish tank size by species, from 30 gallons for a dwarf Channa andrao to 1,000+ for a giant - plus lid, air gap and filtration specs.",
    "h1": "Snakehead Fish Tank Size and Setup",
    "hero_tag": "Tank Size & Setup",
    "hero_meta": "\U0001F5C3️ 30 gal for a dwarf pair &nbsp;|&nbsp; \U0001F4D0 Length &ge; 3&times; body &nbsp;|&nbsp; \U0001F512 Weighted lid mandatory",
    "toc_sections": [
        ("rule", "The Sizing Rule"),
        ("by-species", "Tank Size by Species"),
        ("lid", "The Lid & Air Gap"),
        ("layout", "Aquascape & Layout"),
        ("equipment", "Filtration & Equipment"),
        ("quarantine", "Quarantine Tank"),
        ("mistakes", "Common Mistakes"),
    ],
    "body": TANK_BODY,
    "faqs": [
        ("What is the minimum tank size for a snakehead fish?",
         "For the smallest species, Channa andrao at 4-5 inches, 30 gallons with a 30 x 12 inch footprint suits a bonded pair. Channa bleheri needs 40-55 gallons, mid-sized species such as Channa aurantimaculata need 125 gallons, and giant species like Channa micropeltes need 1,000 gallons or more."),
        ("Can a snakehead live in a 55 gallon tank?",
         "Yes, for dwarf species. Channa bleheri, Channa gachua and Channa limbata are all comfortable in a 55 gallon tank with a 36 x 18 inch footprint. No species over about 8 inches adult length should be housed in a 55 permanently."),
        ("Do snakehead fish need a lid?",
         "Yes, and it is the most important item in the setup. Snakeheads are powerful jumpers that push at loose covers and escape through filter cutouts - more captive snakeheads die on the floor than from disease. Use a full, weighted or latched solid cover with all gaps sealed, and leave a 2-4 inch humid air gap above the water."),
        ("Why do snakehead tanks need an air gap?",
         "Snakeheads are obligate air-breathers and must surface to gulp atmospheric air. The 2-4 inch gap between water and lid holds a layer of warm humid air for them to breathe. Filling the tank to the rim under a tight lid can drown the fish, and an open top in a cold room chills the breathing organ."),
        ("How much water flow do snakeheads need?",
         "Very little. Channa come from sluggish swamps, paddy field margins and slow forest streams, so strong flow keeps them unsettled and hiding. Use filtration rated 1.5-2x tank volume for waste capacity, but baffle the return so the water in the tank is nearly still."),
    ],
    "related": [
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
        ("/guides/snakehead-fish-care/types/", "Snakehead Types & Species"),
        ("/guides/snakehead-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
    ],
}

# ════════════════════════════════════════════════════════════════
# WATER — Water Parameters & Temperature
# ════════════════════════════════════════════════════════════════
WATER_BODY = """    <p>The single most common long-term mistake with snakeheads is keeping a subtropical species at tropical temperatures. It does not kill the fish quickly &mdash; it shortens the lifespan, suppresses breeding and produces a fish that slowly stops eating over two or three years. Before you set a heater, find out where your species comes from.</p>

    <h2 id="targets">Snakehead Water Parameters at a Glance</h2>
    <table class="ptbl">
      <tr><th>Parameter</th><th>Target</th><th>Act now if</th></tr>
      <tr><td>Temperature</td><td>Species-dependent &mdash; see below</td><td>Outside the species range for more than a few days</td></tr>
      <tr><td>pH</td><td>6.0&ndash;7.5</td><td>Below 5.5 or above 8.0</td></tr>
      <tr><td>GH (general hardness)</td><td>2&ndash;15 dGH</td><td>Above 20 dGH</td></tr>
      <tr><td>KH (carbonate hardness)</td><td>2&ndash;10 dKH</td><td>Below 2 dKH &mdash; pH becomes unstable</td></tr>
      <tr><td>Ammonia (NH&#8323;)</td><td>0 ppm</td><td>Any reading above 0</td></tr>
      <tr><td>Nitrite (NO&#8322;)</td><td>0 ppm</td><td>Any reading above 0</td></tr>
      <tr><td>Nitrate (NO&#8323;)</td><td>Under 30 ppm</td><td>Above 50 ppm</td></tr>
      <tr><td>Flow</td><td>Low &mdash; near-still</td><td>Fish is permanently pinned or unsettled</td></tr>
      <tr><td>Air gap above water</td><td>2&ndash;4 in, warm and humid</td><td>Lid sits on the water, or the room is cold</td></tr>
    </table>
    <p>Test ammonia, nitrite and nitrate weekly with a liquid kit. Paper strips are fine for spotting a trend but not for deciding on a treatment. Feed a reading into the <a href="/tools/water-parameter-checker/">water parameter checker</a> to see which number to fix first.</p>

    <h2 id="temperature">Snakehead Fish Temperature by Species Group</h2>
    <p><em>Channa</em> occur from equatorial Borneo to the Amur River, where the water freezes. Three broad groups matter:</p>
    <table class="ptbl">
      <tr><th>Group</th><th>Species</th><th>Year-round range</th><th>Cool season</th></tr>
      <tr><td>Tropical lowland</td><td><em>C. micropeltes</em>, <em>C. striata</em>, <em>C. lucius</em>, <em>C. marulioides</em>, <em>C. marulius</em></td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td><td>Not needed</td></tr>
      <tr><td>Subtropical / highland</td><td><em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em>, <em>C. limbata</em>, <em>C. pulchra</em>, <em>C. stewartii</em>, <em>C. aurantimaculata</em></td><td>68&ndash;79&deg;F (20&ndash;26&deg;C)</td><td>8&ndash;12 weeks at 59&ndash;68&deg;F (15&ndash;20&deg;C)</td></tr>
      <tr><td>Temperate</td><td><em>C. asiatica</em>, <em>C. argus</em></td><td>50&ndash;79&deg;F (10&ndash;26&deg;C)</td><td>A genuine cold winter</td></tr>
    </table>
    <div class="callout"><strong>Many snakeheads need no heater.</strong> In a home held at 68&ndash;74&deg;F, <em>C. andrao</em>, <em>C. bleheri</em> and <em>C. asiatica</em> are perfectly comfortable unheated for most of the year. If you fit a heater at all, set it as a floor (say 66&deg;F) rather than a target.</div>

    <h2 id="cooldown">The Winter Cooldown</h2>
    <p>Subtropical and temperate <em>Channa</em> evolved with a seasonal cycle, and captive fish denied it show a consistent pattern: reduced colour, reluctance to spawn, gradual loss of appetite over years, and a shortened lifespan. Giving them a cool season is straightforward:</p>
    <ol>
      <li><strong>Late autumn:</strong> turn the heater down or off and let the tank drift with room temperature. Drop no faster than 2&ndash;3&deg;F per day.</li>
      <li><strong>8&ndash;12 weeks at 59&ndash;68&deg;F</strong> (15&ndash;20&deg;C) for subtropical species. Colder for <em>C. asiatica</em> and <em>C. argus</em>.</li>
      <li><strong>Feed much less.</strong> Metabolism slows. Once or twice a week is plenty, and a fish that refuses food entirely during the cool period is behaving normally.</li>
      <li><strong>Spring:</strong> raise the temperature over two to three weeks, resume heavier feeding, and increase water change volume with slightly cooler soft water. This is also the standard <a href="/guides/snakehead-fish-care/breeding/">spawning trigger</a>.</li>
    </ol>
    <p>Keep the biological filter running throughout. Nitrifying bacteria slow in cold water but do not die, and the reduced feeding matches the reduced filtration capacity.</p>

    <h2 id="ph-hardness">pH, Hardness and Water Chemistry</h2>
    <p>Most <em>Channa</em> come from soft, slightly acidic, tannin-stained water. Aim for <strong>pH 6.0&ndash;7.5 and 2&ndash;15 dGH</strong>, and prioritise stability over hitting a number. A steady 7.6 beats a pH you chase to 6.8 with chemicals every week.</p>
    <ul>
      <li><strong>Leaf litter and driftwood</strong> release tannins that gently lower pH, tint the water and have mild antibacterial effects. This is the natural way to get there and snakeheads visibly prefer it.</li>
      <li><strong>Avoid pH-down products.</strong> They knock KH out and then the pH swings, which is worse than the original reading.</li>
      <li><strong>Hard tap water</strong> is tolerated by most species but mix with RO if you are above 20 dGH, especially for <em>C. andrao</em> and <em>C. bleheri</em>.</li>
    </ul>

    <h2 id="maintenance">Water Changes and Nitrate Control</h2>
    <p>Snakeheads eat whole seafood and produce a lot of waste for their size. Change <strong>30&ndash;50% weekly</strong> and match the new water's temperature and pH to the tank. Points that matter more here than in a community tank:</p>
    <ul>
      <li><strong>Siphon uneaten food the same day.</strong> A shrimp missed under driftwood spikes ammonia within 24 hours.</li>
      <li><strong>Nitrate creep causes colour loss</strong> before it causes anything dramatic. If a snakehead has gone dull and the other numbers are clean, test nitrate.</li>
      <li><strong>Dechlorinate everything</strong>, including top-off water.</li>
      <li><strong>Close the lid afterwards.</strong> The moments after a water change are when most snakeheads jump.</li>
    </ul>
    <div class="callout callout-warn"><strong>A note on oxygen.</strong> Because they breathe air, snakeheads survive low dissolved oxygen that would kill other fish. That is a hazard, not a feature &mdash; it means a snakehead will look fine in water that is quietly going wrong. Test on schedule rather than waiting for the fish to tell you.</div>

    <h2 id="cycling">Cycling and New Tanks</h2>
    <p>Cycle the tank fully before the fish arrives: dose ammonia to 2&ndash;3 ppm and wait until both ammonia and nitrite read 0 within 24 hours. That takes 4&ndash;6 weeks from scratch, or a few days with seeded media from an established filter. A snakehead in an uncycled tank will not die dramatically &mdash; it will sit through the ammonia spike, breathing air, developing gill damage and the burn marks that later show as dark patches. See <a href="/guides/snakehead-fish-care/diseases/">snakehead diseases and symptoms</a>.</p>
"""

WATER = {
    "slug": "water-parameters",
    "title": "Snakehead Fish Water Parameters & Temperature (Channa by Species)",
    "meta_desc": "Snakehead fish water parameters: temperature by species, pH 6.0-7.5, hardness, nitrate limits and the winter cooldown that subtropical Channa require.",
    "h1": "Snakehead Fish Water Parameters and Temperature",
    "hero_tag": "Water & Temperature",
    "hero_meta": "\U0001F321️ 68&ndash;79&deg;F for most dwarfs &nbsp;|&nbsp; \U0001F9EA pH 6.0&ndash;7.5 &nbsp;|&nbsp; ❄️ Cool season required",
    "toc_sections": [
        ("targets", "Parameters at a Glance"),
        ("temperature", "Temperature by Species"),
        ("cooldown", "The Winter Cooldown"),
        ("ph-hardness", "pH & Hardness"),
        ("maintenance", "Water Changes"),
        ("cycling", "Cycling a New Tank"),
    ],
    "body": WATER_BODY,
    "faqs": [
        ("What temperature do snakehead fish need?",
         "It depends on the species. Tropical lowland species such as Channa micropeltes and Channa striata want 75-82F. Subtropical dwarfs including Channa andrao, Channa bleheri and Channa aurantimaculata want 68-79F with an 8-12 week cool season at 59-68F. Temperate species like Channa asiatica and Channa argus tolerate 50-79F."),
        ("What pH do snakehead fish need?",
         "Aim for pH 6.0-7.5 with hardness of 2-15 dGH. Most Channa come from soft, slightly acidic, tannin-stained water, and driftwood plus leaf litter is a better way to get there than pH-adjusting chemicals, which destabilise carbonate hardness and cause swings."),
        ("Do snakehead fish need a heater?",
         "Often not. In a home held at 68-74F, Channa andrao, Channa bleheri and Channa asiatica are comfortable unheated for most of the year. Tropical species such as Channa micropeltes and Channa striata do need a heater to hold 75-82F. Where a heater is used for a subtropical species, set it as a floor rather than a target."),
        ("Why do snakeheads need a winter cooldown?",
         "Subtropical and temperate Channa evolved with a seasonal cycle. Denied it, they show faded colour, refuse to spawn, gradually lose appetite over years and live shorter lives. Drop the tank to 59-68F for 8-12 weeks, feed sparingly, then warm it over two to three weeks in spring - which also triggers spawning."),
        ("How often should I change the water in a snakehead tank?",
         "Change 30-50% weekly. Snakeheads eat whole seafood and produce a heavy waste load, and nitrate creep above 30 ppm shows up as colour loss before anything more obvious. Siphon uneaten food the same day, and always close the lid immediately afterwards - post-water-change is when most snakeheads jump."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/snakehead-fish-care/diseases/", "Diseases & Symptoms"),
        ("/guides/snakehead-fish-care/tank-size/", "Tank Size & Setup"),
        ("/guides/aquarium-water-parameters/", "Aquarium Water Parameters"),
    ],
}

# ════════════════════════════════════════════════════════════════
# FEEDING — Food & Feeding
# ════════════════════════════════════════════════════════════════
FEEDING_BODY = """    <p>Snakeheads are carnivores, and in the wild that mostly means fish, frogs, crustaceans and insects. In an aquarium, the intuitive translation of that &mdash; a tank of live feeder fish &mdash; is the worst option available. It causes vitamin deficiency, it imports disease, and it teaches a fish that will live a decade to refuse everything else.</p>

    <h2 id="what-they-eat">What Do Snakehead Fish Eat?</h2>
    <p>Build the diet from thawed frozen and fresh whole foods, then wean onto pellets so long-term nutrition is easy to control.</p>
    <table class="ptbl">
      <tr><th>Food</th><th>Suits</th><th>Notes</th></tr>
      <tr><td>Shell-on shrimp and prawn</td><td>All sizes (chop for dwarfs)</td><td>Staple. The shell supplies chitin and carotenoids that hold red colour</td></tr>
      <tr><td>Mussel and clam meat</td><td>Medium and large</td><td>Rich; use as a rotation item, not a staple</td></tr>
      <tr><td>Krill and mysis</td><td>Dwarf and medium</td><td>Excellent colour food, readily accepted</td></tr>
      <tr><td>Silversides and lancefish</td><td>Medium and large</td><td>Whole-fish nutrition without live feeder risk</td></tr>
      <tr><td>White fish fillet (tilapia, cod, pollock)</td><td>All sizes</td><td>Lean, thiaminase-free, good for weaning</td></tr>
      <tr><td>Earthworms</td><td>All sizes</td><td>Close to irresistible; superb conditioning food</td></tr>
      <tr><td>Crickets, dubia roaches, mealworms</td><td>Dwarf and medium</td><td>Dwarf <em>Channa</em> are natural insectivores &mdash; feed sparingly, they are fatty</td></tr>
      <tr><td>Bloodworm, blackworm</td><td>Dwarf species, juveniles</td><td>Good starter food for a new or shy fish</td></tr>
      <tr><td>Carnivore / predator pellets</td><td>All, once weaned</td><td>The goal. Balanced vitamins and minerals in every bite</td></tr>
    </table>

    <h2 id="avoid">What Not to Feed</h2>
    <div class="callout callout-warn"><strong>Do not feed goldfish or rosy red minnows.</strong> Both contain <strong>thiaminase</strong>, an enzyme that destroys vitamin B1. A snakehead fed a thiaminase-heavy diet develops neurological symptoms over months &mdash; loss of coordination, erratic swimming, eventual death &mdash; and the cause is rarely identified in time.</div>
    <ul>
      <li><strong>Live feeder fish generally.</strong> Beyond thiaminase, feeders are the most efficient way to introduce ich, flukes, internal parasites and bacterial infections into a closed system.</li>
      <li><strong>Mammal and bird meat</strong> &mdash; beef heart, chicken, pork. The fat profile is wrong for a fish and causes fatty liver disease.</li>
      <li><strong>Anything from the pond or a local stream</strong> unless you are confident about parasites.</li>
      <li><strong>Anything larger than the eye-to-gill distance</strong> for a nervous or newly imported fish &mdash; it will be dropped and left to rot.</li>
    </ul>
    <p>Live food is not banned outright: earthworms, crickets, roaches and river shrimp from a clean source are all excellent and satisfy the hunting behaviour without the thiaminase or disease problem.</p>

    <h2 id="how-often">How Often to Feed Snakehead Fish</h2>
    <table class="ptbl">
      <tr><th>Stage</th><th>Frequency</th><th>Portion</th></tr>
      <tr><td>Fry (under 1 in)</td><td>2&ndash;3&times; daily</td><td>Baby brine shrimp, microworm, crushed pellet</td></tr>
      <tr><td>Juvenile (1&ndash;4 in)</td><td>Daily</td><td>What is eaten in about a minute</td></tr>
      <tr><td>Sub-adult</td><td>Every other day</td><td>2&ndash;3 pieces roughly eye-sized</td></tr>
      <tr><td>Adult</td><td>2&ndash;3&times; per week</td><td>Enough to produce a slight belly bulge, no more</td></tr>
      <tr><td>Cool season (subtropical)</td><td>Once weekly or less</td><td>Refusal during the cooldown is normal</td></tr>
    </table>
    <div class="callout"><strong>Underfeeding an adult snakehead is almost impossible; overfeeding is easy.</strong> Obesity, fatty liver and buoyancy problems are far more common in captive <em>Channa</em> than malnutrition. A healthy adult should look muscular and slightly lean, not barrel-shaped. Fasting one day a week is good practice.</div>

    <h2 id="weaning">Weaning a Snakehead Onto Pellets</h2>
    <p>Most <em>Channa</em> can be converted to prepared food, which makes vitamin balance and holiday care much simpler. It takes patience rather than technique:</p>
    <ol>
      <li><strong>Start hungry.</strong> Fast the fish 3&ndash;5 days. An adult snakehead is in no danger from that.</li>
      <li><strong>Use tongs and movement.</strong> Snakeheads strike at movement, not smell. Hold a soaked pellet in long tongs and twitch it in front of the fish.</li>
      <li><strong>Scent the pellet.</strong> Soak pellets in the thaw water from frozen krill or shrimp for a few minutes first.</li>
      <li><strong>Mix the ratio down.</strong> Once pellets are taken, offer them alongside a favourite food and slowly shift the proportion.</li>
      <li><strong>Repeat, and accept refusals.</strong> A fish that ignores the pellet today may take it on the fourth attempt. Remove uneaten food each time.</li>
    </ol>
    <p>Keep frozen foods in the rotation even after weaning &mdash; two or three pellet meals and one whole-food meal a week is a good balance.</p>

    <h2 id="not-eating">Snakehead Fish Not Eating</h2>
    <p>This is the most-searched snakehead problem, and most of the time nothing is wrong. Work through the causes in this order:</p>
    <ol>
      <li><strong>Recently imported or moved (most likely).</strong> New snakeheads commonly refuse food for two to four weeks. Dim the lights, add cover, stop approaching the tank, and offer a small item every second day. Remove it if untouched.</li>
      <li><strong>Wrong temperature for the species.</strong> A subtropical fish held at 82&deg;F, or a tropical fish at 68&deg;F, goes off food. Check against the <a href="/guides/snakehead-fish-care/water-parameters/">temperature table</a>.</li>
      <li><strong>Seasonal fast.</strong> During a cool period, refusal is normal and healthy.</li>
      <li><strong>Water quality.</strong> Test ammonia, nitrite and nitrate. Any ammonia or nitrite at all suppresses appetite.</li>
      <li><strong>Still full.</strong> An adult fed heavily three days ago may simply not be hungry. Snakeheads digest slowly.</li>
      <li><strong>Internal parasites.</strong> Suspect this when the fish eats and then spits, or eats normally but stays thin with a sunken belly and pale stringy faeces. Common in wild-caught imports &mdash; see <a href="/guides/snakehead-fish-care/diseases/">diseases and symptoms</a>.</li>
      <li><strong>Food fixation.</strong> A fish previously fed only feeder fish or only bloodworm may refuse everything else. Fast it and restart the weaning process above.</li>
    </ol>
    <p>Escalate only if refusal comes with weight loss, clamped fins, laboured breathing or colour collapse. A bright, alert snakehead sitting on the bottom refusing food for three weeks is a normal snakehead.</p>

    <h2 id="handling">Handling and Feeding Safety</h2>
    <p>Snakeheads learn feeding routines fast and will strike at a hand entering the tank, particularly larger species and any fish guarding fry. Use long tongs, feed at the far end from where you are working, and do maintenance at a different time of day from feeding so the fish does not associate the two.</p>
"""

FEEDING = {
    "slug": "feeding",
    "title": "What Do Snakehead Fish Eat? Best Food & Feeding Schedule (Channa)",
    "meta_desc": "What to feed snakehead fish: best foods, why feeder goldfish are dangerous, how often to feed by age, weaning onto pellets and why one stops eating.",
    "h1": "What Snakehead Fish Eat and How to Feed Them",
    "hero_tag": "Food & Feeding",
    "hero_meta": "\U0001F35A Carnivore &nbsp;|&nbsp; \U0001F4C5 Adults 2&ndash;3&times; weekly &nbsp;|&nbsp; \U0001F6AB No feeder goldfish",
    "toc_sections": [
        ("what-they-eat", "What They Eat"),
        ("avoid", "What Not to Feed"),
        ("how-often", "How Often to Feed"),
        ("weaning", "Weaning Onto Pellets"),
        ("not-eating", "Snakehead Not Eating"),
        ("handling", "Feeding Safety"),
    ],
    "body": FEEDING_BODY,
    "faqs": [
        ("What do snakehead fish eat?",
         "Snakeheads are carnivores. In an aquarium feed thawed frozen and fresh whole foods - shell-on shrimp and prawn, krill, mysis, mussel, silversides, white fish fillet and earthworms - plus insects such as crickets and dubia roaches for dwarf species. Most Channa can then be weaned onto quality carnivore pellets."),
        ("Can you feed snakeheads feeder goldfish?",
         "No. Goldfish and rosy red minnows contain thiaminase, an enzyme that destroys vitamin B1 and causes progressive neurological damage over months. Feeder fish are also the most efficient way to introduce ich, flukes and internal parasites into a tank. Use frozen seafood, earthworms and pellets instead."),
        ("How often should I feed a snakehead fish?",
         "Juveniles under 4 inches eat daily, sub-adults every other day, and adults only 2-3 times a week. Overfeeding causes obesity and fatty liver disease, which are far more common in captive snakeheads than malnutrition. Fasting one day a week is good practice, and subtropical species eat little or nothing during their cool season."),
        ("Why is my snakehead fish not eating?",
         "The most common reason is settling stress - newly imported snakeheads routinely refuse food for two to four weeks. Then check that the temperature matches the species, whether the fish is in its natural cool-season fast, and test ammonia and nitrite. Internal parasites are likely if the fish stays thin, spits food, or passes pale stringy waste. A bright, alert fish refusing food is rarely an emergency."),
        ("How do I get a snakehead to eat pellets?",
         "Fast the fish for 3-5 days, then hold a pellet in long tongs and twitch it in front of the fish - snakeheads strike at movement rather than smell. Soaking the pellet in thaw water from frozen krill helps. Once accepted, mix pellets with a favourite food and shift the proportion gradually, keeping some frozen food in the rotation."),
    ],
    "related": [
        ("/tools/fish-feeding-calculator/", "Fish Feeding Calculator"),
        ("/guides/snakehead-fish-care/diseases/", "Diseases & Symptoms"),
        ("/guides/snakehead-fish-care/size-growth/", "Size & Growth Rate"),
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
    ],
}

# ════════════════════════════════════════════════════════════════
# SIZE & GROWTH
# ════════════════════════════════════════════════════════════════
SIZE_BODY = """    <p>&ldquo;How big do snakehead fish get?&rdquo; has no single answer, and that is exactly why so many end up rehomed or, worse, released. The genus runs from a 4-inch dwarf to a 4-foot predator, and the fast-growing giants are the ones most often sold as inexpensive juveniles.</p>

    <h2 id="by-species">Snakehead Size by Species</h2>
    <table class="ptbl">
      <tr><th>Species</th><th>Typical adult size</th><th>Maximum recorded</th></tr>
      <tr><td><em>C. andrao</em></td><td>4&ndash;5 in (10&ndash;13 cm)</td><td>~5.5 in</td></tr>
      <tr><td><em>C. bleheri</em></td><td>6&ndash;7 in (15&ndash;18 cm)</td><td>~8 in</td></tr>
      <tr><td><em>C. gachua</em> / <em>C. limbata</em></td><td>6&ndash;8 in (15&ndash;20 cm)</td><td>~12 in</td></tr>
      <tr><td><em>C. pulchra</em></td><td>10&ndash;12 in (25&ndash;30 cm)</td><td>~12 in</td></tr>
      <tr><td><em>C. asiatica</em></td><td>12&ndash;13 in (30&ndash;34 cm)</td><td>~13 in</td></tr>
      <tr><td><em>C. aurantimaculata</em></td><td>14&ndash;16 in (35&ndash;40 cm)</td><td>~20 in</td></tr>
      <tr><td><em>C. lucius</em></td><td>16&ndash;20 in (40&ndash;50 cm)</td><td>~24 in</td></tr>
      <tr><td><em>C. marulioides</em></td><td>24&ndash;26 in (60&ndash;65 cm)</td><td>~26 in</td></tr>
      <tr><td><em>C. striata</em></td><td>24&ndash;35 in (60&ndash;90 cm)</td><td>~39 in</td></tr>
      <tr><td><em>C. barca</em></td><td>~35 in (90 cm)</td><td>~36 in</td></tr>
      <tr><td><em>C. argus</em></td><td>24&ndash;36 in (60&ndash;90 cm)</td><td>~40 in</td></tr>
      <tr><td><em>C. marulius</em></td><td>36&ndash;48 in (90&ndash;120 cm)</td><td>~48 in</td></tr>
      <tr><td><em>C. micropeltes</em></td><td>36&ndash;48 in (90&ndash;120 cm)</td><td>~51 in (130 cm)</td></tr>
    </table>
    <p>Aquarium specimens usually land at the lower end of these ranges; the maxima come from wild fish with unlimited space and food. That is not a licence to keep a large species small &mdash; it just means an emperor snakehead in a big tank will more likely stop around 24 inches than 26.</p>

    <h2 id="growth-rate">Snakehead Fish Growth Rate</h2>
    <p>Growth is fastest in the first year and slows steadily after sexual maturity. The rates that catch people out belong to the giants:</p>
    <table class="ptbl">
      <tr><th>Species</th><th>First-year growth</th><th>Adult size reached at</th></tr>
      <tr><td><em>C. andrao</em>, <em>C. bleheri</em></td><td>Roughly 0.3&ndash;0.5 in per month</td><td>12&ndash;18 months</td></tr>
      <tr><td><em>C. pulchra</em>, <em>C. aurantimaculata</em></td><td>Roughly 0.5&ndash;1 in per month</td><td>2&ndash;3 years</td></tr>
      <tr><td><em>C. marulioides</em>, <em>C. striata</em></td><td>Roughly 1&ndash;1.5 in per month</td><td>2&ndash;4 years</td></tr>
      <tr><td><em>C. micropeltes</em></td><td>Over 1 in per month &mdash; often 18&ndash;24 in in year one</td><td>3&ndash;4 years</td></tr>
    </table>
    <div class="callout callout-warn"><strong>The 3-inch giant snakehead.</strong> A red <em>C. micropeltes</em> juvenile bought in January is commonly a foot long by autumn and outgrowing a 75-gallon tank inside two years. Growth rate, not adult size, is what turns this purchase into a crisis.</div>

    <h2 id="stunting">Do Snakeheads Grow to the Size of the Tank?</h2>
    <p>No. This myth kills fish. What actually happens in an undersized tank is <strong>stunting</strong>: the skeleton and fins stop growing while the internal organs continue, producing spinal curvature, organ compression, chronic stress and a badly shortened life. A stunted snakehead is not a conveniently small snakehead &mdash; it is a deformed one.</p>
    <p>Poor growth in a correctly sized tank has three usual causes:</p>
    <ul>
      <li><strong>Nitrate above 40 ppm</strong> suppresses growth even when ammonia and nitrite read zero.</li>
      <li><strong>An unvaried diet</strong>, particularly a bloodworm-only or feeder-only diet, produces a thin fish that grows slowly.</li>
      <li><strong>Wrong temperature</strong> &mdash; a tropical species kept cool grows slowly; a subtropical species kept hot burns through its life faster.</li>
    </ul>

    <h2 id="measuring">Measuring and Tracking Growth</h2>
    <p>Fish are measured as <strong>total length</strong> (snout to the tip of the tail) in the snakehead hobby unless stated otherwise. The practical way to track one without netting it &mdash; netting stresses snakeheads badly and invites a jump &mdash; is to tape a strip of paper marked in inches along the outside of the glass and photograph the fish beside it when it settles on the bottom. Log the number monthly.</p>
    <p>Once you know the adult size, size the tank from the <a href="/guides/snakehead-fish-care/tank-size/">snakehead tank size guide</a>: length at least three times the adult body length. Our <a href="/tools/tank-size-calculator/">tank size calculator</a> turns dimensions into gallons.</p>

    <h2 id="maximise">Growing a Healthy Snakehead</h2>
    <ul>
      <li><strong>Feed juveniles daily</strong> on a varied whole-food diet, then taper to 2&ndash;3 times weekly at adult size.</li>
      <li><strong>Keep nitrate under 30 ppm</strong> with 30&ndash;50% weekly water changes.</li>
      <li><strong>Hold the species-correct temperature</strong>, including the seasonal cooldown for subtropical fish.</li>
      <li><strong>Upgrade the tank ahead of the fish</strong>, not after it looks cramped.</li>
      <li><strong>Reduce stress:</strong> cover, dim light, low flow and a stable routine all show up as better growth.</li>
    </ul>
"""

SIZE = {
    "slug": "size-growth",
    "title": "How Big Do Snakehead Fish Get? Size & Growth Rate by Species",
    "meta_desc": "Snakehead fish size by species, from 4 inch Channa andrao to the 4 foot giant, plus growth rates per month, stunting risks and how to track growth.",
    "h1": "How Big Do Snakehead Fish Get?",
    "hero_tag": "Size & Growth",
    "hero_meta": "\U0001F4CF 4 in to 4 ft &nbsp;|&nbsp; \U0001F4C8 Giants grow 1 in per month &nbsp;|&nbsp; ⚠️ Stunting is not size control",
    "toc_sections": [
        ("by-species", "Size by Species"),
        ("growth-rate", "Growth Rate"),
        ("stunting", "The Tank-Size Myth"),
        ("measuring", "Measuring Growth"),
        ("maximise", "Growing a Healthy Fish"),
    ],
    "body": SIZE_BODY,
    "faqs": [
        ("How big do snakehead fish get?",
         "Between 4 inches and 4 feet depending on species. Channa andrao stays at 4-5 inches, Channa bleheri reaches 6-7 inches, Channa aurantimaculata 14-16 inches, Channa marulioides 24-26 inches, and the giant snakehead Channa micropeltes can exceed 4 feet (130 cm)."),
        ("How fast do snakehead fish grow?",
         "Dwarf species such as Channa andrao add roughly 0.3-0.5 inches a month and reach adult size in 12-18 months. Large species grow far faster - Channa micropeltes commonly reaches 18-24 inches in its first year, adding over an inch a month, which is what makes the cheap red juvenile such a problem purchase."),
        ("Do snakehead fish grow to the size of their tank?",
         "No. In an undersized tank a snakehead stunts: the skeleton and fins stop growing while internal organs continue, causing spinal curvature, organ compression and a shortened life. Stunting is deformity, not size control - size the tank for the adult fish from the start."),
        ("How big does a dwarf snakehead get?",
         "Channa andrao, the smallest species in the trade, reaches 4-5 inches. Channa bleheri reaches 6-7 inches and the Channa gachua complex 6-8 inches. Anything sold as a dwarf snakehead that exceeds 12 inches was mislabelled."),
        ("Why is my snakehead not growing?",
         "Check nitrate first - readings above 40 ppm suppress growth even when ammonia and nitrite are zero. Then look at diet variety, since a bloodworm-only or feeder-only diet produces slow, thin growth, and at temperature, since a tropical species kept too cool grows slowly. A tank that is too small stunts growth permanently."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/types/", "Snakehead Types & Species"),
        ("/guides/snakehead-fish-care/tank-size/", "Snakehead Tank Size"),
        ("/guides/snakehead-fish-care/lifespan/", "Snakehead Lifespan"),
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
    ],
}

# ════════════════════════════════════════════════════════════════
# LIFESPAN
# ════════════════════════════════════════════════════════════════
LIFESPAN_BODY = """    <p>A snakehead is a long-term commitment. Even the 4-inch dwarfs routinely pass eight years, and the large species can outlast a mortgage term. Before buying one, the honest question is not whether you can keep it alive this year but whether you will still want an ambush predator in the living room in 2035.</p>

    <h2 id="how-long">How Long Do Snakehead Fish Live?</h2>
    <table class="ptbl">
      <tr><th>Group</th><th>Species</th><th>Typical captive lifespan</th></tr>
      <tr><td>Dwarf</td><td><em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em></td><td>8&ndash;12 years</td></tr>
      <tr><td>Medium</td><td><em>C. pulchra</em>, <em>C. asiatica</em>, <em>C. aurantimaculata</em></td><td>10&ndash;15 years</td></tr>
      <tr><td>Large</td><td><em>C. marulioides</em>, <em>C. striata</em>, <em>C. lucius</em></td><td>10&ndash;18 years</td></tr>
      <tr><td>Giant</td><td><em>C. micropeltes</em>, <em>C. marulius</em>, <em>C. argus</em></td><td>15&ndash;20+ years</td></tr>
    </table>
    <p>Those figures assume species-correct temperature, a varied diet and a tank the fish can actually live in. Wild lifespans are generally shorter, because predation and fishing pressure remove fish long before old age does.</p>
    <div class="callout"><strong>The realistic captive average is much lower than the potential.</strong> Most snakeheads that die young die of one of three things, and none of them is disease: a jump out of the tank, stunting in an undersized tank, or years of the wrong temperature. All three are avoidable on day one.</div>

    <h2 id="factors">What Determines Lifespan</h2>
    <h3>1. The lid</h3>
    <p>Jumping is the leading cause of premature death in captive <em>Channa</em>, and it is entirely preventable with a weighted, gap-free cover. See the <a href="/guides/snakehead-fish-care/tank-size/">lid specification</a>.</p>
    <h3>2. Tank size</h3>
    <p>A stunted fish is a short-lived fish. Spinal curvature and compressed organs from years in an undersized tank typically cut lifespan by half or more.</p>
    <h3>3. Seasonal temperature</h3>
    <p>This is the quiet one. A subtropical species such as <em>C. aurantimaculata</em> or <em>C. andrao</em> held at 80&deg;F year-round runs a permanently elevated metabolism. The fish looks fine for two or three years, then fades. Give subtropical species their <a href="/guides/snakehead-fish-care/water-parameters/">8&ndash;12 week cool season</a>.</p>
    <h3>4. Diet</h3>
    <p>Two dietary patterns shorten life measurably: a thiaminase-heavy feeder-fish diet, which causes cumulative vitamin B1 deficiency, and simple overfeeding, which produces fatty liver disease. Adults need feeding only two or three times a week &mdash; see <a href="/guides/snakehead-fish-care/feeding/">feeding schedule</a>.</p>
    <h3>5. Water quality</h3>
    <p>Because they breathe air, snakeheads endure bad water longer than most fish. The damage still accumulates: chronic nitrate above 40 ppm and repeated ammonia exposure produce gill and kidney damage that shows up years later.</p>
    <h3>6. Origin of the fish</h3>
    <p>Most snakeheads in the trade are wild-caught and arrive carrying internal parasites and transport damage. A 4&ndash;6 week quarantine with a parasite treatment before the fish enters the display makes a measurable difference to how long it lives.</p>

    <h2 id="wild-vs-captive">Wild vs Captive Lifespan</h2>
    <p>Captive snakeheads generally outlive wild ones, which is unusual for a large predatory fish and worth understanding, because it explains which risks actually matter.</p>
    <p>In the wild, <em>Channa</em> are heavily fished across their native range &mdash; <em>C. striata</em> is one of the most important food fishes in Southeast Asia &mdash; and juveniles are preyed on by birds, larger fish and other snakeheads. Field studies of <em>C. argus</em> in its introduced Potomac population have found few fish older than about eight years, not because the species cannot live longer but because something removes them first. Native-range populations show the same pattern.</p>
    <p>A captive fish faces none of that. Given the right tank it has no predators, no fishing pressure, a reliable food supply and stable water, which is why aquarium <em>Channa</em> routinely pass a decade. The corollary matters: since nothing in a home aquarium is trying to eat your snakehead, essentially every premature death is something the keeper controls &mdash; the lid, the tank size, the temperature cycle and the diet.</p>
    <div class="callout"><strong>Longevity is a setup problem, not a husbandry-skill problem.</strong> The decisions that determine whether a snakehead reaches ten years are nearly all made before the fish arrives: which species, how big the tank is, and how well the lid is built.</div>

    <h2 id="ageing">Signs of an Ageing Snakehead</h2>
    <ul>
      <li><strong>Reduced appetite and longer gaps between meals</strong> &mdash; normal in an old fish, worrying in a young one.</li>
      <li><strong>Faded pattern</strong>, particularly loss of the fin edging in <em>C. andrao</em> and <em>C. bleheri</em>.</li>
      <li><strong>Cloudier eyes</strong> without other symptoms.</li>
      <li><strong>Slower, less frequent surfacing</strong> and longer periods motionless.</li>
      <li><strong>Fin erosion at the margins</strong> that does not respond to water quality improvements.</li>
    </ul>
    <p>None of these needs treatment on its own. Check water parameters to rule out a fixable cause, keep the temperature stable, feed smaller meals, and leave the fish alone.</p>

    <h2 id="maximise">Getting the Full Lifespan</h2>
    <ol>
      <li><strong>Buy the right species for the space you actually have.</strong> The <a href="/guides/snakehead-fish-care/types/">species guide</a> matches tank size to fish.</li>
      <li><strong>Build the lid before the fish arrives.</strong></li>
      <li><strong>Quarantine 4&ndash;6 weeks</strong> and treat for internal parasites.</li>
      <li><strong>Match the seasonal temperature cycle</strong> for subtropical and temperate species.</li>
      <li><strong>Feed varied whole foods and pellets</strong>, never feeder goldfish, and keep adults lean.</li>
      <li><strong>Change 30&ndash;50% of the water weekly</strong> and hold nitrate under 30 ppm.</li>
      <li><strong>Keep it alone or with a proven pair.</strong> Chronic aggression from a bad tank-mate choice is a slow killer &mdash; see <a href="/guides/snakehead-fish-care/tank-mates/">tank mates</a>.</li>
    </ol>
"""

LIFESPAN = {
    "slug": "lifespan",
    "title": "Snakehead Fish Lifespan: How Long Do Channa Live in Captivity?",
    "meta_desc": "Snakehead fish lifespan: 8-12 years for dwarf Channa, 15-20+ for giants. What cuts it short - jumping, stunting, wrong temperature - and how to prevent it.",
    "h1": "Snakehead Fish Lifespan",
    "hero_tag": "Lifespan",
    "hero_meta": "⏳ 8&ndash;12 yrs dwarf &nbsp;|&nbsp; \U0001F4C5 15&ndash;20+ yrs giants &nbsp;|&nbsp; \U0001F512 Jumping is the top killer",
    "toc_sections": [
        ("how-long", "How Long They Live"),
        ("factors", "What Determines Lifespan"),
        ("wild-vs-captive", "Wild vs Captive"),
        ("ageing", "Signs of Ageing"),
        ("maximise", "Getting the Full Lifespan"),
    ],
    "body": LIFESPAN_BODY,
    "faqs": [
        ("How long do snakehead fish live?",
         "Dwarf species such as Channa andrao and Channa bleheri typically live 8-12 years in captivity. Medium species reach 10-15 years, and large species including Channa micropeltes and Channa argus can pass 20 years. Those figures assume species-correct temperature, a varied diet and an adequately sized tank."),
        ("How long do dwarf snakeheads live?",
         "Channa andrao, Channa bleheri and the Channa gachua complex typically live 8-12 years in a well-kept aquarium. That makes even the smallest snakehead a decade-long commitment, comparable to a large cichlid."),
        ("What is the most common cause of death in captive snakeheads?",
         "Jumping out of the tank. Snakeheads are powerful, deliberate jumpers that push at loose lids and escape through filter cutouts, and more captive fish die on the floor than from any disease. Stunting in an undersized tank and years at the wrong temperature are the next two causes."),
        ("Does temperature affect snakehead lifespan?",
         "Significantly, for subtropical and temperate species. Holding Channa andrao or Channa aurantimaculata at 80F year-round keeps their metabolism permanently elevated; the fish looks healthy for two or three years then declines. An 8-12 week cool season at 59-68F each year is part of correct care for these species."),
        ("How can I tell if my snakehead is old?",
         "Look for a gradually reduced appetite, faded pattern and lost fin edging, slightly cloudy eyes with no other symptoms, longer motionless periods and less frequent surfacing, and fin margin erosion that does not respond to better water quality. Rule out water problems first, then simply keep conditions stable and feed smaller meals."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/size-growth/", "Size & Growth Rate"),
        ("/guides/snakehead-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/snakehead-fish-care/diseases/", "Diseases & Symptoms"),
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
    ],
}

# ════════════════════════════════════════════════════════════════
# MALE VS FEMALE
# ════════════════════════════════════════════════════════════════
MVF_BODY = """    <p>Sexing <em>Channa</em> is genuinely difficult, and anyone who tells you there is one reliable visual rule across the genus is guessing. Differences are subtle, species-specific, and in several species only become readable once the fish are mature and in breeding condition. The practical approach used by breeders is not to sex individuals at all &mdash; it is to raise a group and let a pair form.</p>

    <h2 id="quick-table">Male vs Female Snakehead: Quick Comparison</h2>
    <table class="ptbl">
      <tr><th>Trait</th><th>Male</th><th>Female</th></tr>
      <tr><td>Head shape</td><td>Broader, deeper, more angular jaw</td><td>Narrower, more tapered snout</td></tr>
      <tr><td>Body</td><td>Slimmer, more muscular through the shoulder</td><td>Fuller and rounder, especially ahead of the vent</td></tr>
      <tr><td>Colour</td><td>More intense, especially fin margins and iridescence</td><td>Generally subdued; may pale when gravid</td></tr>
      <tr><td>Dorsal / anal fins</td><td>Often longer and more pointed</td><td>Shorter, more rounded</td></tr>
      <tr><td>Size</td><td>Usually the larger of a pair in most species</td><td>Usually slightly smaller</td></tr>
      <tr><td>Genital papilla</td><td>Small and pointed</td><td>Broader, rounder, more prominent when ripe</td></tr>
      <tr><td>Brooding (mouthbrooders)</td><td>Visibly distended throat and lower jaw</td><td>Never carries eggs</td></tr>
    </table>
    <div class="callout callout-warn"><strong>Every one of those cues has exceptions.</strong> In some populations females are the larger fish; in others colour is essentially identical between the sexes. Treat the table as a set of probabilities to weigh together, not as a checklist where any single item decides it.</div>

    <h2 id="reliable">The Two Genuinely Reliable Methods</h2>
    <h3>1. Watch a brooding male</h3>
    <p>In the mouthbrooding dwarf species &mdash; <em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em>, <em>C. pulchra</em> and relatives &mdash; the male incubates the eggs. A fish sitting quietly with an obviously swollen throat and lower jaw, refusing food for several days, is definitively male. This is the only zero-doubt method available to most keepers, and it is retrospective.</p>
    <h3>2. Watch behaviour during pairing</h3>
    <p>When a pair forms, the male typically displays more, holds the chosen territory and initiates the wrapping embrace at spawning. The female approaches, retreats and is the one displaying gravid fullness beforehand.</p>

    <h2 id="by-species">Species-Specific Cues</h2>
    <h3>Channa andrao and Channa bleheri</h3>
    <p>Males develop stronger red-and-white or orange fin margins and a deeper blue base as they mature; females stay comparatively muted and become noticeably rounder when ripe. Head width is the most useful structural cue &mdash; view the fish from directly above, where a mature male's head is visibly broader across the cheeks.</p>
    <h3>Channa gachua and Channa limbata</h3>
    <p>Highly variable between regional populations. Males in most populations carry brighter blue or orange fin edging and a broader head. Because &ldquo;gachua&rdquo; stock may be any of several species, compare only fish from the same source.</p>
    <h3>Channa pulchra and Channa aurantimaculata</h3>
    <p>Males are usually larger with more extensive and more saturated markings; females are stockier through the belly. In <em>C. aurantimaculata</em> the orange barring on a mature male typically extends further onto the head.</p>
    <h3>Large species (striata, marulioides, micropeltes, argus)</h3>
    <p>Essentially not sexable by eye outside of spawning condition. Ripe females show a swollen abdomen and a distended, reddened vent. Commercial hatcheries rely on that plus hormone assay, not on appearance.</p>

    <h2 id="method">The Practical Method: Grow Out a Group</h2>
    <p>This is how nearly all successful hobby breeding starts:</p>
    <ol>
      <li><strong>Buy 5&ndash;6 juveniles</strong> from the same batch, so genetics and age match.</li>
      <li><strong>Grow them out together</strong> in a tank larger than a single adult would need, with heavy cover and multiple sight-breaks. Overcrowding cover is the point &mdash; broken lines of sight reduce fighting.</li>
      <li><strong>Watch for a pair</strong>. Two fish will begin occupying the same territory, resting side by side and tolerating contact. That is a bonded pair regardless of what the sexing table said.</li>
      <li><strong>Remove the others</strong> once a pair bonds, or move the pair to their own tank. Snakeheads with a pair in the tank become intolerant of everyone else fast.</li>
      <li><strong>Have a backup plan.</strong> Grow-out groups produce fish you will need to rehome, and rehoming a snakehead is legally restricted in many places. Do not start a group you cannot place.</li>
    </ol>
    <div class="callout"><strong>Venting is unreliable in <em>Channa</em>.</strong> The papilla difference is real but small, only visible in mature fish, and requires netting and handling &mdash; which stresses snakeheads badly and is the classic prelude to a jump. It is not worth it for a probabilistic answer.</div>

    <h2 id="next">Once You Have a Pair</h2>
    <p>A bonded pair is the requirement for breeding, not just a nice outcome. Conditioning, the cool-season trigger, spawning behaviour and raising fry are covered on the <a href="/guides/snakehead-fish-care/breeding/">snakehead breeding guide</a>, and pair aggression toward everything else in the tank is covered under <a href="/guides/snakehead-fish-care/tank-mates/">tank mates</a>.</p>
"""

MVF = {
    "slug": "male-vs-female",
    "title": "Male vs Female Snakehead Fish: How to Sex Channa Reliably",
    "meta_desc": "How to tell male and female snakehead fish apart: head width, body shape, fin colour and the brooding male - plus why growing out a group beats venting.",
    "h1": "Male vs Female Snakehead Fish",
    "hero_tag": "Male vs Female",
    "hero_meta": "♂ Broader head, brighter fins &nbsp;|&nbsp; ♀ Fuller body &nbsp;|&nbsp; \U0001F95A Brooding male is the only certainty",
    "toc_sections": [
        ("quick-table", "Quick Comparison"),
        ("reliable", "Reliable Methods"),
        ("by-species", "Species-Specific Cues"),
        ("method", "Grow Out a Group"),
        ("next", "Once You Have a Pair"),
    ],
    "body": MVF_BODY,
    "faqs": [
        ("How do you tell a male from a female snakehead?",
         "Mature males generally have a broader, deeper head viewed from above, a slimmer more muscular body, and more intense colour on the fin margins. Females are fuller-bodied ahead of the vent, especially when gravid, with a narrower snout. Every cue has exceptions, so weigh several together rather than relying on one."),
        ("What is the most reliable way to sex a Channa?",
         "Watching a male brood. In the mouthbrooding dwarf species the male incubates the eggs, so a fish with an obviously swollen throat and lower jaw refusing food for several days is definitively male. Short of that, letting a group of 5-6 juveniles grow out and form a pair is far more reliable than trying to sex individuals."),
        ("Can you vent a snakehead fish to sex it?",
         "It is possible but not worth doing. The genital papilla is small and pointed in males and broader and rounder in ripe females, but the difference is only visible in mature fish and requires netting and handling. Snakeheads are stressed badly by handling and a netted fish is very likely to jump afterwards."),
        ("Are male snakeheads bigger than females?",
         "In most species the male is the slightly larger fish of a pair, but this is not consistent across the genus and some populations reverse it. Size alone should never be used to sex a Channa."),
        ("How do I get a breeding pair of snakeheads?",
         "Buy 5-6 juveniles from the same batch and grow them out together in a large tank with heavy cover and broken sight lines. Watch for two fish that occupy the same territory, rest side by side and tolerate contact - that is a bonded pair. Remove the remaining fish once the pair forms, and have a rehoming plan for them before you start."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/breeding/", "Breeding Snakeheads"),
        ("/guides/snakehead-fish-care/types/", "Snakehead Types & Species"),
        ("/guides/snakehead-fish-care/tank-mates/", "Tank Mates"),
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
    ],
}

# ════════════════════════════════════════════════════════════════
# BREEDING
# ════════════════════════════════════════════════════════════════
BREEDING_BODY = """    <p>Snakeheads are among the most attentive parents in freshwater fish. Both reproductive strategies in the genus involve serious, sustained parental care &mdash; which is exactly why a spawning pair turns a peaceful tank into a war zone. Breeding <em>Channa</em> is achievable at home, and the hard parts are pair formation and what to do with the fry, not the spawning itself.</p>

    <div class="callout callout-warn"><strong>Before you breed:</strong> in the US, interstate transport of snakeheads is federally prohibited and most states ban possession, so a successful spawn can leave you with dozens of fish you cannot legally rehome. Confirm you have somewhere for the fry to go before you condition the pair.</div>

    <h2 id="strategies">Two Breeding Strategies</h2>
    <table class="ptbl">
      <tr><th></th><th>Paternal mouthbrooders</th><th>Nest guarders</th></tr>
      <tr><td>Species</td><td><em>C. andrao</em>, <em>C. bleheri</em>, <em>C. gachua</em>, <em>C. limbata</em>, <em>C. pulchra</em>, <em>C. stewartii</em></td><td><em>C. striata</em>, <em>C. argus</em>, <em>C. micropeltes</em>, <em>C. marulius</em>, <em>C. marulioides</em></td></tr>
      <tr><td>Egg count</td><td>Roughly 30&ndash;150</td><td>Often thousands</td></tr>
      <tr><td>Eggs</td><td>Non-adhesive, buoyant, amber</td><td>Buoyant, in a floating raft</td></tr>
      <tr><td>Care</td><td>Male incubates in his mouth</td><td>Both parents guard the raft and shoal of fry</td></tr>
      <tr><td>Incubation</td><td>4&ndash;7 days in the mouth</td><td>2&ndash;3 days to hatch in the nest</td></tr>
      <tr><td>Post-hatch</td><td>Male guards free-swimming fry for weeks</td><td>Parents escort the fry shoal, sometimes for months</td></tr>
    </table>
    <p>Almost all hobby breeding is of the mouthbrooding dwarfs, because the nest guarders are 2&ndash;4 foot fish producing thousands of fry.</p>

    <h2 id="pair">Getting a Pair</h2>
    <p>You cannot reliably pick a male and a female off a shop shelf &mdash; see <a href="/guides/snakehead-fish-care/male-vs-female/">male vs female snakehead</a>. The standard route is to buy <strong>5&ndash;6 juveniles from one batch</strong>, grow them out together in an oversized, heavily decorated tank, and wait for two fish to bond. A bonded pair occupies one territory together, rests in contact, and stops fighting.</p>
    <p>Once a pair forms, remove the other fish. A pair will pursue and kill remaining group members, and pair aggression escalates further once spawning begins.</p>

    <h2 id="conditioning">Conditioning and the Spawning Trigger</h2>
    <p>The trigger reproduces a monsoon: a cool dry season, then warming water and heavy fresh rain.</p>
    <ol>
      <li><strong>Cool period (8&ndash;12 weeks).</strong> Drop subtropical species to 59&ndash;68&deg;F (15&ndash;20&deg;C), feeding lightly or not at all. See the <a href="/guides/snakehead-fish-care/water-parameters/">cooldown schedule</a>.</li>
      <li><strong>Warm up over 2&ndash;3 weeks</strong> back to 75&ndash;79&deg;F (24&ndash;26&deg;C).</li>
      <li><strong>Feed heavily.</strong> Earthworms, shell-on shrimp, krill and insects, daily, for two to three weeks. Females fill out visibly.</li>
      <li><strong>Simulate rain.</strong> Larger water changes (40&ndash;50%) with slightly cooler, softer water, two or three times a week. A drop in TDS is the strongest single cue.</li>
      <li><strong>Lower the water level</strong> a few inches and raise it back over several days, and add dense floating plant cover. Mouthbrooders spawn at the surface and want cover overhead.</li>
    </ol>

    <h2 id="spawning">Spawning Behaviour</h2>
    <p>Courtship in mouthbrooders runs over several days: the pair sits together, the male displays with flared fins, and the two circle at the surface. The spawn itself is an <strong>embrace</strong> &mdash; the male wraps his body around the female and the pair rolls, releasing a small batch of buoyant amber eggs. This repeats over an hour or more until the clutch is complete.</p>
    <p>The male then collects the floating eggs into his mouth. From that point he does not feed. Over <strong>4&ndash;7 days</strong> the eggs hatch inside the mouth, and he releases free-swimming fry &mdash; then continues guarding them, herding strays back and taking them into his mouth again when threatened.</p>
    <p>Nest-guarding species instead clear a patch among plants, release a floating raft of eggs, and both parents patrol beneath it. Eggs hatch in 2&ndash;3 days and the parents escort the fry shoal, often attacking anything that approaches including the keeper's hand.</p>
    <div class="callout"><strong>Do not intervene.</strong> The commonest way to lose a first spawn is disturbing the brooding male. Leave the lights dim, skip the water change, feed the female at the far end of the tank, and stay away from the glass. Snakehead parents are competent; keepers are the risk factor.</div>

    <h2 id="fry">Raising the Fry</h2>
    <table class="ptbl">
      <tr><th>Age</th><th>Food</th><th>Notes</th></tr>
      <tr><td>Days 1&ndash;3 free-swimming</td><td>Baby brine shrimp, microworm, infusoria</td><td>Feed 3&ndash;4&times; daily, small amounts</td></tr>
      <tr><td>Weeks 2&ndash;4</td><td>BBS, grindal worm, chopped bloodworm</td><td>Growth becomes visibly uneven &mdash; start grading</td></tr>
      <tr><td>Weeks 4&ndash;10</td><td>Chopped earthworm, small frozen foods, crushed pellet</td><td>Cannibalism risk peaks here</td></tr>
      <tr><td>3 months+</td><td>Standard adult diet, scaled down</td><td>Separate by size into grow-out tanks</td></tr>
    </table>
    <p>Three things decide whether a brood survives:</p>
    <ul>
      <li><strong>Grade by size relentlessly.</strong> Snakehead fry eat each other, and one fast grower will work through its siblings within days.</li>
      <li><strong>Keep the water pristine.</strong> Fry are heavily fed and produce a lot of waste. Small daily water changes beat one big weekly one.</li>
      <li><strong>Cover the grow-out tanks.</strong> Fry jump too, from about an inch long.</li>
    </ul>
    <p>Leave the guarding male with the fry as long as he is calm &mdash; he is a better fry-herder than any net. Remove him if he starts eating them, which some males do once they resume feeding.</p>

    <h2 id="problems">Common Breeding Problems</h2>
    <ul>
      <li><strong>Pair fights instead of spawning.</strong> Usually not enough cover, or the fish are not actually a bonded pair. Add sight-breaks; separate if damage occurs.</li>
      <li><strong>Male swallows the eggs.</strong> Common on a first spawn, especially in young or disturbed males. Do not intervene &mdash; most get it right on the second or third attempt.</li>
      <li><strong>Eggs fungus in the nest.</strong> Nest-guarding pairs normally remove bad eggs themselves. Persistent fungus points to unfertilised eggs, which usually means an immature male.</li>
      <li><strong>No spawning at all.</strong> Almost always a missing cool season. Subtropical <em>Channa</em> will not spawn without it, however well fed.</li>
      <li><strong>Female is attacked after spawning.</strong> Provide an exit route and a hiding place she can defend, or move her once the male has the eggs.</li>
    </ul>
"""

BREEDING = {
    "slug": "breeding",
    "title": "Breeding Snakehead Fish: Channa Mating, Eggs & Raising Fry",
    "meta_desc": "How to breed snakehead fish: forming a pair, the cool-season trigger, mouthbrooding vs nest guarding, egg incubation and raising Channa fry.",
    "h1": "Breeding Snakehead Fish (Channa)",
    "hero_tag": "Breeding & Fry",
    "hero_meta": "\U0001F95A Mouthbrooders & nest guarders &nbsp;|&nbsp; ❄️ Cool season required &nbsp;|&nbsp; \U0001F423 4&ndash;7 day incubation",
    "toc_sections": [
        ("strategies", "Two Breeding Strategies"),
        ("pair", "Getting a Pair"),
        ("conditioning", "Conditioning & Triggers"),
        ("spawning", "Spawning Behaviour"),
        ("fry", "Raising the Fry"),
        ("problems", "Common Problems"),
    ],
    "body": BREEDING_BODY,
    "faqs": [
        ("How do snakehead fish breed?",
         "Two ways. The dwarf gachua-group species including Channa andrao and Channa bleheri are paternal mouthbrooders: the pair spawns in an embrace at the surface, the male collects the buoyant eggs and incubates them in his mouth for 4-7 days, then guards the free-swimming fry. Large species such as Channa striata and Channa argus are nest guarders that produce a floating raft of thousands of eggs defended by both parents."),
        ("How many eggs do snakehead fish lay?",
         "Mouthbrooding dwarf species lay roughly 30-150 eggs per spawn, limited by what the male can hold in his mouth. Large nest-guarding species such as Channa striata and Channa micropeltes can produce several thousand eggs in a single floating raft."),
        ("What triggers snakeheads to spawn?",
         "A simulated monsoon. Give subtropical species an 8-12 week cool period at 59-68F with little food, warm the tank back to 75-79F over two to three weeks, feed heavily on earthworms and shrimp, then do 40-50% water changes with slightly cooler softer water. The drop in dissolved solids is the strongest single cue, and without the cool season most subtropical Channa will not spawn at all."),
        ("How long do snakehead eggs take to hatch?",
         "In mouthbrooding species the eggs hatch inside the male's mouth after 4-7 days, and he releases free-swimming fry that he continues to guard for weeks. In nest-guarding species the floating eggs hatch in 2-3 days and both parents escort the fry shoal, sometimes for months."),
        ("What do baby snakehead fish eat?",
         "Free-swimming fry start on baby brine shrimp, microworm and infusoria fed 3-4 times daily. From two weeks add grindal worm and chopped bloodworm, and from about a month chopped earthworm and crushed pellet. Grade the fry by size constantly - snakehead fry are cannibalistic and one fast grower will eat its siblings."),
    ],
    "related": [
        ("/guides/snakehead-fish-care/male-vs-female/", "Male vs Female"),
        ("/guides/snakehead-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/snakehead-fish-care/feeding/", "Food & Feeding"),
        ("/guides/snakehead-fish-care/", "Snakehead Care Guide"),
    ],
}

# ════════════════════════════════════════════════════════════════
# DISEASES — Diseases, Parasites & Symptoms
# ════════════════════════════════════════════════════════════════
DISEASES_BODY = """    <p>Snakeheads are physically tough fish, and that is the problem: because they breathe air and tolerate poor water, they hide trouble far longer than a tetra would. Most of what looks alarming in a <em>Channa</em> is normal predator behaviour, and most of what is genuinely wrong traces to three sources &mdash; wild-caught parasite loads, injuries from jumping or fighting, and diet.</p>

    <div class="callout"><strong>Test the water before you medicate.</strong> Ammonia, nitrite, nitrate, temperature. Roughly half of all snakehead symptom threads end with a water quality answer, and medicating a fish in bad water makes things worse. Run a reading through the <a href="/tools/water-parameter-checker/">water parameter checker</a> first.</div>

    <h2 id="symptom-index">Symptom Index</h2>
    <table class="ptbl">
      <tr><th>Symptom</th><th>Most likely cause</th><th>Urgency</th></tr>
      <tr><td>Not moving / lying on the bottom</td><td>Normal ambush behaviour</td><td>None &mdash; see <a href="#normal">normal behaviour</a></td></tr>
      <tr><td>Rising to the surface to gulp air</td><td>Normal &mdash; obligate air-breathing</td><td>None</td></tr>
      <tr><td>Hiding constantly</td><td>New fish settling, or too little cover / too much light</td><td>Low</td></tr>
      <tr><td>Not eating</td><td>Settling stress, wrong temperature, seasonal fast</td><td>Low unless losing weight</td></tr>
      <tr><td>Losing colour / turning black</td><td>Stress signalling, nitrate creep, or healing ammonia burn</td><td>Medium &mdash; test water</td></tr>
      <tr><td>White spots on body and fins</td><td>Ich (<em>Ichthyophthirius</em>)</td><td>High</td></tr>
      <tr><td>Bloated / swollen belly</td><td>Overfeeding; dropsy if scales are pineconed</td><td>Medium to high</td></tr>
      <tr><td>Fin rot, ragged fin edges</td><td>Water quality or bite injury</td><td>Medium</td></tr>
      <tr><td>Cloudy eye</td><td>Impact injury from jumping, or water quality</td><td>Medium</td></tr>
      <tr><td>Swimming sideways / erratic</td><td>Swim bladder, thiaminase deficiency, ammonia damage</td><td>High</td></tr>
      <tr><td>Gasping and staying at the surface</td><td>Gill damage or gill flukes &mdash; not normal air-breathing</td><td>High</td></tr>
      <tr><td>Thin despite eating, stringy white waste</td><td>Internal parasites</td><td>Medium</td></tr>
      <tr><td>Red ulcers, open sores</td><td>Bacterial infection after injury</td><td>High</td></tr>
      <tr><td>Jumping / hitting the lid</td><td>Escape behaviour, stress, poor cover</td><td>High &mdash; fix the lid today</td></tr>
    </table>

    <h2 id="normal">Normal Behaviour Mistaken for Illness</h2>
    <h3>Snakehead not moving or lying on the bottom</h3>
    <p>This is what an ambush predator does. A healthy <em>Channa</em> will sit motionless on the substrate or wedged under wood for hours, moving only to surface for air. Judge the fish on the surrounding signs instead: clear eyes, upright posture, fins held normally rather than clamped, calm gill movement, and a response when you approach. If those are fine, the fish is fine.</p>
    <h3>Snakehead gasping for air at the surface</h3>
    <p>Snakeheads <em>must</em> surface to breathe atmospheric air &mdash; typically every few minutes. Normal air-breathing is a deliberate rise, a gulp, and an immediate return to station on the bottom. Distress looks completely different: the fish <strong>stays</strong> at the surface, gill covers working rapidly, often tilted head-up, and repeats without settling. Normal breathing is not an emergency; staying at the surface is.</p>
    <h3>Snakehead hiding</h3>
    <p>Two to four weeks of hiding after import is standard. Dim the lights, add floating plants and caves, stop approaching the glass, and offer small food items every second day. A snakehead that has never come out after two months usually has too little cover, not too much &mdash; counter-intuitively, fish with more hiding places spend more time in the open.</p>
    <h3>Snakehead losing colour or turning black</h3>
    <p>Colour in <em>Channa</em> is partly a mood signal and can shift within hours. Darkening during territorial disputes, after a move, or under bright light is normal and reverses. Persistent dullness over weeks is different, and the first thing to test is nitrate &mdash; chronic nitrate above 40 ppm produces exactly that. Fixed black patches that appeared after a water quality problem are usually healing ammonia burn and fade over weeks to months.</p>

    <h2 id="parasites">Snakehead Fish Parasites</h2>
    <p>Most snakeheads in the trade are wild-caught and arrive carrying something. This is the single strongest argument for a <strong>4&ndash;6 week quarantine</strong> in a bare-bottom tank before the fish goes anywhere near a display.</p>
    <table class="ptbl">
      <tr><th>Parasite</th><th>Signs</th><th>Treatment</th></tr>
      <tr><td>Internal nematodes (roundworm)</td><td>Thin fish with a good appetite, sunken belly, sometimes visible worms at the vent</td><td>Levamisole or fenbendazole, repeated after 2&ndash;3 weeks</td></tr>
      <tr><td>Cestodes (tapeworm)</td><td>Weight loss, pale stringy waste, food spat out</td><td>Praziquantel, repeated</td></tr>
      <tr><td>Gill and skin flukes</td><td>Flicking, rubbing on d&eacute;cor, rapid gill movement, staying at the surface</td><td>Praziquantel</td></tr>
      <tr><td>Ich (white spot)</td><td>Salt-grain white dots on body and fins, flicking</td><td>Raise temperature gradually, aquarium salt, or a standard ich treatment</td></tr>
      <tr><td>Anchor worm / fish lice</td><td>Visible attached parasites, localised redness</td><td>Manual removal plus an appropriate parasiticide</td></tr>
    </table>
    <div class="callout"><strong>Air-breathing changes the maths on treatment.</strong> Snakeheads tolerate the low dissolved oxygen of heat treatment better than most fish, so raising the temperature for ich is comparatively safe. They also tolerate aquarium salt well. Be conservative with copper-based medications, and always dose to the actual water volume after subtracting substrate and d&eacute;cor.</div>

    <h2 id="bacterial">Bacterial and Fungal Problems</h2>
    <h3>Fin rot</h3>
    <p>Ragged, receding fin margins, sometimes with a white or reddened edge. In snakeheads it is almost always secondary &mdash; a bite from a tank mate or another snakehead, or a jumping injury, followed by poor water. Treat by fixing the water first (daily 30% changes, nitrate under 30 ppm) and only reaching for an antibacterial if the erosion continues after a week.</p>
    <h3>Ulcers and red sores</h3>
    <p><em>Aeromonas</em> and similar bacteria entering through a wound. Common after a fish jumps and lands hard, or after a fight. Isolate, keep the water immaculate, and treat with a broad-spectrum antibacterial. Deep ulcers on a large fish may need a vet-prescribed antibiotic.</p>
    <h3>Cloudy eye</h3>
    <p>One cloudy eye usually means physical injury &mdash; a jump into the lid, or a strike at the glass. Both eyes cloudy usually means water quality. Clean water resolves most cases in one to two weeks.</p>
    <h3>Dropsy</h3>
    <p>A swollen belly <strong>with scales standing out like a pine cone</strong> is organ failure, usually kidney, and the prognosis is poor. A swollen belly with flat scales is almost always overfeeding or constipation &mdash; fast the fish for three to five days and feed a shelled, gut-loaded food such as earthworm afterwards.</p>

    <h2 id="diet-related">Diet-Related Problems</h2>
    <ul>
      <li><strong>Thiamine (B1) deficiency.</strong> Caused by a long-term diet of goldfish or rosy red minnows, which contain thiaminase. Signs are progressive and neurological: erratic swimming, loss of balance, swimming sideways, eventual seizures. Prevention is the only reliable treatment &mdash; see <a href="/guides/snakehead-fish-care/feeding/">what to feed instead</a>.</li>
      <li><strong>Fatty liver disease.</strong> From overfeeding, and from mammal or bird meat such as beef heart. Signs are a persistently swollen body, lethargy and reduced appetite. Reversible early by cutting to 2&ndash;3 feeds a week of lean whole foods.</li>
      <li><strong>Buoyancy problems.</strong> Usually overfeeding or gulping air with floating food. Feed sinking items and fast for a few days.</li>
      <li><strong>Constipation.</strong> A diet of soft foods with no shell or fibre. Shell-on shrimp and earthworms fix it.</li>
    </ul>

    <h2 id="injury">Injuries: Jumping and Fighting</h2>
    <p>These are the injuries that actually kill captive snakeheads.</p>
    <h3>Jumping</h3>
    <p>A snakehead that hits the lid hard can suffer a bruised or cloudy eye, a scraped snout, jaw damage or internal injury; one that gets out will die within hours to a day. Every jump is a warning. Fix the cause the same day: a weighted, gap-free lid, all filter cutouts sealed, plus the underlying stressor &mdash; usually too little cover, too much light, strong flow or an aggressive tank mate. Full lid specification is on the <a href="/guides/snakehead-fish-care/tank-size/">tank size and setup page</a>.</p>
    <h3>Fighting</h3>
    <p>Snakehead-on-snakehead damage is severe and fast &mdash; torn fins, jaw injuries, lost eyes. It happens when a pair bonds and turns on the rest of the group, when two unpaired adults share a tank, or during spawning. There is no medication for it. Separate the fish, treat the wounds as bacterial risk, and re-read <a href="/guides/snakehead-fish-care/tank-mates/">tank mates</a>.</p>

    <h2 id="quarantine">Quarantine and Treatment Protocol</h2>
    <ol>
      <li><strong>Bare-bottom quarantine tank</strong>, 20 gallons or more, with its own sealed lid and a cycled sponge filter.</li>
      <li><strong>Observe for a week</strong> before dosing anything. Let the fish settle; note breathing rate, waste appearance and whether it eats.</li>
      <li><strong>Treat for internal parasites</strong> as a matter of course for a wild-caught import: praziquantel, then levamisole or fenbendazole, each repeated after 2&ndash;3 weeks to catch the next life stage.</li>
      <li><strong>Treat externals only if seen</strong> &mdash; do not stack medications prophylactically.</li>
      <li><strong>Hold 4&ndash;6 weeks total</strong> with clean water and good food before moving the fish to the display.</li>
    </ol>
    <p>Remove carbon before dosing, dose to the real water volume, and keep the lid closed and weighted throughout &mdash; a medicated fish in an unfamiliar bare tank is the most likely of all to jump.</p>
"""

DISEASES = {
    "slug": "diseases",
    "title": "Snakehead Fish Diseases & Symptoms: Not Eating, Black, Bloated",
    "meta_desc": "Snakehead fish symptom guide: not eating, lying on the bottom, turning black, white spots, bloating, fin rot, cloudy eye, gasping and Channa parasites.",
    "h1": "Snakehead Fish Diseases and Symptoms",
    "hero_tag": "Diseases & Symptoms",
    "hero_meta": "\U0001F9EA Test water first &nbsp;|&nbsp; \U0001FAB1 Most stillness is normal &nbsp;|&nbsp; \U0001F41B Quarantine wild-caught 4&ndash;6 wks",
    "toc_sections": [
        ("symptom-index", "Symptom Index"),
        ("normal", "Normal vs Sick Behaviour"),
        ("parasites", "Parasites"),
        ("bacterial", "Bacterial & Fungal"),
        ("diet-related", "Diet-Related Problems"),
        ("injury", "Jumping & Fighting Injuries"),
        ("quarantine", "Quarantine Protocol"),
    ],
    "body": DISEASES_BODY,
    "faqs": [
        ("Why is my snakehead fish not moving?",
         "Almost always because it is behaving normally. Snakeheads are ambush predators that sit motionless on the bottom or under decor for hours, moving only to surface for air. Judge health by the surrounding signs instead - clear eyes, upright posture, unclamped fins, calm gill movement and a response when you approach. If those look right, the fish is fine."),
        ("Is my snakehead gasping for air or breathing normally?",
         "Snakeheads are obligate air-breathers and must surface every few minutes, so a deliberate rise, a gulp and an immediate return to the bottom is normal. Distress looks different: the fish stays at the surface, often tilted head-up, with rapid gill movement, and repeats without settling. That pattern points to gill damage or gill flukes and needs immediate water testing."),
        ("Why is my snakehead fish turning black?",
         "Colour in Channa is partly a mood signal, so darkening during territorial disputes, after a move or under bright light is normal and reverses within hours. Fixed black patches that appeared after a water quality problem are usually healing ammonia burn and fade over weeks to months. Persistent dullness over weeks usually means nitrate above 40 ppm."),
        ("Why does my snakehead fish have white spots?",
         "White salt-grain dots on the body and fins, usually with flicking against decor, indicate ich (Ichthyophthirius). Because snakeheads breathe air they tolerate the low oxygen of heat treatment better than most fish, so raising the temperature gradually alongside aquarium salt or a standard ich medication works well. Remove carbon before dosing."),
        ("Why is my snakehead fish bloated?",
         "Check the scales. A swollen belly with flat scales is nearly always overfeeding or constipation - fast the fish three to five days, then feed shell-on shrimp or earthworm. A swollen belly with scales standing out like a pine cone is dropsy, indicating organ failure, and the prognosis is poor."),
        ("Why does my snakehead fish keep jumping?",
         "Jumping is normal escape behaviour and the leading cause of death in captive snakeheads. Fix the lid the same day - a weighted, gap-free solid cover with all filter cutouts sealed - and then the underlying stressor, which is usually too little cover, too much light, strong flow or an aggressive tank mate."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/snakehead-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/snakehead-fish-care/feeding/", "Food & Feeding"),
        ("/fish-health/", "Fish Health Hub"),
    ],
}

# ════════════════════════════════════════════════════════════════
# TANK MATES
# ════════════════════════════════════════════════════════════════
MATES_BODY = """    <p>The honest answer to &ldquo;what fish can live with a snakehead?&rdquo; is <strong>usually nothing</strong>. Snakeheads are ambush piscivores that hold territory and become dramatically more aggressive when spawning, and the most dangerous tank mate for a snakehead is another snakehead. Where community setups work at all, they work in large, heavily structured tanks with fish chosen against three specific rules.</p>

    <h2 id="rules">The Three Rules</h2>
    <ol>
      <li><strong>Nothing that fits in the mouth.</strong> A snakehead's gape is larger than it looks, and a fish that has coexisted for months will be eaten the night it finally fits.</li>
      <li><strong>Nothing slow or long-finned.</strong> Trailing fins read as prey and get bitten off, even by species that will not eat the fish itself.</li>
      <li><strong>Nothing that competes for the floor.</strong> Snakeheads defend the substrate. Bottom-dwellers of similar size are the fights that end in lost eyes.</li>
    </ol>
    <p>Add a fourth for the keeper: <strong>anything you add must be expendable</strong>. If losing the fish would upset you, do not put it in a snakehead tank.</p>

    <h2 id="compatibility">Snakehead Tank Mate Compatibility</h2>
    <table class="ptbl">
      <tr><th>Tank mate</th><th>Verdict</th><th>Why</th></tr>
      <tr><td>Another snakehead (same species, bonded pair)</td><td>&#9989; Best option</td><td>The only stable multi-snakehead setup</td></tr>
      <tr><td>Another snakehead (different species)</td><td>&#10060; No</td><td>Reliably ends in a death; different needs too</td></tr>
      <tr><td>Large barbs (rosy, tiger, tinfoil)</td><td>&#9989; With dwarf species</td><td>Fast, mid-water dithers; accept some losses</td></tr>
      <tr><td>Large danios and rasboras</td><td>&#9989; With dwarf species</td><td>Dither fish; must be too large to swallow</td></tr>
      <tr><td>Hillstream loaches, <em>Garra</em></td><td>&#9989; With dwarf species</td><td>Fast, flat, stay out of the way</td></tr>
      <tr><td>Bichir (<em>Polypterus</em>)</td><td>&#9888;&#65039; Sometimes</td><td>Best big-fish match &mdash; similar water, both air-breathers; size them equally</td></tr>
      <tr><td>Large plecos, <em>Synodontis</em></td><td>&#9888;&#65039; Sometimes</td><td>Armoured and nocturnal; plecos may rasp at a resting snakehead</td></tr>
      <tr><td>Arowana</td><td>&#9888;&#65039; Risky</td><td>Surface fish vs a fish that must surface to breathe &mdash; conflict at the top</td></tr>
      <tr><td>Oscar and other large cichlids</td><td>&#10060; No</td><td>Two territorial fish, one floor; oscar fins get shredded</td></tr>
      <tr><td>African cichlids</td><td>&#10060; No</td><td>Hard alkaline water is wrong for <em>Channa</em>; relentless aggression</td></tr>
      <tr><td>Corydoras, small catfish</td><td>&#10060; No</td><td>Mouth-sized and on the floor &mdash; both rules broken</td></tr>
      <tr><td>Bristlenose pleco</td><td>&#10060; No</td><td>Fine with a 4-inch dwarf, food for anything larger</td></tr>
      <tr><td>Shrimp and snails</td><td>&#10060; No</td><td>Food</td></tr>
      <tr><td>Turtles</td><td>&#10060; No</td><td>Both bite; both need the surface</td></tr>
    </table>

    <h2 id="conspecific">Snakeheads With Other Snakeheads</h2>
    <p>Conspecific aggression is the number one killer in mixed snakehead tanks. Three arrangements are worth knowing:</p>
    <ul>
      <li><strong>A bonded pair</strong> &mdash; stable, and the only setup that reliably works long term. Pairs form on their own from a grow-out group; you cannot buy one. See <a href="/guides/snakehead-fish-care/male-vs-female/">male vs female</a>.</li>
      <li><strong>A grow-out group of juveniles from one batch</strong> &mdash; works for a while in an oversized, heavily broken-up tank. Expect to break it up as fish mature and a pair forms. Have somewhere for the surplus fish to go before you start.</li>
      <li><strong>Two adults introduced to each other</strong> &mdash; almost always fails, often within hours. Do not attempt it in anything under a very large tank with a full divider available.</li>
    </ul>
    <p>Never mix species. Two different <em>Channa</em> in one tank combine incompatible temperature needs with maximum aggression.</p>

    <h2 id="dwarf-community">Dwarf Snakehead Community Tanks</h2>
    <p>This is the one genuinely workable community setup. A single <em>C. andrao</em> or <em>C. bleheri</em> in a 55&ndash;75 gallon planted tank can live with fast mid-water dithers &mdash; rosy barbs, tiger barbs, larger danios, big rasboras, <em>Garra</em> and hillstream loaches. Dithers actually help: a snakehead that sees other fish feeding confidently spends more time in the open.</p>
    <p>Make it work by:</p>
    <ul>
      <li><strong>Adding the dithers first</strong> and letting them establish before the snakehead goes in.</li>
      <li><strong>Choosing fish over 2 inches</strong> and keeping them in groups of 8+, so no individual is singled out.</li>
      <li><strong>Breaking the tank up</strong> with wood, plants and floating cover so nothing is ever cornered.</li>
      <li><strong>Accepting attrition.</strong> Even in a good setup, an occasional dither disappears.</li>
      <li><strong>Having a backup tank ready</strong> for the day the snakehead decides it is done sharing &mdash; which typically coincides with maturity or a spawning attempt.</li>
    </ul>

    <h2 id="big-species">Large Snakeheads: What Actually Works</h2>
    <p>For anything over about 16 inches, the realistic list is short: a similarly sized bichir, a large armoured catfish, or nothing. Both options need a tank measured in hundreds of gallons, and both fail if the snakehead spawns. Keepers of <em>C. micropeltes</em>, <em>C. marulius</em> and <em>C. argus</em> almost universally end up with a species-only tank, usually after losing something expensive.</p>
    <div class="callout callout-warn"><strong>Introducing a tank mate to an established snakehead rarely works.</strong> The snakehead already owns the tank. If you must, rearrange the d&eacute;cor completely on the day so territory is reset for everyone, add the new fish in the evening with the lights off, and be ready to remove it.</div>

    <h2 id="aggression">Are Snakeheads Aggressive?</h2>
    <p>Yes, on a sliding scale by species &mdash; and this is the practical ranking that matters when choosing tank mates:</p>
    <table class="ptbl">
      <tr><th>Species</th><th>Aggression</th><th>Community potential</th></tr>
      <tr><td><em>C. andrao</em>, <em>C. bleheri</em></td><td>Mild for the genus</td><td>Dwarf community possible</td></tr>
      <tr><td><em>C. gachua</em> / <em>C. limbata</em></td><td>Moderate, population-dependent</td><td>Possible with large dithers</td></tr>
      <tr><td><em>C. pulchra</em>, <em>C. asiatica</em>, <em>C. stewartii</em></td><td>Moderate to high</td><td>Species tank preferred</td></tr>
      <tr><td><em>C. aurantimaculata</em>, <em>C. marulioides</em></td><td>High</td><td>Species tank</td></tr>
      <tr><td><em>C. micropeltes</em>, <em>C. marulius</em>, <em>C. argus</em></td><td>Very high</td><td>Species tank only</td></tr>
    </table>
    <p>All of them escalate sharply when spawning. A pair that has tolerated tank mates for a year will clear the tank in a night once eggs are involved &mdash; see <a href="/guides/snakehead-fish-care/breeding/">breeding</a>. Sanity-check any pairing you are considering with the <a href="/tools/fish-compatibility-checker/">fish compatibility checker</a>.</p>
"""

MATES = {
    "slug": "tank-mates",
    "title": "Snakehead Fish Tank Mates: What Can Live With a Channa?",
    "meta_desc": "Snakehead fish tank mates that work: dither fish for dwarf Channa, bichirs for large species, and why oscars, arowanas and cichlids fail.",
    "h1": "Snakehead Fish Tank Mates",
    "hero_tag": "Tank Mates",
    "hero_meta": "\U0001F420 Species tank is usually right &nbsp;|&nbsp; ⚡ Dithers work with dwarfs &nbsp;|&nbsp; \U0001F6AB Never mix Channa species",
    "toc_sections": [
        ("rules", "The Three Rules"),
        ("compatibility", "Compatibility Chart"),
        ("conspecific", "With Other Snakeheads"),
        ("dwarf-community", "Dwarf Community Tanks"),
        ("big-species", "Large Species"),
        ("aggression", "Aggression by Species"),
    ],
    "body": MATES_BODY,
    "faqs": [
        ("What fish can live with a snakehead?",
         "For dwarf species such as Channa andrao and Channa bleheri, fast mid-water dither fish over 2 inches work well in a 55-75 gallon planted tank - rosy barbs, tiger barbs, large danios, big rasboras, Garra and hillstream loaches. For large snakeheads the realistic options are a similarly sized bichir, a large armoured catfish, or nothing at all."),
        ("Can two snakeheads live together?",
         "Only as a bonded pair of the same species, which forms on its own from a grow-out group of juveniles and cannot be bought ready-made. A group of same-batch juveniles works for a while in an oversized broken-up tank, but two unfamiliar adults introduced to each other almost always fight, often within hours. Never mix different Channa species."),
        ("Can a snakehead live with an oscar?",
         "It is a bad pairing. Both are territorial fish that claim the bottom of the tank, and an oscar's long fins get shredded even when the snakehead cannot eat it. It sometimes holds in a very large tank but ends badly often enough that it is not worth attempting."),
        ("Can snakeheads live with bichirs?",
         "This is the best of the large-fish pairings. Bichirs share the snakehead's water requirements, are armoured, and are also air-breathers, so the surface-trip behaviour does not surprise them. Match the sizes closely - a snakehead will eat a smaller bichir, and a bichir is slow enough to be bitten by a much larger one."),
        ("Are snakehead fish aggressive?",
         "Yes, on a sliding scale. Channa bleheri and Channa andrao are comparatively mild, Channa pulchra and Channa aurantimaculata are moderate to high, and Channa micropeltes, Channa marulius and Channa argus are very aggressive species-tank-only fish. Every species escalates sharply when spawning - a pair that has tolerated tank mates for a year will clear the tank once eggs are involved."),
        ("Can a pleco live with a snakehead?",
         "A large common pleco or Synodontis can work with a mid-sized or large snakehead, though plecos sometimes rasp at the slime coat of a resting fish. A bristlenose pleco is fine alongside a 4-inch dwarf Channa but is simply food for anything larger."),
    ],
    "related": [
        ("/tools/fish-compatibility-checker/", "Compatibility Checker"),
        ("/guides/snakehead-fish-care/types/", "Snakehead Types & Species"),
        ("/guides/snakehead-fish-care/breeding/", "Breeding Snakeheads"),
        ("/guides/snakehead-fish-care/tank-size/", "Tank Size & Setup"),
    ],
}


# ════════════════════════════════════════════════════════════════
PAGES = [PILLAR, TYPES, TANK, WATER, FEEDING, SIZE, LIFESPAN, MVF, BREEDING, DISEASES, MATES]


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
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        url = f"/guides/snakehead-fish-care/{spec['slug']}/" if spec["slug"] else "/guides/snakehead-fish-care/"
        print(f"  {url:<48} {len(html):>7,} bytes")
    print(f"\n{len(PAGES)} pages written to {BASE}")


if __name__ == "__main__":
    main()
