"""
generate_compatibility_pages.py
────────────────────────────────
Generates /compatibility/{slug-a}-and-{slug-b}/index.html for all
C(N,2) pairs from the SPECIES dict, plus a /compatibility/index.html hub.

Compatibility score (0-100) is computed from real species data:
  • Temperature range overlap
  • pH range overlap
  • Temperament pairing
  • Size ratio (predator/prey risk)
  • Special rules (betta+guppy, oscar+small fish, etc.)

Run: python3 generate_compatibility_pages.py
"""

import os, json, math
from pathlib import Path
from itertools import combinations

REPO  = Path(__file__).parent.parent
OUT   = REPO / "compatibility"

# ── Species data ──────────────────────────────────────────────────────────────
# temp_min/max: °F  |  ph: pH units  |  size: adult inches
# temperament: peaceful / semi / aggressive
# water: freshwater / coldwater (goldfish/koi prefer cooler water)
# schooling: min group needed
# eats_small: True if this species will eat very small fish/shrimp

SPECIES = {
  "angelfish": {
    "name":"Angelfish","sci":"Pterophyllum scalare",
    "temp_min":74,"temp_max":84,"ph_min":6.0,"ph_max":7.5,
    "temperament":"semi","size":6,"care":"intermediate","water":"freshwater",
    "min_group":1,"diet":"omnivore","eats_small":True,
    "wiki":"/wiki/angelfish/",
    "desc":"Elegant South American cichlids with long flowing fins. Generally peaceful but territorial when breeding and will eat very small fish.",
  },
  "betta-fish": {
    "name":"Betta Fish","sci":"Betta splendens",
    "temp_min":76,"temp_max":82,"ph_min":6.5,"ph_max":7.5,
    "temperament":"aggressive","size":3,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"carnivore","eats_small":False,
    "wiki":"/wiki/betta-fish/",
    "desc":"Vibrant labyrinth fish from Southeast Asia. Males are highly territorial toward other bettas and fin-nippers; compatible with many peaceful species in large, planted tanks.",
    "special":["male_aggressive_to_male","triggers_on_long_fins"],
  },
  "bristlenose-pleco": {
    "name":"Bristlenose Pleco","sci":"Ancistrus sp.",
    "temp_min":60,"temp_max":80,"ph_min":6.5,"ph_max":7.5,
    "temperament":"peaceful","size":5,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"herbivore","eats_small":False,
    "wiki":"/wiki/bristlenose-pleco/",
    "desc":"Hardy armoured catfish that grazes on algae. Peaceful with virtually all species; tolerates a wide temperature range.",
  },
  "cardinal-tetra": {
    "name":"Cardinal Tetra","sci":"Paracheirodon axelrodi",
    "temp_min":73,"temp_max":82,"ph_min":4.5,"ph_max":7.0,
    "temperament":"peaceful","size":1.5,"care":"intermediate","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/cardinal-tetra/",
    "desc":"Brilliant red-and-blue schooling fish from the Rio Negro. Prefers soft, acidic, warm water — a natural companion for discus.",
  },
  "cherry-barb": {
    "name":"Cherry Barb","sci":"Puntius titteya",
    "temp_min":73,"temp_max":81,"ph_min":6.0,"ph_max":8.0,
    "temperament":"peaceful","size":2,"care":"beginner","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/cherry-barb/",
    "desc":"Unlike most barbs, cherry barbs are peaceful schooling fish safe with bettas and nano species. Males turn vivid red when in breeding condition.",
  },
  "cherry-shrimp": {
    "name":"Cherry Shrimp","sci":"Neocaridina davidi",
    "temp_min":65,"temp_max":80,"ph_min":6.5,"ph_max":8.0,
    "temperament":"peaceful","size":0.8,"care":"beginner","water":"freshwater",
    "min_group":10,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/cherry-shrimp/",
    "desc":"Bright red freshwater shrimp that are excellent algae cleaners. Very small — at risk from any fish large enough to eat them.",
    "special":["prey_for_large_fish"],
  },
  "chili-rasbora": {
    "name":"Chili Rasbora","sci":"Boraras brigittae",
    "temp_min":68,"temp_max":82,"ph_min":4.0,"ph_max":7.0,
    "temperament":"peaceful","size":0.8,"care":"intermediate","water":"freshwater",
    "min_group":8,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/chili-rasbora/",
    "desc":"Vivid red nano fish from Borneo blackwater habitats. Extremely small — only safe with fish too small to swallow them.",
    "special":["prey_for_large_fish"],
  },
  "clown-loach": {
    "name":"Clown Loach","sci":"Chromobotia macracanthus",
    "temp_min":77,"temp_max":86,"ph_min":6.0,"ph_max":7.5,
    "temperament":"peaceful","size":12,"care":"intermediate","water":"freshwater",
    "min_group":5,"diet":"omnivore","eats_small":True,
    "wiki":"/wiki/clown-loach/",
    "desc":"Striking striped loach that grows very large. Peaceful with fish but will eat shrimp, snails and tiny fish.",
    "special":["eats_snails","eats_shrimp"],
  },
  "corydoras": {
    "name":"Corydoras Catfish","sci":"Corydoras spp.",
    "temp_min":70,"temp_max":79,"ph_min":6.0,"ph_max":8.0,
    "temperament":"peaceful","size":2.5,"care":"beginner","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/corydoras/",
    "desc":"Armoured bottom-dwelling catfish that are peaceful with all non-aggressive species. Need fine sand substrate to protect delicate barbels.",
  },
  "discus": {
    "name":"Discus","sci":"Symphysodon spp.",
    "temp_min":82,"temp_max":88,"ph_min":5.0,"ph_max":7.0,
    "temperament":"semi","size":8,"care":"advanced","water":"freshwater",
    "min_group":5,"diet":"omnivore","eats_small":True,
    "wiki":"/wiki/discus/",
    "desc":"The 'king of the aquarium' — beautiful but demanding. Requires very warm, soft, acidic water that excludes most community fish.",
  },
  "dwarf-gourami": {
    "name":"Dwarf Gourami","sci":"Trichogaster lalius",
    "temp_min":72,"temp_max":82,"ph_min":6.0,"ph_max":7.5,
    "temperament":"semi","size":3.5,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/dwarf-gourami/",
    "desc":"Colourful labyrinth fish that is generally peaceful but can be territorial toward similar species. Susceptible to Dwarf Gourami Iridovirus.",
    "special":["risky_with_betta","risky_with_other_gouramis"],
  },
  "ember-tetra": {
    "name":"Ember Tetra","sci":"Hyphessobrycon amandae",
    "temp_min":73,"temp_max":84,"ph_min":5.5,"ph_max":7.0,
    "temperament":"peaceful","size":0.8,"care":"beginner","water":"freshwater",
    "min_group":8,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/ember-tetra/",
    "desc":"Tiny orange-red schooling tetra that is among the most adaptable nano fish. Peaceful with everything too small to eat them.",
    "special":["prey_for_large_fish"],
  },
  "guppy": {
    "name":"Guppy","sci":"Poecilia reticulata",
    "temp_min":72,"temp_max":82,"ph_min":6.8,"ph_max":8.5,
    "temperament":"peaceful","size":2.5,"care":"beginner","water":"freshwater",
    "min_group":3,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/guppy/",
    "desc":"Hardy and colourful livebearers. Males' long flowing tails make them targets for fin-nipping species. Very prolific breeders.",
    "special":["triggers_betta_aggression","fin_nipping_target"],
  },
  "goldfish": {
    "name":"Goldfish","sci":"Carassius auratus",
    "temp_min":50,"temp_max":74,"ph_min":6.5,"ph_max":8.0,
    "temperament":"peaceful","size":12,"care":"beginner","water":"coldwater",
    "min_group":1,"diet":"omnivore","eats_small":True,
    "wiki":"/wiki/goldfish/",
    "desc":"Classic pond and aquarium fish that prefer cool water. Heavy waste producers that require robust filtration. Will eat small fish and shrimp.",
    "special":["eats_small_fish","coldwater_only"],
  },
  "harlequin-rasbora": {
    "name":"Harlequin Rasbora","sci":"Trigonostigma heteromorpha",
    "temp_min":72,"temp_max":81,"ph_min":5.5,"ph_max":7.5,
    "temperament":"peaceful","size":1.75,"care":"beginner","water":"freshwater",
    "min_group":8,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/harlequin-rasbora/",
    "desc":"Active mid-level schooling fish with a distinctive black triangular patch. One of the best all-around community tank fish.",
  },
  "honey-gourami": {
    "name":"Honey Gourami","sci":"Trichogaster chuna",
    "temp_min":71,"temp_max":82,"ph_min":6.0,"ph_max":7.5,
    "temperament":"peaceful","size":2,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/honey-gourami/",
    "desc":"One of the most peaceful gouramis available. Not affected by Dwarf Gourami Iridovirus. Excellent nano community fish.",
  },
  "koi": {
    "name":"Koi","sci":"Cyprinus rubrofuscus",
    "temp_min":50,"temp_max":75,"ph_min":7.0,"ph_max":8.5,
    "temperament":"peaceful","size":24,"care":"intermediate","water":"coldwater",
    "min_group":2,"diet":"omnivore","eats_small":True,
    "wiki":"/wiki/koi/",
    "desc":"Large pond fish that require hundreds of gallons and cool water. Will eat any fish small enough to fit in their mouth.",
    "special":["pond_only","eats_small_fish"],
  },
  "kuhli-loach": {
    "name":"Kuhli Loach","sci":"Pangio kuhlii",
    "temp_min":73,"temp_max":82,"ph_min":5.5,"ph_max":7.0,
    "temperament":"peaceful","size":3.5,"care":"beginner","water":"freshwater",
    "min_group":3,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/kuhli-loach/",
    "desc":"Eel-like bottom dwellers that are peaceful with all non-aggressive fish. Nocturnal and reclusive; need caves and soft substrate.",
  },
  "molly": {
    "name":"Molly","sci":"Poecilia sphenops",
    "temp_min":72,"temp_max":82,"ph_min":7.5,"ph_max":8.5,
    "temperament":"peaceful","size":4,"care":"beginner","water":"freshwater",
    "min_group":3,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/molly/",
    "desc":"Hardy livebearers that prefer alkaline, hard water — sometimes slightly brackish. Prolific breeders; peaceful community fish.",
  },
  "mystery-snail": {
    "name":"Mystery Snail","sci":"Pomacea bridgesii",
    "temp_min":68,"temp_max":80,"ph_min":7.0,"ph_max":8.0,
    "temperament":"peaceful","size":2,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"herbivore","eats_small":False,
    "wiki":"/wiki/mystery-snail/",
    "desc":"Large, peaceful aquarium snails that graze on algae and detritus. Shell provides some protection but can be harassed by certain fish.",
    "special":["eaten_by_loaches","eaten_by_puffers"],
  },
  "neon-tetra": {
    "name":"Neon Tetra","sci":"Paracheirodon innesi",
    "temp_min":72,"temp_max":80,"ph_min":6.0,"ph_max":7.5,
    "temperament":"peaceful","size":1.5,"care":"beginner","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/neon-tetra/",
    "desc":"Iconic schooling fish with vivid electric-blue and red stripes. Hardy in captivity; suitable for most peaceful community setups.",
    "special":["prey_for_large_fish"],
  },
  "nerite-snail": {
    "name":"Nerite Snail","sci":"Nerita spp.",
    "temp_min":65,"temp_max":85,"ph_min":6.5,"ph_max":8.5,
    "temperament":"peaceful","size":1,"care":"beginner","water":"freshwater",
    "min_group":1,"diet":"herbivore","eats_small":False,
    "wiki":"/wiki/nerite-snail/",
    "desc":"Outstanding algae-eating snails that do not reproduce in freshwater. Extremely hardy and compatible with virtually all peaceful fish.",
    "special":["eaten_by_puffers"],
  },
  "otocinclus": {
    "name":"Otocinclus","sci":"Otocinclus spp.",
    "temp_min":72,"temp_max":82,"ph_min":6.0,"ph_max":7.5,
    "temperament":"peaceful","size":1.5,"care":"beginner","water":"freshwater",
    "min_group":4,"diet":"herbivore","eats_small":False,
    "wiki":"/wiki/otocinclus/",
    "desc":"Tiny algae-eating catfish that are peaceful with all species. Need established algae growth and biofilm; sensitive to ammonia.",
  },
  "oscar": {
    "name":"Oscar","sci":"Astronotus ocellatus",
    "temp_min":74,"temp_max":81,"ph_min":6.0,"ph_max":8.0,
    "temperament":"aggressive","size":14,"care":"intermediate","water":"freshwater",
    "min_group":1,"diet":"carnivore","eats_small":True,
    "wiki":"/wiki/oscar/",
    "desc":"Intelligent but aggressive cichlids that will eat any fish small enough to fit in their mouth. Require large tanks (75+ gallons) and robust tank mates.",
    "special":["eats_small_fish","eats_shrimp"],
  },
  "pea-puffer": {
    "name":"Pea Puffer","sci":"Carinotetraodon travancoricus",
    "temp_min":74,"temp_max":82,"ph_min":7.0,"ph_max":8.0,
    "temperament":"semi","size":1,"care":"intermediate","water":"freshwater",
    "min_group":1,"diet":"carnivore","eats_small":False,
    "wiki":"/wiki/pea-puffer/",
    "desc":"World's smallest pufferfish — intensely territorial and nippy despite tiny size. Will attack fins and eat shrimp and snails.",
    "special":["eats_snails","eats_shrimp","nippy","risky_with_long_fins"],
  },
  "platy": {
    "name":"Platy","sci":"Xiphophorus maculatus",
    "temp_min":65,"temp_max":80,"ph_min":7.0,"ph_max":8.5,
    "temperament":"peaceful","size":2.5,"care":"beginner","water":"freshwater",
    "min_group":3,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/platy/",
    "desc":"Hardy livebearers that are among the easiest fish to keep. Peaceful with virtually all community species. Prolific breeders.",
  },
  "pygmy-corydoras": {
    "name":"Pygmy Corydoras","sci":"Corydoras pygmaeus",
    "temp_min":72,"temp_max":79,"ph_min":6.0,"ph_max":7.5,
    "temperament":"peaceful","size":1,"care":"beginner","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/pygmy-corydoras/",
    "desc":"Tiny armoured catfish that school in open water as well as on the substrate. Peaceful with all non-aggressive species.",
    "special":["prey_for_large_fish"],
  },
  "rainbow-shark": {
    "name":"Rainbow Shark","sci":"Epalzeorhynchos frenatum",
    "temp_min":72,"temp_max":79,"ph_min":6.5,"ph_max":7.5,
    "temperament":"semi","size":6,"care":"intermediate","water":"freshwater",
    "min_group":1,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/rainbow-shark/",
    "desc":"Active bottom dweller that becomes territorial at maturity. One per tank; avoid other shark-like or bottom-dwelling species.",
    "special":["territorial_bottom","one_per_tank"],
  },
  "swordtail": {
    "name":"Swordtail","sci":"Xiphophorus hellerii",
    "temp_min":65,"temp_max":80,"ph_min":7.0,"ph_max":8.3,
    "temperament":"peaceful","size":5,"care":"beginner","water":"freshwater",
    "min_group":3,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/swordtail/",
    "desc":"Hardy livebearer with a distinctive elongated lower tail fin in males. Peaceful community fish that tolerate a wide temperature range.",
  },
  "tiger-barb": {
    "name":"Tiger Barb","sci":"Puntigrus tetrazona",
    "temp_min":68,"temp_max":79,"ph_min":6.0,"ph_max":8.0,
    "temperament":"semi","size":2.75,"care":"beginner","water":"freshwater",
    "min_group":6,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/tiger-barb/",
    "desc":"Striking striped barbs that are notorious fin-nippers. Must be kept in groups of 6+ to redirect aggression within the school. Incompatible with long-finned fish.",
    "special":["fin_nipper","risky_with_long_fins"],
  },
  "zebra-danio": {
    "name":"Zebra Danio","sci":"Danio rerio",
    "temp_min":64,"temp_max":82,"ph_min":6.5,"ph_max":8.0,
    "temperament":"peaceful","size":2,"care":"beginner","water":"freshwater",
    "min_group":5,"diet":"omnivore","eats_small":False,
    "wiki":"/wiki/zebra-danio/",
    "desc":"Extremely hardy, fast-moving schooling fish tolerant of a wide temperature range. Active top-to-mid swimmers compatible with most community fish.",
  },
}

