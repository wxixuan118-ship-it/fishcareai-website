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
# The enrichment output lives in the older working copy, not in this
# checkout; keep both candidates so the generator runs from either tree.
RAW_DATA = next(
    (path for path in (
        ROOT.parent / "data-pipeline" / "output" / "08_raw.json",
        ROOT.parent / "fishcare AI website" / "data-pipeline" / "output" / "08_raw.json",
        ROOT / "data-pipeline" / "output" / "08_raw.json",
    ) if path.exists()),
    ROOT.parent / "data-pipeline" / "output" / "08_raw.json",
)
SITEMAP = ROOT / "sitemap.xml"
TODAY = "2026-09-23"

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

# Verified replacements for the 60 v2 catalogue entries.
#
# The fields below used to be derived from `08_raw.json`, an LLM enrichment
# pass that was never fact-checked.  It published the rosy barb as a 2-inch
# 72-82°F fish that does not shoal; it is a 10 cm 16-24°C shoaler that wants a
# group of 8-10.  Errors of that shape fed every pair page's score, comparison
# table and tank-size advice, so the facts are pinned here instead.
#
# Freshwater figures are Seriously Fish species profiles (standard length,
# quick-facts temperature/pH, and the recommended aquarium volume for a group).
# Seriously Fish is freshwater-only; the marine entries and the five freshwater
# species it does not cover use standard hobby references.
#
# temperament/min_group/zone/eats_small are editorial calls made from each
# profile's "Behaviour and compatibility" section, not scraped strings.
V2_FACTS = {
    # slug: (sci, temp_min, temp_max, ph_min, ph_max, temperament, size_in,
    #        min_group, min_tank_gal, zone, eats_small, water)
    "african-butterfly-fish": ("Pantodon buchholzi", 73, 86, 6.0, 7.5, "semi", 4.7, 1, 21, "top", True, "freshwater"),
    "black-ghost-knifefish": ("Apteronotus albifrons", 73, 82, 6.0, 8.0, "semi", 18.0, 1, 100, "bottom", True, "freshwater"),
    "black-neon-tetra": ("Hyphessobrycon herbertaxelrodi", 68, 82, 5.0, 7.5, "peaceful", 1.4, 8, 19, "mid", False, "freshwater"),
    "black-phantom-tetra": ("Hyphessobrycon megalopterus", 68, 82, 5.0, 7.0, "peaceful", 1.4, 8, 19, "mid", False, "freshwater"),
    "black-ruby-barb": ("Pethia nigrofasciata", 68, 81, 5.5, 7.5, "peaceful", 2.2, 6, 19, "mid", False, "freshwater"),
    "bolivian-ram": ("Mikrogeophagus altispinosus", 75, 82, 6.0, 7.5, "semi", 3.1, 2, 48, "bottom", False, "freshwater"),
    "bosemans-rainbowfish": ("Melanotaenia boesemani", 81, 86, 7.0, 8.0, "peaceful", 4.3, 6, 29, "mid", False, "freshwater"),
    "clown-knifefish": ("Chitala ornata", 68, 82, 6.0, 8.0, "aggressive", 39.4, 1, 300, "mid", True, "freshwater"),
    "clown-pleco": ("Panaqolus maccus", 73, 82, 6.5, 7.8, "peaceful", 3.5, 1, 20, "bottom", False, "freshwater"),
    "congo-tetra": ("Phenacogrammus interruptus", 73, 82, 6.0, 7.5, "peaceful", 3.1, 6, 29, "mid", False, "freshwater"),
    "denison-barb": ("Sahyadria denisonii", 59, 77, 6.5, 7.8, "peaceful", 4.3, 6, 64, "mid", False, "freshwater"),
    "diamond-tetra": ("Moenkhausia pittieri", 75, 82, 5.5, 7.0, "peaceful", 2.4, 6, 18, "mid", False, "freshwater"),
    "dwarf-chain-loach": ("Ambastaia sidthimunki", 68, 86, 5.5, 7.5, "peaceful", 2.4, 6, 19, "bottom", False, "freshwater"),
    "electric-yellow-cichlid": ("Labidochromis caeruleus", 75, 82, 7.7, 8.6, "semi", 3.9, 4, 41, "mid", False, "freshwater"),
    "fire-eel": ("Mastacembelus erythrotaenia", 75, 82, 6.0, 7.0, "semi", 39.4, 1, 114, "bottom", True, "freshwater"),
    "frontosa-cichlid": ("Cyphotilapia frontosa", 73, 81, 8.0, 9.0, "semi", 10.0, 5, 228, "mid", True, "freshwater"),
    "giant-danio": ("Devario aequipinnatus", 72, 81, 6.5, 7.5, "semi", 4.0, 6, 30, "mid", False, "freshwater"),
    "glass-catfish": ("Kryptopterus vitreolus", 68, 79, 4.0, 7.0, "peaceful", 2.6, 6, 21, "mid", False, "freshwater"),
    "glowlight-danio": ("Danio choprae", 73, 79, 6.5, 7.5, "peaceful", 1.2, 8, 15, "mid", False, "freshwater"),
    "glowlight-tetra": ("Hemigrammus erythrozonus", 75, 82, 5.5, 7.5, "peaceful", 1.6, 6, 18, "mid", False, "freshwater"),
    "green-terror-cichlid": ("Andinoacara rivulatus", 68, 75, 6.5, 8.0, "aggressive", 11.8, 1, 80, "mid", True, "freshwater"),
    "hillstream-loach": ("Sewellia lineolata", 68, 75, 6.0, 7.5, "peaceful", 2.6, 4, 18, "bottom", False, "freshwater"),
    "jewel-cichlid": ("Hemichromis bimaculatus", 72, 82, 6.0, 7.8, "aggressive", 5.9, 2, 29, "mid", True, "freshwater"),
    "julii-cory": ("Corydoras julii", 68, 79, 5.5, 7.5, "peaceful", 2.2, 6, 21, "bottom", False, "freshwater"),
    "keyhole-cichlid": ("Cleithracara maronii", 70, 82, 4.0, 7.5, "peaceful", 4.3, 2, 21, "mid", False, "freshwater"),
    "lemon-tetra": ("Hyphessobrycon pulchripinnis", 68, 82, 5.0, 7.5, "peaceful", 1.6, 8, 19, "mid", False, "freshwater"),
    "moonlight-gourami": ("Trichopodus microlepis", 77, 86, 6.0, 7.5, "peaceful", 5.9, 1, 21, "top", False, "freshwater"),
    "neon-rainbowfish": ("Melanotaenia praecox", 73, 82, 6.8, 7.5, "peaceful", 3.1, 6, 14, "mid", False, "freshwater"),
    "panda-cory": ("Corydoras panda", 72, 77, 6.0, 7.4, "peaceful", 2.0, 6, 11, "bottom", False, "freshwater"),
    "peacock-cichlid": ("Aulonocara stuartgranti", 73, 84, 7.5, 9.0, "semi", 5.1, 4, 64, "mid", True, "freshwater"),
    "pearl-danio": ("Danio albolineatus", 72, 79, 6.5, 7.5, "peaceful", 2.5, 6, 20, "top", False, "freshwater"),
    "peppered-cory": ("Corydoras paleatus", 72, 79, 6.0, 7.0, "peaceful", 2.8, 6, 18, "bottom", False, "freshwater"),
    "red-eye-tetra": ("Moenkhausia sanctaefilomenae", 72, 79, 6.0, 8.0, "semi", 2.8, 6, 27, "mid", False, "freshwater"),
    "rosy-barb": ("Pethia conchonius", 61, 75, 6.0, 8.0, "peaceful", 3.9, 8, 24, "mid", False, "freshwater"),
    "senegal-bichir": ("Polypterus senegalus", 75, 82, 6.2, 7.8, "semi", 19.7, 1, 143, "bottom", True, "freshwater"),
    "serpae-tetra": ("Hyphessobrycon eques", 68, 82, 5.0, 7.5, "semi", 1.6, 10, 19, "mid", False, "freshwater"),
    "severum-cichlid": ("Heros efasciatus", 72, 84, 5.5, 7.0, "semi", 11.8, 1, 64, "mid", True, "freshwater"),
    "silver-arowana": ("Osteoglossum bicirrhosum", 68, 86, 5.0, 7.5, "aggressive", 31.5, 1, 250, "top", True, "freshwater"),
    "silver-dollar": ("Metynnis argenteus", 75, 82, 6.0, 7.0, "peaceful", 5.9, 5, 69, "mid", False, "freshwater"),
    "sparkling-gourami": ("Trichopsis pumila", 72, 82, 5.0, 7.5, "peaceful", 1.6, 4, 11, "mid", False, "freshwater"),
    "sterbai-cory": ("Corydoras sterbai", 75, 82, 6.0, 7.6, "peaceful", 2.6, 6, 11, "bottom", False, "freshwater"),
    "texas-cichlid": ("Herichthys cyanoguttatus", 68, 82, 6.0, 7.5, "aggressive", 11.8, 1, 125, "mid", True, "freshwater"),
    "threadfin-rainbowfish": ("Iriatherina werneri", 72, 86, 5.0, 8.0, "peaceful", 1.6, 6, 14, "mid", False, "freshwater"),
    "three-spot-gourami": ("Trichopodus trichopterus", 75, 86, 5.5, 8.5, "semi", 5.9, 1, 21, "top", False, "freshwater"),
    "weather-loach": ("Misgurnus anguillicaudatus", 50, 77, 6.0, 8.0, "peaceful", 11.0, 3, 64, "bottom", False, "freshwater"),
    "x-ray-tetra": ("Pristella maxillaris", 72, 82, 6.0, 7.5, "peaceful", 1.8, 6, 14, "mid", False, "freshwater"),
    "yoyo-loach": ("Botia almorhae", 66, 82, 6.0, 7.5, "semi", 6.3, 5, 64, "bottom", False, "freshwater"),
    "zebra-loach": ("Botia striata", 70, 79, 6.0, 7.5, "peaceful", 3.5, 5, 29, "bottom", False, "freshwater"),
    "zebra-pleco": ("Hypancistrus zebra", 79, 86, 6.0, 7.5, "semi", 3.1, 3, 14, "bottom", False, "freshwater"),
    # Marine — Seriously Fish does not cover these; figures are standard
    # reef-keeping references.  pH is the 8.1-8.4 reef band throughout.
    "blue-tang": ("Paracanthurus hepatus", 72, 82, 8.1, 8.4, "semi", 12.0, 1, 180, "mid", False, "saltwater"),
    "coral-beauty": ("Centropyge bispinosa", 72, 82, 8.1, 8.4, "peaceful", 4.0, 1, 55, "mid", False, "saltwater"),
    "firefish-goby": ("Nemateleotris magnifica", 72, 82, 8.1, 8.4, "peaceful", 3.0, 1, 20, "mid", False, "saltwater"),
    "flame-angelfish": ("Centropyge loricula", 72, 82, 8.1, 8.4, "semi", 4.0, 1, 55, "mid", False, "saltwater"),
    "foxface-rabbitfish": ("Siganus vulpinus", 72, 82, 8.1, 8.4, "peaceful", 9.0, 1, 125, "mid", False, "saltwater"),
    "lionfish": ("Pterois volitans", 72, 82, 8.1, 8.4, "aggressive", 15.0, 1, 120, "mid", True, "saltwater"),
    "pajama-cardinalfish": ("Sphaeramia nematoptera", 72, 82, 8.1, 8.4, "peaceful", 3.5, 3, 30, "mid", False, "saltwater"),
    "percula-clownfish": ("Amphiprion percula", 74, 82, 8.1, 8.4, "semi", 3.0, 2, 20, "mid", False, "saltwater"),
    "royal-gramma": ("Gramma loreto", 72, 82, 8.1, 8.4, "semi", 3.0, 1, 30, "mid", False, "saltwater"),
    "watchman-goby": ("Cryptocentrus cinctus", 72, 82, 8.1, 8.4, "peaceful", 4.0, 1, 20, "bottom", False, "saltwater"),
    "yellow-tang": ("Zebrasoma flavescens", 72, 82, 8.1, 8.4, "semi", 8.0, 1, 100, "mid", False, "saltwater"),
}


