"""
generate_betta_cluster.py
──────────────────────────
Generates 4 Betta Fish Care cluster sub-pages under
/guides/betta-fish-care/{slug}/index.html, following the discus
cluster template (artlay 2-column with sidebar cluster nav).

Run:  python3 generate_betta_cluster.py
"""

from pathlib import Path

REPO  = Path(__file__).parent.parent
BASE  = REPO / "guides" / "betta-fish-care"

CLUSTER_NAV = [
    ("/guides/betta-fish-care/",              "🐠 Betta Fish Care Guide", "pillar"),
    ("/guides/betta-fish-care/tank-setup/",   "🪣 Tank Setup"),
    ("/guides/betta-fish-care/tank-mates/",   "🐟 Tank Mates"),
    ("/guides/betta-fish-care/feeding/",      "🦐 Feeding Guide"),
    ("/guides/betta-fish-care/temperature/",  "🌡️ Temperature & Water"),
    ("/guides/how-long-do-betta-fish-live/",  "⏳ Betta Lifespan"),
]

TOOL_LINKS = [
    ("/calculators/betta-fish-tank-size/",     "Betta Tank Size Calculator"),
    ("/tools/fish-compatibility-checker/",     "Compatibility Checker"),
    ("/tools/water-parameter-checker/",        "Water Parameter Checker"),
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
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('/assets/encyclopedia/real/betta-fish-wikimedia-real.jpg') center/cover no-repeat}
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
        cls = css_class
        if is_cur:
            cls = (cls + " cur").strip()
        items.append(f'<a href="{href}" class="{cls}">{label}</a>')
    return "\n".join(items)


def toc_html(sections: list) -> str:
    return "\n".join(f'<a href="#{sid}">{label}</a>' for sid, label in sections)


def tool_links_html() -> str:
    return "\n".join(
        f'<a href="{href}">{label} <span>→</span></a>' for href, label in TOOL_LINKS
    )


def faq_json(faqs: list) -> str:
    import json
    entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False)


def page(
    slug: str,
    title: str,
    meta_desc: str,
    h1: str,
    hero_tag: str,
    hero_meta: str,
    date: str,
    toc_sections: list,
    body_html: str,
    faqs: list,
) -> str:
    canonical = f"https://www.fishcareai.com/guides/betta-fish-care/{slug}/"
    breadcrumb_json = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},'
        '{"@type":"ListItem","position":2,"name":"Guides","item":"https://www.fishcareai.com/guides/"},'
        '{"@type":"ListItem","position":3,"name":"Betta Fish Care Guide","item":"https://www.fishcareai.com/guides/betta-fish-care/"},'
        f'{{"@type":"ListItem","position":4,"name":"{h1}","item":"{canonical}"}}'
        "]}"
    )
    article_json = (
        f'{{"@context":"https://schema.org","@type":"Article","headline":"{title}",'
        f'"description":"{meta_desc}",'
        f'"datePublished":"{date}","dateModified":"{date}",'
        '"author":{"@type":"Organization","name":"FishCare AI Editorial Team"},'
        '"publisher":{"@type":"Organization","name":"FishCare AI","url":"https://www.fishcareai.com"}}'
    )

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
<meta property="og:image" content="https://www.fishcareai.com/assets/encyclopedia/real/betta-fish-wikimedia-real.jpg"/>
<meta name="twitter:card" content="summary_large_image"/>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{faq_json(faqs)}</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260815-betta-cluster"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl act" href="/guides/">Guides</a>
    <a class="nl" href="/wiki/">Encyclopedia</a>
    <a class="nl" href="/fish-health/">Fish Health</a>
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
      <a href="/guides/betta-fish-care/">Betta Fish Care Guide</a><span>/</span>
      <span style="color:rgba(255,255,255,.9)">{hero_tag}</span>
    </div>
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">🐠 Betta Fish Care</div>
    <h1>{h1}</h1>
    <div class="guide-meta">{hero_meta}</div>
  </div>
</section>

<div class="artlay">
  <article class="artc">
{body_html}
  </article>

  <aside class="sidebar">
    <div class="cluster-nav">
      <h4>Betta Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc_sections)}
    </div>
    <div class="tool-card">
      <h4>Betta Tools</h4>
      {tool_links_html()}
    </div>
  </aside>
</div>

<footer class="ft">
  <div class="con"><div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div></div>
  <nav class="legal-links" aria-label="Legal"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