# ── Compatibility rules ───────────────────────────────────────────────────────
SPECIAL_INCOMPATIBLE_PAIRS = [
    # (slug_a, slug_b, reason)
    ("betta-fish", "betta-fish", "Two male bettas will fight seriously; never house together."),
    ("betta-fish", "guppy",      "Male guppies' long fins reliably trigger betta aggression."),
    ("betta-fish", "dwarf-gourami", "Both are territorial labyrinth fish; conflict is likely."),
    ("discus",     "goldfish",   "Goldfish require cool water (50–74°F) incompatible with discus (82–88°F)."),
    ("discus",     "koi",        "Temperature and water type incompatible."),
    ("oscar",      "neon-tetra", "Oscars will eat neon tetras."),
    ("oscar",      "cardinal-tetra", "Oscars will eat cardinal tetras."),
    ("oscar",      "chili-rasbora",  "Oscars will eat chili rasboras."),
    ("oscar",      "ember-tetra",    "Oscars will eat ember tetras."),
    ("oscar",      "cherry-shrimp",  "Oscars will eat cherry shrimp."),
    ("oscar",      "guppy",          "Oscars will eat adult guppies."),
    ("oscar",      "pygmy-corydoras","Oscars will eat pygmy corydoras."),
    ("koi",        "neon-tetra",     "Koi will eat neon tetras."),
    ("koi",        "cherry-shrimp",  "Koi will eat cherry shrimp."),
    ("koi",        "chili-rasbora",  "Koi will eat chili rasboras."),
    ("pea-puffer", "cherry-shrimp",  "Pea puffers will eat cherry shrimp."),
    ("pea-puffer", "nerite-snail",   "Pea puffers will eat nerite snails."),
    ("pea-puffer", "mystery-snail",  "Pea puffers will eat mystery snails."),
    ("pea-puffer", "guppy",          "Pea puffers will aggressively nip guppy fins."),
    ("clown-loach","cherry-shrimp",  "Clown loaches will eat cherry shrimp."),
    ("clown-loach","mystery-snail",  "Clown loaches relentlessly hunt snails."),
    ("clown-loach","nerite-snail",   "Clown loaches eat snails."),
]

