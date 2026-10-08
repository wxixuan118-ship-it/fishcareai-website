#!/usr/bin/env python3
"""Build the clownfish disease species pages and the nginx 301 map.

  python3 scripts/build-clownfish-cluster.py            # write pages
  python3 scripts/build-clownfish-cluster.py --nginx    # print nginx 301 blocks

Click depth stays at 3: Home -> /aquarium-fish-diseases/clownfish/ -> species page.
The 150 legacy /fish-health/<species>-clownfish-<symptom> pages 301 to the
matching section of the species page.
"""
import html, json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from clownfish_cluster_data import REFS, GROUPS, SPECIES, DISEASES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.fishcareai.com"
HUB = "/aquarium-fish-diseases/clownfish/"
HUB_NAME = "Clownfish Health Problems"
UPDATED = "2026-10-08"
TOC_LABEL = {"breathing": "Breathing", "skin": "Spots &amp; slime", "appetite": "Appetite &amp; belly", "swimming": "Swimming &amp; balance",
             "eyes": "Eyes", "fins": "Fins", "behavior": "Behavior", "color": "Color"}
LVL = {"r": "Emergency", "a": "Urgent", "g": "Watch"}


def url(key):
    return f"/aquarium-fish-diseases/{key}-clownfish-diseases/"


NAV = ('<nav class="nb"><a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>'
       '<div class="nav"><a href="/">Home</a><a href="/guides/">Guides</a><a href="/species">Encyclopedia</a><a class="act" href="/fish-health/">Fish Health</a>'
       '<a href="/identify/">🔍 Fish ID</a><a href="/#tools">Tools</a><a class="cta" href="/#tools">Try AI Free</a></div></nav>')
FOOTER = ('<footer>© 2026 FishCare AI · {name}<nav class="legal-links" aria-label="Legal and company information"><a href="/about/">About</a>'
          '<a href="/contact/">Contact</a><a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a><a href="/image-credits/">Image Credits</a></nav></footer>')


def head(title, desc, canonical, image, schema):
    t = html.unescape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{SITE}{canonical}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{SITE}{canonical}"/>
<meta property="og:image" content="{SITE}{image}"/>
<meta property="og:site_name" content="FishCare AI"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="preload" as="image" href="{image}" fetchpriority="high"/>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260823-screenshot"/>
<link rel="stylesheet" href="/assets/clownfish-health.css?v=20261008"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879"/>
<script defer src="/assets/site-compliance.js?v=20260824-dark-fix"></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
"""


def ref_list(keys):
    items = "".join(f'<li>{REFS[k][0]} <a href="{REFS[k][1]}" rel="noopener" target="_blank">Source</a></li>' for k in keys)
    return f'<ol class="refs">{items}</ol>'


def species_page(key, sp):
    others = [k for k in SPECIES if k != key]
    path = url(key)
    used = []
    kw = f"{sp['name'].lower()} clownfish diseases"

    def cite(keys):
        for k in keys:
            if k not in used:
                used.append(k)
        nums = sorted(used.index(k) + 1 for k in keys)
        return "".join(f'<sup><a href="{path}#ref-{used[n - 1]}">[{n}]</a></sup>' for n in nums)

    why_cite = cite(sp["why_refs"]) if sp["why_refs"] else ""
    why = "".join(f"<p>{p}{why_cite if i == len(sp['why']) - 1 else ''}</p>" for i, p in enumerate(sp["why"]))

    groups = []
    for gid, gname, lvl, terms, core, grefs in GROUPS:
        words = ", ".join(t.replace("-", " ") for t in terms)
        groups.append(
            f'<div class="sgroup" id="{gid}"><h3>{gname}<span class="lvl {lvl}">{LVL[lvl]}</span></h3>'
            f'<p class="terms">Covers: {words}</p>'
            f'<p>{core}{cite(grefs) if grefs else ""}</p>'
            f'<p class="note"><strong>{sp["name"]} note:</strong> {sp["notes"][gid]}</p></div>')

    rows = []
    for name, latin, sign, lv, speed, treat, drefs in DISEASES:
        rows.append(f'<tr><td>{name}<small>{latin}</small></td><td>{sign}</td><td><span class="speed {lv}">{speed}</span></td><td>{treat}{cite(drefs)}</td></tr>')

    faq_html = "".join(f"<details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>" for i, (q, a) in enumerate(sp["faq"]))
    sib = "".join(f'<a class="guide-link" href="{url(k)}">{SPECIES[k]["full"]} diseases<span>{SPECIES[k]["latin"]}</span></a>' for k in others)
    cr = sp["credit"]
    src = next((i for i in IMG if i["localFile"] == sp["img"]), {})
    # build references last so numbering matches first use
    body_main = f"""