# ────────────────────────────────────────────────────────────────
# PAGE 1 — Tank Setup
# ────────────────────────────────────────────────────────────────
TANK_SETUP_BODY = """    <h2 id="minimum-size">Minimum Tank Size for a Betta</h2>
    <p>A 5-gallon aquarium is the practical minimum for one adult betta. A 10-gallon tank is a better choice for most keepers: the larger water volume dilutes waste more slowly, buffers against temperature swings, and gives the betta more horizontal swimming space without requiring significantly more maintenance.</p>
    <div class="callout"><strong>Why tank size matters:</strong> Betta fish are often sold in small cups or bowls. These are temporary holding containers, not permanent homes. In confined water, ammonia accumulates within hours, temperature varies wildly with room temperature, and the fish cannot express natural behaviour such as patrolling a territory or exploring plants.</div>
    <table class="ptbl">
      <tr><th>Tank Size</th><th>Verdict</th><th>Notes</th></tr>
      <tr><td>Under 2.5 gal</td><td>❌ Not suitable</td><td>Water quality crashes too fast; no room for a heater</td></tr>
      <tr><td>2.5–4 gal</td><td>⚠️ Marginal</td><td>Possible with frequent water changes; harder to keep stable</td></tr>
      <tr><td>5 gal</td><td>✅ Minimum</td><td>Workable for one betta with weekly 25–30% changes</td></tr>
      <tr><td>10 gal</td><td>✅ Recommended</td><td>Easier water quality management; allows more decor</td></tr>
      <tr><td>20 gal+</td><td>✅ Excellent</td><td>Room for a sorority (females) or community setup</td></tr>
    </table>

    <h2 id="filtration">Filtration: Gentle Flow Is Essential</h2>
    <p>Betta fish are native to slow-moving rice paddies and shallow streams — they are not built for strong currents. A filter that pushes the fish around the tank will exhaust it, damage its fins, and cause chronic stress. The goal is biological filtration (beneficial bacteria breaking down ammonia) with minimal surface turbulence.</p>
    <ul>
      <li><strong>Sponge filter:</strong> the best choice for betta tanks — very gentle flow, provides biological filtration, safe for long fins; air pump required</li>
      <li><strong>Hang-on-back (HOB) filter:</strong> works well if you add a pre-filter sponge over the intake and baffle the outflow with a spray bar, a piece of plastic bottle, or filter floss</li>
      <li><strong>Internal power filter:</strong> usually too strong; reduce flow to minimum or baffle the outflow</li>
      <li><strong>No filter:</strong> not viable long-term without very frequent (daily or every-other-day) large water changes</li>
    </ul>
    <p>Test whether your current is too strong: a betta should swim easily in all directions without being pushed. If it consistently rests in a corner avoiding the flow, the current is too strong.</p>

    <h2 id="heating">Heating: Bettas Need Stable Warmth</h2>
    <p>Betta fish require water temperature between 76–81°F (24–27°C). They are tropical fish — they cannot regulate their own body temperature and will suffer in cool rooms. An adjustable submersible heater with a separate thermometer is the reliable solution.</p>
    <div class="callout callout-warn"><strong>Cold water is the most common betta care mistake.</strong> A betta kept at 68–72°F will become lethargic, stop eating, develop a weakened immune system, and become vulnerable to every disease in the aquarium. Warmth is not optional.</div>
    <table class="ptbl">
      <tr><th>Equipment</th><th>Recommendation</th></tr>
      <tr><td>Heater wattage</td><td>25W for 5 gal; 50W for 10 gal; 100W for 20 gal</td></tr>
      <tr><td>Heater type</td><td>Adjustable submersible with thermostat (Aqueon, Eheim, Fluval)</td></tr>
      <tr><td>Thermometer</td><td>Always use a separate thermometer — do not trust the heater dial alone</td></tr>
      <tr><td>Target temperature</td><td>78–80°F (25–27°C) is the sweet spot for most bettas</td></tr>
    </table>

    <h2 id="substrate">Substrate and Decor</h2>
    <p>Bettas are not strongly substrate-dependent — they spend most of their time in the middle and upper water column. Choose substrate based on aesthetic preference and ease of cleaning:</p>
    <ul>
      <li><strong>Fine sand:</strong> natural look; easy to vacuum; some bettas enjoy resting on it</li>
      <li><strong>Small rounded gravel:</strong> widely available; vacuum debris easily between grains</li>
      <li><strong>Bare bottom:</strong> easiest to clean; sterile-looking but practical for hospital tanks</li>
    </ul>
    <p><strong>Decor rules:</strong> all decorations must be smooth with no sharp edges. Run pantyhose over every surface before adding it to a betta tank — if it snags, it will shred fins. Avoid: rough ceramic, plastic plants with jagged edges, sharp rocks, decor with holes small enough to trap the fish.</p>

    <h2 id="plants">Live vs Artificial Plants</h2>
    <p>Bettas thrive with plant cover — they feel exposed and stressed in bare tanks. Live plants are ideal as they absorb nitrates, provide hiding spots, and give the fish surfaces to rest on near the surface. Recommended plants for betta tanks:</p>
    <ul>
      <li><strong>Java fern</strong> (Microsorum pteropus) — hardy, low-light, attach to driftwood</li>
      <li><strong>Anubias</strong> — very hardy, broad leaves that bettas love to rest on; attach to hardscape</li>
      <li><strong>Amazon sword</strong> — beautiful centrepiece plant for larger tanks</li>
      <li><strong>Water sprite / Ceratopteris</strong> — floating or rooted; excellent surface cover</li>
      <li><strong>Marimo moss balls</strong> — low maintenance; bettas often interact with them</li>
    </ul>
    <p>If using artificial plants, choose only soft silk varieties — never stiff plastic plants with pointed tips.</p>

    <h2 id="lid">Lid: Bettas Jump</h2>
    <p>A secure lid is essential. Betta fish jump — often at night or when startled. Even a 2-inch gap around equipment cables is enough for a betta to escape. Most standard aquarium lids leave a gap at the back for filter and heater cables; cover this gap with cut pieces of plastic mesh or foam. Check under the lid every morning.</p>

    <h2 id="cycling">Cycling the Aquarium</h2>
    <p>Before adding a betta, the aquarium should be cycled — that is, colonised with beneficial bacteria that convert toxic ammonia (from fish waste and uneaten food) into less-toxic nitrite, then into relatively safe nitrate. An uncycled tank can accumulate lethal ammonia levels within 24 hours of the fish being added.</p>
    <ul>
      <li><strong>Fishless cycle:</strong> add a source of ammonia (pure ammonia drops, fish food, raw shrimp) before adding the fish; wait 4–6 weeks until ammonia and nitrite both read 0 ppm</li>
      <li><strong>Seeded cycle:</strong> use filter media, gravel, or a sponge from an existing cycled tank to speed the process dramatically</li>
      <li><strong>Bottled bacteria products:</strong> (Seachem Stability, Fritz Zyme 7) can help establish a cycle faster</li>
    </ul>
    <div class="callout"><strong>Test kit:</strong> An API Master Test Kit (liquid test kit, not strips) is the reliable way to monitor ammonia, nitrite, and nitrate during and after cycling. Test weekly once the tank is established.</div>

    <h2 id="related">Related Guides &amp; Tools</h2>
    <div class="guide-links">
      <a href="/guides/betta-fish-care/">🐠 Betta Fish Care Guide</a>
      <a href="/guides/betta-fish-care/tank-mates/">🐟 Betta Tank Mates</a>
      <a href="/guides/betta-fish-care/temperature/">🌡️ Betta Temperature Guide</a>
      <a href="/calculators/betta-fish-tank-size/">📐 Tank Size Calculator</a>
      <a href="/wiki/betta-fish/">📖 Betta Fish Encyclopedia</a>
      <a href="/guides/how-long-do-betta-fish-live/">⏳ How Long Do Bettas Live?</a>
    </div>"""