CAUTION_PAIRS = [
    ("betta-fish",  "tiger-barb",       "Tiger barbs may nip betta fins; keep tiger barbs in groups of 8+."),
    ("betta-fish",  "angelfish",        "Angelfish may nip betta fins; large size difference; monitor closely."),
    ("betta-fish",  "neon-tetra",       "Generally compatible but some bettas will chase neons; monitor."),
    ("betta-fish",  "cardinal-tetra",   "Generally compatible but individual betta temperament varies."),
    ("betta-fish",  "honey-gourami",    "Labyrinth fish rivalry possible; provide ample space."),
    ("tiger-barb",  "guppy",            "Tiger barbs will nip guppy tails relentlessly."),
    ("tiger-barb",  "betta-fish",       "Tiger barbs nip betta fins; caution required."),
    ("tiger-barb",  "angelfish",        "Tiger barbs may nip angelfish fins."),
    ("rainbow-shark","corydoras",       "Rainbow shark may bully bottom-dwelling corydoras."),
    ("rainbow-shark","kuhli-loach",     "Both occupy the bottom; rainbow shark may be territorial."),
    ("goldfish",    "neon-tetra",       "Temperature incompatibility: goldfish prefer 50–74°F; neons need 72–80°F."),
    ("goldfish",    "guppy",            "Temperature overlap is marginal; guppies prefer warmer water."),
    ("angelfish",   "neon-tetra",       "Angelfish sometimes eat neon tetras; risk depends on fish size and hunger."),
    ("angelfish",   "cherry-shrimp",    "Angelfish will eat adult cherry shrimp and all juveniles."),
    ("discus",      "neon-tetra",       "Temperature mismatch; discus need 82–88°F, neons prefer 72–80°F."),
    ("oscar",       "angelfish",        "Oscars may intimidate or attack angelfish; size difference matters."),
    ("clown-loach", "corydoras",        "Both occupy the bottom; monitor for competition but usually peaceful."),
]

