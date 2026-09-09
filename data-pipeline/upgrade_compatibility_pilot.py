"""Create a risk-led SEO pilot for a deliberately small set of pair pages.

This is intentionally separate from the all-page v2 generator: its raw catalogue
is not present in this checkout. The pilot upgrades existing rendered pages without
touching pairs outside the manifest, so its copy and quality can be reviewed first.
"""

from __future__ import annotations

import argparse
import html
import json
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
    "goldfish-and-molly": ("temperature", "Goldfish stay healthiest in cool water while Mollies need steady tropical warmth and hard, alkaline conditions, so one species is always kept outside its range.", "Keep Mollies in a heated, hard-water tropical tank and give Goldfish a cool, heavily filtered setup of their own."),
    "goldfish-and-oscar": ("temperature", "Oscars need warm tropical water that Goldfish cannot tolerate long term, and an Oscar will also take any tank mate small enough to swallow.", "House the Oscar with robust, similarly sized tropical tank mates and keep Goldfish in a cool-water tank or pond."),
    "betta-fish-and-pea-puffer": ("territory", "Pea Puffers are persistent fin-nippers and a male Betta's trailing fins are an obvious target, while the Betta's own territorial displays keep both fish under constant stress.", "Keep Pea Puffers in a densely planted species-only tank and give the Betta either its own tank or calm, short-finned companions."),
    "green-terror-cichlid-and-senegal-bichir": ("territory", "Green Terrors are aggressive, strongly territorial cichlids, and a slow bottom-dwelling Senegal Bichir cannot avoid sustained harassment once the cichlid claims the floor of the tank.", "Give the Green Terror a species tank or fast, robust cichlid companions, and keep the Senegal Bichir with calm, similarly sized fish that stay out of its way."),
}


VERDICTS = {
    "water": "No. These species need different water types, so a single aquarium cannot meet both sets of requirements.",
    "temperature": "No. Their temperature ranges do not overlap safely, so one of the two would spend its life outside its healthy range.",
    "predation": "No. The adult size difference makes this a predator-and-prey pairing rather than a community one.",
    "territory": "No. Territorial behaviour, rather than tank size, is what makes this pairing fail.",
    "compatible": "Usually, yes — provided their shared water range, group sizes and adult space needs are all met.",
    "caution": "Sometimes, but treat it as a cautious pairing that needs a purpose-built setup rather than a default recommendation.",
}