# ────────────────────────────────────────────────────────────────
# PAGE 2 — Tank Mates
# ────────────────────────────────────────────────────────────────
TANK_MATES_BODY = """    <h2 id="can-betta-live-with-fish">Can Betta Fish Live With Other Fish?</h2>
    <p>The short answer: yes — but with important conditions. Male bettas are territorial and will aggressively attack other male bettas and any fish that resembles one (colourful, long-finned species). With the right tank mates, in a large enough tank with adequate cover, many bettas coexist peacefully with a wide variety of community fish.</p>
    <div class="callout"><strong>The key rule:</strong> No two male bettas together — ever. They will fight to the death. One male betta per tank, always.</div>
    <p>The success of any betta community setup depends on three factors: the individual betta's temperament (some are aggressive toward everything; others are very relaxed), the tank size (10 gallons minimum; larger is better), and the tank mate species.</p>

    <h2 id="best-tank-mates">Best Tank Mates for Betta Fish</h2>
    <p>These species are widely reported as compatible with bettas in appropriately sized, planted tanks:</p>
    <table class="ptbl">
      <tr><th>Species</th><th>Why It Works</th><th>Min. Tank</th></tr>
      <tr><td>Ember Tetra</td><td>Tiny, fast, non-nippy; subdued orange color doesn't trigger betta aggression</td><td>10 gal</td></tr>
      <tr><td>Chili Rasbora</td><td>Very small and fast; largely ignored by bettas; excellent nano tank companion</td><td>10 gal</td></tr>
      <tr><td>Neon Tetra</td><td>Generally compatible; watch for occasional betta aggression in smaller tanks</td><td>15 gal</td></tr>
      <tr><td>Harlequin Rasbora</td><td>Active mid-level swimmer; non-nippy; peaceful with bettas</td><td>15 gal</td></tr>
      <tr><td>Corydoras Catfish</td><td>Bottom dwellers; armoured; bettas rarely harass them; keep in groups of 6+</td><td>15 gal</td></tr>
      <tr><td>Pygmy Corydoras</td><td>Nano-sized; peaceful; excellent bottom cleaner for smaller betta tanks</td><td>10 gal</td></tr>
      <tr><td>Otocinclus</td><td>Algae-eating catfish; very peaceful; ignored by most bettas</td><td>10 gal</td></tr>
      <tr><td>Nerite Snail</td><td>Shell protects them; excellent algae cleaners; bettas may flare at shell but cannot damage it</td><td>5 gal</td></tr>
      <tr><td>Mystery Snail</td><td>Same as nerite; larger shell; some bettas harass them occasionally</td><td>5 gal</td></tr>
      <tr><td>Amano Shrimp</td><td>Large enough that most bettas ignore them; but individual betta temperament matters</td><td>10 gal</td></tr>
    </table>

    <h2 id="avoid">Fish to Avoid With Bettas</h2>
    <p>These species should never be housed with bettas, or require very careful monitoring:</p>
    <ul>
      <li><strong>Other male bettas:</strong> guaranteed fighting; do not attempt under any circumstances</li>
      <li><strong>Guppies:</strong> male guppies' colourful, long-flowing tails trigger betta aggression instinctively; bettas will attack them</li>
      <li><strong>Fin nippers:</strong> tiger barbs, serpae tetras, and some other barb/tetra species will relentlessly nip at betta fins; the betta's long fins make it an especially tempting target</li>
      <li><strong>Gouramis:</strong> same family as bettas; males may trigger territorial aggression; generally not recommended</li>
      <li><strong>Cichlids:</strong> most cichlids are too aggressive; they will bully or injure a betta</li>
      <li><strong>Goldfish:</strong> incompatible water temperature requirements (goldfish prefer cooler water)</li>
      <li><strong>Cherry shrimp (small neocaridina):</strong> high risk of being eaten; larger species like Amano shrimp are safer</li>
    </ul>
    <div class="callout callout-warn"><strong>Individual variation:</strong> Betta temperament varies enormously between individuals. One betta may coexist peacefully with neon tetras for years; another may attack everything in the tank within minutes. Always introduce new tank mates slowly and monitor carefully for 48–72 hours.</div>

    <h2 id="female-betta">Female Betta Sorority Tanks</h2>
    <p>Multiple female bettas can sometimes be kept together in a "sorority tank" — but this is an advanced technique that is frequently unsuccessful. If attempting a sorority:</p>
    <ul>
      <li>Use a 20-gallon minimum, heavily planted with dense sight breaks</li>
      <li>Introduce all females simultaneously — never add a new female to an established group</li>
      <li>Keep 5–6 females minimum — aggression is spread across the group rather than focused on one victim</li>
      <li>Monitor closely for a week; some hierarchical chasing is normal, but any fish being cornered or refused food must be removed</li>
      <li>Have a backup plan (a separate tank) ready for any fish that cannot coexist</li>
    </ul>

    <h2 id="setup-tips">Setup Tips for a Betta Community Tank</h2>
    <ul>
      <li><strong>Size matters:</strong> the larger the tank, the easier it is to manage betta aggression — 15–20 gallons gives tank mates escape room</li>
      <li><strong>Dense planting:</strong> lots of plants, driftwood, and hiding spots break lines of sight and give the betta a territory to defend without controlling the whole tank</li>
      <li><strong>Introduce the betta last:</strong> add tank mates first so they establish themselves; adding the betta to an occupied tank is better than the reverse</li>
      <li><strong>Feed at multiple spots:</strong> betta food near the surface, sinking food for bottom dwellers; prevents the betta from monopolising feeding</li>
    </ul>

    <h2 id="related">Related Guides &amp; Tools</h2>
    <div class="guide-links">
      <a href="/guides/betta-fish-care/">🐠 Betta Fish Care Guide</a>
      <a href="/guides/betta-fish-care/tank-setup/">🪣 Betta Tank Setup</a>
      <a href="/tools/fish-compatibility-checker/">✅ Compatibility Checker</a>
      <a href="/wiki/ember-tetra/">🔥 Ember Tetra</a>
      <a href="/wiki/pygmy-corydoras/">🐾 Pygmy Corydoras</a>
      <a href="/wiki/chili-rasbora/">🔴 Chili Rasbora</a>
    </div>"""