def get_special_rule(slug_a, slug_b):
    """Return (incompatible, caution, note) for a pair."""
    pair = frozenset([slug_a, slug_b])
    for a, b, note in SPECIAL_INCOMPATIBLE_PAIRS:
        if frozenset([a, b]) == pair:
            return True, False, note
    for a, b, note in CAUTION_PAIRS:
        if frozenset([a, b]) == pair:
            return False, True, note
    return False, False, ""

def compute_compat(slug_a, slug_b):
    a, b = SPECIES[slug_a], SPECIES[slug_b]
    is_incompat, is_caution, special_note = get_special_rule(slug_a, slug_b)

    issues, positives = [], []

    # Water type
    if a["water"] != b["water"]:
        return {
            "score": 5,
            "verdict": "incompatible",
            "color": "#E74C3C",
            "issues": [f"{a['name']} requires {'cold' if a['water']=='coldwater' else 'tropical'} water; "
                       f"{b['name']} requires {'cold' if b['water']=='coldwater' else 'tropical'} water. These environments are incompatible."],
            "positives": [],
            "temp_overlap": None,
            "ph_overlap": None,
        }

    score = 100

    # Special incompatible rule
    if is_incompat:
        return {
            "score": 5,
            "verdict": "incompatible",
            "color": "#E74C3C",
            "issues": [special_note],
            "positives": [],
            "temp_overlap": None,
            "ph_overlap": None,
        }

    # Temperature overlap
    t_lo = max(a["temp_min"], b["temp_min"])
    t_hi = min(a["temp_max"], b["temp_max"])
    t_overlap = t_hi - t_lo
    if t_overlap >= 6:
        positives.append(f"Good temperature overlap: both species thrive at {t_lo}–{t_hi}°F.")
        temp_overlap_str = f"{t_lo}–{t_hi}°F"
    elif t_overlap >= 2:
        score -= 15
        issues.append(f"Narrow temperature overlap ({t_lo}–{t_hi}°F) — keeping the tank at exactly {t_lo+1}–{t_hi-1}°F is needed for both species.")
        temp_overlap_str = f"{t_lo}–{t_hi}°F (narrow)"
    elif t_overlap >= 0:
        score -= 25
        issues.append(f"Minimal temperature overlap ({t_lo}–{t_hi}°F) — difficult to satisfy both species simultaneously.")
        temp_overlap_str = f"{t_lo}°F only"
    else:
        score -= 45
        issues.append(f"Temperature ranges do not overlap: {a['name']} needs {a['temp_min']}–{a['temp_max']}°F; {b['name']} needs {b['temp_min']}–{b['temp_max']}°F.")
        temp_overlap_str = "No overlap"

    # pH overlap
    ph_lo = max(a["ph_min"], b["ph_min"])
    ph_hi = min(a["ph_max"], b["ph_max"])
    ph_overlap = ph_hi - ph_lo
    if ph_overlap >= 0.8:
        positives.append(f"pH ranges are compatible: workable range is {ph_lo:.1f}–{ph_hi:.1f}.")
        ph_overlap_str = f"{ph_lo:.1f}–{ph_hi:.1f}"
    elif ph_overlap >= 0.3:
        score -= 10
        issues.append(f"Limited pH overlap ({ph_lo:.1f}–{ph_hi:.1f}) — maintain pH carefully within this narrow window.")
        ph_overlap_str = f"{ph_lo:.1f}–{ph_hi:.1f} (narrow)"
    else:
        score -= 25
        issues.append(f"pH ranges barely or do not overlap: {a['name']} prefers {a['ph_min']}–{a['ph_max']}; {b['name']} prefers {b['ph_min']}–{b['ph_max']}.")
        ph_overlap_str = "Incompatible"

    # Temperament
    t_pair = tuple(sorted([a["temperament"], b["temperament"]]))
    TEMP_MATRIX = {
        ("peaceful","peaceful"): (0,  "Both species are peaceful — low aggression risk."),
        ("peaceful","semi"):     (-10,"Minor aggression possible from the semi-aggressive species; provide hiding spots."),
        ("peaceful","aggressive"):(-35,"Significant aggression risk from the aggressive species; large tank and dense planting required."),
        ("aggressive","aggressive"):(-50,"Both species are aggressive — serious conflict expected."),
        ("semi","semi"):         (-15,"Both species can show some aggression; monitor closely and provide ample territory."),
        ("aggressive","semi"):   (-35,"Aggression risk is high; the aggressive species may dominate or injure the other."),
    }
    t_key = t_pair if t_pair in TEMP_MATRIX else tuple(sorted([a["temperament"],b["temperament"]]))
    t_penalty, t_note = TEMP_MATRIX.get(t_key, (0,""))
    score += t_penalty
    if t_penalty < 0:
        issues.append(t_note)
    else:
        positives.append(t_note)

    # Size ratio
    bigger, smaller = max(a["size"], b["size"]), min(a["size"], b["size"])
    ratio = bigger / smaller if smaller > 0 else 10
    if ratio >= 5:
        score -= 30
        big_name = a["name"] if a["size"] >= b["size"] else b["name"]
        sm_name  = b["name"] if a["size"] >= b["size"] else a["name"]
        issues.append(f"Large size difference: {big_name} ({bigger} in) may predate on {sm_name} ({smaller} in).")
    elif ratio >= 3:
        score -= 15
        issues.append(f"Significant size difference ({bigger} in vs {smaller} in) — the larger species may out-compete for food or intimidate the smaller.")
    else:
        positives.append(f"Similar size range ({a['size']} in vs {b['size']} in) — no significant predation risk.")

    # Shrimp/snail prey check
    a_eats = a.get("eats_small") and b["size"] <= 1
    b_eats = b.get("eats_small") and a["size"] <= 1
    if a_eats or b_eats:
        score -= 25
        eater = a["name"] if a_eats else b["name"]
        prey  = b["name"] if a_eats else a["name"]
        issues.append(f"{eater} is likely to eat or harass {prey}.")

    # Special caution
    if is_caution and special_note:
        score -= 20
        issues.append(special_note)

    # Schooling
    a_school = a["min_group"] > 1
    b_school = b["min_group"] > 1
    if a_school and b_school:
        positives.append(f"Both species are schooling fish — keep {a['name']} in groups of {a['min_group']}+ and {b['name']} in groups of {b['min_group']}+.")
    elif a_school:
        positives.append(f"{a['name']} must be kept in groups of {a['min_group']}+.")
    elif b_school:
        positives.append(f"{b['name']} must be kept in groups of {b['min_group']}+.")

    score = max(0, min(100, score))

    if score >= 75:
        verdict, color = "compatible", "#27AE60"
    elif score >= 45:
        verdict, color = "caution", "#F39C12"
    else:
        verdict, color = "incompatible", "#E74C3C"

    return {
        "score": score,
        "verdict": verdict,
        "color": color,
        "issues": issues,
        "positives": positives,
        "temp_overlap": temp_overlap_str if t_overlap >= 0 else "No overlap",
        "ph_overlap": ph_overlap_str,
    }