POPULARITY = {
    "betta-fish": 100, "goldfish": 96, "guppy": 94, "neon-tetra": 92,
    "angelfish": 90, "oscar": 88, "discus": 87, "molly": 84,
    "platy": 82, "corydoras": 81, "bristlenose-pleco": 80,
    "cherry-shrimp": 78, "clownfish": 78, "blue-tang": 76,
    "zebra-danio": 74, "cardinal-tetra": 72, "tiger-barb": 70,
}


def _number(value, default=2.0):
    """Largest number in the field.

    Sizes arrive as ranges ("5-7"), and `re.search` returned the lower bound,
    so a 10 cm rosy barb published as a 2-inch fish and every size-gap check
    compared juveniles. Adult size is the top of the range.
    """
    matches = re.findall(r"\d+(?:\.\d+)?", str(value or ""))
    return max(float(m) for m in matches) if matches else default


def _temperament(record):
    """Grade temperament from the two fields that describe temperament.

    The old version joined every value in the behaviour dict, so
    `activity_level: "moderate"` matched the "moderate" keyword and graded
    peaceful shoalers such as the rosy barb as semi-aggressive.
    """
    behavior = record.get("behavior", {})
    text = " ".join(str(behavior.get(key, "")) for key in ("temperament", "aggression_level")).lower()
    if any(word in text for word in ("high", "aggressive", "territorial", "predator")):
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