<section class="card" id="answer">
  <span class="eyebrow">Quick answer</span>
  <h2>What diseases affect {sp["name"].lower()} clownfish?</h2>
  <p class="lead">Most {kw} come from stress and a handful of marine parasites. {sp["answer"]}{cite(["blasiola"]) if key != "ocellaris" else cite(["ramudu", "cheng"])}</p>
  <div class="answer"><p><strong>Act the same day</strong> if your {sp["name"].lower()} clownfish breathes fast and shows dust, slime or peeling skin. Velvet and Brooklynella can kill within days; move the fish to a quarantine tank and start treatment.</p></div>
  <p>For any other symptom, test ammonia, nitrite, salinity and temperature first — water problems cause more illness than any single parasite.</p>
</section>

<section class="card" id="profile">
  <span class="eyebrow">Species risk profile</span>
  <h2>Why {sp["name"].lower()} clownfish get sick</h2>
  <div class="profile"><div>{why}
    <div class="table-wrap"><table class="facts" style="min-width:0"><tbody>
      <tr><th>Scientific name</th><td><em>{sp["latin"]}</em> ({sp["alias"]})</td></tr>
      <tr><th>Adult size</th><td>{sp["size"]}</td></tr>
      <tr><th>Temperament</th><td>{sp["temper"]}</td></tr>
      <tr><th>Usual source</th><td>{sp["source"]}</td></tr>
      <tr><th>Main health risk</th><td>{sp["risk"]}</td></tr>
    </tbody></table></div></div>
    <figure><img src="{sp["img"]}" alt="Healthy {sp["name"].lower()} clownfish for comparison when checking for {kw}" width="600" height="450" loading="lazy" decoding="async"/>
    <figcaption>{sp["full"]}. Photo: {cr[0]} via <a href="{src.get("sourcePage", "https://commons.wikimedia.org/")}" rel="noopener" target="_blank">Wikimedia Commons</a>, <a href="{cr[2]}" rel="license noopener" target="_blank">{cr[1]}</a>. Resized.</figcaption></figure>
  </div>
</section>

<section class="card" id="symptoms">
  <span class="eyebrow">Symptoms</span>
  <h2>{sp["full"]} symptoms and what they mean</h2>
  <p>Most {kw} first show up as one of eight symptom groups, covering the 30 signs owners describe most often. Find the closest match, check the urgency label, then confirm the likely disease in the table below.</p>
  {"".join(groups)}
</section>

<section class="card" id="diseases">
  <span class="eyebrow">Diagnosis</span>
  <h2>Common {sp["name"].lower()} clownfish diseases and treatment</h2>
  <p>These are the parasites most often behind the symptoms above. The <a href="{HUB}#diseases">clownfish health problems guide</a> compares them side by side with an illustration of what each looks like.</p>
  <div class="table-wrap"><table class="facts"><thead><tr><th>Disease</th><th>What you see</th><th>Speed</th><th>Treatment in quarantine</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
  <h3>Treating a {sp["name"].lower()} clownfish</h3>
  <p>{sp["treat"]}</p>
  <p>Copper is effective against ich and velvet only while free copper stays at 0.15–0.20 mg/L, so measure it with a test kit at least daily; it is lethal to most invertebrates and must never go into a reef tank.{cite(["fa165"])} Leave the display without fish while you treat: marine ich can complete its life cycle in anything from 6 days to 11 weeks, and its guidance calls for 3–6 weeks of quarantine, sometimes 7–11.{cite(["fa164"])}</p>
</section>

<section class="card" id="prevent">
  <span class="eyebrow">Prevention</span>
  <h2>How to keep {sp["name"].lower()} clownfish healthy</h2>
  <div class="params">
    <div class="param"><span>Temp</span><b>74–80°F</b></div>
    <div class="param"><span>Salinity</span><b>1.020–1.025</b></div>
    <div class="param"><span>pH</span><b>8.0–8.4</b></div>
    <div class="param"><span>Ammonia / NO₂</span><b>0 ppm</b></div>
    <div class="param"><span>Nitrate</span><b>&lt; 20 ppm</b></div>
  </div>
  <p>Most {kw} arrive with a new fish, so quarantine every new fish for at least four weeks before it joins your {sp["name"].lower()} clownfish, buy captive-bred where you can, and keep temperature and salinity steady. Feed a varied marine diet in small portions; a fish in good condition fights off parasites that would overwhelm a stressed one.</p>
  <p>Full setup advice is in the <a href="/guides/clownfish-care-guide/">clownfish care guide</a>.</p>
</section>

<section class="card" id="faq">
  <h2>{sp["full"]} diseases FAQ</h2>
  {faq_html}
