"""
generate_puffer_cluster.py
──────────────────────────
Generates the Puffer Fish (Tetraodontidae) care cluster under
/guides/puffer-fish-care/, following the snakehead/oscar/koi cluster template
(artlay 2-column with sidebar cluster nav).

The pillar page is generated too — no puffer pillar existed before.
Re-runnable and idempotent.

Run:  python3 generate_puffer_cluster.py
"""

from pathlib import Path
import json

REPO = Path(__file__).parent.parent
BASE = REPO / "guides" / "puffer-fish-care"

HERO_IMG = "/assets/encyclopedia/real/dwarf-puffer-wikimedia-real.jpg"
DATE = "2026-09-09"

CLUSTER_NAV = [
    ("/guides/puffer-fish-care/",                       "\U0001F421 Puffer Fish Care Guide", "pillar"),
    ("/guides/puffer-fish-care/types/",                 "\U0001F3A8 Types & Species"),
    ("/guides/puffer-fish-care/freshwater/",            "\U0001F4A7 Freshwater Puffers"),
    ("/guides/puffer-fish-care/saltwater/",             "\U0001F30A Saltwater Puffers"),
    ("/guides/puffer-fish-care/tank-size/",             "\U0001F5C3\uFE0F Tank Size & Setup"),
    ("/guides/puffer-fish-care/water-parameters/",      "\U0001F321\uFE0F Water & Temperature"),
    ("/guides/puffer-fish-care/food/",                  "\U0001F35A Food & Feeding"),
    ("/guides/puffer-fish-care/teeth/",                 "\U0001F9B7 Teeth & Trimming"),
    ("/guides/puffer-fish-care/size-growth/",           "\U0001F4CF Size & Growth"),
    ("/guides/puffer-fish-care/lifespan/",              "\u23F3 Lifespan"),
    ("/guides/puffer-fish-care/pea-puffer/",            "\U0001F7E2 Pea / Dwarf Puffer"),
    ("/guides/puffer-fish-care/figure-8-puffer/",       "\U0001F004 Figure 8 Puffer"),
    ("/guides/puffer-fish-care/green-spotted-puffer/",  "\U0001F7E1 Green Spotted Puffer"),
    ("/guides/puffer-fish-care/amazon-puffer/",         "\U0001F30D Amazon Puffer"),
    ("/guides/puffer-fish-care/fahaka-puffer/",         "\U0001F1EA\U0001F1EC Fahaka Puffer"),
    ("/guides/puffer-fish-care/mbu-puffer/",            "\U0001F40B Mbu Puffer"),
    ("/guides/puffer-fish-care/breeding/",              "\U0001F95A Breeding & Sexing"),
    ("/guides/puffer-fish-care/tank-mates/",            "\U0001F420 Tank Mates"),
    ("/guides/puffer-fish-care/behavior/",              "\U0001F620 Aggression & Behavior"),
    ("/guides/puffer-fish-care/diseases/",              "\U0001FA7A Diseases & Parasites"),
    ("/guides/puffer-fish-care/not-eating/",            "\U0001F6AB Not Eating & Hiding"),
    ("/guides/puffer-fish-care/puffing-up/",            "\U0001F388 Puffing Up & Bloating"),
    ("/guides/puffer-fish-care/color-change/",          "\u26AB Color Changes"),
    ("/guides/puffer-fish-care/swimming-problems/",     "\U0001F300 Swimming & Breathing"),
    ("/wiki/pea-puffer/",                               "\U0001F4D6 Pea Puffer Profile"),
    ("/compatibility/pea-puffer/",                      "\U0001F91D Pea Puffer Pairings"),
]

TOOL_LINKS = [
    ("/tools/tank-size-calculator/",       "Tank Size Calculator"),
    ("/tools/water-parameter-checker/",    "Water Parameter Checker"),
    ("/tools/fish-compatibility-checker/", "Compatibility Checker"),
    ("/tools/fish-feeding-calculator/",    "Feeding Calculator"),
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
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('__HERO__') center/cover no-repeat}
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
.tblwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:16px 0}
.ptbl{width:100%;border-collapse:collapse;margin:0;font-size:.86rem;border-radius:16px;overflow:hidden;box-shadow:0 12px 30px rgba(15,61,110,.08)}
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
            is_cur = href == "/guides/puffer-fish-care/"
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
    return ('    <h2 id="related">Related Puffer Fish Guides and Tools</h2>\n'
            f'    <div class="guide-links">{items}</div>')


def page(slug, title, meta_desc, h1, hero_tag, hero_meta,
         toc_sections, body_html, faqs, related, date=DATE, hero_img=HERO_IMG):
    if slug:
        canonical = f"https://www.fishcareai.com/guides/puffer-fish-care/{slug}/"
        crumb_tail = (
            '<a href="/guides/puffer-fish-care/">Puffer Fish Care Guide</a><span>/</span>\n      '
            f'<span style="color:rgba(255,255,255,.9)">{hero_tag}</span>'
        )
        breadcrumb_items = (
            '{"@type":"ListItem","position":3,"name":"Puffer Fish Care Guide",'
            '"item":"https://www.fishcareai.com/guides/puffer-fish-care/"},'
            f'{{"@type":"ListItem","position":4,"name":{json.dumps(h1)},"item":"{canonical}"}}'
        )
    else:
        canonical = "https://www.fishcareai.com/guides/puffer-fish-care/"
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
        "image": f"https://www.fishcareai.com{hero_img}",
        "about": {"@type": "Thing", "name": "Puffer fish (Tetraodontidae)"},
        "inLanguage": "en",
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
<meta property="og:image" content="https://www.fishcareai.com{hero_img}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{meta_desc}"/>
<meta name="twitter:image" content="https://www.fishcareai.com{hero_img}"/>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{faq_json(faqs)}</script>
<style>{CSS.replace("__HERO__", hero_img)}</style>
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
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">&#128033; Puffer Fish Care</div>
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
      <h4>Puffer Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc)}
    </div>
    <div class="tool-card">
      <h4>Puffer Fish Tools</h4>
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
# PILLAR — Puffer Fish Care Guide
# ════════════════════════════════════════════════════════════════
PILLAR_BODY = """    <p>Puffer fish (family <strong>Tetraodontidae</strong>) are the most personality-heavy fish in the hobby and the most commonly mis-sold. The family name means &ldquo;four teeth&rdquo; &mdash; every true puffer has four fused tooth plates forming a parrot-like beak that never stops growing. Around 200 species are described, roughly 30 of them spend part or all of their lives in fresh or brackish water, and the rest are marine.</p>
    <p>That spread is why generic &ldquo;puffer fish care&rdquo; advice fails so often. A <a href="/guides/puffer-fish-care/pea-puffer/">pea puffer</a> is a 1.4-inch true freshwater fish that lives happily in a 10-gallon tank. A <a href="/guides/puffer-fish-care/green-spotted-puffer/">green spotted puffer</a> sold in the same shop tank will die slowly in that water because it needs to finish its life in near-marine salinity. An <a href="/guides/puffer-fish-care/mbu-puffer/">mbu puffer</a> reaches over two feet and needs a swimming pool of a tank. Identify the species first; everything else follows from it.</p>

    <div class="callout callout-warn"><strong>Before you buy.</strong> Ask the shop for the scientific name, not the trade name. &ldquo;Freshwater puffer&rdquo; on a shop label routinely covers brackish species (<em>Dichotomyctere</em>) and giants (<em>Tetraodon lineatus</em>, <em>T. mbu</em>). Use the <a href="/guides/puffer-fish-care/types/">puffer species table</a> to match the fish to its real requirements.</div>

    <h2 id="what-is">What Is a Puffer Fish?</h2>
    <p>Tetraodontidae sits inside the order Tetraodontiformes alongside boxfish, triggerfish and porcupinefish. Puffers share a set of traits no other aquarium fish combines:</p>
    <ul>
      <li><strong>No scales and no pelvic fins.</strong> The skin is bare or covered in small spines. This is the single most important care fact, because it makes puffers sensitive to copper, formalin and full-strength medications &mdash; see <a href="/guides/puffer-fish-care/diseases/">puffer diseases</a>.</li>
      <li><strong>A fused four-plate beak that grows for life.</strong> Fed soft food only, the beak overgrows and the fish starves. See <a href="/guides/puffer-fish-care/teeth/">puffer fish teeth and trimming</a>.</li>
      <li><strong>Inflation.</strong> Puffers gulp water into a highly elastic stomach diverticulum to roughly triple in volume. It is a last-resort defence, not a trick. See <a href="/guides/puffer-fish-care/puffing-up/">puffing up and bloating</a>.</li>
      <li><strong>Tetrodotoxin.</strong> Most species carry TTX, a potent neurotoxin, in skin, liver and gonads. It is acquired from bacteria in their food chain, so aquarium-raised puffers carry far less &mdash; but never eat one, and wash hands after tank work if you have open cuts.</li>
      <li><strong>Pectoral-fin swimming.</strong> Puffers hover and reverse using their pectoral fins, which is why they are slow, precise, endlessly curious and completely unable to outrun a fin-nipping tank mate.</li>
    </ul>

    <h2 id="quick-numbers">Puffer Fish Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Water</th><th>Minimum tank</th><th>Lifespan</th></tr>
      <tr><td><a href="/guides/puffer-fish-care/pea-puffer/">Pea / dwarf puffer</a></td><td>1&ndash;1.4 in</td><td>Fresh</td><td>10 gal (trio)</td><td>4&ndash;5 yrs</td></tr>
      <tr><td>Red eye puffer</td><td>2 in</td><td>Fresh</td><td>15 gal</td><td>5&ndash;8 yrs</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/figure-8-puffer/">Figure 8 puffer</a></td><td>3 in</td><td>Low brackish</td><td>15&ndash;20 gal</td><td>10&ndash;15 yrs</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/amazon-puffer/">Amazon puffer</a></td><td>3&ndash;3.5 in</td><td>Fresh</td><td>30 gal (group)</td><td>8&ndash;10 yrs</td></tr>
      <tr><td>Avocado puffer</td><td>4&ndash;5 in</td><td>Fresh</td><td>40 gal</td><td>8&ndash;10 yrs</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/green-spotted-puffer/">Green spotted puffer</a></td><td>6 in</td><td>High brackish &rarr; marine</td><td>30 gal</td><td>10&ndash;15 yrs</td></tr>
      <tr><td>Congo puffer</td><td>6 in</td><td>Fresh</td><td>40 gal</td><td>8&ndash;10 yrs</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/fahaka-puffer/">Fahaka puffer</a></td><td>16&ndash;18 in</td><td>Fresh</td><td>125 gal</td><td>10&ndash;15 yrs</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/mbu-puffer/">Mbu puffer</a></td><td>24&ndash;30 in</td><td>Fresh</td><td>500+ gal</td><td>10&ndash;20 yrs</td></tr>
    </table></div>
    <p>Full breakdown on the <a href="/guides/puffer-fish-care/types/">types of puffer fish</a> page, with <a href="/guides/puffer-fish-care/freshwater/">freshwater</a> and <a href="/guides/puffer-fish-care/saltwater/">saltwater</a> guides for each group.</p>

    <h2 id="tank">Tank Size and Setup</h2>
    <p>Puffers are heavy waste producers on a meat-based diet, so tank volume is filtration headroom as much as swimming room. The working rule for the small species is <strong>5 gallons per pea puffer after the first 10</strong>, and for everything above 3 inches it is <strong>at least 30 gallons for the first fish plus most of that again for a second</strong> &mdash; if a second is possible at all.</p>
    <ul>
      <li><strong>Filtration:</strong> 6&ndash;8&times; tank volume per hour, biased toward mechanical and biological media. Oversize it.</li>
      <li><strong>Water changes:</strong> 30&ndash;50% weekly on any puffer tank. Nitrate under 20 ppm.</li>
      <li><strong>Cover and structure:</strong> heavy planting, driftwood and rockwork for small species; open sand and a few big anchors for burrowers and giants.</li>
      <li><strong>Lid:</strong> required. Puffers are curious and will follow food to the surface.</li>
    </ul>
    <p>Details and per-species numbers: <a href="/guides/puffer-fish-care/tank-size/">puffer fish tank size</a>.</p>

    <h2 id="water">Water Parameters</h2>
    <p>Most freshwater puffers want <strong>75&ndash;82&deg;F (24&ndash;28&deg;C)</strong>, <strong>pH 7.0&ndash;8.0</strong> and moderately hard water at <strong>8&ndash;15 dGH</strong>. Ammonia and nitrite must read zero at all times; puffers are scaleless and show ammonia damage faster than almost anything else you can keep.</p>
    <p>Brackish species add salinity to that list, and the target changes with age for green spotted puffers. Get the numbers and the mixing method on the <a href="/guides/puffer-fish-care/water-parameters/">puffer water parameters</a> page, then check your own readings with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="food">Food and Feeding</h2>
    <p>Puffers are molluscivores and crustacean specialists. <strong>Almost no puffer will accept flake or pellet food</strong>, and the ones that nibble at it still need hard-shelled prey to wear their beak down.</p>
    <ul>
      <li><strong>Staple hard food:</strong> pest snails (ramshorn, bladder, Malaysian trumpet), small clams, cockles, mussel, unpeeled shrimp, crayfish pieces.</li>
      <li><strong>Soft supplements:</strong> frozen bloodworms, blackworms, brine shrimp, mysis, krill, silversides for the large species.</li>
      <li><strong>Frequency:</strong> daily for fish under 2 inches, 4&ndash;5 times a week for mid-size, 2&ndash;3 times a week for adults over 6 inches.</li>
      <li><strong>Never feed feeder goldfish or rosy reds.</strong> They carry thiaminase and parasites and are a common cause of long-term puffer decline.</li>
    </ul>
    <p>Full feeding schedules by species and age: <a href="/guides/puffer-fish-care/food/">what do puffer fish eat</a>.</p>

    <h2 id="mates">Tank Mates and Temperament</h2>
    <p>Assume every puffer is a fin-nipper until proven otherwise, and assume every shrimp and ornamental snail is food. Some species &mdash; fahaka, mbu, congo, avocado, adult green spotted &mdash; are effectively <strong>single-specimen fish</strong>. Others tolerate carefully chosen, fast, short-finned company.</p>
    <p>Individual pairings are covered in the <a href="/compatibility/pea-puffer/">pea puffer compatibility hub</a>, and the general rules are on the <a href="/guides/puffer-fish-care/tank-mates/">puffer fish tank mates</a> page. Behaviour, chasing and fighting are on the <a href="/guides/puffer-fish-care/behavior/">aggression page</a>.</p>

    <h2 id="health">Health and Common Problems</h2>
    <p>Because puffers have no scales, they absorb medication faster than scaled fish and are damaged by standard doses of copper, formalin and some organophosphates. Dose at <strong>half strength</strong> unless the label specifically covers scaleless fish, and treat in a bare quarantine tank whenever possible.</p>
    <div class="guide-links" style="margin-top:14px">
      <a href="/guides/puffer-fish-care/diseases/">Diseases, ich, fin rot &amp; parasites</a>
      <a href="/guides/puffer-fish-care/not-eating/">Puffer not eating or hiding</a>
      <a href="/guides/puffer-fish-care/puffing-up/">Puffed up, inflated or bloated</a>
      <a href="/guides/puffer-fish-care/color-change/">Turning black or losing colour</a>
      <a href="/guides/puffer-fish-care/swimming-problems/">Swimming sideways or gasping</a>
      <a href="/guides/puffer-fish-care/teeth/">Overgrown teeth</a>
    </div>

    <h2 id="series">The Puffer Fish Care Series</h2>
    <p>Twenty-three companion guides cover every part of puffer keeping in detail:</p>
    <div class="guide-links">
      <a href="/guides/puffer-fish-care/types/">Types &amp; Species</a>
      <a href="/guides/puffer-fish-care/freshwater/">Freshwater Puffer Fish</a>
      <a href="/guides/puffer-fish-care/saltwater/">Saltwater Puffer Fish</a>
      <a href="/guides/puffer-fish-care/tank-size/">Tank Size &amp; Setup</a>
      <a href="/guides/puffer-fish-care/water-parameters/">Water &amp; Temperature</a>
      <a href="/guides/puffer-fish-care/food/">Food &amp; Feeding</a>
      <a href="/guides/puffer-fish-care/teeth/">Teeth &amp; Trimming</a>
      <a href="/guides/puffer-fish-care/size-growth/">Size &amp; Growth Rate</a>
      <a href="/guides/puffer-fish-care/lifespan/">Lifespan</a>
      <a href="/guides/puffer-fish-care/pea-puffer/">Pea / Dwarf Puffer</a>
      <a href="/guides/puffer-fish-care/figure-8-puffer/">Figure 8 Puffer</a>
      <a href="/guides/puffer-fish-care/green-spotted-puffer/">Green Spotted Puffer</a>
      <a href="/guides/puffer-fish-care/amazon-puffer/">Amazon Puffer</a>
      <a href="/guides/puffer-fish-care/fahaka-puffer/">Fahaka Puffer</a>
      <a href="/guides/puffer-fish-care/mbu-puffer/">Mbu Puffer</a>
      <a href="/guides/puffer-fish-care/breeding/">Breeding &amp; Sexing</a>
      <a href="/guides/puffer-fish-care/tank-mates/">Tank Mates</a>
      <a href="/guides/puffer-fish-care/behavior/">Aggression &amp; Behaviour</a>
      <a href="/guides/puffer-fish-care/diseases/">Diseases &amp; Parasites</a>
      <a href="/guides/puffer-fish-care/not-eating/">Not Eating &amp; Hiding</a>
      <a href="/guides/puffer-fish-care/puffing-up/">Puffing Up &amp; Bloating</a>
      <a href="/guides/puffer-fish-care/color-change/">Colour Changes</a>
      <a href="/guides/puffer-fish-care/swimming-problems/">Swimming &amp; Breathing</a>
    </div>
"""