# ────────────────────────────────────────────────────────────────
# PAGE 3 — Feeding
# ────────────────────────────────────────────────────────────────
FEEDING_BODY = """    <h2 id="what-do-bettas-eat">What Do Betta Fish Eat?</h2>
    <p>Betta fish are carnivores with a strong preference for protein-rich live food. In the wild they eat insects that fall on the water surface, mosquito larvae, small crustaceans, and zooplankton. In the aquarium, a diet that reflects this — primarily protein-based with some variety — keeps bettas in excellent health and vivid colour.</p>
    <div class="callout"><strong>Common mistake:</strong> feeding bettas generic tropical fish flakes. Most flake food is formulated for omnivores and is not nutritionally complete for bettas — it is often high in filler ingredients like wheat and soy. Use betta-specific food as the staple.</div>

    <h2 id="staple-food">Staple Food: Betta Pellets</h2>
    <p>High-quality betta pellets are the most practical staple for most keepers. They are nutritionally complete, easy to portion, and don't foul the water as quickly as some other foods.</p>
    <p>What to look for in betta pellets:</p>
    <ul>
      <li><strong>Protein first:</strong> the first ingredient should be a whole fish or fish meal (salmon, herring, etc.) — not wheat, corn, or soy</li>
      <li><strong>Minimum 40% protein content</strong></li>
      <li><strong>Small pellet size:</strong> betta mouths are small; if pellets are too large the fish will spit them out repeatedly</li>
    </ul>
    <table class="ptbl">
      <tr><th>Brand</th><th>Notes</th></tr>
      <tr><td>Hikari Betta Bio-Gold</td><td>Widely available; good protein content; small pellet size</td></tr>
      <tr><td>Fluval Bug Bites (Betta)</td><td>Black soldier fly larvae as primary ingredient; excellent nutrition</td></tr>
      <tr><td>New Life Spectrum Betta</td><td>High protein; natural colour enhancers; well-regarded</td></tr>
      <tr><td>Northfin Betta Bits</td><td>No artificial ingredients; high protein from whole fish</td></tr>
    </table>

    <h2 id="frozen-food">Frozen & Live Foods</h2>
    <p>Supplementing pellets with frozen or live foods dramatically improves betta health, colour, and breeding condition. Feed these 3–5 times per week as variety, or as the primary diet for serious breeders.</p>
    <ul>
      <li><strong>Frozen blood worms:</strong> bettas go wild for them; excellent protein; do not overfeed — blood worms are high in fat and can cause constipation if fed daily</li>
      <li><strong>Frozen brine shrimp:</strong> excellent protein and natural colour enhancer; highly palatable</li>
      <li><strong>Frozen daphnia:</strong> high fibre content; good for digestion; can help resolve mild constipation</li>
      <li><strong>Frozen mysis shrimp:</strong> high protein; whole prey nutritional profile</li>
      <li><strong>Live food:</strong> fruit flies (flightless Drosophila), blackworms, micro worms, baby brine shrimp — exceptional for conditioning bettas before breeding</li>
    </ul>

    <h2 id="how-much-how-often">How Much and How Often to Feed</h2>
    <p>Bettas have small stomachs — roughly the size of their eye. Overfeeding is one of the most common betta care mistakes and leads to obesity, swim bladder problems, and fouled water.</p>
    <table class="ptbl">
      <tr><th>Factor</th><th>Guidance</th></tr>
      <tr><td>Frequency</td><td>Once or twice daily; twice is ideal for growth and condition</td></tr>
      <tr><td>Portion size (pellets)</td><td>3–5 small pellets per feeding; all consumed within 2 minutes</td></tr>
      <tr><td>Fasting</td><td>Fast for 1 full day per week to prevent constipation and clear the digestive system</td></tr>
      <tr><td>Remove uneaten food</td><td>Use a turkey baster or net to remove uneaten food within 5 minutes of feeding</td></tr>
    </table>
    <div class="callout callout-warn"><strong>Signs of overfeeding:</strong> round or swollen abdomen, constipation (no faeces for 3+ days), cloudy water. Fast for 2–3 days and feed blanched, shelled peas (cut into tiny pieces) to relieve constipation.</div>

    <h2 id="problem-feeding">Feeding Problems: Betta Won't Eat</h2>
    <p>A betta refusing food is a common concern. Causes and solutions:</p>
    <ul>
      <li><strong>New environment stress:</strong> newly purchased bettas often refuse food for 2–5 days while adjusting; wait and keep conditions stable</li>
      <li><strong>Water temperature too low:</strong> below 74°F, betta metabolism slows and appetite decreases dramatically; check temperature first</li>
      <li><strong>Food too large or wrong type:</strong> try a different pellet brand or crush pellets smaller; try frozen blood worms (usually irresistible)</li>
      <li><strong>Illness:</strong> persistent refusal of food combined with lethargy, fin clamping, or unusual posture indicates illness — test water quality and inspect for visible symptoms</li>
      <li><strong>Overfeeding:</strong> some bettas go on short "hunger strikes" after being overfed; fast for 1–2 days</li>
    </ul>

    <h2 id="related">Related Guides &amp; Tools</h2>
    <div class="guide-links">
      <a href="/guides/betta-fish-care/">🐠 Betta Fish Care Guide</a>
      <a href="/guides/betta-fish-care/tank-mates/">🐟 Betta Tank Mates</a>
      <a href="/guides/betta-fish-care/temperature/">🌡️ Temperature & Water Quality</a>
      <a href="/wiki/betta-fish/">📖 Betta Fish Encyclopedia</a>
      <a href="/guides/how-long-do-betta-fish-live/">⏳ How Long Do Bettas Live?</a>
      <a href="/tools/water-parameter-checker/">🔬 Water Parameter Checker</a>
    </div>"""

