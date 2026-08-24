#!/usr/bin/env python3
"""Build crawlable disease hubs only from URLs verified in a GSC Coverage export."""
from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import openpyxl

SITE = "https://www.fishcareai.com"
SYMPTOMS = (
    "rapid-breathing", "pale-color", "fin-rot", "losing-color", "missing-scales",
    "cloudy-eyes", "sunken-belly", "swimming-sideways", "fuzzy-growth", "white-spots",
    "mucus-coating", "curled-body", "not-eating", "black-spots", "spots-on-fins",
    "red-streaks", "clamped-fins", "torn-fins", "bulging-eyes", "bloated", "aggressive",
    "coughing", "darting", "floating", "gasping", "hiding", "jumping", "lethargic",
    "rubbing", "sinking",
)


def label(slug: str) -> str:
    return " ".join(word.upper() if word in {"hith", "ich"} else word.capitalize() for word in slug.split("-"))


def split_slug(slug: str) -> tuple[str, str] | None:
    for symptom in SYMPTOMS:
        token = "-" + symptom
        if slug.endswith(token):
            return slug[: -len(token)], symptom
    return None


def document(title: str, description: str, canonical: str, schema: list[dict], body: str, js: str = "") -> str:
    schemas = "\n".join(
        '<script type="application/ld+json">' + json.dumps(item, separators=(",", ":")) + "</script>" for item in schema
    )
    return f'''<!doctype html>
<html lang="en" data-adsense-content="false"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{html.escape(canonical)}"><link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260823-screenshot">
{schemas}
<style>
body{{background:#07192d;color:#d8eaf5}} main{{max-width:1100px;margin:auto;padding:40px 20px 70px}} .hero{{text-align:center;padding:35px 0 22px}} h1{{color:#fff;font-size:clamp(2rem,5vw,3.2rem)}} h2{{color:#d8eaf5;margin-top:45px}} p,li{{color:#c0ddf0;line-height:1.65}} a{{color:#7ecaf5}} .crumb{{font-size:.86rem}} .search{{background:#0d2741;border:1px solid #286198;border-radius:16px;padding:20px;position:relative}} input{{width:100%;box-sizing:border-box;padding:14px;border-radius:9px;border:1px solid #4ab3e8;background:#07192d;color:#fff;font-size:1rem}} .results{{display:none;position:absolute;left:20px;right:20px;z-index:2;background:#0d2741;border:1px solid #4ab3e8;border-radius:9px;margin-top:6px;overflow:hidden}} .results.show{{display:block}} .result{{display:block;padding:11px 14px;text-decoration:none}} .result[aria-selected=true],.result:hover{{background:#123958}} .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:15px}} .card{{display:block;background:#0d2741;border:1px solid #286198;border-radius:14px;padding:18px;text-decoration:none}} .card:hover{{border-color:#4ab3e8}} .card h3{{color:#d8eaf5;margin:0 0 8px}} .count{{font-size:.85rem;color:#9fc7df}} .notice{{border-left:4px solid #4ab3e8;background:#0d2741;padding:16px 18px;border-radius:8px}} .source li{{margin:8px 0}}
</style><script defer src="/assets/site-compliance.js?v=20260824-dark-fix"></script></head>
<body><nav class="nb"></nav><main>{body}</main><footer class="ft"></footer>{js}</body></html>'''


