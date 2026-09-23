"""Upgrade the rendered compatibility pages in place for on-page SEO.

An audit of the 462 compatibility pages ranking in Google's top 20 found the
same template faults on every v1-pattern pair page: a 72–74 character title
that truncates in the SERP, no heading or alt text carrying the "A and B"
phrase people search, and the site logo as the only <img>. The v2 generator
cannot be re-run here (its raw catalogue is not in this checkout, and ~40
pages were hand-upgraded afterwards), so this patches the HTML that exists:

  pair pages  — title, H1, description, Article/OG copies of both, the first
                and last H2, and a photo of each species in Species Profiles
  species hubs — intro paragraph, list heading, photo, JSON-LD

Pages that no longer match the v1 title pattern (the hand-upgraded pilot set)
are left alone. Safe to re-run: every edit is keyed on the old markup.

Run: python3 data-pipeline/upgrade_compatibility_onpage.py [--dry-run]
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
COMPAT = ROOT / "compatibility"
PHOTOS = ROOT / "assets" / "encyclopedia" / "real"
THUMBS = ROOT / "assets" / "compatibility" / "thumbs"
THUMB_WIDTH = 480
MAX_TITLE = 60
MAX_DESC = 160

# Compatibility slugs whose photo lives under a different encyclopedia slug.
PHOTO_ALIAS = {"pea-puffer": "dwarf-puffer", "pygmy-corydoras": "pygmy-cory"}

# Display names that differ from the URL slug split the searched phrase
# ("corydoras and guppy" never appears in "Corydoras Catfish and Guppy"), so
# the title-level copy uses the slug form for these.
SHORT_NAME = {"corydoras": "Corydoras"}

TITLE_RE = re.compile(r"<title>Can (.+?) Live With (.+?)\? Compatibility Guide \| FishCare AI</title>")
CHIP_RE = re.compile(r'<div class="verdict-chip"[^>]*>(?:[^<]*?)(Compatible|Caution|Not Compatible|Incompatible)[^<]*?(\d+)/100</div>')
PHOTO_CSS = ".sp-photo{display:block;max-width:min(100%,480px);height:auto;border-radius:10px;margin:6px 0 10px}"


def split_pair(dirname: str) -> tuple[str, str]:
    a, b = dirname.split("-and-", 1)
    return a, b


def ensure_thumb(slug: str) -> tuple[str, int, int] | None:
    """Return (src, width, height) for a species thumbnail, building it on first use."""
    source = PHOTOS / f"{PHOTO_ALIAS.get(slug, slug)}-wikimedia-real.jpg"
    if not source.exists():
        return None
    THUMBS.mkdir(parents=True, exist_ok=True)
    out = THUMBS / f"{slug}.webp"
    if not out.exists():
        with Image.open(source) as im:
            im = im.convert("RGB")
            if im.width > THUMB_WIDTH:
                im = im.resize((THUMB_WIDTH, round(im.height * THUMB_WIDTH / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=78, method=6)
    with Image.open(out) as im:
        return f"/assets/compatibility/thumbs/{slug}.webp", im.width, im.height


def build_title(a: str, b: str) -> str:
    variants = [
        f"Can {a} and {b} Live Together? Compatibility Guide",
        f"Can {a} and {b} Live Together?",
        f"{a} and {b} Compatibility Guide",
        f"{a} and {b} Compatibility",
    ]
    return next((v for v in variants if len(v) <= MAX_TITLE), variants[-1])


def build_description(a: str, b: str, verdict: str, score: str) -> str:
    """Set up the question without answering it in the SERP.

    The description used to open "compatibility: not compatible, score
    38/100", which is the whole page in eleven words - a searcher who reads it
    has no reason to click.  Name the factors that decide the pairing instead
    and let the page give the verdict.  `verdict` and `score` stay in the
    signature because the caller passes them and the 34 pilot pages use the
    same shape.
    """
    variants = [
        f"Can {a} and {b} share a tank? Compare their temperature, pH, temperament and adult size, plus the tank size both species need.",
        f"Can {a} and {b} share a tank? Compare temperature, pH, temperament and adult size, plus the tank size both need.",
        f"{a} and {b}: temperature, pH, temperament, adult size and tank size compared side by side.",
        f"{a} and {b}: temperature, pH, temperament and tank size compared.",
    ]
    return next((v for v in variants if len(v) <= MAX_DESC), variants[-1])


def photo_tag(slug: str, alt: str) -> str:
    thumb = ensure_thumb(slug)
    if not thumb:
        return ""
    src, w, h = thumb
    return f'<img class="sp-photo" src="{src}" alt="{html.escape(alt, quote=True)}" width="{w}" height="{h}" loading="lazy" decoding="async">'


def upgrade_pair(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = TITLE_RE.search(text)
    if not m:
        return False
    old_title = m.group(0)[len("<title>"):-len("</title>")]
    name_a, name_b = m.group(1), m.group(2)
    slug_a, slug_b = split_pair(path.parent.name)
    a = SHORT_NAME.get(slug_a, name_a)
    b = SHORT_NAME.get(slug_b, name_b)

    chip = CHIP_RE.search(text)
    verdict, score = (chip.group(1), chip.group(2)) if chip else ("Caution", "50")

    title = build_title(a, b)
    h1 = f"Can {a} and {b} Live Together?"
    desc = build_description(a, b, verdict, score)

    old_desc_m = re.search(r'<meta name="description" content="([^"]*)"', text)
    old_desc = old_desc_m.group(1) if old_desc_m else None

    # Title and description: <title>, meta, OG/Twitter, and the Article schema
    # (which stores the same strings JSON-escaped).
    text = text.replace(old_title, title)
    text = text.replace(json.dumps(old_title)[1:-1], json.dumps(title)[1:-1])
    if old_desc:
        text = text.replace(old_desc, html.escape(desc, quote=True))
        text = text.replace(json.dumps(html.unescape(old_desc))[1:-1], json.dumps(desc)[1:-1])

    text = text.replace(f"<h1>Can {name_a} Live With {name_b}?</h1>", f"<h1>{h1}</h1>", 1)
    text = text.replace("<h2>Compatibility Overview</h2>", f"<h2>{a} and {b} Compatibility Overview</h2>", 1)
    text = text.replace("<h2>Tank size scenarios</h2>", f"<h2>Tank Size for {a} and {b}</h2>", 1)

    # Species photos inside the profiles, one per species.
    if 'class="sp-photo"' not in text:
        for slug, name, other in ((slug_a, name_a, b), (slug_b, name_b, a)):
            tag = photo_tag(slug, f"{a} and {b} compatibility — {name}")
            if not tag:
                continue
            head_re = re.compile(rf"(<h3[^>]*>{re.escape(name)} — <em>[^<]*</em></h3>)")
            text, n = head_re.subn(rf"\1{tag}", text, count=1)
        if 'class="sp-photo"' in text and PHOTO_CSS not in text:
            text = text.replace("</style>", PHOTO_CSS + "</style>", 1)

    path.write_text(text, encoding="utf-8")
    return True


HUB_TITLE_RE = re.compile(r"<title>(.+?) Tank Mates: 90 Compatibility Guides \| FishCare AI</title>")


def upgrade_hub(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = HUB_TITLE_RE.search(text)
    if not m or 'class="hub-intro"' in text:
        return False
    slug = path.parent.name
    name = SHORT_NAME.get(slug, m.group(1))
    display = m.group(1)
    phrase = f"{name} tank mates"

    intro = (
        f'<section class="card hub-intro"><h2>Choosing {name} Tank Mates</h2>'
        f"{photo_tag(slug, f'{name} tank mates guide — {display}')}"
        f"<p>Good {phrase} share the same temperature and pH window, will not be eaten by (or eat) "
        f"the {display}, and do not compete for the same swimming zone or feeding time. Each pair guide "
        f"below scores those factors from 0 to 100 and gives the minimum tank size for keeping both "
        f"species together.</p>"
        f"<p>Start with the highest-scoring pairs; anything under 45 is listed so you know what to avoid, "
        f"not as a recommendation.</p></section>"
    )
    text = text.replace('<main class="hub">', '<main class="hub">' + intro, 1)
    text = text.replace("<h2>Compatibility guides</h2>", f"<h2>{name} Tank Mates Ranked by Compatibility</h2>", 1)
    text = text.replace(
        "All 90 pair guides, ordered by search value and practical compatibility.",
        f"All 90 {phrase} pair guides, ranked by practical compatibility.", 1,
    )
    if 'class="sp-photo"' in text and PHOTO_CSS not in text:
        text = text.replace("</style>", PHOTO_CSS + "</style>", 1)

    schema = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.fishcareai.com/"},
            {"@type": "ListItem", "position": 2, "name": "Fish Compatibility", "item": "https://www.fishcareai.com/compatibility/"},
            {"@type": "ListItem", "position": 3, "name": f"{display} Tank Mates", "item": f"https://www.fishcareai.com/compatibility/{slug}/"},
        ]},
        {"@context": "https://schema.org", "@type": "CollectionPage",
         "name": f"{display} Tank Mates: 90 Compatibility Guides",
         "description": f"Compare {display} with 90 aquarium species. Ranked compatibility scores, water requirements, behavior risks, and tank size guidance.",
         "url": f"https://www.fishcareai.com/compatibility/{slug}/",
         "isPartOf": {"@type": "WebSite", "name": "FishCare AI", "url": "https://www.fishcareai.com/"}},
    ]
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    text = text.replace("</head>", blocks + "</head>", 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", nargs="*", help="page slugs to limit the run to")
    args = parser.parse_args()

    pairs = hubs = skipped = 0
    for page in sorted(COMPAT.glob("*/index.html")):
        slug = page.parent.name
        if args.only and slug not in args.only:
            continue
        if args.dry_run:
            text = page.read_text(encoding="utf-8")
            hit = TITLE_RE.search(text) or HUB_TITLE_RE.search(text)
            print(("would upgrade " if hit else "skip ") + slug)
            continue
        if "-and-" in slug:
            if upgrade_pair(page): pairs += 1
            else: skipped += 1
        else:
            if upgrade_hub(page): hubs += 1
            else: skipped += 1
    print(f"upgraded {pairs} pair pages, {hubs} hubs; left {skipped} untouched")


if __name__ == "__main__":
    main()