# ────────────────────────────────────────────────────────────────
# PAGE 4 — Temperature & Water
# ────────────────────────────────────────────────────────────────
TEMPERATURE_BODY = """    <h2 id="ideal-temperature">Ideal Betta Fish Temperature</h2>
    <p>The ideal water temperature for betta fish is 76–81°F (24–27°C), with 78–80°F (25–27°C) being the sweet spot where bettas are most active, eat well, and maintain a strong immune system. Temperature stability is as important as the target range — sudden shifts of even 4–5°F can trigger illness.</p>
    <table class="ptbl">
      <tr><th>Temperature</th><th>Effect on Betta</th></tr>
      <tr><td>Below 68°F (20°C)</td><td>Severe lethargy, immune system failure, high disease risk, shortened lifespan</td></tr>
      <tr><td>68–75°F (20–24°C)</td><td>Reduced activity, poor appetite, increased susceptibility to disease</td></tr>
      <tr><td>76–81°F (24–27°C)</td><td>Optimal — active, good colour, healthy appetite, strong immunity</td></tr>
      <tr><td>82–84°F (28–29°C)</td><td>Acceptable short-term (e.g. during ich treatment); accelerates metabolism</td></tr>
      <tr><td>Above 84°F (29°C)</td><td>Oxygen depletion; heat stress; do not maintain long-term</td></tr>
    </table>
    <div class="callout callout-warn"><strong>Cold water kills slowly.</strong> A betta kept at 70°F won't die immediately — it will become lethargic, stop eating, develop fin rot and velvet, and die within weeks to months. Cold water is the single most common cause of preventable betta death.</div>

    <h2 id="heater">Choosing and Setting Up a Heater</h2>
    <p>An adjustable submersible aquarium heater with a built-in thermostat is the reliable solution for maintaining betta temperature. Do not rely on room temperature — homes vary by season, and even a warm room can drop below 70°F overnight in winter.</p>
    <ul>
      <li><strong>5-gallon tank:</strong> 25W heater</li>
      <li><strong>10-gallon tank:</strong> 50W heater</li>
      <li><strong>20-gallon tank:</strong> 100W heater</li>
      <li><strong>Thermostat-controlled:</strong> choose a heater with a thermostat dial rather than a fixed-temperature heater</li>
    </ul>
    <p>Always use a separate thermometer — digital clip-on or floating glass — to verify the actual water temperature. Heater dials are often inaccurate by 2–5°F.</p>

    <h2 id="water-parameters">Water Quality Parameters</h2>
    <p>Temperature is only one part of betta water quality. These parameters should be tested regularly with a liquid test kit (not strip tests, which are often inaccurate):</p>
    <table class="ptbl">
      <tr><th>Parameter</th><th>Target Range</th><th>Notes</th></tr>
      <tr><td>Temperature</td><td>76–81°F (24–27°C)</td><td>Use a heater; check with a thermometer</td></tr>
      <tr><td>pH</td><td>6.5–7.5</td><td>Stability more important than exact value; don't chase numbers</td></tr>
      <tr><td>Ammonia</td><td>0 ppm</td><td>Any ammonia is dangerous; indicates a cycling problem</td></tr>
      <tr><td>Nitrite</td><td>0 ppm</td><td>Also toxic; present only in uncycled or disturbed tanks</td></tr>
      <tr><td>Nitrate</td><td>&lt;20 ppm</td><td>Managed with weekly partial water changes</td></tr>
      <tr><td>GH (Hardness)</td><td>5–20 dGH</td><td>Wide tolerance; most tap water is fine without adjustment</td></tr>
    </table>

    <h2 id="water-changes">Water Changes</h2>
    <p>Weekly partial water changes are the most effective single maintenance task for betta health. They dilute nitrate, replenish trace minerals, and remove dissolved waste that tests don't detect.</p>
    <ul>
      <li><strong>How much:</strong> 25–30% of tank volume per week for a filtered, cycled tank</li>
      <li><strong>Temperature match:</strong> always match the replacement water temperature to the tank; never add cold tap water directly</li>
      <li><strong>Dechlorinate:</strong> use a dechlorinator (Seachem Prime, API Stress Coat) on all tap water — chlorine and chloramine kill beneficial bacteria and irritate betta gills</li>
      <li><strong>Gravel vacuum:</strong> use a gravel siphon to remove waste from the substrate during water changes</li>
    </ul>
    <div class="callout"><strong>Tip:</strong> Seachem Prime is the most efficient dechlorinator — it also detoxifies ammonia and nitrite temporarily in emergencies. Use 1 drop per gallon for routine water changes.</div>

    <h2 id="temperature-changes">Handling Temperature Fluctuations</h2>
    <p>Sudden temperature changes are as dangerous as wrong temperature. Common causes of fluctuation:</p>
    <ul>
      <li><strong>Water changes with unmatched water:</strong> always pre-warm replacement water to tank temperature before adding it</li>
      <li><strong>Heater failure:</strong> keep a spare heater; check temperature daily; a sudden temperature drop is one of the most common triggers for ich outbreaks</li>
      <li><strong>Room temperature swings:</strong> in unheated rooms, temperature can drop sharply overnight in winter — keep the tank away from exterior walls and drafty windows</li>
      <li><strong>Direct sunlight:</strong> can overheat a tank in summer; position away from windows</li>
    </ul>

    <h2 id="related">Related Guides &amp; Tools</h2>
    <div class="guide-links">
      <a href="/guides/betta-fish-care/">🐠 Betta Fish Care Guide</a>
      <a href="/guides/betta-fish-care/tank-setup/">🪣 Betta Tank Setup</a>
      <a href="/guides/betta-fish-care/feeding/">🦐 Betta Feeding Guide</a>
      <a href="/tools/water-parameter-checker/">🔬 Water Parameter Checker</a>
      <a href="/wiki/betta-fish/">📖 Betta Fish Encyclopedia</a>
      <a href="/guides/how-long-do-betta-fish-live/">⏳ How Long Do Bettas Live?</a>
    </div>"""


