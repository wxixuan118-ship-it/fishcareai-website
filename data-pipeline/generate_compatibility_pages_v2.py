"""Generate the v2 fish compatibility cluster.

The v1 generator remains the source of the visual pair-page template.  This
module expands its catalogue to 91 species, replaces the scoring engine,
creates a hub for every species, adds stocking/tank scenarios, and rebuilds
only the compatibility section of the root sitemap.

Run from any directory:
    python3 data-pipeline/generate_compatibility_pages_v2.py
"""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from itertools import combinations
from pathlib import Path

import generate_compatibility_pages as v1


ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = ROOT.parent / "data-pipeline" / "output" / "08_raw.json"
SITEMAP = ROOT / "sitemap.xml"
TODAY = "2026-08-18"

# The original 31 plus these 60 commercially common/search-worthy aquarium
# animals form the deliberately bounded v2 catalogue (91 total).
V2_ADDITIONS = (
    "black-neon-tetra", "lemon-tetra", "glowlight-tetra", "congo-tetra",
    "serpae-tetra", "diamond-tetra", "silver-dollar", "red-eye-tetra",
    "black-phantom-tetra", "x-ray-tetra", "electric-yellow-cichlid",
    "frontosa-cichlid", "peacock-cichlid", "jewel-cichlid", "severum-cichlid",
    "green-terror-cichlid", "texas-cichlid", "keyhole-cichlid", "bolivian-ram",
    "panda-cory", "peppered-cory", "sterbai-cory", "julii-cory",
    "clown-pleco", "zebra-pleco", "glass-catfish", "yoyo-loach",
    "zebra-loach", "dwarf-chain-loach", "hillstream-loach", "weather-loach",
    "three-spot-gourami", "moonlight-gourami", "sparkling-gourami",
    "pearl-danio", "giant-danio", "glowlight-danio",
    "black-ruby-barb", "rosy-barb", "denison-barb", "bosemans-rainbowfish",
    "neon-rainbowfish", "threadfin-rainbowfish", "black-ghost-knifefish",
    "clown-knifefish", "silver-arowana", "senegal-bichir", "african-butterfly-fish",
    "fire-eel", "blue-tang", "yellow-tang", "flame-angelfish",
    "coral-beauty", "percula-clownfish", "firefish-goby", "watchman-goby",
    "royal-gramma", "pajama-cardinalfish", "foxface-rabbitfish", "lionfish",
)

POPULARITY = {
    "betta-fish": 100, "goldfish": 96, "guppy": 94, "neon-tetra": 92,
    "angelfish": 90, "oscar": 88, "discus": 87, "molly": 84,
    "platy": 82, "corydoras": 81, "bristlenose-pleco": 80,
    "cherry-shrimp": 78, "clownfish": 78, "blue-tang": 76,
    "zebra-danio": 74, "cardinal-tetra": 72, "tiger-barb": 70,
}


def _number(value, default=2.0):
    match = re.search(r"\d+(?:\.\d+)?", str(value or ""))
    return float(match.group()) if match else default


def _temperament(record):
    text = " ".join(str(x) for x in record.get("behavior", {}).values()).lower()
    if any(word in text for word in ("high", "aggressive", "territorial")):
        return "aggressive"
    if any(word in text for word in ("semi", "moderate", "boisterous")):
        return "semi"
    return "peaceful"


def _zone(slug, record):
    text = (slug + " " + record.get("sections", {}).get("behavior_detail", "")).lower()
    if any(word in text for word in ("catfish", "cory", "loach", "pleco", "goby", "bottom")):
        return "bottom"
    if any(word in text for word in ("hatchet", "butterfly", "surface", "top")):
        return "top"
    return "mid"