def _clip(text, limit=360):
    """Trim an overview to `limit` characters on a sentence boundary.

    A plain text[:360] slice cut mid-word on 30 of the hub pages — readers saw
    lines ending "can be seen darting aroun". Prefer the last complete
    sentence; fall back to the last whole word with an ellipsis.
    """
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    window = text[:limit]
    cut = max(window.rfind(". "), window.rfind("! "), window.rfind("? "))
    if cut >= limit * 0.6:
        return window[: cut + 1]
    return window[: window.rfind(" ")].rstrip(",;:") + "…"


def load_catalogue():
    raw = json.loads(RAW_DATA.read_text(encoding="utf-8"))
    missing = [slug for slug in V2_ADDITIONS if slug not in raw]
    if missing:
        raise RuntimeError(f"Missing v2 enrichment records: {', '.join(missing)}")

    for slug in V2_ADDITIONS:
        row = raw[slug]
        env, behavior = row["environment"], row["behavior"]
        name = re.sub(r"\bFish\b", "Fish", slug.replace("-", " ").title())
        # Care level and the overview paragraph still come from the enrichment
        # pass; every figure that feeds a score or a care recommendation comes
        # from V2_FACTS.  The old derivations stay as the fallback for a slug
        # that has not been checked yet.
        if slug in V2_FACTS:
            (sci, temp_min, temp_max, ph_min, ph_max, temperament, size,
             min_group, min_tank_gal, zone, eats_small, water) = V2_FACTS[slug]
        else:
            size_cm = _number(row.get("physical", {}).get("size_cm"), 5)
            sci, temperament, size = "Aquarium species", _temperament(row), round(size_cm / 2.54, 1)
            temp_min = round(env["temp_min_c"] * 9 / 5 + 32)
            temp_max = round(env["temp_max_c"] * 9 / 5 + 32)
            ph_min, ph_max = float(env["ph_min"]), float(env["ph_max"])
            min_group = 6 if behavior.get("schooling") else 1
            min_tank_gal = max(5, round(float(env["min_tank_liters"]) / 3.785))
            zone, water = _zone(slug, row), "freshwater"
            eats_small = size_cm >= 15 or temperament == "aggressive"
        v1.SPECIES[slug] = {
            "name": name, "sci": sci,
            "temp_min": temp_min, "temp_max": temp_max,
            "ph_min": ph_min, "ph_max": ph_max,
            "temperament": temperament, "size": size,
            "care": row.get("difficulty_level", "intermediate"),
            "water": water,
            "min_group": min_group, "diet": "omnivore",
            "eats_small": eats_small,
            "wiki": f"/wiki/{slug}/", "zone": zone,
            "min_tank_gal": min_tank_gal,
            "desc": _clip(row.get("sections", {}).get("overview", "")),
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
    marine = {a["water"], b["water"]} == {"saltwater", "freshwater"} or (
        "saltwater" in (a["water"], b["water"]) and a["water"] != b["water"])
    if marine:
        score = 0
        issues.append("One of these is a marine species and the other is not; they cannot share one aquarium.")
    elif not same_water:
        # Goldfish and koi carry water="coldwater", and the old check treated
        # cool-water-versus-tropical exactly like marine-versus-freshwater:
        # 156 pages told readers that two freshwater fish "require different
        # water types". They share a water type; what they may not share is a
        # temperature, and the overlap score below already measures that.
        cool = a if a["water"] == "coldwater" else b
        warm = b if cool is a else a
        issues.append(
            f"{cool['name']} is a cool-water fish and {warm['name']} is tropical, "
            "so the usable temperature range decides this pairing."
        )
    if special_bad:
        score = min(score, 18); issues.append(special_note)
    elif special_warn:
        score = min(score, 58); issues.append(special_note)
    if ratio >= 3 and (a.get("eats_small") or b.get("eats_small")):
        score = min(score, 32); issues.append("The adult size gap creates a meaningful predation risk.")
    # Like temperament, a missing temperature overlap is a blocker rather than
    # one weighted input: goldfish (50-74°F) and oscar (74-81°F) share a single
    # degree and still published as "Use Caution 58/100".
    # `temp` is a relative score, so it reads 0 both for ranges that miss each
    # other and for ranges that touch at a single degree. Gate on the degrees.
    temp_gap = min(a["temp_max"], b["temp_max"]) - max(a["temp_min"], b["temp_min"])
    if temp_gap < 0:
        score = min(score, 38)
        issues.append(
            f"There is no shared temperature: {a['name']} needs {a['temp_min']}–{a['temp_max']}°F "
            f"and {b['name']} needs {b['temp_min']}–{b['temp_max']}°F."
        )
    elif temp_gap < 3:
        score = min(score, 52)
        issues.append(
            f"Their ranges meet only at {max(a['temp_min'], b['temp_min'])}–{min(a['temp_max'], b['temp_max'])}°F, "
            "which leaves no margin for a heater drifting or a warm room."
        )
    elif temp < 35:
        score = min(score, 58)
        issues.append("Their preferred temperature ranges have little safe overlap.")
    else:
        positives.append("A stable shared temperature range is available.")
    # Same gate as temperature, one notch softer: many species adapt to a pH
    # outside their stated band, so a miss is a caution rather than a block.
    # Without it, cardinal tetra (4.5-7.0) and molly (7.5-8.5) published as
    # "Compatible" on a page whose own table read "pH Range: No overlap".
    ph_gap = min(a["ph_max"], b["ph_max"]) - max(a["ph_min"], b["ph_min"])
    if ph_gap < 0:
        score = min(score, 52)
        issues.append(
            f"Their pH ranges do not meet: {a['name']} wants {a['ph_min']:.1f}–{a['ph_max']:.1f} "
            f"and {b['name']} wants {b['ph_min']:.1f}–{b['ph_max']:.1f}."
        )
    elif ph_gap < 0.4:
        score = min(score, 65)
        issues.append("Their usable pH overlap is narrow and requires stable, tested water.")
    elif ph < 75:
        issues.append("Their pH ranges overlap only partly, so aim for the shared band and keep it steady.")
    else:
        positives.append("Their pH requirements overlap.")
    # A bad temperament match is a blocker, not one weighted input among six.
    # Weighting alone let aggressive x semi (25/100) still publish as
    # "Compatible 78/100" with an empty Caution Points card, because nothing
    # here ever wrote the temperament mismatch into `issues`.
    if temperament <= 15:
        score = min(score, 38)
        issues.append(
            f"{a['name']} and {b['name']} are both {'aggressive' if a['temperament'] == b['temperament'] else 'assertive'}; "
            "housing them together invites sustained fighting rather than an occasional squabble."
        )
    elif temperament <= 30:
        score = min(score, 58)
        issues.append(
            f"{a['name']} is {a['temperament']} and {b['name']} is {b['temperament']}. "
            "Expect chasing and fin damage unless the tank is oversized, heavily planted, and watched closely."
        )
    elif temperament < 65:
        issues.append(
            f"Both are {a['temperament']}, so give them a larger, well-planted tank and watch how they settle in."
            if a["temperament"] == b["temperament"] else
            "Their temperaments differ enough that a larger, well-planted tank and regular observation are needed."
        )
    else:
        positives.append("Temperament risk is relatively low when normal group sizes are maintained.")
    # Applied last: the editorial overrides exist to beat the model, so they
    # have to run after every cap, not before them.
    if frozenset((slug_a, slug_b)) == frozenset(("discus", "cardinal-tetra")):
        # A widely used warm-water combination; the shared point at 82°F is
        # viable when stock is acclimated and water quality is excellent.
        score = max(score, 76)
        issues = [item for item in issues if "temperature" not in item.lower() and "°F" not in item]
        positives.append("Both species can be maintained together at about 82°F in soft, clean water.")

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


def related_guides(sa, sb):
    """Return useful pair pages sharing either species, excluding this pair."""
    candidates = []
    for shared in (sa, sb):
        for other in v1.SPECIES:
            if other in (sa, sb):
                continue
            pair = "-and-".join(sorted((shared, other)))
            result = enhanced_compat(shared, other)
            priority = POPULARITY.get(other, 35)
            candidates.append((priority, result["score"], pair, shared, other))
    candidates.sort(key=lambda row: (-row[0], -row[1], row[2]))
    selected = []
    seen = set()
    for _, _, pair, shared, other in candidates:
        if pair in seen:
            continue
        seen.add(pair)
        selected.append((pair, f"{v1.SPECIES[shared]['name']} + {v1.SPECIES[other]['name']}"))
        if len(selected) == 6:
            break
    return selected


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
    scenarios = "".join(f"<tr><td><strong>{html.escape(label)}</strong></td><td>{gallons} gal</td><td>{html.escape(note)}</td></tr>" for label, gallons, note in tank_scenarios(a, b))
    related = "".join(f'<a href="/compatibility/{pair}/">🔗 {html.escape(label)}</a>' for pair, label in related_guides(sa, sb))
    section = f'''<section class="card"><h2>Tank size scenarios</h2><p>Use the scenario that matches the actual group sizes and temperament you plan to keep.</p>
<table class="cmp-table"><thead><tr><th>Scenario</th><th>Tank</th><th>When it applies</th></tr></thead><tbody>{scenarios}</tbody></table></section>'''
    marker = '<div class="guide-links">'
    related_block = f'<div class="related-pairs"><h3>More pair guides</h3><div class="guide-links">{related}</div></div>'
    pos = html_text.find(marker)
    return html_text[:pos] + section + related_block + html_text[pos:] if pos >= 0 else html_text.replace("</main>", section + related_block + "</main>")


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
<main class="hub"><section class="card"><h2>Care baseline</h2><p>{html.escape(fish['desc'])}</p><table class="cmp-table"><tr><td>Temperature</td><td>{fish['temp_min']}–{fish['temp_max']}°F</td></tr><tr><td>pH</td><td>{fish['ph_min']}–{fish['ph_max']}</td></tr><tr><td>Adult size</td><td>{fish['size']} in</td></tr><tr><td>Minimum group</td><td>{fish['min_group']}</td></tr></table></section>{'<section class="card shrimp-cluster"><h2>Betta &amp; Shrimp</h2><p>Compare the most common shrimp tank-mate options. Amano shrimp are usually the more robust choice; cherry and ghost shrimp remain individual-temperament risks.</p><div class="guide-links"><a href="/compatibility/betta-fish-and-amano-shrimp/">Betta &amp; Amano Shrimp</a><a href="/compatibility/betta-fish-and-cherry-shrimp/">Betta &amp; Cherry Shrimp</a><a href="/compatibility/betta-fish-and-ghost-shrimp/">Betta &amp; Ghost Shrimp</a></div></section>' if slug == 'betta-fish' else ''}{PEA_PUFFER_CARD if slug == 'pea-puffer' else ''}<h2>Compatibility guides</h2>{''.join(cards)}</main></body></html>'''


PEA_PUFFER_CARD = (
    '<section class="card"><h2>Pea Puffer Care Guides</h2><p>Tank size, water parameters, feeding and teeth care for pea puffers and the wider puffer family.</p><div class="guide-links"><a href="/guides/puffer-fish-care/pea-puffer/">Pea Puffer Care Guide</a><a href="/guides/puffer-fish-care/tank-mates/">Puffer Fish Tank Mates</a><a href="/guides/puffer-fish-care/food/">Puffer Food &amp; Feeding</a><a href="/guides/puffer-fish-care/">Puffer Fish Care Guide</a></div></section>'
)


def rebuild_sitemap(pair_rows):
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    # sitemap.xml became a <sitemapindex> after the compatibility URLs were
    # split into sitemaps/compatibility-*.xml.  Appending <url> nodes to an
    # index would produce an invalid sitemap, so refresh the split files'
    # lastmod instead and leave the index alone.
    if ET.parse(SITEMAP).getroot().tag == f"{ns}sitemapindex":
        # Rewrite the dates as text.  An ElementTree round-trip drops the
        # files' ns0: prefix and reformats all 12,500 lines of each one, which
        # buries a one-token change in a 50,000-line diff.
        for path in sorted((ROOT / "sitemaps").glob("compatibility-*.xml")):
            text = path.read_text(encoding="utf-8")
            text, count = re.subn(r"(<(?:\w+:)?lastmod>)[^<]*(</(?:\w+:)?lastmod>)", rf"\g<1>{TODAY}\2", text)
            path.write_text(text, encoding="utf-8")
            print(f"refreshed {count} lastmod dates in {path.relative_to(ROOT)}")
        return
    tree = ET.parse(SITEMAP); root = tree.getroot()
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
