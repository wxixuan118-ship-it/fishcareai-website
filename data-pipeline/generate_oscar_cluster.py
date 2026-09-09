"""
generate_oscar_cluster.py
─────────────────────────
Generates the Oscar fish (Astronotus ocellatus) care cluster under
/guides/oscar-fish-care/, following the koi/parrot cluster template
(2-column artlay with cluster-nav sidebar).

The pillar page /guides/oscar-fish-care/index.html already exists and ranks,
so this script never overwrites it — it only writes the sub-pages. The pillar
gets a hand-added "Oscar Fish Care Series" block, same as the koi pillar.

Run:  python3 generate_oscar_cluster.py
"""

from pathlib import Path
import json

REPO = Path(__file__).parent.parent
BASE = REPO / "guides" / "oscar-fish-care"

HERO_IMG = "/assets/encyclopedia/real/oscar-fish-wikimedia-real.jpg"
DATE = "2026-09-09"

CLUSTER_NAV = [
    ("/guides/oscar-fish-care/",                    "\U0001F41F Oscar Fish Care Guide", "pillar"),
    ("/guides/oscar-fish-care/tank-size/",          "\U0001F5C3️ Tank Size & Setup"),
    ("/guides/oscar-fish-care/water-parameters/",   "\U0001F321️ Water & Temperature"),
    ("/guides/oscar-fish-care/food/",               "\U0001F35A Food & Feeding"),
    ("/guides/oscar-fish-care/size-growth/",        "\U0001F4CF Size & Growth"),
    ("/guides/oscar-fish-care/lifespan/",           "⏳ Lifespan"),
    ("/guides/oscar-fish-care/types/",              "\U0001F3A8 Types & Colors"),
    ("/guides/oscar-fish-care/male-vs-female/",     "⚖️ Male vs Female"),
    ("/guides/oscar-fish-care/breeding/",           "\U0001F95A Breeding & Babies"),
    ("/guides/oscar-fish-care/tank-mates/",         "\U0001F420 Tank Mates"),
    ("/guides/oscar-fish-care/behavior/",           "\U0001F620 Aggression & Behavior"),
    ("/guides/oscar-fish-care/diseases/",           "\U0001FA7A Diseases & Parasites"),
    ("/guides/oscar-fish-care/not-eating/",         "\U0001F6AB Not Eating & Hiding"),
    ("/guides/oscar-fish-care/color-change/",       "⚫ Color Changes"),
    ("/guides/oscar-fish-care/white-spots/",        "⚪ White Spots (Ich)"),
    ("/guides/oscar-fish-care/hole-in-the-head/",   "\U0001F573️ Hole in the Head"),
    ("/guides/oscar-fish-care/swimming-problems/",  "\U0001F300 Swimming & Breathing"),
    ("/species/oscar",                                "\U0001F4D6 Species Profile"),
]

TOOL_LINKS = [
    ("/calculators/oscar-fish-tank-size/", "Oscar Tank Size Calculator"),
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
.guide-hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.9),rgba(15,61,94,.7)),url('/assets/encyclopedia/real/oscar-fish-wikimedia-real.jpg') center/cover no-repeat}
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
.tblwrap{overflow-x:auto;margin:16px 0}
.ptbl{width:100%;border-collapse:collapse;font-size:.86rem;border-radius:16px;overflow:hidden;box-shadow:0 12px 30px rgba(15,61,110,.08)}
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
            is_cur = href == "/guides/oscar-fish-care/"
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
    return ('    <h2 id="related">Related Oscar Fish Guides and Tools</h2>\n'
            f'    <div class="guide-links">{items}</div>')


def page(slug, title, meta_desc, h1, hero_tag, hero_meta,
         toc_sections, body_html, faqs, related, date=DATE):
    canonical = f"https://www.fishcareai.com/guides/oscar-fish-care/{slug}/"
    crumb_tail = (
        '<a href="/guides/oscar-fish-care/">Oscar Fish Care Guide</a><span>/</span>\n      '
        f'<span style="color:rgba(255,255,255,.9)">{hero_tag}</span>'
    )
    breadcrumb_json = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},'
        '{"@type":"ListItem","position":2,"name":"Guides","item":"https://www.fishcareai.com/guides/"},'
        '{"@type":"ListItem","position":3,"name":"Oscar Fish Care Guide",'
        '"item":"https://www.fishcareai.com/guides/oscar-fish-care/"},'
        f'{{"@type":"ListItem","position":4,"name":{json.dumps(h1)},"item":"{canonical}"}}]}}'
    )
    article_json = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": meta_desc,
        "datePublished": date, "dateModified": date,
        "image": f"https://www.fishcareai.com{HERO_IMG}",
        "about": {"@type": "Thing", "name": "Oscar fish (Astronotus ocellatus)"},
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
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">&#128031; Oscar Fish Care</div>
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
      <h4>Oscar Fish Care</h4>
      {cluster_nav_html(slug)}
    </div>
    <div class="toc">
      <h4>On this page</h4>
      {toc_html(toc)}
    </div>
    <div class="tool-card">
      <h4>Oscar Fish Tools</h4>
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
# TANK SIZE
# ════════════════════════════════════════════════════════════════
TANK_BODY = """    <p>The single most common oscar mistake is buying a 2-inch fish for a 30-gallon tank. That fish grows roughly an inch a month for its first year and finishes at 10&ndash;14 inches, so the tank that fits it today is undersized by Christmas. Plan the tank around the adult, not the juvenile in the bag.</p>

    <h2 id="minimum">Minimum Tank Size for One Oscar</h2>
    <p><strong>Seventy-five gallons is the working minimum for one adult oscar.</strong> You will still see 55 gallons quoted, and a single oscar can physically survive in one &mdash; but a 55 is only 12 inches front to back, which means a 13-inch fish cannot turn around without bending. Every experienced oscar keeper who starts at 55 gallons ends up upgrading.</p>
    <p>The reason is not just length. Oscars are among the messiest freshwater fish sold: they tear food apart rather than swallowing it, they rearrange substrate constantly, and they produce a nitrate load closer to a goldfish pond than a community tank. Water volume is your buffer against that, and 75 gallons is where the buffer starts working.</p>
    <div class="callout"><strong>Quick rule.</strong> 75 gallons for the first oscar, then add roughly 50&ndash;60 gallons for each additional oscar. Round up, never down &mdash; crowding is the direct cause of most oscar aggression problems.</div>

    <h2 id="by-number">Tank Size by Number of Oscars</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Setup</th><th>Minimum tank</th><th>Comfortable tank</th><th>Notes</th></tr>
      <tr><td>1 oscar</td><td>75 gallons</td><td>90&ndash;125 gallons</td><td>48&times;18 inch footprint or larger</td></tr>
      <tr><td>2 oscars (pair)</td><td>125 gallons</td><td>150 gallons</td><td>Two territories, one tank &mdash; length matters most</td></tr>
      <tr><td>3 oscars</td><td>180 gallons</td><td>210 gallons</td><td>Odd numbers spread aggression better than pairs</td></tr>
      <tr><td>1 oscar + large tank mates</td><td>125 gallons</td><td>180 gallons</td><td>See <a href="/guides/oscar-fish-care/tank-mates/">oscar tank mates</a></td></tr>
      <tr><td>Juvenile grow-out (under 4 in)</td><td>40 gallons</td><td>&mdash;</td><td>Temporary only &mdash; 3&ndash;5 months maximum</td></tr>
    </table></div>
    <p>Work out the volume of a tank you already own, or the tank a given oscar needs, with the <a href="/calculators/oscar-fish-tank-size/">oscar fish tank size calculator</a>.</p>

    <h2 id="dimensions">Dimensions Matter More Than Gallons</h2>
    <p>Two tanks can both hold 75 gallons and only one of them is an oscar tank. What you are buying is floor space:</p>
    <ul>
      <li><strong>Length: 48 inches minimum.</strong> An oscar turns by pivoting its whole body. Anything shorter than four feet forces a large adult into a permanent three-point turn.</li>
      <li><strong>Front to back: 18 inches minimum.</strong> This is the dimension that separates a standard 75 (48&times;18&times;21) from a standard 55 (48&times;13&times;21), and it is why the 75 works and the 55 does not.</li>
      <li><strong>Height: largely irrelevant.</strong> Oscars use the bottom two-thirds of the tank. Tall show tanks and hex tanks waste water volume on space the fish never occupies.</li>
    </ul>
    <p>If you are choosing between a 90-gallon (48&times;18&times;24) and a 75-gallon (48&times;18&times;21), the extra height buys you dilution but not swimming room. A 125-gallon (72&times;18&times;22) buys you both, and it is the tank most long-term oscar keepers settle on.</p>

    <h2 id="juveniles">Can a Juvenile Oscar Start Smaller?</h2>
    <p>Yes, briefly. A 2&ndash;3 inch oscar in a 40-gallon grow-out tank is fine for three to five months, and some keepers prefer it because a small fish in a big tank can be hard to feed and monitor. What makes it work is a hard deadline: at 5&ndash;6 inches the fish moves to its permanent tank, no exceptions.</p>
    <div class="callout callout-warn"><strong>Stunting is not a size control.</strong> An oscar kept in a small tank does not stay small and healthy &mdash; its body growth slows while its internal organs keep developing, which shortens life and causes spinal and swim bladder problems. See <a href="/guides/oscar-fish-care/size-growth/">oscar fish size and growth rate</a>.</div>

    <h2 id="filtration">Filtration and Water Changes</h2>
    <p>Filter for roughly <strong>6&ndash;8 times the tank volume per hour</strong>, which means a 75-gallon oscar tank wants 450&ndash;600 GPH of real, in-tank flow rate. In practice that is one large canister rated well above your volume, or a canister plus a sponge filter, or a sump if you have the space.</p>
    <ul>
      <li><strong>Mechanical media first.</strong> Oscars generate visible debris; coarse foam and filter floss that you rinse weekly keep it out of the biomedia.</li>
      <li><strong>Oversize the biomedia.</strong> Waste load, not tank size, sets how much bacteria surface you need.</li>
      <li><strong>Water changes: 30&ndash;50% weekly.</strong> Non-negotiable. Nitrate creep is the number one driver of <a href="/guides/oscar-fish-care/hole-in-the-head/">hole-in-the-head disease</a> in oscars.</li>
      <li><strong>Keep flow moderate at the surface.</strong> Oscars are strong swimmers but they do not enjoy being blasted; aim the return along the glass rather than into the open swimming lane.</li>
    </ul>

    <h2 id="setup">Substrate, Decor and Lid</h2>
    <p>Oscars redecorate. They will move gravel into piles, uproot plants, and shove anything they can get their mouth around. Set the tank up so that behavior is harmless rather than trying to stop it:</p>
    <ul>
      <li><strong>Substrate:</strong> fine sand or smooth medium gravel, 1&ndash;2 inches deep. Sharp gravel scrapes mouths when they dig. Bare bottom is legitimate and by far the easiest to keep clean.</li>
      <li><strong>Rock and wood:</strong> stack rock directly on the glass (or on an eggcrate base), never on top of sand &mdash; an oscar digging underneath a rock pile can bring it down. Large driftwood pieces are ideal and help lower pH slightly.</li>
      <li><strong>Plants:</strong> anything rooted gets pulled up. Use anubias or java fern glued to wood, or plastic plants you can re-anchor.</li>
      <li><strong>Heater:</strong> guarded or, better, an inline or sump heater. Oscars have broken glass heaters.</li>
      <li><strong>Lid:</strong> a tight, weighted one. Oscars jump, especially when startled or newly moved. See <a href="/guides/oscar-fish-care/behavior/">oscar behavior and aggression</a>.</li>
    </ul>

    <h2 id="mistakes">Five Tank Mistakes That Cost Oscars</h2>
    <ol>
      <li><strong>Buying the fish before the tank.</strong> The juvenile is cheap; the 125-gallon tank, stand and filter are not. Price the whole setup first.</li>
      <li><strong>Tall tanks.</strong> Hex and cube tanks trade the footprint an oscar needs for height it will not use.</li>
      <li><strong>Underfiltering.</strong> A filter rated "up to 100 gallons" on a lightly stocked community tank is a filter rated for maybe 50 gallons of oscar.</li>
      <li><strong>Loose decor near glass.</strong> An oscar shunting a rock into the side panel is a real way to crack a tank.</li>
      <li><strong>No quarantine tank.</strong> A 20-gallon spare doubles as a hospital tank, and treating a sick oscar in the display tank means dosing 75+ gallons of medication.</li>
    </ol>
"""