def load_catalogue():
    raw = json.loads(RAW_DATA.read_text(encoding="utf-8"))
    missing = [slug for slug in V2_ADDITIONS if slug not in raw]
    if missing:
        raise RuntimeError(f"Missing v2 enrichment records: {', '.join(missing)}")

    for slug in V2_ADDITIONS:
        row = raw[slug]
        env, behavior = row["environment"], row["behavior"]
        size_cm = _number(row.get("physical", {}).get("size_cm"), 5)
        schooling = bool(behavior.get("schooling"))
        name = re.sub(r"\bFish\b", "Fish", slug.replace("-", " ").title())
        v1.SPECIES[slug] = {
            "name": name,
            "sci": "Aquarium species",
            "temp_min": round(env["temp_min_c"] * 9 / 5 + 32),
            "temp_max": round(env["temp_max_c"] * 9 / 5 + 32),
            "ph_min": float(env["ph_min"]), "ph_max": float(env["ph_max"]),
            "temperament": _temperament(row), "size": round(size_cm / 2.54, 1),
            "care": row.get("difficulty_level", "intermediate"),
            "water": "saltwater" if "salt" in slug or slug in {
                "blue-tang", "yellow-tang", "flame-angelfish", "coral-beauty",
                "percula-clownfish", "firefish-goby", "watchman-goby",
                "royal-gramma", "pajama-cardinalfish", "foxface-rabbitfish", "lionfish",
            } else "freshwater",
            "min_group": 6 if schooling else 1, "diet": "omnivore",
            "eats_small": size_cm >= 15 or _temperament(row) == "aggressive",
            "wiki": f"/wiki/{slug}/", "zone": _zone(slug, row),
            "min_tank_gal": max(5, round(float(env["min_tank_liters"]) / 3.785)),
            "desc": row.get("sections", {}).get("overview", "")[:360],
        }

    for slug, fish in v1.SPECIES.items():
        fish.setdefault("zone", _zone(slug, {}))
        fish.setdefault("min_tank_gal", v1.min_tank_size(fish, fish))
    if len(v1.SPECIES) != 91:
        raise RuntimeError(f"Expected 91 species, loaded {len(v1.SPECIES)}")


def overlap_score(a_min, a_max, b_min, b_max):
    overlap = max(0.0, min(a_max, b_max) - max(a_min, b_min))
    narrower = max(0.01, min(a_max - a_min, b_max - b_min))
    return round(min(100, overlap / narrower * 100))


def enhanced_compat(slug_a, slug_b):
    a, b = v1.SPECIES[slug_a], v1.SPECIES[slug_b]
    temp = overlap_score(a["temp_min"], a["temp_max"], b["temp_min"], b["temp_max"])
    ph = overlap_score(a["ph_min"], a["ph_max"], b["ph_min"], b["ph_max"])
    same_water = a["water"] == b["water"]
    temperament = {
        ("peaceful", "peaceful"): 100, ("peaceful", "semi"): 75,
        ("semi", "semi"): 62, ("aggressive", "peaceful"): 30,
        ("aggressive", "semi"): 25, ("aggressive", "aggressive"): 12,
    }.get(tuple(sorted((a["temperament"], b["temperament"]))), 50)
    ratio = max(a["size"], b["size"]) / max(.25, min(a["size"], b["size"]))
    size = 100 if ratio < 2 else 72 if ratio < 3 else 38 if ratio < 5 else 8
    zone = 92 if a["zone"] != b["zone"] else 68
    social = 85 if a["min_group"] > 1 and b["min_group"] > 1 else 92
    subscores = {"temperature": temp, "ph": ph, "temperament": temperament,
                 "adult_size": size, "swim_zone": zone, "social_needs": social}
    score = round(temp * .20 + ph * .15 + temperament * .25 + size * .20 + zone * .08 + social * .12)
    issues, positives = [], []
    special_bad, special_warn, special_note = v1.get_special_rule(slug_a, slug_b)
    if not same_water:
        score = 0; issues.append("These animals require different water types and cannot share one aquarium.")
    if special_bad:
        score = min(score, 18); issues.append(special_note)
    elif special_warn:
        score = min(score, 58); issues.append(special_note)
    if ratio >= 3 and (a.get("eats_small") or b.get("eats_small")):
        score = min(score, 32); issues.append("The adult size gap creates a meaningful predation risk.")
    trusted_pair = frozenset((slug_a, slug_b))
    if trusted_pair == frozenset(("discus", "cardinal-tetra")):
        # A widely used warm-water combination; the shared point at 82°F is
        # viable when stock is acclimated and water quality is excellent.
        score = max(score, 76)
        issues = [item for item in issues if "temperature" not in item.lower()]
        positives.append("Both species can be maintained together at about 82°F in soft, clean water.")
    if temp < 35: issues.append("Their preferred temperature ranges have little or no safe overlap.")
    else: positives.append("A stable shared temperature range is available.")
    if ph < 35: issues.append("Their preferred pH ranges are difficult to reconcile.")
    else: positives.append("Their pH requirements overlap.")
    if temperament >= 75: positives.append("Temperament risk is relatively low when normal group sizes are maintained.")
    verdict = "compatible" if score >= 75 else "caution" if score >= 45 else "incompatible"
    color = {"compatible": "#27AE60", "caution": "#F39C12", "incompatible": "#E74C3C"}[verdict]
    return {"score": score, "verdict": verdict, "color": color, "issues": issues,
            "positives": positives, "temp_overlap": f"{max(a['temp_min'], b['temp_min'])}–{min(a['temp_max'], b['temp_max'])}°F" if temp else "No overlap",
            "ph_overlap": f"{max(a['ph_min'], b['ph_min']):.1f}–{min(a['ph_max'], b['ph_max']):.1f}" if ph else "No overlap",
            "subscores": subscores}


