"""Upgrade all species compatibility hub pages to the compact template.

The compact template (pilot: blue-tang online) shows ~10-12 curated tank mates
per species instead of all 90. Selection logic:
  1. All same-water-type species (the natural tank mates)
  2. Highest-scoring cross-water "Use Caution" pairs if same-water < 10
  3. 1-2 low-scoring cross-water examples (score 0) as explicit "avoid" cases

Also updates:
  - meta description species count ("90" → actual shown count)
  - JSON-LD CollectionPage description count
  - Pair list sorted by score descending (highest first)

Run: python3 data-pipeline/upgrade_hub_compact.py [--dry-run]
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPAT = ROOT / "compatibility"

# The 11 saltwater species in the catalogue. Everything else is freshwater
# or coldwater (treated as freshwater for compatibility purposes).
SALTWATER = {
    "blue-tang", "coral-beauty", "firefish-goby", "flame-angelfish",
    "foxface-rabbitfish", "lionfish", "pajama-cardinalfish", "percula-clownfish",
    "royal-gramma", "watchman-goby", "yellow-tang",
}

# Patterns for parsing existing hub HTML
PAIR_RE = re.compile(
    r'<a class="pair" href="/compatibility/([^"]+)/">'
    r'<span><strong>([^<]+) \+ ([^<]+)</strong>'
    r'<small>SEO priority (\d+)/100</small></span>'
    r'<b style="color:[^"]+">(\d+)/100\s*·\s*([^<]+)</b></a>'
)
DESC_COUNT_RE = re.compile(r"Compare .+? with \d+ aquarium species")
JSONLD_DESC_COUNT_RE = re.compile(r'"description":\s*"Compare .+? with \d+ aquarium species')


def parse_hub(path: Path) -> dict:
    """Parse a hub page and return structured data."""
    text = path.read_text(encoding="utf-8")
    slug = path.parent.name

    # Extract main species display name from H1
    h1_match = re.search(r"<h1>([^<]+) Tank Mates</h1>", text)
    main_name = h1_match.group(1) if h1_match else slug.replace("-", " ").title()

    pairs = []
    for m in PAIR_RE.finditer(text):
        pair_slug = m.group(1)          # e.g. "blue-tang-and-coral-beauty" or "coral-beauty-and-blue-tang"
        name_a = m.group(2)             # Always main species display name (from strong tag)
        name_b = m.group(3)             # Always other species display name
        seo_priority = int(m.group(4))  # e.g. 69
        score = int(m.group(5))         # e.g. 65
        verdict = m.group(6).strip()    # e.g. "Use Caution"

        # name_a is always the hub's main species (verified: all 90 have main as name_a)
        # name_b is always the tank mate we want to show
        other_name = name_b

        # Determine other_slug from pair_slug (it's the one that's NOT our slug)
        a_slug, b_slug = pair_slug.rsplit("-and-", 1)
        other_slug = b_slug if slug == a_slug else a_slug

        other_is_salt = other_slug in SALTWATER
        main_is_salt = slug in SALTWATER
        same_water = (main_is_salt == other_is_salt)

        pairs.append({
            "pair_slug": pair_slug,
            "other_slug": other_slug,
            "other_name": other_name,
            "seo_priority": seo_priority,
            "score": score,
            "verdict": verdict,
            "same_water": same_water,
        })

    return {"slug": slug, "main_name": main_name, "text": text, "pairs": pairs}


def select_pairs(data: dict, max_show: int = 12) -> list[dict]:
    """Select which pairs to show, following blue-tang compact logic.

    Strategy:
      1. All same-water pairs if they fit in max_show - 1
         (the -1 leaves room for at least one cross-water "avoid" example)
      2. Otherwise, top-scoring same-water up to max_show - 2
      3. Add 1-2 lowest-scoring cross-water pairs as explicit "avoid" examples
      4. Final sort: score descending
    """
    pairs = data["pairs"]
    slug = data["slug"]

    same_water = [p for p in pairs if p["same_water"]]
    cross_water = [p for p in pairs if not p["same_water"]]

    # Sort same-water by score desc, then SEO priority desc
    same_water.sort(key=lambda p: (-p["score"], -p["seo_priority"]))
    cross_water.sort(key=lambda p: (p["score"], -p["seo_priority"]))  # asc for worst-first

    selected = []

    # Reserve slots for cross-water examples only when the hub actually links any
    reserve = 2 if cross_water else 0

    if len(same_water) <= max_show - 1:
        # Few same-water pairs (e.g. saltwater species): show all + 1 cross-water example
        selected.extend(same_water)
    else:
        # Many same-water pairs (e.g. freshwater species): show top ones
        selected.extend(same_water[: max_show - reserve])

    # Add cross-water "avoid" examples (worst score first)
    for p in cross_water:
        if len(selected) >= max_show:
            break
        selected.append(p)

    # Final sort: score descending
    selected.sort(key=lambda p: (-p["score"], -p["seo_priority"]))

    return selected


def build_pair_html(main_name: str, pairs: list[dict]) -> str:
    """Build the <a class="pair"> elements."""
    verdict_map = {
        "Compatible": "#27AE60",
        "Use Caution": "#F39C12",
        "Not Compatible": "#E74C3C",
        "Incompatible": "#E74C3C",
    }
    parts = []
    for p in pairs:
        color = verdict_map.get(p["verdict"], "#E74C3C")
        parts.append(
            f'<a class="pair" href="/compatibility/{p["pair_slug"]}/">'
            f'<span><strong>{html.escape(main_name)} + {html.escape(p["other_name"])}</strong>'
            f'<small>SEO priority {p["seo_priority"]}/100</small></span>'
            f'<b style="color:{color}">{p["score"]}/100 · {p["verdict"]}</b></a>'
        )
    return "".join(parts)


def rewrite_hub(path: Path, dry_run: bool = False) -> bool:
    """Rewrite a hub page with the compact pair list."""
    data = parse_hub(path)
    slug = data["slug"]
    text = data["text"]
    pairs = data["pairs"]

    if not pairs:
        print(f"  SKIP {slug}: no pairs found")
        return False

    selected = select_pairs(data)
    shown_count = len(selected)
    total_count = len(pairs)
    main_name = data["main_name"]

    # Build new pair HTML
    new_pair_html = build_pair_html(main_name, selected)

    # Find old pair block and replace it.
    # Old pairs are between <h2>...Tank Mates Ranked by Compatibility</h2> and </main>
    h2_match = re.search(r"(<h2>[^<]*Tank Mates Ranked by Compatibility</h2>)", text)
    if not h2_match:
        print(f"  SKIP {slug}: cannot find h2 heading")
        return False

    # Find </main>
    main_end = text.rfind("</main>")
    if main_end < 0:
        print(f"  SKIP {slug}: cannot find </main>")
        return False

    new_text = text[:h2_match.end()] + new_pair_html + text[main_end:]

    # Update meta description count
    new_text = DESC_COUNT_RE.sub(
        lambda m: re.sub(r"\d+", str(shown_count), m.group(0)), new_text
    )

    # Update JSON-LD CollectionPage description count
    new_text = JSONLD_DESC_COUNT_RE.sub(
        lambda m: re.sub(r"\d+", str(shown_count), m.group(0)), new_text
    )

    # Update sup text "All 90 ..." → "All N ..."
    new_text = re.sub(
        r"All 90 ([^<]+?) pair guides, ranked by practical compatibility\.",
        f"All {shown_count} \\1 pair guides, ranked by practical compatibility.",
        new_text,
    )

    if dry_run:
        print(f"  {slug}: show {shown_count}/{total_count} pairs (dry-run)")
        return True

    path.write_text(new_text, encoding="utf-8")
    print(f"  {slug}: show {shown_count}/{total_count} pairs ✅")
    return True


def main():
    parser = argparse.ArgumentParser(description="Compact hub pages to curated tank mate lists")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--only", nargs="*", help="Only process specific slugs")
    parser.add_argument("--max", type=int, default=12, help="Max pairs to show per hub (default 12)")
    args = parser.parse_args()

    hub_paths = sorted(COMPAT.glob("*/index.html"))
    hub_paths = [p for p in hub_paths if "-and-" not in p.parent.name]

    if args.only:
        hub_paths = [p for p in hub_paths if p.parent.name in args.only]

    print(f"Found {len(hub_paths)} hub pages to process" + (" (dry-run)" if args.dry_run else ""))
    print("=" * 60)

    upgraded = skipped = 0
    for path in hub_paths:
        if rewrite_hub(path, dry_run=args.dry_run):
            upgraded += 1
        else:
            skipped += 1

    print("=" * 60)
    print(f"Done: {upgraded} upgraded, {skipped} skipped")


if __name__ == "__main__":
    main()