TANK = {
    "slug": "tank-size",
    "title": "Oscar Fish Tank Size: Minimum Gallons for 1, 2 or 3 Oscars",
    "meta_desc": "How big a tank an oscar fish needs: 75 gallons minimum for one adult, 125 for a pair. Tank dimensions, filtration rates, substrate, lids and grow-out advice.",
    "h1": "Oscar Fish Tank Size and Aquarium Setup",
    "hero_tag": "Tank Size & Setup",
    "hero_meta": "\U0001F5C3️ 75 gal minimum &nbsp;|&nbsp; \U0001F4CF 48-inch footprint &nbsp;|&nbsp; ⚡ 6&ndash;8&times; turnover &nbsp;|&nbsp; \U0001F4A7 30&ndash;50% weekly",
    "toc_sections": [
        ("minimum", "Minimum for One Oscar"),
        ("by-number", "Tank Size by Number"),
        ("dimensions", "Dimensions Matter More"),
        ("juveniles", "Starting Smaller"),
        ("filtration", "Filtration & Water Changes"),
        ("setup", "Substrate, Decor & Lid"),
        ("mistakes", "Five Tank Mistakes"),
    ],
    "body": TANK_BODY,
    "faqs": [
        ("What size tank does an oscar fish need?",
         "One adult oscar needs 75 gallons as a working minimum, with 90-125 gallons preferred. A pair needs 125 gallons and three oscars need 180 gallons. The tank should be at least 48 inches long and 18 inches front to back so the fish can turn around freely."),
        ("Can an oscar fish live in a 55 gallon tank?",
         "A single oscar can survive in a 55 gallon, but a standard 55 is only 13 inches front to back, which is narrower than a full-grown oscar is long. Most keepers who start at 55 gallons upgrade within a year, so buying 75 gallons or larger from the start is cheaper."),
        ("Can an oscar fish live in a 30 gallon tank?",
         "Only as temporary grow-out space for a fish under about 4 inches, and only for a few months. Oscars grow roughly an inch a month in their first year, so a 30 gallon is outgrown quickly and long-term confinement stunts the fish and shortens its life."),
        ("How many oscars can I keep in a 125 gallon tank?",
         "Two adult oscars comfortably, or three if the tank is heavily filtered and well broken up with rock and wood. Odd-numbered groups spread aggression better than pairs, because two oscars that fall out have nowhere to redirect."),
        ("Do oscar fish need a lid on the tank?",
         "Yes. Oscars are strong, easily startled fish that jump, particularly in the first weeks after a move or when they are chased. A tight, weighted lid is standard equipment on an oscar tank."),
        ("What kind of filter does an oscar tank need?",
         "Aim for 6-8 times the tank volume per hour, so 450-600 GPH on a 75 gallon. A large canister filter, a canister plus sponge filter, or a sump all work. Oversize the mechanical media, because oscars tear food apart and generate visible debris."),
    ],
    "related": [
        ("/calculators/oscar-fish-tank-size/", "Oscar Tank Size Calculator"),
        ("/guides/oscar-fish-care/size-growth/", "Oscar Size & Growth Rate"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Temperature & Parameters"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# WATER PARAMETERS
# ════════════════════════════════════════════════════════════════
WATER_BODY = """    <p>Oscars are hardy fish with a narrow tolerance for one thing only: dirty water. They forgive a pH that is not textbook perfect and shrug off hardness that would bother a discus, but they respond badly and quickly to ammonia, nitrite and accumulated nitrate. Get the numbers below right and most oscar health problems never start.</p>

    <h2 id="quick-table">Oscar Fish Water Parameters at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parameter</th><th>Acceptable range</th><th>Target</th></tr>
      <tr><td>Temperature</td><td>74&ndash;81&deg;F (23&ndash;27&deg;C)</td><td>77&ndash;80&deg;F (25&ndash;27&deg;C)</td></tr>
      <tr><td>pH</td><td>6.0&ndash;8.0</td><td>6.5&ndash;7.5, stable</td></tr>
      <tr><td>General hardness (GH)</td><td>5&ndash;20 dGH</td><td>8&ndash;12 dGH</td></tr>
      <tr><td>Carbonate hardness (KH)</td><td>4&ndash;15 dKH</td><td>6&ndash;10 dKH</td></tr>
      <tr><td>Ammonia (NH<sub>3</sub>)</td><td>0 ppm</td><td>0 ppm, always</td></tr>
      <tr><td>Nitrite (NO<sub>2</sub>)</td><td>0 ppm</td><td>0 ppm, always</td></tr>
      <tr><td>Nitrate (NO<sub>3</sub>)</td><td>Under 40 ppm</td><td>Under 20 ppm</td></tr>
      <tr><td>Water change</td><td>25&ndash;50% weekly</td><td>40&ndash;50% weekly</td></tr>
    </table></div>
    <p>Score your own readings against these ranges with the <a href="/tools/water-parameter-checker/">water parameter checker</a>.</p>

    <h2 id="temperature">Oscar Fish Water Temperature</h2>
    <p>Keep an oscar tank at <strong>77&ndash;80&deg;F (25&ndash;27&deg;C)</strong>. The wider survivable range is 74&ndash;81&deg;F, and oscars come from warm, slow Amazon basin waters that sit in the upper half of that band year-round.</p>
    <p>What the temperature actually controls:</p>
    <ul>
      <li><strong>Below 74&deg;F</strong> the immune system slows down. Chronically cool oscars are the ones that catch ich, develop fin rot and stop eating for no obvious reason.</li>
      <li><strong>Above 82&deg;F</strong> dissolved oxygen drops while the fish's metabolism rises. Sustained heat is a common reason for <a href="/guides/oscar-fish-care/swimming-problems/">an oscar gasping at the surface</a>.</li>
      <li><strong>82&ndash;86&deg;F short term</strong> is a legitimate treatment temperature for ich, held for the length of the course with extra aeration.</li>
    </ul>
    <p>Use a heater rated 3&ndash;5 watts per gallon, and use two smaller heaters rather than one large one on tanks over 75 gallons &mdash; if one fails on, it cannot cook the tank alone; if one fails off, the other holds the line. Guard the glass or run the heater in a sump: oscars have broken heaters by shoving them.</p>
    <div class="callout"><strong>Stability beats the ideal number.</strong> A tank that sits at a steady 76&deg;F is healthier than one that swings between 75&deg;F and 82&deg;F chasing 79&deg;F. Check the temperature with an independent thermometer, not the dial on the heater.</div>

    <h2 id="ph">Oscar Fish pH</h2>
    <p>Oscars accept <strong>pH 6.0 to 8.0</strong> and thrive anywhere from 6.5 to 7.5. Wild fish live in soft, acidic blackwater around pH 6.0&ndash;6.5, but virtually every oscar in the trade is tank-bred and has never seen those conditions.</p>
    <p>The practical advice is simple: <strong>match your tap water and leave it alone.</strong> If your water comes out at 7.8 and holds there, keep the fish at 7.8. Chasing a lower number with pH-down products, peat or driftwood dosing produces exactly the swings oscars do not tolerate. The one time to intervene is when pH is drifting on its own, which is a KH problem, not a pH problem.</p>

    <h2 id="hardness">Hardness, KH and pH Crashes</h2>
    <p>Carbonate hardness (KH) is the buffer that stops pH moving. Oscar tanks are heavily fed and heavily stocked, so they generate acid fast; if KH falls below about 4 dKH, pH can crash overnight and take the fish with it.</p>
    <ul>
      <li><strong>Test KH monthly</strong> even if pH looks stable. Falling KH is the early warning; falling pH is the emergency.</li>
      <li><strong>If KH is low</strong>, raise it gently with crushed coral in the filter or a small dose of baking soda calculated for your volume, and increase water change frequency.</li>
      <li><strong>GH of 5&ndash;20 dGH</strong> is fine. Oscars are not fussy about general hardness and there is no reason to soften or remineralise water for them.</li>
    </ul>

    <h2 id="nitrogen">Ammonia, Nitrite and Nitrate</h2>
    <p>Ammonia and nitrite must read <strong>0 ppm at all times</strong>. Anything above zero is an active emergency: change 50% of the water, stop feeding, and dose a detoxifier while you find the cause.</p>
    <p>Nitrate is the number that quietly separates a good oscar tank from a bad one. It is not acutely toxic, so a tank can run at 80&ndash;100 ppm for months while the fish looks fine &mdash; and then the fish develops faded color, lethargy, and pitting above the eyes. <strong>Keep nitrate under 40 ppm, and under 20 ppm if you can.</strong> That is achieved with water changes, not with products.</p>
    <div class="callout callout-warn"><strong>New tank syndrome kills oscars fast.</strong> An oscar is a large bioload dropped into a small bacterial colony. Cycle the tank fully before the fish arrives, or run a fishless cycle with ammonia until the tank processes 2 ppm to zero nitrite in 24 hours. Never cycle a tank with an oscar in it.</div>

    <h2 id="changes">Water Change Routine</h2>
    <p>The standard oscar routine is <strong>40&ndash;50% once a week</strong>, or 25&ndash;30% twice a week on a heavily stocked tank. Two details matter more than the exact percentage:</p>
    <ul>
      <li><strong>Match the temperature.</strong> Refill within a couple of degrees of the tank. Cold refills are a classic ich trigger.</li>
      <li><strong>Dechlorinate every time.</strong> Chloramine in particular will damage gills and stall the filter's bacteria.</li>
      <li><strong>Vacuum the substrate</strong> where the oscar feeds. Uneaten pellet fragments buried in sand are where nitrate comes from.</li>
      <li><strong>Rinse mechanical media weekly</strong> in old tank water, and biomedia rarely and gently.</li>
    </ul>

    <h2 id="testing">What to Test and How Often</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Test</th><th>New tank</th><th>Established tank</th></tr>
      <tr><td>Ammonia &amp; nitrite</td><td>Daily</td><td>Monthly, plus any time behavior changes</td></tr>
      <tr><td>Nitrate</td><td>Every 2&ndash;3 days</td><td>Weekly, before the water change</td></tr>
      <tr><td>pH</td><td>Weekly</td><td>Monthly</td></tr>
      <tr><td>KH</td><td>Weekly</td><td>Monthly</td></tr>
      <tr><td>Temperature</td><td>Daily</td><td>Daily (glance at the thermometer)</td></tr>
    </table></div>
    <p>Use a liquid test kit rather than strips for ammonia and nitrate. Strips are fine for a quick pH or KH trend but are not accurate enough for the readings that matter on an oscar tank.</p>

    <h2 id="troubleshooting">Reading the Fish Instead of the Numbers</h2>
    <p>Oscars telegraph water problems before a test kit is opened. Any of these means test immediately:</p>
    <ul>
      <li>Sitting on the bottom or hovering in a corner &mdash; see <a href="/guides/oscar-fish-care/not-eating/">oscar not eating or hiding</a>.</li>
      <li>Rapid gill movement or hanging at the surface &mdash; oxygen, ammonia or gill irritation.</li>
      <li>Colors going pale or dark within hours &mdash; a stress response, often to a parameter swing.</li>
      <li>Clamped fins, or scratching against decor.</li>
      <li>Refusing food for more than two days when nothing else changed.</li>
    </ul>
"""

WATER = {
    "slug": "water-parameters",
    "title": "Oscar Fish Water Temperature, pH and Water Parameters",
    "meta_desc": "Oscar fish water temperature is 74-81F, ideally 77-80F, with pH 6.5-7.5 and nitrate under 20 ppm. Full parameter table, testing and water change routine.",
    "h1": "Oscar Fish Water Temperature and Water Parameters",
    "hero_tag": "Water & Temperature",
    "hero_meta": "\U0001F321️ 77&ndash;80&deg;F &nbsp;|&nbsp; \U0001F9EA pH 6.5&ndash;7.5 &nbsp;|&nbsp; \U0001F4A7 Nitrate under 20 ppm &nbsp;|&nbsp; \U0001F504 40&ndash;50% weekly",
    "toc_sections": [
        ("quick-table", "Parameters at a Glance"),
        ("temperature", "Water Temperature"),
        ("ph", "Oscar Fish pH"),
        ("hardness", "Hardness & KH"),
        ("nitrogen", "Ammonia, Nitrite, Nitrate"),
        ("changes", "Water Change Routine"),
        ("testing", "What to Test"),
        ("troubleshooting", "Reading the Fish"),
    ],
    "body": WATER_BODY,
    "faqs": [
        ("What water temperature do oscar fish need?",
         "Keep oscar fish at 77-80F (25-27C). The wider tolerated range is 74-81F. Below 74F their immune system slows and disease becomes more likely; above 82F dissolved oxygen falls while their oxygen demand rises."),
        ("What pH do oscar fish need?",
         "Oscars accept pH 6.0 to 8.0 and do best between 6.5 and 7.5. Because almost all oscars sold are tank-bred, matching your tap water and keeping it stable matters far more than hitting a specific number."),
        ("Can oscar fish live without a heater?",
         "Only in a room that reliably stays at 75-80F day and night, which almost no home does. A heater is standard equipment for oscars, and on tanks over 75 gallons two smaller heaters are safer than one large one."),
        ("What nitrate level is safe for oscar fish?",
         "Keep nitrate under 40 ppm and ideally under 20 ppm. Nitrate is not acutely toxic, so a tank can sit high for months while the fish looks fine, but chronic nitrate is strongly linked to faded colour, lethargy and hole-in-the-head disease in oscars."),
        ("How often should I change the water in an oscar tank?",
         "Change 40-50% once a week, or 25-30% twice a week on a heavily stocked tank. Match the refill temperature to within a couple of degrees, dechlorinate every time, and vacuum the substrate where the oscar feeds."),
        ("Do oscar fish need hard or soft water?",
         "Neither in particular. Oscars are comfortable from 5 to 20 dGH. What does matter is carbonate hardness (KH): keep it above about 4 dKH so heavy feeding cannot cause an overnight pH crash."),
    ],
    "related": [
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size & Setup"),
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases & Parasites"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# FOOD & FEEDING
# ════════════════════════════════════════════════════════════════
FOOD_BODY = """    <p>Oscars will eat almost anything you put in the tank, which is exactly why so many of them are fed badly. They are opportunistic omnivores that lean carnivorous, and the difference between a 10-year oscar and a 5-year oscar is usually diet and water quality rather than genetics.</p>

    <h2 id="what-they-eat">What Do Oscar Fish Eat in the Wild?</h2>
    <p>Wild oscars in the Amazon basin eat <strong>insects and insect larvae, crustaceans, snails, small fish, and a surprising amount of plant material</strong> &mdash; fruit and seeds that fall into flooded forest. Stomach content studies consistently find catfish and small cichlids alongside shrimp and vegetable matter.</p>
    <p>Two things follow from that. First, an oscar needs animal protein as the base of its diet. Second, it is not a pure predator, and a diet of nothing but protein produces the fatty liver disease that shows up in necropsies of aquarium oscars. The captive diet should mirror the wild ratio: mostly protein, with regular vegetable content.</p>

    <h2 id="best-food">The Best Food for Oscar Fish</h2>
    <p><strong>A quality sinking or slow-sinking cichlid pellet is the staple &mdash; roughly 70&ndash;80% of everything the fish eats.</strong> Look for a pellet with whole fish or krill meal as the first ingredient, 35&ndash;45% crude protein, and added vitamin C and astaxanthin. Pellet size should match the mouth: an adult oscar takes a large (7&ndash;10 mm) pellet comfortably.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Food type</th><th>Role</th><th>How often</th></tr>
      <tr><td>Large cichlid pellets</td><td>Staple, 70&ndash;80% of diet</td><td>Every feeding</td></tr>
      <tr><td>Frozen krill, mysis, prawn</td><td>Protein and colour</td><td>2&ndash;3 times a week</td></tr>
      <tr><td>Earthworms, blackworms</td><td>Best single treat &mdash; excellent protein</td><td>1&ndash;2 times a week</td></tr>
      <tr><td>Blanched peas, deshelled</td><td>Fibre; also the fix for constipation</td><td>Weekly</td></tr>
      <tr><td>Spirulina or veggie pellets</td><td>Plant content</td><td>1&ndash;2 times a week</td></tr>
      <tr><td>Crickets, mealworms (gut-loaded)</td><td>Enrichment</td><td>Occasional</td></tr>
      <tr><td>Freeze-dried krill</td><td>Hand-feeding and training</td><td>Occasional, pre-soaked</td></tr>
    </table></div>
    <p>Frozen food should be thawed in tank water before it goes in, and freeze-dried food soaked for a minute. Dry food that expands in the gut is a common cause of the bloating covered in <a href="/guides/oscar-fish-care/swimming-problems/">oscar swimming problems</a>.</p>

    <h2 id="how-often">How Often to Feed an Oscar Fish</h2>
    <p>Feeding frequency drops as the fish grows. A juvenile is building a body at nearly an inch a month; an adult is maintaining one.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Age / size</th><th>Meals per day</th><th>Portion</th></tr>
      <tr><td>Fry to 2 inches</td><td>3&ndash;4</td><td>What is eaten in 1&ndash;2 minutes</td></tr>
      <tr><td>2&ndash;4 inches</td><td>3</td><td>What is eaten in 2 minutes</td></tr>
      <tr><td>4&ndash;8 inches</td><td>2</td><td>What is eaten in 2&ndash;3 minutes</td></tr>
      <tr><td>8 inches and up (adult)</td><td>1, or every other day</td><td>What is eaten in 3 minutes</td></tr>
    </table></div>
    <p>Adults genuinely do well on a feed-one-day, skip-one-day schedule, and many long-lived oscars are kept that way. Add <strong>one fasting day a week</strong> at any age &mdash; it clears the gut and costs the fish nothing.</p>
    <p>To size portions for your specific tank and stocking, use the <a href="/tools/fish-feeding-calculator/">fish feeding calculator</a>.</p>
    <div class="callout"><strong>The 3-minute rule.</strong> Feed only what the oscar finishes in about three minutes, then net out anything left. An oscar begging at the glass is not a hungry oscar &mdash; it is a fish that has learned you respond. They beg permanently.</div>

    <h2 id="chart">Weekly Oscar Feeding Chart</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Day</th><th>Adult oscar (8 in+)</th><th>Juvenile (4&ndash;8 in)</th></tr>
      <tr><td>Monday</td><td>Cichlid pellets</td><td>Pellets AM, pellets PM</td></tr>
      <tr><td>Tuesday</td><td>Frozen krill or mysis</td><td>Pellets AM, frozen krill PM</td></tr>
      <tr><td>Wednesday</td><td>Fast day</td><td>Pellets AM, pellets PM</td></tr>
      <tr><td>Thursday</td><td>Cichlid pellets</td><td>Pellets AM, earthworm PM</td></tr>
      <tr><td>Friday</td><td>Earthworms or blackworms</td><td>Pellets AM, pellets PM</td></tr>
      <tr><td>Saturday</td><td>Pellets + blanched pea</td><td>Pellets AM, blanched pea PM</td></tr>
      <tr><td>Sunday</td><td>Spirulina or veggie pellets</td><td>Pellets AM, spirulina PM</td></tr>
    </table></div>

    <h2 id="feeder-fish">Why Not to Feed Feeder Fish</h2>
    <p>Feeder goldfish and rosy reds are the traditional oscar food and one of the worst things you can give the fish. Three separate problems:</p>
    <ul>
      <li><strong>Thiaminase.</strong> Goldfish and other cyprinids contain an enzyme that destroys vitamin B1. A long-term feeder diet produces thiamine deficiency &mdash; neurological symptoms, poor growth and reduced lifespan.</li>
      <li><strong>Disease.</strong> Feeder tanks at the store are crowded, unfiltered and untreated. Ich, columnaris and internal parasites arrive with the fish.</li>
      <li><strong>Fat.</strong> Goldfish are fatty, and fatty liver disease is routine in oscars fed this way.</li>
    </ul>
    <p>If you want live food for enrichment, use gut-loaded crickets, earthworms from a clean source, or ghost shrimp quarantined for a fortnight. None of them carry the same risks.</p>
    <div class="callout callout-warn"><strong>Also avoid:</strong> mammalian meat such as beef heart or chicken (oscars cannot process the saturated fat), bread, and any dry food more than about six months past opening &mdash; vitamin C degrades quickly and vitamin deficiency is one of the drivers of <a href="/guides/oscar-fish-care/hole-in-the-head/">hole-in-the-head</a>.</div>

    <h2 id="refusing">When an Oscar Refuses Food</h2>
    <p>A healthy adult oscar can go a week without food and be perfectly fine, so a skipped meal is not a crisis. Treat it as a signal to check things in this order:</p>
    <ol>
      <li><strong>Test the water.</strong> Ammonia, nitrite, nitrate. Loss of appetite is often the first symptom of a water problem.</li>
      <li><strong>Check temperature.</strong> A tank that has drifted below 74&deg;F will slow feeding.</li>
      <li><strong>Consider recent changes.</strong> New tank, new tank mate, moved decor, new food brand. Oscars sulk after change and usually resume within a week.</li>
      <li><strong>Look at the fish.</strong> Pitting, white spots, stringy white faeces, a swollen belly, or laboured breathing all move this from fussiness to illness.</li>
    </ol>
    <p>Full diagnostic walkthrough: <a href="/guides/oscar-fish-care/not-eating/">oscar fish not eating</a>.</p>

    <h2 id="overfeeding">Signs You Are Overfeeding</h2>
    <ul>
      <li>Nitrate climbing above 40 ppm between weekly water changes.</li>
      <li>Uneaten pellets in the substrate an hour after feeding.</li>
      <li>A visibly rounded belly that stays rounded, or trailing white faeces.</li>
      <li>Persistent surface film and cloudy water.</li>
      <li>A fish that has grown fast but looks thick and short rather than long.</li>
    </ul>
    <p>Overfeeding is the more common error by a wide margin. Oscars beg convincingly and there is no oscar in the hobby that has starved from a missed meal.</p>
"""

FOOD = {
    "slug": "food",
    "title": "What Do Oscar Fish Eat? Best Food and Feeding Chart",
    "meta_desc": "What to feed oscar fish, the best pellets and treats, how often to feed by size, a weekly feeding chart, and why feeder goldfish shorten an oscar's life.",
    "h1": "Oscar Fish Food, Feeding Chart and How Often to Feed",
    "hero_tag": "Food & Feeding",
    "hero_meta": "\U0001F35A Pellet staple &nbsp;|&nbsp; \U0001F551 1&ndash;3 meals by size &nbsp;|&nbsp; ⏱️ 3-minute rule &nbsp;|&nbsp; \U0001F6AB No feeder fish",
    "toc_sections": [
        ("what-they-eat", "What Oscars Eat"),
        ("best-food", "Best Food for Oscars"),
        ("how-often", "How Often to Feed"),
        ("chart", "Weekly Feeding Chart"),
        ("feeder-fish", "Why Not Feeder Fish"),
        ("refusing", "When They Refuse Food"),
        ("overfeeding", "Signs of Overfeeding"),
    ],
    "body": FOOD_BODY,
    "faqs": [
        ("What do oscar fish eat?",
         "Oscars are opportunistic omnivores that lean carnivorous. In the wild they eat insects, crustaceans, snails, small fish and fallen fruit and seeds. In an aquarium the staple should be a large quality cichlid pellet, with frozen krill or mysis, earthworms, and vegetable foods such as blanched peas and spirulina in rotation."),
        ("What is the best food for oscar fish?",
         "A large sinking or slow-sinking cichlid pellet with whole fish or krill meal as the first ingredient, 35-45% crude protein and added vitamin C. That should make up 70-80% of the diet, with frozen and vegetable foods filling the rest."),
        ("How often should I feed my oscar fish?",
         "Fry and fish under 2 inches eat 3-4 times a day, 2-4 inch juveniles 3 times, 4-8 inch fish twice, and adults over 8 inches once daily or every other day. Add one fasting day a week at any age."),
        ("Can oscar fish eat feeder goldfish?",
         "They can, but they should not. Goldfish contain thiaminase, which destroys vitamin B1 and causes deficiency over time; feeder tanks are a reliable source of ich, columnaris and internal parasites; and goldfish are fatty enough to contribute to fatty liver disease."),
        ("How long can an oscar fish go without food?",
         "A healthy adult oscar can go one to two weeks without food without harm, which is why fasting days and holiday gaps are not a problem. A juvenile should not miss more than a couple of days because it is still growing quickly."),
        ("Why is my oscar fish spitting out its food?",
         "Usually the pellet is too large or too hard, and the fish is softening it. Oscars also spit food when they are stressed by a recent move or a new tank mate, and when water quality is off. If it continues for several days alongside other symptoms, test the water and check for hole-in-the-head pitting."),
    ],
    "related": [
        ("/tools/fish-feeding-calculator/", "Fish Feeding Calculator"),
        ("/guides/oscar-fish-care/not-eating/", "Oscar Not Eating"),
        ("/guides/oscar-fish-care/size-growth/", "Oscar Size & Growth"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# SIZE & GROWTH
# ════════════════════════════════════════════════════════════════
SIZE_BODY = """    <p>Oscars are sold at two inches and finish at twelve or more. That growth curve &mdash; roughly an inch a month through the first year &mdash; is the single fact that determines whether an oscar purchase works out, because the tank has to be ready before the fish needs it, not after.</p>

    <h2 id="how-big">How Big Do Oscar Fish Get?</h2>
    <p><strong>Aquarium oscars reach 10&ndash;14 inches (25&ndash;35 cm) and 2&ndash;3.5 lb.</strong> Twelve inches is the typical adult in a well-kept 75&ndash;125 gallon tank. Wild fish and exceptional aquarium specimens reach 16&ndash;18 inches (40&ndash;45 cm), and the recorded maximum for <em>Astronotus ocellatus</em> is around 18 inches.</p>
    <p>Body shape matters as much as length. A healthy adult oscar is a deep, oval, muscular fish roughly a third as tall as it is long &mdash; a 12-inch oscar is a substantially bigger animal than a 12-inch fish of most other species, which is why the tank requirement is so much higher than length alone suggests.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Measure</th><th>Typical aquarium</th><th>Maximum recorded</th></tr>
      <tr><td>Length</td><td>10&ndash;14 in (25&ndash;35 cm)</td><td>~18 in (45 cm)</td></tr>
      <tr><td>Weight</td><td>2&ndash;3.5 lb (0.9&ndash;1.6 kg)</td><td>~3.5 lb (1.6 kg)</td></tr>
      <tr><td>Body depth</td><td>4&ndash;5 in at the dorsal</td><td>6 in</td></tr>
      <tr><td>Age at full size</td><td>2&ndash;3 years</td><td>&mdash;</td></tr>
    </table></div>

    <h2 id="growth-rate">Oscar Fish Growth Rate by Age</h2>
    <p>Oscars grow fastest in the first twelve months and then slow sharply. Expect roughly <strong>1 inch per month for the first year</strong>, then a couple of inches over the second year, then very little.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Age</th><th>Expected length</th><th>What is happening</th></tr>
      <tr><td>Hatching</td><td>~0.3 in</td><td>Yolk sac, not free-swimming</td></tr>
      <tr><td>1 month</td><td>0.75&ndash;1 in</td><td>Free-swimming fry, feeding constantly</td></tr>
      <tr><td>3 months</td><td>2.5&ndash;3.5 in</td><td>Usual store size</td></tr>
      <tr><td>6 months</td><td>5&ndash;7 in</td><td>Fastest growth phase; adult colours appearing</td></tr>
      <tr><td>9 months</td><td>7&ndash;9 in</td><td>Needs its permanent tank by now</td></tr>
      <tr><td>12 months</td><td>9&ndash;11 in</td><td>Growth begins to slow</td></tr>
      <tr><td>18 months</td><td>10&ndash;12 in</td><td>Sexual maturity typically reached</td></tr>
      <tr><td>2&ndash;3 years</td><td>11&ndash;14 in</td><td>Full adult size; growth essentially finished</td></tr>
    </table></div>
    <p>Individual variation is wide. Two oscars from the same spawn can differ by two inches at a year old on identical food, so use the table as a trend rather than a target.</p>

    <h2 id="what-affects">What Actually Controls Growth</h2>
    <ul>
      <li><strong>Water quality.</strong> The largest single factor. Fish in tanks with nitrate consistently under 20 ppm grow faster and finish larger than the same fish in a tank running at 60 ppm.</li>
      <li><strong>Tank size.</strong> Not because of the "grows to its tank" myth, but because a small tank means high waste concentration, which suppresses growth and damages organs.</li>
      <li><strong>Diet quality.</strong> A varied protein-led diet built on a good pellet outgrows a flake or feeder-fish diet substantially.</li>
      <li><strong>Feeding frequency in the first year.</strong> Two to three meals a day for a juvenile, not one.</li>
      <li><strong>Temperature.</strong> Sustained 77&ndash;80&deg;F supports a faster metabolism than a tank sitting at 74&deg;F.</li>
      <li><strong>Genetics and strain.</strong> Long-fin and some heavily line-bred colour morphs finish smaller than standard tiger oscars.</li>
    </ul>

    <h2 id="stunting">Stunting: The Myth and the Reality</h2>
    <p>"A fish only grows to the size of its tank" is half a fact wrapped around a dangerous misunderstanding. What actually happens in an undersized tank is that <strong>skeletal growth slows while internal organs keep developing on schedule.</strong> The result is a fish that looks small on the outside and is compressed on the inside.</p>
    <p>Stunted oscars typically show a short, deep body with an oversized head, a bent or humped spine, buoyancy problems, and a lifespan cut to three to five years. The damage is not reversible &mdash; moving a stunted fish to a large tank improves its quality of life but does not restore normal growth.</p>
    <div class="callout callout-warn"><strong>A small oscar is not a healthy oscar.</strong> If a year-old oscar is still under 6 inches, treat it as a warning sign: check tank size, nitrate, feeding frequency and temperature before assuming it is simply a small individual.</div>

    <h2 id="too-fast">Can an Oscar Grow Too Fast?</h2>
    <p>Sort of. Pushing a juvenile with four heavy protein meals a day produces rapid length gain and, often, a fat, short-bodied adult with fatty liver disease. The healthy pattern is steady growth on a varied diet, not maximum growth &mdash; a fish that reaches 11 inches at two years on a balanced diet outlives one that hit 11 inches at fourteen months on nothing but krill.</p>

    <h2 id="tank-by-size">Matching Tank Size to Growth</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Oscar length</th><th>Minimum tank</th><th>Action</th></tr>
      <tr><td>2&ndash;4 in</td><td>40 gallons</td><td>Grow-out only &mdash; plan the upgrade now</td></tr>
      <tr><td>4&ndash;7 in</td><td>55&ndash;75 gallons</td><td>Move to the permanent tank</td></tr>
      <tr><td>7&ndash;10 in</td><td>75 gallons</td><td>Increase filtration and water change volume</td></tr>
      <tr><td>10 in and up</td><td>75&ndash;125 gallons</td><td>125 gallons if any tank mates are present</td></tr>
    </table></div>
    <p>Details and dimensions: <a href="/guides/oscar-fish-care/tank-size/">oscar fish tank size</a>, or run the numbers in the <a href="/calculators/oscar-fish-tank-size/">oscar tank size calculator</a>.</p>
"""

SIZE = {
    "slug": "size-growth",
    "title": "How Big Do Oscar Fish Get? Size Chart and Growth Rate by Age",
    "meta_desc": "Oscar fish reach 10-14 inches and grow about an inch a month for the first year. Full growth chart by age, what controls growth, and why stunting shortens life.",
    "h1": "Oscar Fish Size and Growth Rate",
    "hero_tag": "Size & Growth",
    "hero_meta": "\U0001F4CF 10&ndash;14 inches adult &nbsp;|&nbsp; \U0001F4C8 ~1 in/month year one &nbsp;|&nbsp; \U0001F553 Full size at 2&ndash;3 years",
    "toc_sections": [
        ("how-big", "How Big They Get"),
        ("growth-rate", "Growth Rate by Age"),
        ("what-affects", "What Controls Growth"),
        ("stunting", "Stunting Myth & Reality"),
        ("too-fast", "Growing Too Fast"),
        ("tank-by-size", "Tank Size by Length"),
    ],
    "body": SIZE_BODY,
    "faqs": [
        ("How big do oscar fish get?",
         "Aquarium oscars reach 10-14 inches (25-35 cm) and 2-3.5 lb, with 12 inches typical in a well-kept 75-125 gallon tank. Wild fish and exceptional specimens reach 16-18 inches."),
        ("How fast do oscar fish grow?",
         "About one inch per month for the first year, taking a 3-inch store fish to 9-11 inches by twelve months. Growth slows sharply after that, with full adult size reached at two to three years."),
        ("How big is an oscar fish at 6 months?",
         "A six-month-old oscar is typically 5-7 inches long and in its fastest growth phase. This is the point at which a grow-out tank stops being adequate and the fish should be moving to its permanent 75-gallon-or-larger home."),
        ("Do oscar fish only grow to the size of their tank?",
         "No. In a small tank an oscar's skeletal growth slows while its internal organs keep developing, producing a stunted fish with a compressed body, often a bent spine, and a lifespan cut to three to five years. It is organ damage, not natural size regulation."),
        ("Why is my oscar fish not growing?",
         "The usual causes are a tank that is too small, nitrate consistently above 40 ppm, a poor or monotonous diet, feeding a juvenile only once a day, or a tank running below 74F. Check those four before assuming the fish is simply small."),
        ("How long does it take for an oscar to reach full size?",
         "Two to three years. Most of the length is added in the first twelve months, a couple more inches come in the second year, and growth is essentially finished by year three."),
    ],
    "related": [
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size"),
        ("/guides/oscar-fish-care/lifespan/", "Oscar Fish Lifespan"),
        ("/guides/oscar-fish-care/food/", "Oscar Food & Feeding"),
        ("/species/oscar", "Oscar Species Profile"),
    ],
}


# ════════════════════════════════════════════════════════════════
# LIFESPAN
# ════════════════════════════════════════════════════════════════
LIFESPAN_BODY = """    <p>Oscars are a long commitment. A well-kept fish stays with you for over a decade, which is longer than most dogs manage, and considerably longer than the tank most people buy for it lasts before needing an upgrade.</p>

    <h2 id="how-long">How Long Do Oscar Fish Live?</h2>
    <p><strong>A properly kept oscar lives 10&ndash;15 years in an aquarium, and 18&ndash;20 years is documented.</strong> Wild oscars are generally shorter-lived than captive ones, because predation and seasonal food scarcity do what clean water and daily pellets do not.</p>
    <p>The figure you will also see quoted &mdash; five to eight years &mdash; is not wrong, it is just a description of badly kept oscars. Fish in undersized tanks, on feeder-fish diets, or in water that runs at 60&ndash;100 ppm nitrate consistently die at that age. The species is capable of much more.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Condition</th><th>Typical lifespan</th></tr>
      <tr><td>Well kept: 75&ndash;125 gal, nitrate under 20 ppm, varied diet</td><td>12&ndash;15 years</td></tr>
      <tr><td>Average home aquarium</td><td>8&ndash;12 years</td></tr>
      <tr><td>Undersized tank or poor diet</td><td>3&ndash;6 years</td></tr>
      <tr><td>Exceptional care, documented cases</td><td>18&ndash;20 years</td></tr>
      <tr><td>Wild (Amazon basin)</td><td>8&ndash;10 years estimated</td></tr>
    </table></div>

    <h2 id="factors">What Decides Whether You Get 5 Years or 15</h2>
    <ol>
      <li><strong>Nitrate, week after week.</strong> This is the biggest single lever. Chronic nitrate exposure is linked to organ damage, faded colour and <a href="/guides/oscar-fish-care/hole-in-the-head/">hole-in-the-head disease</a>. Weekly 40&ndash;50% water changes are the whole intervention.</li>
      <li><strong>Tank size during the growth year.</strong> A stunted juvenile becomes a compromised adult. See <a href="/guides/oscar-fish-care/size-growth/">size and growth</a>.</li>
      <li><strong>Diet variety.</strong> A protein-only or feeder-fish diet causes fatty liver disease and thiamine deficiency. A pellet base with frozen and vegetable rotation does not.</li>
      <li><strong>Stable temperature.</strong> 77&ndash;80&deg;F held steady. Chronic cold suppresses immunity; swings cause repeated stress events.</li>
      <li><strong>Stress load.</strong> Constant aggression from a badly chosen tank mate shortens life the same way poor water does. See <a href="/guides/oscar-fish-care/tank-mates/">oscar tank mates</a>.</li>
      <li><strong>Quarantine.</strong> Every new fish quarantined for four weeks is one fewer chance of introducing something that costs the oscar years.</li>
    </ol>

    <h2 id="stages">Oscar Life Stages</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Stage</th><th>Age</th><th>What to expect</th></tr>
      <tr><td>Fry</td><td>0&ndash;2 months</td><td>Free-swimming from about day 5; parents guard the brood</td></tr>
      <tr><td>Juvenile</td><td>2&ndash;12 months</td><td>Fastest growth; wild-type banding fading into adult pattern</td></tr>
      <tr><td>Young adult</td><td>1&ndash;3 years</td><td>Sexual maturity around 12&ndash;18 months; peak colour and activity</td></tr>
      <tr><td>Mature adult</td><td>3&ndash;10 years</td><td>Stable size; strong personality; pairs may spawn repeatedly</td></tr>
      <tr><td>Senior</td><td>10 years+</td><td>Slower, less food needed, colours often deepen and dull slightly</td></tr>
    </table></div>

    <h2 id="ageing">Telling an Old Oscar From a Sick One</h2>
    <p>Ageing oscars slow down. They spend more time resting on the substrate, eat less and less often, and lose a little of the colour intensity they had at three or four years old. None of that is alarming on its own in a ten-year-old fish.</p>
    <p>What is not normal ageing, at any age:</p>
    <ul>
      <li>Rapid or laboured breathing &mdash; see <a href="/guides/oscar-fish-care/swimming-problems/">swimming and breathing problems</a>.</li>
      <li>Sudden weight loss, a hollow belly, or stringy white faeces.</li>
      <li>Pitting or holes appearing above the eyes or along the lateral line.</li>
      <li>Refusing food for more than a few days &mdash; see <a href="/guides/oscar-fish-care/not-eating/">oscar not eating</a>.</li>
      <li>Loss of balance, listing to one side, or floating.</li>
    </ul>

    <h2 id="extend">A Practical Longevity Checklist</h2>
    <ul>
      <li>75 gallons minimum, 125 gallons preferred, from the fish's first year.</li>
      <li>40&ndash;50% water change every week, without exception.</li>
      <li>Nitrate tested weekly and kept under 20 ppm.</li>
      <li>Quality large cichlid pellet as the staple, replaced every six months so vitamins stay active.</li>
      <li>Frozen protein twice a week, vegetable food weekly, one fasting day a week.</li>
      <li>Two heaters, guarded, holding 77&ndash;80&deg;F.</li>
      <li>Filtration rated well above the tank volume, with mechanical media rinsed weekly.</li>
      <li>Four-week quarantine on every new fish, plant and piece of used equipment.</li>
    </ul>
"""

LIFESPAN = {
    "slug": "lifespan",
    "title": "Oscar Fish Lifespan: How Long Do Oscar Fish Live?",
    "meta_desc": "Oscar fish live 10-15 years in a well-kept aquarium and up to 20 with excellent care. What shortens it to five, life stages by age, and a longevity checklist.",
    "h1": "Oscar Fish Lifespan: How Long Do Oscars Live?",
    "hero_tag": "Lifespan",
    "hero_meta": "⏳ 10&ndash;15 years typical &nbsp;|&nbsp; \U0001F3C6 Up to 20 years &nbsp;|&nbsp; \U0001F4A7 Nitrate is the main lever",
    "toc_sections": [
        ("how-long", "How Long They Live"),
        ("factors", "5 Years vs 15 Years"),
        ("stages", "Oscar Life Stages"),
        ("ageing", "Old vs Sick"),
        ("extend", "Longevity Checklist"),
    ],
    "body": LIFESPAN_BODY,
    "faqs": [
        ("How long do oscar fish live?",
         "A properly kept oscar lives 10-15 years in an aquarium, and 18-20 years is documented with excellent care. Oscars in undersized tanks or on poor diets commonly die at three to six years, which is where the shorter figures quoted online come from."),
        ("What is the oldest recorded oscar fish?",
         "Well-documented aquarium oscars have reached 18-20 years. Reaching that age takes a large tank kept from the first year, weekly large water changes, and a varied diet built on a quality pellet rather than feeder fish."),
        ("Why did my oscar fish die so young?",
         "The most common causes are chronic high nitrate from insufficient water changes, a tank too small during the growth year, a feeder-fish or protein-only diet causing fatty liver disease, an uncycled tank, or a disease introduced by a fish added without quarantine."),
        ("Do oscar fish live longer in bigger tanks?",
         "Yes, substantially. A larger tank dilutes the heavy waste load an oscar produces, keeps nitrate low between water changes, and allows normal skeletal growth. Tank size during the first twelve months has the strongest effect."),
        ("How can I tell how old my oscar fish is?",
         "There is no precise method, but size is a reasonable guide in the first two years: roughly an inch per month to about 9-11 inches at one year, 11-14 inches by two to three years. After full size is reached, age can only be estimated from behaviour and colour."),
        ("How long do oscar fish live in the wild?",
         "Wild oscars in the Amazon basin are estimated to live around 8-10 years, shorter than well-kept aquarium fish, because they face predation, seasonal food scarcity and variable water conditions."),
    ],
    "related": [
        ("/guides/oscar-fish-care/size-growth/", "Oscar Size & Growth"),
        ("/guides/oscar-fish-care/water-parameters/", "Water & Temperature"),
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TYPES & COLORS
# ════════════════════════════════════════════════════════════════
TYPES_BODY = """    <p>Every oscar in the hobby is the same species, <em>Astronotus ocellatus</em>. Tiger, red, albino, lemon and long-fin are colour and fin varieties produced by selective breeding, not separate fish &mdash; they grow to the same size, need the same tank and live the same length of time. Which one you buy is purely a matter of looks.</p>

    <h2 id="varieties">Types of Oscar Fish at a Glance</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Variety</th><th>Appearance</th><th>Notes</th></tr>
      <tr><td>Wild / common oscar</td><td>Dark olive-brown with irregular pale banding and an orange-ringed eyespot on the tail</td><td>The original form; juveniles look completely different from adults</td></tr>
      <tr><td>Tiger oscar</td><td>Black or dark base heavily marbled with orange and red</td><td>By far the most common variety sold</td></tr>
      <tr><td>Red oscar</td><td>Broad solid red-orange over a dark base, little marbling</td><td>Colour deepens with age and a carotenoid-rich diet</td></tr>
      <tr><td>Albino oscar</td><td>White or cream body with red-orange patches; pink or red eyes</td><td>True albino &mdash; lacks melanin, so eyes are unpigmented</td></tr>
      <tr><td>Lutino oscar</td><td>Similar to albino but with dark eyes</td><td>Often sold as albino; a different mutation</td></tr>
      <tr><td>White oscar</td><td>Almost entirely white with faint pale markings</td><td>Selectively bred from albino lines</td></tr>
      <tr><td>Lemon oscar</td><td>Pale yellow to butter-yellow body</td><td>A soft-coloured albino-line variant</td></tr>
      <tr><td>Black oscar</td><td>Very dark, near-black base with minimal orange</td><td>Usually a dark tiger or wild-type; colour also shifts with mood</td></tr>
      <tr><td>Blue / green oscar</td><td>Blue or green body</td><td>Not a natural colour &mdash; see the dyed fish warning below</td></tr>
      <tr><td>Long-fin (veil) oscar</td><td>Any of the above with extended, flowing fins</td><td>Slower swimmer; fins tear easily; often finishes slightly smaller</td></tr>
    </table></div>

    <h2 id="tiger">Tiger Oscar</h2>
    <p>The tiger oscar is the variety most people picture: a dark, almost black body broken up by wide irregular orange and red marbling, with the classic orange-ringed ocellus near the base of the tail. It is the most widely bred and cheapest variety, usually $10&ndash;$25 as a juvenile.</p>
    <p>Tiger patterning is individual &mdash; no two fish carry the same markings &mdash; and it develops as the fish grows. A three-inch tiger oscar in a store tank often looks muddy and vaguely striped; the marbling resolves into the adult pattern between four and eight months.</p>

    <h2 id="red">Red Oscar</h2>
    <p>Red oscars trade the marbling for large blocks of solid red-orange over a dark base. They were selectively bred from tiger stock and are the second most common variety.</p>
    <p>Colour intensity is genuinely diet-dependent in this variety. A red oscar on a pellet containing astaxanthin, plus regular frozen krill, holds a noticeably deeper red than the same fish on a plain flake diet. That is the one legitimate use of "colour-enhancing" food &mdash; it works on carotenoid-based reds and oranges, and does nothing for anything else.</p>

    <h2 id="albino">Albino, Lutino, White and Lemon Oscars</h2>
    <p>These four run along the same spectrum: reduced or absent melanin.</p>
    <ul>
      <li><strong>Albino oscar</strong> &mdash; genuinely albino, with no melanin at all, which is why the eyes are pink or red. Body is white to cream with red-orange patches where the tiger marbling would have been.</li>
      <li><strong>Lutino oscar</strong> &mdash; visually similar but with normal dark eyes, because the mutation only removes some pigment types. Very frequently sold under the "albino" label.</li>
      <li><strong>White oscar</strong> &mdash; bred toward an almost entirely white fish with only faint ghost markings.</li>
      <li><strong>Lemon oscar</strong> &mdash; a soft yellow variant from the same lines.</li>
    </ul>
    <div class="callout"><strong>Light sensitivity.</strong> Albino fish have no pigment shielding their eyes, so a very brightly lit, bare tank is uncomfortable for them. Give an albino oscar shaded areas under wood or rock and moderate lighting, and it will be as confident as any other variety.</div>

    <h2 id="longfin">Long-Fin and Veil-Tail Oscars</h2>
    <p>Long-fin oscars carry extended dorsal, anal and caudal fins on any colour base &mdash; long-fin tigers and long-fin albinos are both common. They look striking and they come with practical trade-offs:</p>
    <ul>
      <li>They swim more slowly, so they lose races to food in a mixed tank.</li>
      <li>Trailing fins tear on sharp decor and are the first target for any nippy tank mate.</li>
      <li>Damaged long fins are more prone to <a href="/guides/oscar-fish-care/diseases/">fin rot</a>, so water quality has to be that bit better.</li>
      <li>Many finish an inch or so shorter in the body than standard oscars.</li>
    </ul>
    <p>Keep them with smooth decor, no fin-nippers, and ideally alone or with one calm large tank mate.</p>

    <h2 id="dyed">Blue, Purple and "Painted" Oscars</h2>
    <div class="callout callout-warn"><strong>There is no naturally blue, purple or green oscar.</strong> Fish sold as "blueberry", "strawberry", "purple" or "painted" oscars have been injected with or dipped in dye. The process strips the slime coat, is painful, and kills a large share of the fish within months of sale. The colour fades within a year on any that survive. Do not buy them &mdash; the practice continues only because it sells.</div>
    <p>Photographs of genuinely blue or green "oscars" online are almost always either digitally edited, or a different species entirely &mdash; frequently a marine parrotfish or a peacock cichlid.</p>

    <h2 id="colour-change">Why an Oscar's Colour Changes</h2>
    <p>Oscars change colour constantly, and most of it is normal. Understanding which is which saves a lot of unnecessary medicating:</p>
    <ul>
      <li><strong>Juvenile to adult change</strong> &mdash; wild-type juveniles are dark with white wavy markings and look nothing like the adult. This transformation is complete by roughly six months.</li>
      <li><strong>Mood darkening</strong> &mdash; an oscar that goes near-black in seconds is displaying, spawning, or annoyed. It reverses just as fast.</li>
      <li><strong>Stress paling</strong> &mdash; washed-out colour after a move, a water change or a new tank mate. Normally resolves in days.</li>
      <li><strong>Slow fade over weeks</strong> &mdash; this one is not behavioural. It points to nitrate, diet or illness.</li>
    </ul>
    <p>Full diagnostic walkthrough: <a href="/guides/oscar-fish-care/color-change/">oscar fish losing colour, turning white or turning black</a>.</p>

    <h2 id="choosing">Choosing a Healthy Oscar in the Store</h2>
    <ul>
      <li>Clear, undamaged eyes &mdash; no cloudiness or bulging.</li>
      <li>Smooth skin above the eyes and along the lateral line, with no pitting.</li>
      <li>Full, upright fins with no ragged or white edges.</li>
      <li>Active interest in you at the glass. A juvenile oscar hiding at the back of a store tank is a warning sign.</li>
      <li>A rounded, not hollow, belly, and normal breathing rate.</li>
      <li>Ask what the store feeds them &mdash; a shop running feeder goldfish is telling you what the fish has been exposed to.</li>
    </ul>
"""

TYPES = {
    "slug": "types",
    "title": "Types of Oscar Fish: Tiger, Red, Albino & Long-Fin Colors",
    "meta_desc": "Every oscar fish type explained: tiger, red, albino, lutino, white, lemon, black and long-fin oscars, and why blue and purple oscars are always dyed.",
    "h1": "Types of Oscar Fish and Their Colors",
    "hero_tag": "Types & Colors",
    "hero_meta": "\U0001F3A8 One species, many morphs &nbsp;|&nbsp; \U0001F42F Tiger is most common &nbsp;|&nbsp; ⚠️ Blue oscars are dyed",
    "toc_sections": [
        ("varieties", "Types at a Glance"),
        ("tiger", "Tiger Oscar"),
        ("red", "Red Oscar"),
        ("albino", "Albino, Lutino & Lemon"),
        ("longfin", "Long-Fin Oscars"),
        ("dyed", "Blue & Painted Oscars"),
        ("colour-change", "Why Colour Changes"),
        ("choosing", "Choosing a Healthy Oscar"),
    ],
    "body": TYPES_BODY,
    "faqs": [
        ("What are the different types of oscar fish?",
         "The main varieties are wild/common, tiger, red, albino, lutino, white, lemon, black and long-fin (veil) oscars. All are the same species, Astronotus ocellatus, differing only in colour and fin shape, so they need identical care and reach the same adult size."),
        ("What is a tiger oscar?",
         "A tiger oscar is the most common variety: a dark, near-black body heavily marbled with irregular orange and red, plus the orange-ringed eyespot near the tail. The pattern is unique to each fish and develops fully between about four and eight months old."),
        ("What is the difference between an albino and a lutino oscar?",
         "An albino oscar has no melanin at all, so its eyes are pink or red. A lutino oscar looks similar in the body but has normal dark eyes because only some pigment types are missing. Lutinos are very often sold labelled as albinos."),
        ("Are blue oscar fish real?",
         "No. Oscars sold as blue, purple, blueberry or painted have been artificially dyed, a process that strips the slime coat, causes pain and kills many of the fish within months. Blue and green fish shown as oscars online are usually a different species entirely."),
        ("Do long-fin oscars need different care?",
         "The care requirements are the same, but long-fin oscars swim more slowly, tear their fins on sharp decor, and are more vulnerable to fin rot and fin-nipping tank mates. Keep them with smooth decor and no nippy companions."),
        ("Why is my oscar fish changing colour?",
         "Fast darkening or paling is normal mood and stress signalling and reverses within hours. Juveniles also change appearance completely as they mature, finishing around six months. A slow fade over weeks is different and usually points to nitrate build-up, poor diet or illness."),
    ],
    "related": [
        ("/guides/oscar-fish-care/color-change/", "Oscar Colour Changes"),
        ("/species/oscar", "Oscar Species Profile"),
        ("/guides/oscar-fish-care/size-growth/", "Oscar Size & Growth"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# MALE VS FEMALE
# ════════════════════════════════════════════════════════════════
SEX_BODY = """    <p>Oscars are effectively impossible to sex reliably by eye. They are monomorphic &mdash; males and females look the same &mdash; and almost every "trick" circulating in the hobby is either unreliable or plainly wrong. Here is what actually works, and what does not.</p>

    <h2 id="short-answer">The Short Answer</h2>
    <p><strong>The only dependable method for a non-spawning oscar is venting</strong>, and even that requires a mature fish and a careful eye. The only completely certain method is watching which fish lays the eggs.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Method</th><th>Reliability</th><th>Requires</th></tr>
      <tr><td>Watching which fish lays eggs</td><td>Certain</td><td>A spawning pair</td></tr>
      <tr><td>Venting (papilla shape)</td><td>Good, with practice</td><td>Fish over ~10 in / 12 months</td></tr>
      <tr><td>Breeding tube visible at spawning</td><td>Certain, but only briefly</td><td>Active spawning</td></tr>
      <tr><td>Body size and shape</td><td>Weak</td><td>&mdash;</td></tr>
      <tr><td>Fin length or shape</td><td>Unreliable</td><td>&mdash;</td></tr>
      <tr><td>Colour intensity</td><td>Unreliable</td><td>&mdash;</td></tr>
      <tr><td>Dark spots on the dorsal fin</td><td>Myth</td><td>&mdash;</td></tr>
    </table></div>

    <h2 id="venting">How to Vent an Oscar</h2>
    <p>Venting means examining the genital papilla, the small projection just behind the anus. In a mature oscar the two sexes differ in shape:</p>
    <ul>
      <li><strong>Female:</strong> a broader, blunter, rounder papilla &mdash; the ovipositor. Often described as O-shaped or resembling a short thick tube.</li>
      <li><strong>Male:</strong> a narrower, more pointed papilla that tapers to a tip. Often described as V-shaped or cone-like.</li>
    </ul>
    <p>Practical method:</p>
    <ol>
      <li>Wait until the fish is at least 10 inches or a year old. Juvenile papillae are too small to read.</li>
      <li>Wet your hands, net the fish into a clean container of tank water and lift it briefly with wet hands supporting the body.</li>
      <li>Look at the two openings behind the vent, closest to the anal fin. Photograph rather than stare &mdash; it is easier to compare images than to judge in the moment.</li>
      <li>Return the fish within 20&ndash;30 seconds. Do not repeat this more than necessary.</li>
    </ol>
    <div class="callout callout-warn"><strong>Compare, do not judge in isolation.</strong> Venting is a relative call. A single fish tells you very little; two fish side by side tells you which is which. If you only have one oscar, accept that you probably will not know.</div>

    <h2 id="spawning">The Breeding Tube</h2>
    <p>When an oscar pair is ready to spawn, both fish drop a visible breeding tube. This is the one time the difference is obvious even to a beginner:</p>
    <ul>
      <li><strong>The female's ovipositor</strong> is thick, blunt and noticeably wider &mdash; it has to pass eggs.</li>
      <li><strong>The male's</strong> is thinner and pointed.</li>
    </ul>
    <p>The tubes are visible for a few days around spawning and then retract. If you are trying to sex a group, this is the window to look. More on the process: <a href="/guides/oscar-fish-care/breeding/">oscar fish breeding and eggs</a>.</p>

    <h2 id="myths">Sexing Myths That Do Not Work</h2>
    <ul>
      <li><strong>"Males are bigger."</strong> Often true on average and useless on any individual pair. Growth depends far more on tank, diet and age.</li>
      <li><strong>"Males have longer, more pointed fins."</strong> Sometimes slightly true in mature fish, but so variable it decides nothing &mdash; and completely meaningless in long-fin strains.</li>
      <li><strong>"Males are more colourful."</strong> No. Colour tracks mood, diet and variety, not sex.</li>
      <li><strong>"Females have dark spots on the dorsal fin."</strong> A widespread claim with no basis. Both sexes carry dorsal markings.</li>
      <li><strong>"Females have a rounder belly."</strong> A gravid female does swell, but so does an overfed male and so does a fish with dropsy or internal parasites. See <a href="/guides/oscar-fish-care/swimming-problems/">bloated oscar</a>.</li>
      <li><strong>"Males have a nuchal hump."</strong> Oscars do not reliably develop the forehead hump some other cichlids do.</li>
    </ul>

    <h2 id="behaviour">Behavioural Clues</h2>
    <p>Behaviour is weak evidence but not zero evidence, particularly in a group:</p>
    <ul>
      <li>The fish that cleans and defends a flat rock surface most obsessively before spawning is more often the female.</li>
      <li>Males tend to be the more overtly aggressive of a pair toward outsiders, and lip-locking contests are usually male&ndash;male.</li>
      <li>After eggs are laid, the fish that fans the eggs most is typically the female, while the male patrols the perimeter.</li>
    </ul>
    <p>None of this is diagnostic on its own. Read it alongside <a href="/guides/oscar-fish-care/behavior/">oscar aggression and behaviour</a>.</p>

    <h2 id="pairing">Getting a Pair Without Knowing the Sexes</h2>
    <p>Because sexing is so unreliable, the standard approach among oscar breeders is to skip it entirely: <strong>buy five or six juveniles, raise them together in a large tank, and let a pair form.</strong> Oscars choose their own partners and a self-selected pair bonds far more reliably than two fish you introduce because you think you sexed them correctly.</p>
    <p>Once a pair forms, they will separate themselves, claim a corner and defend it. At that point the remaining fish need to be removed &mdash; a bonded oscar pair in spawning condition will not tolerate company. Budget for a second tank before you start; that is the part of this plan people underestimate.</p>
"""

SEX = {
    "slug": "male-vs-female",
    "title": "Male vs Female Oscar Fish: How to Tell the Difference",
    "meta_desc": "How to sex an oscar fish: venting the genital papilla is the only reliable method, plus the breeding tube at spawning, and the myths that do not work.",
    "h1": "Male vs Female Oscar Fish",
    "hero_tag": "Male vs Female",
    "hero_meta": "⚖️ Monomorphic species &nbsp;|&nbsp; \U0001F50D Venting is the only reliable test &nbsp;|&nbsp; \U0001F95A Certain only at spawning",
    "toc_sections": [
        ("short-answer", "The Short Answer"),
        ("venting", "How to Vent an Oscar"),
        ("spawning", "The Breeding Tube"),
        ("myths", "Sexing Myths"),
        ("behaviour", "Behavioural Clues"),
        ("pairing", "Getting a Pair"),
    ],
    "body": SEX_BODY,
    "faqs": [
        ("How can you tell if an oscar fish is male or female?",
         "Venting is the only reliable method outside spawning: the female's genital papilla is broad, blunt and rounded, the male's is narrower and pointed. The fish needs to be at least 10 inches or a year old, and comparing two fish side by side is far more reliable than judging one alone."),
        ("Are male oscar fish bigger than females?",
         "On average males run slightly larger, but the difference is far smaller than the variation caused by tank size, diet and age. Size cannot be used to sex an individual oscar."),
        ("Do female oscar fish have spots on their dorsal fin?",
         "No. The claim that dark dorsal spots indicate a female is a persistent hobby myth with no basis. Both sexes carry markings on the dorsal fin."),
        ("At what age can you sex an oscar fish?",
         "Not usefully before about twelve months or 10 inches, because the genital papilla is too small to read in juveniles. Sexual maturity is typically reached between 12 and 18 months."),
        ("How do I get a breeding pair of oscars?",
         "Buy five or six juveniles, raise them together in a large tank and let a pair form naturally. Oscars choose their own partners and self-selected pairs bond far more reliably than fish paired by a keeper. Have a second tank ready, because a bonded pair will not tolerate the others."),
        ("Can two male oscars live together?",
         "Two males can coexist in a large, well-broken-up tank, but same-sex pairs of oscars frequently fight, including jaw-locking contests. Odd-numbered groups in 180 gallons or more spread the aggression better than any pair."),
    ],
    "related": [
        ("/guides/oscar-fish-care/breeding/", "Oscar Breeding & Eggs"),
        ("/guides/oscar-fish-care/behavior/", "Oscar Aggression & Behaviour"),
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# BREEDING
# ════════════════════════════════════════════════════════════════
BREED_BODY = """    <p>Oscars are among the easier large cichlids to breed and among the harder ones to breed <em>responsibly</em>. A single spawn can run to 2,000 eggs, and the market for oscar fry is small. Read the last section before you start.</p>

    <h2 id="pairing">Getting a Pair</h2>
    <p>Because oscars cannot be sexed reliably by eye, the standard method is to <strong>raise a group of five or six juveniles together in a large tank and wait for a pair to form.</strong> Oscars are choosy: a self-selected pair bonds properly, while two fish put together by a keeper frequently fight.</p>
    <p>Pair formation looks like this &mdash; two fish begin swimming together, defend a shared corner, and turn on everything else in the tank. That is your signal to move the other fish out. Sexual maturity comes at <strong>12&ndash;18 months</strong> or roughly 10 inches, and pairs stay bonded for years once formed.</p>
    <p>See <a href="/guides/oscar-fish-care/male-vs-female/">male vs female oscar fish</a> for venting technique if you want to check the pairing.</p>

    <h2 id="setup">Breeding Tank Setup</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Requirement</th><th>Setting</th></tr>
      <tr><td>Tank size</td><td>75 gallons minimum for a pair; 125 gallons preferred</td></tr>
      <tr><td>Temperature</td><td>79&ndash;82&deg;F (26&ndash;28&deg;C) &mdash; slightly warmer than normal</td></tr>
      <tr><td>pH</td><td>6.5&ndash;7.2</td></tr>
      <tr><td>Hardness</td><td>Soft to moderate, 5&ndash;12 dGH</td></tr>
      <tr><td>Spawning surface</td><td>A large flat rock, slate, or a wide clay saucer</td></tr>
      <tr><td>Substrate</td><td>Sand, or bare bottom with the spawning slate</td></tr>
      <tr><td>Lighting</td><td>Dim; the pair should feel unobserved</td></tr>
      <tr><td>Water changes</td><td>Frequent, generous, with slightly cooler fresh water to trigger</td></tr>
    </table></div>
    <p>The classic trigger is a simulated rainy season: several large water changes over a week using water two or three degrees cooler than the tank, alongside heavier feeding of protein foods. Raising the temperature back to 80&deg;F afterwards often does the rest.</p>

    <h2 id="spawning">Mating and Egg-Laying</h2>
    <p>Pre-spawning behaviour is unmistakable. The pair lip-locks, quivers alongside each other, darkens in colour, and then spends a day or two obsessively cleaning a flat surface &mdash; scrubbing the rock with their mouths until it is spotless.</p>
    <p>Both fish drop a visible breeding tube. The female then lays in neat rows across the cleaned surface, and the male passes over to fertilise. A spawn runs to <strong>300&ndash;2,000 eggs</strong>, with 1,000 typical for a mature female.</p>
    <div class="callout"><strong>Fresh eggs are white, not clear.</strong> Newly laid oscar eggs look opaque white and turn translucent brown-grey as they develop &mdash; the opposite of the usual "white eggs are dead" rule for many fish. Eggs that stay chalky white and grow fuzz after 24&ndash;36 hours are the infertile ones, and the parents usually remove them.</div>

    <h2 id="eggs">Egg Development Timeline</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Stage</th><th>Timing at 80&deg;F</th><th>What you see</th></tr>
      <tr><td>Eggs laid</td><td>Day 0</td><td>Opaque white eggs in rows on the flat rock</td></tr>
      <tr><td>Fertile eggs develop</td><td>Day 1&ndash;2</td><td>Colour shifts to translucent; eyes become visible</td></tr>
      <tr><td>Hatching</td><td>Day 2&ndash;4</td><td>Wrigglers with yolk sacs; parents move them to a pit</td></tr>
      <tr><td>Free-swimming</td><td>Day 5&ndash;8</td><td>Fry leave the pit as a shoal under the parents</td></tr>
      <tr><td>First feeding</td><td>Day 5&ndash;9</td><td>Baby brine shrimp, microworms, powdered fry food</td></tr>
      <tr><td>Separation</td><td>Week 4&ndash;6</td><td>Move fry out before the parents spawn again</td></tr>
    </table></div>

    <h2 id="fry">Raising Baby Oscars</h2>
    <p>Oscars are attentive parents &mdash; they fan the eggs, move the wrigglers to a pit they dig themselves, and shepherd free-swimming fry around the tank. Leaving the fry with the parents for the first few weeks generally works well.</p>
    <p>Feeding and maintenance for the first two months:</p>
    <ul>
      <li><strong>Days 5&ndash;14:</strong> newly hatched baby brine shrimp, three to four times a day. Microworms and commercial fry powder work as supplements.</li>
      <li><strong>Weeks 3&ndash;6:</strong> add finely crushed pellet, frozen daphnia and chopped bloodworm.</li>
      <li><strong>Week 6 onward:</strong> small cichlid pellets; the fry are eating essentially adult food by two months.</li>
      <li><strong>Water:</strong> small daily changes of 10&ndash;20%. Fry are far more sensitive to ammonia than adults and grow visibly faster in clean water.</li>
      <li><strong>Sorting:</strong> oscar fry grow at very different rates and the big ones eat the small ones. Grade them into size groups by week four.</li>
    </ul>
    <p>Growth is fast: 0.75&ndash;1 inch at one month, 2.5&ndash;3.5 inches by three months. See <a href="/guides/oscar-fish-care/size-growth/">oscar growth rate by age</a>.</p>

    <h2 id="problems">When Spawns Fail</h2>
    <ul>
      <li><strong>Eggs eaten within hours.</strong> Extremely common with first-time pairs. Most learn after two or three attempts &mdash; let them try again rather than intervening.</li>
      <li><strong>Every egg goes fuzzy.</strong> The spawn was infertile, or the "pair" is two females. Two females will lay and guard eggs that never develop.</li>
      <li><strong>Eggs fungus over despite fertility.</strong> Water quality, or a disturbed pair that stopped fanning. Methylene blue works if you are artificially hatching, but the parents usually do a better job than you will.</li>
      <li><strong>The pair turns on each other.</strong> Usually too small a tank. A spawning pair needs room to retreat from each other between bouts.</li>
      <li><strong>Repeated spawning, no fry.</strong> Check the temperature is at 79&ndash;82&deg;F and let them keep practising; inexperienced pairs improve.</li>
    </ul>

    <h2 id="pregnant">Is My Oscar Fish Pregnant?</h2>
    <p>No &mdash; oscars are egg-layers, so there is no pregnancy. A female carrying eggs is <strong>gravid</strong>, which shows as a modestly fuller belly for a few days before spawning, alongside a visible breeding tube and rock-cleaning behaviour.</p>
    <div class="callout callout-warn"><strong>A swollen belly without spawning behaviour is a health problem, not eggs.</strong> Bloating with raised scales suggests dropsy; bloating with stringy white faeces suggests internal parasites; bloating with buoyancy trouble suggests constipation or swim bladder disorder. See <a href="/guides/oscar-fish-care/swimming-problems/">bloated and abnormal swimming</a>.</div>

    <h2 id="ethics">Before You Breed: The Honest Part</h2>
    <p>One successful oscar spawn produces hundreds of fish that each grow to a foot long and need a 75-gallon tank. Local stores rarely take fry, and rehoming a hundred juvenile oscars is a genuinely hard problem &mdash; which is why unwanted oscars turn up in rescue groups and, in warm regions, in waterways where they have become an invasive species.</p>
    <p>Breed oscars if you have somewhere for the fry to go and the grow-out space to hold them in the meantime. If a pair spawns unplanned, letting the parents eat the eggs is a legitimate and common choice.</p>
"""

BREED = {
    "slug": "breeding",
    "title": "Oscar Fish Breeding: Eggs, Mating and Raising Baby Oscars",
    "meta_desc": "How oscar fish breed: pairing, spawning triggers, the egg timeline, raising fry, why oscar eggs are white, and whether an oscar can really be pregnant.",
    "h1": "Oscar Fish Breeding, Eggs and Baby Oscars",
    "hero_tag": "Breeding & Babies",
    "hero_meta": "\U0001F95A 300&ndash;2,000 eggs &nbsp;|&nbsp; \U0001F423 Hatch in 2&ndash;4 days &nbsp;|&nbsp; \U0001F4C5 Mature at 12&ndash;18 months",
    "toc_sections": [
        ("pairing", "Getting a Pair"),
        ("setup", "Breeding Tank Setup"),
        ("spawning", "Mating & Egg-Laying"),
        ("eggs", "Egg Timeline"),
        ("fry", "Raising Baby Oscars"),
        ("problems", "When Spawns Fail"),
        ("pregnant", "Is My Oscar Pregnant?"),
        ("ethics", "Before You Breed"),
    ],
    "body": BREED_BODY,
    "faqs": [
        ("How do oscar fish breed?",
         "Oscars are substrate spawners. A bonded pair cleans a large flat rock, both fish drop a breeding tube, the female lays 300-2,000 eggs in rows and the male fertilises them. Both parents guard and fan the eggs, which hatch in two to four days at 80F."),
        ("How long do oscar fish eggs take to hatch?",
         "Two to four days at 79-82F. The wrigglers then sit in a pit dug by the parents for a further three to five days before becoming free-swimming and taking their first food at around day five to eight."),
        ("Why are my oscar fish eggs white?",
         "Freshly laid oscar eggs are naturally opaque white and turn translucent brown-grey as they develop, which is the opposite of the usual rule for many fish. Eggs that stay chalky white and grow fuzz after 24-36 hours are infertile, and the parents usually remove them."),
        ("Can oscar fish get pregnant?",
         "No. Oscars are egg-layers, so there is no pregnancy. A female ready to spawn is gravid, showing a slightly fuller belly for a few days along with a visible breeding tube and obsessive rock-cleaning. A swollen belly without that behaviour is a health problem, not eggs."),
        ("Why do my oscars keep eating their eggs?",
         "This is very common with first-time pairs and usually stops after two or three attempts. Let them keep trying rather than intervening. Persistent egg-eating alongside eggs that never develop can also mean the pair is two females."),
        ("What do baby oscar fish eat?",
         "Newly free-swimming fry take baby brine shrimp, microworms and powdered fry food three to four times a day. From week three add finely crushed pellet, frozen daphnia and chopped bloodworm, and they are eating small cichlid pellets by about two months."),
        ("How many babies do oscar fish have?",
         "A single spawn runs from 300 to around 2,000 eggs, with about 1,000 typical for a mature female. Survival to saleable size is much lower, but even a modest hatch leaves hundreds of fish that each need a 75-gallon tank as adults."),
    ],
    "related": [
        ("/guides/oscar-fish-care/male-vs-female/", "Male vs Female Oscars"),
        ("/guides/oscar-fish-care/size-growth/", "Oscar Size & Growth"),
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# TANK MATES
# ════════════════════════════════════════════════════════════════
MATES_BODY = """    <p>An oscar is a foot-long predator with a personality. The honest starting position is that <strong>the safest oscar tank is an oscar-only tank</strong>, and everything below is about managing risk rather than eliminating it. If you do want companions, the rules are simple: too big to swallow, too fast or too armoured to be caught, and not aggressive enough to pick a fight.</p>

    <h2 id="rules">The Three Rules</h2>
    <ol>
      <li><strong>Anything that fits in the mouth will eventually go in the mouth.</strong> An adult oscar can swallow a 4-inch fish. It may ignore a tank mate for a year and eat it the week it grows large enough to try.</li>
      <li><strong>Tank size is the real compatibility factor.</strong> Almost every pairing that works, works in 125 gallons and fails in 75. Volume gives the other fish somewhere to be.</li>
      <li><strong>Add tank mates early or not at all.</strong> Fish introduced while the oscar is a juvenile are accepted far more readily than a stranger dropped into an adult's established territory.</li>
    </ol>
    <p>Run any specific pairing you are considering through the <a href="/tools/fish-compatibility-checker/">fish compatibility checker</a>, or browse all <a href="/compatibility/oscar/">oscar compatibility guides</a>.</p>

    <h2 id="best">Best Tank Mates for Oscar Fish</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Species</th><th>Verdict</th><th>Minimum tank</th></tr>
      <tr><td><a href="/compatibility/oscar-and-silver-dollar/">Silver dollars</a></td><td>Excellent &mdash; fast, deep-bodied, schooling</td><td>125 gal</td></tr>
      <tr><td><a href="/compatibility/bristlenose-pleco-and-oscar/">Bristlenose pleco</a></td><td>Very good &mdash; armoured, nocturnal, stays small enough to hide</td><td>75 gal</td></tr>
      <tr><td><a href="/compatibility/oscar-and-severum-cichlid/">Severum cichlid</a></td><td>Very good &mdash; similar size, similar temperament</td><td>125 gal</td></tr>
      <tr><td><a href="/compatibility/oscar-and-senegal-bichir/">Senegal bichir</a></td><td>Good &mdash; bottom dweller, armoured, occupies a different zone</td><td>125 gal</td></tr>
      <tr><td><a href="/compatibility/clown-loach-and-oscar/">Clown loach</a></td><td>Good in a group &mdash; grows large, but needs 6+ and lots of room</td><td>150 gal</td></tr>
      <tr><td><a href="/compatibility/congo-tetra-and-oscar/">Congo tetra</a></td><td>Risky but often works &mdash; fast, and just about too deep to swallow</td><td>125 gal</td></tr>
      <tr><td>Common or sailfin pleco</td><td>Good with care &mdash; see the warning below</td><td>125 gal</td></tr>
      <tr><td>Pictus catfish</td><td>Fair &mdash; fast and spiny, but small enough to be a target</td><td>125 gal</td></tr>
    </table></div>

    <h2 id="cichlids">Oscars With Other Cichlids</h2>
    <p>"Can I keep oscars with cichlids" has no single answer, because the family covers everything from dwarf rams to red devils. What matters is <strong>size, aggression level and water chemistry</strong>.</p>
    <ul>
      <li><strong><a href="/compatibility/oscar-and-severum-cichlid/">Severums</a>, <a href="/compatibility/oscar-and-texas-cichlid/">Texas cichlids</a> and <a href="/compatibility/green-terror-cichlid-and-oscar/">green terrors</a></strong> &mdash; realistic companions in 125&ndash;180 gallons. Same size class, same soft-to-neutral water, comparable temperament. Green terrors are the most likely of the three to start something.</li>
      <li><strong>Jack Dempsey</strong> &mdash; a classic pairing that works surprisingly often. Both are large, robust and similarly aggressive, so neither becomes an easy target. Needs 125 gallons minimum, two caves at opposite ends, and a keeper willing to separate them if it goes wrong.</li>
      <li><strong>Convict cichlid</strong> &mdash; possible but poor. Convicts are small enough to be eaten and aggressive enough to keep provoking a much larger fish, which is the worst combination. They also breed constantly, and a spawning convict pair will attack an oscar many times their size.</li>
      <li><strong><a href="/compatibility/frontosa-cichlid-and-oscar/">Frontosa</a> and African rift lake cichlids</strong> &mdash; avoid. The water chemistry is wrong (African cichlids want hard, alkaline water; oscars do not) and mbuna aggression is relentless.</li>
      <li><strong><a href="/compatibility/discus-and-oscar/">Discus</a></strong> &mdash; no. Discus are slow, timid, need 84&deg;F+ and pristine water, and will be outcompeted and bullied into starvation.</li>
      <li><strong>Blood parrot cichlid</strong> &mdash; a common question with a cautious answer. Parrots are a similar size but far poorer swimmers with a deformed mouth that cannot defend or compete. It can work in 125&ndash;180 gallons with plenty of caves; below that the parrot loses. Read <a href="/guides/parrot-fish-care/tank-mates/">parrot fish tank mates</a> before trying it.</li>
      <li><strong><a href="/compatibility/oscar-and-peacock-cichlid/">Peacock cichlids</a> and <a href="/compatibility/jewel-cichlid-and-oscar/">jewel cichlids</a></strong> &mdash; poor matches on chemistry, size or temperament.</li>
    </ul>

    <h2 id="pleco">Oscars and Plecos</h2>
    <p>Plecos are the most commonly kept oscar companion and the pairing needs two caveats.</p>
    <p><strong><a href="/compatibility/bristlenose-pleco-and-oscar/">Bristlenose plecos</a></strong> are the better choice: they top out at 5 inches, are heavily armoured, work at night and hide in caves during the day. They also do not outgrow the tank.</p>
    <p><strong>Common and sailfin plecos</strong> reach 18&ndash;24 inches, which solves the size problem and creates a bioload problem &mdash; two enormous waste producers in one tank. There is also a documented habit among large plecos of rasping the slime coat of flat-sided fish at night, and oscars are exactly the shape that invites it. Watch for scraped patches on the oscar's flanks.</p>
    <div class="callout"><strong>Plecos need their own food.</strong> An oscar tank has no algae to speak of and the oscar will take any wafer that lands in the open. Feed the pleco after lights out, and drop the wafer near its cave.</div>

    <h2 id="large">Oscars With Other Large Fish</h2>
    <ul>
      <li><strong><a href="/compatibility/oscar-and-silver-arowana/">Silver arowana</a></strong> &mdash; possible only in a very large tank (250 gallons or more). Arowanas are surface fish and oscars are mid-to-bottom, so the zones work, but the space requirement is enormous.</li>
      <li><strong><a href="/compatibility/clown-knifefish-and-oscar/">Clown knifefish</a></strong> &mdash; both grow huge and both are predators. A tank measured in hundreds of gallons only.</li>
      <li><strong><a href="/compatibility/fire-eel-and-oscar/">Fire eels</a> and other spiny eels</strong> &mdash; workable in large tanks with a sand bed and caves; the eel needs somewhere the oscar cannot follow.</li>
      <li><strong>Large catfish</strong> &mdash; redtails, shovelnose and similar are oscar-safe in the sense that they will not be eaten, and oscar-fatal in the sense that they grow to three feet and will eventually eat the oscar. Pictus catfish are a more realistic option, though they sit just at the edge of swallowable.</li>
    </ul>

    <h2 id="avoid">What Fish Can Not Live With Oscars</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Fish</th><th>Why it fails</th></tr>
      <tr><td><a href="/compatibility/neon-tetra-and-oscar/">Neon tetras</a> and all small tetras</td><td>Food. Not a compatibility question at all</td></tr>
      <tr><td><a href="/compatibility/guppy-and-oscar/">Guppies</a>, endlers, small livebearers</td><td>Food</td></tr>
      <tr><td><a href="/compatibility/angelfish-and-oscar/">Angelfish</a></td><td>Slow, tall, fragile fins &mdash; bullied, then eaten</td></tr>
      <tr><td><a href="/compatibility/discus-and-oscar/">Discus</a></td><td>Temperature and temperament both wrong</td></tr>
      <tr><td><a href="/compatibility/goldfish-and-oscar/">Goldfish</a> and <a href="/compatibility/koi-and-oscar/">koi</a></td><td>Coldwater species; also the classic feeder-fish disease route</td></tr>
      <tr><td>Shrimp and snails</td><td>Snacks, and a mystery snail is an expensive one</td></tr>
      <tr><td>Tiger barbs, serpae tetras</td><td>Fin-nippers, and small enough to be eaten in return</td></tr>
      <tr><td>Red devils, flowerhorns, jaguar cichlids</td><td>More aggressive than the oscar and capable of real damage</td></tr>
      <tr><td>Betta fish, gouramis, dwarf cichlids</td><td>Too small, too slow, too easily stressed</td></tr>
    </table></div>

    <h2 id="two-oscars">Keeping Two or More Oscars Together</h2>
    <p>Oscars kept with other oscars is often the best answer, with conditions. They are not schooling fish, but they tolerate their own kind better than most large cichlids, and a group raised together from juveniles usually settles.</p>
    <ul>
      <li><strong>Raise them together.</strong> Introducing an adult oscar to an established adult oscar rarely goes well.</li>
      <li><strong>Odd numbers over pairs.</strong> Three or five spread aggression; two that fall out have nowhere to redirect it.</li>
      <li><strong>125 gallons for two, 180 for three.</strong> Space is the whole solution.</li>
      <li><strong>Break sight lines.</strong> Large rock and wood structures let a chased fish get out of view, which ends the chase.</li>
      <li><strong>Watch for a formed pair.</strong> Once two oscars pair off they will turn on everything else in the tank, including the other oscars. Have a plan.</li>
    </ul>

    <h2 id="introducing">How to Introduce a Tank Mate Safely</h2>
    <ol>
      <li>Quarantine the new fish for four weeks in a separate tank.</li>
      <li>Rearrange the oscar's decor on the day of introduction. Resetting the territory removes the "this is my rock" advantage.</li>
      <li>Add the new fish with the lights off, and leave them off overnight.</li>
      <li>Feed the oscar just before the introduction so it is not hunting.</li>
      <li>Watch for the first two hours, then check regularly for three days. Chasing that does not settle within a week is not going to settle.</li>
      <li>Keep a back-up tank ready. Roughly a third of oscar tank mate attempts end in a separation.</li>
    </ol>
"""

MATES = {
    "slug": "tank-mates",
    "title": "Oscar Fish Tank Mates: What Fish Can Live With Oscars?",
    "meta_desc": "The best oscar fish tank mates and the ones that fail: plecos, silver dollars, severums, Jack Dempseys, parrot fish and arowanas, with tank sizes for each.",
    "h1": "Oscar Fish Tank Mates",
    "hero_tag": "Tank Mates",
    "hero_meta": "\U0001F420 125 gal for most pairings &nbsp;|&nbsp; \U0001F441️ If it fits, it gets eaten &nbsp;|&nbsp; \U0001F504 Add early, not late",
    "toc_sections": [
        ("rules", "The Three Rules"),
        ("best", "Best Tank Mates"),
        ("cichlids", "Oscars With Cichlids"),
        ("pleco", "Oscars and Plecos"),
        ("large", "Other Large Fish"),
        ("avoid", "Fish to Avoid"),
        ("two-oscars", "Two or More Oscars"),
        ("introducing", "Introducing Safely"),
    ],
    "body": MATES_BODY,
    "faqs": [
        ("What fish can live with oscar fish?",
         "The most reliable companions are silver dollars, bristlenose plecos, severum cichlids, Senegal bichirs and clown loach groups, all in 125 gallons or more. The common thread is that they are too large to swallow, armoured or fast, and not aggressive enough to provoke the oscar."),
        ("Can oscars live with parrot fish?",
         "It can work in 125-180 gallons with plenty of caves, but it is risky. Blood parrots are a similar size yet are poor swimmers with a deformed mouth that cannot compete for food or defend a territory, so in a smaller tank the parrot loses consistently."),
        ("Can oscars live with plecos?",
         "Yes, and plecos are the most common oscar companion. Bristlenose plecos are the better choice because they stay around 5 inches and hide during the day. Common and sailfin plecos reach 18-24 inches, double the waste load, and occasionally rasp the slime coat of flat-sided fish at night."),
        ("Can an oscar live with an angelfish?",
         "No. Angelfish are slow, tall and fragile-finned, and an adult oscar will bully them and eventually eat them. The only scenario where it lasts is a very large tank with fish raised together, and even that usually ends badly."),
        ("Can oscars live with goldfish?",
         "No. Goldfish are a coldwater species that needs 65-72F while oscars need 77-80F, so one of them is always wrong. Feeding goldfish to oscars is also the traditional route for introducing ich and internal parasites."),
        ("Can two oscars live together?",
         "Yes, if they are raised together from juveniles in 125 gallons or more, with large rock and wood structures breaking up sight lines. Odd-numbered groups spread aggression better than pairs. Watch for two fish pairing off, because a bonded pair will turn on everything else."),
        ("Can oscars live with Jack Dempseys?",
         "Often yes, in 125 gallons or larger. Both are big, robust and similarly aggressive, so neither is an easy target. Provide caves at opposite ends of the tank and be ready to separate them if the fighting escalates beyond display."),
    ],
    "related": [
        ("/compatibility/oscar/", "All Oscar Compatibility Guides"),
        ("/tools/fish-compatibility-checker/", "Fish Compatibility Checker"),
        ("/guides/oscar-fish-care/behavior/", "Oscar Aggression & Behaviour"),
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size"),
    ],
}


# ════════════════════════════════════════════════════════════════
# BEHAVIOR & AGGRESSION
# ════════════════════════════════════════════════════════════════
BEHAV_BODY = """    <p>Oscars are the reason people describe fish as having personality. They recognise their keeper, beg at the glass, rearrange the tank to their own preferences, sulk when moved, and occasionally play dead well enough to convince an experienced fishkeeper. They are also large, territorial cichlids, and the same intelligence that makes them engaging makes their aggression deliberate rather than random.</p>

    <h2 id="aggressive">Are Oscar Fish Aggressive?</h2>
    <p><strong>Yes &mdash; semi-aggressive, territorial and predatory, but not indiscriminately violent.</strong> An oscar's aggression has causes you can usually name: it is defending a territory, competing for food, responding to crowding, or hunting something small enough to eat.</p>
    <p>What that looks like in practice:</p>
    <ul>
      <li><strong>Territorial defence</strong> &mdash; claiming a cave or corner and chasing anything that enters it. Intensifies dramatically around spawning.</li>
      <li><strong>Predation</strong> &mdash; not aggression at all from the oscar's point of view. Anything under about 4 inches is food.</li>
      <li><strong>Displacement aggression</strong> &mdash; a stressed or crowded oscar takes it out on whatever is available, which is why tank size is the most effective aggression treatment there is.</li>
      <li><strong>Displays without contact</strong> &mdash; flaring gills, darkening, and side-on posturing. Most oscar "fighting" is this, and it resolves itself.</li>
    </ul>

    <h2 id="fighting">Oscar Fish Fighting: Normal or Not?</h2>
    <p>Two oscars sizing each other up is routine. The escalation ladder runs: darkening and flaring &rarr; side-by-side posturing &rarr; tail slapping &rarr; lip-locking &rarr; biting and chasing.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Behaviour</th><th>Normal?</th><th>Action</th></tr>
      <tr><td>Flaring gills, darkening, posturing</td><td>Yes</td><td>Watch only</td></tr>
      <tr><td>Tail slapping and short chases</td><td>Yes</td><td>Watch; check hiding places exist</td></tr>
      <tr><td>Lip-locking for a few seconds</td><td>Yes &mdash; a strength contest</td><td>Watch closely</td></tr>
      <tr><td>Sustained chasing, one fish hiding constantly</td><td>No</td><td>Add cover, then separate</td></tr>
      <tr><td>Torn fins, missing scales, bleeding</td><td>No</td><td>Separate immediately</td></tr>
      <tr><td>One fish not eating for days</td><td>No</td><td>Separate; it is being suppressed</td></tr>
    </table></div>
    <p>The five interventions that actually reduce fighting, in order of effect:</p>
    <ol>
      <li><strong>More space.</strong> 125 gallons for two oscars, 180 for three. Nothing else comes close.</li>
      <li><strong>Break sight lines.</strong> Large rock stacks and wood mean a chased fish disappears, which ends the chase.</li>
      <li><strong>Odd numbers.</strong> Three oscars distribute aggression; two concentrate it.</li>
      <li><strong>Rearrange the decor.</strong> Resetting territory boundaries defuses an entrenched bully.</li>
      <li><strong>Feed adequately, at two ends of the tank.</strong> Competition-driven aggression drops when nobody is short.</li>
    </ol>

    <h2 id="jumping">Why Oscars Jump</h2>
    <p>Oscars jump, and a jumped oscar on the floor is a common and preventable way to lose a fish. The triggers are consistent:</p>
    <ul>
      <li><strong>Startle response</strong> &mdash; sudden lights, a hand over the tank, or a bang. Most jumps happen in the first weeks in a new tank.</li>
      <li><strong>Being chased</strong> by a tank mate with nowhere to escape.</li>
      <li><strong>Poor water quality</strong> &mdash; a fish trying to leave water it cannot breathe in. Test immediately after any jump.</li>
      <li><strong>Hunting</strong> &mdash; oscars strike upward at food and sometimes carry the momentum out of the water.</li>
      <li><strong>Territorial pursuit</strong> in a crowded tank.</li>
    </ul>
    <div class="callout callout-warn"><strong>A tight, weighted lid is not optional on an oscar tank.</strong> Cover every gap, including cutouts for filter pipes, and leave 3&ndash;5 inches of space between the water surface and the lid. If a jump does happen, wet your hands, return the fish gently, and keep the lights off for a day &mdash; oscars survive short periods out of water more often than people expect.</div>

    <h2 id="normal">Normal Oscar Behaviour</h2>
    <ul>
      <li><strong>Begging.</strong> Oscars learn your routine within days and will beg every time you enter the room. It means nothing about hunger.</li>
      <li><strong>Redecorating.</strong> Moving gravel, uprooting plants, shoving decor. This is normal, permanent, and worth designing the tank around.</li>
      <li><strong>Following your hand.</strong> Many oscars will track a finger along the glass and can be trained to hand-feed.</li>
      <li><strong>Colour flashing.</strong> Going near-black or pale within seconds is mood signalling, not illness.</li>
      <li><strong>Playing dead.</strong> Some oscars lie motionless on their side, occasionally with faded colour. It is a genuine documented behaviour, thought to be a hunting or avoidance strategy &mdash; but it is indistinguishable from a serious health problem, so test the water before assuming it is theatre.</li>
      <li><strong>Sulking after change.</strong> New tank, new decor, new tank mate &mdash; expect a few days of hiding and refused food.</li>
      <li><strong>Spitting substrate.</strong> Picking up sand and blowing it out is normal foraging.</li>
    </ul>

    <h2 id="worrying">Behaviour That Should Worry You</h2>
    <p>These are the behaviours that are not personality:</p>
    <ul>
      <li>Sitting on the bottom for days, breathing heavily &mdash; see <a href="/guides/oscar-fish-care/not-eating/">oscar lying on the bottom and not eating</a>.</li>
      <li>Hanging at the surface gulping &mdash; see <a href="/guides/oscar-fish-care/swimming-problems/">gasping and abnormal swimming</a>.</li>
      <li>Scratching against decor or substrate &mdash; parasites or irritants; see <a href="/guides/oscar-fish-care/white-spots/">white spots and ich</a>.</li>
      <li>Rocking or shimmying in place without moving forward.</li>
      <li>Hiding permanently in a tank with no aggressor &mdash; almost always water quality.</li>
      <li>Colour that fades slowly over weeks rather than flashing &mdash; see <a href="/guides/oscar-fish-care/color-change/">oscar colour changes</a>.</li>
    </ul>

    <h2 id="enrichment">Enrichment for an Intelligent Fish</h2>
    <p>Oscars are among the few aquarium fish that visibly benefit from enrichment. A bored oscar in a bare tank is more likely to redirect energy into aggression and glass-surfing.</p>
    <ul>
      <li><strong>Structure they can rearrange.</strong> Smooth river stones, sand to dig, a sturdy piece of driftwood.</li>
      <li><strong>Floating objects.</strong> A ping-pong ball at the surface is a classic and many oscars will push it around for months.</li>
      <li><strong>Hand-feeding.</strong> Pre-soaked krill from your fingers, once the fish is settled. Mind the strike &mdash; it is faster than you expect.</li>
      <li><strong>Varied food.</strong> Different textures and foraging behaviours, not just the same pellet twice a day.</li>
      <li><strong>Occasional rearrangement</strong> of the layout, which also resets territorial disputes.</li>
    </ul>
"""

BEHAV = {
    "slug": "behavior",
    "title": "Are Oscar Fish Aggressive? Fighting, Jumping & Behavior",
    "meta_desc": "Why oscar fish are aggressive, when fighting is normal and when to separate them, why oscars jump out of tanks, and what counts as normal oscar behaviour.",
    "h1": "Oscar Fish Aggression, Fighting and Behavior",
    "hero_tag": "Aggression & Behavior",
    "hero_meta": "\U0001F620 Semi-aggressive &nbsp;|&nbsp; \U0001F94A Most fights are display &nbsp;|&nbsp; ⬆️ Jumpers &mdash; lid required",
    "toc_sections": [
        ("aggressive", "Are Oscars Aggressive?"),
        ("fighting", "Fighting: Normal or Not"),
        ("jumping", "Why Oscars Jump"),
        ("normal", "Normal Behaviour"),
        ("worrying", "Behaviour to Worry About"),
        ("enrichment", "Enrichment"),
    ],
    "body": BEHAV_BODY,
    "faqs": [
        ("Are oscar fish aggressive?",
         "Oscars are semi-aggressive, territorial and predatory, but their aggression has identifiable causes: defending territory, competing for food, crowding, or hunting anything small enough to eat. Most of what looks like fighting is display that resolves on its own."),
        ("Why are my oscars fighting?",
         "Flaring, posturing, tail slapping and brief lip-locking are normal contests between oscars. Sustained chasing, torn fins, missing scales, or one fish hiding and not eating mean the tank is too small or lacks cover. More space, broken sight lines and odd-numbered groups are the effective fixes."),
        ("Why did my oscar fish jump out of the tank?",
         "Oscars jump when startled, when chased with nowhere to escape, when water quality is bad enough that they try to leave it, and sometimes on the follow-through from striking at food. Test the water after any jump, and fit a tight weighted lid covering every gap including filter cutouts."),
        ("Why is my oscar lying on its side?",
         "Some oscars genuinely play dead, lying motionless on one side with faded colour, and it is a documented behaviour. However it looks identical to serious illness, so always test ammonia, nitrite and nitrate first and check for other symptoms before assuming it is behavioural."),
        ("Do oscar fish recognise their owners?",
         "Oscars learn the routine and the person who feeds them, beg at the glass on approach, and can be trained to hand-feed. Whether that is recognition in a strict sense is debatable, but the behavioural response to a familiar keeper is consistent and well documented among keepers."),
        ("Why does my oscar move the gravel and decorations?",
         "Digging, moving substrate and shoving decor are normal oscar foraging and territory behaviour, and it does not stop. Design the tank around it: place rock directly on the glass rather than on sand, and use plants attached to wood rather than rooted."),
    ],
    "related": [
        ("/guides/oscar-fish-care/tank-mates/", "Oscar Tank Mates"),
        ("/guides/oscar-fish-care/not-eating/", "Oscar Not Eating or Hiding"),
        ("/guides/oscar-fish-care/tank-size/", "Oscar Tank Size"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# DISEASES & PARASITES
# ════════════════════════════════════════════════════════════════
DIS_BODY = """    <p>Most oscar illness is a water quality problem wearing a disease costume. Oscars are hardy fish with a heavy waste output, and the pattern is nearly always the same: nitrate creeps up or a filter falls behind, the immune system drops, and an opportunistic pathogen that was always present takes hold. <strong>Test the water before you medicate.</strong> It is the right first move in the large majority of cases.</p>
    <div class="callout"><strong>How to use this page.</strong> Find the symptom, confirm the likely cause, and act. For a severe or fast-deteriorating fish, contact an aquatic veterinarian &mdash; these guides are educational and are not a veterinary diagnosis.</div>

    <h2 id="symptom-table">Symptom Quick Reference</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>What you see</th><th>Most likely cause</th><th>Detail</th></tr>
      <tr><td>Salt-grain white dots on body and fins</td><td>Ich (white spot)</td><td><a href="/guides/oscar-fish-care/white-spots/">White spots</a></td></tr>
      <tr><td>Pits or holes above the eyes, along the lateral line</td><td>Hole-in-the-head / HLLE</td><td><a href="/guides/oscar-fish-care/hole-in-the-head/">Hole in the head</a></td></tr>
      <tr><td>Ragged, receding, white-edged fins</td><td>Fin rot</td><td>Below</td></tr>
      <tr><td>Refusing food, sitting on the bottom, hiding</td><td>Water quality, stress, internal parasites</td><td><a href="/guides/oscar-fish-care/not-eating/">Not eating</a></td></tr>
      <tr><td>Swollen belly, raised scales</td><td>Dropsy or constipation</td><td><a href="/guides/oscar-fish-care/swimming-problems/">Swimming problems</a></td></tr>
      <tr><td>Swimming sideways or upside down</td><td>Swim bladder disorder</td><td><a href="/guides/oscar-fish-care/swimming-problems/">Swimming problems</a></td></tr>
      <tr><td>Gasping at the surface, rapid gills</td><td>Low oxygen, ammonia, gill flukes</td><td><a href="/guides/oscar-fish-care/swimming-problems/">Breathing problems</a></td></tr>
      <tr><td>One or both eyes bulging</td><td>Popeye</td><td>Below</td></tr>
      <tr><td>Cloudy or milky eye surface</td><td>Injury or bacterial infection</td><td>Below</td></tr>
      <tr><td>Colour fading, darkening or new black marks</td><td>Stress, nitrate, healing burns</td><td><a href="/guides/oscar-fish-care/color-change/">Colour changes</a></td></tr>
      <tr><td>White stringy faeces, weight loss</td><td>Internal parasites</td><td>Below</td></tr>
      <tr><td>Grey-white patches, cottony film, fast onset</td><td>Columnaris</td><td>Below</td></tr>
      <tr><td>Scratching against decor, flicking</td><td>Flukes, ich, ammonia irritation</td><td>Below</td></tr>
    </table></div>

    <h2 id="common">The Diseases Oscars Actually Get</h2>

    <h3>Ich (white spot disease)</h3>
    <p>The most common oscar disease by a wide margin. Small white grains like salt over the body and fins, usually preceded by scratching against decor. Caused by <em>Ichthyophthirius multifiliis</em>, triggered by chilling, a temperature crash during a water change, or a new fish added without quarantine.</p>
    <p>Treatment: raise the temperature to 82&ndash;86&deg;F gradually, add extra aeration, treat with a proprietary ich medication for the full course, and continue for a week past the last visible spot. Full walkthrough on <a href="/guides/oscar-fish-care/white-spots/">oscar fish white spots</a>.</p>

    <h3>Hole-in-the-head (HITH) and head and lateral line erosion (HLLE)</h3>
    <p>Pitting that starts as small depressions above the eyes and can develop into open craters. Strongly associated with chronic high nitrate, poor diet and stale water; often with the parasite <em>Hexamita</em> present as a secondary factor. It is the signature oscar disease. Detail: <a href="/guides/oscar-fish-care/hole-in-the-head/">hole in the head</a>.</p>

    <h3>Fin rot</h3>
    <p>Fins fray, recede and develop white or red edges. Bacterial, and almost always secondary to water quality or to fin damage from a tank mate or sharp decor. Long-fin oscars are noticeably more prone to it.</p>
    <p>Treatment: correct the water first with large daily changes and confirm ammonia and nitrite read 0. Mild cases heal on clean water alone within two weeks. If the erosion continues into the fin base, treat with an antibacterial such as a nitrofuran or kanamycin in a hospital tank. Aquarium salt at 1 tablespoon per 5 gallons supports healing in the short term.</p>

    <h3>Columnaris</h3>
    <p>Grey-white saddle-shaped patches, a cottony look around the mouth or gills, and rapid deterioration &mdash; sometimes within 48 hours. It is bacterial, not fungal, despite the appearance, and it moves faster at high temperatures.</p>
    <p>Treatment: unlike ich, <strong>do not raise the temperature</strong>. Lower it slightly if the tank is warm, and treat immediately with an antibacterial medication. Columnaris kills quickly and is one of the few oscar problems where waiting is a mistake.</p>

    <h3>Popeye</h3>
    <p>One eye bulging usually means physical injury &mdash; oscars regularly collide with decor and glass. Both eyes bulging suggests an internal bacterial infection or a systemic water quality problem.</p>
    <p>Treatment: clean water and Epsom salt (1 tablespoon per 5 gallons) to draw down the swelling. Add an antibacterial if both eyes are affected or if it does not improve within a week.</p>

    <h3>Cloudy eye</h3>
    <p>A milky or hazy film over the eye surface. Causes are physical abrasion, poor water quality, or a bacterial infection. Single-eye cloudiness after a tank rearrangement is almost always an abrasion and clears on its own in clean water; both eyes clouding points to water chemistry &mdash; test nitrate and pH.</p>

    <h3>Dropsy</h3>
    <p>A swollen abdomen with scales standing out from the body, giving the classic pinecone appearance when viewed from above. Dropsy is a symptom of organ failure rather than a disease in itself, and the prognosis is poor once scales are raised. Epsom salt baths and antibacterial treatment in a hospital tank are worth attempting; prevention through water quality is far more effective.</p>

    <h2 id="parasites">Oscar Fish Parasites</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Parasite</th><th>Signs</th><th>Treatment</th></tr>
      <tr><td>Ich (<em>Ichthyophthirius</em>)</td><td>White salt grains, scratching</td><td>Heat to 82&ndash;86&deg;F plus ich medication</td></tr>
      <tr><td>Gill flukes (<em>Dactylogyrus</em>)</td><td>Rapid gill movement, one gill held shut, gasping</td><td>Praziquantel</td></tr>
      <tr><td>Skin flukes (<em>Gyrodactylus</em>)</td><td>Flicking, excess slime, small red marks</td><td>Praziquantel</td></tr>
      <tr><td><em>Hexamita</em> / <em>Spironucleus</em></td><td>White stringy faeces, weight loss, often with head pits</td><td>Metronidazole, in food if the fish is eating</td></tr>
      <tr><td>Camallanus worms</td><td>Red threads protruding from the vent</td><td>Levamisole or fenbendazole, repeated after 3 weeks</td></tr>
      <tr><td>Anchor worm / fish lice</td><td>Visible attached parasites, red irritated points</td><td>Manual removal plus an appropriate parasiticide</td></tr>
      <tr><td>Velvet (<em>Oodinium</em>)</td><td>Fine gold dust sheen, clamped fins</td><td>Copper or a proprietary velvet treatment; dim the tank</td></tr>
    </table></div>
    <p>Nearly all of these arrive on new fish, live food or unquarantined plants. A four-week quarantine on everything that goes into the tank prevents more oscar disease than any medication cabinet.</p>

    <h2 id="triage">First-Response Triage</h2>
    <ol>
      <li><strong>Test ammonia, nitrite, nitrate, pH and temperature.</strong> Write the numbers down.</li>
      <li><strong>If ammonia or nitrite is above 0</strong> &mdash; change 50% of the water, stop feeding, dose a detoxifier, and repeat daily. Do not medicate; you have found the cause.</li>
      <li><strong>If nitrate is over 40 ppm</strong> &mdash; bring it down with successive water changes over several days rather than one massive change.</li>
      <li><strong>Check the temperature</strong> against 77&ndash;80&deg;F and check the heater is working.</li>
      <li><strong>Look for external signs</strong> in good light: spots, pits, fin edges, eyes, gill movement rate, faeces.</li>
      <li><strong>Isolate if needed.</strong> A hospital tank means treating 20 gallons instead of 125, and keeps medication away from your biofilter.</li>
      <li><strong>Treat one thing at a time</strong>, for the full course. Mixing medications is a common way to kill a fish that the original illness would not have.</li>
    </ol>

    <h2 id="hospital">Setting Up a Hospital Tank</h2>
    <ul>
      <li>20&ndash;40 gallons, bare bottom, with a heater and a sponge filter.</li>
      <li>Keep the sponge filter running in the display tank permanently so it is always cycled and ready.</li>
      <li>No substrate, no carbon in the filter during treatment (carbon removes medication).</li>
      <li>Dim lighting and a hiding place &mdash; a length of PVC pipe works.</li>
      <li>Daily 25% water changes during treatment, re-dosing to maintain the medication level.</li>
    </ul>

    <h2 id="prevention">Prevention That Actually Works</h2>
    <ul>
      <li><strong>40&ndash;50% weekly water change.</strong> The single highest-value habit in oscar keeping.</li>
      <li><strong>Nitrate under 20 ppm.</strong> Test it weekly, before the water change, so you know your real number.</li>
      <li><strong>Four-week quarantine</strong> on every new fish.</li>
      <li><strong>No feeder fish.</strong> See <a href="/guides/oscar-fish-care/food/">oscar food and feeding</a>.</li>
      <li><strong>Replace dry food every six months.</strong> Vitamin C degrades and deficiency contributes to head pitting.</li>
      <li><strong>Stable 77&ndash;80&deg;F</strong> with a reliable, guarded heater.</li>
      <li><strong>Match refill temperature</strong> during water changes &mdash; cold refills are a classic ich trigger.</li>
    </ul>
    <p>Species-specific symptom guides: <a href="/aquarium-fish-diseases/oscar-diseases/">oscar disease index</a>.</p>
"""

DIS = {
    "slug": "diseases",
    "title": "Oscar Fish Diseases and Parasites: Symptoms and Treatment",
    "meta_desc": "Oscar fish diseases explained: ich, hole-in-the-head, fin rot, columnaris, popeye, dropsy and parasites, with a symptom table and first-response triage.",
    "h1": "Oscar Fish Diseases and Parasites",
    "hero_tag": "Diseases & Parasites",
    "hero_meta": "\U0001F9EA Test water first &nbsp;|&nbsp; \U0001FA7A Symptom lookup table &nbsp;|&nbsp; \U0001F3E5 Hospital tank guide",
    "toc_sections": [
        ("symptom-table", "Symptom Quick Reference"),
        ("common", "Common Oscar Diseases"),
        ("parasites", "Oscar Fish Parasites"),
        ("triage", "First-Response Triage"),
        ("hospital", "Hospital Tank"),
        ("prevention", "Prevention"),
    ],
    "body": DIS_BODY,
    "faqs": [
        ("What are the most common oscar fish diseases?",
         "Ich (white spot) is the most common, followed by hole-in-the-head and lateral line erosion, fin rot, columnaris, popeye, cloudy eye and dropsy. Most of them are opportunistic infections that take hold after water quality slips, which is why testing the water comes before medicating."),
        ("What parasites do oscar fish get?",
         "Ich, gill and skin flukes, Hexamita or Spironucleus, Camallanus worms, anchor worm and fish lice, and velvet. Almost all of them arrive on new fish, live food or unquarantined plants, so a four-week quarantine prevents more oscar disease than any medication."),
        ("Why does my oscar fish keep getting sick?",
         "Recurring illness in an oscar almost always traces back to chronic water quality: nitrate creeping above 40 ppm between water changes, a filter undersized for the waste load, or an unstable temperature. Fix the maintenance routine before treating each new symptom individually."),
        ("Should I use salt to treat an oscar fish?",
         "Aquarium salt at about 1 tablespoon per 5 gallons supports healing for fin rot and minor wounds, and Epsom salt at the same rate helps with popeye and constipation. Neither is a general-purpose treatment, and salt should be dosed deliberately for a specific problem rather than kept in the tank permanently."),
        ("Do I need a hospital tank for an oscar?",
         "It is strongly recommended. Treating a 20-40 gallon hospital tank instead of a 125-gallon display costs a fraction of the medication, keeps medication away from your biofilter, and lets you observe and adjust doses. Keep a sponge filter running in the display tank so it is always cycled."),
        ("How do I know if my oscar is sick or just sulking?",
         "Sulking follows a change - a move, new decor, a new tank mate - and resolves within a few days with no physical signs. Illness comes with something visible or measurable: bad water test results, spots, pits, ragged fins, laboured breathing, stringy white faeces, or a swollen belly."),
    ],
    "related": [
        ("/guides/oscar-fish-care/hole-in-the-head/", "Hole in the Head"),
        ("/guides/oscar-fish-care/white-spots/", "Oscar White Spots (Ich)"),
        ("/aquarium-fish-diseases/oscar-diseases/", "Oscar Disease Index"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
    ],
}


# ════════════════════════════════════════════════════════════════
# HOLE IN THE HEAD
# ════════════════════════════════════════════════════════════════
HITH_BODY = """    <p>Hole-in-the-head is the disease oscars are known for. It starts as small pale pits above the eyes, often mistaken for damage from digging, and if the cause is not corrected it develops into open craters along the head and lateral line. It is treatable, and it is very largely preventable.</p>
    <div class="callout"><strong>The short version.</strong> Pits above the eyes on an oscar mean the tank's long-term water quality or the fish's diet is wrong. Fix nitrate and diet first, and treat with metronidazole if the fish is also losing weight or passing white stringy faeces.</div>

    <h2 id="what-is">What Hole-in-the-Head Is</h2>
    <p>Two overlapping conditions get the same name:</p>
    <ul>
      <li><strong>HITH (hole-in-the-head)</strong> &mdash; pitting concentrated on the head, above and around the eyes, frequently associated with the flagellate parasite <em>Hexamita</em> (also classified as <em>Spironucleus</em>).</li>
      <li><strong>HLLE (head and lateral line erosion)</strong> &mdash; the same kind of erosion extending backward along the lateral line, usually with no parasite involvement at all.</li>
    </ul>
    <p>In practice the two run together in oscars and respond to the same corrections. <em>Hexamita</em> is a normal resident of a healthy cichlid's intestine; it only becomes a problem when a fish is immunosuppressed &mdash; which is why treating the parasite without fixing the tank produces a fish that relapses within months.</p>

    <h2 id="causes">What Causes It</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>How it contributes</th><th>Strength of evidence</th></tr>
      <tr><td>Chronic high nitrate</td><td>Sustained immunosuppression and tissue stress</td><td>Strong &mdash; the most consistent factor</td></tr>
      <tr><td>Poor or monotonous diet</td><td>Vitamin C and D deficiency; stale dry food</td><td>Strong</td></tr>
      <tr><td><em>Hexamita</em> overgrowth</td><td>Intestinal parasite spreading systemically</td><td>Strong in cases with weight loss</td></tr>
      <tr><td>Infrequent water changes</td><td>Accumulated dissolved organics</td><td>Strong</td></tr>
      <tr><td>Chronic stress</td><td>Crowding, aggression, undersized tank</td><td>Moderate</td></tr>
      <tr><td>Activated carbon</td><td>Long-debated link to HLLE; unproven</td><td>Weak &mdash; not a reason to panic</td></tr>
      <tr><td>Stray voltage</td><td>Occasionally implicated in HLLE</td><td>Weak, but worth checking equipment</td></tr>
    </table></div>

    <h2 id="symptoms">Symptoms in Order of Appearance</h2>
    <ol>
      <li>Small pale or white pits above the eyes, 1&ndash;2 mm across. Easy to miss.</li>
      <li>Pits deepen and widen; the surrounding skin loses colour.</li>
      <li>Erosion extends backward along the lateral line.</li>
      <li>White or cream-coloured mucus threads from the openings.</li>
      <li>Appetite drops; the fish becomes lethargic.</li>
      <li>White stringy faeces and visible weight loss &mdash; this is the sign that <em>Hexamita</em> is systemically involved.</li>
      <li>Secondary bacterial and fungal infection of the open lesions.</li>
    </ol>
    <div class="callout callout-warn"><strong>Do not confuse pits with sensory pores.</strong> Every oscar has a row of normal sensory pores across the head &mdash; small, evenly spaced, symmetrical and the same colour as the surrounding skin. HITH lesions are irregular, uneven, pale-rimmed and get bigger over weeks.</div>

    <h2 id="treatment">Treatment, Step by Step</h2>
    <p><strong>Stage 1 &mdash; fix the environment (always, whatever else you do).</strong></p>
    <ul>
      <li>Test nitrate. If it is over 40 ppm, bring it down with 30% changes daily for several days rather than one huge change.</li>
      <li>Move to 50% weekly water changes permanently, or twice weekly if the tank is heavily stocked.</li>
      <li>Confirm ammonia and nitrite read 0 and the filter is adequate for the tank.</li>
      <li>Check the tank size and any aggression from tank mates &mdash; chronic stress is a real contributor.</li>
    </ul>
    <p><strong>Stage 2 &mdash; fix the diet.</strong></p>
    <ul>
      <li>Replace dry food opened more than six months ago. Vitamin content degrades.</li>
      <li>Switch to a quality pellet with added vitamin C, and add frozen foods &mdash; krill, mysis &mdash; two or three times a week.</li>
      <li>Add vegetable content: blanched peas, spirulina.</li>
      <li>Vitamin-soaking food with a commercial fish vitamin supplement is worthwhile during recovery.</li>
    </ul>
    <p><strong>Stage 3 &mdash; medicate, if indicated.</strong></p>
    <ul>
      <li>Treat with <strong>metronidazole</strong> if the fish shows weight loss, white stringy faeces or a poor appetite alongside the pits.</li>
      <li>Medicated food is far more effective than water dosing, because the target is in the gut. If the fish is still eating, soak pellets in a metronidazole solution.</li>
      <li>If the fish is not eating, dose the water in a hospital tank &mdash; typically around 250 mg per 10 gallons every 24 hours for three days, with a 25&ndash;50% water change before each dose. Follow the product's instructions.</li>
      <li>Add an antibacterial only if the lesions are visibly infected, red-rimmed or fungused.</li>
    </ul>

    <h2 id="recovery">What Recovery Looks Like</h2>
    <p>The pits do not close overnight. Expect this sequence:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Timeframe</th><th>What to expect</th></tr>
      <tr><td>Week 1&ndash;2</td><td>Appetite improves; lesions stop spreading; mucus threads stop</td></tr>
      <tr><td>Week 3&ndash;6</td><td>Pit edges become less inflamed; new tissue starts filling shallow pits</td></tr>
      <tr><td>Month 2&ndash;4</td><td>Shallow pits close; deeper craters visibly shrink</td></tr>
      <tr><td>Month 4&ndash;12</td><td>Deep lesions fill in; faint scarring may remain permanently</td></tr>
    </table></div>
    <p>Deep craters often leave a permanent mark. That is cosmetic, and a fish with scarred pits that have stopped progressing is a recovered fish.</p>

    <h2 id="prevention">Prevention</h2>
    <ul>
      <li><strong>Nitrate under 20 ppm, tested weekly.</strong> This alone prevents most cases.</li>
      <li>40&ndash;50% water changes every week without fail.</li>
      <li>A varied diet with genuine vitamin content, and dry food replaced twice a year.</li>
      <li>A tank large enough that the fish is not chronically stressed &mdash; see <a href="/guides/oscar-fish-care/tank-size/">oscar tank size</a>.</li>
      <li>Quarantine new fish for four weeks so you are not importing parasites.</li>
      <li>Check the head above the eyes every week while you feed. Early pits are trivially easy to reverse; deep craters take a year.</li>
    </ul>
    <p>Related: <a href="/guides/oscar-fish-care/diseases/">oscar fish diseases and parasites</a> and <a href="/guides/oscar-fish-care/water-parameters/">water parameters</a>.</p>
"""

HITH = {
    "slug": "hole-in-the-head",
    "title": "Oscar Fish Hole in the Head: Causes, Treatment and Recovery",
    "meta_desc": "Hole-in-the-head in oscar fish explained: what causes the pits, how to tell them from normal sensory pores, metronidazole treatment, and the recovery timeline.",
    "h1": "Oscar Fish Hole in the Head (HITH and HLLE)",
    "hero_tag": "Hole in the Head",
    "hero_meta": "\U0001F573️ Pits above the eyes &nbsp;|&nbsp; \U0001F4A7 Nitrate is the main cause &nbsp;|&nbsp; \U0001F48A Metronidazole if wasting",
    "toc_sections": [
        ("what-is", "What HITH Is"),
        ("causes", "What Causes It"),
        ("symptoms", "Symptoms in Order"),
        ("treatment", "Treatment Step by Step"),
        ("recovery", "Recovery Timeline"),
        ("prevention", "Prevention"),
    ],
    "body": HITH_BODY,
    "faqs": [
        ("What causes hole in the head in oscar fish?",
         "The most consistent factors are chronic high nitrate from infrequent water changes and a poor or vitamin-deficient diet, which suppress the fish's immunity. The parasite Hexamita, a normal gut resident, then overgrows and spreads. Chronic stress from an undersized tank contributes."),
        ("How do I treat hole in the head in an oscar?",
         "Fix the environment first: bring nitrate under 20 ppm with successive water changes and move to 50% weekly changes. Then fix the diet with fresh vitamin-rich food. Add metronidazole - ideally in food - if the fish is also losing weight, passing white stringy faeces, or off its food."),
        ("Are the holes on my oscar's head normal pores?",
         "Every oscar has a row of normal sensory pores across its head: small, evenly spaced, symmetrical and the same colour as the surrounding skin. Hole-in-the-head lesions are irregular, uneven, pale-rimmed, and grow larger over weeks."),
        ("Will hole in the head heal on its own?",
         "Shallow early pits often close once nitrate and diet are corrected, without medication. Established lesions with weight loss or white stringy faeces need metronidazole as well. Untreated, the erosion continues and secondary bacterial infection becomes likely."),
        ("How long does it take an oscar to recover from hole in the head?",
         "Lesions stop spreading within one to two weeks of correcting water and diet. Shallow pits close over two to four months, and deep craters can take four months to a year to fill in, often leaving faint permanent scarring that is cosmetic only."),
        ("Is hole in the head contagious to other fish?",
         "Not in the way ich is. Hexamita is present in most healthy cichlids already and only causes disease in fish whose immunity is compromised. If several fish in one tank develop pitting, the shared cause is the tank conditions, not fish-to-fish transmission."),
    ],
    "related": [
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases & Parasites"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/oscar-fish-care/food/", "Oscar Food & Feeding"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
    ],
}


# ════════════════════════════════════════════════════════════════
# WHITE SPOTS / ICH
# ════════════════════════════════════════════════════════════════
ICH_BODY = """    <p>White spots on an oscar are usually ich, and ich on an oscar is usually the result of a temperature drop or a fish added without quarantine. It is highly treatable if you start early and, critically, treat for the full life cycle rather than until the spots disappear.</p>

    <h2 id="identify">Is It Actually Ich?</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>What you see</th><th>Likely cause</th></tr>
      <tr><td>Distinct raised white dots like grains of salt, on body and fins</td><td>Ich (<em>Ichthyophthirius multifiliis</em>)</td></tr>
      <tr><td>Very fine gold or rust-coloured dust, best seen with a torch at an angle</td><td>Velvet (<em>Oodinium</em>)</td></tr>
      <tr><td>Flat white or grey patches, cottony edges, fast spread</td><td>Columnaris &mdash; do not raise the temperature</td></tr>
      <tr><td>A few white dots only on the fin rays or edges</td><td>Often normal breeding tubercles or fin damage</td></tr>
      <tr><td>Fuzzy white tufts on one spot after an injury</td><td>Fungus</td></tr>
      <tr><td>Whole body pale or whitening, no discrete dots</td><td>Stress or colour change &mdash; see <a href="/guides/oscar-fish-care/color-change/">colour changes</a></td></tr>
    </table></div>
    <p>The clinching test for ich is behaviour before appearance: <strong>scratching against rocks and substrate for a day or two comes before the spots.</strong> If your oscar flicked against the decor and white grains appeared the next day, it is ich.</p>

    <h2 id="lifecycle">Why the Life Cycle Matters</h2>
    <p>Ich has three stages and only one of them is treatable:</p>
    <ol>
      <li><strong>Trophont</strong> &mdash; the parasite embedded in the fish's skin. This is the white spot you can see, and it is protected from medication.</li>
      <li><strong>Tomont</strong> &mdash; it drops off, encysts on the substrate and divides. Still protected.</li>
      <li><strong>Theront</strong> &mdash; hundreds of free-swimming juveniles hunting a host. <strong>This is the only stage medication kills.</strong></li>
    </ol>
    <p>Two consequences follow. First, spots disappearing means the parasite dropped off, not that it died &mdash; stopping treatment there guarantees a worse outbreak in a week. Second, warmth speeds the cycle up, so raising the temperature shortens the time the parasite spends in a stage you cannot touch.</p>

    <h2 id="treatment">Treating Ich on an Oscar</h2>
    <ol>
      <li><strong>Raise the temperature</strong> gradually to 82&ndash;86&deg;F over 12&ndash;24 hours. Oscars tolerate this well.</li>
      <li><strong>Add aeration.</strong> Warm water holds less oxygen and this is the stage where a gasping fish becomes a real risk. An extra airstone is not optional.</li>
      <li><strong>Dose a proprietary ich medication</strong> &mdash; malachite green with formalin is the standard, and oscars tolerate it at full dose. Remove activated carbon first.</li>
      <li><strong>Vacuum the substrate daily.</strong> Tomonts sit on the bottom; removing them physically shortens the outbreak.</li>
      <li><strong>Do a 25&ndash;30% water change before each re-dose</strong>, following the product's schedule.</li>
      <li><strong>Continue for a full week after the last visible spot.</strong> This is the step people skip and it is the step that decides the outcome.</li>
      <li><strong>Return the temperature to 78&ndash;80&deg;F</strong> gradually once the course is complete.</li>
    </ol>
    <div class="callout"><strong>Salt as an alternative.</strong> Aquarium salt at 1&ndash;2 tablespoons per 5 gallons, held for two weeks alongside raised temperature, is an effective ich treatment for oscars and gentler on the biofilter than malachite green. It is not suitable if the tank contains loaches, plecos in some cases, or live plants.</div>

    <h2 id="causes">Why Your Oscar Got Ich</h2>
    <ul>
      <li><strong>A cold water change.</strong> The single most common trigger &mdash; a large refill several degrees below tank temperature.</li>
      <li><strong>A failing or undersized heater</strong> letting the tank drift below 74&deg;F.</li>
      <li><strong>A new fish added without quarantine.</strong> Ich is nearly always introduced, not spontaneous.</li>
      <li><strong>Live food, particularly feeder fish.</strong> See <a href="/guides/oscar-fish-care/food/">why not to feed feeder fish</a>.</li>
      <li><strong>Chronic stress</strong> from high nitrate, crowding or aggression, which lets a low-level infection take hold.</li>
    </ul>

    <h2 id="after">After Treatment</h2>
    <ul>
      <li>Watch for two to three weeks. A relapse usually means the course was stopped early.</li>
      <li>Expect the fish to be off its food for a few days &mdash; both the illness and the medication suppress appetite.</li>
      <li>Check the biofilter. Ich medications can knock back beneficial bacteria; test ammonia and nitrite for a week afterwards.</li>
      <li>Feed well once appetite returns. Recovering fish rebuild the slime coat and damaged skin.</li>
      <li>Damaged fins usually regrow within a few weeks in clean water.</li>
    </ul>

    <h2 id="black-spots">And If the Spots Are Black?</h2>
    <p>Black spots or patches on an oscar are a different problem entirely and are rarely parasitic. In oscars they are most often healing ammonia burn, stress marbling, or simply the fish's own pattern developing. See <a href="/guides/oscar-fish-care/color-change/">oscar fish black spots and colour changes</a>.</p>
"""

ICH = {
    "slug": "white-spots",
    "title": "Oscar Fish White Spots: Ich Identification and Treatment",
    "meta_desc": "White spots on an oscar fish are usually ich. How to tell ich from velvet, columnaris and fungus, and the full treatment plan that stops it coming back.",
    "h1": "Oscar Fish White Spots (Ich)",
    "hero_tag": "White Spots",
    "hero_meta": "⚪ Salt-grain dots &nbsp;|&nbsp; \U0001F321️ Heat to 82&ndash;86&deg;F &nbsp;|&nbsp; \U0001F4C5 Treat a week past the last spot",
    "toc_sections": [
        ("identify", "Is It Actually Ich?"),
        ("lifecycle", "Why the Life Cycle Matters"),
        ("treatment", "Treating Ich"),
        ("causes", "Why It Happened"),
        ("after", "After Treatment"),
        ("black-spots", "If the Spots Are Black"),
    ],
    "body": ICH_BODY,
    "faqs": [
        ("Why does my oscar fish have white spots?",
         "Distinct raised white dots like grains of salt, usually preceded by a day or two of scratching against decor, are ich. A fine gold dust sheen is velvet instead, and flat grey-white patches that spread fast are columnaris, which must not be treated with heat."),
        ("How do you treat ich on an oscar fish?",
         "Raise the temperature gradually to 82-86F, add extra aeration, remove activated carbon and dose a proprietary ich medication, vacuuming the substrate daily. Continue the full course for a week after the last visible spot, then return the temperature to 78-80F gradually."),
        ("How long does it take to cure ich on an oscar?",
         "Visible spots usually clear within five to seven days at raised temperature, but treatment must continue for a full week beyond that, so plan on two weeks total. Stopping when the spots disappear is the most common reason ich comes back worse."),
        ("Can I treat oscar ich with salt instead of medication?",
         "Yes. Aquarium salt at 1-2 tablespoons per 5 gallons held for two weeks, alongside raised temperature, is effective on oscars and gentler on the biofilter than malachite green. It is not suitable if the tank holds loaches or live plants."),
        ("Can ich kill an oscar fish?",
         "Yes, if it is left untreated or treated too briefly. Heavy infestations damage the gills and cause suffocation, and open lesions invite secondary bacterial infection. Caught early, ich on a healthy adult oscar is very treatable."),
        ("Why does my oscar keep getting ich?",
         "Repeat outbreaks mean either the treatment course was stopped early and the parasite survived on the substrate, or a persistent trigger remains: cold water changes, a failing heater letting the tank drift below 74F, unquarantined new fish, or chronic stress from high nitrate."),
    ],
    "related": [
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases & Parasites"),
        ("/guides/oscar-fish-care/color-change/", "Oscar Colour Changes"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/oscar-fish-care/", "Oscar Fish Care Guide"),
    ],
}


# ════════════════════════════════════════════════════════════════
# NOT EATING / HIDING / LYING ON BOTTOM
# ════════════════════════════════════════════════════════════════
EAT_BODY = """    <p>An oscar that stops eating, hides, or sits on the bottom is showing you the same signal three different ways. Sometimes it is a sulk after a change and resolves itself in a week. Sometimes it is the first visible stage of a water quality problem that has been building for a month. This page tells you which one you are looking at.</p>
    <div class="callout"><strong>Do this first.</strong> Test ammonia, nitrite, nitrate, pH and temperature before anything else. In the majority of cases the answer is in those five numbers, and adding medication to a water quality problem makes things worse.</div>

    <h2 id="how-long">How Long Can an Oscar Go Without Eating?</h2>
    <p>A healthy adult oscar can go <strong>one to two weeks without food</strong> with no harm at all. Fish are not mammals; a missed meal is not an emergency. A juvenile under 6 inches should not skip more than two or three days, because it is still growing quickly.</p>
    <p>So the question is never "how do I make it eat" &mdash; it is "why has it stopped".</p>

    <h2 id="causes">Causes, Ranked by How Common They Are</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>Other signs</th><th>What to do</th></tr>
      <tr><td>Ammonia or nitrite above 0</td><td>Gasping, red gills, lethargy, clamped fins</td><td>50% water change now, daily until 0; stop feeding</td></tr>
      <tr><td>Nitrate over 40 ppm</td><td>Faded colour, listlessness, head pitting</td><td>Successive 30% changes over several days</td></tr>
      <tr><td>Recent change (move, decor, tank mate)</td><td>Otherwise normal fish, hiding</td><td>Wait a week; dim the lights; do not fuss</td></tr>
      <tr><td>Temperature below 74&deg;F</td><td>Sluggish, sitting still, slow to respond</td><td>Check the heater; raise gradually to 78&ndash;80&deg;F</td></tr>
      <tr><td>Bullying from a tank mate</td><td>Hiding, torn fins, feeding only when alone</td><td>Add cover; separate if it does not settle</td></tr>
      <tr><td>Internal parasites</td><td>White stringy faeces, weight loss despite eating</td><td>Metronidazole or a dewormer</td></tr>
      <tr><td>Hole-in-the-head</td><td>Pits above the eyes</td><td><a href="/guides/oscar-fish-care/hole-in-the-head/">HITH treatment</a></td></tr>
      <tr><td>Constipation or bloat</td><td>Swollen belly, no faeces, buoyancy trouble</td><td>Fast 3 days, then blanched pea</td></tr>
      <tr><td>Food changed or gone stale</td><td>Spits pellets out; eats other foods</td><td>Offer a different food; replace old dry food</td></tr>
      <tr><td>Ich or another infection</td><td>Spots, scratching, ragged fins, laboured breathing</td><td><a href="/guides/oscar-fish-care/diseases/">Diseases and parasites</a></td></tr>
      <tr><td>Simply full</td><td>Fat, healthy adult on daily feeding</td><td>Move to every-other-day feeding</td></tr>
    </table></div>

    <h2 id="bottom">Oscar Lying on the Bottom</h2>
    <p>An oscar resting on the substrate is not automatically ill &mdash; adults do rest, and old fish rest a lot. What separates normal resting from a problem is everything happening around it:</p>
    <ul>
      <li><strong>Probably normal:</strong> upright, breathing steadily, alert to you approaching, normal colour, eats when offered food, older fish.</li>
      <li><strong>Probably a problem:</strong> breathing fast or hard, leaning or on its side, colour faded or unusually dark, unresponsive when you approach, refusing food, fins clamped.</li>
    </ul>
    <p>Oscars also famously <strong>play dead</strong> &mdash; lying motionless on one side, sometimes with washed-out colour, then swimming off perfectly normally. It is a documented behaviour. It is also indistinguishable from a fish in trouble, so treat it as a health event until the water tests come back clean.</p>

    <h2 id="hiding">Oscar Hiding</h2>
    <p>Hiding has three distinct patterns and they mean different things:</p>
    <ul>
      <li><strong>New fish hiding for one to three weeks.</strong> Completely normal. Newly moved oscars often refuse food entirely for the first week. Dim the lights, provide a cave, feed once a day, and stop staring at it.</li>
      <li><strong>An established fish that suddenly starts hiding.</strong> Something changed. Test the water, then look for an aggressor, a moved piece of decor, or new activity outside the tank &mdash; a new pet, a moved piece of furniture, more foot traffic.</li>
      <li><strong>Permanent hiding in a tank with no aggressor.</strong> Almost always water quality, or a tank so bare the fish has no sense of security. Add structure and correct nitrate.</li>
    </ul>

    <h2 id="walkthrough">Diagnostic Walkthrough</h2>
    <ol>
      <li><strong>Test the water.</strong> Ammonia and nitrite must be 0; nitrate under 40 ppm; temperature 77&ndash;80&deg;F. Anything off here is your answer.</li>
      <li><strong>Look at the fish in good light.</strong> Check above the eyes for pits, the body for spots, the fins for ragged edges, the belly for swelling, the gills for rapid movement.</li>
      <li><strong>Check the faeces.</strong> Normal is dark and segmented. White, stringy and trailing means internal parasites.</li>
      <li><strong>List what changed</strong> in the last two weeks: water change, new fish, new food, new decor, heater, house move, new pet outside the tank.</li>
      <li><strong>Watch feeding with nobody in the room.</strong> A bullied or nervous fish often eats fine when it is not being observed &mdash; a phone propped up will tell you.</li>
      <li><strong>Offer a tempting food.</strong> A live earthworm or thawed frozen krill will move a fish that ignores pellets. Refusal of a live earthworm is a meaningful negative sign.</li>
      <li><strong>If everything tests clean and refusal passes a week</strong>, treat for internal parasites with metronidazole or a dewormer.</li>
    </ol>

    <h2 id="restart">Getting an Oscar Eating Again</h2>
    <ul>
      <li><strong>Fix the water first.</strong> Appetite returns on its own once the cause is gone.</li>
      <li><strong>Warm the tank</strong> to the upper end of the range, 79&ndash;80&deg;F.</li>
      <li><strong>Offer live or frozen food.</strong> Earthworms and blackworms have the strongest track record for restarting a fasting oscar.</li>
      <li><strong>Feed at a quiet time</strong> with the room lights low and nobody at the glass.</li>
      <li><strong>Remove uneaten food after five minutes</strong> so it does not add to the problem you are fixing.</li>
      <li><strong>Do not keep switching foods daily.</strong> Give each option two or three days.</li>
      <li><strong>Do not medicate blindly.</strong> Medicating a fish that is off its food because of nitrate makes it weaker, not better.</li>
    </ul>
    <div class="callout callout-warn"><strong>When to escalate.</strong> Visible weight loss, a hollow belly, laboured breathing, open sores, or refusal beyond two weeks in an adult (or four days in a juvenile) all warrant contacting an aquatic veterinarian. These pages are educational and not a veterinary diagnosis.</div>
"""

EAT = {
    "slug": "not-eating",
    "title": "Oscar Fish Not Eating, Hiding or Lying on the Bottom",
    "meta_desc": "Why an oscar fish stops eating, hides or sits on the bottom, ranked by likelihood, with a diagnostic walkthrough and how to get an oscar feeding again.",
    "h1": "Oscar Fish Not Eating, Hiding or Lying on the Bottom",
    "hero_tag": "Not Eating & Hiding",
    "hero_meta": "\U0001F9EA Test water first &nbsp;|&nbsp; \U0001F553 Adults survive 1&ndash;2 weeks fasting &nbsp;|&nbsp; \U0001FAB1 Earthworm restarts most fish",
    "toc_sections": [
        ("how-long", "How Long Without Food"),
        ("causes", "Causes Ranked"),
        ("bottom", "Lying on the Bottom"),
        ("hiding", "Oscar Hiding"),
        ("walkthrough", "Diagnostic Walkthrough"),
        ("restart", "Getting Them Eating Again"),
    ],
    "body": EAT_BODY,
    "faqs": [
        ("Why is my oscar fish not eating?",
         "The most common causes, in order, are ammonia or nitrite above zero, nitrate over 40 ppm, a recent change such as a move or a new tank mate, a tank that has drifted below 74F, bullying, and internal parasites. Test ammonia, nitrite, nitrate, pH and temperature before doing anything else."),
        ("How long can an oscar fish go without eating?",
         "A healthy adult oscar can go one to two weeks without food with no harm. A juvenile under 6 inches should not skip more than two or three days because it is still growing quickly. The question to answer is why it stopped, not how to force it to eat."),
        ("Why is my oscar fish lying on the bottom?",
         "Adults do rest on the substrate and old fish rest often, so it is only a problem alongside other signs: fast or laboured breathing, leaning or lying on one side, faded or unusually dark colour, refusing food, or clamped fins. Oscars also genuinely play dead, but always test the water before assuming that."),
        ("Why is my oscar fish hiding all the time?",
         "A newly added oscar hiding for one to three weeks is normal. An established fish that suddenly starts hiding has had something change - test the water, then look for an aggressor or a disturbance outside the tank. Permanent hiding with no aggressor is usually water quality or a tank with no structure."),
        ("My oscar fish won't eat but seems fine otherwise. What should I do?",
         "Confirm the water tests clean and the temperature is 77-80F, then offer a live earthworm or thawed frozen krill at a quiet time with the lights low. A well-fed adult on daily feeding may simply be full, in which case move to every-other-day feeding."),
        ("When should I worry about an oscar that isn't eating?",
         "Escalate if there is visible weight loss or a hollow belly, laboured breathing, white stringy faeces, pits above the eyes, open sores, or refusal beyond two weeks in an adult or four days in a juvenile. At that point contact an aquatic veterinarian."),
    ],
    "related": [
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases & Parasites"),
        ("/guides/oscar-fish-care/food/", "Oscar Food & Feeding"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/oscar-fish-care/behavior/", "Oscar Behaviour"),
    ],
}


# ════════════════════════════════════════════════════════════════
# COLOR CHANGES
# ════════════════════════════════════════════════════════════════
COLOR_BODY = """    <p>Oscars change colour more than almost any other aquarium fish, and most of it is completely normal. The single most useful question is <strong>how fast did it happen</strong>: colour that shifts in seconds or minutes is mood, colour that shifts over days is stress, and colour that fades over weeks is a health or water problem.</p>

    <h2 id="speed-test">The Speed Test</h2>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Timescale</th><th>Meaning</th><th>Action</th></tr>
      <tr><td>Seconds to minutes</td><td>Mood &mdash; display, aggression, spawning, alarm</td><td>None. It reverses on its own</td></tr>
      <tr><td>Hours to days</td><td>Stress &mdash; move, new tank mate, parameter swing</td><td>Remove the stressor; expect recovery in days</td></tr>
      <tr><td>Weeks to months</td><td>Water quality, diet, illness, or ageing</td><td>Test water; review diet; check for other symptoms</td></tr>
      <tr><td>Gradual over the first 6 months of life</td><td>Normal juvenile-to-adult development</td><td>None</td></tr>
    </table></div>

    <h2 id="losing-color">Oscar Losing Colour or Turning Pale</h2>
    <p>A washed-out, faded oscar has one of these behind it:</p>
    <ul>
      <li><strong>Stress.</strong> A recent move, a water change with mismatched temperature, a new tank mate, or activity outside the tank. Colour comes back within a few days.</li>
      <li><strong>Chronic nitrate.</strong> The most common cause of a slow, unexplained fade. Test it; anything over 40 ppm is your answer.</li>
      <li><strong>Diet.</strong> Reds and oranges in oscars are carotenoid-based and genuinely fade on a poor or monotonous diet. A pellet containing astaxanthin plus regular frozen krill restores them over several weeks.</li>
      <li><strong>Lighting and background.</strong> Oscars pale over light substrate and bright bare tanks, and darken over sand and wood. This is camouflage, not illness.</li>
      <li><strong>Illness.</strong> Fading alongside clamped fins, refused food, laboured breathing or visible lesions is a symptom &mdash; see <a href="/guides/oscar-fish-care/diseases/">oscar diseases</a>.</li>
      <li><strong>Age.</strong> Very old oscars lose some intensity. Normal in a ten-year-old fish, not in a two-year-old.</li>
    </ul>

    <h2 id="turning-white">Oscar Turning White</h2>
    <p>Distinguish three different things people describe as "turning white":</p>
    <ul>
      <li><strong>Overall pallor</strong> &mdash; the stress response above. Fast onset, reverses.</li>
      <li><strong>Discrete white dots like salt grains</strong> &mdash; ich, not colour change. See <a href="/guides/oscar-fish-care/white-spots/">oscar white spots</a>.</li>
      <li><strong>Patchy white areas with a fuzzy or slimy texture</strong> &mdash; columnaris or fungus, and urgent. Grey-white saddle patches that spread within a day need immediate antibacterial treatment.</li>
    </ul>
    <p>There is also a legitimate variety consideration: albino, lutino, white and lemon oscars are pale by breeding. A fish that has always been white is not changing colour. See <a href="/guides/oscar-fish-care/types/">types of oscar fish</a>.</p>

    <h2 id="turning-black">Oscar Turning Black</h2>
    <p>Darkening is usually the least worrying of the colour changes.</p>
    <ul>
      <li><strong>Rapid full-body darkening</strong> &mdash; display or aggression. An oscar that goes near-black while facing another fish is posturing. It reverses in minutes.</li>
      <li><strong>Darkening during spawning</strong> &mdash; both parents typically darken while guarding eggs.</li>
      <li><strong>Darkening in response to the environment</strong> &mdash; sand, wood and dim lighting all encourage a darker fish.</li>
      <li><strong>Juvenile pattern development</strong> &mdash; a young tiger oscar's black base expands as it matures. Normal and permanent.</li>
      <li><strong>Sustained blackness with hiding and refused food</strong> &mdash; this one is stress or illness. Test the water.</li>
    </ul>

    <h2 id="black-spots">Oscar Black Spots</h2>
    <p>New black spots or patches on an oscar are, in order of likelihood:</p>
    <ol>
      <li><strong>Healing ammonia or nitrite burn.</strong> By far the most common. Melanin is deposited as burned tissue repairs, which is why the marks often appear <em>after</em> a water quality problem is over. They fade over weeks to months and sometimes leave a faint permanent shadow.</li>
      <li><strong>Normal pattern development.</strong> Tiger oscars gain and lose black marbling for their first year.</li>
      <li><strong>Stress marbling.</strong> Blotchy dark patches that come and go with mood and settle once the fish does.</li>
      <li><strong>Bruising after an injury</strong> or a collision with decor.</li>
      <li><strong>Black spot disease</strong> (digenean fluke cysts) &mdash; genuinely rare in aquariums, because the parasite's life cycle needs snails and fish-eating birds. Only consider it if the spots are uniform, raised, pepper-like dots.</li>
    </ol>
    <div class="callout"><strong>The diagnostic question for black spots:</strong> did you have an ammonia or nitrite reading in the last month, or is this a newly set up or recently disturbed tank? If yes, you are almost certainly looking at healing burn, and the treatment is clean water and time &mdash; not medication.</div>

    <h2 id="restore">Restoring Colour</h2>
    <ul>
      <li><strong>Nitrate under 20 ppm.</strong> The most reliable single change.</li>
      <li><strong>A pellet with astaxanthin and spirulina</strong>, plus frozen krill two or three times a week.</li>
      <li><strong>Dark substrate and wood.</strong> Oscars display better colour over a darker background.</li>
      <li><strong>Moderate lighting</strong> rather than a bright bare tank.</li>
      <li><strong>Reduce stress</strong> &mdash; adequate space, hiding places, no bullying tank mate.</li>
      <li><strong>Give it weeks.</strong> Carotenoid colour rebuilds slowly; judge it after a month, not a week.</li>
    </ul>
    <p>Related: <a href="/guides/oscar-fish-care/types/">oscar types and colours</a>, <a href="/guides/oscar-fish-care/water-parameters/">water parameters</a>.</p>
"""

COLOR = {
    "slug": "color-change",
    "title": "Oscar Fish Losing Color, Turning White or Turning Black",
    "meta_desc": "Why an oscar fish loses colour, turns white, turns black or develops black spots, how fast the change tells you the cause, and how to restore an oscar's colour.",
    "h1": "Oscar Fish Color Changes: Fading, White, Black and Black Spots",
    "hero_tag": "Color Changes",
    "hero_meta": "⚡ Seconds = mood &nbsp;|&nbsp; \U0001F4C6 Weeks = water or health &nbsp;|&nbsp; ⚫ Black spots usually healing burn",
    "toc_sections": [
        ("speed-test", "The Speed Test"),
        ("losing-color", "Losing Colour"),
        ("turning-white", "Turning White"),
        ("turning-black", "Turning Black"),
        ("black-spots", "Black Spots"),
        ("restore", "Restoring Colour"),
    ],
    "body": COLOR_BODY,
    "faqs": [
        ("Why is my oscar fish losing its colour?",
         "Fast fading over hours is a stress response to a move, a mismatched water change or a new tank mate, and it reverses in days. A slow fade over weeks points to nitrate above 40 ppm, a monotonous diet lacking carotenoids, or illness. Oscars also pale naturally over light substrate in a bright bare tank."),
        ("Why is my oscar fish turning black?",
         "Rapid full-body darkening is normal display, aggression or spawning behaviour and reverses in minutes. Juvenile tiger oscars also gain black as their adult pattern develops. Sustained darkness alongside hiding and refused food is stress or illness, so test the water."),
        ("Why does my oscar fish have black spots?",
         "The most common cause by far is healing ammonia or nitrite burn - melanin deposited as damaged tissue repairs, which is why the marks often appear after the water problem has passed. They fade over weeks to months. Normal pattern development, stress marbling and bruising account for most of the rest."),
        ("Why is my oscar turning white?",
         "Overall pallor is a stress response. Discrete white dots like salt grains are ich, not a colour change. Patchy white areas with a fuzzy or slimy texture that spread within a day are columnaris or fungus and need urgent antibacterial treatment. Albino and lemon oscars are pale by breeding."),
        ("Do oscar fish change colour when they are stressed?",
         "Yes, and it is one of the clearest stress signals in the hobby. Oscars pale, darken or go blotchy within seconds to hours in response to alarm, aggression, handling and parameter swings, and return to normal once the stressor is gone."),
        ("How do I make my oscar fish more colourful?",
         "Keep nitrate under 20 ppm, feed a pellet containing astaxanthin and spirulina with frozen krill two or three times a week, use dark substrate and wood rather than a bright bare tank, and reduce stress. Carotenoid colour rebuilds over weeks, so judge results after a month."),
    ],
    "related": [
        ("/guides/oscar-fish-care/types/", "Oscar Types & Colors"),
        ("/guides/oscar-fish-care/white-spots/", "Oscar White Spots (Ich)"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Parameters"),
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases"),
    ],
}


# ════════════════════════════════════════════════════════════════
# SWIMMING & BREATHING PROBLEMS
# ════════════════════════════════════════════════════════════════
SWIM_BODY = """    <p>An oscar swimming sideways, floating upside down, bloated, or hanging at the surface gulping air is showing one of two families of problem: a buoyancy and digestion problem, or an oxygen and gill problem. They look different once you know what to compare, and they need opposite responses.</p>
    <div class="callout"><strong>Sort it in one question.</strong> Is the fish struggling to stay upright and level (buoyancy &mdash; swim bladder, constipation, bloat), or struggling to breathe while swimming normally (oxygen &mdash; low O<sub>2</sub>, ammonia, gill parasites)? Everything below follows from that.</div>

    <h2 id="gasping">Oscar Gasping for Air at the Surface</h2>
    <p>A fish at the surface with rapid gill movement is not "getting air" &mdash; it is using the thin oxygen-rich layer at the surface because it cannot get enough elsewhere. Treat it as urgent.</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Cause</th><th>How to confirm</th><th>Fix</th></tr>
      <tr><td>Low dissolved oxygen</td><td>Warm tank, little surface movement, all fish affected</td><td>Add an airstone, increase surface agitation, cool slightly</td></tr>
      <tr><td>Ammonia or nitrite</td><td>Test kit; red or inflamed gills</td><td>50% water change now, then daily; stop feeding</td></tr>
      <tr><td>Gill flukes</td><td>One gill cover held shut, flicking, no water quality issue</td><td>Praziquantel</td></tr>
      <tr><td>Ich in the gills</td><td>White spots elsewhere on the body, scratching</td><td><a href="/guides/oscar-fish-care/white-spots/">Ich treatment</a> plus heavy aeration</td></tr>
      <tr><td>Tank too warm</td><td>Thermometer over 82&deg;F</td><td>Cool gradually; add aeration immediately</td></tr>
      <tr><td>Overstocking or a stalled filter</td><td>Everything is affected at once</td><td>Water change, aeration, check the filter is running</td></tr>
      <tr><td>Chlorine or chloramine</td><td>Started right after a water change</td><td>Dose dechlorinator immediately at the full tank volume</td></tr>
    </table></div>
    <p><strong>Immediate steps for a gasping oscar:</strong> add aeration, change 50% of the water with temperature-matched dechlorinated water, stop feeding, and test. That sequence is safe whatever the cause turns out to be.</p>

    <h2 id="bloated">Bloated Oscar or Swollen Belly</h2>
    <p>Swelling is a symptom, not a diagnosis. What surrounds it decides what to do:</p>
    <div class="tblwrap"><table class="ptbl">
      <tr><th>Pattern</th><th>Likely cause</th><th>Response</th></tr>
      <tr><td>Rounded belly, no faeces, fish still active</td><td>Constipation</td><td>Fast 3 days, then blanched deshelled pea; Epsom salt 1 tbsp/5 gal</td></tr>
      <tr><td>Belly swollen, scales raised like a pinecone</td><td>Dropsy &mdash; organ failure</td><td>Hospital tank, Epsom salt, antibacterial; poor prognosis</td></tr>
      <tr><td>Swelling with white stringy faeces and weight loss</td><td>Internal parasites</td><td>Metronidazole or a dewormer</td></tr>
      <tr><td>Belly full, fish eating heavily</td><td>Overfeeding</td><td>Reduce portions; adopt the 3-minute rule</td></tr>
      <tr><td>Fuller belly, rock cleaning, breeding tube visible</td><td>Gravid female</td><td>Nothing &mdash; see <a href="/guides/oscar-fish-care/breeding/">breeding</a></td></tr>
      <tr><td>One-sided or lumpy swelling</td><td>Tumour or internal growth</td><td>Veterinary assessment</td></tr>
    </table></div>
    <p>Constipation is the most common of these in oscars and the easiest to fix: it is caused by too much dry food, food that was not pre-soaked, or a diet with no vegetable content at all.</p>

    <h2 id="sideways">Swimming Sideways, Upside Down or Sinking</h2>
    <p>These are swim bladder problems. In oscars the causes, in order:</p>
    <ol>
      <li><strong>Constipation or overfeeding.</strong> A distended gut presses on the swim bladder. Most common cause by a wide margin, and reversible.</li>
      <li><strong>Gulped air.</strong> Fish that take floating pellets aggressively from the surface swallow air. Switch to sinking or pre-soaked food.</li>
      <li><strong>Dry food expanding in the gut.</strong> Soak pellets and freeze-dried food before feeding.</li>
      <li><strong>Bacterial infection of the swim bladder.</strong> Usually alongside other signs of illness; needs an antibacterial.</li>
      <li><strong>Injury.</strong> After a collision, a jump, or rough handling.</li>
      <li><strong>Chronic stunting.</strong> A fish grown in an undersized tank can develop permanent spinal and swim bladder problems. See <a href="/guides/oscar-fish-care/size-growth/">size and growth</a>.</li>
      <li><strong>Cold water.</strong> Digestion slows below 74&deg;F and buoyancy problems follow.</li>
    </ol>

    <h3>The standard swim bladder protocol</h3>
    <ol>
      <li><strong>Fast the fish for three days.</strong> This alone resolves a large share of cases.</li>
      <li><strong>Test and correct the water.</strong> Ammonia and nitrite at 0, nitrate under 40 ppm.</li>
      <li><strong>Raise the temperature to 79&ndash;80&deg;F</strong> to speed digestion.</li>
      <li><strong>Add Epsom salt</strong> (magnesium sulphate) at 1 tablespoon per 5 gallons &mdash; a muscle relaxant that helps the gut clear. Not table salt, not aquarium salt.</li>
      <li><strong>Feed a blanched, deshelled pea</strong> on day four.</li>
      <li><strong>Lower the water level</strong> if the fish is struggling to reach the surface, and reduce flow so it is not fighting the current.</li>
      <li><strong>If nothing improves in a week</strong> and other symptoms are present, treat with an antibacterial in a hospital tank.</li>
    </ol>
    <div class="callout callout-warn"><strong>Rule out playing dead.</strong> Oscars lie motionless on their side as a genuine behaviour, then swim off normally. If the fish rights itself instantly when startled and has clean water tests, you are probably watching theatre &mdash; see <a href="/guides/oscar-fish-care/behavior/">oscar behaviour</a>.</div>

    <h2 id="other">Other Abnormal Swimming</h2>
    <ul>
      <li><strong>Glass surfing</strong> &mdash; pacing the front pane repeatedly. Usually a bored fish in a bare tank, sometimes a reflection it is displaying at, sometimes a water quality problem.</li>
      <li><strong>Shimmying in place</strong> &mdash; rocking without forward movement. Check temperature and hardness, then look for neurological causes such as long-term thiaminase exposure from a feeder-fish diet.</li>
      <li><strong>Scratching and flicking against decor</strong> &mdash; parasites or an irritant such as ammonia. See <a href="/guides/oscar-fish-care/diseases/">diseases and parasites</a>.</li>
      <li><strong>Darting and crashing into decor</strong> &mdash; a startle response, or a genuine toxin exposure. Test, and consider what went into or near the tank recently.</li>
      <li><strong>Hovering nose-down in a corner</strong> &mdash; stress or illness; test water and check for other symptoms.</li>
    </ul>

    <h2 id="prevention">Preventing All of It</h2>
    <ul>
      <li>Pre-soak dry food; use sinking or slow-sinking pellets rather than floating ones.</li>
      <li>Feed to the 3-minute rule with a weekly fasting day &mdash; see <a href="/guides/oscar-fish-care/food/">oscar feeding</a>.</li>
      <li>Include vegetable content weekly.</li>
      <li>Keep an airstone running, particularly in summer.</li>
      <li>Hold the tank at a stable 77&ndash;80&deg;F.</li>
      <li>40&ndash;50% weekly water changes, temperature-matched and dechlorinated.</li>
      <li>Give the fish a tank large enough that it never had to grow up stunted.</li>
    </ul>
"""

SWIM = {
    "slug": "swimming-problems",
    "title": "Oscar Fish Swimming Sideways, Bloated or Gasping for Air",
    "meta_desc": "Why an oscar fish swims sideways or upside down, bloats, or gasps at the surface, with cause tables and the standard swim bladder treatment protocol.",
    "h1": "Oscar Fish Swimming and Breathing Problems",
    "hero_tag": "Swimming & Breathing",
    "hero_meta": "\U0001F300 Buoyancy vs oxygen &nbsp;|&nbsp; \U0001F374 Fast 3 days, then peas &nbsp;|&nbsp; \U0001F4A8 Gasping is urgent",
    "toc_sections": [
        ("gasping", "Gasping for Air"),
        ("bloated", "Bloated or Swollen Belly"),
        ("sideways", "Sideways & Upside Down"),
        ("other", "Other Abnormal Swimming"),
        ("prevention", "Prevention"),
    ],
    "body": SWIM_BODY,
    "faqs": [
        ("Why is my oscar fish gasping for air at the surface?",
         "It cannot get enough oxygen elsewhere in the tank. The usual causes are low dissolved oxygen in warm or still water, ammonia or nitrite poisoning, gill flukes, ich in the gills, or chlorine after an undosed water change. Add aeration, change 50% of the water and test immediately."),
        ("Why is my oscar fish swimming sideways?",
         "This is a swim bladder problem, most often caused by constipation or overfeeding, gulped air from taking floating food at the surface, or dry food expanding in the gut. Fast the fish three days, raise the temperature to 79-80F, add Epsom salt at 1 tablespoon per 5 gallons, then feed a blanched deshelled pea."),
        ("Why is my oscar fish upside down but still alive?",
         "A fish that floats or rolls but is otherwise responsive almost always has a buoyancy problem rather than a fatal illness. Work through the swim bladder protocol: fast, correct the water, warm the tank, Epsom salt and a pea. Also rule out playing dead, a genuine oscar behaviour."),
        ("Why is my oscar fish bloated?",
         "Constipation is the most common cause and is fixed by fasting and a blanched pea. Swelling with raised pinecone scales is dropsy and serious. Swelling with white stringy faeces and weight loss points to internal parasites. A gravid female swells for a few days before spawning."),
        ("What is the treatment for swim bladder in an oscar?",
         "Fast for three days, confirm ammonia and nitrite are 0 and nitrate is under 40 ppm, raise the temperature to 79-80F, add Epsom salt at 1 tablespoon per 5 gallons, then offer a blanched deshelled pea on day four. Lower the water level and reduce flow if the fish is struggling."),
        ("Why does my oscar keep swimming against the glass?",
         "Glass surfing is usually boredom in a bare tank, a reflection the fish is displaying at, or a water quality problem. Add structure the fish can explore and rearrange, reduce external reflections, and test ammonia, nitrite and nitrate."),
    ],
    "related": [
        ("/guides/oscar-fish-care/diseases/", "Oscar Diseases & Parasites"),
        ("/guides/oscar-fish-care/food/", "Oscar Food & Feeding"),
        ("/guides/oscar-fish-care/water-parameters/", "Water Parameters"),
        ("/tools/water-parameter-checker/", "Water Parameter Checker"),
    ],
}


# ════════════════════════════════════════════════════════════════
PAGES = [TANK, WATER, FOOD, SIZE, LIFESPAN, TYPES, SEX, BREED, MATES,
         BEHAV, DIS, HITH, ICH, EAT, COLOR, SWIM]


def main():
    for spec in PAGES:
        html = page(
            slug=spec["slug"], title=spec["title"], meta_desc=spec["meta_desc"],
            h1=spec["h1"], hero_tag=spec["hero_tag"], hero_meta=spec["hero_meta"],
            toc_sections=spec["toc_sections"], body_html=spec["body"],
            faqs=spec["faqs"], related=spec["related"],
        )
        out_dir = BASE / spec["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"  /guides/oscar-fish-care/{spec['slug']}/{'':<20} {len(html):>7,} bytes")
    print(f"\n{len(PAGES)} pages written to {BASE}")


if __name__ == "__main__":
    main()
