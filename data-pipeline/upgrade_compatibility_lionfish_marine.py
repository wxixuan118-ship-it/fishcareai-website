"""Upgrade the three lionfish marine pair pages that Google discovered but never indexed.

GSC's 2026-11-01 "Discovered - currently not indexed" export listed three marine pairs
(/compatibility/lionfish-and-{percula-clownfish,watchman-goby,yellow-tang}/). An on-page
audit scored all three at 91.4: ~550 words, and the pair phrase repeated nine times for a
keyword density of 5.8-6.4%, well over the 3% ceiling.

Two faults are fixed here:

  * The shared template is freshwater copy. It tells the reader to keep a lionfish tank
    "heavily planted" with "dense planting" - advice that does not apply to a FOWLR
    system and reads as machine-written to anyone who keeps marine fish.
  * The pair name is repeated in running prose where a pronoun does the same work.

Each page also gains a "What actually decides it" section with the predation arithmetic
for that specific pair, which is the question a reader has and the template never answers.

The v2 generator cannot be re-run (see upgrade_compatibility_onpage.py for why), so this
patches the rendered HTML. Every edit is keyed on the old markup and skipped when the new
markup is already present, so the script is safe to re-run.

Run: python3 data-pipeline/upgrade_compatibility_lionfish_marine.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The template sentence, identical on all three pages apart from the partner name.
OLD_AGGRO = ("Lionfish is aggressive and {p} is {t}. Expect chasing and fin damage unless "
             "the tank is oversized, heavily planted, and watched closely.")
NEW_AGGRO = ("Lionfish is aggressive and {p} is {t}. A lionfish does not chase - it waits, "
             "so the risk is a single strike rather than ongoing harassment.")

PAIRS = {
    "lionfish-and-percula-clownfish": {
        "partner": "Percula Clownfish",
        "temperament": "semi",
        "overview": (
            "A volitans lionfish reaches 15 inches and swallows prey whole. A percula clownfish "
            "tops out near 3 inches. That size gap is the whole story, and no amount of rockwork "
            "closes it."
        ),
        "verdict_title": "What Actually Decides It: Gape Size",
        "verdict": [
            "A lionfish feeds by engulfing: it drifts within range, flares its pectorals and inhales. "
            "Anything that fits in the mouth is food, and the mouth of an adult <em>Pterois volitans</em> "
            "opens wider than a percula clownfish is deep. The clownfish does not need to be caught in "
            "the open &mdash; lionfish hunt at dusk and dawn, and a clownfish asleep in its host anemone "
            "is an easier target than a moving one.",
            "Keepers do report the pairing working, almost always in one of two situations: the lionfish "
            "is a juvenile and has not grown into its gape yet, or the clownfish is a large adult of a "
            "bigger species such as a maroon. Neither describes a percula. The usual outcome is months "
            "of apparent success followed by an empty tank one morning.",
            "If you want anemonefish and a lionfish in the same system, the answer is two tanks. If the "
            "lionfish is already in place, a dwarf fuzzy (<em>Dendrochirus brachypterus</em>) has a much "
            "smaller gape and is the species people actually get away with alongside clownfish &mdash; "
            "though it is still a predator, not a community fish.",
        ],
    },
    "lionfish-and-watchman-goby": {
        "partner": "Watchman Goby",
        "temperament": "peaceful",
        "overview": (
            "A watchman goby spends its life hovering at the entrance of a burrow in open sand. "
            "That is precisely where an ambush predator looks, and at 3 to 4 inches the goby is "
            "well inside a lionfish's gape."
        ),
        "verdict_title": "What Actually Decides It: Where the Goby Sits",
        "verdict": [
            "The yellow watchman and its relatives are burrow fish. They perch at the mouth of a hole "
            "in open substrate, propped on their pectorals, and dart in when something approaches. That "
            "behaviour works against a reef's usual predators, which chase. It does not work against a "
            "lionfish, which holds station a few inches away and waits for the goby to settle back out.",
            "The burrow is not the refuge it looks like either. A goby bolting into sand leaves a hole "
            "an adult lionfish can hover over, and the goby has to emerge to feed. Pistol shrimp pairings "
            "make this worse, not better: the shrimp keeps the burrow open and the goby out in the light.",
            "There is a second problem specific to this pairing. Lionfish readily eat ornamental shrimp, "
            "so the pistol shrimp half of a goby-shrimp partnership is also on the menu. If you want the "
            "symbiosis, the lionfish has to go in a different tank.",
        ],
    },
    "lionfish-and-yellow-tang": {
        "partner": "Yellow Tang",
        "temperament": "semi-aggressive",
        "overview": (
            "This is the one lionfish pairing on the list that is genuinely workable. An adult "
            "yellow tang is 8 inches of deep-bodied, fast-moving fish &mdash; too large to swallow "
            "and too quick to ambush."
        ),
        "verdict_title": "What Actually Decides It: Introduce the Tang Full-Grown",
        "verdict": [
            "Body depth is what saves the tang. A lionfish judges prey by whether it will fit, and a "
            "mature <em>Zebrasoma flavescens</em> is a disc rather than a torpedo &mdash; far deeper than "
            "its 8-inch length suggests. Add a tang at full size and the lionfish loses interest within "
            "days. Add a 2-inch juvenile and you have bought an expensive meal.",
            "The real friction is husbandry, not aggression. Lionfish are messy carnivores that produce a "
            "heavy nitrogenous load, and yellow tangs are among the more ich-prone fish in the trade and "
            "want clean, well-oxygenated water with strong flow. The two demands pull in opposite "
            "directions, which is why 100 gallons is a floor rather than a target: 125 gallons and "
            "oversized skimming make this pairing far easier to keep stable.",
            "Two practical notes. Copper-based ich treatment is risky in a tank holding invertebrates and "
            "awkward around a scaleless-skinned predator, so quarantine the tang properly rather than "
            "planning to treat in the display. And give the tang open water on one side &mdash; it grazes "
            "all day and needs room that is not in the lionfish's strike line.",
        ],
    },
}


def build_section(cfg: dict) -> str:
    paras = "\n      ".join(f"<p>{p}</p>" for p in cfg["verdict"])
    return (f'\n    <div class="card">\n'
            f'      <h2>{cfg["verdict_title"]}</h2>\n'
            f'      {paras}\n'
            f'    </div>\n')


def upgrade(slug: str, cfg: dict, dry_run: bool) -> str:
    path = ROOT / "compatibility" / slug / "index.html"
    if not path.exists():
        return f"  {slug}: MISSING"
    html = path.read_text(encoding="utf-8")
    before = html
    notes = []

    old = OLD_AGGRO.format(p=cfg["partner"], t=cfg["temperament"].split("-")[0])
    new = NEW_AGGRO.format(p=cfg["partner"], t=cfg["temperament"].split("-")[0])
    if old in html:
        html = html.replace(old, new)
        notes.append(f"planted-tank copy x{before.count(old)}")

    # Overview paragraph. The template ships two variants: a "can potentially coexist" tail
    # that recommends dense planting, and a "not recommended" tail. Replace whichever is
    # present with a sentence about this specific pair.
    tails = (" A larger tank (minimum 100 gallons), dense planting, and close monitoring are essential.",
             " Review the behavior and water details before deciding whether to attempt the pairing.")
    for tail in tails:
        if tail in html:
            html = html.replace(tail, " " + cfg["overview"])
            notes.append("overview tail")
            break

    # Drop one redundant repeat of the pair name in the opening sentence of the overview.
    for opener, repl in (
        (f'<p>Lionfish and {cfg["partner"]} can potentially coexist, but',
         "<p>The two can potentially coexist, but"),
        (f'<p>Lionfish and {cfg["partner"]} are generally not recommended to be housed together.',
         "<p>The two are generally not recommended to be housed together."),
    ):
        if opener in html:
            html = html.replace(opener, repl)
            notes.append("opening repeat")
            break

    # The pair name is also repeated in boilerplate where it carries no search value:
    # the screen-reader table caption, the second species photo's alt, and two FAQ lines.
    pair = f'Lionfish and {cfg["partner"]}'
    for a, b in (
        (f'<caption class="sr-only">Compatibility factors for {pair}</caption>',
         '<caption class="sr-only">Compatibility factors at a glance</caption>'),
        (f'alt="{pair} compatibility &mdash; {cfg["partner"]}"',
         f'alt="{cfg["partner"]} in a marine aquarium"'),
        (f'alt="{pair} compatibility — {cfg["partner"]}"',
         f'alt="{cfg["partner"]} in a marine aquarium"'),
        (f'A minimum of 100 gallons is recommended for keeping {pair} together.',
         'A minimum of 100 gallons is recommended for keeping the two together.'),
        (f'<summary>What temperature suits both {pair}?</summary>',
         '<summary>What temperature suits both species?</summary>'),
    ):
        if a in html:
            html = html.replace(a, b)
            notes.append("boilerplate repeat")

    section = build_section(cfg)
    if cfg["verdict_title"] not in html:
        anchor = '\n\n\n    <div class="card faq">'
        if anchor not in html:
            return f"  {slug}: ANCHOR NOT FOUND - section not added"
        html = html.replace(anchor, section + "\n\n    <div class=\"card faq\">", 1)
        notes.append("verdict section")

    if html == before:
        return f"  {slug}: already up to date"
    if not dry_run:
        path.write_text(html, encoding="utf-8")
    return f"  {slug}: {', '.join(notes)}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print("Upgrading 3 lionfish marine pair pages" + (" (dry run)" if args.dry_run else ""))
    for slug, cfg in PAIRS.items():
        print(upgrade(slug, cfg, args.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