# ── HTML template ─────────────────────────────────────────────────────────────
VERDICT_EMOJI = {"compatible": "✅", "caution": "⚠️", "incompatible": "❌"}
VERDICT_TEXT  = {"compatible": "Compatible", "caution": "Use Caution", "incompatible": "Not Compatible"}

CSS = """:root{--p:#1B5E8B;--pl:#2E84C0;--pd:#0F3D5E;--s:#2E9E7D;--bg:#F0F7FF;--tx:#1A2B3C;--mu:#5A7A94;--bd:#D0E4F0;--ok:#27AE60;--wn:#F39C12;--er:#E74C3C}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--p);text-decoration:none}
.con{max-width:1100px;margin:0 auto;padding:0 22px}
h1{font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:800;line-height:1.2}
h2{font-size:1.2rem;font-weight:700}
h3{font-size:1rem;font-weight:700}
p{margin-bottom:.85rem;color:var(--mu)}p:last-child{margin-bottom:0}
.nb{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid var(--bd);padding:0 22px;height:64px;display:flex;align-items:center;justify-content:space-between}
.brand img{height:36px;width:auto;display:block}
.nlinks{display:flex;gap:2px}.nl{padding:7px 13px;border-radius:8px;font-weight:500;font-size:.86rem;color:var(--mu);transition:all .15s}.nl:hover{color:var(--p);background:rgba(27,94,139,.07)}
.hero{background:linear-gradient(135deg,#051C2A,#0F3D5E,#1B5E8B);padding:52px 22px 44px;color:#fff}
.hero .con{max-width:1100px;margin:0 auto}
.breadcrumb{display:flex;gap:6px;font-size:.78rem;color:rgba(255,255,255,.55);margin-bottom:14px;flex-wrap:wrap}
.breadcrumb a{color:rgba(255,255,255,.7)}.breadcrumb a:hover{color:#fff}
.breadcrumb span{color:rgba(255,255,255,.35)}
.tag{display:inline-block;padding:3px 11px;border-radius:20px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;background:rgba(255,255,255,.15);color:rgba(255,255,255,.9);margin-bottom:10px}
.hero h1{color:#fff;margin-bottom:18px}
.verdict-chip{display:inline-flex;align-items:center;gap:8px;padding:8px 18px;border-radius:99px;font-size:.95rem;font-weight:700;color:#fff;margin-top:4px}
.score-row{display:flex;align-items:center;gap:14px;margin-top:14px;flex-wrap:wrap}
.score-ring{width:64px;height:64px;flex-shrink:0}
.score-bar-wrap{flex:1;min-width:160px}
.score-bar-bg{height:10px;border-radius:10px;background:rgba(255,255,255,.15);overflow:hidden}
.score-bar-fg{height:100%;border-radius:10px;transition:width .6s}
.score-label{font-size:.78rem;color:rgba(255,255,255,.65);margin-top:5px}
.layout{display:grid;grid-template-columns:1fr 280px;gap:28px;max-width:1100px;margin:32px auto 60px;padding:0 22px}
@media(max-width:860px){.layout{grid-template-columns:1fr}.sidebar{display:none}}
.card{background:#fff;border-radius:16px;border:1px solid var(--bd);padding:26px 28px;margin-bottom:20px;box-shadow:0 4px 16px rgba(27,94,139,.06)}
.card h2{color:var(--pd);margin-bottom:14px;padding-bottom:10px;border-bottom:1.5px solid var(--bd)}
.card p{font-size:.95rem;line-height:1.78}
.card ul{margin:8px 0 12px 18px}
.card li{font-size:.94rem;line-height:1.7;color:var(--mu);margin-bottom:5px}
.card strong{color:var(--tx)}
.cmp-table{width:100%;border-collapse:collapse;font-size:.86rem;margin:10px 0}
.cmp-table th{background:var(--p);color:#fff;padding:9px 13px;text-align:left}
.cmp-table td{padding:9px 13px;border-bottom:1px solid var(--bd);color:var(--mu);vertical-align:top}
.cmp-table tr:nth-child(even) td{background:#F8FAFE}
.cmp-table tr:last-child td{border-bottom:none}
.cmp-table td:first-child{font-weight:600;color:var(--tx);width:38%}
.ok{color:var(--ok)}.wn{color:var(--wn)}.er{color:var(--er)}
.point{display:flex;gap:10px;padding:9px 12px;border-radius:8px;margin-bottom:6px;font-size:.88rem}
.point-ok{background:rgba(39,174,96,.08);border:1px solid rgba(39,174,96,.2)}
.point-wn{background:rgba(243,156,18,.08);border:1px solid rgba(243,156,18,.2)}
.point-er{background:rgba(231,76,60,.08);border:1px solid rgba(231,76,60,.2)}
.point-icon{flex-shrink:0;font-size:1rem}
.guide-links{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:12px}
.guide-links a{background:#fff;border:1px solid var(--bd);border-radius:8px;padding:11px 14px;color:var(--tx);font-weight:700;font-size:.83rem;transition:border-color .15s}
.guide-links a:hover{border-color:var(--p);background:#F0F7FF}
@media(max-width:540px){.guide-links{grid-template-columns:1fr}}
.sidebar .card{padding:18px 20px;margin-bottom:16px}
.sidebar .card h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--pd);margin-bottom:10px}
.sidebar .card a{display:block;padding:5px 0;font-size:.82rem;color:var(--mu);border-bottom:1px solid var(--bd)}
.sidebar .card a:last-child{border-bottom:none}
.sidebar .card a:hover{color:var(--p)}
.faq details{border-bottom:1px solid var(--bd);padding:12px 0}
.faq details:last-child{border-bottom:none}
.faq summary{font-weight:600;font-size:.92rem;color:var(--tx);cursor:pointer;list-style:none;padding-right:20px;position:relative}
.faq summary::after{content:'﹢';position:absolute;right:0;color:var(--mu)}
.faq details[open] summary::after{content:'﹣'}
.faq details p{margin:8px 0 0;font-size:.88rem;line-height:1.72;color:var(--mu)}
.ft{background:#0F3D5E;padding:28px 22px;margin-top:40px;text-align:center}
.ftb{color:rgba(255,255,255,.4);font-size:.76rem}"""


