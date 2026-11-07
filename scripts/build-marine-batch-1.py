#!/usr/bin/env python3
"""Build the first saltwater and equipment batch as static pages.

Run from the repo root. The CSS, nav and footer come from an existing guide so the
pages inherit the site chrome. Page copy lives here; edit it and re-run.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from marine_batch_1_figures import write_all  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.fishcareai.com"
SHELL = (ROOT / "guides/tang-fish-care/diseases/index.html").read_text(encoding="utf-8")
UPDATED = "2026-11-07"

STYLE = re.search(r"<style>:root.*?</style>", SHELL, re.S).group(0)
GLASS = re.search(r'<link rel="stylesheet" href="/assets/fishcare-glass-redesign\.css[^>]*>', SHELL).group(0)
FOOTER = SHELL[SHELL.index('<footer class="ft">'):SHELL.index("</body>")]

EXTRA_CSS = """<style>
.cta-box{border-radius:14px;padding:20px 22px;margin:22px 0;color:#fff}
.artc .cta-box h3{color:#fff;margin:0 0 7px;font-size:1rem}
.artc figure{margin:20px 0}
.artc figure img{display:block;width:100%;height:auto;border-radius:14px}
.artc figcaption{font-size:.8rem;line-height:1.5;margin-top:7px;opacity:.85}
.artc .cta-box p{color:rgba(255,255,255,.86);font-size:.88rem;margin-bottom:14px}
.artc .cta-box a.btn{display:inline-block;background:#fff;color:#0F3D5E;padding:9px 18px;border-radius:8px;font-weight:700;font-size:.88rem}
.table-wrap{overflow-x:auto;margin:14px 0 18px}
.ptbl{width:100%;border-collapse:collapse;font-size:.88rem;min-width:460px}
.calc-box{border:1px solid var(--bd);border-radius:16px;padding:20px;margin:0 0 22px}
.calc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.calc-box label{display:block;font-size:.84rem;font-weight:600;margin-bottom:5px}
.calc-box input,.calc-box select{width:100%;padding:10px 12px;border:1px solid var(--bd);border-radius:8px;font-size:16px;background:#fff;color:#1A2B3C}
.calc-note{font-size:.8rem;margin-top:5px;opacity:.85}
.calc-btn{margin-top:16px;width:100%;padding:12px;border:0;border-radius:10px;background:#1B5E8B;color:#fff;font-size:1rem;font-weight:700;cursor:pointer}
.calc-out{margin-top:16px;padding:16px;border-radius:12px;background:rgba(46,158,125,.14);border:1px solid rgba(46,158,125,.4)}
.calc-big{font-size:1.5rem;font-weight:800;margin-bottom:6px}
.calc-out ul{margin:8px 0 0 18px}
.calc-err{color:#E74C3C;font-weight:600}
.presets{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}
.presets button{padding:7px 12px;border-radius:999px;border:1px solid var(--bd);background:transparent;color:inherit;font-size:.82rem;cursor:pointer}
.page-meta{font-size:.82rem;opacity:.8;margin-bottom:16px}
.refs li{font-size:.86rem}
.artlay>*{min-width:0}
@media(max-width:640px){.calc-grid{grid-template-columns:1fr}.artc{padding:22px 18px}}
</style>"""

CLUSTER = [
    ("/guides/saltwater-fish-quarantine/", "🧪 Saltwater Fish Quarantine"),
    ("/guides/saltwater-ich-treatment/", "🩺 Saltwater Ich Treatment"),
    ("/guides/reef-tank-salinity/", "🌊 Reef Tank Salinity"),
    ("/tools/aquarium-heater-calculator/", "🌡️ Aquarium Heater Calculator"),
    ("/tools/aquarium-weight-calculator/", "⚖️ Aquarium Weight Calculator"),
    ("/guides/clownfish-care-guide/", "🐠 Clownfish Care Guide"),
    ("/guides/tang-fish-care/", "🐟 Tang Fish Care Guide"),
]


def app_cta(placement):
    return f"""<div class="cta-box" data-app-cta="{placement}" style="background:linear-gradient(135deg,#0F3D5E,#2E9E7D)">
  <h3>🧪 Test your water first</h3>
  <p>Ammonia, nitrite and temperature problems can cause or worsen many fish symptoms. Enter your readings in our free water parameter checker to see what's out of range.</p>
  <a class="btn" href="/tools/water-parameter-checker/">Check My Water →</a>
</div>"""


DIMS = write_all(ROOT)


def photo_size(name):
    out = subprocess.run(["file", str(ROOT / "assets/encyclopedia/real" / name)], capture_output=True, text=True).stdout
    w, h = re.findall(r"(\d{3,5})x(\d{3,5})", out)[-1]
    return w, h


def fig(name, alt, caption):
    w, h = DIMS[name]
    return f'<figure><img src="/assets/guides/marine/{name}.svg" alt="{html.escape(alt, quote=True)}" width="{w}" height="{h}" loading="lazy"/><figcaption>{caption}</figcaption></figure>'


def photo(name, alt, caption):
    w, h = photo_size(name)
    return f'<figure><img src="/assets/encyclopedia/real/{name}" alt="{html.escape(alt, quote=True)}" width="{w}" height="{h}" loading="lazy"/><figcaption>{caption} <a href="/image-credits/">Image credits</a>.</figcaption></figure>'


def page(p):
    url = f"{SITE}{p['path']}"
    if p["kind"] == "tool":
        m = re.search(r"\s*<p>This <strong>.*?</p>", p["body"], re.S)
        p["body"] = m.group(0).lstrip("\n") + "\n\n" + p["body"].replace(m.group(0), "", 1)
    is_tool = p["kind"] == "tool"
    parent = ("/tools/", "Tools") if is_tool else ("/guides/", "Guides")
    title, desc = html.escape(p["title"]), html.escape(p["description"], quote=True)
    img = f"/assets/encyclopedia/real/{p['image']}"
    style = STYLE.replace("/assets/encyclopedia/real/tang-fish-wikimedia-real.jpg", img)

    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": parent[1], "item": f"{SITE}{parent[0]}"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url},
        ],
    }
    author = {"@type": "Organization", "name": "FishCare AI", "url": f"{SITE}/"}
    if is_tool:
        main = {
            "@context": "https://schema.org", "@type": "WebApplication", "name": p["h1"], "url": url,
            "description": p["description"], "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "Any", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        }
    else:
        main = {
            "@context": "https://schema.org", "@type": "Article", "headline": p["title"],
            "description": p["description"], "datePublished": UPDATED, "dateModified": UPDATED,
            "author": author, "publisher": author, "mainEntityOfPage": url, "image": f"{SITE}{img}",
        }
    faq = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in p["faq"]
        ],
    }
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>'
        for x in (crumbs, main, faq)
    )
    faq_html = "\n".join(
        f"    <h3>{html.escape(q)}</h3>\n    <p>{html.escape(a)}</p>" for q, a in p["faq"]
    )
    toc = "\n".join(
        f'      <a href="{p["path"]}#{i}">{html.escape(t)}</a>'
        for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])
    )
    cur = ' class="cur"'
    cluster = "\n".join(
        f'      <a href="{h}"{cur if h == p["path"] else ""}>{n}</a>' for h, n in CLUSTER
    )
    refs = "\n".join(
        f'      <li><a href="{u}" target="_blank" rel="noopener">{html.escape(n)}</a></li>' for n, u in p["refs"]
    )
    related = "".join(f'<a href="{h}" title="{html.escape(n)}">{html.escape(n)}</a>' for h, n in p["related"])
    scripts = '<script defer src="/assets/app-cta.js?v=20261107b"></script>'
    tool_script = f"\n<script>\n{p['script']}\n</script>" if p.get("script") else ""
    guides_act = ' act' if not is_tool else ''
    tools_act = ' act' if is_tool else ''

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true" data-cms-sync="off">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{url}"/>
<meta property="og:type" content="{'website' if is_tool else 'article'}"/>
<meta property="og:site_name" content="FishCare AI"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:image" content="{SITE}{img}"/>
<meta name="twitter:card" content="summary_large_image"/>
{ld}
{style}
{EXTRA_CSS}
{GLASS}
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260923-analytics"></script>{scripts}
<style id="mobile-fit">@media(max-width:860px){{.artlay>*,.sp-layout>*,.wrap>*,.content>*,.layout>*,main>*{{min-width:0}}.artc img,main figure img{{max-width:100%;height:auto}}.fig-scroll{{max-width:100%;overflow-x:auto}}.artc table,main .card table,.content table,.cmp-table{{display:block;max-width:100%;overflow-x:auto}}.artc p,.artc li,.artc td,main .card p{{overflow-wrap:anywhere}}}}</style></head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl{guides_act}" href="/guides/">Guides</a>
    <a class="nl" href="/species">Encyclopedia</a>
    <a class="nl" href="/fish-health">Fish Health</a>
    <a class="nl{tools_act}" href="/tools/">Tools</a>
    <a class="nl" href="/about/">About Us</a>
  </div>
  <button class="hbg" aria-label="Menu" onclick="document.querySelector('.nlinks').classList.toggle('open')">
    <span></span><span></span><span></span>
  </button>
</nav>

<main>
<section class="guide-hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="{parent[0]}">{parent[1]}</a><span>/</span>
      <span style="color:rgba(255,255,255,.9)">{html.escape(p['crumb'])}</span>
    </div>
    <div class="tag" style="background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)">{p['tag']}</div>
    <h1>{html.escape(p['h1'])}</h1>
    <div class="guide-meta">{p['meta']}</div>
  </div>
</section>

<div class="artlay">
  <article class="artc">
    <p class="page-meta">Updated November 7, 2026 · FishCare AI editorial team</p>
{p['body']}

    <h2 id="faq">{html.escape(p['faq_h2'])}</h2>
{faq_html}

    <h2 id="method">{html.escape(p['method_h2'])}</h2>
    <p>{p['method']}</p>

    <h2 id="references">References</h2>
    <ul class="refs">
{refs}
    </ul>

    <h2 id="related">Related Guides and Tools</h2>
    <div class="guide-links">{related}</div>
  </article>

  <aside class="sidebar">
    <div class="cluster-nav">
      <p class="sb-h">Saltwater &amp; Equipment</p>
{cluster}
    </div>
    <div class="toc">
      <p class="sb-h">On this page</p>
{toc}
      <a href="{p['path']}#faq">FAQ</a>
    </div>
  </aside>
</div>
</main>

{FOOTER}{tool_script}
</body>
</html>
"""


FA164 = ("UF/IFAS Extension FA164: Cryptocaryon irritans Infections in Fish", "https://ask.ifas.ufl.edu/publication/FA164")
FISHVET = ("Fish Vet (Dr. Jessie Sanders): Correct Quarantine Tank Setup", "https://cafishvet.com/fish-tanks/correct-quarantine-tank-setup/")
BRS_QT = ("Bulk Reef Supply: How to Set Up a Quarantine Tank", "https://www.bulkreefsupply.com/content/post/md-2020-05-how-to-setup-a-quarantine-tank")
BRS_ICH = ("Bulk Reef Supply: The Life Cycle of Marine Ich", "https://www.bulkreefsupply.com/content/post/md-how-to-get-rid-of-ich-in-a-reef-tank-separating-fact-from-fiction")
RHF = ("Randy Holmes-Farley, Reefkeeping: What is Salinity?", "http://reefkeeping.com/issues/2006-12/rhf/index.php")
BRS_SAL = ("Bulk Reef Supply: How to Measure Salinity in a Saltwater Aquarium", "https://www.bulkreefsupply.com/content/post/md-2019-06-salinity-measurements-in-aquariums-2")
BRS_SALT = ("Bulk Reef Supply: How Much Salt Do I Put in My Saltwater Tank?", "https://www.bulkreefsupply.com/content/post/how-much-salt-do-i-put-in-my-saltwater-tank")
TANKARIUM = ("Tankarium: Aquarium Sizes and Weights", "https://www.tankarium.com/?p=10474")
TOPSHELF = ("Top Shelf Aquatics: Aquarium Weight Calculator", "https://topshelfaquatics.com/pages/aquarium-weight-calculator")
BYA = ("Build Your Aquarium: Aquarium Heater Size", "https://www.buildyouraquarium.com/aquarium-heater-size/")
FISHLAB = ("Fish Laboratory: Aquarium Heater Guide", "https://www.fishlaboratory.com/fish/aquarium-heater/")

PAGES = []

PAGES.append({
    "kind": "guide", "path": "/guides/saltwater-fish-quarantine/", "image": "yellow-tang-wikimedia-real.jpg",
    "title": "Saltwater Fish Quarantine: Tank Setup and 4-6 Week Plan",
    "description": "Saltwater fish quarantine explained: how long to quarantine, the bare-bottom tank setup, what to watch each week and when a new fish is safe to add.",
    "h1": "Saltwater Fish Quarantine: Tank Setup and a 4-6 Week Plan",
    "crumb": "Saltwater Fish Quarantine", "tag": "🧪 Saltwater Health",
    "meta": "⏳ Plan on 4–6 weeks &nbsp;|&nbsp; 🪣 Bare-bottom tank &nbsp;|&nbsp; 🔬 Watch first, treat when there's a reason",
    "body": f"""    <p><strong>Saltwater fish quarantine</strong> means keeping every new fish in a separate tank for <strong>4 to 6 weeks</strong> before it joins your display. An aquatic veterinarian ties that length to how long pathogens take to incubate and show signs. The practical reason is simple: once marine ich reaches a reef, you can't treat the display with copper, because corals and invertebrates are highly sensitive to many ich medications.</p>

{photo("yellow-tang-wikimedia-real.jpg", "Yellow tang, a new saltwater fish that needs quarantine before joining a reef", "Tangs are often among the first fish to show marine ich, so keepers take extra care quarantining them.")}

    <h2 id="how-long">How Long to Quarantine Saltwater Fish</h2>
    <p>Use <strong>4 to 6 weeks</strong> as the default. Dr. Jessie Sanders, an aquatic veterinarian, applies that window to all new additions, including invertebrates and plants. Bulk Reef Supply gives the same 4–6 week range for isolating and observing new fish.</p>
    <p>Treat that as a floor when ich is involved. The University of Florida advises at least 3–6 weeks at 24–27°C (75–81°F) for <em>Cryptocaryon</em>, and says 7–11 weeks may be needed because the off-fish stage is so unpredictable. If spots appear, restart the clock from the end of treatment rather than from the day the fish arrived.</p>

    <h2 id="setup">Quarantine Tank Setup for Marine Fish</h2>
    <p>A quarantine tank should be plain, stable and easy to clean. Size it to the fish, not to the space you have left: Bulk Reef Supply suggests a 20-gallon, 24-inch tank for most fish up to 4 inches and a 40-gallon breeder or similar 36-inch tank for larger ones. Long-bodied swimmers such as tangs will need the bigger end of that range.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Item</th><th>What to use</th><th>Why it matters</th></tr>
      <tr><td>Bottom</td><td>Bare glass</td><td>Some parasites have a stage that develops on the substrate, and a bare floor is easier to siphon.</td></tr>
      <tr><td>Filter</td><td>Hang-on or internal, with mature media</td><td>Uncycled media means ammonia can become the problem you are treating.</td></tr>
      <tr><td>Oxygen</td><td>Air pump and stone</td><td>Parasites can make breathing harder, and some medications can lower oxygen.</td></tr>
      <tr><td>Heater and thermometer</td><td>Sized for the tank</td><td>Temperature should hold steady. Use the <a href="/tools/aquarium-heater-calculator/">heater calculator</a> to size it.</td></tr>
      <tr><td>Hides</td><td>PVC pipe, 2–4 inches wide</td><td>A hiding place lowers stress and can be disinfected between fish.</td></tr>
      <tr><td>Lid and light</td><td>Tight lid, low-output light</td><td>New fish jump. A dim tank lets them settle while you can still see them.</td></tr>
      <tr><td>Test kits</td><td>Ammonia, nitrite, nitrate, refractometer, plus a copper test if you dose copper</td><td>You can't manage what you aren't measuring. See the <a href="/guides/reef-tank-salinity/">salinity guide</a> for calibration.</td></tr>
    </table></div>
    <p>Keep biosecurity strict. Dr. Sanders recommends placing the tank at least 3 feet from the display, keeping separate labeled nets, siphons and scrubbers for each system, and sterilizing any media before it goes back to the main tank.</p>

{fig("saltwater-fish-quarantine-tank-setup", "Saltwater fish quarantine tank setup with bare bottom, filter, heater, PVC hide and air stone", "A simple saltwater fish quarantine setup. Keep it plain so it stays easy to clean and observe.")}

    <h2 id="plan">A Week-by-Week Quarantine Plan</h2>
    <p>This schedule is our editorial summary of the sources below, not a veterinary protocol. Adjust it with your vet if the fish is valuable or already looks unwell.</p>
    <ol>
      <li><strong>Arrival day:</strong> match temperature and salinity slowly, net the fish across and discard the store water. Keep the lights low.</li>
      <li><strong>Week 1:</strong> offer small meals and note what the fish eats. Check it closely every day, and test ammonia and nitrite often, since a new tank with a stressed fish can swing quickly.</li>
      <li><strong>Weeks 2–4:</strong> keep watching for spots, cloudy eyes, rubbing, fast breathing or hanging at the surface. Do water changes based on your test results.</li>
      <li><strong>Weeks 4–6:</strong> continue observing. A fish that is eating, breathing normally and showing no signs by the end is a much safer addition.</li>
      <li><strong>Moving day:</strong> acclimate to the display, and don't pour quarantine water into it. Sterilize or dry out the quarantine gear before the next fish.</li>
    </ol>

{fig("saltwater-fish-quarantine-timeline", "Saltwater fish quarantine timeline from arrival to moving day over 4 to 6 weeks", "Our editorial summary of a 4–6 week plan. Extend it if the fish needs treatment.")}

{app_cta("guide-saltwater-quarantine")}

    <h2 id="treat">Should You Treat Every New Fish in Quarantine?</h2>
    <p>Keepers disagree on this, so it helps to know both positions. Dr. Sanders advises <strong>no prophylactic treatments</strong>: dosing antibiotics or cure-alls without signs of disease encourages resistance. Many reef keepers still run copper or tank transfers on every new fish, because marine ich can be hidden in the gills and the cost of letting it into a reef is high.</p>
    <p>Our default is to observe first and treat for a specific reason, with a fish health specialist involved where you can get one. If you do choose to treat, follow a defined protocol such as those in the <a href="/guides/saltwater-ich-treatment/">saltwater ich treatment guide</a>. Never guess at a copper dose.</p>

    <h2 id="signs">Warning Signs During Quarantine</h2>
    <ul>
      <li><strong>White spots or nodules</strong> on the skin or fins suggest marine ich, though pale fish can hide them.</li>
      <li><strong>Fast breathing, flashing or hanging at the surface</strong> can mean a gill infection even with no visible spots.</li>
      <li><strong>Ragged fins, cloudy eyes, extra mucus or a thin body</strong> are also listed as signs of <em>Cryptocaryon</em>, but other diseases cause them as well.</li>
      <li><strong>Refusing food for days</strong> needs a water test first, then a closer look at the fish.</li>
    </ul>
    <p>UF/IFAS notes that white spots aren't enough for a diagnosis: confirming ich takes a microscope, and other parasites look similar. If you can reach an aquatic vet, this is the moment to call.</p>""",
    "faq_h2": "Saltwater Fish Quarantine FAQ",
    "faq": [
        ("How long should you quarantine saltwater fish?", "Plan on 4 to 6 weeks. If marine ich appears, count again from the end of treatment. UF/IFAS advises at least 3 to 6 weeks for Cryptocaryon and says 7 to 11 weeks may be needed."),
        ("Does a quarantine tank need to be cycled?", "Yes. Use mature filter media from an established system, or keep media running in a sump or display ahead of time. Uncycled media makes ammonia a risk. Sterilize that media before it returns to your main tank."),
        ("Can I skip quarantine if the store treated the fish?", "It's a risk. You can't confirm what the fish was treated with or whether the course was complete, and fish that survive ich can carry it. Isolating them yourself is the only check you control."),
        ("Do corals and invertebrates need quarantine too?", "Dr. Sanders applies the 4 to 6 week guideline to all new additions, including invertebrates and plants. Never put copper in a tank that holds them, because they are sensitive to many ich medications."),
        ("Can I quarantine several new fish together?", "You can, but a problem in one fish then affects them all, and the clock restarts for the whole group if you add another fish. Add new fish together rather than in stages."),
    ],
    "method_h2": "How We Checked This Saltwater Quarantine Guide",
    "method": "FishCare AI did not run its own quarantine trials. We compared guidance from an aquatic veterinarian, the University of Florida's extension fact sheet and a large reef retailer, and we say where keepers disagree. This guide doesn't replace a diagnosis from an aquatic veterinarian.",
    "refs": [FISHVET, FA164, BRS_QT, BRS_ICH],
    "related": [("/guides/saltwater-ich-treatment/", "Saltwater Ich Treatment"), ("/guides/reef-tank-salinity/", "Reef Tank Salinity"), ("/guides/tang-fish-care/diseases/", "Tang Fish Diseases"), ("/tools/water-parameter-checker/", "Water Parameter Checker")],
})

PAGES.append({
    "kind": "guide", "path": "/guides/saltwater-ich-treatment/", "image": "blue-tang-wikimedia-real.jpg",
    "title": "Saltwater Ich Treatment: Copper, Hyposalinity, Tank Transfer",
    "description": "Saltwater ich treatment compared: copper, hyposalinity, tank transfer and chloroquine, with doses from UF/IFAS, and why a reef needs a fallow period.",
    "h1": "Saltwater Ich Treatment: What Works and How Long It Takes",
    "crumb": "Saltwater Ich Treatment", "tag": "🩺 Saltwater Health",
    "meta": "🐟 Move fish to a bare tank &nbsp;|&nbsp; 🧪 Copper 0.15–0.20 mg/L &nbsp;|&nbsp; ⏳ Treat at least 3–6 weeks",
    "body": f"""    <p><strong>Saltwater ich treatment</strong> works best in a separate bare tank, because the options that clear marine ich aren't safe or practical in a reef. University of Florida guidance lists copper, hyposalinity and chloroquine as the standard baths, with copper considered by many the most effective. Plan on a minimum of <strong>3 to 6 weeks</strong>. Marine ich (<em>Cryptocaryon irritans</em>) is a parasite, and most of its life happens where no medicine can reach it.</p>

    <div class="callout callout-warn"><strong>Before you dose anything:</strong> move fish out of any tank holding corals, snails, shrimp or crabs. Check that the drug is legal where you live, and read the label. If you can, have an aquatic vet or fish health specialist confirm the diagnosis.</div>

{photo("blue-tang-wikimedia-real.jpg", "Blue tang, a marine fish that may need saltwater ich treatment", "Tangs are often among the first fish in a tank to show marine ich.")}

    <h2 id="signs">How to Recognize Marine Ich</h2>
    <p>Marine ich usually shows as small white spots, nodules or patches on the fins, skin or gills. Fish may also scratch against rock, breathe fast, hang at the surface or on the bottom, or turn lethargic. Ragged fins, cloudy eyes, extra mucus and weight loss are also listed.</p>
    <p>Spots alone don't settle it, and a lack of spots doesn't rule it out. Pale fish can hide them, and an infection limited to the gills may show none. UF/IFAS says confirming it takes a microscope, and that inexperienced keepers can mistake it for other ciliates such as <em>Uronema</em> or <em>Brooklynella</em>.</p>

    <h2 id="life-cycle">Why the Marine Ich Life Cycle Makes Treatment Slow</h2>
    <p>Spots that disappear haven't been cured. The parasite has simply dropped off the fish to reproduce, and only the free-swimming stage is really exposed to treatment. That is why every option below runs for weeks.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Stage</th><th>Where it is</th><th>Timing</th><th>Can treatment reach it?</th></tr>
      <tr><td>Trophont</td><td>Under the fish's skin</td><td>Feeds about 3–7 days</td><td>Relatively protected</td></tr>
      <tr><td>Protomont</td><td>Moving onto a surface</td><td>About 2–18 hours</td><td>Possibly, for a short time</td></tr>
      <tr><td>Tomont</td><td>Hard cyst on surfaces, producing about 100–1,000 tomites</td><td>Most release in 4–8 days; reported range 3–72 days</td><td>Well protected</td></tr>
      <tr><td>Theront</td><td>Swimming, looking for a fish</td><td>Infectivity falls sharply after 6–8 hours</td><td>Yes, the main target</td></tr>
    </table></div>
{fig("saltwater-ich-treatment-life-cycle", "Marine ich life cycle for saltwater ich treatment, from trophont to protomont, tomont and theront", "Most treatments target the free-swimming theront. Timing varies by strain, temperature and fish species.")}

    <p>A full cycle averages 1–2 weeks but ranges from 6 days to 11 weeks. Fish that survive can resist reinfection for up to about 6 months while still carrying the parasite, so a calm tank doesn't prove the parasite is gone.</p>

{fig("saltwater-ich-treatment-timing", "Saltwater ich treatment timing chart comparing parasite stages with the copper treatment minimum", "Why a short course isn't enough: the off-fish stage can outlast it. Source: UF/IFAS FA164.")}

    <h2 id="options">Saltwater Ich Treatment Options Compared</h2>
    <p>The figures below come from the UF/IFAS fact sheet. Commercial products vary, so follow the label for the product you actually bought.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Option</th><th>Protocol</th><th>Limits</th></tr>
      <tr><td><strong>Copper sulfate</strong></td><td>0.15–0.20 mg/L free copper, reached gradually over 2–3 days. Test at least twice a day. Treat at least 3–6 weeks.</td><td>Toxic to invertebrates. Levels fluctuate, so a good test kit is essential.</td></tr>
      <tr><td><strong>Chelated copper</strong></td><td>Follow the manufacturer's dose and test method.</td><td>Safety and effectiveness are more variable than copper sulfate.</td></tr>
      <tr><td><strong>Hyposalinity</strong></td><td>Lower salinity by 5–10 g/L per day to 15 g/L, then hold 21–30 days.</td><td>Some strains tolerate low salinity, and many marine fish tolerate it poorly.</td></tr>
      <tr><td><strong>Tank transfer</strong></td><td>Move fish to a clean, bare tank every 3 days, 3–5 times depending on temperature. Clean, disinfect and dry tanks between moves.</td><td>Not practical for large groups, and hard on weak fish.</td></tr>
      <tr><td><strong>Chloroquine diphosphate</strong></td><td>10 mg/L as a prolonged bath for 2–3 weeks or more.</td><td>Availability and legal use vary. Work with a vet.</td></tr>
    </table></div>
    <p>A salinity of 15 g/L is roughly specific gravity 1.011. Measure it with a calibrated instrument, as explained in the <a href="/guides/reef-tank-salinity/">reef tank salinity guide</a>, because a small reading error matters more at that level.</p>

    <h2 id="not-enough">Saltwater Ich Treatments That Fall Short</h2>
    <ul>
      <li><strong>Freshwater dips:</strong> up to 18 hours in fresh water did not seem to affect trophonts in one study, so a short dip won't cure the fish.</li>
      <li><strong>UV sterilizers:</strong> they only reach theronts passing through the unit, and required doses for marine ich are anecdotal or extrapolated. Cysts on the rock stay untouched.</li>
      <li><strong>"Reef-safe" additives:</strong> they aren't among the standard treatments in the UF/IFAS list. Don't rely on one to clear an outbreak in a display, even if the spots fade for a while, because fading is normal in the life cycle.</li>
    </ul>

{app_cta("guide-saltwater-ich")}

    <h2 id="reef">How to Clear Marine Ich From a Reef Tank</h2>
    <p>Corals and invertebrates can't catch ich, but they are highly sensitive to many of the medications, so the fish have to leave. Treating the fish alone isn't enough; the display has to stay without fish long enough for the parasite to die out.</p>
    <ol>
      <li><strong>Move every fish</strong> to a bare treatment tank, including those that look healthy.</li>
      <li><strong>Treat for the full course,</strong> then keep the fish isolated while the display sits empty.</li>
      <li><strong>Leave the display fishless.</strong> Bulk Reef Supply gives roughly 4 weeks, but theronts have emerged as late as 72 days after a tomont formed. Many reef keepers wait about 76 days to cover that. If you can, use the longer period.</li>
      <li><strong>Quarantine everything new</strong> afterwards, using the <a href="/guides/saltwater-fish-quarantine/">saltwater fish quarantine plan</a>.</li>
    </ol>
    <p>Tangs tend to be among the first fish to show it. See the <a href="/guides/tang-fish-care/diseases/">tang fish diseases guide</a> for how ich compares with velvet and black ich.</p>""",
    "faq_h2": "Saltwater Ich Treatment FAQ",
    "faq": [
        ("What is the best saltwater ich treatment?", "Many specialists consider copper the most effective, used in a bare tank at 0.15 to 0.20 mg/L free copper for at least 3 to 6 weeks. The right choice still depends on the fish species, your equipment and what is legal where you live."),
        ("Can you treat marine ich in a reef tank?", "Not with copper. Corals and invertebrates are highly sensitive to many ich medications. Move the fish to a treatment tank and leave the display without fish."),
        ("How long does marine ich live without a fish?", "Theronts lose most of their infectivity within 6 to 8 hours, but cysts can release new theronts for much longer. Release has been reported as late as 72 days after a tomont formed."),
        ("Why did the white spots go away and come back?", "The feeding stage drops off the fish after about 3 to 7 days to reproduce on surfaces. New infective stages then return, often in greater numbers."),
        ("Is marine ich the same as freshwater ich?", "No. They look alike and behave similarly, but UF/IFAS says the two parasites are only distantly related and differ in salinity tolerance and life cycle length."),
    ],
    "method_h2": "How We Checked This Saltwater Ich Treatment Guide",
    "method": "The doses and timings here come from University of Florida extension publication FA164, with reef-keeping context from Bulk Reef Supply. FishCare AI did not test these treatments, and this page isn't veterinary advice. Medications can harm or kill fish if dosed incorrectly, so confirm the plan with a fish health specialist where possible.",
    "refs": [FA164, BRS_ICH, FISHVET],
    "related": [("/guides/saltwater-fish-quarantine/", "Saltwater Fish Quarantine"), ("/guides/reef-tank-salinity/", "Reef Tank Salinity"), ("/guides/tang-fish-care/diseases/", "Tang Fish Diseases"), ("/guides/clownfish-care-guide/", "Clownfish Care Guide")],
})

SALINITY_SCRIPT = """(function(){
  var K=0.000754;
  var ppt=document.getElementById('sal-ppt'),sg=document.getElementById('sal-sg'),out=document.getElementById('sal-out');
  function note(p){
    if(p<30)return 'Below the normal range for a reef. Treatment-level salinity is only for fish in a separate tank.';
    if(p<32)return 'Below the 32\\u201336 ppt range suggested for reefs. Raise it slowly.';
    if(p<=36)return p>=34.5&&p<=35.5?'At or close to natural seawater, the usual reef target.':'Inside the 32\\u201336 ppt reef range. Aim to keep it steady.';
    return 'Above the 32\\u201336 ppt range suggested for reefs. Check your instrument, then lower it slowly.';
  }
  function show(p){out.innerHTML='<div class="calc-big">'+p.toFixed(1)+' ppt = SG '+(1+p*K).toFixed(4)+'</div><div>'+note(p)+'</div>';}
  ppt.addEventListener('input',function(){var p=parseFloat(ppt.value);if(isNaN(p)||p<0||p>45){out.innerHTML='<span class="calc-err">Enter a salinity from 0 to 45 ppt.</span>';return;}sg.value=(1+p*K).toFixed(4);show(p);});
  sg.addEventListener('input',function(){var s=parseFloat(sg.value);if(isNaN(s)||s<1||s>1.034){out.innerHTML='<span class="calc-err">Enter a specific gravity from 1.000 to 1.034.</span>';return;}var p=(s-1)/K;ppt.value=p.toFixed(1);show(p);});
  show(35);
})();"""

PAGES.append({
    "kind": "guide", "path": "/guides/reef-tank-salinity/", "image": "ocellaris-clownfish-wikimedia-real.jpg",
    "title": "Reef Tank Salinity: Ideal Level, SG to PPT Chart",
    "description": "Reef tank salinity explained: why 35 ppt is SG 1.0264 and not 1.025, a conversion chart and calculator, how to calibrate, and how to raise or lower salinity.",
    "h1": "Reef Tank Salinity: Ideal Level, SG to PPT Chart and Converter",
    "crumb": "Reef Tank Salinity", "tag": "🌊 Saltwater Basics",
    "meta": "🎯 Target 35 ppt / SG 1.0264 &nbsp;|&nbsp; 📏 Reef range 32–36 ppt &nbsp;|&nbsp; 💧 Top off with fresh water",
    "script": SALINITY_SCRIPT,
    "body": """    <p>The usual <strong>reef tank salinity</strong> target is <strong>35 ppt, a specific gravity of 1.0264</strong> at 25°C, which matches natural seawater. Chemist Randy Holmes-Farley suggests 32–36 ppt (SG 1.024–1.027) as an acceptable reef range. Note that SG 1.025, often quoted as "35 ppt," works out closer to 33 ppt. Stability matters too, so correct any drift slowly.</p>

    <div class="calc-box">
      <div class="calc-grid">
        <div><label for="sal-ppt">Salinity (ppt)</label><input id="sal-ppt" type="number" inputmode="decimal" step="0.1" value="35"></div>
        <div><label for="sal-sg">Specific gravity</label><input id="sal-sg" type="number" inputmode="decimal" step="0.0001" value="1.0264"></div>
      </div>
      <div class="calc-out" id="sal-out" aria-live="polite"></div>
      <p class="calc-note">Based on a straight-line fit to the 30–39 ppt table below, at 25°C. Treat values well below 30 ppt as approximate.</p>
    </div>

[[PHOTO_SAL]]

    <h2 id="chart">Reef Tank Salinity Chart: PPT to Specific Gravity</h2>
    <p>These values are from Holmes-Farley's table at 25°C. Use them to check a reading against the range you are aiming for.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Salinity (ppt)</th><th>Specific gravity</th><th>What it means</th></tr>
      <tr><td>30</td><td>1.0226</td><td>Low for a reef</td></tr>
      <tr><td>31</td><td>1.0233</td><td>Low for a reef</td></tr>
      <tr><td>32</td><td>1.0241</td><td>Low end of the suggested range</td></tr>
      <tr><td>33</td><td>1.0249</td><td>In range; about where SG 1.025 sits</td></tr>
      <tr><td>34</td><td>1.0256</td><td>In range</td></tr>
      <tr><td><strong>35</strong></td><td><strong>1.0264</strong></td><td><strong>Natural seawater, the usual target</strong></td></tr>
      <tr><td>36</td><td>1.0271</td><td>High end of the suggested range</td></tr>
      <tr><td>37</td><td>1.0279</td><td>High for a reef</td></tr>
    </table></div>
[[FIG_SCALE]]

    <p>Fish-only tanks are often run lower. Bulk Reef Supply lists SG 1.017–1.023 for fish with live rock and 1.023–1.026 for reefs. Keep corals and invertebrates close to natural seawater.</p>

    <h2 id="measure">How to Measure Reef Tank Salinity Accurately</h2>
    <p>A calibrated reading is what counts, and each tool fails in its own way.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Tool</th><th>Good to know</th></tr>
      <tr><td><strong>Refractometer</strong></td><td>Calibrate with a 35 ppt seawater standard. A salt (NaCl) refractometer reads seawater about 1.7 ppt high, so it can show 35 ppt when the tank is really 33.3 ppt.</td></tr>
      <tr><td><strong>Conductivity meter</strong></td><td>Natural seawater is about 53 mS/cm. Calibrate with a 35 ppt or 53 mS/cm standard.</td></tr>
      <tr><td><strong>Swing-arm hydrometer</strong></td><td>Can't be calibrated, and must read water at its stated temperature.</td></tr>
    </table></div>
    <p>Some manufacturers tell you to zero a refractometer on fresh water. Holmes-Farley recommends a seawater standard instead, because it checks the instrument right where you read it. Bulk Reef Supply suggests calibrating before every use and checking salinity 1–3 times a week, plus before and after water changes.</p>

    <h2 id="adjust">How to Raise or Lower Salinity Safely</h2>
    <p>None of the sources we reviewed gives a fixed safe rate for a reef, so make small changes and retest. Bulk Reef Supply simply advises gradual change.</p>
    <ul>
      <li><strong>To raise it:</strong> mix salt into RO/DI water in a separate container, then swap it in during small water changes. Never add dry salt to the tank.</li>
      <li><strong>To lower it:</strong> replace a little tank water with RO/DI, then retest once the water has mixed.</li>
      <li><strong>If it keeps rising:</strong> that's usually evaporation. Fresh water leaves and salt stays, so top off with RO/DI only. An auto top-off unit can handle this for you.</li>
    </ul>
    <p>Fish in a treatment tank are a different case. The hyposalinity protocol in the <a href="/guides/saltwater-ich-treatment/">saltwater ich treatment guide</a> goes far below these ranges and isn't for tanks with corals or invertebrates.</p>

[[FIG_EVAP]]

    <h2 id="mix">How Much Salt to Mix for Reef Water</h2>
    <p>Follow the label and confirm with your refractometer, since brands differ. As one example, Bulk Reef Supply cites Aquaforest at 405 grams per 2.7 gallons for 35 ppt, or 150 grams per gallon. Add salt slowly to water heated to about 75–78°F, let it mix fully, then measure before using it.</p>""",
    "faq_h2": "Reef Tank Salinity FAQ",
    "faq": [
        ("What should salinity be in a reef tank?", "Aim for 35 ppt, which is specific gravity 1.0264 at 25°C. A range of 32 to 36 ppt, or SG 1.024 to 1.027, is the range Randy Holmes-Farley suggests for reefs."),
        ("Is 1.025 specific gravity good for a reef tank?", "Yes, it falls inside the suggested range, but it is closer to 33 ppt than 35 ppt. If you want to match natural seawater, aim for about 1.0264."),
        ("Why is my salinity going up?", "Evaporation is the most common cause. Fresh water leaves the tank while salt stays behind. Top off with RO/DI water, not salt water."),
        ("How often should I check salinity?", "Bulk Reef Supply suggests 1 to 3 times a week and before and after water changes. An auto top-off doesn't remove the need to check."),
        ("Does temperature affect specific gravity?", "Yes. Specific gravity readings depend on temperature, which is why this table is stated at 25°C and why swing-arm hydrometers must read water at their stated temperature."),
    ],
    "method_h2": "How We Checked This Reef Salinity Guide",
    "method": "The conversion values come from Randy Holmes-Farley's published table. The converter uses a straight-line fit to that table, so it may differ from it in the fourth decimal. Practical ranges come from Bulk Reef Supply. FishCare AI did not measure instruments for this page.",
    "refs": [RHF, BRS_SAL, BRS_SALT],
    "related": [("/guides/saltwater-ich-treatment/", "Saltwater Ich Treatment"), ("/guides/saltwater-fish-quarantine/", "Saltwater Fish Quarantine"), ("/tools/water-parameter-checker/", "Water Parameter Checker"), ("/guides/clownfish-care-guide/", "Clownfish Care Guide")],
})

HEATER_SCRIPT = """(function(){
  var $=function(i){return document.getElementById(i)};
  var SIZES=[25,50,75,100,150,200,250,300,400,500,600,800];
  function up(w){for(var i=0;i<SIZES.length;i++)if(SIZES[i]>=w)return SIZES[i];return null;}
  function perGal(g){return g<=55?5:g>=60?3:5-(g-55)*0.4;}
  function run(){
    var c=$('h-unit').value==='c',l=$('h-vol-unit').value==='l',v=parseFloat($('h-vol').value),room=parseFloat($('h-room').value),t=parseFloat($('h-target').value),o=$('h-out');
    if(isNaN(v)||v<=0||isNaN(room)||isNaN(t)){o.innerHTML='<span class="calc-err">Enter tank volume, room temperature and target temperature.</span>';return;}
    var g=l?v/3.785:v;
    if(g>1000){o.innerHTML='<span class="calc-err">This estimate is for aquariums up to 1,000 gallons.</span>';return;}
    var rise=(t-room)*(c?1.8:1);
    if(rise<=0){o.innerHTML='<div class="calc-big">No heater power needed for that room</div><div>The room is already at or above your target. Check the coldest night of the year before skipping a heater, because the room may not stay this warm.</div>';return;}
    var w=g*perGal(g)*rise/10*($('h-lid').value==='open'?1.2:1);
    var n=parseInt($('h-count').value,10),each=w/n,sz=up(each),extra=[];
    if(g>=75&&n===1)extra.push('Consider two heaters on a tank this size. They add up to the same total and can give some backup, but a stuck-on heater is still a risk.');
    if(rise>=20)extra.push('A rise of this size is demanding. Check the heater maker\\u2019s chart for this rise, and insulate or warm the room if you can.');
    if(sz===null)extra.push('That is more than a single common heater size. Split the load across more heaters.');
    extra.push('Use a separate thermometer, and consider a temperature controller as a cut-off if a heater sticks on.');
    o.innerHTML='<div class="calc-big">About '+Math.round(w)+' W total</div><div>'+(sz?n+' \\u00d7 '+sz+' W heater'+(n>1?'s are':' is')+' the nearest common size.':'')+' Temperature rise: '+Math.round(rise)+'\\u00b0F ('+(rise/1.8).toFixed(1)+'\\u00b0C).</div><ul>'+extra.map(function(e){return '<li>'+e+'</li>'}).join('')+'</ul>';
    if(typeof window.gtag==='function')window.gtag('event','tool_calculate',{tool:'aquarium-heater-calculator'});
  }
  $('h-go').addEventListener('click',run);
  $('h-unit').addEventListener('change',function(){var c=this.value==='c';$('h-room').value=c?20:68;$('h-target').value=c?25.5:78;});
  Array.prototype.forEach.call(document.querySelectorAll('[data-g]'),function(b){b.addEventListener('click',function(){$('h-vol-unit').value='gal';$('h-vol').value=b.getAttribute('data-g');run();});});
})();"""

PAGES.append({
    "kind": "tool", "path": "/tools/aquarium-heater-calculator/", "image": "clownfish-wikimedia-real.jpg",
    "title": "Aquarium Heater Calculator: What Size Heater Do You Need?",
    "description": "Free aquarium heater calculator. Enter tank size, room temperature and target temperature to estimate heater wattage, with a size chart and safety tips.",
    "h1": "Aquarium Heater Calculator: What Size Heater Do You Need?",
    "crumb": "Aquarium Heater Calculator", "tag": "🌡️ Free Tool",
    "meta": "📐 Based on temperature rise &nbsp;|&nbsp; 🐠 Freshwater or saltwater &nbsp;|&nbsp; ⚠️ Confirm with the heater's own chart",
    "script": HEATER_SCRIPT,
    "body": """    <div class="calc-box">
      <div class="presets" aria-label="Common tank sizes"><button type="button" data-g="10">10 gal</button><button type="button" data-g="20">20 gal</button><button type="button" data-g="29">29 gal</button><button type="button" data-g="40">40 gal</button><button type="button" data-g="55">55 gal</button><button type="button" data-g="75">75 gal</button><button type="button" data-g="125">125 gal</button></div>
      <div class="calc-grid">
        <div><label for="h-vol">Tank volume</label><input id="h-vol" type="number" inputmode="decimal" min="1" value="20"></div>
        <div><label for="h-vol-unit">Volume unit</label><select id="h-vol-unit"><option value="gal">US gallons</option><option value="l">Litres</option></select></div>
        <div><label for="h-room">Coldest normal room temperature</label><input id="h-room" type="number" inputmode="decimal" value="68"></div>
        <div><label for="h-target">Target tank temperature</label><input id="h-target" type="number" inputmode="decimal" value="78"></div>
        <div><label for="h-unit">Temperature unit</label><select id="h-unit"><option value="f">°F</option><option value="c">°C</option></select></div>
        <div><label for="h-lid">Lid</label><select id="h-lid"><option value="closed">Closed lid</option><option value="open">Open top</option></select></div>
        <div><label for="h-count">Number of heaters</label><select id="h-count"><option value="1">1 heater</option><option value="2">2 heaters</option></select></div>
      </div>
      <button class="calc-btn" id="h-go" type="button">Calculate Heater Size</button>
      <div class="calc-out" id="h-out" aria-live="polite">Your estimate will appear here.</div>
      <p class="calc-note">This is a planning estimate. Check the chart for the exact heater you plan to buy.</p>
    </div>

    <p>This <strong>aquarium heater calculator</strong> estimates fish tank heater wattage from two numbers: water volume and how far the tank must sit above the coldest normal room temperature. A common rule of thumb is about 5 watts per gallon, but a single number hides that difference. To heat a tank to 78°F, a room that drops to 60°F needs far more power than one at 68°F.</p>

    <h2 id="chart">Aquarium Heater Size Chart by Tank and Temperature Rise</h2>
    <p>These watt figures come from the same estimate as the calculator, for a closed lid. Choose the nearest heater size at or above the number, then compare it with the maker's chart.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Tank</th><th>+5°F rise</th><th>+10°F rise</th><th>+15°F rise</th><th>+20°F rise</th></tr>
      <tr><td>10 gal</td><td>25 W</td><td>50 W</td><td>75 W</td><td>100 W</td></tr>
      <tr><td>20 gal</td><td>50 W</td><td>100 W</td><td>150 W</td><td>200 W</td></tr>
      <tr><td>29 gal</td><td>73 W</td><td>145 W</td><td>218 W</td><td>290 W</td></tr>
      <tr><td>40 gal</td><td>100 W</td><td>200 W</td><td>300 W</td><td>400 W</td></tr>
      <tr><td>55 gal</td><td>138 W</td><td>275 W</td><td>413 W</td><td>550 W</td></tr>
      <tr><td>75 gal</td><td>113 W</td><td>225 W</td><td>338 W</td><td>450 W</td></tr>
      <tr><td>125 gal</td><td>188 W</td><td>375 W</td><td>563 W</td><td>750 W</td></tr>
    </table></div>
    <p>The dip after 55 gallons is intentional. Larger tanks lose heat more slowly relative to their volume, so the estimate tapers. Near that crossover, lean toward the higher figure if your room runs cold.</p>

[[FIG_HBARS]]

    <h2 id="how">How the Fish Tank Heater Calculator Works</h2>
    <ol>
      <li><strong>Temperature rise:</strong> target temperature minus the coldest normal room temperature. Measure the room overnight rather than guessing.</li>
      <li><strong>Base watts:</strong> 0.5 W per gallon for each °F of rise up to 55 gallons, which equals the 5 W per gallon rule at a 10°F rise. Above 60 gallons it uses 0.3 W, and it blends the two in between.</li>
      <li><strong>Open top:</strong> adds 20% for extra heat loss. This percentage and the taper are our planning assumptions, not measured figures.</li>
      <li><strong>Heater count:</strong> divides the total, then rounds up to a common heater size.</li>
    </ol>

[[FIG_HSTEP]]

    <h2 id="one-or-two">One Aquarium Heater or Two?</h2>
    <p>Two heaters can spread heat across a long tank and give some backup if one stops working. Add their wattages to check total capacity. They don't remove the risk of a heater stuck on, so a separate thermometer helps, and a temperature controller gives you a cut-off that works independently of the heater's own thermostat.</p>
    <p>Avoid going far above your estimate. A large heater in a small tank can warm it quickly if it fails on. For the rest of your equipment, use the <a href="/tools/aquarium-equipment-calculator/">aquarium equipment calculator</a>.</p>""",
    "faq_h2": "Aquarium Heater Calculator FAQ",
    "faq": [
        ("What size heater do I need for a 20 gallon tank?", "About 100 W for a 10°F rise with a closed lid. If the room is only 5°F below your target, 50 W may be enough; a 20°F rise calls for about 200 W."),
        ("What size heater do I need for a 55 gallon tank?", "This estimate gives about 275 W for a 10°F rise, so a 300 W heater or two 150 W heaters would be the nearest common choices. Check the maker's chart for your room temperature."),
        ("How many watts per gallon does an aquarium heater need?", "About 5 W per gallon is the common rule of thumb, and it corresponds to about a 10°F rise. Rooms that are colder need more, while larger tanks usually need fewer watts per gallon."),
        ("Do saltwater tanks need a different heater size?", "This estimate treats saltwater and freshwater the same. What usually differs is the heater's material and rating, so confirm that the heater you buy is rated for saltwater."),
        ("Can an aquarium heater be too big?", "Yes. A large heater that sticks on can overheat a small tank quickly. Stay close to the size you need, and use a thermometer or controller as a check."),
    ],
    "method_h2": "How Accurate Is This Heater Estimate?",
    "method": "It's a planning estimate, not a measured heat-loss model. Room drafts, tank shape, glass thickness, lids, pumps and lights all change the real figure. We started from the temperature-rise approach and the common 5 W per gallon rule cited below, then added the taper and open-top adjustment as stated assumptions. FishCare AI didn't bench-test heaters for this tool.",
    "refs": [BYA, FISHLAB],
    "related": [("/tools/aquarium-equipment-calculator/", "Aquarium Equipment Calculator"), ("/tools/aquarium-weight-calculator/", "Aquarium Weight Calculator"), ("/tools/aquarium-size-calculator/", "Aquarium Size Calculator"), ("/guides/saltwater-fish-quarantine/", "Saltwater Fish Quarantine")],
})

WEIGHT_SCRIPT = """(function(){
  var $=function(i){return document.getElementById(i)};
  var T=[[2.5,3],[5,7],[10,11],[15,21],[20,25],[25,32],[29,40],[40,58],[55,78],[65,126],[75,140],[90,160],[125,206],[150,338],[180,430]];
  function glass(g){
    if(g<=T[0][0])return T[0][1]*g/T[0][0];
    for(var i=1;i<T.length;i++)if(g<=T[i][0]){var a=T[i-1],b=T[i];return a[1]+(b[1]-a[1])*(g-a[0])/(b[0]-a[0]);}
    return 430*g/180;
  }
  function n(id){var v=parseFloat($(id).value);return isNaN(v)||v<0?0:v;}
  function fmt(x){return Math.round(x).toLocaleString('en-US');}
  function run(){
    var o=$('w-out'),l=$('w-vol-unit').value==='l',v=parseFloat($('w-vol').value);
    if(isNaN(v)||v<=0){o.innerHTML='<span class="calc-err">Enter the tank volume.</span>';return;}
    var g=l?v/3.785:v;
    if(g>1000){o.innerHTML='<span class="calc-err">This estimate is for aquariums up to 1,000 gallons.</span>';return;}
    var per=$('w-water').value==='salt'?8.554:8.345;
    var sump=n('w-sump'),water=(g+sump)*per;
    var tank=glass(g)*($('w-mat').value==='acrylic'?0.5:1);
    var sub=n('w-sub'),rock=n('w-rock'),stand=n('w-stand'),total=water+tank+sub+rock+stand;
    var tip=g<=55?'Place it on a solid floor, ideally near a load-bearing wall, and check that the stand is rated for this weight.':'Tanks of 75 gallons and up deserve extra care. Run the tank across the floor joists, and ask a professional to check the floor, especially upstairs.';
    o.innerHTML='<div class="calc-big">About '+fmt(total)+' lb ('+fmt(total*0.4536)+' kg)</div><ul><li>Water: '+fmt(water)+' lb</li><li>Empty tank: '+fmt(tank)+' lb</li><li>Substrate and rock: '+fmt(sub+rock)+' lb</li><li>Stand: '+fmt(stand)+' lb</li></ul><p style="margin-top:10px">'+tip+'</p>';
    if(typeof window.gtag==='function')window.gtag('event','tool_calculate',{tool:'aquarium-weight-calculator'});
  }
  $('w-go').addEventListener('click',run);
  Array.prototype.forEach.call(document.querySelectorAll('[data-g]'),function(b){b.addEventListener('click',function(){$('w-vol-unit').value='gal';$('w-vol').value=b.getAttribute('data-g');$('w-sub').value=b.getAttribute('data-g');run();});});
})();"""

PAGES.append({
    "kind": "tool", "path": "/tools/aquarium-weight-calculator/", "image": "blue-tang-wikimedia-real.jpg",
    "title": "Aquarium Weight Calculator: How Much Does a Fish Tank Weigh?",
    "description": "Free aquarium weight calculator. Estimate filled fish tank weight with water, glass, sand, rock and stand, for fresh or salt water, plus a size chart.",
    "h1": "Aquarium Weight Calculator: How Much Does a Full Tank Weigh?",
    "crumb": "Aquarium Weight Calculator", "tag": "⚖️ Free Tool",
    "meta": "💧 Fresh 8.35 lb/gal, salt 8.55 lb/gal &nbsp;|&nbsp; 🪨 Add sand, rock and stand &nbsp;|&nbsp; 🏠 Floor tips included",
    "script": WEIGHT_SCRIPT,
    "body": """    <div class="calc-box">
      <div class="presets" aria-label="Common tank sizes"><button type="button" data-g="10">10 gal</button><button type="button" data-g="20">20 gal</button><button type="button" data-g="29">29 gal</button><button type="button" data-g="40">40 gal</button><button type="button" data-g="55">55 gal</button><button type="button" data-g="75">75 gal</button><button type="button" data-g="125">125 gal</button></div>
      <div class="calc-grid">
        <div><label for="w-vol">Tank volume</label><input id="w-vol" type="number" inputmode="decimal" min="1" value="55"></div>
        <div><label for="w-vol-unit">Volume unit</label><select id="w-vol-unit"><option value="gal">US gallons</option><option value="l">Litres</option></select></div>
        <div><label for="w-water">Water</label><select id="w-water"><option value="fresh">Freshwater</option><option value="salt">Saltwater</option></select></div>
        <div><label for="w-mat">Tank material</label><select id="w-mat"><option value="glass">Glass</option><option value="acrylic">Acrylic</option></select></div>
        <div><label for="w-sub">Substrate (lb)</label><input id="w-sub" type="number" inputmode="decimal" min="0" value="55"><p class="calc-note">Guide: about 1 lb per gallon, up to twice that for sand.</p></div>
        <div><label for="w-rock">Rock and decor (lb)</label><input id="w-rock" type="number" inputmode="decimal" min="0" value="0"></div>
        <div><label for="w-sump">Sump water (gallons)</label><input id="w-sump" type="number" inputmode="decimal" min="0" value="0"></div>
        <div><label for="w-stand">Stand (lb)</label><input id="w-stand" type="number" inputmode="decimal" min="0" value="0"></div>
      </div>
      <button class="calc-btn" id="w-go" type="button">Calculate Tank Weight</button>
      <div class="calc-out" id="w-out" aria-live="polite">Your estimate will appear here.</div>
    </div>

    <p>This <strong>aquarium weight calculator</strong> adds up water, tank, substrate, rock, sump and stand to estimate the total weight of a filled tank. As a quick check, freshwater weighs about 8.35 lb per gallon and saltwater about 8.55 lb. A complete setup comes out heavier than the water alone. Top Shelf Aquatics puts a typical 55-gallon setup at 600–700 lb, and says a filled reef runs closer to 10–11 lb per gallon.</p>

    <h2 id="chart">Aquarium Weight Chart by Tank Size</h2>
    <p>The figures below are published estimates for standard glass tanks, and real weights vary by maker and glass thickness. Water weight is calculated at 8.345 lb per gallon.</p>
    <div class="table-wrap"><table class="ptbl">
      <tr><th>Tank</th><th>Empty glass (lb)</th><th>Water only (lb)</th><th>Typical filled system (lb)</th></tr>
      <tr><td>10 gal</td><td>11</td><td>83</td><td>110–130</td></tr>
      <tr><td>20 gal</td><td>25</td><td>167</td><td>215–250</td></tr>
      <tr><td>29 gal</td><td>40</td><td>242</td><td>310–360</td></tr>
      <tr><td>40 gal breeder</td><td>58</td><td>334</td><td>430–500</td></tr>
      <tr><td>55 gal</td><td>78</td><td>459</td><td>600–700</td></tr>
      <tr><td>75 gal</td><td>140</td><td>626</td><td>850–1,000</td></tr>
      <tr><td>90 gal</td><td>160</td><td>751</td><td>1,000–1,200</td></tr>
      <tr><td>125 gal</td><td>206</td><td>1,043</td><td>1,400–1,650</td></tr>
      <tr><td>180 gal</td><td>430</td><td>1,502</td><td>2,000–2,300</td></tr>
    </table></div>

[[FIG_WBARS]]

    <h2 id="how">How the Aquarium Weight Calculator Works</h2>
    <ul>
      <li><strong>Water:</strong> volume plus any sump water, multiplied by 8.345 lb per gallon for fresh or 8.554 lb for salt. It assumes a completely full tank, which overstates water slightly and errs on the safe side.</li>
      <li><strong>Empty tank:</strong> interpolated from published weights for standard glass tanks. The acrylic option halves that figure. This is our rough assumption, because thick acrylic tanks vary widely, so use the maker's weight if you have it.</li>
      <li><strong>Everything else:</strong> the substrate, rock and stand weights you enter. Sand and gravel run about 85–105 lb per cubic foot.</li>
    </ul>

[[FIG_WCMP]]

    <h2 id="floor">Aquarium Weight and Floor Safety</h2>
    <p>This calculator can't tell you what your floor will hold, since that depends on the joists, span and condition of the building. Top Shelf Aquatics suggests that tanks up to about 55 gallons usually sit fine on a solid floor near a load-bearing wall, while 75 gallons and up should run across the joists, with a professional consulted when in doubt.</p>
    <ul>
      <li>Check that the stand is rated for your total and sits level.</li>
      <li>Remember the weight sits on a small footprint, so it concentrates the load.</li>
      <li>Take extra care upstairs, over a crawl space or on an old floor.</li>
      <li>Move a tank only when it's empty. Water and sand are what make it dangerous.</li>
    </ul>
    <p>When you are planning the whole setup, the <a href="/tools/aquarium-size-calculator/">aquarium size calculator</a> gives you the volume from the tank's dimensions.</p>""",
    "faq_h2": "Aquarium Weight FAQ",
    "faq": [
        ("How much does a 55 gallon fish tank weigh?", "About 459 lb of fresh water plus about 78 lb for the empty glass tank, or roughly 540 lb before substrate and decor. A complete system is commonly estimated at 600 to 700 lb."),
        ("How much does a 75 gallon fish tank weigh?", "About 626 lb of fresh water plus about 140 lb of glass, or roughly 770 lb. With substrate, decor and equipment, a common estimate is 850 to 1,000 lb."),
        ("Is saltwater heavier than freshwater?", "Yes, slightly. Saltwater is about 8.55 lb per gallon compared with 8.35 lb for fresh, but rock and sand are usually what make a reef noticeably heavier."),
        ("Can I put a 55 gallon tank on the second floor?", "Many people do, but it depends on the building. Place it near a load-bearing wall and across the joists, and ask a professional if you are unsure."),
        ("How much does a gallon of water weigh?", "About 8.35 lb for a US gallon of fresh water and about 8.55 lb for salt water."),
    ],
    "method_h2": "How Accurate Is This Aquarium Weight Estimate?",
    "method": "It's an estimate for planning, using published empty-tank weights, standard water weights and the numbers you enter. Published figures disagree, so we favor conservative totals and show the ranges. This tool isn't a structural assessment. FishCare AI didn't weigh tanks for this page.",
    "refs": [TANKARIUM, TOPSHELF],
    "related": [("/tools/aquarium-size-calculator/", "Aquarium Size Calculator"), ("/tools/aquarium-heater-calculator/", "Aquarium Heater Calculator"), ("/tools/aquarium-substrate-calculator/", "Aquarium Substrate Calculator"), ("/tools/aquarium-equipment-calculator/", "Aquarium Equipment Calculator")],
})

TOKENS = {
    "[[PHOTO_SAL]]": photo("ocellaris-clownfish-wikimedia-real.jpg", "Ocellaris clownfish in a reef tank with stable salinity", "Clownfish and other marine fish do best when salinity holds steady."),
    "[[FIG_SCALE]]": fig("reef-tank-salinity-scale", "Reef tank salinity scale showing the 32 to 36 ppt range, SG 1.025 and natural seawater at SG 1.0264", "SG 1.025 sits inside the reef range, but below natural seawater."),
    "[[FIG_EVAP]]": fig("reef-tank-salinity-evaporation", "Why reef tank salinity rises with evaporation and how to top off with RO/DI water", "Most slow salinity rises come from evaporation, not from the salt you added."),
    "[[FIG_HBARS]]": fig("aquarium-heater-calculator-watts", "Aquarium heater calculator chart of estimated watts by tank size at a 10°F rise", "The same figures as the +10°F column above."),
    "[[FIG_HSTEP]]": fig("aquarium-heater-calculator-example", "Aquarium heater calculator worked example for a 20 gallon tank", "A worked example using the calculator's defaults."),
    "[[FIG_WBARS]]": fig("aquarium-weight-calculator-by-size", "Aquarium weight calculator chart of water and empty glass weight by tank size", "Water makes up most of the weight at every size. Empty weights are published estimates."),
    "[[FIG_WCMP]]": fig("aquarium-weight-calculator-breakdown", "Aquarium weight calculator breakdown for 55 gallon freshwater and reef examples", "Illustrative amounts. Use the calculator with your own sand and rock weights."),
}
for p in PAGES:
    for k, v in TOKENS.items():
        p["body"] = p["body"].replace(k, v)
for p in PAGES:
    out = ROOT / p["path"].strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(p), encoding="utf-8")
    print(p["path"], len(p["title"]), len(p["description"]))