def tank_scenarios(a, b):
    base = max(a["min_tank_gal"], b["min_tank_gal"], v1.min_tank_size(a, b))
    groups = a["min_group"] + b["min_group"]
    return (
        ("Minimum viable", base, "Only for the recommended minimum groups, mature filtration, and close monitoring."),
        ("Recommended community", round_up(base * 1.35), "Adds territory, swimming room, and a safer buffer for behavior."),
        ("Low-conflict setup", round_up(base * 1.75 + groups), "Best when keeping larger schools or reducing territorial pressure."),
    )


def round_up(value):
    for gallons in (10, 15, 20, 29, 40, 55, 75, 90, 100, 125, 150, 180, 220, 300):
        if gallons >= value: return gallons
    return int((value + 49) // 50 * 50)


def seo_priority(sa, sb, result):
    demand = (POPULARITY.get(sa, 35) + POPULARITY.get(sb, 35)) / 2
    useful = 100 - abs(60 - result["score"]) * .65  # uncertain pairs answer stronger queries
    return round(min(100, demand * .68 + useful * .32))


def inject_v2(html_text, sa, sb, result):
    a, b = v1.SPECIES[sa], v1.SPECIES[sb]
    score_rows = "".join(f"<tr><td>{label.replace('_',' ').title()}</td><td>{value}/100</td></tr>" for label, value in result["subscores"].items())
    scenarios = "".join(f"<tr><td><strong>{html.escape(label)}</strong></td><td>{gallons} gal</td><td>{html.escape(note)}</td></tr>" for label, gallons, note in tank_scenarios(a, b))
    section = f'''<section class="card v2-analysis"><h2>Compatibility score breakdown</h2>
<p>The overall score is weighted across water chemistry, behavior, adult size, swimming zone, and social needs. A score is a planning aid—not a guarantee for individual fish.</p>
<table class="cmp-table"><thead><tr><th>Factor</th><th>Score</th></tr></thead><tbody>{score_rows}</tbody></table></section>
<section class="card"><h2>Tank size scenarios</h2><p>Use the scenario that matches the actual group sizes and temperament you plan to keep.</p>
<table class="cmp-table"><thead><tr><th>Scenario</th><th>Tank</th><th>When it applies</th></tr></thead><tbody>{scenarios}</tbody></table></section>'''
    marker = '<div class="guide-links">'
    pos = html_text.find(marker)
    return html_text[:pos] + section + html_text[pos:] if pos >= 0 else html_text.replace("</main>", section + "</main>")


def species_hub(slug, ranked):
    fish = v1.SPECIES[slug]
    cards = []
    for other, result, priority in ranked:
        pair = "-and-".join(sorted((slug, other)))
        cards.append(f'''<a class="pair" href="/compatibility/{pair}/"><span><strong>{html.escape(fish['name'])} + {html.escape(v1.SPECIES[other]['name'])}</strong><small>SEO priority {priority}/100</small></span><b style="color:{result['color']}">{result['score']}/100 · {v1.VERDICT_TEXT[result['verdict']]}</b></a>''')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(fish['name'])} Tank Mates: 90 Compatibility Guides | FishCare AI</title><meta name="description" content="Compare {html.escape(fish['name'])} with 90 aquarium species. Ranked compatibility scores, water requirements, behavior risks, and tank size guidance.">