def min_tank_size(a, b):
    """Estimate min tank size for the pair."""
    base = max(a.get("min_group",1), b.get("min_group",1))
    size_a = a["size"]
    size_b = b["size"]
    # rough rule: big_fish × 10 + schooling bonus
    needed = max(size_a, size_b) * 8
    if base > 1:
        needed += base * 3
    needed = max(needed, 10)
    # Round to sensible tank size
    for t in [5,10,15,20,29,30,40,55,75,100]:
        if t >= needed:
            return t
    return 100


def temp_verdict(a, b):
    lo = max(a["temp_min"], b["temp_min"])
    hi = min(a["temp_max"], b["temp_max"])
    if hi - lo >= 4:
        return f"✅ {lo}–{hi}°F", "ok"
    elif hi - lo >= 0:
        return f"⚠️ {lo}–{hi}°F (narrow)", "wn"
    else:
        return "❌ No overlap", "er"


def ph_verdict(a, b):
    lo = max(a["ph_min"], b["ph_min"])
    hi = min(a["ph_max"], b["ph_max"])
    if hi - lo >= 0.8:
        return f"✅ {lo:.1f}–{hi:.1f}", "ok"
    elif hi - lo >= 0:
        return f"⚠️ {lo:.1f}–{hi:.1f} (narrow)", "wn"
    else:
        return "❌ No overlap", "er"


def make_page(slug_a, slug_b):
    a, b = SPECIES[slug_a], SPECIES[slug_b]
    compat = compute_compat(slug_a, slug_b)
    verdict = compat["verdict"]
    score   = compat["score"]
    color   = compat["color"]
    v_emoji = VERDICT_EMOJI[verdict]
    v_text  = VERDICT_TEXT[verdict]

    min_tank = min_tank_size(a, b)
    tv, tv_cls = temp_verdict(a, b)
    pv, pv_cls = ph_verdict(a, b)

    size_ratio = max(a["size"],b["size"]) / min(a["size"],b["size"]) if min(a["size"],b["size"])>0 else 1
    size_v = "✅ Similar" if size_ratio < 2 else (f"⚠️ {size_ratio:.1f}× difference" if size_ratio < 4 else f"❌ {size_ratio:.0f}× difference")
    size_cls = "ok" if size_ratio<2 else ("wn" if size_ratio<4 else "er")

    temp_v = "✅ Compatible" if a["temperament"]==b["temperament"]=="peaceful" else (
             "⚠️ Monitor" if "aggressive" not in [a["temperament"],b["temperament"]] else "❌ Risk")
    temp_cls = "ok" if temp_v.startswith("✅") else ("wn" if temp_v.startswith("⚠️") else "er")

    positives_html = "".join(
        f'<div class="point point-ok"><span class="point-icon">✅</span><span>{p}</span></div>'
        for p in compat["positives"]
    ) or '<div class="point point-ok"><span class="point-icon">✅</span><span>No specific synergy notes; compatibility is primarily water-parameter based.</span></div>'

    issues_html = "".join(
        f'<div class="point point-{"er" if verdict=="incompatible" else "wn"}"><span class="point-icon">{"❌" if verdict=="incompatible" else "⚠️"}</span><span>{i}</span></div>'
        for i in compat["issues"]
    ) or '<div class="point point-ok"><span class="point-icon">✅</span><span>No major compatibility issues identified for this pair.</span></div>'

    # Verdict paragraph
    if verdict == "compatible":
        verdict_para = (
            f"{a['name']} and {b['name']} can generally share an aquarium with appropriate planning. "
            f"Both species prefer overlapping temperature and pH ranges, and neither poses a major aggression risk to the other. "
            f"A minimum {min_tank}-gallon tank is recommended to provide adequate territory and water volume for both species."
        )
    elif verdict == "caution":
        verdict_para = (
            f"{a['name']} and {b['name']} can potentially coexist, but the combination requires careful attention. "
            f"Some combination of water parameter differences, size mismatch, or temperament issues make this pair challenging. "
            f"A larger tank (minimum {min_tank} gallons), dense planting, and close monitoring are essential."
        )
    else:
        verdict_para = (
            f"{a['name']} and {b['name']} are generally not recommended to be housed together. "
            f"The issues listed above — whether water parameter incompatibility, predation risk, or aggression — "
            f"create conditions where one or both fish are likely to suffer harm or chronic stress."
        )

    # FAQs
    faqs = [
        (f"Can {a['name']} live with {b['name']}?",
         f"{'Yes, in a well-planned setup.' if verdict=='compatible' else ('With significant caution and a larger tank.' if verdict=='caution' else 'Generally not recommended.')} {verdict_para}"),
        (f"What tank size do I need for {a['name']} and {b['name']} together?",
         f"A minimum of {min_tank} gallons is recommended for keeping {a['name']} and {b['name']} together. A larger tank improves water stability and reduces territorial conflict."),
        (f"What temperature suits both {a['name']} and {b['name']}?",
         tv.replace("✅ ","").replace("⚠️ ","").replace("❌ ","")),
        (f"Is a {a['name']} aggressive toward a {b['name']}?",
         f"{a['name']} is {a['temperament']} and {b['name']} is {b['temperament']}. {compat['issues'][0] if compat['issues'] else 'No major aggression issues are expected between these species.'}"),
    ]

    faqs_html = "\n".join(
        f"<details><summary>{q}</summary><p>{ans}</p></details>"
        for q, ans in faqs
    )

    faq_json_entities = json.dumps([
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q, a in faqs
    ], ensure_ascii=False)

    canon = f"https://www.fishcareai.com/compatibility/{slug_a}-and-{slug_b}/"
    title = f"Can {a['name']} Live With {b['name']}? Compatibility Guide | FishCare AI"
    meta_desc = (f"{v_emoji} {v_text}: {a['name']} and {b['name']} compatibility — "
                 f"temperature, pH, aggression risk, tank size, and verdict for keeping them together.")

    breadcrumb_json = json.dumps({
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},
            {"@type":"ListItem","position":2,"name":"Compatibility","item":"https://www.fishcareai.com/compatibility/"},
            {"@type":"ListItem","position":3,"name":f"{a['name']} & {b['name']}","item":canon},
        ]
    })

    article_json = json.dumps({
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":meta_desc,
        "datePublished":"2026-08-15","dateModified":"2026-08-15",
        "author":{"@type":"Organization","name":"FishCare AI Editorial Team"},
        "publisher":{"@type":"Organization","name":"FishCare AI","url":"https://www.fishcareai.com"}
    })

    faq_schema = json.dumps({
        "@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":json.loads(faq_json_entities)
    })

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{meta_desc}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{meta_desc}"/>
<meta property="og:url" content="{canon}"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{faq_schema}</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260815-compat"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/guides/">Guides</a>
    <a class="nl" href="/wiki/">Encyclopedia</a>
    <a class="nl act" href="/compatibility/">Compatibility</a>
    <a class="nl" href="/#tools">Tools</a>
  </div>
