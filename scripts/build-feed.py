#!/usr/bin/env python3
"""Build /feed.xml — an RSS 2.0 feed of the newest guides and fish-health pages.

Blog directories (Feedspot, Blogarama, Blog Flux, Inoreader, ooh.directory)
only list sites that publish a feed, so this exists mainly to unlock them.

Items come from the static pages this repo owns:
  * every URL in sitemaps/guides.xml
  * every pre-rendered page under fish-health/<slug>/index.html
pubDate is the date the page's index.html was first committed, so an item's
date never moves when the page is later edited — feed readers treat a changed
pubDate as a new post. Title, description and image are read from the page.

Re-run after publishing new pages, then commit feed.xml:
    python3 scripts/build-feed.py
"""
import html
import re
import subprocess
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.fishcareai.com"
MAX_ITEMS = 50


def first_commit_dates():
    """Map repo path -> datetime of the commit that first added it."""
    out = subprocess.run(
        ["git", "log", "--reverse", "--diff-filter=A", "--name-only",
         "--format=@@%aI", "--", "guides", "fish-health"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    dates, current = {}, None
    for line in out.splitlines():
        if line.startswith("@@"):
            current = datetime.fromisoformat(line[2:])
        elif line.endswith("index.html") and line not in dates:
            dates[line] = current
    return dates


def page_urls():
    sitemap = (ROOT / "sitemaps/guides.xml").read_text()
    urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    urls += [f"{SITE}/fish-health/{p.parent.name}"
             for p in sorted((ROOT / "fish-health").glob("*/index.html"))]
    return [u for u in urls if u.rstrip("/") != f"{SITE}/guides"]


def meta(doc, *patterns):
    for pattern in patterns:
        m = re.search(pattern, doc, re.I | re.S)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def main():
    dates = first_commit_dates()
    items = []
    for url in page_urls():
        rel = url[len(SITE) + 1:].rstrip("/") + "/index.html"
        path = ROOT / rel
        if not path.exists() or rel not in dates:
            continue
        doc = path.read_text(errors="ignore")
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', doc, re.I):
            continue
        title = meta(doc, r"<title>(.*?)</title>")
        title = re.sub(r"\s*[|·–-]\s*FishCare AI\s*$", "", title)
        items.append({
            "url": url,
            "title": title,
            "desc": meta(doc, r'<meta\s+name="description"\s+content="([^"]*)"'),
            "image": meta(doc, r'<meta\s+property="og:image"\s+content="([^"]*)"'),
            "date": dates[rel],
        })

    items.sort(key=lambda i: (i["date"], i["url"]), reverse=True)
    items = items[:MAX_ITEMS]
    esc = lambda s: html.escape(s, quote=False)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<?xml-stylesheet type="text/xsl" href="/feed.xsl"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:media="http://search.yahoo.com/mrss/">',
        "<channel>",
        "  <title>FishCare AI — Aquarium Care Guides</title>",
        f"  <link>{SITE}/</link>",
        f'  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>',
        "  <description>New aquarium fish care guides, species care sheets and "
        "fish health troubleshooting from FishCare AI.</description>",
        "  <language>en-us</language>",
        f"  <lastBuildDate>{format_datetime(items[0]['date'].astimezone(timezone.utc), usegmt=True)}</lastBuildDate>",
        "  <ttl>1440</ttl>",
        "  <image>",
        f"    <url>{SITE}/assets/pwa/icon-192.png</url>",
        "    <title>FishCare AI — Aquarium Care Guides</title>",
        f"    <link>{SITE}/</link>",
        "  </image>",
    ]
    for i in items:
        lines += [
            "  <item>",
            f"    <title>{esc(i['title'])}</title>",
            f"    <link>{i['url']}</link>",
            f'    <guid isPermaLink="true">{i["url"]}</guid>',
            f"    <pubDate>{format_datetime(i['date'].astimezone(timezone.utc), usegmt=True)}</pubDate>",
            f"    <description>{esc(i['desc'])}</description>",
        ]
        if i["image"]:
            lines.append(f'    <media:content url="{html.escape(i["image"])}" medium="image"/>')
        lines.append("  </item>")
    lines += ["</channel>", "</rss>", ""]

    (ROOT / "feed.xml").write_text("\n".join(lines))
    print(f"feed.xml: {len(items)} items, newest {items[0]['date']:%Y-%m-%d}, "
          f"oldest {items[-1]['date']:%Y-%m-%d}")


if __name__ == "__main__":
    main()