</section>

<section class="card" id="related">
  <h2>Other clownfish disease guides</h2>
  <div class="sib">{sib}</div>
  <p style="margin-top:14px"><a href="{HUB}">← All clownfish health problems</a></p>
</section>
"""
    refs = "".join(f'<li id="ref-{k}">{REFS[k][0]} <a href="{REFS[k][1]}" rel="noopener" target="_blank">Read source</a></li>' for k in used)
    body_main += f"""
<section class="card" id="sources">
  <h2>Research sources</h2>
  <ol class="refs">{refs}</ol>
  <div class="byline"><div class="byline-mark">FC</div><p><strong>FishCare AI Editorial Team</strong> · Reviewed October 2026. Educational information only — consult an aquatic veterinarian for severe or persistent symptoms. <a href="/editorial-policy/">Editorial policy</a></p></div>
</section>
"""
    toc = "".join(f'<a href="{path}#{i}">{t}</a>' for i, t in [("answer", "Quick answer"), ("profile", "Risk profile"), ("symptoms", "Symptoms")]
                  + [(g[0], TOC_LABEL[g[0]]) for g in GROUPS] + [("diseases", "Diseases &amp; treatment"), ("prevent", "Prevention"), ("faq", "FAQ"), ("sources", "Sources")])

    crumbs = [("Home", "/"), (HUB_NAME, HUB), (f"{sp['full']} Diseases", path)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": html.unescape(sp["title"]), "description": sp["desc"], "image": SITE + sp["img"],
         "datePublished": UPDATED, "dateModified": UPDATED, "mainEntityOfPage": SITE + path,
         "author": {"@type": "Organization", "name": "FishCare AI Editorial Team", "url": SITE + "/editorial-policy/"},
         "publisher": {"@type": "Organization", "name": "FishCare AI", "logo": {"@type": "ImageObject", "url": SITE + "/assets/fishcare-logo.svg"}},
         "citation": [REFS[k][1] for k in used]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sp["faq"]]},
    ]}
    crumb_html = '<span>/</span>'.join([f'<a href="/">Home</a>', f'<a href="{HUB}">{HUB_NAME}</a>', f"{sp['full']}"])
    hero = f"""{NAV}
<header class="cf-hero">
  <img src="{sp["img"]}" alt="{sp["img_alt"]}" width="1600" height="1100" fetchpriority="high"/>
  <div class="hero-inner">
    <div class="crumbs">{crumb_html}</div>
    <span class="tag">Saltwater Fish Health</span>
    <h1>{sp["full"]} Diseases: Symptoms, Causes and Treatment</h1>
    <p>Identify {kw} from the symptoms you can see on <em>{sp["latin"]}</em>, judge how urgent each one is, and treat it safely in quarantine.</p>
  </div>
</header>
<main class="page">
<aside class="toc" aria-label="Article navigation"><strong>On this page</strong><div class="toc-list">{toc}</div>
<div class="toc-cta">Not sure what you're looking at? <a href="/#tools">Upload a photo to the AI fish doctor →</a></div></aside>
<article class="article">"""
    return head(sp["title"], sp["desc"], path, sp["img"], schema) + hero + body_main + "</article>\n</main>\n" + FOOTER.format(name=f"{sp['full']} Diseases") + "\n</body>\n</html>\n"


def nginx_blocks():
    out = ["    # ── Clownfish cluster (2026-10-08): 150 symptom pages + 5 species health hubs",
           "    # consolidated into /aquarium-fish-diseases/<species>-clownfish-diseases/.",
           "    # Must stay above the trailing-slash regex and the /fish-health proxy."]
    out.append("    location ~ ^/fish-health/fish/(?:true-)?(percula|ocellaris|tomato|maroon)-clownfish/?$ { return 301 /aquarium-fish-diseases/$1-clownfish-diseases/; }")
    for gid, _, _, terms, _, _ in GROUPS:
        out.append(f"    location ~ ^/fish-health/(?:true-)?(percula|ocellaris|tomato|maroon)-clownfish-(?:{'|'.join(terms)})/?$ {{ return 301 /aquarium-fish-diseases/$1-clownfish-diseases/#{gid}; }}")
    return "\n".join(out)


IMG = json.load(open(os.path.join(ROOT, "assets/encyclopedia/real/real-image-sources.json")))
if isinstance(IMG, dict):
    IMG = IMG.get("images") or list(IMG.values())

if __name__ == "__main__":
    if "--nginx" in sys.argv:
        print(nginx_blocks())
        sys.exit()
    for key, sp in SPECIES.items():
        d = os.path.join(ROOT, url(key).strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(species_page(key, sp))
        print("wrote", url(key))