</nav>

<header class="hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="/compatibility/">Compatibility</a><span>/</span>
      <span>{a['name']} &amp; {b['name']}</span>
    </div>
    <div class="tag">🐠 Fish Compatibility Guide</div>
    <h1>Can {a['name']} Live With {b['name']}?</h1>
    <div class="verdict-chip" style="background:{color}">{v_emoji} {v_text} — Compatibility Score: {score}/100</div>
    <div class="score-row">
      <div class="score-bar-wrap">
        <div class="score-bar-bg"><div class="score-bar-fg" style="width:{score}%;background:{color}"></div></div>
        <div class="score-label">{score}/100 — {v_text}</div>
      </div>
    </div>
  </div>
</header>

<div class="layout">
  <main>
    <div class="card">
      <h2>Compatibility Overview</h2>
      <p>{verdict_para}</p>
      <table class="cmp-table">
        <tr><th>Factor</th><th>{a['name']}</th><th>{b['name']}</th><th>Verdict</th></tr>
        <tr><td>Temperature</td><td>{a['temp_min']}–{a['temp_max']}°F</td><td>{b['temp_min']}–{b['temp_max']}°F</td><td class="{tv_cls}">{tv}</td></tr>
        <tr><td>pH Range</td><td>{a['ph_min']}–{a['ph_max']}</td><td>{b['ph_min']}–{b['ph_max']}</td><td class="{pv_cls}">{pv}</td></tr>
        <tr><td>Temperament</td><td style="text-transform:capitalize">{a['temperament']}</td><td style="text-transform:capitalize">{b['temperament']}</td><td class="{temp_cls}">{temp_v}</td></tr>
        <tr><td>Adult Size</td><td>{a['size']} in</td><td>{b['size']} in</td><td class="{size_cls}">{size_v}</td></tr>
        <tr><td>Min. Group</td><td>{a['min_group']}+</td><td>{b['min_group']}+</td><td>See below</td></tr>
        <tr><td>Min. Tank Size</td><td colspan="2" style="text-align:center">{min_tank} gallons (for both species)</td><td>—</td></tr>
      </table>
    </div>

    <div class="card">
      <h2>✅ Compatibility Positives</h2>
      {positives_html}
    </div>

    <div class="card">
      <h2>{'⚠️ Caution Points' if verdict!='incompatible' else '❌ Incompatibility Reasons'}</h2>
      {issues_html}
    </div>

    <div class="card">
      <h2>Species Profiles</h2>
      <h3>{a['name']} — <em>{a['sci']}</em></h3>
      <p>{a['desc']}</p>
      <p><a href="{a['wiki']}">→ Full {a['name']} care guide</a></p>
      <h3 style="margin-top:18px">{b['name']} — <em>{b['sci']}</em></h3>
      <p>{b['desc']}</p>
      <p><a href="{b['wiki']}">→ Full {b['name']} care guide</a></p>
    </div>

    <div class="card faq">
      <h2>Frequently Asked Questions</h2>
      {faqs_html}
    </div>

    <div class="card">
      <h2>Related Compatibility Guides</h2>
      <div class="guide-links">
        <a href="{a['wiki']}">📖 {a['name']} Encyclopedia</a>
        <a href="{b['wiki']}">📖 {b['name']} Encyclopedia</a>
        <a href="/compatibility/">🔄 All Compatibility Guides</a>
        <a href="/tools/fish-compatibility-checker/">🛠️ Compatibility Checker Tool</a>
        <a href="/guides/">📋 Fish Care Guides</a>
        <a href="/tools/water-parameter-checker/">💧 Water Parameter Checker</a>
      </div>
    </div>
  </main>

  <aside class="sidebar">
    <div class="card">
      <h3>Quick Facts</h3>
      <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Verdict</td><td style="padding:5px 0;font-weight:700;color:{color};border-bottom:1px solid var(--bd);text-align:right">{v_emoji} {v_text}</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Score</td><td style="padding:5px 0;font-weight:700;border-bottom:1px solid var(--bd);text-align:right">{score}/100</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Min. Tank</td><td style="padding:5px 0;font-weight:700;border-bottom:1px solid var(--bd);text-align:right">{min_tank} gal</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu)">Temp. Overlap</td><td style="padding:5px 0;font-weight:700;text-align:right">{tv.split(' ',1)[-1].split(' (')[0]}</td></tr>
      </table>
    </div>
    <div class="card">
      <h3>{a['name']} Guides</h3>
      <a href="{a['wiki']}">Species Profile</a>
      {'<a href="/guides/betta-fish-care/">Care Guide</a><a href="/guides/betta-fish-care/tank-mates/">Tank Mates</a><a href="/calculators/betta-fish-tank-size/">Tank Size Calculator</a>' if slug_a=='betta-fish' else ''}
      {'<a href="/guides/betta-fish-care/">Care Guide</a><a href="/guides/betta-fish-care/tank-mates/">Tank Mates</a><a href="/calculators/betta-fish-tank-size/">Tank Size Calculator</a>' if slug_b=='betta-fish' else ''}
    </div>
    <div class="card">
      <h3>Tools</h3>
      <a href="/tools/fish-compatibility-checker/">Compatibility Checker</a>
      <a href="/tools/water-parameter-checker/">Water Checker</a>
      <a href="/tools/tank-size-calculator/">Tank Size Calculator</a>
    </div>
  </aside>
</div>

<footer class="ft">
  <div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div>
  <nav class="legal-links"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