PAGES = [
    {
        "slug": "tank-setup",
        "title": "Betta Fish Tank Setup Guide 2026: Size, Filter & Heater | FishCare AI",
        "meta_desc": "Complete betta fish tank setup guide: minimum tank size, gentle filtration, heater requirements, substrate, plants, and how to cycle an aquarium for bettas.",
        "h1": "Betta Fish Tank Setup: Size, Filter, Heater & Plants",
        "hero_tag": "Tank Setup",
        "hero_meta": "📏 Minimum 5 gallons &nbsp;|&nbsp; 🌡️ 76–81°F required &nbsp;|&nbsp; 🔄 Gentle filtration essential",
        "date": "2026-08-15",
        "toc_sections": [
            ("minimum-size", "Minimum Tank Size"),
            ("filtration", "Filtration"),
            ("heating", "Heating"),
            ("substrate", "Substrate & Decor"),
            ("plants", "Live vs Artificial Plants"),
            ("lid", "Lid: Bettas Jump"),
            ("cycling", "Cycling the Aquarium"),
        ],
        "body": TANK_SETUP_BODY,
        "faqs": [
            ("What is the minimum tank size for a betta fish?",
             "5 gallons is the practical minimum for one adult betta. A 10-gallon tank is easier to keep stable and is recommended for most keepers."),
            ("Do betta fish need a heater?",
             "Yes. Betta fish are tropical fish that require water temperature between 76–81°F (24–27°C). Room temperature in most homes is too cold without a heater."),
            ("What filter is best for a betta tank?",
             "A sponge filter is ideal for betta tanks — it provides biological filtration with very gentle flow. Bettas are native to slow-moving water and are stressed by strong currents."),
            ("Do bettas need live plants?",
             "Live plants are not required but are highly beneficial — they absorb nitrates, provide hiding spots, and give bettas surfaces to rest on near the surface. Java fern and Anubias are easy choices for beginners."),
        ],
    },
    {
        "slug": "tank-mates",
        "title": "Betta Fish Tank Mates 2026: Safe & Incompatible Species | FishCare AI",
        "meta_desc": "Best betta fish tank mates in 2026: ember tetras, corydoras, rasboras, snails, and species to avoid. Plus female sorority guidance and community tank tips.",
        "h1": "Betta Fish Tank Mates: What Can Live With a Betta?",
        "hero_tag": "Tank Mates",
        "hero_meta": "🐠 One male only &nbsp;|&nbsp; 🌿 Dense planting helps &nbsp;|&nbsp; 📏 15+ gallons recommended for community",
        "date": "2026-08-15",
        "toc_sections": [
            ("can-betta-live-with-fish", "Can Bettas Live With Fish?"),
            ("best-tank-mates", "Best Tank Mates"),
            ("avoid", "Species to Avoid"),
            ("female-betta", "Female Betta Sorority"),
            ("setup-tips", "Community Tank Tips"),
        ],
        "body": TANK_MATES_BODY,
        "faqs": [
            ("Can betta fish live with other fish?",
             "Yes, with the right species in a large enough, well-planted tank. Male bettas cannot live with other male bettas, and should not be housed with fin-nipping species like tiger barbs or guppies with flowing tails."),
            ("What fish can live with bettas?",
             "Good betta tank mates include ember tetras, chili rasboras, pygmy corydoras, otocinclus catfish, nerite snails, and Amano shrimp. These species are peaceful, small, and non-nippy."),
            ("Can bettas live with guppies?",
             "Generally no — male guppies' colourful flowing tails trigger betta aggression. Bettas will typically attack guppies. This combination is not recommended."),
            ("Can bettas live with shrimp?",
             "Large shrimp like Amano shrimp are usually safe with bettas. Small shrimp like cherry shrimp are at high risk of being eaten, especially juveniles. Individual betta temperament plays a large role."),
        ],
    },
    {
        "slug": "feeding",
        "title": "Betta Fish Food Guide 2026: What Do Bettas Eat? | FishCare AI",
        "meta_desc": "Complete betta fish feeding guide: best pellets, frozen food, how much to feed, how often, fasting schedule, and what to do when a betta won't eat.",
        "h1": "What Do Betta Fish Eat? Complete Feeding Guide",
        "hero_tag": "Feeding Guide",
        "hero_meta": "🦐 Carnivore diet &nbsp;|&nbsp; 🍽️ Feed 2× daily &nbsp;|&nbsp; 🚫 Fast 1 day per week",
        "date": "2026-08-15",
        "toc_sections": [
            ("what-do-bettas-eat", "What Do Bettas Eat?"),
            ("staple-food", "Staple Food: Pellets"),
            ("frozen-food", "Frozen & Live Foods"),
            ("how-much-how-often", "How Much & How Often"),
            ("problem-feeding", "Betta Won't Eat"),
        ],
        "body": FEEDING_BODY,
        "faqs": [
            ("What do betta fish eat?",
             "Betta fish are carnivores. They eat high-protein betta pellets as a staple, supplemented with frozen blood worms, brine shrimp, and daphnia. In the wild they eat insects and small crustaceans."),
            ("How often should I feed my betta fish?",
             "Feed once or twice daily, offering only as much as the fish can consume in about 2 minutes. Fast for one full day per week to prevent constipation."),
            ("Can betta fish eat tropical flake food?",
             "Generic tropical flake food is not ideal — it is formulated for omnivores and lacks the protein content bettas need. Use betta-specific pellets as the staple food."),
            ("Why won't my betta fish eat?",
             "Common causes include: adjustment stress in a new tank (wait 2–5 days), water temperature too low (check it's 76–81°F), wrong food type, or illness. Try frozen blood worms — most bettas find them irresistible."),
        ],
    },
    {
        "slug": "temperature",
        "title": "Betta Fish Temperature Guide 2026: Ideal Range & Heater Tips | FishCare AI",
        "meta_desc": "Ideal betta fish water temperature is 76–81°F. Complete guide to heater selection, water parameter targets, weekly water changes, and avoiding temperature fluctuations.",
        "h1": "Betta Fish Temperature: Ideal Range, Heaters & Water Quality",
        "hero_tag": "Temperature & Water",
        "hero_meta": "🌡️ 76–81°F ideal &nbsp;|&nbsp; 💧 Ammonia & nitrite: 0 ppm &nbsp;|&nbsp; 🔄 25–30% weekly change",
        "date": "2026-08-15",
        "toc_sections": [
            ("ideal-temperature", "Ideal Temperature"),
            ("heater", "Choosing a Heater"),
            ("water-parameters", "Water Quality Parameters"),
            ("water-changes", "Water Changes"),
            ("temperature-changes", "Handling Fluctuations"),
        ],
        "body": TEMPERATURE_BODY,
        "faqs": [
            ("What temperature do betta fish need?",
             "Betta fish need water temperature between 76–81°F (24–27°C). The optimal range is 78–80°F. They are tropical fish and cannot tolerate cold water — temperatures below 74°F cause immune suppression and disease."),
            ("Do betta fish need a heater?",
             "Yes. Most homes are too cool for bettas, especially at night or in winter. An adjustable submersible heater rated for the tank size is essential."),
            ("How often should I change betta fish water?",
             "Change 25–30% of the water weekly in a filtered, cycled tank. Always match the temperature of the replacement water to the tank temperature, and dechlorinate all tap water before adding."),
            ("What pH do betta fish need?",
             "Bettas tolerate pH 6.5–7.5. Stability is more important than exact value — avoid frequently adding pH-adjusting chemicals, which can cause dangerous swings."),
        ],
    },
]


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
        )
        (out / "index.html").write_text(html, encoding="utf-8")
        print(f"✓ /guides/betta-fish-care/{pg['slug']}/  ({len(html):,} bytes)")
    print(f"\nDone — {len(PAGES)} sub-pages generated.")


if __name__ == "__main__":
    main()