def breadcrumbs(items: list[tuple[str, str]]) -> dict:
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url} for i, (name, url) in enumerate(items)
    ]}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coverage", type=Path)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    wb = openpyxl.load_workbook(args.coverage, read_only=True, data_only=True)
    sheet = wb["表格"]
    urls = sorted({str(row[0]).rstrip("/") for row in sheet.iter_rows(min_row=2, values_only=True) if row and row[0]})
    condition_urls = [url for url in urls if "/fish-health/" in url and "/fish-health/fish/" not in url]
    groups: dict[str, list[dict]] = defaultdict(list)
    skipped = []
    for url in condition_urls:
        slug = url.rsplit("/", 1)[-1]
        parsed = split_slug(slug)
        if not parsed:
            skipped.append(url)
            continue
        species, symptom = parsed
        groups[species].append({"species": label(species), "speciesSlug": species, "condition": label(symptom), "slug": slug, "url": url})
    for pages in groups.values():
        pages.sort(key=lambda page: (page["condition"], page["slug"]))

    root = args.root
    hubs = []
    for species, pages in sorted(groups.items(), key=lambda item: (-len(item[1]), label(item[0]))):
        hub_path = f"/aquarium-fish-diseases/{species}-diseases/"
        hub_url = SITE + hub_path
        species_name = label(species)
        hubs.append({"species": species_name, "speciesSlug": species, "url": hub_path, "count": len(pages), "examples": [p["condition"] for p in pages[:3]]})
        item_list = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f'{page["species"]} {page["condition"]}', "url": page["url"]}
            for i, page in enumerate(pages)
        ]}
        faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": "How should I use these fish symptom guides?", "acceptedAnswer": {"@type": "Answer", "text": "Start with water test results, the fish species and visible symptoms. Similar signs can have different causes, so these pages are educational starting points rather than a diagnosis."}},
            {"@type": "Question", "name": "When should I seek professional help?", "acceptedAnswer": {"@type": "Answer", "text": "Contact an aquatic veterinarian or fish-health professional for severe breathing difficulty, open ulcers, rapid deterioration, repeated deaths or symptoms that persist after water conditions are corrected."}},
        ]}
        cards = "".join(f'''<a class="card" href="{html.escape(page["url"])}"><h3>{html.escape(page["condition"])} on {html.escape(page["species"])} </h3><p>View symptoms and possible causes.</p></a>''' for page in pages)
        body = f'''<p class="crumb"><a href="/">Home</a> › <a href="/aquarium-fish-diseases/">Aquarium Fish Diseases</a> › {html.escape(species_name)} Diseases</p>
<section class="hero"><h1>{html.escape(species_name)} Diseases: Symptoms, Causes &amp; Guides</h1><p>Browse {len(pages)} currently indexed symptom and disease guides for {html.escape(species_name)}. Check water quality first and use symptoms only to narrow possible causes.</p></section>
<section class="notice"><strong>Important:</strong> Similar symptoms may have infectious, environmental, nutritional or physical causes. These guides are educational and are not a veterinary diagnosis.</section>
<section><h2>{html.escape(species_name)} symptom and disease guides</h2><div class="grid">{cards}</div></section>
<section><h2>What to check before treatment</h2><ol><li>Test ammonia, nitrite, nitrate, pH and temperature.</li><li>Record the symptom, duration and changes in behaviour.</li><li>Check whether other fish are affected and whether new fish, plants or equipment were added.</li><li>Avoid mixing medications based on one visible symptom alone.</li></ol></section>
<section><h2>Frequently asked questions</h2><h3>How should I use these fish symptom guides?</h3><p>Start with water test results, the fish species and visible symptoms. Similar signs can have different causes, so these pages are educational starting points rather than a diagnosis.</p><h3>When should I seek professional help?</h3><p>Contact an aquatic veterinarian or fish-health professional for severe breathing difficulty, open ulcers, rapid deterioration, repeated deaths or symptoms that persist after water conditions are corrected.</p></section>'''
        schema = [
            {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{species_name} Diseases", "url": hub_url},
            breadcrumbs([("Home", SITE + "/"), ("Aquarium Fish Diseases", SITE + "/aquarium-fish-diseases/"), (f"{species_name} Diseases", hub_url)]), item_list, faq,
        ]
        write(root / "aquarium-fish-diseases" / f"{species}-diseases" / "index.html", document(f"{species_name} Diseases: Symptoms, Causes & Guides", f"Browse {len(pages)} indexed {species_name} symptom and disease guides. Compare signs, possible causes and next checks.", hub_url, schema, body))

    search_index = [page | {"hubUrl": f'/aquarium-fish-diseases/{page["speciesSlug"]}-diseases/'} for pages in groups.values() for page in pages]
    write(root / "assets" / "disease-search-index.json", json.dumps(search_index, indent=2) + "\n")
    hub_cards = "".join(f'''<a class="card" href="{hub["url"]}"><h3>{html.escape(hub["species"])} Diseases</h3><p class="count">{hub["count"]} indexed guides</p><p>{html.escape(" · ".join(hub["examples"]))}</p><strong>View {html.escape(hub["species"])} guides →</strong></a>''' for hub in hubs)
    quick = "".join(f'<button type="button" data-query="{html.escape(hub["species"])} {html.escape(hub["examples"][0])}">{html.escape(hub["species"])} {html.escape(hub["examples"][0])}</button>' for hub in hubs[:6])
    item_list = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f'{hub["species"]} Diseases', "url": SITE + hub["url"]} for i, hub in enumerate(hubs)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "What are common aquarium fish disease symptoms?", "acceptedAnswer": {"@type": "Answer", "text": "Common warning signs include spots, fin damage, swelling, unusual swimming, appetite changes, rapid breathing and changes in colour or waste. Similar symptoms can have different causes."}},
        {"@type": "Question", "name": "Can poor water quality make fish look sick?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Ammonia, nitrite, unsuitable temperature, unstable pH and low oxygen can contribute to breathing difficulty, lethargy, appetite loss, skin damage and abnormal swimming."}},
        {"@type": "Question", "name": "Are these fish disease guides a veterinary diagnosis?", "acceptedAnswer": {"@type": "Answer", "text": "No. They provide educational information and possible explanations. Diagnosis and medication decisions should be confirmed by a qualified aquatic veterinarian or fish-health professional where possible."}},
    ]}
    body = f'''<p class="crumb"><a href="/">Home</a> › Aquarium Fish Diseases</p><section class="hero"><h1>Aquarium Fish Diseases: Symptoms, Causes &amp; Treatment</h1><p>Is your fish showing white spots, fin damage, swelling, unusual swimming, appetite loss or breathing problems? Explore FishCareAI's disease library by species and symptom to find relevant educational guides.</p></section>
<section class="search" aria-labelledby="search-label"><label id="search-label" for="disease-search"><strong>Search by fish species and disease or symptom</strong></label><input id="disease-search" type="search" placeholder="Try: betta white spots, goldfish fin rot, guppy bloated" autocomplete="off" aria-expanded="false" aria-controls="disease-results"><div id="disease-results" class="results" role="listbox"></div><p class="count">Search uses {len(search_index)} currently indexed Fish Health guides. Results appear after two characters.</p><div>{quick}</div></section>
<section><h2>Fish Diseases by Species</h2><p>Each species Hub contains only links that appeared in the supplied Google Coverage export on {date.today().isoformat()}.</p><div class="grid">{hub_cards}</div></section>
<section><h2>Common Aquarium Fish Disease Symptoms</h2><p>Use the species Hubs to explore white spots, frayed or rotting fins, fuzzy growth, cloudy or swollen eyes, bloating, red streaks, rapid breathing, rubbing, appetite loss, floating, sinking and swimming sideways.</p></section>
<section><h2>What to Check Before Treating a Sick Fish</h2><ol><li>Measure ammonia, nitrite, nitrate, pH and temperature.</li><li>Observe whether one fish or several fish show symptoms.</li><li>Check for recent additions or equipment changes.</li><li>Record symptoms and their progression; isolate a sick fish where appropriate.</li><li>Do not combine medications based on one visible sign alone.</li><li>Seek professional care for severe or deteriorating cases.</li></ol></section>
<section><h2>Sources and Editorial Method</h2><p>Last reviewed: August 2026. Reviewed for: species naming, symptom terminology, water-quality guidance and source quality.</p><ul class="source"><li><a href="https://www.merckvetmanual.com/all-other-pets/fish/disorders-and-diseases-of-fish">Merck Veterinary Manual — Disorders and Diseases of Fish</a></li><li><a href="https://www.merckvetmanual.com/exotic-and-laboratory-animals/aquarium-fish/management-of-aquarium-fish">Merck Veterinary Manual — Management of Aquarium Fish</a></li><li><a href="https://www.woah.org/en/what-we-do/animal-health-and-welfare/aquatic-animals/">World Organisation for Animal Health — Aquatic Animals</a></li></ul></section>
<section><h2>Frequently asked questions</h2><h3>What are common aquarium fish disease symptoms?</h3><p>Common warning signs include spots, fin damage, swelling, unusual swimming, appetite changes, rapid breathing and changes in colour or waste. Similar symptoms can have different causes.</p><h3>Can poor water quality make fish look sick?</h3><p>Yes. Ammonia, nitrite, unsuitable temperature, unstable pH and low oxygen can contribute to breathing difficulty, lethargy, appetite loss, skin damage and abnormal swimming.</p><h3>Are these fish disease guides a veterinary diagnosis?</h3><p>No. They provide educational information and possible explanations. Diagnosis and medication decisions should be confirmed by a qualified aquatic veterinarian or fish-health professional where possible.</p></section>'''
    root_schema = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Aquarium Fish Diseases: Symptoms, Causes & Treatment", "url": SITE + "/aquarium-fish-diseases/"}, breadcrumbs([("Home", SITE + "/"), ("Aquarium Fish Diseases", SITE + "/aquarium-fish-diseases/")]), item_list, faq]
    js = '''<script>const input=document.querySelector('#disease-search'),box=document.querySelector('#disease-results');let matches=[],selected=-1;fetch('/assets/disease-search-index.json').then(r=>r.json()).then(data=>{function render(){const q=input.value.trim().toLowerCase();if(q.length<2){box.classList.remove('show');return}const terms=q.split(/\\s+/);matches=data.filter(x=>{const hay=[x.species,x.condition,x.slug].join(' ').toLowerCase();return terms.every(t=>hay.includes(t))}).slice(0,10);selected=-1;box.innerHTML=matches.length?matches.map((x,i)=>`<a class="result" role="option" aria-selected="false" href="${x.url}"><strong>${x.species} · ${x.condition}</strong><br><span class="count">View guide →</span></a>`).join(''):'<p class="result">No matching guide. Try the <a href="/tools/water-parameter-checker/">Water Parameter Checker</a> or <a href="https://identify.fishcareai.com/">Fish Identify</a>.</p>';box.classList.add('show')}input.addEventListener('input',render);input.addEventListener('keydown',e=>{const nodes=[...box.querySelectorAll('.result[role=option]')];if(!nodes.length)return;if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();selected=(selected+(e.key==='ArrowDown'?1:nodes.length-1))%nodes.length;nodes.forEach((n,i)=>n.setAttribute('aria-selected',String(i===selected)))}if(e.key==='Enter'&&selected>=0)nodes[selected].click()});document.querySelectorAll('[data-query]').forEach(b=>b.addEventListener('click',()=>{input.value=b.dataset.query;input.focus();render()}))});</script>'''
    write(root / "aquarium-fish-diseases" / "index.html", document("Aquarium Fish Diseases: Symptoms, Causes & Treatment Guide", "Identify common aquarium fish diseases by species and symptoms. Explore possible causes, warning signs, prevention tips and species-specific fish disease guides.", SITE + "/aquarium-fish-diseases/", root_schema, body, js))
    print(json.dumps({"condition_pages": len(condition_urls), "mapped_pages": len(search_index), "species_hubs": len(hubs), "unmapped_pages": len(skipped)}, indent=2))


if __name__ == "__main__":
    main()