PILLAR = {
    "slug": "",
    "title": "Puffer Fish Care Guide: Tank, Water, Food and Species",
    "meta_desc": "Complete puffer fish care guide: tank size, water parameters, feeding, teeth, tank mates and lifespan for pea, figure 8, green spotted, fahaka and mbu puffers.",
    "h1": "Puffer Fish Care Guide (Tetraodontidae)",
    "hero_tag": "Puffer Fish Care Guide",
    "hero_meta": "\U0001F421 ~200 species &nbsp;|&nbsp; \U0001F5C3️ 10&ndash;500+ gal &nbsp;|&nbsp; \U0001F321️ 75&ndash;82&deg;F &nbsp;|&nbsp; ⏳ 4&ndash;20 yrs",
    "toc_sections": [
        ("what-is", "What Is a Puffer Fish?"),
        ("quick-numbers", "Care at a Glance"),
        ("tank", "Tank Size & Setup"),
        ("water", "Water Parameters"),
        ("food", "Food & Feeding"),
        ("mates", "Tank Mates"),
        ("health", "Health Problems"),
        ("series", "The Full Series"),
    ],
    "body": PILLAR_BODY,
    "faqs": [
        ("How do you care for a puffer fish?",
         "Identify the species first, because requirements vary enormously. Give it the right water type (fresh, brackish or marine), a tank sized for the adult fish, 6-8 times turnover filtration and 30-50% weekly water changes, and feed hard-shelled foods such as snails, clams and unpeeled shrimp so the beak wears down. Keep ammonia and nitrite at zero and nitrate under 20 ppm."),
        ("What is the easiest puffer fish to keep?",
         "The pea puffer (Carinotetraodon travancoricus) is the easiest for most aquarists. It stays under 1.5 inches, lives in true freshwater, and a trio fits in a 10 gallon planted tank. Its only demanding requirement is live or frozen food, including a steady supply of pest snails."),
        ("Are puffer fish poisonous to keep in an aquarium?",
         "Most puffers carry tetrodotoxin in their skin and organs, but it is not released into the water and handling a healthy puffer is not dangerous. The risk is in eating one, or in a puffer dying and being eaten by tank mates. Wash your hands after tank maintenance and never consume aquarium puffers."),
        ("Can puffer fish live in freshwater?",
         "Some can. About 30 species are true freshwater fish, including the pea puffer, Amazon puffer, congo puffer, fahaka and mbu. Others such as the green spotted puffer and figure 8 puffer are brackish and decline in plain freshwater even though shops sell them from freshwater tanks."),
        ("Do puffer fish need a big tank?",
         "It depends entirely on species. A pea puffer trio needs 10 gallons, a figure 8 puffer needs 15-20 gallons, a green spotted puffer needs 30 gallons, a fahaka puffer needs 125 gallons and an mbu puffer realistically needs 500 gallons or a custom pond."),
        ("Why won't my puffer fish eat pellets?",
         "Puffers are molluscivores with a fused beak built for crushing shells, and most simply do not recognise dry food as prey. Even the individuals that will pick at pellets still need hard-shelled food to grind their continuously growing teeth down."),
        ("How long do puffer fish live?",
         "Between four and twenty years depending on species. Pea puffers live 4-5 years, figure 8 and green spotted puffers 10-15 years, and fahaka and mbu puffers 10-20 years or more in a large, well-maintained tank."),
    ],
    "related": [
        ("/guides/puffer-fish-care/types/", "Types of Puffer Fish"),
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
        ("/guides/puffer-fish-care/food/", "What Do Puffer Fish Eat"),
        ("/wiki/pea-puffer/", "Pea Puffer Species Profile"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TYPES & SPECIES
# ════════════════════════════════════════════════════════════════
TYPES_BODY = """    <p>&ldquo;Puffer fish&rdquo; covers about 200 species in the family Tetraodontidae plus a handful of look-alikes from neighbouring families that the trade sells under the same name. Around thirty live in fresh or brackish water; the rest are marine. This page lists the species you will actually meet in a shop, what they really need, and which trade names hide which fish.</p>

    <h2 id="freshwater-species">Freshwater Puffer Fish Species</h2>
    <p>These are true freshwater puffers &mdash; they live their whole lives without added salt. Everything else marketed as a &ldquo;freshwater puffer&rdquo; is brackish and will decline in plain fresh water.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Common name</th><th>Scientific name</th><th>Adult size</th><th>Minimum tank</th><th>Temperament</th></tr>
      <tr><td>Pea / dwarf / Indian dwarf puffer</td><td><em>Carinotetraodon travancoricus</em></td><td>1&ndash;1.4 in</td><td>10 gal (trio)</td><td>Territorial, fin-nipper</td></tr>
      <tr><td>Red eye puffer</td><td><em>Carinotetraodon irrubesco</em></td><td>2 in</td><td>15 gal</td><td>Mildest of the small puffers</td></tr>
      <tr><td>Amazon / South American / bee puffer</td><td><em>Colomesus asellus</em></td><td>3&ndash;3.5 in</td><td>30 gal (group of 5+)</td><td>Shoaling, hyperactive nipper</td></tr>
      <tr><td>Avocado / bronze puffer</td><td><em>Auriglobus modestus</em></td><td>4&ndash;5 in</td><td>40 gal</td><td>Fast, highly aggressive</td></tr>
      <tr><td>Congo / potato puffer</td><td><em>Tetraodon miurus</em></td><td>6 in</td><td>40 gal</td><td>Ambush predator, solitary</td></tr>
      <tr><td>Hairy puffer</td><td><em>Pao baileyi</em></td><td>6 in</td><td>55 gal</td><td>Ambush predator, solitary</td></tr>
      <tr><td>Fahaka / Nile / lineatus puffer</td><td><em>Tetraodon lineatus</em></td><td>16&ndash;18 in</td><td>125 gal</td><td>Solitary, dangerous to tank mates</td></tr>
      <tr><td>Mbu / giant puffer</td><td><em>Tetraodon mbu</em></td><td>24&ndash;30 in</td><td>500+ gal</td><td>Solitary specimen fish</td></tr>
    </table></div>
    <p>Care detail for the freshwater group is on the <a href="/guides/puffer-fish-care/freshwater/">freshwater puffer fish</a> page.</p>

    <h2 id="brackish-species">Brackish Puffer Fish Species</h2>
    <p>Brackish puffers are the most commonly mis-sold fish in the hobby, because juveniles look fine in freshwater shop tanks for months before the damage shows.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Common name</th><th>Scientific name</th><th>Adult size</th><th>Salinity target</th><th>Minimum tank</th></tr>
      <tr><td><a href="/guides/puffer-fish-care/figure-8-puffer/">Figure 8 puffer</a></td><td><em>Dichotomyctere ocellatus</em></td><td>3 in</td><td>SG 1.005&ndash;1.008 lifelong</td><td>15&ndash;20 gal</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/green-spotted-puffer/">Green spotted puffer</a></td><td><em>Dichotomyctere nigroviridis</em></td><td>6 in</td><td>SG 1.005 juvenile &rarr; 1.018&ndash;1.022 adult</td><td>30 gal</td></tr>
      <tr><td>Ceylon / Topaz puffer</td><td><em>Dichotomyctere fluviatilis</em></td><td>6&ndash;7 in</td><td>SG 1.005&ndash;1.015</td><td>40 gal</td></tr>
      <tr><td>Target / arrowhead puffer</td><td><em>Dichotomyctere sp.</em></td><td>5&ndash;6 in</td><td>SG 1.005&ndash;1.012</td><td>40 gal</td></tr>
    </table></div>

    <h2 id="saltwater-species">Saltwater Puffer Fish Species</h2>
    <p>Marine puffers split into true puffers (Tetraodontidae), the small tobies of the genus <em>Canthigaster</em>, and the porcupinefish of the related family Diodontidae, which the trade sells as puffers too.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Common name</th><th>Scientific name</th><th>Adult size</th><th>Minimum tank</th><th>Reef safe?</th></tr>
      <tr><td>Valentini / black-saddled toby</td><td><em>Canthigaster valentini</em></td><td>4 in</td><td>30 gal</td><td>No &mdash; nips corals and clams</td></tr>
      <tr><td>Dogface puffer</td><td><em>Arothron nigropunctatus</em></td><td>12&ndash;13 in</td><td>180 gal</td><td>No</td></tr>
      <tr><td>Porcupine puffer</td><td><em>Diodon holocanthus</em></td><td>12&ndash;14 in</td><td>125 gal</td><td>No</td></tr>
      <tr><td>Spiny box / burrfish</td><td><em>Chilomycterus schoepfi</em></td><td>8&ndash;10 in</td><td>100 gal</td><td>No</td></tr>
      <tr><td>Stars and stripes puffer</td><td><em>Arothron hispidus</em></td><td>18&ndash;20 in</td><td>250 gal</td><td>No</td></tr>
    </table></div>
    <p>Marine care detail is on the <a href="/guides/puffer-fish-care/saltwater/">saltwater puffer fish</a> page.</p>

    <h2 id="small">Small Puffer Fish for Small Tanks</h2>
    <p>Only three puffers are genuinely small-tank fish, and only one of them is a beginner fish:</p>
    <ul>
      <li><strong>Pea puffer, 1&ndash;1.4 in &mdash; 10 gallons for a trio.</strong> The only puffer most aquarists should start with. Full care on the <a href="/guides/puffer-fish-care/pea-puffer/">pea puffer page</a>.</li>
      <li><strong>Red eye puffer, 2 in &mdash; 15 gallons.</strong> Less common, less aggressive, slightly fussier about soft acidic water than the pea puffer.</li>
      <li><strong>Figure 8 puffer, 3 in &mdash; 15&ndash;20 gallons.</strong> Small but brackish, so it needs a hydrometer or refractometer and marine salt for life.</li>
    </ul>
    <div class="callout callout-warn"><strong>Not small:</strong> green spotted puffers are sold at 1 inch and reach 6, fahakas are sold at 2 inches and reach 18, and mbu puffers are sold as cute juveniles and reach two and a half feet. Buy for the adult size on the <a href="/guides/puffer-fish-care/size-growth/">growth page</a>.</div>

    <h2 id="species-notes">Species Notes on Less Common Puffers</h2>
    <h3>Congo puffer (<em>Tetraodon miurus</em>)</h3>
    <p>A true freshwater ambush predator from the Congo River rapids. It buries itself in fine sand with only the eyes and upturned mouth exposed and takes prey with an explosive lunge. Give it 40 gallons, 3&ndash;4 inches of soft sand, strong flow and no tank mates &mdash; it will attack fish several times its own length. Colour varies from brick red through orange to grey and shifts with substrate and mood.</p>
    <h3>Hairy puffer (<em>Pao baileyi</em>)</h3>
    <p>A Mekong species covered in cutaneous cirri &mdash; the &ldquo;hair&rdquo; is skin, not algae. Another sit-and-wait predator: it perches on wood in fast water and rarely swims. Wants 55 gallons, high flow, cool-to-moderate temperatures around 75&ndash;79&deg;F, and strictly solitary housing. Almost always wild-caught, so a deworming quarantine is standard.</p>
    <h3>Avocado puffer (<em>Auriglobus modestus</em>)</h3>
    <p>Also sold as bronze or golden puffer. Unlike most puffers it is a fast open-water swimmer, which makes it both a good display fish and a relentless attacker of anything with fins. Forty gallons minimum with a long footprint, and single-specimen housing.</p>
    <h3>Red eye puffer (<em>Carinotetraodon irrubesco</em>)</h3>
    <p>A 2-inch Sumatran and Bornean species with a red tail on the male. It is the closest thing to a peaceful puffer &mdash; still not community safe, but a pair can often share 15&ndash;20 gallons. Prefers soft, slightly acidic water and dim, heavily planted tanks.</p>

    <h2 id="identify">How to Identify Which Puffer You Bought</h2>
    <ol>
      <li><strong>Count the spots and check the belly.</strong> A bright white belly with black-green spotting on a golden-green back is a green spotted puffer. A brown fish with yellow figure-eight and ring markings is a figure 8.</li>
      <li><strong>Measure it.</strong> Under 1.5 inches with a yellow-green body and dark blotches is a pea puffer.</li>
      <li><strong>Look for vertical stripes.</strong> Bold yellow-and-brown horizontal striping with an orange belly on a fish already over 3 inches is a fahaka.</li>
      <li><strong>Look at the eyes.</strong> Eyes set on top of the head with an upturned mouth means an ambush burrower: congo or hairy puffer.</li>
      <li><strong>Ask for the scientific name.</strong> If the shop cannot give one, assume it is brackish and expensive to keep until proven otherwise.</li>
    </ol>
"""

TYPES = {
    "slug": "types",
    "title": "Types of Puffer Fish: 20 Species by Size and Water Type",
    "meta_desc": "Types of puffer fish compared: freshwater, brackish and saltwater species with adult size, tank size and temperament, from pea puffers to the mbu.",
    "h1": "Types of Puffer Fish and Puffer Species",
    "hero_tag": "Types & Species",
    "hero_meta": "\U0001F3A8 ~200 species &nbsp;|&nbsp; \U0001F4A7 8 freshwater &nbsp;|&nbsp; \U0001F9C2 4 brackish &nbsp;|&nbsp; \U0001F30A 5 marine",
    "toc_sections": [
        ("freshwater-species", "Freshwater Species"),
        ("brackish-species", "Brackish Species"),
        ("saltwater-species", "Saltwater Species"),
        ("small", "Small Puffer Fish"),
        ("species-notes", "Less Common Puffers"),
        ("identify", "Identify Your Puffer"),
    ],
    "body": TYPES_BODY,
    "faqs": [
        ("How many types of puffer fish are there?",
         "About 200 species are described in the family Tetraodontidae, spread across roughly 29 genera. Around 30 of them live in fresh or brackish water and the rest are marine. Only a dozen or so appear regularly in the aquarium trade."),
        ("What types of freshwater puffer fish are there?",
         "The true freshwater puffers kept in aquariums are the pea or dwarf puffer, red eye puffer, Amazon puffer, avocado puffer, congo puffer, hairy puffer, fahaka puffer and mbu puffer. Green spotted and figure 8 puffers are often sold as freshwater but are brackish."),
        ("What is the smallest puffer fish?",
         "The pea puffer, Carinotetraodon travancoricus, at 1 to 1.4 inches. It is also called the dwarf puffer or Indian dwarf puffer, and it is the only puffer suited to a 10 gallon tank."),
        ("What is the biggest puffer fish you can keep?",
         "The mbu puffer, Tetraodon mbu, reaching 24 to 30 inches. It needs 500 gallons or more, which in practice means a custom tank or an indoor pond. The fahaka puffer at 16 to 18 inches is the largest puffer most people can realistically house."),
        ("Is a porcupine puffer a real puffer fish?",
         "Not in the strict sense. Porcupine puffers belong to the family Diodontidae rather than Tetraodontidae, and they have two fused tooth plates rather than four. They inflate the same way and are kept the same way, so the trade groups them with puffers."),
        ("Which puffer fish is best for a beginner?",
         "The pea puffer. It stays tiny, lives in ordinary hard freshwater, and a trio is happy in a 10 gallon planted tank. Its only real demand is live and frozen food plus a supply of pest snails to grind its teeth."),
    ],
    "related": [
        ("/guides/puffer-fish-care/freshwater/", "Freshwater Puffer Fish"),
        ("/guides/puffer-fish-care/saltwater/", "Saltwater Puffer Fish"),
        ("/guides/puffer-fish-care/size-growth/", "Puffer Size & Growth"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# FRESHWATER PUFFERS
# ════════════════════════════════════════════════════════════════
FRESH_BODY = """    <p>A freshwater puffer is a puffer that completes its whole life cycle without added salt. That definition matters because most fish sold under the label are not freshwater at all &mdash; they are brackish juveniles that look healthy for six to twelve months in fresh water and then fade. Roughly eight species reach the hobby as genuine freshwater fish, and they range from a 1-inch pea puffer to a 30-inch mbu.</p>

    <h2 id="true-list">True Freshwater Puffer Fish</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Tank</th><th>Temp</th><th>pH</th></tr>
      <tr><td><a href="/guides/puffer-fish-care/pea-puffer/">Pea puffer</a></td><td>1&ndash;1.4 in</td><td>10 gal trio</td><td>74&ndash;82&deg;F</td><td>7.0&ndash;8.0</td></tr>
      <tr><td>Red eye puffer</td><td>2 in</td><td>15 gal</td><td>73&ndash;79&deg;F</td><td>6.0&ndash;7.5</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/amazon-puffer/">Amazon puffer</a></td><td>3&ndash;3.5 in</td><td>30 gal group</td><td>72&ndash;82&deg;F</td><td>6.5&ndash;7.5</td></tr>
      <tr><td>Avocado puffer</td><td>4&ndash;5 in</td><td>40 gal</td><td>75&ndash;82&deg;F</td><td>6.5&ndash;7.5</td></tr>
      <tr><td>Congo puffer</td><td>6 in</td><td>40 gal</td><td>75&ndash;82&deg;F</td><td>6.5&ndash;7.5</td></tr>
      <tr><td>Hairy puffer</td><td>6 in</td><td>55 gal</td><td>75&ndash;79&deg;F</td><td>6.5&ndash;7.5</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/fahaka-puffer/">Fahaka puffer</a></td><td>16&ndash;18 in</td><td>125 gal</td><td>75&ndash;82&deg;F</td><td>7.0&ndash;8.0</td></tr>
      <tr><td><a href="/guides/puffer-fish-care/mbu-puffer/">Mbu puffer</a></td><td>24&ndash;30 in</td><td>500+ gal</td><td>75&ndash;82&deg;F</td><td>7.0&ndash;8.0</td></tr>
    </table></div>

    <h2 id="mis-sold">The Fish Sold as Freshwater That Are Not</h2>
    <p>Three fish account for most of the confusion. All three are commonly kept in freshwater shop tanks and all three need salt:</p>
    <ul>
      <li><strong><a href="/guides/puffer-fish-care/green-spotted-puffer/">Green spotted puffer</a>.</strong> Juveniles genuinely start in near-fresh water in the wild, then move to increasingly saline estuary and coastal water. In a freshwater aquarium the adult develops bloating, poor colour and shortened life.</li>
      <li><strong><a href="/guides/puffer-fish-care/figure-8-puffer/">Figure 8 puffer</a>.</strong> Needs a permanent low brackish specific gravity around 1.005&ndash;1.008. It survives freshwater longer than a GSP, which is why the myth persists.</li>
      <li><strong>Ceylon and target puffers.</strong> Both are estuarine <em>Dichotomyctere</em> species with the same requirement.</li>
    </ul>
    <div class="callout"><strong>Test for yourself.</strong> If a shop cannot give you the scientific name, treat the fish as brackish until you have identified it against the <a href="/guides/puffer-fish-care/types/">species table</a>.</div>

    <h2 id="setup">Freshwater Puffer Tank Setup</h2>
    <p>The setup differs by feeding style more than by size. Sort your species into one of three groups:</p>
    <h3>Small hunters &mdash; pea, red eye</h3>
    <p>Heavily planted, dim, low flow, plenty of sight breaks. Java moss, anubias and floating plants let the fish set up small territories and stop the constant staring contests that turn into nipping. Sand or fine gravel. Sponge filter or a low-flow internal.</p>
    <h3>Open-water swimmers &mdash; Amazon, avocado</h3>
    <p>Length and current. Amazon puffers come from river channels and need a 36-inch-plus footprint, moderate to strong flow, and open swimming lanes with wood along the back. They shoal, so plan on five or more of them.</p>
    <h3>Ambush burrowers and giants &mdash; congo, hairy, fahaka, mbu</h3>
    <p>Deep soft sand for the burrowers &mdash; three to four inches so a congo puffer can bury completely &mdash; plus flat rock and heavy wood anchors. For fahaka and mbu the priority is footprint and filtration: these are messy predators eating whole shellfish, and they need sump-scale biological capacity plus 40&ndash;50% weekly water changes.</p>

    <h2 id="water">Freshwater Puffer Water Parameters</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Range</th><th>Target</th></tr>
      <tr><td>Temperature</td><td>73&ndash;82&deg;F (23&ndash;28&deg;C)</td><td>77&ndash;79&deg;F (25&ndash;26&deg;C)</td></tr>
      <tr><td>pH</td><td>6.5&ndash;8.0 by species</td><td>7.2&ndash;7.8 for most</td></tr>
      <tr><td>General hardness</td><td>5&ndash;20 dGH</td><td>8&ndash;15 dGH</td></tr>
      <tr><td>Ammonia / nitrite</td><td>0 ppm</td><td>0 ppm always</td></tr>
      <tr><td>Nitrate</td><td>Under 40 ppm</td><td>Under 20 ppm</td></tr>
      <tr><td>Water change</td><td>25&ndash;50% weekly</td><td>40&ndash;50% weekly</td></tr>
    </table></div>
    <p>Puffers are scaleless, so ammonia and nitrite burn them faster than scaled fish. Never add a puffer to a tank that is not fully cycled. Full detail on the <a href="/guides/puffer-fish-care/water-parameters/">water parameters page</a>, and you can score your own test results with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="feeding">Feeding Freshwater Puffers</h2>
    <p>Every freshwater puffer is a hard-food specialist. The practical staple list:</p>
    <ul>
      <li><strong>Pea and red eye puffers:</strong> bladder and ramshorn snails, live blackworms, frozen bloodworms, frozen brine shrimp, daphnia.</li>
      <li><strong>Amazon puffers:</strong> small snails, frozen bloodworms, mysis, chopped cockle. They grow teeth faster than any other species and need shells constantly.</li>
      <li><strong>Congo, hairy, avocado:</strong> whole frozen shrimp with the shell on, crayfish, earthworms, mussel, silversides for the larger individuals.</li>
      <li><strong>Fahaka and mbu:</strong> whole mussels and clams in shell, crayfish, unpeeled prawns, crab legs. Shell-on food is not optional at this size &mdash; the beak growth is rapid.</li>
    </ul>
    <p>Culture your own snails in a spare tank or a bucket on a windowsill; buying them gets expensive fast. See the <a href="/guides/puffer-fish-care/food/">feeding guide</a> and the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</p>

    <h2 id="mates">Are Freshwater Puffers Community Fish?</h2>
    <p>No. Some can be kept with carefully chosen company, but none is a community fish in the usual sense:</p>
    <ul>
      <li><strong>Pea puffer:</strong> species-only is safest. Otocinclus and fast bottom dwellers sometimes work in 20 gallons or more.</li>
      <li><strong>Amazon puffer:</strong> keep as a shoal of its own kind; fast mid-water dithers in a large tank only.</li>
      <li><strong>Congo, hairy, avocado, fahaka, mbu:</strong> single specimen. These fish kill tank mates, including much larger ones.</li>
    </ul>
    <p>Pairing-by-pairing verdicts are in the <a href="/compatibility/pea-puffer/">pea puffer compatibility hub</a> and the <a href="/guides/puffer-fish-care/tank-mates/">tank mates guide</a>.</p>
"""

FRESH = {
    "slug": "freshwater",
    "title": "Freshwater Puffer Fish: Species, Care and Tank Setup",
    "meta_desc": "Freshwater puffer fish care: the 8 true freshwater species, tank setup by feeding style, water parameters, diet and which shop puffers are actually brackish.",
    "h1": "Freshwater Puffer Fish Care",
    "hero_tag": "Freshwater Puffers",
    "hero_meta": "\U0001F4A7 8 true species &nbsp;|&nbsp; \U0001F5C3️ 10&ndash;500 gal &nbsp;|&nbsp; \U0001F321️ 73&ndash;82&deg;F &nbsp;|&nbsp; \U0001F9EA pH 6.5&ndash;8.0",
    "toc_sections": [
        ("true-list", "True Freshwater Species"),
        ("mis-sold", "Mis-sold as Freshwater"),
        ("setup", "Tank Setup"),
        ("water", "Water Parameters"),
        ("feeding", "Feeding"),
        ("mates", "Community Fish?"),
    ],
    "body": FRESH_BODY,
    "faqs": [
        ("Which puffer fish are truly freshwater?",
         "The pea or dwarf puffer, red eye puffer, Amazon puffer, avocado puffer, congo puffer, hairy puffer, fahaka puffer and mbu puffer are true freshwater species. Green spotted, figure 8, Ceylon and target puffers are brackish even though shops keep them in freshwater."),
        ("What is the best freshwater puffer fish for a beginner?",
         "The pea puffer. It reaches only 1 to 1.4 inches, needs no salt, and a trio lives well in a 10 gallon planted tank. Its main requirement is live or frozen food plus pest snails for its teeth."),
        ("What water parameters do freshwater puffers need?",
         "Most want 75 to 82F, pH 7.0 to 8.0 and 8 to 15 dGH, with ammonia and nitrite at zero and nitrate under 20 ppm. Red eye and Amazon puffers prefer slightly softer, more acidic water around pH 6.5 to 7.5."),
        ("Can freshwater puffer fish live with other fish?",
         "Rarely and never safely by default. Pea and Amazon puffers can sometimes share a large tank with fast, short-finned species, while congo, hairy, avocado, fahaka and mbu puffers must be kept alone. Assume every puffer is a fin-nipper until it proves otherwise."),
        ("Do freshwater puffer fish need salt?",
         "True freshwater species do not, and long-term salt exposure stresses them. Brackish species sold as freshwater do need it, which is why identifying the species before you buy matters more for puffers than for almost any other fish."),
        ("How big do freshwater puffer fish get?",
         "From 1.4 inches for a pea puffer to 30 inches for an mbu puffer. The commonly sold middle ground is 3 to 6 inches: Amazon puffers at 3.5 inches, avocado puffers at 4 to 5 inches, and congo and hairy puffers at 6 inches."),
    ],
    "related": [
        ("/guides/puffer-fish-care/types/", "Types of Puffer Fish"),
        ("/guides/puffer-fish-care/pea-puffer/", "Pea Puffer Care"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
    ],
}


# ════════════════════════════════════════════════════════════════
# SALTWATER PUFFERS
# ════════════════════════════════════════════════════════════════
SALT_BODY = """    <p>Marine puffers are the biggest personalities on most reef shop lists and the most consistently under-housed. The common trade species run from a 4-inch valentini toby that fits a 30-gallon tank to an <em>Arothron hispidus</em> that reaches 20 inches and needs 250 gallons. None of them is reef safe, and all of them share the scaleless skin that makes copper-based treatments risky.</p>

    <h2 id="species">Saltwater Puffer Species in the Trade</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Scientific name</th><th>Adult size</th><th>Minimum tank</th><th>Notes</th></tr>
      <tr><td>Valentini puffer / black-saddled toby</td><td><em>Canthigaster valentini</em></td><td>4 in</td><td>30 gal</td><td>Smallest common marine puffer</td></tr>
      <tr><td>Dogface puffer</td><td><em>Arothron nigropunctatus</em></td><td>12&ndash;13 in</td><td>180 gal</td><td>Most interactive; heavy waste load</td></tr>
      <tr><td>Porcupine puffer</td><td><em>Diodon holocanthus</em></td><td>12&ndash;14 in</td><td>125 gal</td><td>Family Diodontidae; erectile spines</td></tr>
      <tr><td>Spiny box / burrfish</td><td><em>Chilomycterus schoepfi</em></td><td>8&ndash;10 in</td><td>100 gal</td><td>Slow, deliberate, easily out-competed</td></tr>
      <tr><td>Stars and stripes puffer</td><td><em>Arothron hispidus</em></td><td>18&ndash;20 in</td><td>250 gal</td><td>Frequently sold far too small</td></tr>
      <tr><td>Blue spotted puffer</td><td><em>Arothron caeruleopunctatus</em></td><td>20 in</td><td>300 gal</td><td>Public-aquarium scale fish</td></tr>
    </table></div>

    <h2 id="water">Marine Puffer Water Parameters</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Range</th><th>Target</th></tr>
      <tr><td>Temperature</td><td>72&ndash;80&deg;F (22&ndash;27&deg;C)</td><td>76&ndash;78&deg;F</td></tr>
      <tr><td>Specific gravity</td><td>1.020&ndash;1.026</td><td>1.024&ndash;1.025</td></tr>
      <tr><td>pH</td><td>8.1&ndash;8.4</td><td>8.2&ndash;8.3</td></tr>
      <tr><td>Alkalinity</td><td>8&ndash;12 dKH</td><td>9&ndash;10 dKH</td></tr>
      <tr><td>Ammonia / nitrite</td><td>0 ppm</td><td>0 ppm always</td></tr>
      <tr><td>Nitrate</td><td>Under 20 ppm</td><td>Under 10 ppm</td></tr>
    </table></div>
    <p>Puffers eat shellfish whole and produce a nitrogen load closer to a large predator than to a typical reef stocking list. Plan on an oversized skimmer, a refugium or heavy mechanical export, and 20&ndash;30% water changes weekly.</p>

    <h2 id="reef">Are Saltwater Puffers Reef Safe?</h2>
    <p>No. Every commonly kept marine puffer will sample corals, clams, snails, hermit crabs, ornamental shrimp and feather dusters. The valentini toby is the worst offender relative to its size &mdash; it nips coral polyps and clam mantles almost constantly. A puffer belongs in a fish-only-with-live-rock (FOWLR) system.</p>
    <div class="callout callout-warn"><strong>Mimic warning.</strong> The mimic filefish (<em>Paraluteres prionurus</em>) is sold as a valentini puffer and looks nearly identical. Count the dorsal spine: the filefish has a single erectile spine above the eye that the toby lacks.</div>

    <h2 id="feeding">Feeding Marine Puffers</h2>
    <p>Same principle as freshwater: hard shells wear the beak. Rotate through:</p>
    <ul>
      <li><strong>Shell-on staples:</strong> whole clams and mussels, unpeeled shrimp, crab legs, snails, crayfish.</li>
      <li><strong>Soft supplements:</strong> silversides, squid, chopped scallop, mysis, krill, marine algae sheets for the tobies.</li>
      <li><strong>Frequency:</strong> daily for juveniles under 4 inches, every other day for adults. Adults over 10 inches often do best on three feeds a week.</li>
      <li><strong>Avoid freshwater feeder fish entirely</strong> &mdash; thiaminase and disease risk with no nutritional upside.</li>
    </ul>
    <p>Detail and portion guidance is on the <a href="/guides/puffer-fish-care/food/">puffer feeding page</a>, and the beak maintenance case is on the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</p>

    <h2 id="health">Health: Why Copper Is a Problem</h2>
    <p>Puffers and porcupinefish have no scales, so copper and formalin at standard marine doses cause visible skin damage, loss of appetite and sometimes death. Practical alternatives:</p>
    <ul>
      <li><strong>Marine ich and velvet:</strong> hyposalinity at SG 1.009 for four weeks, or chloroquine phosphate under careful dosing, in a bare quarantine tank.</li>
      <li><strong>Flukes:</strong> praziquantel, which puffers tolerate well.</li>
      <li><strong>Internal worms in wild-caught fish:</strong> a course of praziquantel plus metronidazole or levamisole during quarantine.</li>
      <li><strong>Freshwater dips:</strong> tolerated for 3&ndash;5 minutes by most marine puffers if the pH and temperature are matched.</li>
    </ul>
    <p>General puffer disease work-ups are on the <a href="/guides/puffer-fish-care/diseases/">diseases page</a>.</p>

    <h2 id="handling">Never Net a Puffer</h2>
    <p>A netted puffer gulps air and may not be able to expel it, which leads to a fish that floats and cannot right itself. Move puffers in a submerged container or a bag, always underwater. Symptoms and the fix are covered on the <a href="/guides/puffer-fish-care/puffing-up/">puffing up page</a>.</p>
"""

SALT = {
    "slug": "saltwater",
    "title": "Saltwater Puffer Fish Care: Species, Tank Size and Diet",
    "meta_desc": "Saltwater puffer fish care: porcupine, dogface and valentini puffers compared, marine water parameters, tank size, shell-on feeding and why copper is unsafe.",
    "h1": "Saltwater Puffer Fish Care",
    "hero_tag": "Saltwater Puffers",
    "hero_meta": "\U0001F30A FOWLR only &nbsp;|&nbsp; \U0001F5C3️ 30&ndash;300 gal &nbsp;|&nbsp; \U0001F9C2 SG 1.024&ndash;1.025 &nbsp;|&nbsp; ⚠️ No copper",
    "toc_sections": [
        ("species", "Species in the Trade"),
        ("water", "Water Parameters"),
        ("reef", "Reef Safe?"),
        ("feeding", "Feeding"),
        ("health", "Copper and Medication"),
        ("handling", "Never Net a Puffer"),
    ],
    "body": SALT_BODY,
    "faqs": [
        ("What tank size does a porcupine puffer need?",
         "125 gallons for Diodon holocanthus, which reaches 12 to 14 inches. Larger porcupinefish such as Diodon hystrix reach 20 inches and need 250 gallons or more. Filtration matters as much as volume because these fish eat whole shellfish."),
        ("Are saltwater puffer fish reef safe?",
         "No. Dogface, porcupine, stars and stripes and valentini puffers all nip corals, clams, snails, hermit crabs and ornamental shrimp. Keep marine puffers in a fish-only-with-live-rock system rather than a reef tank."),
        ("How big does a dogface puffer get?",
         "Arothron nigropunctatus reaches about 12 to 13 inches in captivity and needs a minimum of 180 gallons. It is one of the most interactive marine fish available but also one of the heaviest waste producers for its size."),
        ("Can you treat a saltwater puffer with copper?",
         "It is risky. Puffers are scaleless and copper at standard marine doses causes skin damage and appetite loss. Use hyposalinity at specific gravity 1.009, chloroquine phosphate or praziquantel in a quarantine tank instead, depending on the parasite."),
        ("How big does a valentini puffer get?",
         "Canthigaster valentini reaches about 4 inches and can be kept in 30 gallons, making it the smallest commonly available marine puffer. Watch for the mimic filefish, which is sold under the same name and has an erectile spine above the eye."),
        ("What do saltwater puffer fish eat?",
         "Shell-on foods: whole clams and mussels, unpeeled shrimp, crab legs, snails and crayfish, supplemented with silversides, squid, mysis and krill. Hard shells are essential because the fused beak grows continuously."),
    ],
    "related": [
        ("/guides/puffer-fish-care/types/", "Types of Puffer Fish"),
        ("/guides/puffer-fish-care/teeth/", "Puffer Teeth & Trimming"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TANK SIZE
# ════════════════════════════════════════════════════════════════
TANK_BODY = """    <p>There is no single puffer fish tank size, because the family spans a 1-inch pea puffer and a 30-inch mbu. What every puffer does share is a heavy waste load from a shellfish diet and near-zero tolerance for ammonia, so tank volume buys you biological headroom as much as swimming room. Size the tank for the adult fish and for the mess, not for the juvenile in the bag.</p>

    <h2 id="by-species">Puffer Fish Tank Size by Species</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Minimum tank</th><th>Comfortable tank</th><th>Footprint</th></tr>
      <tr><td>Pea puffer (single)</td><td>1&ndash;1.4 in</td><td>5 gal</td><td>10 gal</td><td>16&times;8 in</td></tr>
      <tr><td>Pea puffer (trio, 1M 2F)</td><td>1&ndash;1.4 in</td><td>10 gal</td><td>20 gal long</td><td>20&times;10 in</td></tr>
      <tr><td>Pea puffer (group of 6)</td><td>1&ndash;1.4 in</td><td>20 gal long</td><td>29 gal</td><td>30&times;12 in</td></tr>
      <tr><td>Red eye puffer</td><td>2 in</td><td>15 gal</td><td>20 gal</td><td>24&times;12 in</td></tr>
      <tr><td>Figure 8 puffer</td><td>3 in</td><td>15 gal</td><td>20&ndash;29 gal</td><td>24&times;12 in</td></tr>
      <tr><td>Amazon puffer (group of 5)</td><td>3&ndash;3.5 in</td><td>30 gal</td><td>40&ndash;55 gal</td><td>36&times;15 in</td></tr>
      <tr><td>Avocado puffer</td><td>4&ndash;5 in</td><td>40 gal</td><td>55 gal</td><td>36&times;15 in</td></tr>
      <tr><td>Green spotted puffer</td><td>6 in</td><td>30 gal</td><td>40&ndash;55 gal</td><td>36&times;15 in</td></tr>
      <tr><td>Congo puffer</td><td>6 in</td><td>40 gal</td><td>55 gal</td><td>36&times;18 in</td></tr>
      <tr><td>Hairy puffer</td><td>6 in</td><td>55 gal</td><td>75 gal</td><td>48&times;18 in</td></tr>
      <tr><td>Fahaka puffer</td><td>16&ndash;18 in</td><td>125 gal</td><td>180 gal</td><td>72&times;24 in</td></tr>
      <tr><td>Mbu puffer</td><td>24&ndash;30 in</td><td>500 gal</td><td>1000 gal / pond</td><td>10&times;4 ft</td></tr>
      <tr><td>Valentini puffer (marine)</td><td>4 in</td><td>30 gal</td><td>55 gal</td><td>36&times;15 in</td></tr>
      <tr><td>Porcupine puffer (marine)</td><td>12&ndash;14 in</td><td>125 gal</td><td>180 gal</td><td>72&times;18 in</td></tr>
      <tr><td>Dogface puffer (marine)</td><td>12&ndash;13 in</td><td>180 gal</td><td>240 gal</td><td>72&times;24 in</td></tr>
    </table></div>
    <p>Convert dimensions to gallons or litres with the <a href="/tools/tank-size-calculator/">tank size calculator</a>, or plan a whole build with the <a href="/tools/aquarium-planner/">aquarium planner</a>.</p>

    <h2 id="pea-tank">Pea Puffer Tank Size in Detail</h2>
    <p>The pea puffer is the one puffer where stocking arithmetic actually matters, because people keep them in groups. The working rules:</p>
    <ul>
      <li><strong>Five gallons for a single fish</strong> is the absolute floor and only works as a species-only tank with heavy planting.</li>
      <li><strong>Ten gallons for a trio</strong> &mdash; one male and two females. Two fish is the worst possible number, because one becomes a full-time target.</li>
      <li><strong>Add three to five gallons per additional puffer</strong>, and add plants and hardscape at the same time. Sight breaks do more for peace than volume does.</li>
      <li><strong>Length beats height.</strong> A 20-gallon long at 30&times;12 inches holds a much calmer group than a 20-gallon tall at 24&times;12.</li>
    </ul>
    <p>Full care detail on the <a href="/guides/puffer-fish-care/pea-puffer/">pea puffer page</a>.</p>

    <h2 id="filtration">Filtration and Water Changes</h2>
    <p>Target <strong>6&ndash;8 times tank volume per hour</strong> of real flow. Puffers eat messy, protein-heavy food and leave shell fragments and uneaten flesh behind, so mechanical export matters as much as biological capacity.</p>
    <ul>
      <li><strong>Small tanks (5&ndash;20 gal):</strong> a sponge filter plus a small internal, or a low-flow hang-on-back with the outflow baffled. Pea puffers are weak swimmers and hate being blown around.</li>
      <li><strong>Mid tanks (30&ndash;75 gal):</strong> a canister rated above your volume, plus a sponge for redundancy.</li>
      <li><strong>Large tanks (125 gal+):</strong> a sump. Fahaka and mbu puffers eat whole shellfish and a sump gives you the mechanical stages and the biomedia surface to handle it.</li>
      <li><strong>Water changes:</strong> 30&ndash;50% weekly on any puffer tank; 40&ndash;50% on the large predators. Keep nitrate under 20 ppm.</li>
    </ul>

    <h2 id="hardscape">Substrate, Plants and Hardscape</h2>
    <ul>
      <li><strong>Sand for burrowers.</strong> Congo puffers need three to four inches of soft sand to bury in; a shallow gravel bed leaves them stressed and permanently exposed.</li>
      <li><strong>Planting for small species.</strong> Pea and red eye puffers need dense cover: java moss, anubias, crypts, floating plants. Line of sight is what triggers puffer aggression, so break it up.</li>
      <li><strong>Open lanes for swimmers.</strong> Amazon and avocado puffers want the middle of the tank clear and structure along the back and sides.</li>
      <li><strong>Nothing sharp.</strong> Scaleless skin scrapes easily on lava rock and sharp slate.</li>
      <li><strong>A lid, always.</strong> Puffers follow food to the surface and startle easily.</li>
    </ul>

    <h2 id="mistakes">Tank Mistakes That Kill Puffers</h2>
    <ol>
      <li><strong>Buying the juvenile size.</strong> A 1-inch green spotted puffer in a 10-gallon tank is a 6-inch fish in a 10-gallon tank fifteen months later.</li>
      <li><strong>Uncycled tanks.</strong> Scaleless fish show ammonia damage within days. Cycle first, always.</li>
      <li><strong>Two pea puffers.</strong> Keep one, or keep three or more. Never two.</li>
      <li><strong>Freshwater for a brackish species.</strong> See the <a href="/guides/puffer-fish-care/water-parameters/">water parameters page</a> for salinity targets.</li>
      <li><strong>Under-filtering a predator tank.</strong> A filter rated for a community 55 is not rated for a fahaka in a 125.</li>
    </ol>
"""

TANK = {
    "slug": "tank-size",
    "title": "Puffer Fish Tank Size: Minimum Gallons by Species",
    "meta_desc": "Puffer fish tank size by species: 10 gallons for a pea puffer trio, 30 for a green spotted puffer, 125 for a fahaka. Filtration, footprint and setup guidance.",
    "h1": "Puffer Fish Tank Size and Setup",
    "hero_tag": "Tank Size & Setup",
    "hero_meta": "\U0001F5C3️ 5&ndash;500+ gal &nbsp;|&nbsp; ⚡ 6&ndash;8&times; turnover &nbsp;|&nbsp; \U0001F4A7 30&ndash;50% weekly &nbsp;|&nbsp; \U0001F9F1 Sand for burrowers",
    "toc_sections": [
        ("by-species", "Tank Size by Species"),
        ("pea-tank", "Pea Puffer Tank Size"),
        ("filtration", "Filtration & Water Changes"),
        ("hardscape", "Substrate & Hardscape"),
        ("mistakes", "Tank Mistakes"),
    ],
    "body": TANK_BODY,
    "faqs": [
        ("What size tank does a puffer fish need?",
         "It depends on the species. A single pea puffer needs 5 gallons and a trio needs 10, a figure 8 puffer needs 15 to 20, a green spotted puffer needs 30, a fahaka puffer needs 125 and an mbu puffer needs 500 gallons or more."),
        ("How many pea puffers can I keep in a 10 gallon tank?",
         "Three, ideally one male and two females, in a heavily planted 10 gallon. Never keep exactly two, because one fish becomes a permanent target. Add three to five gallons and more planting for each puffer beyond the trio."),
        ("Can a puffer fish live in a 5 gallon tank?",
         "Only a single pea puffer, and only in a heavily planted species-only tank with a sponge filter and weekly water changes. Every other puffer in the trade outgrows a 5 gallon within months."),
        ("How big a tank does a green spotted puffer need?",
         "30 gallons minimum for one adult, with 40 to 55 gallons preferred, and a 36 inch or longer footprint. The tank also has to be brackish, moving from about specific gravity 1.005 as a juvenile to 1.018 to 1.022 as an adult."),
        ("What filtration do puffer fish need?",
         "Aim for 6 to 8 times the tank volume per hour, weighted toward mechanical and biological media. Puffers eat shellfish and leave debris, so oversize the mechanical stage and do 30 to 50 percent water changes weekly to keep nitrate under 20 ppm."),
        ("Do puffer fish need sand or gravel?",
         "Sand for burrowing species such as the congo puffer, which needs three to four inches to bury in. Fine sand or smooth small gravel suits everything else. Avoid sharp substrate and hardscape, because puffers have no scales to protect their skin."),
    ],
    "related": [
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/puffer-fish-care/size-growth/", "Puffer Size & Growth"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# WATER PARAMETERS
# ════════════════════════════════════════════════════════════════
WATER_BODY = """    <p>Puffers have no scales. That single fact drives everything about their water: ammonia and nitrite burn them faster than scaled fish, medications absorb faster, and swings in salinity or temperature show up as visible skin and colour problems within days. Get the numbers below stable and most puffer health problems never start.</p>

    <h2 id="quick-table">Puffer Fish Water Parameters at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Freshwater puffers</th><th>Brackish puffers</th><th>Marine puffers</th></tr>
      <tr><td>Temperature</td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td><td>76&ndash;82&deg;F (24&ndash;28&deg;C)</td><td>72&ndash;80&deg;F (22&ndash;27&deg;C)</td></tr>
      <tr><td>pH</td><td>7.0&ndash;8.0</td><td>7.5&ndash;8.4</td><td>8.1&ndash;8.4</td></tr>
      <tr><td>Hardness (GH)</td><td>8&ndash;15 dGH</td><td>12&ndash;20 dGH</td><td>n/a</td></tr>
      <tr><td>Specific gravity</td><td>1.000</td><td>1.005&ndash;1.022 by species and age</td><td>1.024&ndash;1.025</td></tr>
      <tr><td>Ammonia / nitrite</td><td>0 ppm</td><td>0 ppm</td><td>0 ppm</td></tr>
      <tr><td>Nitrate</td><td>Under 20 ppm</td><td>Under 20 ppm</td><td>Under 10 ppm</td></tr>
      <tr><td>Water change</td><td>30&ndash;50% weekly</td><td>30&ndash;50% weekly</td><td>20&ndash;30% weekly</td></tr>
    </table></div>
    <p>Score your own test kit results against these ranges with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="temperature">Puffer Fish Water Temperature</h2>
    <p>Most freshwater and brackish puffers sit best at <strong>77&ndash;80&deg;F (25&ndash;27&deg;C)</strong>. The wider tolerated band is 74&ndash;82&deg;F. Two species want the cooler half of that range: the <strong>hairy puffer</strong> (75&ndash;79&deg;F) and the <strong>red eye puffer</strong> (73&ndash;79&deg;F), both from shaded, flowing habitats.</p>
    <ul>
      <li><strong>Below 74&deg;F</strong> the immune system slows. Chronically cool puffers are the ones that catch ich and stop eating for no visible reason.</li>
      <li><strong>Above 82&deg;F</strong> dissolved oxygen falls while metabolism rises. Sustained heat is a common reason for <a href="/guides/puffer-fish-care/swimming-problems/">a puffer gasping at the surface</a>.</li>
      <li><strong>Stability beats the ideal number.</strong> A steady 77&deg;F is healthier than a tank that swings between 75 and 82 chasing 79.</li>
    </ul>
    <p>Guard the heater or run it in a sump. Large puffers have cracked glass heaters, and a scaleless fish resting against a hot element burns.</p>

    <h2 id="ph">pH and Hardness</h2>
    <p>Most puffers want neutral to slightly alkaline, moderately hard water &mdash; <strong>pH 7.0&ndash;8.0 at 8&ndash;15 dGH</strong>. The exceptions are the softwater species:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>pH</th><th>GH</th></tr>
      <tr><td>Pea puffer</td><td>7.0&ndash;8.0</td><td>8&ndash;15 dGH</td></tr>
      <tr><td>Red eye puffer</td><td>6.0&ndash;7.5</td><td>4&ndash;12 dGH</td></tr>
      <tr><td>Amazon puffer</td><td>6.5&ndash;7.5</td><td>5&ndash;12 dGH</td></tr>
      <tr><td>Congo / hairy puffer</td><td>6.5&ndash;7.5</td><td>5&ndash;15 dGH</td></tr>
      <tr><td>Fahaka / mbu puffer</td><td>7.0&ndash;8.0</td><td>10&ndash;20 dGH</td></tr>
      <tr><td>Figure 8 / green spotted</td><td>7.5&ndash;8.4</td><td>12&ndash;20 dGH</td></tr>
    </table></div>
    <p>Chasing a decimal on the pH meter is counterproductive. A stable 7.6 out of the tap beats a swinging 7.2 maintained with buffers. Keep KH above 4 dKH so the pH does not crash between water changes.</p>

    <h2 id="salinity">Brackish Salinity: Getting It Right</h2>
    <p>This is where most puffer keeping goes wrong. Brackish puffers need <strong>marine salt mix</strong> &mdash; not aquarium salt, not tonic salt, not table salt &mdash; measured with a refractometer or a good glass hydrometer.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species / stage</th><th>Specific gravity</th><th>Rough salt per 10 gal</th></tr>
      <tr><td>Figure 8 puffer, all ages</td><td>1.005&ndash;1.008</td><td>2.5&ndash;4 oz</td></tr>
      <tr><td>Green spotted puffer, under 2 in</td><td>1.005&ndash;1.008</td><td>2.5&ndash;4 oz</td></tr>
      <tr><td>Green spotted puffer, 2&ndash;4 in</td><td>1.010&ndash;1.015</td><td>5&ndash;7.5 oz</td></tr>
      <tr><td>Green spotted puffer, adult</td><td>1.018&ndash;1.022</td><td>9&ndash;11 oz</td></tr>
      <tr><td>Ceylon / target puffer</td><td>1.005&ndash;1.015</td><td>2.5&ndash;7.5 oz</td></tr>
    </table></div>
    <div class="callout"><strong>Mix outside the tank.</strong> Dissolve marine salt fully in the change water, match temperature, then add. Never pour dry salt into an occupied tank. Raise salinity gradually &mdash; no more than about 0.002 SG per week &mdash; and remember that the biological filter has to re-adapt each time you change it.</div>

    <h2 id="cycling">Cycling and Nitrate Control</h2>
    <p>Never add a puffer to an uncycled tank. Because puffers are scaleless and eat protein-heavy food, they combine the highest sensitivity to ammonia with the highest ammonia production. Practical routine:</p>
    <ul>
      <li>Cycle to the point where 2 ppm ammonia processes to nitrate within 24 hours before the fish arrives.</li>
      <li>Test ammonia, nitrite and nitrate weekly for the first two months, then fortnightly.</li>
      <li>Remove uneaten shell and flesh within an hour of feeding &mdash; it is the biggest single nitrate source in a puffer tank.</li>
      <li>Hold nitrate under 20 ppm with 30&ndash;50% weekly changes. Chronic nitrate is a common cause of <a href="/guides/puffer-fish-care/color-change/">colour loss and darkening</a>.</li>
    </ul>
"""

WATER = {
    "slug": "water-parameters",
    "title": "Puffer Fish Water Parameters: Temperature, pH and Salinity",
    "meta_desc": "Puffer fish water parameters: temperature 75-82F, pH 7.0-8.0, hardness targets and brackish specific gravity charts for figure 8 and green spotted puffers.",
    "h1": "Puffer Fish Water Parameters and Temperature",
    "hero_tag": "Water & Temperature",
    "hero_meta": "\U0001F321️ 75&ndash;82&deg;F &nbsp;|&nbsp; \U0001F9EA pH 7.0&ndash;8.0 &nbsp;|&nbsp; \U0001F9C2 SG 1.000&ndash;1.022 &nbsp;|&nbsp; \U0001F4A7 NO3 under 20 ppm",
    "toc_sections": [
        ("quick-table", "Parameters at a Glance"),
        ("temperature", "Water Temperature"),
        ("ph", "pH and Hardness"),
        ("salinity", "Brackish Salinity"),
        ("cycling", "Cycling & Nitrate"),
    ],
    "body": WATER_BODY,
    "faqs": [
        ("What temperature do puffer fish need?",
         "Most freshwater and brackish puffers do best at 77 to 80F, within a tolerated range of 74 to 82F. Hairy puffers and red eye puffers prefer the cooler half at 73 to 79F. Marine puffers sit at 76 to 78F."),
        ("What pH do puffer fish need?",
         "Neutral to slightly alkaline for most species: pH 7.0 to 8.0 at 8 to 15 dGH. Red eye and Amazon puffers prefer softer, slightly acidic water at pH 6.5 to 7.5, and brackish species sit higher at 7.5 to 8.4."),
        ("What are the water parameters for a freshwater puffer?",
         "Temperature 75 to 82F, pH 7.0 to 8.0, general hardness 8 to 15 dGH, ammonia and nitrite at 0 ppm and nitrate under 20 ppm, with 30 to 50 percent weekly water changes. Specific gravity stays at 1.000 with no added salt."),
        ("How much salt does a brackish puffer need?",
         "A figure 8 puffer needs specific gravity 1.005 to 1.008 for life. A green spotted puffer starts at 1.005 to 1.008 as a juvenile and finishes at 1.018 to 1.022 as an adult. Use marine salt mix and a refractometer, never aquarium tonic salt."),
        ("Are puffer fish sensitive to ammonia?",
         "Very. Puffers have no scales, so ammonia and nitrite damage their skin and gills faster than scaled fish, and they produce a heavy waste load from a shellfish diet. Never add a puffer to an uncycled tank and keep both readings at zero."),
        ("Can puffer fish live in hard water?",
         "Most prefer it. Pea, fahaka, mbu and the brackish species all want moderately hard to hard water at 8 to 20 dGH. Only red eye and Amazon puffers prefer soft water, and even they tolerate moderate hardness if it is stable."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/aquarium-water-parameters/", "Aquarium Water Parameters"),
    ],
}


# ════════════════════════════════════════════════════════════════
# FOOD & FEEDING
# ════════════════════════════════════════════════════════════════
FOOD_BODY = """    <p>Puffers are durophagous &mdash; built to crush hard prey. In the wild that means snails, clams, crabs, crayfish and other shelled invertebrates, and their four fused tooth plates grow continuously to keep up with the wear. In an aquarium that translates into one hard rule: <strong>a puffer fed only soft food will eventually be unable to eat at all</strong>.</p>

    <h2 id="what-eat">What Do Puffer Fish Eat?</h2>
    <p>Build every puffer diet from two lists. The hard list keeps the beak in check; the soft list fills the fish out.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Hard-shelled foods (beak maintenance)</th><th>Soft foods (nutrition and variety)</th></tr>
      <tr><td>Bladder, ramshorn and Malaysian trumpet snails</td><td>Frozen bloodworms</td></tr>
      <tr><td>Small clams and cockles in shell</td><td>Live blackworms</td></tr>
      <tr><td>Whole mussels</td><td>Frozen brine shrimp and mysis</td></tr>
      <tr><td>Unpeeled shrimp and prawns</td><td>Krill</td></tr>
      <tr><td>Crayfish and crab legs (large species)</td><td>Chopped white fish and squid</td></tr>
      <tr><td>Nerite and pond snails</td><td>Earthworms (large species)</td></tr>
    </table></div>
    <div class="callout callout-warn"><strong>Never feed live feeder fish.</strong> Goldfish and rosy reds carry thiaminase, which destroys vitamin B1, plus a real parasite and disease load. They are behind a large share of unexplained long-term puffer decline.</div>

    <h2 id="by-species">What to Feed by Species</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Staple diet</th><th>Feeding frequency</th></tr>
      <tr><td>Pea / dwarf puffer</td><td>Small pest snails, live blackworms, frozen bloodworms, daphnia</td><td>Once or twice daily, small amounts</td></tr>
      <tr><td>Red eye puffer</td><td>Small snails, bloodworms, brine shrimp</td><td>Daily</td></tr>
      <tr><td>Figure 8 puffer</td><td>Snails, small clams, bloodworms, mysis</td><td>Daily to every other day</td></tr>
      <tr><td>Amazon puffer</td><td>Snails, chopped cockle, bloodworms, mysis</td><td>Daily &mdash; fastest tooth growth of any puffer</td></tr>
      <tr><td>Green spotted puffer</td><td>Snails, clams, mussel, unpeeled shrimp, krill</td><td>Every other day as an adult</td></tr>
      <tr><td>Congo / hairy puffer</td><td>Whole shrimp in shell, earthworms, mussel, crayfish</td><td>Every 2&ndash;3 days</td></tr>
      <tr><td>Fahaka / mbu puffer</td><td>Whole mussels and clams, crayfish, crab legs, unpeeled prawns</td><td>2&ndash;3 times a week as an adult</td></tr>
      <tr><td>Marine puffers</td><td>Clams, mussels, unpeeled shrimp, crab, squid, silversides</td><td>Daily as juveniles, every other day as adults</td></tr>
    </table></div>

    <h2 id="how-often">How Often to Feed a Puffer Fish</h2>
    <p>Frequency tracks size and metabolism, not appetite &mdash; a puffer always looks hungry.</p>
    <ul>
      <li><strong>Under 2 inches:</strong> once or twice a day. Small puffers have fast metabolisms and empty out quickly.</li>
      <li><strong>2&ndash;6 inches:</strong> once daily, or every other day for the slower predators.</li>
      <li><strong>Over 6 inches:</strong> two to three times a week. Large puffers gorge on a big meal and digest for days.</li>
      <li><strong>Portion size:</strong> as much as the fish clears in two to three minutes, or one shellfish-sized item for large species.</li>
    </ul>
    <p>Estimate portions across your whole stocking list with the <a href="/tools/fish-feeding-calculator/">fish feeding calculator</a>.</p>

    <h2 id="dry-food">Will Puffers Eat Pellets or Flakes?</h2>
    <p>Almost never, and it does not matter. A puffer's beak is built for crushing, not for picking flakes off the surface, and most individuals do not register dry food as prey. A few captive-bred puffers can be trained onto sinking carnivore pellets, but pellets do nothing for tooth wear, so hard-shelled food still has to be in the rotation.</p>
    <p>If your puffer refuses everything including live food, the problem is usually water quality, internal parasites or an overgrown beak, not fussiness. Work through the <a href="/guides/puffer-fish-care/not-eating/">puffer not eating</a> checklist.</p>

    <h2 id="snails">Culturing Snails for Puffers</h2>
    <p>Buying snails one bag at a time gets expensive. Set up a dedicated snail culture instead:</p>
    <ol>
      <li>Use a 5&ndash;10 gallon tank, a bucket, or a large storage tub with a sponge filter and a heater.</li>
      <li>Seed it with bladder or ramshorn snails from a fellow hobbyist or a plant order.</li>
      <li>Feed algae wafers, blanched courgette, spinach and leftover fish food.</li>
      <li>Keep hardness above 8 dGH and add a cuttlebone so shells stay strong &mdash; a soft shell is no use for tooth wear.</li>
      <li>Harvest the size class that suits your puffer: pinhead snails for pea puffers, dime-sized for a green spotted puffer.</li>
    </ol>
    <div class="callout callout-ok"><strong>Quarantine snails from unknown tanks.</strong> Snails carry flukes and other parasites. Culture your own, or hold bought snails in a separate container for two weeks before feeding.</div>

    <h2 id="mistakes">Feeding Mistakes</h2>
    <ol>
      <li><strong>All soft food, no shells.</strong> The single most common cause of an overgrown beak &mdash; see the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</li>
      <li><strong>Overfeeding large species.</strong> Adult fahaka and mbu puffers fed daily become obese and fatty-livered. Two or three meals a week is correct.</li>
      <li><strong>Leaving leftovers in.</strong> Uneaten mussel fouls a tank within hours. Remove shell and flesh with tongs after feeding.</li>
      <li><strong>Feeder fish.</strong> Thiaminase and disease, no upside.</li>
      <li><strong>Hand feeding large puffers.</strong> A fahaka bite goes through a fingernail. Use tongs.</li>
    </ol>
"""

FOOD = {
    "slug": "food",
    "title": "What Do Puffer Fish Eat? Food and Feeding Guide",
    "meta_desc": "What to feed puffer fish: snails, clams and shell-on foods that grind their teeth, plus feeding frequency by species, portion sizes and why pellets do not work.",
    "h1": "Puffer Fish Food and Feeding",
    "hero_tag": "Food & Feeding",
    "hero_meta": "\U0001F35A Snails &amp; shellfish &nbsp;|&nbsp; \U0001F6AB No pellets &nbsp;|&nbsp; \U0001F4C5 Daily to 3&times;/week &nbsp;|&nbsp; ⚠️ No feeder fish",
    "toc_sections": [
        ("what-eat", "What Do They Eat?"),
        ("by-species", "Diet by Species"),
        ("how-often", "How Often to Feed"),
        ("dry-food", "Pellets and Flakes"),
        ("snails", "Culturing Snails"),
        ("mistakes", "Feeding Mistakes"),
    ],
    "body": FOOD_BODY,
    "faqs": [
        ("What do puffer fish eat?",
         "Hard-shelled invertebrates: snails, small clams, cockles, mussels, unpeeled shrimp, crayfish and crab legs, supplemented with frozen bloodworms, blackworms, brine shrimp, mysis and krill. The hard foods are essential because a puffer's fused beak grows continuously."),
        ("What is the best food for a puffer fish?",
         "Pest snails such as bladder and ramshorn are the single best staple, because they provide both nutrition and the shell hardness that wears the beak down. Pair them with frozen bloodworms and mysis for variety, and clams or unpeeled shrimp for larger species."),
        ("How often should I feed my puffer fish?",
         "Puffers under 2 inches eat once or twice a day, 2 to 6 inch puffers eat daily or every other day, and puffers over 6 inches eat two or three times a week. Feed what the fish clears in two to three minutes."),
        ("Will puffer fish eat pellets or flakes?",
         "Most will not. Their beak is built for crushing shells rather than picking at floating food, and the few that accept sinking carnivore pellets still need hard-shelled prey to keep their teeth worn down."),
        ("Can I feed my puffer fish feeder goldfish?",
         "No. Feeder goldfish and rosy reds contain thiaminase, which destroys vitamin B1, and they carry parasites and disease. They are a common cause of slow, unexplained decline in captive puffers."),
        ("How do I grow snails for my puffer?",
         "Set up a spare tank, bucket or tub with a sponge filter and heater, seed it with bladder or ramshorn snails, and feed algae wafers, blanched courgette and leftover fish food. Keep hardness above 8 dGH and add a cuttlebone so the shells stay hard."),
        ("Why is my puffer fish always hungry?",
         "Puffers beg constantly and will eat well past a sensible portion, especially the large species. Feed to a schedule rather than to the fish's behaviour, and watch for a rounded, sagging belly as the sign that you are overfeeding."),
    ],
    "related": [
        ("/guides/puffer-fish-care/teeth/", "Puffer Teeth & Trimming"),
        ("/tools/fish-feeding-calculator/", "Fish Feeding Calculator"),
        ("/guides/puffer-fish-care/not-eating/", "Puffer Not Eating"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TEETH
# ════════════════════════════════════════════════════════════════
TEETH_BODY = """    <p>The family name Tetraodontidae means &ldquo;four teeth&rdquo;. A puffer's jaw carries four fused tooth plates &mdash; two upper, two lower &mdash; forming a beak strong enough to crack a clam. Those plates grow continuously throughout the fish's life, and in an aquarium the only thing that stops them overgrowing is hard food. Overgrown teeth are the leading avoidable cause of death in captive puffers.</p>

    <h2 id="anatomy">How Puffer Teeth Work</h2>
    <p>Each plate is a fused row of teeth that keeps adding material at the base while the crushing edge wears away at the tip. In the wild the fish eats molluscs and crustaceans daily and the two rates cancel out. On a diet of bloodworms and pellets, growth continues and wear stops, so the beak lengthens until the fish physically cannot open its mouth wide enough to take food.</p>
    <p>Growth rate varies by species. <strong>Amazon puffers</strong> (<em>Colomesus asellus</em>) grow teeth faster than any other commonly kept puffer and often need trimming even on a good diet. <strong>Pea puffers</strong> rarely need it if they get snails. Large species such as fahaka and mbu need constant shell-on food but generally keep their own beaks in shape when fed correctly.</p>

    <h2 id="prevention">Preventing Overgrown Teeth</h2>
    <ul>
      <li><strong>Feed shelled prey at least three times a week.</strong> Snails for small puffers; clams, mussels, unpeeled shrimp, crayfish and crab legs for large ones.</li>
      <li><strong>Match the shell to the fish.</strong> Pinhead snails for pea puffers, dime-sized for a green spotted puffer. A shell too hard to crack teaches the fish to ignore it; one too soft does no grinding.</li>
      <li><strong>Keep hardness up in your snail culture.</strong> Snails grown in soft water have thin shells that do nothing for tooth wear.</li>
      <li><strong>Do not peel the shrimp.</strong> The exoskeleton is the working part of the meal.</li>
    </ul>
    <p>Full diet planning is on the <a href="/guides/puffer-fish-care/food/">puffer feeding page</a>.</p>

    <h2 id="signs">Signs of Overgrown Teeth</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Sign</th><th>What it means</th></tr>
      <tr><td>Visible white beak protruding past the lips</td><td>Overgrowth is already advanced</td></tr>
      <tr><td>Chasing food but failing to take it</td><td>The mouth cannot open far enough</td></tr>
      <tr><td>Taking food then spitting it out</td><td>The fish cannot crush or manipulate the item</td></tr>
      <tr><td>Weight loss with a sunken belly while still interested in food</td><td>Classic overgrowth starvation</td></tr>
      <tr><td>Preferring only the smallest, softest items</td><td>Early stage &mdash; correct the diet now</td></tr>
    </table></div>
    <p>A puffer that is uninterested in food is a different problem &mdash; see <a href="/guides/puffer-fish-care/not-eating/">puffer not eating</a>.</p>

    <h2 id="trimming">How Puffer Fish Teeth Trimming Works</h2>
    <div class="callout callout-warn"><strong>This is a veterinary-grade procedure.</strong> It involves sedating a fish and cutting bone-hard tissue millimetres from its jaw. If you have never done it, find an aquatic vet or an experienced keeper for the first one. The description below is what the procedure involves, not an instruction to attempt it unprepared.</div>
    <ol>
      <li><strong>Prepare a sedation bath.</strong> Clove oil is the standard: roughly 1&ndash;2 drops per litre, emulsified in a jar of warm tank water first, then added slowly to a container of tank water. Have a clean recovery container of untreated, aerated tank water ready.</li>
      <li><strong>Sedate to stage three.</strong> The fish loses equilibrium and stops responding to touch but gill movement continues. Overdosing is the main risk &mdash; add the emulsion in stages and stop as soon as the fish is under.</li>
      <li><strong>Support the fish in wet hands or on a wet cloth.</strong> Keep it wet throughout. Total handling time should be under two minutes.</li>
      <li><strong>Trim the plates.</strong> Cuticle clippers or small bone rongeurs for the tips, then a fine emery board or nail file to smooth them. Take only the overgrown portion &mdash; cutting into living tissue causes bleeding and lasting damage.</li>
      <li><strong>Recover.</strong> Move the fish to the aerated recovery container and gently move water over the gills until it swims on its own, usually one to five minutes.</li>
      <li><strong>Feed soft food for 48 hours</strong>, then reintroduce shelled prey to keep the problem from returning.</li>
    </ol>

    <h2 id="frequency">How Often Do Puffers Need Their Teeth Trimmed?</h2>
    <p>On a correct diet, most puffers never need it. When it is needed the usual pattern is:</p>
    <ul>
      <li><strong>Amazon puffer:</strong> every 4&ndash;8 months even on good food, purely because of growth rate.</li>
      <li><strong>Figure 8 and green spotted puffers:</strong> once every year or two if the diet slipped.</li>
      <li><strong>Pea puffers:</strong> almost never &mdash; they are also small enough that trimming is high risk.</li>
      <li><strong>Fahaka and mbu:</strong> rarely, but the consequences of overgrowth are severe because the fish is too large to sedate casually.</li>
    </ul>

    <h2 id="alternatives">Alternatives to Cutting</h2>
    <p>If the overgrowth is caught early, diet alone often corrects it. Offer harder food than the fish currently manages: crack a snail shell partly so the puffer gets purchase, or wedge a small clam so it has to work at it. Some keepers use a piece of cuttlebone or a coral fragment the fish can gnaw. This only works before the fish stops being able to open its mouth &mdash; once feeding has stopped, trimming is the only route.</p>
"""

TEETH = {
    "slug": "teeth",
    "title": "Puffer Fish Teeth: Overgrowth, Diet and Trimming",
    "meta_desc": "Why puffer fish teeth never stop growing, how to prevent overgrowth with snails and shell-on food, warning signs, and how puffer teeth trimming is done safely.",
    "h1": "Puffer Fish Teeth and Teeth Trimming",
    "hero_tag": "Teeth & Trimming",
    "hero_meta": "\U0001F9B7 4 fused plates &nbsp;|&nbsp; \U0001F41A Shells prevent overgrowth &nbsp;|&nbsp; ✂️ Clove oil sedation",
    "toc_sections": [
        ("anatomy", "How Puffer Teeth Work"),
        ("prevention", "Preventing Overgrowth"),
        ("signs", "Signs of Overgrowth"),
        ("trimming", "How Trimming Works"),
        ("frequency", "How Often"),
        ("alternatives", "Alternatives to Cutting"),
    ],
    "body": TEETH_BODY,
    "faqs": [
        ("Do puffer fish teeth keep growing?",
         "Yes. A puffer has four fused tooth plates that add material continuously throughout its life. In the wild, crushing snails and shellfish wears them down at the same rate. On a soft diet, growth continues unchecked and the beak eventually stops the fish from feeding."),
        ("How do I stop my puffer's teeth from overgrowing?",
         "Feed hard-shelled prey at least three times a week: pest snails for small puffers, clams, mussels, unpeeled shrimp, crayfish and crab legs for large ones. Match the shell hardness to the fish, and never peel shrimp before feeding."),
        ("How do you trim a puffer fish's teeth?",
         "The fish is sedated in a clove oil bath until it loses equilibrium but keeps breathing, held in wet hands for under two minutes while the overgrown tips are clipped with cuticle clippers and smoothed with an emery board, then revived in aerated tank water. It is best done by an aquatic vet or an experienced keeper."),
        ("How do I know if my puffer's teeth are too long?",
         "Look for a white beak protruding past the lips, a fish that chases food but cannot take it, food taken and spat out, or weight loss and a sunken belly while the fish still shows interest in feeding."),
        ("Which puffer fish need their teeth trimmed most often?",
         "Amazon puffers, Colomesus asellus, grow teeth faster than any other commonly kept species and often need trimming every four to eight months even on a good diet. Most other puffers never need it if they are fed shelled prey."),
        ("Why does a puffer fish have four teeth?",
         "The family name Tetraodontidae literally means four teeth. Each jaw carries two fused tooth plates, giving a four-part beak strong enough to crack snail and clam shells. Porcupinefish, a related family, have two plates instead."),
    ],
    "related": [
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/not-eating/", "Puffer Not Eating"),
        ("/guides/puffer-fish-care/amazon-puffer/", "Amazon Puffer Care"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# SIZE & GROWTH
# ════════════════════════════════════════════════════════════════
SIZE_BODY = """    <p>&ldquo;How big do puffer fish get?&rdquo; has no single answer &mdash; the family runs from a fish that fits on a fingernail to one longer than your forearm. What matters is that shops sell nearly all of them at the same 1&ndash;2 inch juvenile size, so the fish in the bag tells you almost nothing about the tank you will need in two years.</p>

    <h2 id="size-table">How Big Do Puffer Fish Get?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Adult size</th><th>Sold at</th><th>Time to adult size</th></tr>
      <tr><td>Pea / dwarf puffer</td><td>1&ndash;1.4 in (2.5&ndash;3.5 cm)</td><td>0.5 in</td><td>8&ndash;12 months</td></tr>
      <tr><td>Red eye puffer</td><td>2 in (5 cm)</td><td>0.75 in</td><td>10&ndash;14 months</td></tr>
      <tr><td>Figure 8 puffer</td><td>3 in (8 cm)</td><td>1 in</td><td>18&ndash;24 months</td></tr>
      <tr><td>Amazon puffer</td><td>3&ndash;3.5 in (8&ndash;9 cm)</td><td>1 in</td><td>12&ndash;18 months</td></tr>
      <tr><td>Avocado puffer</td><td>4&ndash;5 in (10&ndash;13 cm)</td><td>1.5 in</td><td>18&ndash;24 months</td></tr>
      <tr><td>Green spotted puffer</td><td>6 in (15 cm)</td><td>1 in</td><td>2&ndash;3 years</td></tr>
      <tr><td>Congo puffer</td><td>6 in (15 cm)</td><td>2 in</td><td>2 years</td></tr>
      <tr><td>Hairy puffer</td><td>6 in (15 cm)</td><td>2&ndash;3 in</td><td>2&ndash;3 years</td></tr>
      <tr><td>Fahaka puffer</td><td>16&ndash;18 in (40&ndash;45 cm)</td><td>2 in</td><td>3&ndash;4 years</td></tr>
      <tr><td>Mbu puffer</td><td>24&ndash;30 in (60&ndash;75 cm)</td><td>2&ndash;3 in</td><td>5&ndash;7 years</td></tr>
      <tr><td>Valentini puffer</td><td>4 in (11 cm)</td><td>1.5 in</td><td>18 months</td></tr>
      <tr><td>Porcupine puffer</td><td>12&ndash;14 in (30&ndash;35 cm)</td><td>3 in</td><td>3&ndash;4 years</td></tr>
      <tr><td>Dogface puffer</td><td>12&ndash;13 in (30&ndash;33 cm)</td><td>3 in</td><td>3&ndash;4 years</td></tr>
    </table></div>

    <h2 id="growth-rate">Puffer Fish Growth Rate</h2>
    <p>Puffers grow fastest in their first year and then slow markedly. Typical patterns:</p>
    <ul>
      <li><strong>Pea puffers</strong> reach full size within a year and are effectively adult at eight months.</li>
      <li><strong>Green spotted puffers</strong> add roughly an inch every four to six months for the first two years, then slow to a crawl.</li>
      <li><strong>Fahaka puffers</strong> commonly add 4&ndash;6 inches in their first year on a heavy diet, which is why keepers who buy a 2-inch fish find themselves needing a 125-gallon tank inside eighteen months.</li>
      <li><strong>Mbu puffers</strong> are slower but relentless: an inch every month or two through the juvenile phase and steady growth for five to seven years.</li>
    </ul>
    <div class="callout"><strong>Growth is driven by food and water volume.</strong> A well-fed puffer in clean, spacious water grows near the top of these ranges. That is what you want &mdash; slow growth in this family usually means a problem, not a smaller adult.</div>

    <h2 id="stunting">Does a Small Tank Keep a Puffer Small?</h2>
    <p>No, and the belief kills fish. A puffer in an undersized tank does slow its external growth, but its internal organs continue developing at close to the normal rate. The result is spinal deformity, organ compression, a compromised immune system and a fish that dies years early. A fahaka kept in a 55-gallon tank does not become a 55-gallon fish &mdash; it becomes a sick 12-inch fish in a tank it cannot turn around in.</p>
    <p>Buy the tank for the adult size in the table above. Tank guidance by species is on the <a href="/guides/puffer-fish-care/tank-size/">puffer tank size page</a>.</p>

    <h2 id="measure">How to Measure and Track a Puffer</h2>
    <ul>
      <li>Measure standard length &mdash; snout to the base of the tail &mdash; not total length including the caudal fin. Most published sizes are standard length.</li>
      <li>Photograph the fish against the same tank background every month; a side-by-side after six months shows growth that day-to-day observation misses.</li>
      <li>Track the tank at the same time: work out the volume you actually have with the <a href="/tools/tank-size-calculator/">tank size calculator</a> and compare it to what the adult will need.</li>
    </ul>

    <h2 id="slow">Why Is My Puffer Not Growing?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>What to check</th></tr>
      <tr><td>Underfeeding</td><td>Juveniles need daily food; a growing puffer eats a lot</td></tr>
      <tr><td>Poor diet</td><td>Bloodworms alone are not enough &mdash; see the <a href="/guides/puffer-fish-care/food/">feeding guide</a></td></tr>
      <tr><td>Internal parasites</td><td>Wild-caught fish, thin body, white stringy faeces</td></tr>
      <tr><td>Chronic nitrate</td><td>Test; hold under 20 ppm with weekly changes</td></tr>
      <tr><td>Overgrown teeth</td><td>Fish interested in food but unable to eat &mdash; see the <a href="/guides/puffer-fish-care/teeth/">teeth page</a></td></tr>
      <tr><td>Wrong salinity</td><td>Brackish species in freshwater stall and decline</td></tr>
    </table></div>
"""

SIZE = {
    "slug": "size-growth",
    "title": "How Big Do Puffer Fish Get? Size and Growth Rate",
    "meta_desc": "Puffer fish size by species, from the 1.4-inch pea puffer to the 30-inch mbu, with growth rates and why a small tank never keeps a puffer small.",
    "h1": "Puffer Fish Size and Growth Rate",
    "hero_tag": "Size & Growth",
    "hero_meta": "\U0001F4CF 1.4 in &rarr; 30 in &nbsp;|&nbsp; \U0001F4C8 Fastest in year one &nbsp;|&nbsp; ⚠️ Stunting is not size control",
    "toc_sections": [
        ("size-table", "How Big They Get"),
        ("growth-rate", "Growth Rate"),
        ("stunting", "Does a Small Tank Stunt?"),
        ("measure", "Measuring Growth"),
        ("slow", "Why Is Mine Not Growing?"),
    ],
    "body": SIZE_BODY,
    "faqs": [
        ("How big do puffer fish get?",
         "Between 1.4 inches and 30 inches depending on species. Pea puffers reach 1 to 1.4 inches, figure 8 puffers 3 inches, green spotted puffers 6 inches, fahaka puffers 16 to 18 inches and mbu puffers 24 to 30 inches."),
        ("How fast do puffer fish grow?",
         "Fastest in the first year, then slowing sharply. Pea puffers are full size in 8 to 12 months, green spotted puffers add about an inch every four to six months for two years, and fahaka puffers commonly add 4 to 6 inches in their first year."),
        ("Will a puffer fish stay small in a small tank?",
         "No. Confining a puffer slows its external growth while its organs keep developing, which causes spinal deformity, organ damage and a shortened life. Buy the tank for the species' adult size instead."),
        ("How big does a green spotted puffer get?",
         "About 6 inches, reached over two to three years. They are usually sold at around an inch, which is why so many end up in tanks that are far too small and too fresh for an adult."),
        ("How big does a fahaka puffer get?",
         "16 to 18 inches, and it gets most of the way there in three to four years. A fahaka needs a 125 gallon tank with a 72 by 24 inch footprint, and it must be housed alone."),
        ("Why is my puffer fish not growing?",
         "The usual causes are underfeeding, a diet of soft food only, internal parasites in a wild-caught fish, chronic nitrate above 20 ppm, overgrown teeth preventing feeding, or a brackish species being kept in freshwater."),
    ],
    "related": [
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
        ("/guides/puffer-fish-care/lifespan/", "Puffer Lifespan"),
        ("/guides/puffer-fish-care/types/", "Types of Puffer Fish"),
        ("/tools/tank-size-calculator/", "Tank Size Calculator"),
    ],
}


# ════════════════════════════════════════════════════════════════
# LIFESPAN
# ════════════════════════════════════════════════════════════════
LIFE_BODY = """    <p>Puffers are long-lived for their size. A pea puffer that fits in a 10-gallon tank outlives most tetras, and a fahaka or mbu is a fifteen-to-twenty-year commitment &mdash; longer than many dogs. Most captive puffers die well short of those numbers, and almost always for the same handful of reasons.</p>

    <h2 id="table">How Long Do Puffer Fish Live?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Typical captive lifespan</th><th>Well-kept</th></tr>
      <tr><td>Pea / dwarf puffer</td><td>3&ndash;4 years</td><td>5 years</td></tr>
      <tr><td>Red eye puffer</td><td>4&ndash;6 years</td><td>8 years</td></tr>
      <tr><td>Figure 8 puffer</td><td>8&ndash;10 years</td><td>15 years</td></tr>
      <tr><td>Amazon puffer</td><td>6&ndash;8 years</td><td>10 years</td></tr>
      <tr><td>Avocado puffer</td><td>6&ndash;8 years</td><td>10 years</td></tr>
      <tr><td>Green spotted puffer</td><td>8&ndash;10 years</td><td>15 years</td></tr>
      <tr><td>Congo puffer</td><td>6&ndash;8 years</td><td>10 years</td></tr>
      <tr><td>Hairy puffer</td><td>8&ndash;10 years</td><td>12 years</td></tr>
      <tr><td>Fahaka puffer</td><td>10 years</td><td>15 years</td></tr>
      <tr><td>Mbu puffer</td><td>10&ndash;15 years</td><td>20+ years</td></tr>
      <tr><td>Porcupine puffer</td><td>10 years</td><td>15 years</td></tr>
      <tr><td>Dogface puffer</td><td>10 years</td><td>15 years</td></tr>
    </table></div>
    <p>Note the gap between the two columns. It is almost entirely down to husbandry, and it is bigger in puffers than in most families because their two commonest killers &mdash; wrong salinity and overgrown teeth &mdash; are both slow, silent and completely preventable.</p>

    <h2 id="shortens">What Shortens a Puffer's Life</h2>
    <ol>
      <li><strong>Brackish species kept in freshwater.</strong> A green spotted puffer in fresh water typically lives three to five years instead of ten to fifteen. This is the single largest cause of premature puffer death in the hobby &mdash; see the <a href="/guides/puffer-fish-care/water-parameters/">salinity guide</a>.</li>
      <li><strong>Soft-food diets and overgrown teeth.</strong> The fish starves slowly while still appearing interested in food. See the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</li>
      <li><strong>Undersized tanks.</strong> Chronic nitrate and no room to move; organ damage accumulates for years before it shows.</li>
      <li><strong>Untreated internal parasites.</strong> Most large puffers are wild-caught and arrive with worms. Quarantine and deworm on arrival.</li>
      <li><strong>Feeder fish.</strong> Thiaminase-driven vitamin B1 deficiency causes neurological decline over months.</li>
      <li><strong>Full-strength medication.</strong> A scaleless fish dosed like a scaled one can be killed by the treatment.</li>
    </ol>

    <h2 id="longer">How to Help a Puffer Live Longer</h2>
    <ul>
      <li><strong>Confirm the species and its water type before you buy.</strong> Everything else follows from getting this right.</li>
      <li><strong>Oversize the tank and the filter</strong>, then hold nitrate under 20 ppm with 30&ndash;50% weekly water changes.</li>
      <li><strong>Feed shelled prey at least three times a week</strong> and rotate soft foods for nutrition.</li>
      <li><strong>Quarantine every new puffer for four weeks</strong>, with a praziquantel and metronidazole course for wild-caught fish.</li>
      <li><strong>Halve medication doses</strong> unless the product is labelled safe for scaleless fish.</li>
      <li><strong>Keep the tank calm.</strong> Chronic stress from aggressive tank mates shortens life measurably &mdash; see the <a href="/guides/puffer-fish-care/tank-mates/">tank mates guide</a>.</li>
    </ul>

    <h2 id="aging">Signs of an Aging Puffer</h2>
    <p>Old puffers slow down in recognisable ways: colours mute, the fish spends more time resting on the substrate or wedged in a favourite spot, appetite falls to two or three feeds a week, and the eyes lose some clarity. None of this needs treating on its own. Distinguish it from illness by the timeline &mdash; ageing takes months, illness takes days. Sudden changes are covered on the <a href="/guides/puffer-fish-care/diseases/">diseases page</a> and the <a href="/guides/puffer-fish-care/color-change/">colour change page</a>.</p>
"""

LIFESPAN = {
    "slug": "lifespan",
    "title": "Puffer Fish Lifespan: How Long Do Puffer Fish Live?",
    "meta_desc": "Puffer fish lifespan by species: 4-5 years for a pea puffer, 10-15 for figure 8 and green spotted puffers, 20+ for an mbu, and what shortens it.",
    "h1": "Puffer Fish Lifespan",
    "hero_tag": "Lifespan",
    "hero_meta": "⏳ 3&ndash;20+ years &nbsp;|&nbsp; \U0001F7E2 Pea puffer 4&ndash;5 &nbsp;|&nbsp; \U0001F40B Mbu 20+ &nbsp;|&nbsp; \U0001F9C2 Salinity is the biggest factor",
    "toc_sections": [
        ("table", "Lifespan by Species"),
        ("shortens", "What Shortens It"),
        ("longer", "Living Longer"),
        ("aging", "Signs of Ageing"),
    ],
    "body": LIFE_BODY,
    "faqs": [
        ("How long do puffer fish live?",
         "Between three and twenty years depending on species. Pea puffers live 4 to 5 years, Amazon and congo puffers 8 to 10, figure 8 and green spotted puffers 10 to 15, and mbu puffers 20 years or more in a large, well-maintained tank."),
        ("How long do pea puffers live?",
         "Four to five years in a well-kept tank, with three to four being typical. They need clean, stable water, a varied live and frozen diet, and enough space and planting to avoid constant territorial stress."),
        ("How long do green spotted puffers live?",
         "Ten to fifteen years when kept in the brackish and then near-marine salinity they need. Kept permanently in freshwater, the same fish usually dies at three to five years, which is why so many owners believe they are short-lived fish."),
        ("Why did my puffer fish die suddenly?",
         "The most common causes are ammonia or nitrite in an under-cycled tank, full-strength medication on a scaleless fish, a brackish species kept in freshwater, untreated internal parasites, or a swallowed air gulp after being netted."),
        ("Do puffer fish live longer in bigger tanks?",
         "Yes, indirectly. A larger volume dilutes the heavy waste load of a shellfish diet, keeps nitrate low and reduces territorial stress. Undersized tanks cause chronic nitrate exposure and organ damage that shortens life by years."),
        ("What is the longest living aquarium puffer?",
         "The mbu puffer, Tetraodon mbu, at 20 years or more, followed by figure 8, green spotted, fahaka, porcupine and dogface puffers at 10 to 15 years. All of them need the correct water type and shelled food to reach those numbers."),
    ],
    "related": [
        ("/guides/puffer-fish-care/size-growth/", "Puffer Size & Growth"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PEA / DWARF PUFFER
# ════════════════════════════════════════════════════════════════
PEA_BODY = """    <p>The pea puffer (<em>Carinotetraodon travancoricus</em>) is the smallest puffer in the world and the only one most aquarists should start with. It is also sold as the dwarf puffer, Indian dwarf puffer, pygmy puffer or bumblebee puffer &mdash; all the same fish, endemic to the rivers and backwaters of Kerala and Karnataka in south-west India. At 1 to 1.4 inches it fits a 10-gallon tank, it needs no salt, and it has more visible personality per cubic inch than anything else in freshwater.</p>

    <h2 id="quick">Pea Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Carinotetraodon travancoricus</em></td></tr>
      <tr><td>Adult size</td><td>1&ndash;1.4 in (2.5&ndash;3.5 cm)</td></tr>
      <tr><td>Lifespan</td><td>4&ndash;5 years</td></tr>
      <tr><td>Minimum tank</td><td>5 gal single; 10 gal for a trio</td></tr>
      <tr><td>Water type</td><td>True freshwater &mdash; no salt</td></tr>
      <tr><td>Temperature</td><td>74&ndash;82&deg;F (23&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>7.0&ndash;8.0</td></tr>
      <tr><td>Hardness</td><td>8&ndash;15 dGH</td></tr>
      <tr><td>Diet</td><td>Live and frozen only &mdash; snails, blackworms, bloodworms</td></tr>
      <tr><td>Temperament</td><td>Territorial, curious, fin-nipper</td></tr>
      <tr><td>Difficulty</td><td>Intermediate &mdash; easy water, demanding food</td></tr>
    </table></div>

    <h2 id="tank">Pea Puffer Tank Size and Setup</h2>
    <p>Five gallons holds one pea puffer. <strong>Ten gallons is the practical minimum for a group</strong>, and a group means three or more &mdash; one male and two females is the classic ratio. Never keep exactly two: the subordinate fish becomes a full-time target with nowhere to go.</p>
    <ul>
      <li><strong>Add 3&ndash;5 gallons per extra puffer</strong>, and add planting at the same time.</li>
      <li><strong>Plant heavily.</strong> Java moss, anubias, crypts, hornwort and floating plants. Line of sight is what triggers pea puffer aggression, so the goal is a tank where no fish can see the whole tank at once.</li>
      <li><strong>Low flow.</strong> Pea puffers hover rather than swim and get pushed around by a strong filter. A sponge filter or a baffled internal is ideal.</li>
      <li><strong>Sand or fine gravel</strong>, driftwood, leaf litter and caves.</li>
      <li><strong>Lid required.</strong> They are small, curious and jump when startled.</li>
    </ul>
    <p>Work out your exact volume with the <a href="/tools/tank-size-calculator/">tank size calculator</a>.</p>

    <h2 id="water">Pea Puffer Water Parameters</h2>
    <p>Pea puffers want ordinary hard tap water: <strong>74&ndash;82&deg;F (23&ndash;28&deg;C), pH 7.0&ndash;8.0, 8&ndash;15 dGH</strong>. Target 77&ndash;79&deg;F. They are scaleless, so ammonia and nitrite must read zero and nitrate should stay under 20 ppm. A 10-gallon pea puffer tank needs 30&ndash;50% weekly water changes because the diet is entirely protein.</p>
    <div class="callout callout-warn"><strong>Never add salt.</strong> Pea puffers are true freshwater fish. The salt advice that circulates for green spotted and figure 8 puffers does not apply and stresses them.</div>
    <p>Check your readings with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="food">Pea Puffer Food and Feeding</h2>
    <p>This is the demanding part. <strong>Pea puffers do not eat flake or pellet food.</strong> Plan the food supply before you buy the fish.</p>
    <ul>
      <li><strong>Snails &mdash; the staple.</strong> Small bladder and ramshorn snails, roughly the size of the fish's eye. They are food and tooth maintenance in one. Culture your own in a bucket or spare tank.</li>
      <li><strong>Live blackworms.</strong> The single most reliable food for getting a new pea puffer eating.</li>
      <li><strong>Frozen bloodworms, brine shrimp, daphnia, cyclops.</strong> Thaw in tank water and offer with tweezers or a pipette.</li>
      <li><strong>Frequency:</strong> once or twice a day, only as much as the fish clear in two minutes. A pea puffer with a squared-off, bulging belly has had enough.</li>
    </ul>
    <p>More detail on the <a href="/guides/puffer-fish-care/food/">feeding page</a> and the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</p>

    <h2 id="sexing">Male vs Female Pea Puffers</h2>
    <p>Pea puffers are the only commonly kept puffer that can be reliably sexed by eye, and only once they are mature at around 8 months:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Feature</th><th>Male</th><th>Female</th></tr>
      <tr><td>Belly stripe</td><td>Dark line running down the centre of the belly</td><td>No stripe</td></tr>
      <tr><td>Eye wrinkles</td><td>Iridescent creases radiating behind the eye</td><td>Absent</td></tr>
      <tr><td>Body shape</td><td>Slimmer, more streamlined</td><td>Rounder, fuller</td></tr>
      <tr><td>Colour</td><td>Brighter yellow, higher contrast</td><td>More olive, spots more diffuse</td></tr>
      <tr><td>Size</td><td>Slightly smaller</td><td>Slightly larger</td></tr>
    </table></div>
    <p>Keep two or three females per male. Males chase females hard during spawning attempts, and a lone female bears all of it.</p>

    <h2 id="mates">Pea Puffer Tank Mates</h2>
    <p>A species-only tank is the safest and most rewarding option. If you want company, the requirements are narrow: fast, short-finned, bottom-oriented or too small to interest the puffer, in a tank of at least 20 gallons.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Tank mate</th><th>Verdict</th></tr>
      <tr><td><a href="/compatibility/otocinclus-and-pea-puffer/">Otocinclus</a></td><td>Best option &mdash; peaceful, stays low, ignores the puffer</td></tr>
      <tr><td><a href="/compatibility/kuhli-loach-and-pea-puffer/">Kuhli loach</a></td><td>Workable in 20 gal+ &mdash; nocturnal and hidden</td></tr>
      <tr><td><a href="/compatibility/pea-puffer-and-pygmy-corydoras/">Pygmy corydoras</a></td><td>Sometimes works &mdash; watch for nipped barbels</td></tr>
      <tr><td><a href="/compatibility/ember-tetra-and-pea-puffer/">Ember tetra</a></td><td>Risky &mdash; fast enough, but fins get sampled</td></tr>
      <tr><td><a href="/compatibility/chili-rasbora-and-pea-puffer/">Chili rasbora</a></td><td>Risky &mdash; small enough to be seen as food by a large female</td></tr>
      <tr><td><a href="/compatibility/betta-fish-and-pea-puffer/">Betta fish</a></td><td>No &mdash; long fins are a guaranteed target</td></tr>
      <tr><td><a href="/compatibility/guppy-and-pea-puffer/">Guppy</a></td><td>No &mdash; slow and long-finned</td></tr>
      <tr><td><a href="/compatibility/cherry-shrimp-and-pea-puffer/">Cherry shrimp</a></td><td>No &mdash; this is food, not a tank mate</td></tr>
      <tr><td><a href="/compatibility/mystery-snail-and-pea-puffer/">Mystery snail</a></td><td>No &mdash; ornamental snails get eaten alive</td></tr>
      <tr><td><a href="/compatibility/goldfish-and-pea-puffer/">Goldfish</a></td><td>No &mdash; wrong temperature, wrong everything</td></tr>
    </table></div>
    <p>All ninety pairings are scored in the <a href="/compatibility/pea-puffer/">pea puffer compatibility hub</a>, or test your own list with the <a href="/tools/fish-compatibility-checker/">compatibility checker</a>.</p>

    <h2 id="breeding">Breeding Pea Puffers</h2>
    <p>Pea puffers are one of the few puffers that breed readily in aquariums, which matters because most stock is still wild-caught from a limited range.</p>
    <ol>
      <li>Condition a group on live blackworms and snails for two to three weeks.</li>
      <li>Provide dense java moss &mdash; the male drives the female into it to spawn.</li>
      <li>Eggs are scattered singly in the moss and hatch in about five days at 79&deg;F.</li>
      <li>Remove the adults or move the moss; the parents eat eggs and fry.</li>
      <li>Feed fry infusoria and vinegar eels for the first week, then microworms and baby brine shrimp.</li>
    </ol>
    <p>More on the <a href="/guides/puffer-fish-care/breeding/">puffer breeding page</a>.</p>

    <h2 id="problems">Common Pea Puffer Problems</h2>
    <ul>
      <li><strong>Refusing food on arrival.</strong> Normal for the first days. Live blackworms almost always break the standoff. See <a href="/guides/puffer-fish-care/not-eating/">not eating</a>.</li>
      <li><strong>Constant chasing.</strong> Too few fish, too little planting, or too many males. Add cover first, then rebalance the sexes.</li>
      <li><strong>Internal parasites.</strong> Wild-caught stock frequently arrives with worms. A thin fish with white stringy faeces needs a levamisole or praziquantel course.</li>
      <li><strong>Ich.</strong> Treat at half dose and raise the temperature to 82&deg;F &mdash; scaleless fish absorb medication fast. See <a href="/guides/puffer-fish-care/diseases/">diseases</a>.</li>
    </ul>
"""

PEA = {
    "slug": "pea-puffer",
    "title": "Pea Puffer Care: Tank Size, Food, Lifespan and Tank Mates",
    "meta_desc": "Pea puffer care guide: 10 gallon tank for a trio, 74-82F freshwater, snail and blackworm diet, sexing males and females, tank mates and a 4-5 year lifespan.",
    "h1": "Pea Puffer Care (Dwarf Puffer)",
    "hero_tag": "Pea / Dwarf Puffer",
    "hero_meta": "\U0001F7E2 1&ndash;1.4 in &nbsp;|&nbsp; \U0001F5C3️ 10 gal trio &nbsp;|&nbsp; \U0001F321️ 74&ndash;82&deg;F &nbsp;|&nbsp; ⏳ 4&ndash;5 yrs",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("tank", "Tank Size & Setup"),
        ("water", "Water Parameters"),
        ("food", "Food & Feeding"),
        ("sexing", "Male vs Female"),
        ("mates", "Tank Mates"),
        ("breeding", "Breeding"),
        ("problems", "Common Problems"),
    ],
    "body": PEA_BODY,
    "faqs": [
        ("How big a tank does a pea puffer need?",
         "Five gallons for a single fish and ten gallons for a trio of one male and two females. Add three to five gallons for each additional puffer, and plant heavily, because breaking up line of sight matters as much as volume for keeping the peace."),
        ("What do pea puffers eat?",
         "Live and frozen food only: small bladder and ramshorn snails, live blackworms, frozen bloodworms, brine shrimp, daphnia and cyclops. They do not eat flake or pellets, and snails are essential to keep their beak worn down."),
        ("How long do pea puffers live?",
         "Four to five years in a well-maintained tank, with three to four years being typical. Clean stable water, a varied live and frozen diet, and enough space and cover to avoid constant territorial stress are what make the difference."),
        ("How do you tell a male pea puffer from a female?",
         "Mature males have a dark stripe running down the centre of the belly and iridescent wrinkle lines radiating behind the eye, and they are slimmer and brighter yellow. Females are rounder, more olive, and have no belly stripe. The differences appear around eight months."),
        ("Can pea puffers live with other fish?",
         "Only carefully. Otocinclus and kuhli loaches work best in tanks of 20 gallons or more. Pygmy corydoras, ember tetras and chili rasboras are risky. Bettas, guppies, ornamental shrimp and snails are not options at all."),
        ("How many pea puffers should I keep together?",
         "One, or three or more. Never exactly two, because the subordinate fish becomes a permanent target. A trio of one male and two females in a heavily planted 10 gallon is the standard setup."),
        ("Are pea puffers hard to keep?",
         "Their water requirements are easy: ordinary hard freshwater at 74 to 82F. The difficulty is food, because they need a steady supply of live or frozen items and pest snails. Arrange the food supply before you buy the fish."),
    ],
    "related": [
        ("/wiki/pea-puffer/", "Pea Puffer Species Profile"),
        ("/compatibility/pea-puffer/", "Pea Puffer Tank Mates"),
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/breeding/", "Puffer Breeding & Sexing"),
    ],
    "hero_img": "/assets/encyclopedia/real/dwarf-puffer-wikimedia-real.jpg",
}


# ════════════════════════════════════════════════════════════════
# FIGURE 8 PUFFER
# ════════════════════════════════════════════════════════════════
F8_BODY = """    <p>The figure 8 puffer (<em>Dichotomyctere ocellatus</em>, formerly <em>Tetraodon biocellatus</em>) is the best-behaved of the medium puffers and the one most often sold under a false description. It comes from the estuaries and lower river reaches of Malaysia, Borneo, Sumatra and Thailand, and it needs <strong>low brackish water for its whole life</strong> &mdash; not the freshwater tank it is usually displayed in.</p>

    <h2 id="quick">Figure 8 Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Dichotomyctere ocellatus</em></td></tr>
      <tr><td>Adult size</td><td>3 in (8 cm)</td></tr>
      <tr><td>Lifespan</td><td>10&ndash;15 years</td></tr>
      <tr><td>Minimum tank</td><td>15 gal single; 20&ndash;29 gal preferred</td></tr>
      <tr><td>Water type</td><td>Low brackish, SG 1.005&ndash;1.008</td></tr>
      <tr><td>Temperature</td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>7.5&ndash;8.2</td></tr>
      <tr><td>Hardness</td><td>10&ndash;20 dGH</td></tr>
      <tr><td>Diet</td><td>Snails, clams, bloodworms, mysis</td></tr>
      <tr><td>Temperament</td><td>Curious, semi-aggressive, fin-nipper</td></tr>
    </table></div>

    <h2 id="tank">Figure 8 Puffer Tank Size</h2>
    <p><strong>Fifteen gallons is the minimum for one figure 8 puffer</strong>, with 20 to 29 gallons much better. A 24-inch footprint is the practical floor. For a second fish, add at least 10 gallons and enough hardscape to give each one its own end of the tank &mdash; and be ready to separate them if the chasing does not settle within a fortnight.</p>
    <ul>
      <li><strong>Sand substrate</strong>, driftwood, smooth rock and caves.</li>
      <li><strong>Brackish-tolerant plants only</strong> at this salinity: java fern, anubias, crypts and marimo will hold at SG 1.005; most stem plants will not.</li>
      <li><strong>Moderate flow</strong> with an oversized filter &mdash; a shellfish diet is messy.</li>
      <li><strong>Lid.</strong> They are strong swimmers and follow food upward.</li>
    </ul>

    <h2 id="brackish">Salinity: Why Freshwater Is Not Enough</h2>
    <p>A figure 8 puffer will live in freshwater for a year or two, which is exactly why the myth persists. Long term it develops poor colour, reduced appetite, susceptibility to fungal and bacterial infections, and a lifespan cut roughly in half.</p>
    <ol>
      <li>Use <strong>marine salt mix</strong>, never aquarium tonic salt or table salt.</li>
      <li>Target <strong>specific gravity 1.005&ndash;1.008</strong>, roughly 2.5&ndash;4 oz of salt per 10 gallons. Measure with a refractometer.</li>
      <li>Dissolve the salt fully in the change water at matched temperature, then add.</li>
      <li>If converting an existing freshwater tank, raise salinity by no more than 0.002 SG per week so the biofilter can adapt.</li>
    </ol>
    <p>Full salinity tables are on the <a href="/guides/puffer-fish-care/water-parameters/">water parameters page</a>.</p>

    <h2 id="food">Figure 8 Puffer Food</h2>
    <p>Snails are the staple &mdash; ramshorn, bladder and small nerites &mdash; supported by small clams and cockles in shell, frozen bloodworms, mysis and chopped krill. Feed daily as a juvenile, every other day as an adult, and always include something with a shell so the beak stays worn. See the <a href="/guides/puffer-fish-care/food/">feeding guide</a>.</p>
    <div class="callout"><strong>Snail supply note.</strong> Most freshwater pest snails survive fine at SG 1.005 for the few minutes it takes a puffer to eat them, so you can culture them in a plain freshwater tub and drop them straight in.</div>

    <h2 id="mates">Figure 8 Puffer Tank Mates</h2>
    <p>The best figure 8 tank is a species tank. Where company is attempted it has to be brackish-tolerant, fast and short-finned:</p>
    <ul>
      <li><strong>Sometimes work:</strong> bumblebee gobies, knight gobies, orange chromides, mollies acclimated to brackish water &mdash; in 29 gallons or more.</li>
      <li><strong>Do not work:</strong> anything long-finned, anything slow, all shrimp, all ornamental snails, and every freshwater community fish that cannot handle salt.</li>
      <li><strong>Other puffers:</strong> a second figure 8 is possible in a large, well-broken-up tank; green spotted puffers are too aggressive to pair with them long term.</li>
    </ul>
    <p>General rules on the <a href="/guides/puffer-fish-care/tank-mates/">tank mates page</a>.</p>

    <h2 id="behaviour">Behaviour and Health</h2>
    <p>Figure 8 puffers are alert, food-motivated and quick to recognise their keeper. They rest on the substrate and on leaves &mdash; this is normal, not illness. Watch for the specific problems this species runs into:</p>
    <ul>
      <li><strong>Ich after a temperature drop.</strong> Treat at half dose; puffers are scaleless. Raising salinity toward 1.010 also helps.</li>
      <li><strong>Internal worms in wild-caught fish.</strong> Nearly all figure 8s are wild-caught. Quarantine and deworm on arrival.</li>
      <li><strong>Overgrown teeth</strong> if the diet drifts to bloodworms alone &mdash; see the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</li>
      <li><strong>Bloating after a large meal</strong> is normal and passes; persistent swelling is not &mdash; see <a href="/guides/puffer-fish-care/puffing-up/">puffing up and bloating</a>.</li>
    </ul>
    <p>Symptom-by-symptom guides are indexed at <a href="/aquarium-fish-diseases/figure-eight-puffer-diseases/">figure eight puffer diseases</a>.</p>
"""

F8 = {
    "slug": "figure-8-puffer",
    "title": "Figure 8 Puffer Care: Tank Size, Brackish Water and Diet",
    "meta_desc": "Figure 8 puffer care: 15-20 gallon tank, brackish specific gravity 1.005-1.008, a snail and clam diet, tank mates, and a 10-15 year lifespan.",
    "h1": "Figure 8 Puffer Care",
    "hero_tag": "Figure 8 Puffer",
    "hero_meta": "\U0001F004 3 in &nbsp;|&nbsp; \U0001F5C3️ 15&ndash;20 gal &nbsp;|&nbsp; \U0001F9C2 SG 1.005&ndash;1.008 &nbsp;|&nbsp; ⏳ 10&ndash;15 yrs",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("tank", "Tank Size"),
        ("brackish", "Salinity"),
        ("food", "Food"),
        ("mates", "Tank Mates"),
        ("behaviour", "Behaviour & Health"),
    ],
    "body": F8_BODY,
    "faqs": [
        ("What size tank does a figure 8 puffer need?",
         "Fifteen gallons is the minimum for one adult, with 20 to 29 gallons preferred and a 24 inch footprint as the practical floor. Add at least 10 gallons and plenty of hardscape for a second fish."),
        ("Do figure 8 puffers need brackish water?",
         "Yes, for their whole lives. Target specific gravity 1.005 to 1.008 using marine salt mix, which is roughly 2.5 to 4 ounces per 10 gallons. They survive freshwater for a year or two, then decline in colour, appetite and lifespan."),
        ("What do figure 8 puffers eat?",
         "Snails as the staple, plus small clams and cockles in shell, frozen bloodworms, mysis and chopped krill. Feed daily as a juvenile and every other day as an adult, always including a shelled item to wear the beak down."),
        ("What are good figure 8 puffer tank mates?",
         "A species-only tank is safest. In 29 gallons or more, bumblebee gobies, knight gobies, orange chromides and brackish-acclimated mollies sometimes work. Long-finned fish, slow fish, shrimp and ornamental snails never do."),
        ("How long do figure 8 puffers live?",
         "Ten to fifteen years in correct low brackish water. Kept permanently in freshwater the same fish typically manages five to seven years, which is where the reputation for a short lifespan comes from."),
        ("Can figure 8 puffers live with green spotted puffers?",
         "Not long term. Green spotted puffers become considerably more aggressive as they mature and need much higher salinity as adults, so the two species end up incompatible on both temperament and water chemistry."),
    ],
    "related": [
        ("/guides/puffer-fish-care/green-spotted-puffer/", "Green Spotted Puffer Care"),
        ("/guides/puffer-fish-care/water-parameters/", "Brackish Water Parameters"),
        ("/aquarium-fish-diseases/figure-eight-puffer-diseases/", "Figure 8 Puffer Diseases"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
    "hero_img": "/assets/encyclopedia/real/figure-eight-puffer-wikimedia-real.jpg",
}


# ════════════════════════════════════════════════════════════════
# GREEN SPOTTED PUFFER
# ════════════════════════════════════════════════════════════════
GSP_BODY = """    <p>The green spotted puffer (<em>Dichotomyctere nigroviridis</em>), or GSP, is the most widely sold and most widely mis-kept puffer in the hobby. Shops display 1-inch juveniles in freshwater community tanks. The fish reaches 6 inches, becomes progressively more aggressive, and needs to finish its life in <strong>high brackish to near-marine water</strong>. Get that right and it is a fifteen-year fish with enormous character.</p>

    <h2 id="quick">Green Spotted Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Dichotomyctere nigroviridis</em></td></tr>
      <tr><td>Adult size</td><td>6 in (15 cm)</td></tr>
      <tr><td>Lifespan</td><td>10&ndash;15 years</td></tr>
      <tr><td>Minimum tank</td><td>30 gal single; 40&ndash;55 gal preferred</td></tr>
      <tr><td>Water type</td><td>Brackish, increasing with age to SG 1.018&ndash;1.022</td></tr>
      <tr><td>Temperature</td><td>76&ndash;82&deg;F (24&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>7.8&ndash;8.4</td></tr>
      <tr><td>Diet</td><td>Snails, clams, mussel, unpeeled shrimp, krill</td></tr>
      <tr><td>Temperament</td><td>Aggressive, especially as an adult</td></tr>
    </table></div>

    <h2 id="salinity">The Salinity Ramp</h2>
    <p>This is the whole game with GSPs. In the wild the fish is born in near-fresh river water and migrates seawards as it grows. Reproduce that:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Size</th><th>Specific gravity</th><th>Rough marine salt per 10 gal</th></tr>
      <tr><td>Under 2 in (juvenile)</td><td>1.005&ndash;1.008</td><td>2.5&ndash;4 oz</td></tr>
      <tr><td>2&ndash;4 in (sub-adult)</td><td>1.010&ndash;1.015</td><td>5&ndash;7.5 oz</td></tr>
      <tr><td>Over 4 in (adult)</td><td>1.018&ndash;1.022</td><td>9&ndash;11 oz</td></tr>
    </table></div>
    <p>Raise salinity slowly &mdash; about 0.002 SG per week &mdash; and remember the biofilter re-adapts each time. Measure with a refractometer, not a floating hydrometer. Full method on the <a href="/guides/puffer-fish-care/water-parameters/">water parameters page</a>.</p>
    <div class="callout callout-warn"><strong>A GSP kept permanently in freshwater</strong> typically shows dull colour, bloating, fungal and bacterial infections, and dies at three to five years instead of ten to fifteen. This is the most common preventable puffer death in the hobby.</div>

    <h2 id="tank">Green Spotted Puffer Tank Size</h2>
    <p><strong>Thirty gallons is the minimum for one adult GSP</strong>, and 40 to 55 gallons is the realistic target given the waste load. Use a 36-inch or longer footprint. Two GSPs need at least 55 gallons plus dense hardscape, and many pairs still have to be separated eventually.</p>
    <ul>
      <li><strong>Filtration:</strong> 6&ndash;8&times; turnover, oversized mechanical stage. A canister or sump.</li>
      <li><strong>Substrate:</strong> aragonite sand or crushed coral helps hold pH and alkalinity at high salinity.</li>
      <li><strong>Hardscape:</strong> rock, wood and caves &mdash; adults need somewhere to retreat and something to explore, or they get destructive.</li>
      <li><strong>Plants:</strong> at adult salinity, use macroalgae such as <em>Caulerpa</em> rather than freshwater plants.</li>
    </ul>

    <h2 id="food">Green Spotted Puffer Food</h2>
    <p>Snails and shellfish, always in shell. GSPs have powerful beaks and need the work:</p>
    <ul>
      <li><strong>Staples:</strong> ramshorn and bladder snails, small clams, cockles, mussel, unpeeled shrimp.</li>
      <li><strong>Supplements:</strong> krill, mysis, chopped squid and white fish, frozen bloodworms for juveniles.</li>
      <li><strong>Frequency:</strong> daily under 2 inches, every other day as an adult.</li>
      <li><strong>Remove leftovers</strong> within an hour &mdash; shellfish fouls water fast.</li>
    </ul>

    <h2 id="mates">Green Spotted Puffer Tank Mates</h2>
    <p>An adult GSP is effectively a single-specimen fish. Juveniles tolerate company; adults kill it. Where people succeed it is usually with:</p>
    <ul>
      <li><strong>Other GSPs</strong> in 55 gallons or more, introduced young and at the same size, with plenty of visual breaks &mdash; and a backup tank ready.</li>
      <li><strong>Brackish-tolerant, fast species</strong> such as knight gobies, monos or scats in large tanks, with mixed results.</li>
      <li><strong>Nothing else.</strong> No shrimp, no ornamental snails, no long-finned fish, and no freshwater community fish, which cannot survive the salinity anyway.</li>
    </ul>
    <p>See the <a href="/guides/puffer-fish-care/tank-mates/">tank mates guide</a> and <a href="/guides/puffer-fish-care/behavior/">puffer aggression</a>.</p>

    <h2 id="health">Common GSP Health Problems</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Problem</th><th>Likely cause</th><th>Action</th></tr>
      <tr><td>Dull colour, dark belly</td><td>Stress, wrong salinity, poor water</td><td>Test everything; check SG against the ramp table</td></tr>
      <tr><td>Bloating that does not resolve</td><td>Constipation, internal issue, long-term freshwater</td><td>Fast 2&ndash;3 days; review salinity and diet</td></tr>
      <tr><td>Refusing food</td><td>New arrival, parasites, overgrown teeth</td><td>See <a href="/guides/puffer-fish-care/not-eating/">not eating</a></td></tr>
      <tr><td>White spots</td><td>Ich, usually after a temperature drop</td><td>Half-dose meds, raise temperature and salinity</td></tr>
      <tr><td>Cloudy eye</td><td>Water quality or physical injury</td><td>Large water change; check nitrate</td></tr>
    </table></div>
    <p>Detail on the <a href="/guides/puffer-fish-care/diseases/">puffer diseases page</a>.</p>
"""

GSP = {
    "slug": "green-spotted-puffer",
    "title": "Green Spotted Puffer Care: Tank Size, Salinity and Diet",
    "meta_desc": "Green spotted puffer care: 30 gallon minimum, the brackish salinity ramp from 1.005 to 1.022, shell-on diet, and why freshwater halves their lifespan.",
    "h1": "Green Spotted Puffer Care",
    "hero_tag": "Green Spotted Puffer",
    "hero_meta": "\U0001F7E1 6 in &nbsp;|&nbsp; \U0001F5C3️ 30 gal min &nbsp;|&nbsp; \U0001F9C2 SG 1.005 &rarr; 1.022 &nbsp;|&nbsp; ⏳ 10&ndash;15 yrs",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("salinity", "The Salinity Ramp"),
        ("tank", "Tank Size"),
        ("food", "Food"),
        ("mates", "Tank Mates"),
        ("health", "Health Problems"),
    ],
    "body": GSP_BODY,
    "faqs": [
        ("What size tank does a green spotted puffer need?",
         "Thirty gallons minimum for one adult, with 40 to 55 gallons preferred and a 36 inch or longer footprint. Two green spotted puffers need at least 55 gallons plus heavy hardscape, and they still often have to be separated."),
        ("Do green spotted puffers need salt water?",
         "They need brackish water that increases with age. Juveniles under 2 inches sit at specific gravity 1.005 to 1.008, sub-adults at 1.010 to 1.015, and adults over 4 inches at 1.018 to 1.022, which is close to full marine."),
        ("Can a green spotted puffer live in freshwater?",
         "Only as a young juvenile, and only temporarily. Kept in freshwater long term, a green spotted puffer loses colour, bloats, becomes prone to fungal and bacterial infection, and typically dies at three to five years rather than ten to fifteen."),
        ("What do green spotted puffers eat?",
         "Shell-on food: ramshorn and bladder snails, small clams, cockles, mussel and unpeeled shrimp, supplemented with krill, mysis, squid and white fish. Feed daily as a juvenile and every other day as an adult."),
        ("What tank mates can a green spotted puffer have?",
         "Realistically none as an adult. Other green spotted puffers in 55 gallons or more sometimes work if introduced young at the same size, and brackish species like knight gobies, monos and scats occasionally do in large tanks. Shrimp, snails and long-finned fish never do."),
        ("How big do green spotted puffers get?",
         "About 6 inches, reached over two to three years. They are usually sold at around one inch, which is why so many end up in tanks that are far too small by the time they mature."),
    ],
    "related": [
        ("/guides/puffer-fish-care/figure-8-puffer/", "Figure 8 Puffer Care"),
        ("/guides/puffer-fish-care/water-parameters/", "Brackish Water Parameters"),
        ("/guides/puffer-fish-care/tank-mates/", "Puffer Tank Mates"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# AMAZON PUFFER
# ════════════════════════════════════════════════════════════════
AMAZON_BODY = """    <p>The Amazon puffer (<em>Colomesus asellus</em>) is the odd one out in the family: a <strong>true freshwater, genuinely shoaling puffer</strong> that swims in open water all day rather than hovering in a corner. It is also sold as the South American puffer, bee puffer or Brazilian puffer, and it comes from the main channels of the Amazon and Orinoco basins. Keep it in a group, give it flow and length, and be ready for the fastest tooth growth of any aquarium puffer.</p>

    <h2 id="quick">Amazon Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Colomesus asellus</em></td></tr>
      <tr><td>Adult size</td><td>3&ndash;3.5 in (8&ndash;9 cm)</td></tr>
      <tr><td>Lifespan</td><td>8&ndash;10 years</td></tr>
      <tr><td>Minimum tank</td><td>30 gal for a group of five</td></tr>
      <tr><td>Water type</td><td>True freshwater &mdash; no salt</td></tr>
      <tr><td>Temperature</td><td>72&ndash;82&deg;F (22&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>6.5&ndash;7.5</td></tr>
      <tr><td>Group size</td><td>5 or more &mdash; genuinely shoaling</td></tr>
      <tr><td>Temperament</td><td>Hyperactive, persistent fin-nipper</td></tr>
    </table></div>

    <h2 id="group">Why Amazon Puffers Need a Group</h2>
    <p>Unlike almost every other puffer, <em>Colomesus asellus</em> shoals in the wild and behaves badly alone. A single Amazon puffer becomes nervous, hides and often stops eating; a pair pushes all the aggression onto one fish. <strong>Keep five or more.</strong> In a group the constant low-level chasing spreads out and no individual takes the brunt of it.</p>
    <p>That group needs room: <strong>30 gallons for five</strong>, and 40 to 55 gallons is better. Prioritise length &mdash; a 36-inch footprint minimum, 48 inches for a larger group.</p>

    <h2 id="tank">Tank Setup and Flow</h2>
    <ul>
      <li><strong>Open swimming lanes.</strong> Structure along the back and sides, clear water in the middle.</li>
      <li><strong>Moderate to strong flow.</strong> These are river-channel fish and they use current all day. A powerhead or a canister return aimed along the length works well.</li>
      <li><strong>Driftwood and root tangles</strong> at the ends of the tank for retreat.</li>
      <li><strong>Sand or fine gravel</strong>, and plants they will ignore rather than eat &mdash; anubias and java fern on wood.</li>
      <li><strong>Filtration:</strong> 6&ndash;8&times; turnover, plus 30&ndash;50% weekly changes. Nitrate under 20 ppm.</li>
    </ul>

    <h2 id="food">Amazon Puffer Food and the Teeth Problem</h2>
    <p>Amazon puffers grow their beak faster than any other commonly kept puffer, so shelled food is not optional and even a good diet may not be enough.</p>
    <ul>
      <li><strong>Daily staples:</strong> small snails, chopped cockle in shell, frozen bloodworms, mysis, brine shrimp.</li>
      <li><strong>Feed daily</strong> &mdash; this is an active fish with a fast metabolism.</li>
      <li><strong>Expect to check the beak.</strong> Many Amazon puffers need trimming every four to eight months regardless of diet. See the <a href="/guides/puffer-fish-care/teeth/">teeth and trimming page</a>.</li>
      <li><strong>Watch the fastest eaters.</strong> In a group, one or two fish take most of the shelled food; spread it across the tank.</li>
    </ul>

    <h2 id="mates">Amazon Puffer Tank Mates</h2>
    <p>Their own kind first. Beyond that, Amazon puffers are relentless nippers &mdash; a slow or long-finned fish will be stripped. Where mixed tanks work it is usually a large, high-flow South American setup with fast mid-water fish that keep clear:</p>
    <ul>
      <li><strong>Possible in 55 gal+:</strong> large fast tetras, silver dollars, hoplo catfish, larger loricariids that stay under wood.</li>
      <li><strong>No:</strong> angelfish, gouramis, bettas, guppies, corydoras with long barbels, all shrimp and ornamental snails.</li>
    </ul>
    <p>Check any pairing with the <a href="/tools/fish-compatibility-checker/">compatibility checker</a>, and see the <a href="/guides/puffer-fish-care/tank-mates/">tank mates guide</a>.</p>

    <h2 id="health">Health Notes</h2>
    <ul>
      <li><strong>Wild-caught by default.</strong> Quarantine for four weeks and deworm with praziquantel and metronidazole on arrival.</li>
      <li><strong>Nitrate sensitivity.</strong> As an active fish in a group, it shows chronic nitrate as faded colour and reduced activity before anything else.</li>
      <li><strong>Half-dose medication.</strong> Scaleless, like every puffer.</li>
      <li><strong>Beak checks every few months</strong> &mdash; catching overgrowth early avoids sedation.</li>
    </ul>
"""

AMAZON = {
    "slug": "amazon-puffer",
    "title": "Amazon Puffer Care: Tank Size, Group Size and Diet",
    "meta_desc": "Amazon puffer care guide: a true freshwater shoaling puffer needing groups of five, a 30 gallon tank with flow, daily shelled food and frequent teeth checks.",
    "h1": "Amazon Puffer Care (South American Puffer)",
    "hero_tag": "Amazon Puffer",
    "hero_meta": "\U0001F30D 3&ndash;3.5 in &nbsp;|&nbsp; \U0001F41F Groups of 5+ &nbsp;|&nbsp; \U0001F5C3️ 30 gal &nbsp;|&nbsp; \U0001F9B7 Fastest tooth growth",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("group", "Why They Need a Group"),
        ("tank", "Tank Setup & Flow"),
        ("food", "Food & Teeth"),
        ("mates", "Tank Mates"),
        ("health", "Health Notes"),
    ],
    "body": AMAZON_BODY,
    "faqs": [
        ("What size tank does an Amazon puffer need?",
         "Thirty gallons for a group of five, with 40 to 55 gallons preferred. Length matters most: a 36 inch footprint is the minimum and 48 inches suits a larger group, because these are open-water river fish that swim all day."),
        ("Do Amazon puffers need to be kept in groups?",
         "Yes. Colomesus asellus is one of the few genuinely shoaling puffers. A single fish becomes nervous and often stops eating, and a pair concentrates all the aggression on one individual. Keep five or more."),
        ("What do Amazon puffers eat?",
         "Small snails, chopped cockle in shell, frozen bloodworms, mysis and brine shrimp, fed daily. Shelled food matters more for this species than any other because it grows its beak faster than any other aquarium puffer."),
        ("Are Amazon puffers freshwater?",
         "Yes, genuinely. Colomesus asellus lives its whole life in the fresh water of the Amazon and Orinoco basins and needs no added salt, unlike green spotted and figure 8 puffers."),
        ("What tank mates work with Amazon puffers?",
         "Their own kind first. In 55 gallons or more, fast mid-water fish such as large tetras and silver dollars sometimes work. Angelfish, gouramis, bettas, guppies, shrimp and ornamental snails do not, because Amazon puffers are persistent fin-nippers."),
        ("How often do Amazon puffers need their teeth trimmed?",
         "Many need it every four to eight months even on a diet full of shelled food, because their beak grows unusually fast. Check the mouth every few months and correct the diet early rather than waiting for the fish to stop eating."),
    ],
    "related": [
        ("/guides/puffer-fish-care/teeth/", "Puffer Teeth & Trimming"),
        ("/guides/puffer-fish-care/freshwater/", "Freshwater Puffer Fish"),
        ("/guides/puffer-fish-care/tank-mates/", "Puffer Tank Mates"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# FAHAKA PUFFER
# ════════════════════════════════════════════════════════════════
FAHAKA_BODY = """    <p>The fahaka puffer (<em>Tetraodon lineatus</em>) is the largest puffer most aquarists can realistically keep: a 16&ndash;18 inch true freshwater predator from the Nile and the river systems of west and central Africa. It is also sold as the Nile puffer, lineatus puffer or globe fish. It is intelligent, interactive, entirely intolerant of tank mates, and it will bite hard enough to cause real injury.</p>

    <h2 id="quick">Fahaka Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Tetraodon lineatus</em></td></tr>
      <tr><td>Adult size</td><td>16&ndash;18 in (40&ndash;45 cm)</td></tr>
      <tr><td>Lifespan</td><td>10&ndash;15 years</td></tr>
      <tr><td>Minimum tank</td><td>125 gal (72&times;24 in); 180 gal preferred</td></tr>
      <tr><td>Water type</td><td>True freshwater</td></tr>
      <tr><td>Temperature</td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>7.0&ndash;8.0</td></tr>
      <tr><td>Hardness</td><td>10&ndash;20 dGH</td></tr>
      <tr><td>Tank mates</td><td>None &mdash; strictly solitary</td></tr>
    </table></div>

    <h2 id="tank">Fahaka Puffer Tank Size</h2>
    <p><strong>One hundred and twenty-five gallons is the working minimum</strong>, and the dimensions matter more than the number: you want at least 72 inches long by 24 inches front to back so an 18-inch fish can turn without bending. A 180-gallon or a 6&times;2&times;2 foot custom tank is where most long-term fahaka keepers end up.</p>
    <ul>
      <li><strong>Grow-out:</strong> a 2-inch juvenile can start in a 40-gallon for six to nine months, then must move. Fahakas add 4&ndash;6 inches in their first year.</li>
      <li><strong>Filtration:</strong> a sump, or two large canisters. This fish eats whole shellfish and the waste load is closer to a large cichlid pond than an aquarium.</li>
      <li><strong>Water changes:</strong> 40&ndash;50% weekly, every week.</li>
      <li><strong>Hardscape:</strong> sand, heavy smooth rock and large driftwood, all placed so a digging fish cannot bring it down. Nothing sharp &mdash; fahakas rub and scrape.</li>
      <li><strong>Heater:</strong> guarded or in the sump. Fahakas have broken heaters.</li>
    </ul>
    <p>Check dimensions against volume with the <a href="/tools/tank-size-calculator/">tank size calculator</a>.</p>

    <h2 id="solitary">Why Fahakas Are Kept Alone</h2>
    <p>A fahaka puffer will eventually kill anything you put with it, including fish far larger than itself. Juveniles sometimes tolerate company for months, which persuades people it will work; the change when it comes is fast and fatal. Plan a single-specimen tank from the start.</p>
    <div class="callout callout-warn"><strong>Handling.</strong> A fahaka's beak crushes crab shells. Never hand-feed, never put a hand in the tank with the fish loose at the same end, and move the fish in a container rather than a net &mdash; a netted puffer can gulp air.</div>

    <h2 id="food">Fahaka Puffer Food</h2>
    <ul>
      <li><strong>Staples:</strong> whole mussels and clams in shell, crayfish, unpeeled prawns, crab legs, cockles, large snails.</li>
      <li><strong>Supplements:</strong> chunks of white fish, squid, earthworms.</li>
      <li><strong>Frequency:</strong> daily as a small juvenile, every other day through the grow-out, then two to three times a week as an adult. Adult fahakas fed daily become obese.</li>
      <li><strong>Never feeder fish.</strong> Thiaminase and disease risk with no benefit.</li>
      <li><strong>Use long tongs.</strong> Always.</li>
    </ul>
    <p>See the <a href="/guides/puffer-fish-care/food/">feeding guide</a> and the <a href="/guides/puffer-fish-care/teeth/">teeth page</a> &mdash; shell-on food is what keeps an 18-inch beak in check.</p>

    <h2 id="behaviour">Behaviour</h2>
    <p>Fahakas recognise their keeper, follow movement outside the glass, and beg. They also rearrange the tank, dig, and go through moody phases where they hide for a day or two. Colour shifts from bright yellow-and-brown striping to dark and muted with mood and stress &mdash; see <a href="/guides/puffer-fish-care/color-change/">colour changes</a>. Sudden glass-surfing or refusing food for more than a few days is worth investigating; both are covered on the <a href="/guides/puffer-fish-care/not-eating/">not eating page</a>.</p>

    <h2 id="health">Health Notes</h2>
    <ul>
      <li><strong>Wild-caught.</strong> Almost all fahakas are. Quarantine and deworm with praziquantel and metronidazole on arrival.</li>
      <li><strong>Nitrate is the chronic killer.</strong> Test weekly; hold under 20 ppm.</li>
      <li><strong>Half-dose medication</strong> and avoid copper.</li>
      <li><strong>Scrapes and cuts</strong> heal well in clean water but infect quickly in dirty water &mdash; another reason for the large weekly change.</li>
    </ul>
"""

FAHAKA = {
    "slug": "fahaka-puffer",
    "title": "Fahaka Puffer Care: Tank Size, Diet and Why It Lives Alone",
    "meta_desc": "Fahaka puffer care guide: 125 gallon minimum for a 16-18 inch Nile puffer, freshwater parameters, shell-on diet, solitary housing and safe handling advice.",
    "h1": "Fahaka Puffer Care (Nile Puffer)",
    "hero_tag": "Fahaka Puffer",
    "hero_meta": "\U0001F1EA\U0001F1EC 16&ndash;18 in &nbsp;|&nbsp; \U0001F5C3️ 125 gal min &nbsp;|&nbsp; \U0001F6AB Solitary &nbsp;|&nbsp; ⏳ 10&ndash;15 yrs",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("tank", "Tank Size"),
        ("solitary", "Kept Alone"),
        ("food", "Food"),
        ("behaviour", "Behaviour"),
        ("health", "Health Notes"),
    ],
    "body": FAHAKA_BODY,
    "faqs": [
        ("What size tank does a fahaka puffer need?",
         "125 gallons is the working minimum, with a footprint of at least 72 by 24 inches so an 18 inch fish can turn freely. 180 gallons or a custom 6 by 2 by 2 foot tank is where most long-term keepers end up."),
        ("How big does a fahaka puffer get?",
         "16 to 18 inches, reached over three to four years, with 4 to 6 inches of growth in the first year alone. A 2 inch juvenile outgrows a 40 gallon grow-out tank within six to nine months."),
        ("Can a fahaka puffer live with other fish?",
         "No. Fahakas are strictly solitary. Juveniles sometimes tolerate tank mates for months, which misleads keepers, but an adult will eventually kill anything sharing its tank, including much larger fish."),
        ("What do fahaka puffers eat?",
         "Whole mussels and clams in shell, crayfish, unpeeled prawns, crab legs, cockles and large snails, with white fish, squid and earthworms as supplements. Feed adults two to three times a week and always use long tongs."),
        ("Do fahaka puffers need brackish water?",
         "No. Tetraodon lineatus is a true freshwater fish from the Nile and other African river systems. Keep it at pH 7.0 to 8.0 and 10 to 20 dGH with no added salt."),
        ("Are fahaka puffers aggressive?",
         "Extremely, toward other fish. Toward their keeper they are curious and interactive but capable of a serious bite, so never hand-feed and never move one with a net, because a netted puffer can gulp air."),
    ],
    "related": [
        ("/guides/puffer-fish-care/mbu-puffer/", "Mbu Puffer Care"),
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
    "hero_img": "/assets/encyclopedia/real/fahaka-puffer-wikimedia-real.jpg",
}


# ════════════════════════════════════════════════════════════════
# MBU PUFFER
# ════════════════════════════════════════════════════════════════
MBU_BODY = """    <p>The mbu puffer (<em>Tetraodon mbu</em>) is the largest freshwater puffer in the world, reaching 24 to 30 inches in captivity. It comes from the Congo River basin and Lake Tanganyika, and it is sold at two or three inches for the price of a pizza. Almost every mbu sold ends up rehomed, given to a public aquarium, or dead in an inadequate tank. If you are considering one, price the tank first.</p>

    <div class="callout callout-warn"><strong>Reality check.</strong> An adult mbu needs 500 gallons as an absolute floor and 1,000 gallons or an indoor pond to thrive. That is a ten-foot tank, a stand rated for several tonnes, a floor that can take it, and a sump-scale filtration system. This is a fifteen-to-twenty-year commitment.</div>

    <h2 id="quick">Mbu Puffer Care at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Value</th></tr>
      <tr><td>Scientific name</td><td><em>Tetraodon mbu</em></td></tr>
      <tr><td>Adult size</td><td>24&ndash;30 in (60&ndash;75 cm)</td></tr>
      <tr><td>Lifespan</td><td>10&ndash;20+ years</td></tr>
      <tr><td>Minimum tank</td><td>500 gal; 1,000 gal or pond to thrive</td></tr>
      <tr><td>Water type</td><td>True freshwater</td></tr>
      <tr><td>Temperature</td><td>75&ndash;82&deg;F (24&ndash;28&deg;C)</td></tr>
      <tr><td>pH</td><td>7.0&ndash;8.0</td></tr>
      <tr><td>Tank mates</td><td>None &mdash; strictly solitary</td></tr>
    </table></div>

    <h2 id="tank">Mbu Puffer Tank Size</h2>
    <p>The published minimum of 500 gallons assumes a footprint around 10 feet by 4 feet. Height is largely wasted &mdash; mbus use the bottom two-thirds. Practical routes people take:</p>
    <ul>
      <li><strong>Custom acrylic or plywood-and-glass builds</strong>, 10&times;4&times;2 feet or larger, on an engineered stand.</li>
      <li><strong>Indoor heated ponds</strong>, often the most economical option at this volume.</li>
      <li><strong>Grow-out staging:</strong> a 3-inch juvenile can spend a year in 75&ndash;125 gallons, then needs 300 gallons by year three and the full build by year five. Do not buy the fish planning to build later.</li>
    </ul>
    <p>Filtration has to be pond-scale: a large sump, high-capacity mechanical stages, and 30&ndash;50% weekly water changes with an automated system if you value your evenings.</p>

    <h2 id="food">Mbu Puffer Food</h2>
    <p>An adult mbu eats like a small predator. Shell-on food is essential &mdash; the beak on a 28-inch puffer overgrows fast and sedating a fish that size for trimming is a serious undertaking.</p>
    <ul>
      <li><strong>Staples:</strong> whole mussels and clams, crayfish, crab legs, unpeeled prawns, large snails.</li>
      <li><strong>Supplements:</strong> squid, whole white fish, earthworms.</li>
      <li><strong>Frequency:</strong> daily as a juvenile, every other day through grow-out, two to three times a week as an adult.</li>
      <li><strong>Tongs, always.</strong> An adult mbu bite is a hospital visit.</li>
    </ul>

    <h2 id="solitary">Tank Mates and Temperament</h2>
    <p>Mbus are curious and famously interactive with keepers, and completely unsuitable for community life. Even in a very large tank an adult will eventually take an interest in anything sharing the water. Keep one fish per system.</p>

    <h2 id="alternatives">Should You Get One?</h2>
    <p>For almost everyone the honest answer is no. If the character of a large puffer is what appeals, the <a href="/guides/puffer-fish-care/fahaka-puffer/">fahaka puffer</a> gives you most of it in a 125-gallon tank. For interactivity at a fraction of the scale, a <a href="/guides/puffer-fish-care/green-spotted-puffer/">green spotted puffer</a> in 40 gallons or a group of <a href="/guides/puffer-fish-care/pea-puffer/">pea puffers</a> in 20 gallons deliver far more per gallon.</p>
    <p>Buy an mbu only if the adult-sized system already exists or is fully funded and scheduled. See the <a href="/guides/puffer-fish-care/size-growth/">growth timeline</a> for how quickly the clock runs.</p>

    <h2 id="health">Health Notes</h2>
    <ul>
      <li><strong>Wild-caught.</strong> Quarantine and deworm on arrival &mdash; while the fish is still a size you can quarantine.</li>
      <li><strong>Nitrate control is everything</strong> at this waste load. Under 20 ppm, weekly.</li>
      <li><strong>Half-dose medication</strong>, and note that medicating 500 gallons is expensive &mdash; another argument for a strict quarantine period.</li>
      <li><strong>Never net an adult.</strong> Move it in a large submerged container.</li>
    </ul>
"""

MBU = {
    "slug": "mbu-puffer",
    "title": "Mbu Puffer Care: Tank Size, Diet and Adult Reality Check",
    "meta_desc": "Mbu puffer care guide: the 24-30 inch giant freshwater puffer needs 500+ gallons, pond-scale filtration, shell-on food and solitary housing for 15-20 years.",
    "h1": "Mbu Puffer Care (Giant Freshwater Puffer)",
    "hero_tag": "Mbu Puffer",
    "hero_meta": "\U0001F40B 24&ndash;30 in &nbsp;|&nbsp; \U0001F5C3️ 500+ gal &nbsp;|&nbsp; \U0001F6AB Solitary &nbsp;|&nbsp; ⏳ 10&ndash;20+ yrs",
    "toc_sections": [
        ("quick", "Care at a Glance"),
        ("tank", "Tank Size"),
        ("food", "Food"),
        ("solitary", "Tank Mates"),
        ("alternatives", "Should You Get One?"),
        ("health", "Health Notes"),
    ],
    "body": MBU_BODY,
    "faqs": [
        ("What size tank does an mbu puffer need?",
         "500 gallons is the absolute minimum for an adult and 1,000 gallons or an indoor pond is what the fish actually needs, with a footprint around 10 feet by 4 feet. Height matters little because mbus use the bottom two-thirds."),
        ("How big does an mbu puffer get?",
         "24 to 30 inches in captivity, making it the largest freshwater puffer in the world. It is usually sold at two or three inches and takes five to seven years to reach full size."),
        ("Can an mbu puffer live with other fish?",
         "No. Mbu puffers are strictly solitary. Even in a very large system an adult will eventually attack anything sharing the water, so plan one fish per tank."),
        ("What do mbu puffers eat?",
         "Whole mussels and clams, crayfish, crab legs, unpeeled prawns and large snails, supplemented with squid, whole white fish and earthworms. Feed adults two or three times a week and always use long tongs."),
        ("How long do mbu puffers live?",
         "Ten to twenty years or more in a correctly sized system. That makes buying one a longer commitment than most pets, and it is the main reason so many end up rehomed to public aquariums."),
        ("Is there a smaller alternative to an mbu puffer?",
         "Yes. A fahaka puffer gives you most of the same character in a 125 gallon tank, a green spotted puffer fits 40 gallons, and a group of pea puffers thrives in 20 gallons with far more activity per gallon."),
    ],
    "related": [
        ("/guides/puffer-fish-care/fahaka-puffer/", "Fahaka Puffer Care"),
        ("/guides/puffer-fish-care/size-growth/", "Puffer Size & Growth"),
        ("/guides/puffer-fish-care/tank-size/", "Puffer Tank Size"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TANK MATES
# ════════════════════════════════════════════════════════════════
MATES_BODY = """    <p>The short version: <strong>most puffers should be kept alone or with their own kind</strong>. Puffers are slow, curious, food-motivated and equipped with a beak that takes a clean bite out of a fin. They also eat invertebrates for a living, which rules out every shrimp and ornamental snail. That said, a handful of species do tolerate carefully chosen company, and the rules for choosing it are consistent.</p>

    <h2 id="rules">The Five Rules for Puffer Tank Mates</h2>
    <ol>
      <li><strong>Fast and short-finned.</strong> Anything flowing, trailing or slow becomes a chew toy.</li>
      <li><strong>Not an invertebrate.</strong> Shrimp and ornamental snails are food, not tank mates.</li>
      <li><strong>Same water type.</strong> A brackish puffer rules out every freshwater community fish automatically.</li>
      <li><strong>Big enough tank.</strong> Nothing on the "sometimes works" list works in a 10-gallon. Twenty gallons is the floor for a mixed pea puffer tank; 55 gallons for anything larger.</li>
      <li><strong>Have a backup plan.</strong> A separate tank ready before you try, because the failure mode is a bitten fish, not a warning.</li>
    </ol>

    <h2 id="by-species">Which Puffers Can Have Tank Mates?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Tank mates possible?</th></tr>
      <tr><td>Pea / dwarf puffer</td><td>Sometimes &mdash; otocinclus, kuhli loaches in 20 gal+</td></tr>
      <tr><td>Red eye puffer</td><td>Sometimes &mdash; the mildest of the small puffers</td></tr>
      <tr><td>Amazon puffer</td><td>Own kind (groups of 5+); fast large tetras in 55 gal+</td></tr>
      <tr><td>Figure 8 puffer</td><td>Rarely &mdash; bumblebee and knight gobies at matching salinity</td></tr>
      <tr><td>Green spotted puffer</td><td>Juveniles only; adults are effectively solitary</td></tr>
      <tr><td>Congo, hairy, avocado puffer</td><td>No &mdash; ambush predators or relentless attackers</td></tr>
      <tr><td>Fahaka, mbu puffer</td><td>No &mdash; strictly single specimen</td></tr>
      <tr><td>Marine puffers</td><td>Robust, fast FOWLR fish only; never invertebrates or corals</td></tr>
    </table></div>

    <h2 id="best">Best Tank Mates for a Pea Puffer</h2>
    <p>Most "puffer tank mates" searches are really about pea puffers, because they are the only puffer small enough for a normal community tank. In a 20-gallon-plus, heavily planted tank:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Verdict</th><th>Why</th></tr>
      <tr><td><a href="/compatibility/otocinclus-and-pea-puffer/">Otocinclus</a></td><td>Best option</td><td>Peaceful algae grazer, stays low, no fin interest</td></tr>
      <tr><td><a href="/compatibility/kuhli-loach-and-pea-puffer/">Kuhli loach</a></td><td>Good</td><td>Nocturnal, hides, fast when it moves</td></tr>
      <tr><td><a href="/compatibility/pea-puffer-and-pygmy-corydoras/">Pygmy corydoras</a></td><td>Fair</td><td>Works in groups; watch for nipped barbels</td></tr>
      <tr><td><a href="/compatibility/pea-puffer-and-zebra-danio/">Zebra danio</a></td><td>Fair</td><td>Fast enough to stay clear, but boisterous</td></tr>
      <tr><td><a href="/compatibility/harlequin-rasbora-and-pea-puffer/">Harlequin rasbora</a></td><td>Risky</td><td>Fast, but fins are still a target</td></tr>
      <tr><td><a href="/compatibility/ember-tetra-and-pea-puffer/">Ember tetra</a></td><td>Risky</td><td>Small enough for a large female to try</td></tr>
    </table></div>

    <h2 id="never">Fish That Never Work With Puffers</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Pairing</th><th>Verdict</th><th>Reason</th></tr>
      <tr><td><a href="/compatibility/betta-fish-and-pea-puffer/">Puffer and betta</a></td><td>No</td><td>Long flowing fins plus two territorial fish</td></tr>
      <tr><td><a href="/compatibility/guppy-and-pea-puffer/">Puffer and guppies</a></td><td>No</td><td>Slow, long-finned, brightly coloured &mdash; a target</td></tr>
      <tr><td><a href="/compatibility/neon-tetra-and-pea-puffer/">Puffer and tetras</a></td><td>Usually no</td><td>Only the fastest species in large tanks stand a chance</td></tr>
      <tr><td><a href="/compatibility/electric-yellow-cichlid-and-pea-puffer/">Puffer and cichlids</a></td><td>No</td><td>Two aggressive fish, mismatched water and size</td></tr>
      <tr><td><a href="/compatibility/bristlenose-pleco-and-pea-puffer/">Puffer and pleco</a></td><td>No</td><td>Puffers bite at the pleco's flanks; plecos rasp at resting puffers</td></tr>
      <tr><td><a href="/compatibility/cherry-shrimp-and-pea-puffer/">Puffer and shrimp</a></td><td>No</td><td>Shrimp are prey, not tank mates</td></tr>
      <tr><td><a href="/compatibility/mystery-snail-and-pea-puffer/">Puffer and snails</a></td><td>Food only</td><td>Pest snails are ideal food; ornamental snails get eaten alive</td></tr>
      <tr><td><a href="/compatibility/goldfish-and-pea-puffer/">Puffer and goldfish</a></td><td>No</td><td>Wrong temperature, wrong waste load, long fins</td></tr>
      <tr><td><a href="/compatibility/angelfish-and-pea-puffer/">Puffer and angelfish</a></td><td>No</td><td>Trailing fins are the first thing a puffer tests</td></tr>
    </table></div>
    <p>Every pairing above has a full scored guide in the <a href="/compatibility/pea-puffer/">pea puffer compatibility hub</a>, and you can test any combination with the <a href="/tools/fish-compatibility-checker/">fish compatibility checker</a>.</p>

    <h2 id="snails">Snails: Food, Not Tank Mates</h2>
    <p>Pest snails &mdash; bladder, ramshorn, small Malaysian trumpet &mdash; are the single best puffer food and the main reason a puffer keeps its teeth in shape. Ornamental snails such as mystery, nerite and rabbit snails are the same thing to a puffer, just more expensive. Never add one to a puffer tank expecting it to survive. Culture pest snails separately and feed them deliberately &mdash; see the <a href="/guides/puffer-fish-care/food/">feeding guide</a>.</p>

    <h2 id="introducing">How to Introduce Tank Mates Safely</h2>
    <ol>
      <li><strong>Rearrange the hardscape first</strong> so the puffer's established territory is broken up before the newcomer arrives.</li>
      <li><strong>Add the new fish in a group</strong>, not singly &mdash; attention spread across six fish is survivable, attention on one is not.</li>
      <li><strong>Feed the puffer first</strong>, then introduce, so it is not hunting.</li>
      <li><strong>Watch for two hours, then check daily for a fortnight.</strong> Nipped fins mean the experiment has failed; act immediately.</li>
      <li><strong>Keep the backup tank cycled and running</strong> until you are sure.</li>
    </ol>
"""

MATES = {
    "slug": "tank-mates",
    "title": "Puffer Fish Tank Mates: What Can Live With a Puffer?",
    "meta_desc": "Puffer fish tank mates that actually work, species by species, plus the pairings that never do: bettas, guppies, tetras, cichlids, plecos, shrimp and goldfish.",
    "h1": "Puffer Fish Tank Mates",
    "hero_tag": "Tank Mates",
    "hero_meta": "\U0001F420 Most puffers live alone &nbsp;|&nbsp; \U0001F990 Shrimp are food &nbsp;|&nbsp; \U0001F41A Snails are food &nbsp;|&nbsp; \U0001F5C3️ 20 gal floor",
    "toc_sections": [
        ("rules", "The Five Rules"),
        ("by-species", "Which Puffers Can Share"),
        ("best", "Best Pea Puffer Mates"),
        ("never", "Pairings That Never Work"),
        ("snails", "Snails Are Food"),
        ("introducing", "Introducing Safely"),
    ],
    "body": MATES_BODY,
    "faqs": [
        ("What fish can live with a puffer fish?",
         "Very few. Pea puffers sometimes live with otocinclus, kuhli loaches or pygmy corydoras in a planted tank of 20 gallons or more. Amazon puffers do best in groups of their own kind. Fahaka, mbu, congo, avocado and adult green spotted puffers must be kept alone."),
        ("Can a puffer fish live with a betta?",
         "No. Bettas have long flowing fins that a puffer will nip, and both fish are territorial. Even in a large planted tank the pairing usually ends with a shredded betta."),
        ("Can puffer fish live with shrimp?",
         "No. Shrimp are natural puffer prey and will be hunted down, including in heavily planted tanks. The same applies to ornamental snails, which puffers eat straight out of the shell."),
        ("Do puffer fish eat snails?",
         "Yes, and they should. Pest snails such as bladder and ramshorn are the best staple food for most puffers because they provide nutrition and wear the continuously growing beak down. Ornamental snails are eaten just as readily."),
        ("Can puffer fish live with goldfish?",
         "No. Goldfish prefer cooler water, produce a very different waste load, and have long fins that a puffer will target. The pairing fails on temperature, water chemistry and temperament at once."),
        ("What are the best tank mates for a pea puffer?",
         "Otocinclus are the best option, followed by kuhli loaches and pygmy corydoras, all in a heavily planted tank of 20 gallons or more. A species-only tank of three or more pea puffers is still the safest and most rewarding setup."),
        ("Can two puffer fish live together?",
         "It depends on species. Pea puffers do well in groups of three or more but never in pairs. Amazon puffers need groups of five. Figure 8 puffers sometimes share a large tank. Fahaka, mbu, congo, hairy and adult green spotted puffers cannot."),
    ],
    "related": [
        ("/compatibility/pea-puffer/", "Pea Puffer Compatibility Hub"),
        ("/tools/fish-compatibility-checker/", "Fish Compatibility Checker"),
        ("/guides/puffer-fish-care/behavior/", "Puffer Aggression"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# BEHAVIOR / AGGRESSION
# ════════════════════════════════════════════════════════════════
BEHAV_BODY = """    <p>Puffers are the most behaviourally interesting fish in freshwater and among the least suited to community life. They recognise their keeper, solve problems, hold grudges against particular tank mates, and investigate everything with their mouth &mdash; which is where the trouble starts. Understanding what drives puffer aggression is what turns a chaotic tank into a stable one.</p>

    <h2 id="why">Why Puffers Are Aggressive</h2>
    <ul>
      <li><strong>They are predators with poor speed.</strong> A puffer cannot chase down prey, so it evolved to investigate, test and ambush. A fin drifting past is a legitimate target.</li>
      <li><strong>They hold territory.</strong> Most species claim a patch and defend it against anything that enters, including much larger fish.</li>
      <li><strong>Line of sight drives it.</strong> In an open tank a puffer can see every other fish all the time, and the constant visual contact escalates.</li>
      <li><strong>Hunger raises it.</strong> An underfed puffer is a far more aggressive puffer.</li>
    </ul>

    <h2 id="signs">Reading Puffer Body Language</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Behaviour</th><th>What it means</th></tr>
      <tr><td>Hovering, watching, following you outside the glass</td><td>Normal curiosity &mdash; usually begging</td></tr>
      <tr><td>Resting on the substrate or a leaf</td><td>Normal for most species; puffers rest often</td></tr>
      <tr><td>Darkening body, dark belly stripe (pea puffer males)</td><td>Display or breeding mood, not necessarily illness</td></tr>
      <tr><td>Head-on approach with fins flared</td><td>Territorial challenge &mdash; a fight is imminent</td></tr>
      <tr><td>Fast darting and chasing across the tank</td><td>Active aggression; separate the fish if it does not settle</td></tr>
      <tr><td>Grinding or clicking noises</td><td>Beak grinding &mdash; usually feeding-related</td></tr>
      <tr><td>Wedged in a corner, clamped fins, pale</td><td>Stress or illness &mdash; check water and see <a href="/guides/puffer-fish-care/not-eating/">not eating</a></td></tr>
    </table></div>

    <h2 id="fighting">Puffer Fish Fighting: What to Do</h2>
    <p>Fighting between puffers is normally a territory or breeding dispute. Work through this order:</p>
    <ol>
      <li><strong>Break up line of sight immediately.</strong> Add plants, wood, rock and tall cover. This alone resolves most pea puffer disputes.</li>
      <li><strong>Check the numbers.</strong> Two pea puffers is the worst configuration; three or more spreads aggression. Amazon puffers need five or more.</li>
      <li><strong>Check the sex ratio.</strong> Two or three females per male for pea puffers. Multiple males in a small tank is a recipe for constant chasing.</li>
      <li><strong>Feed more often, in smaller amounts.</strong> A well-fed puffer investigates less.</li>
      <li><strong>Rearrange the hardscape.</strong> Resetting established territories often resets the conflict too.</li>
      <li><strong>Separate.</strong> If a fish is being pinned, bitten or kept from food, remove one of them. Persistent bullying does not resolve itself.</li>
    </ol>
    <div class="callout callout-warn"><strong>Bitten fins need clean water, not medication, in the first instance.</strong> Raise water change frequency and watch for fungus or red edges. Treat only if infection appears &mdash; and at half dose, because puffers are scaleless.</div>

    <h2 id="nipping">Fin Nipping</h2>
    <p>Nipping is not usually a fight &mdash; it is feeding behaviour. A puffer that finds a trailing fin interesting will keep returning to it. Once a puffer has learned that a particular tank mate is edible, that behaviour does not stop. The only reliable fixes are removing the target fish or removing the puffer. See the <a href="/guides/puffer-fish-care/tank-mates/">tank mates guide</a> for which fish are viable in the first place.</p>

    <h2 id="glass">Glass Surfing, Pacing and Boredom</h2>
    <p>Puffers are intelligent and get visibly bored in bare tanks. Repeated pacing along the front glass usually means one of:</p>
    <ul>
      <li><strong>Nothing to do.</strong> Add caves, wood, leaf litter, and rearrange the layout occasionally.</li>
      <li><strong>Reflections.</strong> A puffer displaying at its own reflection paces constantly. Dim the room side of the tank or add a background.</li>
      <li><strong>Water quality.</strong> Test ammonia, nitrite and nitrate before assuming it is behavioural.</li>
      <li><strong>Hunger.</strong> Check the feeding schedule on the <a href="/guides/puffer-fish-care/food/">feeding page</a>.</li>
    </ul>
    <p>Enrichment works: puffers will hunt snails released at the far end of the tank, dig in sand, and investigate new decor for days.</p>

    <h2 id="handling">Handling and Bites</h2>
    <p>Large puffers bite hard enough to draw blood and break a fingernail. Never hand-feed a fahaka, mbu, congo or adult green spotted puffer &mdash; use long tongs. Never net a puffer either: a netted puffer may gulp air, which can leave it floating and unable to right itself. Move puffers in a submerged container. See <a href="/guides/puffer-fish-care/puffing-up/">puffing up and trapped air</a>.</p>
"""

BEHAV = {
    "slug": "behavior",
    "title": "Puffer Fish Aggression: Fighting, Nipping and Behaviour",
    "meta_desc": "Why puffer fish are aggressive, how to read puffer body language, how to stop fighting and fin nipping, and what glass surfing and pacing actually mean.",
    "h1": "Puffer Fish Aggression and Behaviour",
    "hero_tag": "Aggression & Behavior",
    "hero_meta": "\U0001F620 Territorial &nbsp;|&nbsp; ✂️ Fin nippers &nbsp;|&nbsp; \U0001F3E0 Line of sight drives it &nbsp;|&nbsp; \U0001F9E0 Highly intelligent",
    "toc_sections": [
        ("why", "Why They Are Aggressive"),
        ("signs", "Reading Body Language"),
        ("fighting", "Fighting: What to Do"),
        ("nipping", "Fin Nipping"),
        ("glass", "Glass Surfing & Boredom"),
        ("handling", "Handling and Bites"),
    ],
    "body": BEHAV_BODY,
    "faqs": [
        ("Why is my puffer fish so aggressive?",
         "Puffers are territorial predators that investigate everything with their mouth, and open tanks with constant line of sight escalate that behaviour. Hunger, too few hiding places, the wrong group size and an unbalanced sex ratio all make it worse."),
        ("How do I stop my puffer fish from fighting?",
         "Break up line of sight with plants, wood and rock first, then check group size and sex ratio, feed more often in smaller amounts, and rearrange the hardscape to reset territories. If one fish is being pinned or kept from food, separate them."),
        ("Why does my puffer fish nip fins?",
         "Fin nipping is feeding behaviour rather than fighting. A trailing fin looks like prey, and once a puffer learns a particular tank mate is edible the habit does not stop. The only reliable fix is separating the two fish."),
        ("Is it normal for a puffer fish to rest on the bottom?",
         "Yes. Most puffers rest on the substrate, on leaves or wedged against decor, and burrowing species such as the congo puffer spend most of the day buried. It only signals a problem when combined with clamped fins, pale colour or refusing food."),
        ("Why is my puffer fish swimming against the glass?",
         "Usually boredom in a sparse tank, or displaying at its own reflection. Add caves, wood and leaf litter, dim the room side of the tank, and test ammonia, nitrite and nitrate to rule out a water quality problem."),
        ("Do puffer fish bite people?",
         "Large species can and do. A fahaka or mbu bite draws blood and can break a fingernail, so always feed with long tongs and never put a hand in the tank at the same end as the fish."),
    ],
    "related": [
        ("/guides/puffer-fish-care/tank-mates/", "Puffer Tank Mates"),
        ("/guides/puffer-fish-care/not-eating/", "Puffer Not Eating"),
        ("/guides/puffer-fish-care/puffing-up/", "Puffing Up & Bloating"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# BREEDING & SEXING
# ════════════════════════════════════════════════════════════════
BREED_BODY = """    <p>Puffers are among the hardest aquarium fish to breed, and for most species it has never been done reliably in captivity. The single exception is the pea puffer, which spawns readily in a planted tank. Almost every other puffer you can buy &mdash; green spotted, figure 8, fahaka, mbu, Amazon, congo &mdash; is wild-caught, which is why sexing and breeding information for them is so thin.</p>

    <h2 id="sexing">Male vs Female Puffer Fish</h2>
    <p>Most puffers show no reliable external sexual dimorphism at all. The species where you can tell:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Can you sex it?</th><th>How</th></tr>
      <tr><td>Pea / dwarf puffer</td><td>Yes, from ~8 months</td><td>Males: dark belly stripe, iridescent wrinkle lines behind the eye, slimmer, brighter yellow. Females: rounder, olive, no stripe</td></tr>
      <tr><td>Red eye puffer</td><td>Yes</td><td>Males have a red-orange tail and a dark ventral ridge; females are patterned brown with a plain tail</td></tr>
      <tr><td>Figure 8 puffer</td><td>No</td><td>No reliable external difference</td></tr>
      <tr><td>Green spotted puffer</td><td>No</td><td>No reliable external difference</td></tr>
      <tr><td>Amazon puffer</td><td>Difficult</td><td>Mature females are slightly deeper-bodied; not reliable</td></tr>
      <tr><td>Fahaka / mbu puffer</td><td>No</td><td>Only distinguishable by behaviour during rare spawning attempts</td></tr>
      <tr><td>Marine puffers</td><td>Mostly no</td><td><em>Canthigaster</em> tobies show slight fin and colour differences in mature males</td></tr>
    </table></div>

    <h2 id="pea-breeding">Breeding Pea Puffers Step by Step</h2>
    <p>The pea puffer is the realistic project, and captive-bred stock genuinely matters: wild pea puffers come from a small area of south-west India under heavy collection pressure.</p>
    <ol>
      <li><strong>Set up a group.</strong> One male to two or three females in a 10&ndash;20 gallon planted tank at 78&ndash;80&deg;F, pH 7.0&ndash;7.6.</li>
      <li><strong>Condition for two to three weeks</strong> on live blackworms, small snails and frozen bloodworms fed twice daily.</li>
      <li><strong>Provide dense java moss</strong> or a similar fine-leaved plant across at least a third of the floor.</li>
      <li><strong>Watch for courtship.</strong> The male darkens his belly stripe, displays and drives the female into the moss.</li>
      <li><strong>Eggs are laid singly</strong> among the moss, roughly 5&ndash;15 per spawn, and are not guarded.</li>
      <li><strong>Remove the adults or move the moss</strong> to a separate container &mdash; both parents eat eggs and fry.</li>
      <li><strong>Eggs hatch in about five days</strong> at 79&deg;F. Fry are tiny and remain on their yolk sac for a further two to three days.</li>
      <li><strong>Feed infusoria and vinegar eels</strong> for the first week, then microworms, then baby brine shrimp from around week two.</li>
      <li><strong>Keep the fry tank spotless.</strong> Small daily water changes with a rigid airline; fry are intolerant of any ammonia.</li>
    </ol>

    <h2 id="eggs">Puffer Fish Eggs and Fry</h2>
    <ul>
      <li><strong>Appearance:</strong> pea puffer eggs are clear to pale amber and roughly 1 mm across &mdash; easy to miss in moss.</li>
      <li><strong>Hatch time:</strong> about five days at 79&deg;F, longer in cooler water.</li>
      <li><strong>Fry size:</strong> under 2 mm at hatch, which is why infusoria rather than brine shrimp is the correct first food.</li>
      <li><strong>Growth:</strong> recognisably puffer-shaped by three weeks, taking baby snails by two months, adult size and sexable at around eight months.</li>
      <li><strong>Survival:</strong> expect losses. A first spawn producing five or six juveniles is a normal result.</li>
    </ul>

    <h2 id="other">Breeding Other Puffer Species</h2>
    <p>Realistic expectations for the rest:</p>
    <ul>
      <li><strong>Green spotted and figure 8 puffers:</strong> not bred in home aquariums. All stock is wild-caught from estuaries, and reproducing the migratory salinity cycle is beyond a home setup.</li>
      <li><strong>Amazon puffers:</strong> spawn seasonally in the wild with flood cycles; occasional aquarium spawns are reported but raising fry is rare.</li>
      <li><strong>Fahaka puffers:</strong> a handful of documented captive spawns, all in very large tanks. Males guard eggs on a flat surface.</li>
      <li><strong>Congo and hairy puffers:</strong> essentially unrecorded in captivity.</li>
      <li><strong>Marine puffers:</strong> pelagic spawners; larvae need a rotifer and copepod culture chain that is impractical outside a dedicated facility.</li>
    </ul>

    <h2 id="pregnant">Is My Puffer Pregnant?</h2>
    <p>No &mdash; puffers are egg scatterers, not livebearers, so there is no pregnancy. A female carrying eggs looks fuller for a few days before spawning and then returns to normal. A puffer that stays swollen has a different problem: constipation, internal parasites, dropsy or trapped air. Work through the <a href="/guides/puffer-fish-care/puffing-up/">bloating and puffing up page</a>.</p>
"""

BREED = {
    "slug": "breeding",
    "title": "Puffer Fish Breeding: Sexing, Eggs and Raising Fry",
    "meta_desc": "Puffer fish breeding and sexing: telling male from female pea puffers, a step-by-step spawning method, egg and fry care, and which species never breed.",
    "h1": "Puffer Fish Breeding and Sexing",
    "hero_tag": "Breeding & Sexing",
    "hero_meta": "\U0001F95A Pea puffers only &nbsp;|&nbsp; \U0001F5D3️ Hatch ~5 days &nbsp;|&nbsp; \U0001F41B Infusoria first &nbsp;|&nbsp; ⚧ Most species unsexable",
    "toc_sections": [
        ("sexing", "Male vs Female"),
        ("pea-breeding", "Breeding Pea Puffers"),
        ("eggs", "Eggs and Fry"),
        ("other", "Other Species"),
        ("pregnant", "Is My Puffer Pregnant?"),
    ],
    "body": BREED_BODY,
    "faqs": [
        ("How can you tell a male puffer fish from a female?",
         "Only in a few species. Mature male pea puffers have a dark stripe down the centre of the belly, iridescent wrinkle lines behind the eye, a slimmer body and brighter yellow colour. Green spotted, figure 8, fahaka and mbu puffers show no reliable external differences."),
        ("Can puffer fish breed in an aquarium?",
         "Pea puffers breed readily in a planted tank. Fahaka puffers have spawned a handful of times in very large tanks. Green spotted, figure 8, congo and marine puffers are not bred in home aquariums, so the stock in shops is wild-caught."),
        ("How do you breed pea puffers?",
         "Keep one male to two or three females at 78 to 80F in a planted tank, condition them on live blackworms and snails for two to three weeks, and provide dense java moss. The male drives the female into the moss to spawn, and eggs must be separated from the adults."),
        ("How long do puffer fish eggs take to hatch?",
         "Pea puffer eggs hatch in about five days at 79F, longer in cooler water. The fry stay on their yolk sac for a further two to three days before needing infusoria or vinegar eels as a first food."),
        ("What do baby puffer fish eat?",
         "Infusoria and vinegar eels for the first week, then microworms, then baby brine shrimp from around week two. By two months they can take crushed or newly hatched pest snails."),
        ("Can a puffer fish be pregnant?",
         "No. Puffers scatter eggs rather than bearing live young. A female looks fuller for a few days before spawning, but a puffer that stays swollen has constipation, internal parasites, dropsy or trapped air instead."),
    ],
    "related": [
        ("/guides/puffer-fish-care/pea-puffer/", "Pea Puffer Care"),
        ("/guides/puffer-fish-care/puffing-up/", "Bloating & Puffing Up"),
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# DISEASES
# ════════════════════════════════════════════════════════════════
DIS_BODY = """    <p>Everything about treating a sick puffer follows from one fact: <strong>puffers have no scales</strong>. Medication crosses their skin far faster than it does a scaled fish, so standard doses of copper, formalin and some organophosphates can do more damage than the disease. On top of that, most large puffers are wild-caught and arrive carrying internal parasites. Quarantine and half-dose everything.</p>

    <div class="callout callout-warn"><strong>Medication rule for puffers.</strong> Unless a product is explicitly labelled safe for scaleless fish, use half the stated dose, treat in a bare quarantine tank, and add extra aeration. Avoid copper entirely where an alternative exists.</div>

    <h2 id="common">Common Puffer Diseases at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Disease</th><th>Signs</th><th>First action</th></tr>
      <tr><td>Ich (white spot)</td><td>Salt-grain white spots on body and fins, flashing</td><td>Raise temperature to 82&deg;F, half-dose ich treatment, extra aeration</td></tr>
      <tr><td>Internal parasites / worms</td><td>Thin fish that eats, white stringy faeces, sunken belly</td><td>Praziquantel or levamisole, then metronidazole</td></tr>
      <tr><td>Fin rot</td><td>Ragged, receding, red- or white-edged fins</td><td>Large water changes; antibacterial only if it progresses</td></tr>
      <tr><td>Cloudy eye</td><td>Milky film over one or both eyes</td><td>Test water; 50% change; check for injury</td></tr>
      <tr><td>Flukes (gill and skin)</td><td>Flashing, rapid gilling, clamped fins, no visible spots</td><td>Praziquantel &mdash; well tolerated by puffers</td></tr>
      <tr><td>Bacterial infection / ulcers</td><td>Red sores, open lesions, grey patches</td><td>Quarantine, clean water, half-dose antibacterial</td></tr>
      <tr><td>Dropsy</td><td>Swelling with raised, pinecone-like skin</td><td>Poor prognosis; isolate, Epsom salt bath, review water</td></tr>
      <tr><td>Constipation</td><td>Swollen belly, no faeces, still active</td><td>Fast 2&ndash;3 days, then feed shelled prey</td></tr>
    </table></div>
    <p>Symptom-indexed guides also exist for <a href="/aquarium-fish-diseases/dwarf-puffer-diseases/">dwarf puffers</a>, <a href="/aquarium-fish-diseases/figure-eight-puffer-diseases/">figure eight puffers</a> and <a href="/aquarium-fish-diseases/porcupine-puffer-diseases/">porcupine puffers</a>.</p>

    <h2 id="ich">Puffer Fish White Spots (Ich)</h2>
    <p>Ich looks the same on a puffer as on any fish &mdash; white spots the size of salt grains, plus flashing against decor &mdash; but the treatment differs.</p>
    <ol>
      <li><strong>Raise the temperature to 82&deg;F</strong> over 24 hours and add an airstone. This speeds the parasite's life cycle so the free-swimming stage is exposed to treatment sooner.</li>
      <li><strong>Use a half dose</strong> of a malachite green or formalin-free ich product, or salt at 1 tablespoon per 5 gallons for freshwater species that tolerate it.</li>
      <li><strong>Brackish species:</strong> raising salinity toward 1.010&ndash;1.012 is often enough on its own.</li>
      <li><strong>Treat for the full course</strong> plus three days after the last visible spot; the parasite is only vulnerable between hosts.</li>
      <li><strong>Never use copper on a puffer</strong> if any alternative is available.</li>
    </ol>

    <h2 id="parasites">Internal Parasites in Wild-Caught Puffers</h2>
    <p>Assume every wild-caught puffer &mdash; which means practically every fahaka, mbu, congo, hairy, figure 8, green spotted and Amazon puffer &mdash; has internal worms. The classic picture is a fish with a healthy appetite that stays thin, passing white stringy faeces.</p>
    <ul>
      <li><strong>Quarantine every new puffer for four weeks</strong> in a bare tank with a cycled sponge filter.</li>
      <li><strong>Praziquantel</strong> for flatworms and flukes, dosed in-tank, repeated after seven days.</li>
      <li><strong>Levamisole</strong> for roundworms, with a large water change and gravel vacuum 24 hours after dosing.</li>
      <li><strong>Metronidazole</strong> for protozoan infections, ideally in food if the fish is still eating.</li>
      <li><strong>Feed well throughout.</strong> A dewormed fish needs to rebuild condition.</li>
    </ul>

    <h2 id="finrot">Fin Rot and Bacterial Problems</h2>
    <p>Fin rot in a puffer tank is usually a consequence of two things: nipped fins from a tank mate dispute, and nitrate that has been allowed to climb. Fix both before reaching for medication.</p>
    <ol>
      <li>Test ammonia, nitrite and nitrate. Change 50% of the water and repeat daily for three days.</li>
      <li>Remove or separate whichever fish is doing the biting &mdash; see the <a href="/guides/puffer-fish-care/behavior/">aggression page</a>.</li>
      <li>If the edges are red or the erosion advances into the fin body, use a half-dose antibacterial in quarantine.</li>
      <li>Fins regrow clear and then re-pigment; expect several weeks.</li>
    </ol>

    <h2 id="eye">Cloudy Eye</h2>
    <p>A milky film over the eye is a symptom, not a disease. In puffers the usual causes are poor water quality, a physical scrape (very common in a scaleless fish that rubs on decor), or a bacterial infection following one of those. Test the water, do a large change, remove sharp decor, and only medicate if the eye also swells or the fish stops eating.</p>

    <h2 id="quarantine">The Puffer Quarantine Protocol</h2>
    <ol>
      <li><strong>Bare tank, cycled sponge filter, heater, one hiding place.</strong> Sized for the fish: 10 gallons for a pea puffer, 40 for a juvenile fahaka.</li>
      <li><strong>Four weeks minimum.</strong> Observe feeding, faeces and breathing daily.</li>
      <li><strong>Deworm in week one</strong> with praziquantel, then levamisole in week two if the fish is wild-caught.</li>
      <li><strong>Do not medicate prophylactically for ich</strong> &mdash; watch instead, and treat if it appears.</li>
      <li><strong>Match water parameters</strong> to the display tank, including salinity for brackish species, before moving the fish.</li>
    </ol>
    <p>Test your parameters against the targets on the <a href="/guides/puffer-fish-care/water-parameters/">water parameters page</a> or with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>
"""

DIS = {
    "slug": "diseases",
    "title": "Puffer Fish Diseases: Ich, Parasites, Fin Rot and Cures",
    "meta_desc": "Puffer fish diseases and treatments: white spot, internal parasites, fin rot and cloudy eye, plus half-dose medication rules for scaleless fish.",
    "h1": "Puffer Fish Diseases and Parasites",
    "hero_tag": "Diseases & Parasites",
    "hero_meta": "\U0001FA7A Scaleless &nbsp;|&nbsp; ½ Half-dose meds &nbsp;|&nbsp; \U0001F6AB No copper &nbsp;|&nbsp; \U0001F9EB 4-week quarantine",
    "toc_sections": [
        ("common", "Diseases at a Glance"),
        ("ich", "White Spots (Ich)"),
        ("parasites", "Internal Parasites"),
        ("finrot", "Fin Rot"),
        ("eye", "Cloudy Eye"),
        ("quarantine", "Quarantine Protocol"),
    ],
    "body": DIS_BODY,
    "faqs": [
        ("Why does my puffer fish have white spots?",
         "Salt-grain white spots with flashing against decor is ich. Raise the temperature to 82F with extra aeration and use a half dose of a copper-free ich treatment, because puffers are scaleless and absorb medication quickly. For brackish species, raising salinity to 1.010-1.012 often clears it alone."),
        ("Can you use copper on a puffer fish?",
         "Avoid it wherever possible. Puffers have no scales and absorb copper rapidly, which causes skin damage and appetite loss. Use hyposalinity, chloroquine phosphate or praziquantel instead, depending on the parasite."),
        ("How do I treat internal parasites in a puffer?",
         "Praziquantel for flatworms and flukes, repeated after seven days; levamisole for roundworms with a large water change and gravel vacuum 24 hours later; and metronidazole for protozoan infections. Assume every wild-caught puffer needs a course during quarantine."),
        ("Why does my puffer fish have fin rot?",
         "Usually nipped fins from a tank mate dispute combined with rising nitrate. Test the water, do 50 percent changes for three days, separate the biting fish, and use a half-dose antibacterial only if the edges turn red or the erosion advances."),
        ("What causes cloudy eye in puffer fish?",
         "Poor water quality, a physical scrape on decor, or a bacterial infection following either. Puffers have no scales and scrape easily, so test the water, do a large change, remove sharp decor, and medicate only if the eye swells or the fish stops eating."),
        ("How long should I quarantine a new puffer fish?",
         "Four weeks in a bare tank with a cycled sponge filter, a heater and one hiding place. Deworm wild-caught fish with praziquantel in week one and levamisole in week two, and match water parameters to the display tank before moving the fish."),
    ],
    "related": [
        ("/guides/puffer-fish-care/not-eating/", "Puffer Not Eating"),
        ("/guides/puffer-fish-care/swimming-problems/", "Swimming & Breathing"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/aquarium-fish-diseases/dwarf-puffer-diseases/", "Dwarf Puffer Diseases"),
    ],
}


# ════════════════════════════════════════════════════════════════
# NOT EATING / HIDING
# ════════════════════════════════════════════════════════════════
EAT_BODY = """    <p>A puffer that stops eating is a genuine warning sign, because a healthy puffer begs constantly. The good news is that the causes fall into a short, checkable list. Work through it in order &mdash; the first three explain the large majority of cases.</p>

    <h2 id="checklist">The Five-Minute Checklist</h2>
    <ol>
      <li><strong>Test the water.</strong> Ammonia, nitrite, nitrate, temperature, and specific gravity for brackish species. Ammonia above zero stops a puffer eating within a day.</li>
      <li><strong>Look at the mouth.</strong> If the beak protrudes past the lips, the fish physically cannot feed &mdash; see the <a href="/guides/puffer-fish-care/teeth/">teeth page</a>.</li>
      <li><strong>Count the days since it arrived.</strong> New puffers commonly refuse food for three to seven days.</li>
      <li><strong>Check the faeces.</strong> White and stringy means internal parasites.</li>
      <li><strong>Check for a bully.</strong> A puffer being chased off food hides and thins out.</li>
    </ol>

    <h2 id="causes">Why a Puffer Fish Stops Eating</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>Other signs</th><th>Fix</th></tr>
      <tr><td>New arrival stress</td><td>Hiding, pale, otherwise healthy</td><td>Dim lights, offer live blackworms, wait 3&ndash;7 days</td></tr>
      <tr><td>Ammonia or nitrite</td><td>Gasping, red gills, clamped fins</td><td>50% water change now, then daily until zero</td></tr>
      <tr><td>Overgrown teeth</td><td>Chases food, cannot take or crush it</td><td>Soft food short term; trimming if advanced</td></tr>
      <tr><td>Internal parasites</td><td>Thin body, white stringy faeces</td><td>Praziquantel then levamisole in quarantine</td></tr>
      <tr><td>Wrong salinity</td><td>Brackish species, dull colour, lethargy</td><td>Correct SG gradually &mdash; see <a href="/guides/puffer-fish-care/water-parameters/">salinity guide</a></td></tr>
      <tr><td>Wrong food</td><td>Interested but will not take pellets or flake</td><td>Offer live or frozen; puffers rarely take dry food</td></tr>
      <tr><td>Bullying</td><td>Hiding, clamped fins, nipped edges</td><td>Separate; see <a href="/guides/puffer-fish-care/behavior/">aggression</a></td></tr>
      <tr><td>Temperature too low</td><td>Sluggish, slow to respond</td><td>Bring to 77&ndash;80&deg;F gradually</td></tr>
      <tr><td>Constipation</td><td>Swollen belly, no faeces</td><td>Fast 2&ndash;3 days, then shelled prey</td></tr>
    </table></div>

    <h2 id="new">Getting a New Puffer to Eat</h2>
    <ol>
      <li><strong>Dim the tank and the room</strong> for the first few days and keep traffic past the glass low.</li>
      <li><strong>Offer live food.</strong> Live blackworms break more hunger strikes than anything else; live pest snails work well for pea and figure 8 puffers.</li>
      <li><strong>Feed at the same time each day</strong> and leave the room. Many new puffers will not eat while watched.</li>
      <li><strong>Target-feed with tweezers or a pipette</strong> so food reaches the fish rather than the substrate.</li>
      <li><strong>Remove uneaten food after an hour</strong> so it does not foul the water and make the problem worse.</li>
      <li><strong>Give it a week</strong> before escalating to medication. Most healthy new puffers start eating within seven days.</li>
    </ol>

    <h2 id="hiding">Puffer Fish Hiding</h2>
    <p>Some hiding is normal. Congo and hairy puffers spend most of the day buried or wedged, and every puffer has a favourite corner. It becomes a symptom when it is new behaviour, or when it comes with clamped fins, pale colour, refusing food or rapid gilling.</p>
    <ul>
      <li><strong>New tank:</strong> normal for the first week. Add more cover rather than less &mdash; a fish with hiding places explores sooner than one with none.</li>
      <li><strong>Sudden hiding in an established tank:</strong> test water first, then look for a tank mate that has started chasing.</li>
      <li><strong>Hiding plus pale colour:</strong> treat as illness &mdash; see the <a href="/guides/puffer-fish-care/diseases/">diseases page</a>.</li>
    </ul>

    <h2 id="bottom">Puffer Lying on the Bottom</h2>
    <p>Resting on the substrate is normal puffer behaviour &mdash; they have no swim-bladder-driven need to hover and they park regularly. Distinguish normal resting from a problem:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Normal</th><th>Concerning</th></tr>
      <tr><td>Upright, fins relaxed, alert eyes</td><td>Leaning, rolling or on its side</td></tr>
      <tr><td>Moves off readily when you approach</td><td>Unresponsive or struggling to lift off</td></tr>
      <tr><td>Still eating normally</td><td>Refusing food alongside it</td></tr>
      <tr><td>Normal colour</td><td>Pale, blotchy or very dark</td></tr>
      <tr><td>Steady gill movement</td><td>Rapid gilling or gasping</td></tr>
    </table></div>
    <p>If the fish is on its side or struggling to stay off the bottom, go to the <a href="/guides/puffer-fish-care/swimming-problems/">swimming and breathing page</a>.</p>
"""

EAT = {
    "slug": "not-eating",
    "title": "Puffer Fish Not Eating, Hiding or Lying on the Bottom",
    "meta_desc": "Why a puffer fish stops eating: water quality, overgrown teeth, internal parasites, new-arrival stress and bullying, plus how to get a new puffer feeding again.",
    "h1": "Puffer Fish Not Eating and Hiding",
    "hero_tag": "Not Eating & Hiding",
    "hero_meta": "\U0001F6AB Check water first &nbsp;|&nbsp; \U0001F9B7 Then the beak &nbsp;|&nbsp; \U0001FAB1 Live blackworms work &nbsp;|&nbsp; \U0001F4C5 Give it 7 days",
    "toc_sections": [
        ("checklist", "Five-Minute Checklist"),
        ("causes", "Why They Stop Eating"),
        ("new", "Getting a New Puffer to Eat"),
        ("hiding", "Puffer Hiding"),
        ("bottom", "Lying on the Bottom"),
    ],
    "body": EAT_BODY,
    "faqs": [
        ("Why is my puffer fish not eating?",
         "Check water quality first, then the beak. Ammonia or nitrite above zero, overgrown teeth that stop the fish taking food, internal parasites, new-arrival stress, wrong salinity for a brackish species and bullying account for almost every case."),
        ("How long can a puffer fish go without eating?",
         "A healthy adult puffer can go one to two weeks without lasting harm, and new arrivals commonly refuse food for three to seven days. Small species such as pea puffers have less reserve and should be eating within a week."),
        ("How do I get my new puffer fish to eat?",
         "Dim the lights, keep traffic past the tank low, and offer live blackworms or live pest snails. Feed at the same time daily and leave the room, target-feed with tweezers, and remove uneaten food after an hour."),
        ("Why is my puffer fish hiding all the time?",
         "Some hiding is normal, especially in a new tank or for burrowing species. Sudden hiding in an established tank usually means a water quality problem or a tank mate that has started chasing. Pale colour or clamped fins alongside it points to illness."),
        ("Is it normal for a puffer fish to lie on the bottom?",
         "Yes. Puffers rest on the substrate regularly and burrowing species stay there most of the day. It is only a problem if the fish leans or rolls onto its side, cannot lift off, is refusing food, looks pale, or is gilling rapidly."),
        ("My puffer eats but stays thin, what is wrong?",
         "That pattern is the classic sign of internal parasites, particularly in wild-caught fish. Look for white stringy faeces and treat with praziquantel followed by levamisole in a quarantine tank, feeding well throughout."),
    ],
    "related": [
        ("/guides/puffer-fish-care/teeth/", "Puffer Teeth & Trimming"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
    ],
}


# ════════════════════════════════════════════════════════════════
# PUFFING UP / BLOATING
# ════════════════════════════════════════════════════════════════
PUFF_BODY = """    <p>Inflating is what puffers are famous for, and it is the behaviour most misunderstood by new keepers. A puffer does not puff up because it is happy or showing off. It is a last-resort defence that costs the fish energy and carries real risk &mdash; and a puffer that inflates regularly in your tank is telling you something is wrong.</p>

    <h2 id="how">How Puffing Up Works</h2>
    <p>A puffer has an extremely elastic stomach diverticulum and skin that can stretch to several times its resting area. Threatened, it gulps water rapidly into that chamber until the body becomes a rigid sphere, often two to three times its normal volume, which makes it too large for a predator's mouth. Species with spines &mdash; porcupine puffers and burrfish &mdash; erect them at the same time.</p>
    <ul>
      <li><strong>It is water, not air.</strong> A healthy puffer inflates with water and deflates by expelling it through the mouth and gills within seconds.</li>
      <li><strong>Puffers have no ribs and no pelvic fins</strong>, which is what allows the body to expand that far.</li>
      <li><strong>Inflation is stressful.</strong> It takes energy, and repeated inflation is linked to reduced appetite and susceptibility to infection.</li>
    </ul>

    <h2 id="never-air">Never Make a Puffer Puff Up</h2>
    <div class="callout callout-warn"><strong>Do not net a puffer, and never lift one out of the water.</strong> A puffer that inflates in air gulps air instead of water, and air is far harder to expel. A fish with trapped air floats at the surface, cannot right itself, and may not recover. Move puffers in a submerged container or a bag, always keeping the fish underwater.</div>
    <p>The same applies to poking, chasing with a net, or deliberately provoking the fish for a photograph. If someone tells you it is harmless, it is not.</p>

    <h2 id="trapped">If a Puffer Has Swallowed Air</h2>
    <p>Signs: the fish floats at the surface, often on its side or upside down, and cannot swim down despite trying. Act quickly.</p>
    <ol>
      <li><strong>Hold the fish underwater</strong> in a container, gently, head slightly down.</li>
      <li><strong>Rock it slowly side to side</strong> and stroke along the belly from the throat backwards to encourage the air out through the mouth. Many fish release the air within a minute or two.</li>
      <li><strong>Lower the water level</strong> in the tank afterwards so the fish does not have to fight to reach the bottom, and reduce flow.</li>
      <li><strong>Keep the water pristine</strong> and dim the tank while it recovers.</li>
      <li><strong>If the fish is still trapped after several attempts</strong>, contact an aquatic vet &mdash; needle aspiration is a veterinary procedure, not a home one.</li>
    </ol>

    <h2 id="bloated">Puffed Up vs Bloated: Telling Them Apart</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Inflated (defensive)</th><th>Bloated (health problem)</th></tr>
      <tr><td>Sudden, whole body becomes spherical</td><td>Gradual, mostly the belly</td></tr>
      <tr><td>Deflates within seconds to minutes</td><td>Persists for days</td></tr>
      <tr><td>Triggered by a visible threat</td><td>No obvious trigger</td></tr>
      <tr><td>Fish behaves normally afterwards</td><td>Lethargy, refusing food, changed faeces</td></tr>
      <tr><td>Skin smooth and taut</td><td>Scaleless skin may look stretched or, in dropsy, raised</td></tr>
    </table></div>

    <h2 id="causes">Why Is My Puffer Fish Bloated?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>Signs</th><th>Action</th></tr>
      <tr><td>Overfeeding</td><td>Full round belly after a meal, otherwise normal</td><td>Normal &mdash; reduce portion size next feed</td></tr>
      <tr><td>Constipation</td><td>Swollen for days, no faeces, still active</td><td>Fast 2&ndash;3 days, then shelled food; Epsom salt at 1 tbsp per 5 gal</td></tr>
      <tr><td>Trapped air</td><td>Floating, cannot swim down</td><td>See the trapped air steps above</td></tr>
      <tr><td>Internal parasites</td><td>Swelling with weight loss elsewhere, stringy faeces</td><td>Praziquantel then levamisole &mdash; see <a href="/guides/puffer-fish-care/diseases/">diseases</a></td></tr>
      <tr><td>Dropsy</td><td>Swelling with raised, pinecone-like skin, lethargy</td><td>Isolate, Epsom bath, review water; prognosis poor</td></tr>
      <tr><td>Chronic wrong salinity</td><td>Brackish species in freshwater, gradual swelling</td><td>Correct the salinity gradually</td></tr>
      <tr><td>Tumour or organ enlargement</td><td>One-sided swelling, slow progression</td><td>Supportive care; consult an aquatic vet</td></tr>
    </table></div>

    <h2 id="constipation">Treating Constipation in a Puffer</h2>
    <ol>
      <li><strong>Fast the fish for two to three days.</strong> Puffers handle this easily.</li>
      <li><strong>Confirm the water is clean</strong> &mdash; ammonia and nitrite at zero, nitrate under 20 ppm.</li>
      <li><strong>Add Epsom salt (magnesium sulphate)</strong> at one tablespoon per 5 gallons, dissolved in change water first. This is a muscle relaxant, not aquarium salt.</li>
      <li><strong>Hold the temperature at 78&ndash;80&deg;F</strong> to keep the metabolism moving.</li>
      <li><strong>Resume feeding with shelled prey</strong> rather than bloodworms &mdash; a diet of soft food is a common cause in the first place.</li>
    </ol>
    <p>If the swelling persists past a week of this, treat it as an internal problem rather than constipation.</p>
"""

PUFF = {
    "slug": "puffing-up",
    "title": "Puffer Fish Puffing Up and Bloating: Causes and Fixes",
    "meta_desc": "Why puffer fish puff up, why you should never make one inflate, how to release trapped air, and how to tell defensive inflation from bloating or dropsy.",
    "h1": "Puffer Fish Puffing Up and Bloating",
    "hero_tag": "Puffing Up & Bloating",
    "hero_meta": "\U0001F388 Defence, not display &nbsp;|&nbsp; \U0001F6AB Never net a puffer &nbsp;|&nbsp; \U0001F4A8 Air is the danger",
    "toc_sections": [
        ("how", "How Puffing Up Works"),
        ("never-air", "Never Force It"),
        ("trapped", "Swallowed Air"),
        ("bloated", "Puffed vs Bloated"),
        ("causes", "Why Is It Bloated?"),
        ("constipation", "Treating Constipation"),
    ],
    "body": PUFF_BODY,
    "faqs": [
        ("Why do puffer fish puff up?",
         "It is a last-resort defence. The fish gulps water into a highly elastic stomach chamber until its body becomes a rigid sphere two to three times normal volume, too large for a predator to swallow. It is stressful and costly, not a display of contentment."),
        ("Is it bad for a puffer fish to puff up?",
         "Yes, repeatedly. Inflation costs energy and is linked to reduced appetite and infection risk. A puffer that inflates often in your tank is signalling stress from a tank mate, handling or poor conditions."),
        ("What happens if a puffer fish puffs up with air?",
         "Air is far harder to expel than water, so the fish floats at the surface and cannot swim down. This usually happens when a puffer is lifted out of the water in a net. Hold the fish underwater head slightly down and rock it gently to release the air."),
        ("How do you get air out of a puffer fish?",
         "Hold it underwater in a container with the head slightly down, rock it slowly side to side and stroke along the belly from the throat backwards to encourage the air out of the mouth. Lower the tank water level afterwards and reduce flow while it recovers."),
        ("Why is my puffer fish bloated?",
         "Overfeeding causes a normal full belly that resolves. Persistent swelling points to constipation, trapped air, internal parasites, dropsy or long-term exposure to the wrong salinity. Fast the fish two to three days and check the water before treating."),
        ("Should I net my puffer fish?",
         "No. Netting risks lifting the fish clear of the water, and a puffer that inflates in air can end up with trapped air it cannot expel. Move puffers in a submerged container or bag, keeping the fish underwater at all times."),
    ],
    "related": [
        ("/guides/puffer-fish-care/swimming-problems/", "Swimming & Breathing"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/puffer-fish-care/food/", "Puffer Food & Feeding"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# COLOR CHANGE
# ════════════════════════════════════════════════════════════════
COLOR_BODY = """    <p>Puffers change colour more than almost any other aquarium fish, and most of it is completely normal. They darken when annoyed, pale when relaxed, shift pattern when hunting, and mottle to match the substrate. The skill is telling mood-driven colour change from the kind that signals a problem, and the deciding factor is almost always what else the fish is doing.</p>

    <h2 id="normal">Normal Colour Changes</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Change</th><th>Usual meaning</th></tr>
      <tr><td>Darkening for minutes to hours, then back</td><td>Mood: irritation, territorial display, or being watched</td></tr>
      <tr><td>Dark belly stripe on a male pea puffer</td><td>Breeding condition &mdash; a sexing feature, not illness</td></tr>
      <tr><td>Mottling and blotching</td><td>Camouflage against substrate; strong in congo and hairy puffers</td></tr>
      <tr><td>Paling at night</td><td>Normal sleep colouration in most species</td></tr>
      <tr><td>Darkening during feeding</td><td>Hunting excitement</td></tr>
      <tr><td>Gradual colour deepening over months</td><td>Maturity &mdash; many puffers intensify as adults</td></tr>
    </table></div>

    <h2 id="black">Puffer Fish Turning Black</h2>
    <p>A puffer that goes dark and stays dark for more than a few hours is worth investigating. Common causes, most likely first:</p>
    <ol>
      <li><strong>Stress.</strong> A new tank, a new tank mate, a rearranged layout, or a chasing dispute. Look at what changed in the last 48 hours.</li>
      <li><strong>Water quality.</strong> Test ammonia, nitrite and nitrate. Chronic nitrate above 40 ppm produces a persistently dark, listless fish.</li>
      <li><strong>Wrong salinity.</strong> A brackish species in freshwater darkens and dulls over weeks &mdash; see the <a href="/guides/puffer-fish-care/water-parameters/">salinity guide</a>.</li>
      <li><strong>Temperature.</strong> Both too cold and too warm produce colour changes plus behaviour changes.</li>
      <li><strong>Illness.</strong> Dark colour with clamped fins, rapid gilling or refusing food is a symptom, not a mood &mdash; go to the <a href="/guides/puffer-fish-care/diseases/">diseases page</a>.</li>
    </ol>
    <div class="callout"><strong>Rule of thumb.</strong> Dark plus normal behaviour is mood. Dark plus clamped fins, hiding or not eating is a health problem. The behaviour tells you more than the colour does.</div>

    <h2 id="pale">Puffer Fish Losing Colour or Turning Pale</h2>
    <p>Paling is the more concerning direction, because a healthy relaxed puffer is pale only briefly. Sustained loss of colour usually means:</p>
    <ul>
      <li><strong>Poor water quality</strong> &mdash; test first, change 50% of the water.</li>
      <li><strong>Poor diet.</strong> A puffer fed only bloodworms loses colour over months. Rotate shelled prey, mysis, krill and varied frozen food &mdash; see the <a href="/guides/puffer-fish-care/food/">feeding page</a>.</li>
      <li><strong>Internal parasites.</strong> Pale plus thin plus stringy white faeces is the classic combination.</li>
      <li><strong>Chronic stress.</strong> Constant harassment leaves a fish permanently washed out.</li>
      <li><strong>Age.</strong> Old puffers mute gradually over months. Ageing is slow; illness is fast.</li>
      <li><strong>Blotchy white patches</strong> on a scaleless fish can be a fungal or bacterial skin problem rather than a colour change &mdash; look closely for texture.</li>
    </ul>

    <h2 id="substrate">Substrate and Lighting Effects</h2>
    <p>Puffers adjust to their background. The same fish looks dark over black sand and pale over white sand, and bright overhead lighting washes colour out while dimmer, warmer light brings it back. Before troubleshooting a colour change, check whether you changed the substrate, the background, the lighting or the position of the tank. Adding floating plants or dimming the light often restores a fish that suddenly looks washed out.</p>

    <h2 id="action">When to Act</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Situation</th><th>Action</th></tr>
      <tr><td>Colour shifts and returns within hours</td><td>Normal &mdash; no action</td></tr>
      <tr><td>Persistently dark, otherwise normal</td><td>Test water; look for a stressor</td></tr>
      <tr><td>Dark plus clamped fins or not eating</td><td>Treat as illness &mdash; test water, quarantine if needed</td></tr>
      <tr><td>Pale and thin over weeks</td><td>Check for internal parasites; review diet</td></tr>
      <tr><td>Patchy white areas with texture</td><td>Possible fungal or bacterial infection &mdash; half-dose treatment</td></tr>
      <tr><td>Gradual muting over many months in an old fish</td><td>Ageing &mdash; see <a href="/guides/puffer-fish-care/lifespan/">lifespan</a></td></tr>
    </table></div>
"""

COLOR = {
    "slug": "color-change",
    "title": "Puffer Fish Turning Black or Losing Colour: What It Means",
    "meta_desc": "Why a puffer fish turns black, pale or blotchy: normal mood and camouflage changes versus stress, nitrate, wrong salinity, poor diet and parasites.",
    "h1": "Puffer Fish Colour Changes",
    "hero_tag": "Color Changes",
    "hero_meta": "⚫ Dark = mood or stress &nbsp;|&nbsp; ⚪ Pale = check health &nbsp;|&nbsp; \U0001F50D Behaviour decides",
    "toc_sections": [
        ("normal", "Normal Colour Changes"),
        ("black", "Turning Black"),
        ("pale", "Losing Colour"),
        ("substrate", "Substrate & Lighting"),
        ("action", "When to Act"),
    ],
    "body": COLOR_BODY,
    "faqs": [
        ("Why is my puffer fish turning black?",
         "Short darkening that passes within hours is mood: irritation, territorial display or hunting excitement. Staying dark points to stress from a recent change, ammonia or high nitrate, the wrong salinity for a brackish species, or illness if the fins are clamped and the fish is not eating."),
        ("Why is my puffer fish losing its colour?",
         "Sustained paling usually means poor water quality, a diet of soft food only, internal parasites, or chronic stress from harassment. Old puffers also mute gradually over months, which you can distinguish by how slowly it happens."),
        ("Is it normal for puffer fish to change colour?",
         "Yes, and they do it more than most aquarium fish. Puffers darken when irritated, pale at night, mottle to match the substrate, and intensify as they mature. Colour change alongside normal behaviour is not a problem."),
        ("Why does my puffer have a dark stripe on its belly?",
         "On a mature pea puffer that stripe identifies a male. It intensifies when he is in breeding condition or displaying, and it is a sexing feature rather than a health symptom."),
        ("My puffer went pale after I changed the substrate, is it sick?",
         "Probably not. Puffers adjust their colour to their background, so a fish over new pale sand will look washed out. Check the lighting too, because bright overhead light mutes colour. Add floating plants or dim the light and give it a few days."),
        ("When should I worry about a puffer's colour change?",
         "When the colour change comes with clamped fins, hiding, refusing food, rapid gilling, weight loss or patchy areas with visible texture. Colour alone is rarely the useful signal; the accompanying behaviour is."),
    ],
    "related": [
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/guides/puffer-fish-care/not-eating/", "Puffer Not Eating"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/puffer-fish-care/", "Puffer Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# SWIMMING & BREATHING
# ════════════════════════════════════════════════════════════════
SWIM_BODY = """    <p>Puffers swim with their pectoral fins, hovering and reversing with precision rather than powering forward with the tail. That makes abnormal swimming easy to spot and easy to misread. Two problems account for most cases: buoyancy trouble, which is usually digestive or air-related, and oxygen trouble, which is usually water quality. They need different responses, so identify which one you are looking at first.</p>

    <h2 id="gasping">Puffer Fish Gasping for Air</h2>
    <p>A puffer at the surface taking rapid, shallow breaths is not getting enough oxygen at its gills. Treat this as urgent.</p>
    <ol>
      <li><strong>Add aeration immediately</strong> &mdash; an airstone, or angle the filter return to break the surface.</li>
      <li><strong>Change 50% of the water</strong> with temperature-matched, dechlorinated water.</li>
      <li><strong>Test ammonia and nitrite.</strong> Either above zero is the most likely cause and both damage gills directly.</li>
      <li><strong>Check the temperature.</strong> Above 82&deg;F, warm water holds less oxygen while the fish needs more.</li>
      <li><strong>Look for gill parasites.</strong> Rapid gilling with flashing and no visible spots points to flukes &mdash; praziquantel is well tolerated by puffers.</li>
      <li><strong>Check salinity</strong> for brackish species; a sudden swing stresses gills.</li>
    </ol>
    <div class="callout callout-warn"><strong>Chlorine.</strong> An undosed water change is a common cause of sudden gasping across the whole tank. If you have just changed water, dose dechlorinator now.</div>

    <h2 id="sideways">Puffer Fish Swimming Sideways or Upside Down</h2>
    <p>This is a buoyancy problem. In puffers, the three usual causes are trapped air, constipation and a swim bladder problem following an infection.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>Clues</th><th>Action</th></tr>
      <tr><td>Trapped air after netting</td><td>Floats at the surface, struggles to swim down, recent handling</td><td>Release the air &mdash; see <a href="/guides/puffer-fish-care/puffing-up/">puffing up</a></td></tr>
      <tr><td>Constipation</td><td>Swollen belly, no faeces, soft-food diet</td><td>Fast 2&ndash;3 days, Epsom salt 1 tbsp per 5 gal, then shelled prey</td></tr>
      <tr><td>Overfeeding</td><td>Follows a large meal, resolves in a day</td><td>Reduce portions</td></tr>
      <tr><td>Swim bladder infection</td><td>Persistent, with clamped fins or lethargy</td><td>Clean water, warmth, half-dose antibacterial in quarantine</td></tr>
      <tr><td>Water quality</td><td>Other fish affected too</td><td>Test and change water</td></tr>
      <tr><td>Injury or neurological damage</td><td>After a fall, a fight, or long-term feeder fish diet</td><td>Supportive care; lower the water level</td></tr>
    </table></div>

    <h2 id="protocol">The Buoyancy Protocol</h2>
    <ol>
      <li><strong>Rule out trapped air first</strong> if the fish has been netted or handled recently.</li>
      <li><strong>Fast for two to three days.</strong> Puffers tolerate this easily and constipation is the most common cause.</li>
      <li><strong>Confirm water:</strong> ammonia and nitrite 0, nitrate under 20 ppm, temperature 78&ndash;80&deg;F.</li>
      <li><strong>Add Epsom salt</strong> at one tablespoon per 5 gallons, dissolved in change water first.</li>
      <li><strong>Lower the water level and reduce flow</strong> so a struggling fish is not exhausted reaching the bottom or fighting current.</li>
      <li><strong>Resume feeding with shelled prey</strong> on day four, not bloodworms.</li>
    </ol>

    <h2 id="other">Other Abnormal Swimming</h2>
    <ul>
      <li><strong>Flashing &mdash; rubbing against decor or substrate.</strong> Parasites, most often ich or flukes. See the <a href="/guides/puffer-fish-care/diseases/">diseases page</a>.</li>
      <li><strong>Shimmying in place.</strong> Usually a water quality or temperature problem; test and check the heater.</li>
      <li><strong>Corkscrewing or spiralling.</strong> Neurological. Long-term feeder-fish diets causing vitamin B1 deficiency are one preventable cause; bacterial infection is another.</li>
      <li><strong>Sitting on the bottom but upright and alert.</strong> Normal puffer resting &mdash; see <a href="/guides/puffer-fish-care/not-eating/">lying on the bottom</a>.</li>
      <li><strong>Wedging into a corner nose-down.</strong> Stress or a strong current; check flow and look for a chasing tank mate.</li>
    </ul>

    <h2 id="prevention">Prevention</h2>
    <ul>
      <li>Never net a puffer; move it in a submerged container.</li>
      <li>Feed shelled food regularly and avoid a bloodworm-only diet.</li>
      <li>Keep nitrate under 20 ppm with 30&ndash;50% weekly water changes.</li>
      <li>Keep an airstone on any puffer tank running above 80&deg;F.</li>
      <li>Quarantine and deworm new fish before they meet the display tank.</li>
    </ul>
"""

SWIM = {
    "slug": "swimming-problems",
    "title": "Puffer Fish Swimming Sideways or Gasping for Air",
    "meta_desc": "Why a puffer fish swims sideways, floats or gasps at the surface: trapped air, constipation, ammonia and gill flukes, with a step-by-step buoyancy protocol.",
    "h1": "Puffer Fish Swimming and Breathing Problems",
    "hero_tag": "Swimming & Breathing",
    "hero_meta": "\U0001F300 Buoyancy vs oxygen &nbsp;|&nbsp; \U0001F4A8 Gasping is urgent &nbsp;|&nbsp; \U0001F374 Fast 2&ndash;3 days",
    "toc_sections": [
        ("gasping", "Gasping for Air"),
        ("sideways", "Swimming Sideways"),
        ("protocol", "Buoyancy Protocol"),
        ("other", "Other Abnormal Swimming"),
        ("prevention", "Prevention"),
    ],
    "body": SWIM_BODY,
    "faqs": [
        ("Why is my puffer fish gasping for air at the surface?",
         "It cannot get enough oxygen at the gills. The usual causes are ammonia or nitrite above zero, low dissolved oxygen in warm or still water, gill flukes, an undosed water change leaving chlorine in the tank, or a sudden salinity swing. Add aeration and change 50 percent of the water now."),
        ("Why is my puffer fish swimming sideways?",
         "It is a buoyancy problem. The usual causes are air trapped after the fish was netted, constipation from a soft-food diet, overfeeding, or a swim bladder problem following an infection. Rule out trapped air first if the fish has been handled recently."),
        ("Why is my puffer fish floating at the top and cannot swim down?",
         "That pattern almost always means trapped air, usually after being lifted out of the water in a net. Hold the fish underwater head slightly down and rock it gently while stroking the belly forward to back to release the air."),
        ("How do you treat swim bladder problems in a puffer?",
         "Fast the fish for two to three days, confirm ammonia and nitrite are zero and nitrate is under 20 ppm, hold the temperature at 78 to 80F, add Epsom salt at one tablespoon per 5 gallons, lower the water level to reduce effort, and resume feeding with shelled prey."),
        ("Why is my puffer fish rubbing against things?",
         "Flashing against decor or substrate is a parasite sign, most often ich or gill and skin flukes. Look for white spots, and if there are none, treat for flukes with praziquantel, which puffers tolerate well."),
        ("Why is my puffer fish breathing fast?",
         "Rapid gilling means oxygen stress or gill irritation: ammonia or nitrite, high temperature, low oxygen, gill flukes or a chemical in the water. Test the water, add aeration and change 50 percent immediately."),
    ],
    "related": [
        ("/guides/puffer-fish-care/puffing-up/", "Puffing Up & Trapped Air"),
        ("/guides/puffer-fish-care/diseases/", "Puffer Diseases"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/puffer-fish-care/water-parameters/", "Water Parameters"),
    ],
}


# ════════════════════════════════════════════════════════════════
PAGES = [PILLAR, TYPES, FRESH, SALT, TANK, WATER, FOOD, TEETH, SIZE, LIFESPAN,
         PEA, F8, GSP, AMAZON, FAHAKA, MBU, BREED, MATES, BEHAV, DIS, EAT,
         PUFF, COLOR, SWIM]


def main():
    written = 0
    for spec in PAGES:
        html = page(
            slug=spec["slug"], title=spec["title"], meta_desc=spec["meta_desc"],
            h1=spec["h1"], hero_tag=spec["hero_tag"], hero_meta=spec["hero_meta"],
            toc_sections=spec["toc_sections"], body_html=spec["body"],
            faqs=spec["faqs"], related=spec["related"],
            hero_img=spec.get("hero_img", HERO_IMG),
        )
        out_dir = BASE / spec["slug"] if spec["slug"] else BASE
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        url = f"/guides/puffer-fish-care/{spec['slug']}/" if spec["slug"] else "/guides/puffer-fish-care/"
        print(f"  {url:<48} {len(html):>7,} bytes")
        written += 1
    print(f"\n{written} pages written to {BASE}")


if __name__ == "__main__":
    main()
