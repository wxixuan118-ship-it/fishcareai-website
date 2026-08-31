"""Create a risk-led SEO pilot for a deliberately small set of pair pages.

This is intentionally separate from the all-page v2 generator: its raw catalogue
is not present in this checkout. The pilot upgrades existing rendered pages without
touching pairs outside the manifest, so its copy and quality can be reviewed first.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPATIBILITY = ROOT / "compatibility"

# Each page has a unique, fact-specific risk and next step. The category controls
# structure, while the per-page copy prevents a find-and-replace content cluster.
PILOT_PAGES = {
    "koi-and-silver-arowana": ("water", "Koi are cool-water pond fish, while Silver Arowana need a warm, enclosed tropical system.", "Keep Koi in a purpose-built pond and house Silver Arowana separately in a heated aquarium."),
    "goldfish-and-zebra-danio": ("temperature", "Goldfish thrive in cooler water, while Zebra Danios need a stable temperature that can make long-term compromise difficult.", "Choose a cool-water community for Goldfish or build a dedicated Zebra Danio school."),
    "koi-and-pygmy-corydoras": ("predation", "The adult size gap makes tiny Pygmy Corydoras vulnerable and Koi require a very different pond-scale setup.", "Keep Pygmy Corydoras with peaceful tropical community fish instead."),
    "blue-tang-and-diamond-tetra": ("water", "Blue Tangs are marine reef fish and Diamond Tetras are freshwater fish, so there is no shared water system.", "Build a marine community around the Blue Tang and a freshwater school around the Diamond Tetras."),
    "percula-clownfish-and-sparkling-gourami": ("water", "Percula Clownfish require saltwater and Sparkling Gourami require freshwater.", "Keep each species in a dedicated marine or freshwater aquarium."),
    "lionfish-and-zebra-loach": ("water", "Lionfish are marine predators, while Zebra Loaches are freshwater schooling fish.", "Do not attempt to bridge the saltwater-freshwater divide with acclimation experiments."),
    "angelfish-and-oscar": ("territory", "Oscars are large, powerful cichlids that can injure or outcompete Angelfish as they mature.", "Plan an Oscar species tank or pair Angelfish with calmer, similarly sized companions."),
    "betta-fish-and-guppy": ("territory", "A Betta may target Guppies' flowing fins, while fast Guppy activity can also stress a territorial Betta.", "Use a heavily planted, closely monitored setup only if both fish show calm behavior; separate them at the first sign of chasing."),
    "ember-tetra-and-tiger-barb": ("territory", "Tiger Barbs can harass the much smaller Ember Tetras and compete aggressively at feeding time.", "Keep Tiger Barbs in a large group with robust, quick tank mates rather than nano tetras."),
    "cherry-shrimp-and-mystery-snail": ("compatible", "Neither animal is a predatory threat to the other, provided water parameters and food are managed carefully.", "Provide calcium for the snail, biofilm for the shrimp, and avoid copper-based treatments."),
    "cherry-shrimp-and-fire-eel": ("predation", "A Fire Eel grows large enough to treat Cherry Shrimp as food rather than tank mates.", "Keep Cherry Shrimp in a shrimp-focused aquarium with small, peaceful companions."),
    "dwarf-chain-loach-and-pea-puffer": ("territory", "Pea Puffers are territorial and Dwarf Chain Loaches may be harassed or compete for the same lower-tank space.", "Keep Pea Puffers in a species-focused setup and maintain loaches in their own group."),
    "discus-and-neon-tetra": ("caution", "Neon Tetras can survive near the low end of a Discus temperature range, but prolonged warm water may shorten their lifespan.", "Use Cardinal Tetras for a warmer Discus setup, or keep Neons with fish that prefer a cooler tropical range."),
    "congo-tetra-and-neon-tetra": ("caution", "The two schooling species can overlap in water parameters, but Congo Tetras' size and activity can unsettle small Neon Tetras.", "Use a long planted tank, full schools of both species, and observe feeding competition."),
    "goldfish-and-hillstream-loach": ("caution", "Both can prefer cooler water, but Goldfish waste output and feeding behavior can overwhelm Hillstream Loaches.", "Use strong filtration, high oxygen, and a mature tank with algae-covered surfaces."),
    "guppy-and-zebra-danio": ("caution", "Fast Zebra Danios may nip Guppy fins or outcompete them for food in an undersized tank.", "Keep larger groups, provide cover, and avoid long-finned Guppy strains."),
    "molly-and-sterbai-cory": ("caution", "Their pH and temperature preferences only partly overlap, so a compromise setup needs stable, tested water.", "Choose a stable middle range and keep both species in their appropriate social groups."),
    "corydoras-and-oscar": ("predation", "An adult Oscar can injure or swallow small Corydoras, despite their armoured bodies.", "Choose robust, appropriately sized Oscar tank mates instead of small catfish."),
    "black-ghost-knifefish-and-zebra-danio": ("predation", "A mature Black Ghost Knifefish may view small Zebra Danios as prey, especially after dark.", "Use larger, calm companions that cannot fit in the knifefish's mouth."),
    "clown-knifefish-and-nerite-snail": ("predation", "A Clown Knifefish becomes far too large for a typical mixed aquarium and can disturb or consume small invertebrates.", "Plan a specialist system for the Clown Knifefish and keep Nerite Snails in a peaceful community."),
    "jewel-cichlid-and-mystery-snail": ("territory", "Breeding or territorial Jewel Cichlids can repeatedly harass a slow Mystery Snail.", "Keep the snail with peaceful community fish or provide a separate cichlid territory."),
    "electric-yellow-cichlid-and-flame-angelfish": ("water", "Electric Yellow Cichlids are freshwater fish and Flame Angelfish are marine reef fish.", "These species require separate freshwater and saltwater systems."),
    "firefish-goby-and-oscar": ("water", "Firefish Gobies are saltwater reef fish, while Oscars are large freshwater cichlids.", "Keep each species in an environment designed for its water type and behavior."),
    "coral-beauty-and-platy": ("water", "Coral Beauty Angelfish need a marine reef and Platies need freshwater.", "Do not mix freshwater and marine livestock in a single system."),
    "discus-and-lionfish": ("water", "Discus are freshwater fish and Lionfish are marine predators.", "Keep both species in dedicated systems with their own compatible tank mates."),
    "koi-and-zebra-pleco": ("temperature", "Koi need cool, pond-scale conditions while Zebra Plecos need warm, oxygen-rich tropical aquariums.", "Keep Zebra Plecos in a warm specialist aquarium with caves and strong filtration."),
    "pajama-cardinalfish-and-silver-arowana": ("water", "Pajama Cardinalfish are marine fish, while Silver Arowana are freshwater fish.", "Maintain separate reef and freshwater predator systems."),
    "foxface-rabbitfish-and-zebra-danio": ("water", "Foxface Rabbitfish are marine fish and Zebra Danios are freshwater fish.", "Use species-appropriate marine and freshwater communities instead."),
    "clown-loach-and-silver-dollar": ("compatible", "These active fish can share warm freshwater when their large adult size, schooling needs, and tank footprint are respected.", "Use a long aquarium, full groups, and robust filtration before considering the combination."),
    "goldfish-and-percula-clownfish": ("water", "Goldfish are freshwater fish and Percula Clownfish are marine fish.", "Keep the Goldfish in a cool freshwater setup and the Clownfish in a mature saltwater aquarium."),
}


PROFILE_LABELS = {
    "water": "Water Type Makes This Pair Impossible",
    "temperature": "Temperature and Habitat Requirements Conflict",
    "predation": "Adult Size and Predation Risk",
    "territory": "Behavior and Territory Are the Main Risk",
    "compatible": "What Makes This Pair Work",
    "caution": "How to Reduce the Risk",
}


def page_names(text: str) -> tuple[str, str]:
    match = re.search(r"<h1>Can (.+?) Live With (.+?)\?</h1>", text, re.I)
    if not match:
        match = re.search(r"<h1>Can (.+?) and (.+?) Live Together\?</h1>", text, re.I)
    if not match:
        raise ValueError("Could not find the pair H1")
    return html.unescape(match.group(1)), html.unescape(match.group(2))


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.S | re.I)
    if count != 1:
        raise ValueError(f"Expected one {label} replacement, found {count}")
    return result


def faq_html(a: str, b: str, kind: str, risk: str, action: str) -> str:
    if kind == "compatible":
        questions = [
            (f"Can {a} live with {b} long term?", f"Usually, yes, when their shared water range, group sizes, and adult space needs are met. {risk}"),
            (f"What tank setup helps {a} and {b} coexist?", action),
            (f"What should I monitor after adding {a} and {b}?", "Monitor feeding access, chasing, water quality, and whether every animal can use its preferred swimming or resting area."),
            (f"When should {a} and {b} be separated?", "Separate them if aggression, repeated food competition, injury, or declining water quality appears."),
        ]
    elif kind == "caution":
        questions = [
            (f"Can {a} live with {b}?", f"They may coexist, but this is a cautious pairing rather than a default recommendation. {risk}"),
            (f"What is the main risk with {a} and {b}?", risk),
            (f"What setup reduces conflict between {a} and {b}?", action),
            (f"When should I avoid keeping {a} and {b} together?", "Avoid the pairing in a small tank, with incomplete social groups, or when either species shows persistent stress or aggression."),
        ]
    else:
        questions = [
            (f"Can {a} live with {b}?", f"No, this is not a suitable long-term pairing. {risk}"),
            (f"What is the biggest risk for {a} and {b}?", risk),
            (f"Would a larger tank make {a} and {b} compatible?", "More space can reduce some conflict, but it cannot solve incompatible water type, temperature, predation, or core welfare needs."),
            (f"What is a safer alternative to keeping {a} and {b} together?", action),
        ]
    return "\n".join(
        f"<details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in questions
    )


def clip_words(text: str, limit: int) -> str:
    """Keep meta copy in the snippet range without cutting a word in half."""
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "."


def meta_description(question: str, risk: str) -> str:
    suffix = " Explore tank setup and safer alternatives."
    available = 160 - len(question) - len(suffix) - 1
    return f"{question} {clip_words(risk, max(45, available))}{suffix}"


def seo_title(a: str, b: str, question: str) -> str:
    """Prefer the natural full question, with a compact fallback for long names."""
    if len(question) <= 60:
        return question
    return f"Can {a} Live With {b}?"


def upgrade_page(path: Path, kind: str, risk: str, action: str) -> None:
    text = path.read_text(encoding="utf-8")
    a, b = page_names(text)
    question = f"Can {a} and {b} Live Together?"
    # The search intent is the complete question; do not dilute it with a
    # repeated category label or a brand suffix that pushes long fish names past 60 characters.
    title = seo_title(a, b, question)
    description = meta_description(question, risk)
    overview = f"{question} {'Usually, yes, with careful planning.' if kind == 'compatible' else 'Only with caution and a purpose-built setup.' if kind == 'caution' else 'No, not as a long-term shared setup.'} {risk}"
    risk_section = (
        f'<div class="card"><h2>{html.escape(PROFILE_LABELS[kind])}</h2><p>{html.escape(risk)}</p></div>'
        f'<div class="card"><h2>A Safer Plan for {html.escape(a)} and {html.escape(b)}</h2><p>{html.escape(action)}</p></div>'
    )

    text = replace_once(text, r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", "title")
    text = replace_once(text, r'(<meta name="description" content=").*?("/>)', rf'\g<1>{html.escape(description, quote=True)}\2', "description")
    text = replace_once(text, r'(<meta property="og:title" content=").*?("/>)', rf'\g<1>{html.escape(title, quote=True)}\2', "Open Graph title")
    text = replace_once(text, r'(<meta property="og:description" content=").*?("/>)', rf'\g<1>{html.escape(description, quote=True)}\2', "Open Graph description")
    text = replace_once(text, r'("@type": "Article", "headline": ").*?("\s*,\s*"description": ").*?("\s*,\s*"datePublished")', rf'\g<1>{html.escape(title, quote=True)}\2{html.escape(description, quote=True)}\3', "Article schema")
    text = replace_once(text, r"<h1>.*?</h1>", f"<h1>{html.escape(question)}</h1>", "H1")
    text = replace_once(text, r"<div class=\"card\">\s*<h2>(?:Compatibility Overview|Can .*? Live Together\?)</h2>\s*<p>.*?</p>", f'<div class="card"><h2>{html.escape(question)}</h2><p>{html.escape(overview)}</p>', "overview")
    text = replace_once(text, r"(<div class=\"card faq\">\s*<h2>Frequently Asked Questions</h2>).*?(</div>\s*<div class=\"card\">\s*<h2>Related Compatibility Guides</h2>)", rf"\1\n{faq_html(a, b, kind, risk, action)}\n\2", "FAQ")
    existing_risks = r'<div class="card"><h2>(?:' + "|".join(re.escape(label) for label in PROFILE_LABELS.values()) + r')</h2><p>.*?</p></div><div class="card"><h2>A Safer Plan for .*?</h2><p>.*?</p></div>\s*'
    text, replaced = re.subn(existing_risks, risk_section + "\n", text, count=1, flags=re.S)
    if replaced == 0:
        text = replace_once(text, r"(<div class=\"card\">\s*<h2>Species Profiles</h2>)", risk_section + r"\n\1", "risk sections")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate the manifest without writing files.")
    args = parser.parse_args()
    missing = [slug for slug in PILOT_PAGES if not (COMPATIBILITY / slug / "index.html").exists()]
    if missing:
        raise SystemExit("Missing pilot pages: " + ", ".join(missing))
    if args.check:
        print(f"Pilot manifest is valid: {len(PILOT_PAGES)} pages")
        return
    for slug, (kind, risk, action) in PILOT_PAGES.items():
        upgrade_page(COMPATIBILITY / slug / "index.html", kind, risk, action)
    print(f"Upgraded {len(PILOT_PAGES)} compatibility pilot pages")


if __name__ == "__main__":
    main()
