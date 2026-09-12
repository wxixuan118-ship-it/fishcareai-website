#!/usr/bin/env python3
"""
Build the /tank-sizes/ experiment pages.

    python3 data-pipeline/tank_sizes/build.py

Writes tank-sizes/<slug>/index.html for each content module. These three pages
are an SEO experiment; do not add further sizes here until the experiment has
been evaluated in Search Console.
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from template import render_page, diagram_svg  # noqa: E402

PAGES = ["content_55", "content_50", "content_100"]

for mod_name in PAGES:
    page = importlib.import_module(mod_name).PAGE
    out_dir = REPO / "tank-sizes" / page["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    html = render_page(page)
    d = page["diagram"]
    asset_dir = REPO / "assets" / "tank-sizes"
    asset_dir.mkdir(parents=True, exist_ok=True)
    svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + diagram_svg(page["gallons"], d["l"], d["w"], d["h"], d["label"])
    (asset_dir / f"{page['slug']}-dimensions.svg").write_text(svg, encoding="utf-8")
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    words = len(__import__("re").sub(r"<[^>]+>", " ", html.split("<main>")[1].split("</main>")[0]).split())
    print(f"wrote {out_dir.relative_to(REPO)}/index.html  ({len(html):,} bytes, ~{words:,} words in main)")
