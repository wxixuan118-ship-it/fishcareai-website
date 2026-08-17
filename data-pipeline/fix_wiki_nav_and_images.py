"""
fix_wiki_nav_and_images.py
──────────────────────────
1. Replaces the old wiki nav with the homepage-style nav (hamburger + full links + CTA button)
2. Fixes og:image and JSON-LD image: replaces wrong betta-fish placeholder with the actual
   hero image URL extracted from each page's <img class="sp-hero-img"> tag
3. Adds missing CSS for .btn/.bp/.bsm/.hbg and mobile breakpoint
"""

import re
from pathlib import Path

WIKI_DIR = Path(__file__).parent.parent / "wiki"

# ── New nav HTML ──────────────────────────────────────────────────────────────
NEW_NAV = '''\
<nav class="nb" id="navbar">
  <a title="FishCare AI" class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks" id="nlinks">
    <a title="Home" class="nl" href="/">Home</a>
    <a title="Care Guides" class="nl" href="/guides/">Guides</a>
    <a title="Aquarium Encyclopedia" class="nl act" href="/wiki/">Encyclopedia</a>
    <a title="Fish Health" class="nl" href="/fish-health/">Fish Health</a>
    <a title="Tools" class="nl" href="/tools/">Tools</a>
    <a title="About Us" class="nl" href="/about/">About Us</a>
    <a title="Contact" class="nl" href="/contact/">Contact</a>
    <a title="Try AI Free" class="btn bp bsm nb-cta" href="/tools/fish-compatibility-checker/">Try AI Free</a>
  </div>
  <button class="hbg" type="button" aria-label="Open navigation menu" onclick="document.getElementById('nlinks').classList.toggle('open')"><span></span><span></span><span></span></button>
</nav>'''

# ── Extra CSS to inject after the existing .nl rule ───────────────────────────
EXTRA_CSS = (
    '.btn{display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:999px;'
    'font-size:.9rem;font-weight:700;border:none;cursor:pointer;transition:all .18s;white-space:nowrap;'
    'box-shadow:0 10px 24px rgba(15,61,110,.12)}'
    '.bp{background:linear-gradient(135deg,var(--pd),#155C98);color:#fff}'
    '.bp:hover{background:linear-gradient(135deg,#08294C,var(--pd));transform:translateY(-1px);'
    'box-shadow:0 14px 28px rgba(15,61,110,.2)}'
    '.bsm{padding:7px 14px;font-size:.82rem}'
    '.hbg{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:7px;border:none;background:none}'
    '.hbg span{display:block;width:21px;height:2px;background:var(--tx);border-radius:2px}'
    '@media(max-width:760px){'
    '.nlinks{display:none;position:absolute;top:64px;left:0;right:0;background:#fff;'
    'flex-direction:column;padding:12px;border-bottom:1px solid var(--bd);gap:3px;'
    'box-shadow:0 4px 20px rgba(27,94,139,.12)}'
    '.nlinks.open{display:flex}.hbg{display:flex}.nb-cta{display:none}}'
)

def fix_file(path: Path) -> tuple[bool, list[str]]:
    html = path.read_text(encoding="utf-8")
    changes = []
    original = html

    # 1. Fix nav ----------------------------------------------------------------
    # Match old nav block (from <nav class="nb"> to its closing </nav>)
    nav_pattern = re.compile(r'<nav class="nb">.*?</nav>', re.DOTALL)
    if nav_pattern.search(html):
        html = nav_pattern.sub(NEW_NAV, html, count=1)
        changes.append("nav updated")
    elif 'id="navbar"' in html:
        changes.append("nav already updated — skipped")
    else:
        changes.append("WARNING: nav block not found")

    # 2. Add missing CSS (only if not present) ---------------------------------
    if '.hbg{' not in html and '.btn{' not in html:
        # Insert after the .nl hover rule (present in all wiki pages)
        nl_rule = '.nl:hover,.nl.act{color:var(--p);background:rgba(27,94,139,.07)}'
        if nl_rule in html:
            html = html.replace(nl_rule, nl_rule + EXTRA_CSS, 1)
            changes.append("nav CSS added")
        else:
            changes.append("WARNING: anchor CSS rule not found; CSS not added")

    # 3. Extract hero image URL ------------------------------------------------
    hero_match = re.search(
        r'<img[^>]+class="sp-hero-img"[^>]+src="([^"]+)"',
        html
    )
    if not hero_match:
        # Also try reversed attribute order
        hero_match = re.search(
            r'<img[^>]+src="([^"]+)"[^>]+class="sp-hero-img"',
            html
        )

    hero_url = hero_match.group(1) if hero_match else None

    # 4. Fix og:image ----------------------------------------------------------
    bad_og = re.compile(r'(<meta property="og:image" content=")[^"]*(")')
    og_match = bad_og.search(html)
    if og_match and hero_url:
        html = bad_og.sub(rf'\g<1>{hero_url}\g<2>', html, count=1)
        changes.append(f"og:image → {hero_url[:60]}...")
    elif og_match and not hero_url:
        changes.append("WARNING: og:image wrong but no hero img found")

    # 5. Fix JSON-LD image -----------------------------------------------------
    bad_image = re.compile(r'"image"\s*:\s*"/assets/fish-images/[^"]*"')
    if bad_image.search(html) and hero_url:
        html = bad_image.sub(f'"image":"{hero_url}"', html, count=1)
        changes.append("JSON-LD image fixed")

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True, changes
    return False, changes or ["no changes needed"]


def main():
    sub_pages = [
        p for p in WIKI_DIR.iterdir()
        if p.is_dir() and (p / "index.html").exists()
    ]
    # Also handle wiki/index.html
    wiki_index = WIKI_DIR / "index.html"

    all_files = sub_pages + ([wiki_index] if wiki_index.exists() else [])

    updated = 0
    for page_dir in sorted(sub_pages, key=lambda p: p.name):
        f = page_dir / "index.html"
        changed, notes = fix_file(f)
        status = "✅" if changed else "—"
        print(f"{status} {page_dir.name}: {', '.join(notes)}")
        if changed:
            updated += 1

    # wiki/index.html — nav is slightly different (no sp-hero-img), handle separately
    if wiki_index.exists():
        changed, notes = fix_file(wiki_index)
        status = "✅" if changed else "—"
        print(f"{status} wiki/index: {', '.join(notes)}")
        if changed:
            updated += 1

    print(f"\nDone — {updated}/{len(all_files)} files updated")


if __name__ == "__main__":
    main()