<link rel="canonical" href="https://www.fishcareai.com/compatibility/{slug}/"><link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260818-compat-v2">
<style>{v1.CSS}.hub{{max-width:960px;margin:32px auto;padding:0 22px}}.pair{{display:flex;justify-content:space-between;gap:16px;background:#fff;border:1px solid var(--bd);border-radius:12px;padding:14px 16px;margin:8px 0;color:var(--tx)}}.pair small{{display:block;color:var(--mu)}}@media(max-width:620px){{.pair{{display:block}}}}</style></head><body>
<header class="hero"><div class="con"><div class="breadcrumb"><a href="/">Home</a><span>›</span><a href="/compatibility/">Compatibility</a><span>›</span>{html.escape(fish['name'])}</div><h1>{html.escape(fish['name'])} Tank Mates</h1><p style="color:#dceef8">All 90 pair guides, ordered by search value and practical compatibility.</p></div></header>
<main class="hub"><section class="card"><h2>Care baseline</h2><p>{html.escape(fish['desc'])}</p><table class="cmp-table"><tr><td>Temperature</td><td>{fish['temp_min']}–{fish['temp_max']}°F</td></tr><tr><td>pH</td><td>{fish['ph_min']}–{fish['ph_max']}</td></tr><tr><td>Adult size</td><td>{fish['size']} in</td></tr><tr><td>Minimum group</td><td>{fish['min_group']}</td></tr></table></section><h2>Compatibility guides</h2>{''.join(cards)}</main></body></html>'''


def rebuild_sitemap(pair_rows):
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(SITEMAP); root = tree.getroot(); ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    for node in list(root):
        loc = node.find(f"{ns}loc")
        if loc is not None and "/compatibility/" in (loc.text or ""):
            root.remove(node)
    def add(path, priority):
        url = ET.SubElement(root, f"{ns}url")
        for tag, value in (("loc", f"https://www.fishcareai.com{path}"), ("lastmod", TODAY), ("changefreq", "monthly"), ("priority", f"{priority:.1f}")):
            ET.SubElement(url, f"{ns}{tag}").text = value
    add("/compatibility/", .8)
    for slug in sorted(v1.SPECIES): add(f"/compatibility/{slug}/", .7)
    # Keep the sitemap focused: index only P0/P1 pair pages; all pair pages remain
    # crawlable through hubs, preventing a 4,000-page low-value sitemap explosion.
    for sa, sb, priority in sorted(pair_rows, key=lambda x: -x[2]):
        if priority >= 62: add(f"/compatibility/{sa}-and-{sb}/", .7 if priority >= 78 else .6)
    ET.indent(tree, space="  "); tree.write(SITEMAP, encoding="utf-8", xml_declaration=True)


def main_hub(pairs):
    """Reuse the v1 presentation while pointing Browse by Species at v2 hubs."""
    page = v1.make_index(pairs)
    split_at = page.index("<h2>Browse by Species</h2>")
    head, browse = page[:split_at], page[split_at:]
    for slug in v1.SPECIES:
        browse = re.sub(
            rf'href="/compatibility/{re.escape(slug)}-and-[^"]+/"',
            f'href="/compatibility/{slug}/"', browse, count=1,
        )
    return head + browse


def main():
    load_catalogue()
    v1.compute_compat = enhanced_compat
    pairs = list(combinations(sorted(v1.SPECIES), 2))
    ranked_by_species = {slug: [] for slug in v1.SPECIES}
    sitemap_rows = []
    for index, (sa, sb) in enumerate(pairs, 1):
        result = enhanced_compat(sa, sb); priority = seo_priority(sa, sb, result)
        out = ROOT / "compatibility" / f"{sa}-and-{sb}" / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(inject_v2(v1.make_page(sa, sb), sa, sb, result), encoding="utf-8")
        ranked_by_species[sa].append((sb, result, priority)); ranked_by_species[sb].append((sa, result, priority))
        sitemap_rows.append((sa, sb, priority))
        if index % 500 == 0: print(f"Generated {index}/{len(pairs)} pair pages")
    for slug, rows in ranked_by_species.items():
        rows.sort(key=lambda item: (-item[2], -item[1]["score"], item[0]))
        out = ROOT / "compatibility" / slug / "index.html"; out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(species_hub(slug, rows), encoding="utf-8")
    (ROOT / "compatibility" / "index.html").write_text(main_hub(pairs), encoding="utf-8")
    rebuild_sitemap(sitemap_rows)
    print(f"Done: {len(v1.SPECIES)} species, {len(pairs)} pairs, {len(ranked_by_species)} species hubs")


if __name__ == "__main__":
    main()