# Long-form copy for pages that need real depth rather than another restatement
# of the risk line. Written to lean on varied referents ("the pair", "the puffer")
# so that adding words lowers keyword density instead of raising it.
PILOT_DETAIL = {
    "goldfish-and-molly": (
        "What Actually Goes Wrong",
        "<p>The temperature gap is the part that cannot be designed around. One side of this pair is a cool-water fish that does best between 65 and 72&nbsp;&deg;F; the other is a tropical livebearer that wants 75 to 82&nbsp;&deg;F. Setting a heater to a compromise near 74&nbsp;&deg;F leaves both animals mildly stressed rather than either one comfortable &mdash; the cool-water fish runs a faster metabolism than it should, while the livebearer sits at the bottom of its range, where it becomes noticeably more prone to fungal and bacterial infection.</p>"
        "<p>Hardness pulls in the same direction. Livebearers do best in mineral-rich water above pH&nbsp;7.5, which the other fish tolerates but does not need. The problem is holding that chemistry steady: a heavy waste producer in the small, warm tank the livebearer prefers will swing pH and nitrate faster than a weekly change can correct.</p>"
        "<p>A size and feeding mismatch then shows up later. A mature specimen reaches six inches or more in the body and will sample anything that fits in its mouth, starting with fry and eventually including an adult livebearer that swims too slowly to get out of the way. The pairing often looks fine for a first year, while both fish are still small, and fails as the larger one grows.</p>"
        "<p>If the goal is one tank rather than two, choose the temperature bracket first and stock around it. A cool-water setup works with white cloud mountain minnows or hillstream loaches; a heated, hard-water setup works with platies and swordtails.</p>"
    ),
    "goldfish-and-oscar": (
        "What Actually Goes Wrong",
        "<p>Temperature is the first blocker and the one the calculator scores hardest. A large South American cichlid is kept between 74 and 81&nbsp;&deg;F, while the other fish here is a cool-water species that is healthiest below 72&nbsp;&deg;F and can be kept unheated in most rooms. There is no overlap that serves both animals; a heater set for the cichlid keeps the cool-water fish permanently over-warmed, which shortens its life without ever producing an obvious symptom.</p>"
        "<p>Adult size settles the rest. The cichlid reaches twelve to fourteen inches and swallows anything that fits. Feeder fish are sold for precisely this purpose, and the practice is worth avoiding on its own merits: they are typically raised at high density, arrive carrying parasites, and a diet built on them contributes to thiaminase-linked deficiency in the predator. What looks like a stocking decision is really a feeding decision.</p>"
        "<p>Waste load is the third strike. Both species are unusually heavy producers for their size, and combining them in one system means sizing filtration for the pair rather than for either fish &mdash; on top of a temperature setting that is already wrong for one of them.</p>"
        "<p>Keep the cichlid in a warm 75-gallon or larger tank with robust, similarly sized companions, and keep the cool-water fish in an unheated tank or a pond.</p>"
    ),
    "betta-fish-and-pea-puffer": (
        "Why This Pairing Fails in a Small Tank",
        "<p>Both fish are small, which makes this look like an easier pairing than it is. Size is not what drives the outcome here &mdash; hunting style is. The puffer is a micro-predator that spends its day picking at snails, biofilm and anything that drifts slowly past, and it investigates with its teeth. Long, unpaired, slow-moving fins are exactly the kind of target that behaviour is built around.</p>"
        "<p>The pressure runs both ways. A male betta flares and holds station at a chosen spot, and a puffer does not read that display as a reason to leave. Neither animal retreats, so instead of one clear aggressor and one victim you get sustained low-level conflict, which shows up as clamped fins, hiding and refused food long before any visible bite appears.</p>"
        "<p>Tank shape matters more than raw volume. Broken sightlines &mdash; dense stem plants, wood, floating cover &mdash; do more to reduce contact than an extra ten gallons of open water, because the conflict is driven by encounters rather than by crowding.</p>"
        "<p>Diet is the quieter problem. Pufferfish teeth grow continuously and need hard-shelled food, so a steady supply of small snails is part of routine care. That feeding regime does not fit a betta&rsquo;s needs, and a tank stocked with snails for one fish gives the other a permanent source of competition and mess.</p>"
    ),
    "green-terror-cichlid-and-senegal-bichir": (
        "Why the Bottom of the Tank Is the Problem",
        "<p>These two are often proposed together because they are similar in size and both are sold as tough fish. Adult length is not the constraint. Both occupy the same part of the tank, and only one of them defends it.</p>"
        "<p>The cichlid claims and patrols the substrate, and it does so continuously rather than in response to a specific intruder. The bichir is a slow, nocturnal, scent-driven feeder that has no way to answer that pressure &mdash; it cannot outswim a patrolling cichlid, and it will not compete for food dropped in open water. In practice the bottom-dweller stops feeding properly, which is easy to miss because it feeds at night in the first place.</p>"
        "<p>Spawning is when the arrangement breaks outright. A paired cichlid claims a territory measured in feet, not inches, and drives everything else out of it. In a tank that has one floor, there is nowhere for the displaced fish to go, and its armoured scales prevent obvious injury while damage accumulates around the eyes and fins.</p>"
        "<p>If both fish are already owned, a very long tank of 125 gallons or more with separate caves at each end, night-time target feeding, and a divider ready before breeding season is the minimum that makes the attempt defensible.</p>"
    ),
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


def replace_once(text: str, pattern: str, replacement, label: str) -> str:
    result, count = re.subn(pattern, replacement, text, count=1, flags=re.S | re.I)
    if count != 1:
        raise ValueError(f"Expected one {label} replacement, found {count}")
    return result


def faq_items(a: str, b: str, kind: str, risk: str, action: str) -> list[tuple[str, str]]:
    if kind == "compatible":
        return [
            (f"Can {a} live with {b} long term?", VERDICTS[kind]),
            (f"What is worth watching with {a} and {b}?", risk),
            (f"What tank setup helps {a} and {b} coexist?", action),
            (f"When should {a} and {b} be separated?", "Separate them if aggression, repeated food competition, injury, or declining water quality appears."),
        ]
    if kind == "caution":
        return [
            (f"Can {a} live with {b}?", VERDICTS[kind]),
            (f"What is the main risk with {a} and {b}?", risk),
            (f"What setup reduces conflict between {a} and {b}?", action),
            (f"When should I avoid keeping {a} and {b} together?", "Avoid the pairing in a small tank, with incomplete social groups, or when either species shows persistent stress or aggression."),
        ]
    return [
        (f"Can {a} live with {b}?", VERDICTS[kind]),
        (f"What is the biggest risk for {a} and {b}?", risk),
        (f"Would a larger tank make {a} and {b} compatible?", "More space can reduce some conflict, but it cannot solve incompatible water type, temperature, predation, or core welfare needs."),
        (f"What is a safer alternative to keeping {a} and {b} together?", action),
    ]


def faq_html(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f"<details><summary>{html.escape(question)}</summary><p>{html.escape(answer)}</p></details>"
        for question, answer in items
    )


def faq_jsonld(items: list[tuple[str, str]]) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return json.dumps(payload, ensure_ascii=False)


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
    text = replace_once(text, r'(<meta name="description" content=").*?("\s*/?>)', rf'\g<1>{html.escape(description, quote=True)}\2', "description")
    text = replace_once(text, r'(<meta property="og:title" content=").*?("\s*/?>)', rf'\g<1>{html.escape(title, quote=True)}\2', "Open Graph title")
    text = replace_once(text, r'(<meta property="og:description" content=").*?("\s*/?>)', rf'\g<1>{html.escape(description, quote=True)}\2', "Open Graph description")
    text = replace_once(text, r'("@type": "Article", "headline": ").*?("\s*,\s*"description": ").*?("\s*,\s*"datePublished")', rf'\g<1>{html.escape(title, quote=True)}\2{html.escape(description, quote=True)}\3', "Article schema")
    text = replace_once(text, r"<h1>.*?</h1>", f"<h1>{html.escape(question)}</h1>", "H1")
    text = replace_once(text, r"<div class=\"card\">\s*<h2>(?:Compatibility Overview|Can .*? Live Together\?)</h2>\s*<p>.*?</p>", f'<div class="card"><h2>{html.escape(question)}</h2><p>{html.escape(overview)}</p>', "overview")
    items = faq_items(a, b, kind, risk, action)
    text = replace_once(text, r"(<div class=\"card faq\">\s*<h2>Frequently Asked Questions</h2>).*?(</div>\s*<div class=\"card\">\s*<h2>Related Compatibility Guides</h2>)", rf"\1\n{faq_html(items)}\n\2", "FAQ")
    # The FAQPage block had drifted away from the questions actually on the page,
    # which breaks Google's requirement that schema match visible content.
    # Not every pair page ships a FAQPage block, so sync it only where one exists.
    text, _ = re.subn(
        r'(<script type="application/ld\+json">)\{"@context": "https://schema\.org", "@type": "FAQPage".*?\}(</script>)',
        lambda m: m.group(1) + faq_jsonld(items) + m.group(2),
        text,
        count=1,
        flags=re.S,
    )
    detail = PILOT_DETAIL.get(path.parent.name)
    if detail:
        heading, body = detail
        risk_section += f'<div class="card"><h2>{html.escape(heading)}</h2>{body}</div>'

    detail_headings = {heading for heading, _ in PILOT_DETAIL.values()}
    # Re-runs must consume the previously inserted detail card too, or each run
    # would append another copy of it.
    existing_risks = (
        r'<div class="card"><h2>(?:' + "|".join(re.escape(label) for label in PROFILE_LABELS.values())
        + r')</h2><p>.*?</p></div><div class="card"><h2>A Safer Plan for .*?</h2><p>.*?</p></div>'
        + r'(?:<div class="card"><h2>(?:' + "|".join(re.escape(h) for h in detail_headings) + r')</h2>.*?</div>)?'
        + r'\s*'
    )
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