def make_index(all_pairs):
    """Generate /compatibility/index.html hub page."""
    # Group by first species
    by_species = {}
    for sa, sb in all_pairs:
        by_species.setdefault(sa, []).append(sb)

    # Count verdict categories
    verdicts = {}
    for sa, sb in all_pairs:
        c = compute_compat(sa, sb)
        verdicts[(sa,sb)] = c["verdict"]

    n_compat  = sum(1 for v in verdicts.values() if v=="compatible")
    n_caution = sum(1 for v in verdicts.values() if v=="caution")
    n_incompat= sum(1 for v in verdicts.values() if v=="incompatible")

    # Featured pairs (high-value for SEO)
    featured = [
        ("betta-fish","neon-tetra"),("betta-fish","guppy"),
        ("betta-fish","cherry-shrimp"),("betta-fish","corydoras"),
        ("betta-fish","angelfish"),("betta-fish","tiger-barb"),
        ("goldfish","neon-tetra"),("oscar","angelfish"),
        ("neon-tetra","cardinal-tetra"),("discus","cardinal-tetra"),
        ("guppy","platy"),("molly","swordtail"),
    ]

    featured_html = ""
    for sa, sb in featured:
        if sa in SPECIES and sb in SPECIES:
            c = compute_compat(sa, sb)
            v = c["verdict"]
            col = c["color"]
            em  = VERDICT_EMOJI[v]
            slug = f"{sa}-and-{sb}"
            featured_html += (
                f'<a href="/compatibility/{slug}/" style="display:flex;align-items:center;justify-content:space-between;'
                f'background:#fff;border:1px solid var(--bd);border-radius:10px;padding:13px 16px;'
                f'color:var(--tx);font-weight:600;font-size:.88rem;transition:border-color .15s;text-decoration:none">'
                f'<span>{SPECIES[sa]["name"]} + {SPECIES[sb]["name"]}</span>'
                f'<span style="color:{col};font-size:.82rem;font-weight:700">{em} {VERDICT_TEXT[v]}</span></a>\n'
            )

    # All species list links
    species_html = "".join(
        f'<a href="/compatibility/{slug}-and-{list(by_species.get(slug,[]))[0] if by_species.get(slug) else slug}/" '
        f'style="display:block;background:#fff;border:1px solid var(--bd);border-radius:8px;padding:8px 12px;'
        f'font-size:.84rem;font-weight:600;color:var(--tx);margin-bottom:6px;transition:border-color .15s">'
        f'🐠 {SPECIES[slug]["name"]}</a>'
        for slug in sorted(SPECIES.keys())
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Fish Compatibility Guides 2026: Can These Fish Live Together? | FishCare AI</title>
<meta name="description" content="Browse {len(all_pairs)} fish compatibility guides. Find out if betta fish, neon tetras, goldfish, guppies and 30+ species can share an aquarium — with scores, tank size and verdict."/>
<meta name="robots" content="index,follow"/>
<link rel="canonical" href="https://www.fishcareai.com/compatibility/"/>
<style>{CSS}
.hero{{background:linear-gradient(135deg,#051C2A,#0F3D5E,#1B5E8B);padding:60px 22px;color:#fff;text-align:center}}
.hero h1{{color:#fff;margin-bottom:12px}}
.hero p{{color:rgba(255,255,255,.75);max-width:560px;margin:0 auto 20px;font-size:1rem}}
.stats{{display:flex;gap:20px;justify-content:center;flex-wrap:wrap;margin-top:18px}}
.stat{{background:rgba(255,255,255,.12);border-radius:12px;padding:12px 22px;text-align:center}}
.stat .n{{font-size:1.8rem;font-weight:800;color:#fff}}
.stat .l{{font-size:.76rem;color:rgba(255,255,255,.65);margin-top:2px}}
.sec{{padding:52px 0}}
.sh{{text-align:center;margin-bottom:30px}}
.sh h2{{color:var(--pd);margin-bottom:8px;font-size:1.5rem}}
.sh p{{color:var(--mu);max-width:520px;margin:0 auto}}
.g2{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}
.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
@media(max-width:760px){{.g3,.g2{{grid-template-columns:1fr}}}}
</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260815-compat"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a><a class="nl" href="/guides/">Guides</a>
    <a class="nl" href="/wiki/">Encyclopedia</a>
    <a class="nl act" href="/compatibility/">Compatibility</a>
    <a class="nl" href="/#tools">Tools</a>
  </div>
</nav>

<header class="hero">
  <div class="tag">🐠 Fish Compatibility Database</div>
  <h1>Fish Compatibility Guides</h1>
  <p>Find out if your fish can safely share an aquarium — with compatibility scores, water parameter analysis, and expert verdicts for {len(all_pairs)} species pairs.</p>
  <div class="stats">
    <div class="stat"><div class="n ok">{n_compat}</div><div class="l">Compatible Pairs</div></div>
    <div class="stat"><div class="n wn">{n_caution}</div><div class="l">Caution Pairs</div></div>
    <div class="stat"><div class="n er">{n_incompat}</div><div class="l">Incompatible Pairs</div></div>
    <div class="stat"><div class="n" style="color:#fff">{len(SPECIES)}</div><div class="l">Species Covered</div></div>
  </div>
</header>

<section class="sec" style="background:#fff">
  <div class="con">
    <div class="sh"><h2>Most-Searched Compatibility Questions</h2><p>The most common "can X live with Y" questions answered with compatibility scores.</p></div>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:800px;margin:0 auto">
      {featured_html}
    </div>
  </div>
</section>

<section class="sec">
  <div class="con">
    <div class="sh"><h2>Browse by Species</h2><p>Select any species to see all its compatibility guides.</p></div>
    <div class="g3" style="max-width:760px;margin:0 auto">
      {species_html}
    </div>
  </div>
</section>

<section class="sec" style="background:#fff">
  <div class="con">
    <div class="sh"><h2>Use the Interactive Checker</h2><p>Want to check a custom combination? Use our free tool.</p></div>
    <div style="text-align:center">
      <a href="/tools/fish-compatibility-checker/" style="display:inline-flex;align-items:center;gap:8px;padding:13px 28px;background:var(--p);color:#fff;border-radius:10px;font-weight:700;font-size:.97rem">🛠️ Open Compatibility Checker</a>
    </div>
  </div>
</section>

<footer class="ft">
  <div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div>
  <nav class="legal-links"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


def main():
    slugs = sorted(SPECIES.keys())
    all_pairs = list(combinations(slugs, 2))

    print(f"Species: {len(slugs)}  |  Pairs: {len(all_pairs)}")

    # Generate individual pages
    ok = fail = 0
    for slug_a, slug_b in all_pairs:
        pair_slug = f"{slug_a}-and-{slug_b}"
        out_dir = OUT / pair_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            html = make_page(slug_a, slug_b)
            (out_dir / "index.html").write_text(html, encoding="utf-8")
            ok += 1
        except Exception as e:
            print(f"  ERROR {pair_slug}: {e}")
            fail += 1

    # Generate index page
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(make_index(all_pairs), encoding="utf-8")

    print(f"\nDone — {ok} pages generated, {fail} errors.")
    print(f"Hub:  /compatibility/index.html")
    print(f"Example: /compatibility/betta-fish-and-neon-tetra/")


if __name__ == "__main__":
    main()
