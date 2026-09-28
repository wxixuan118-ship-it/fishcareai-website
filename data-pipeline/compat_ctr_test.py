"""CTR experiment on compatibility pair pages — 2026-09-28.

Why: the 90-day GSC export for /compatibility/ shows 789 of 1,000 pair pages at
an average position of 5-10 with a 0.56% CTR. The SERPs for those queries open
with an AI Overview that already answers "can A and B live together", followed
by Reddit/Quora threads. A title that repeats the question and a description
that withholds the answer give the searcher nothing the Overview did not.

The test variant:
  title        states the verdict ("No, Here's Why" / "Yes, With Setup Tips" /
               "Only With Care"), keeping the "Can A and B Live Together?" phrase
  description  verdict + the concrete reason (temperatures, temperament, size)
               + what the page adds that the Overview does not
  quick answer a boxed one-paragraph answer directly under the first H2, so the
               verdict and its numbers are extractable
  tank mates   a "Safer / More Good Tank Mates" card listing the five highest-
               scoring compatible partners for each species, linked

Control pages are left untouched. Pages are paired by impressions within each
verdict and one of each pair is assigned to the test group at random, so the
groups start with matching traffic and verdict mix.

  python3 data-pipeline/compat_ctr_test.py select <gsc-export.xlsx>
  python3 data-pipeline/compat_ctr_test.py apply [--dry-run]

`select` writes reports/compat-ctr-test-2026-09-28.csv; `apply` patches only the
rows marked "test" in it. Safe to re-run: patched pages carry class="quick-answer"
and are skipped.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPAT = ROOT / "compatibility"
SITEMAPS = sorted((ROOT / "sitemaps").glob("compatibility-*.xml"))
REPORT = ROOT / "reports" / "compat-ctr-test-2026-09-28.csv"

TEST_DATE = "2026-09-28"
TEST_DATE_HUMAN = "September 28, 2026"
SEED = 20260928
MAX_PAGES = 200          # 100 test + 100 control
MAX_POSITION = 15.0
MAX_TITLE = 60
MAX_DESC = 160

# Pages whose hand-written prose says "No" while the scored verdict says
# Caution/Compatible (or the reverse). Their verdict needs an editorial call
# before a title can state it, so they stay out of both groups.
EXCLUDE = {
    "angelfish-and-oscar", "betta-fish-and-pea-puffer", "ember-tetra-and-tiger-barb",
    "goldfish-and-oscar", "green-terror-cichlid-and-senegal-bichir",
    "jewel-cichlid-and-mystery-snail", "koi-and-silver-arowana",
    "dwarf-chain-loach-and-pea-puffer", "discus-and-neon-tetra",
    "goldfish-and-hillstream-loach", "koi-and-turtles",
}

H1_RE = re.compile(r"<h1>Can (.+?) (?:and|Live With) (.+?)(?: Live Together)?\?</h1>")
QF_RE = r'>{key}</td><td[^>]*>(.*?)</td>'


def text(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def quick_fact(page: str, key: str) -> str:
    m = re.search(QF_RE.format(key=re.escape(key)), page)
    return text(m.group(1)) if m else ""


def verdict_of(page: str) -> str:
    v = quick_fact(page, "Verdict")
    if "Not" in v:
        return "no"
    if "Caution" in v:
        return "caution"
    if "Compatible" in v:
        return "yes"
    return ""


def table_row(page: str, factor: str) -> tuple[str, str, str] | None:
    m = re.search(rf"<tr><td>{re.escape(factor)}</td><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td></tr>", page)
    return (text(m.group(1)), text(m.group(2)), text(m.group(3))) if m else None


def load_pages() -> dict[str, dict]:
    pages = {}
    for d in sorted(COMPAT.iterdir()):
        f = d / "index.html"
        if "-and-" not in d.name or not f.exists():
            continue
        page = f.read_text(encoding="utf-8")
        h1 = H1_RE.search(page)
        if not h1:
            continue
        score = re.match(r"(\d+)", quick_fact(page, "Score"))
        pages[d.name] = {
            "a": h1.group(1), "b": h1.group(2),
            "verdict": verdict_of(page),
            "score": int(score.group(1)) if score else 0,
        }
    return pages


# ---------------------------------------------------------------- select

def select(export: Path) -> None:
    from openpyxl import load_workbook

    pages = load_pages()
    wb = load_workbook(export, read_only=True)
    rows = list(wb["网页"].iter_rows(values_only=True))[1:]
    eligible = []
    for url, clicks, impr, ctr, pos in rows:
        m = re.search(r"/compatibility/([^/]+-and-[^/]+)/?$", url or "")
        if not m or m.group(1) in EXCLUDE or m.group(1) not in pages:
            continue
        if pos > MAX_POSITION or not pages[m.group(1)]["verdict"]:
            continue
        eligible.append({"slug": m.group(1), "url": url, "clicks": int(clicks),
                         "impressions": int(impr), "ctr": round(ctr * 100, 2),
                         "position": round(pos, 2), "verdict": pages[m.group(1)]["verdict"]})
    eligible.sort(key=lambda r: -r["impressions"])
    eligible = eligible[:MAX_PAGES]

    rng = random.Random(SEED)
    by_verdict = defaultdict(list)
    for r in eligible:
        by_verdict[r["verdict"]].append(r)
    for group in by_verdict.values():
        for i in range(0, len(group), 2):
            pair = group[i:i + 2]
            rng.shuffle(pair)
            pair[0]["group"] = "test"
            if len(pair) > 1:
                pair[1]["group"] = "control"

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    fields = ["slug", "group", "verdict", "impressions", "clicks", "ctr", "position", "url"]
    with REPORT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(eligible, key=lambda r: (r["group"], -r["impressions"])))

    for g in ("test", "control"):
        rs = [r for r in eligible if r["group"] == g]
        imp = sum(r["impressions"] for r in rs)
        clk = sum(r["clicks"] for r in rs)
        mix = {v: sum(1 for r in rs if r["verdict"] == v) for v in ("yes", "caution", "no")}
        print(f"{g:8} pages={len(rs):3} impressions={imp:6} clicks={clk:3} "
              f"ctr={clk / imp * 100:.2f}% avg_pos={sum(r['position'] for r in rs) / len(rs):.2f} {mix}")
    print(f"wrote {REPORT.relative_to(ROOT)}")


# ---------------------------------------------------------------- copy

def f_range(s: str) -> str:
    return s.replace("–", "-")


def first_point(page: str) -> str:
    """The page's own leading risk note: first ❌ point, else first ⚠️ point, first clause only."""
    points = re.findall(r'class="point point-(er|wn)"[^>]*>.*?</span>\s*<span>(.*?)</span>', page, re.S)
    for level in ("er", "wn"):
        for lv, raw in points:
            if lv == level:
                note = text(raw).split(". ")[0].split(", so ")[0].split("; ")[0].rstrip(".")
                return note
    return ""


def reason(page: str, v: str, a: str, b: str) -> str:
    """One clause naming the deciding factor, in the page's own numbers and words."""
    temp = table_row(page, "Temperature")
    temper = table_row(page, "Temperament")

    if v == "yes":
        parts = []
        if temp and "✅" in temp[2]:
            parts.append(f"both do well at {f_range(temp[2].replace('✅', '').strip())}")
        if temper and temper[0] == temper[1] == "peaceful":
            parts.append("both are peaceful")
        return " and ".join(parts) or "their water needs overlap"

    if "marine species" in page and "cannot share one aquarium" in page:
        return "one is a marine fish and the other freshwater"
    if temp and ("No overlap" in temp[2] or "narrow" in temp[2]):
        return f"{a} needs {f_range(temp[0])} and {b} needs {f_range(temp[1])}"
    note = first_point(page)
    if note:
        return note[0].lower() + note[1:] if note.startswith("Their ") else note
    return "their water and temperament needs only partly overlap"


def cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def first_fit(options: list[str], limit: int) -> str:
    return next((o for o in options if len(o) <= limit), options[-1])


def build_title(v: str, a: str, b: str) -> str:
    tail = {"no": ("No, Here's Why", "Not Compatible"),
            "caution": ("Only With Care", "Risky Pair"),
            "yes": ("Yes, With Setup Tips", "Compatible")}[v]
    return first_fit([
        f"Can {a} and {b} Live Together? {tail[0]}",
        f"{a} and {b}: {tail[1]} — {tail[0].split(',')[-1].strip()}",
        f"{a} and {b}: {tail[1]}",
        f"{a} and {b} Compatibility",
    ], MAX_TITLE)


def build_description(v: str, a: str, b: str, why: str) -> str:
    if v == "no":
        opts = [f"No. {cap(why)}. See why they clash and safer tank mates for each.",
                f"No. {cap(why)}. See safer tank mates for each.",
                f"No. {cap(why)}."]
    elif v == "caution":
        opts = [f"Only with care: {why}. See what to watch, the setup that lowers the risk, and safer tank mates.",
                f"Only with care: {why}. See what to watch and safer tank mates.",
                f"Only with care: {why}."]
    else:
        opts = [f"Yes. {cap(why)}. See the tank size, group size and setup that keep both healthy, plus more good tank mates.",
                f"Yes. {cap(why)}. See the tank size, group size and setup that keep both healthy.",
                f"Yes. {cap(why)}."]
    return first_fit(opts, MAX_DESC)


def quick_answer(v: str, why: str, a: str, b: str) -> str:
    lead = {"no": "Short answer: No.", "caution": "Short answer: only with care.", "yes": "Short answer: Yes."}[v]
    tail = {"no": f"Keep them in separate tanks, or pick one of the safer tank mates listed below.",
            "caution": f"It can work in a large, well-planted tank if you watch both fish closely for the first weeks.",
            "yes": f"Match the tank size and group size in the table below and both should do well."}[v]
    return ('<p class="quick-answer" style="background:rgba(46,132,192,.16);border-left:4px solid var(--pl);'
            'padding:12px 14px;border-radius:8px;margin:0 0 14px">'
            f"<strong>{lead}</strong> {html.escape(cap(why))}. {tail}</p>")


def mates_card(slug: str, v: str, a: str, b: str, pages: dict, index: dict) -> str:
    slug_a, slug_b = slug.split("-and-", 1)
    cols = []
    for sp_slug, name, other in ((slug_a, a, slug_b), (slug_b, b, slug_a)):
        mates = [m for m in index.get(sp_slug, []) if m["partner"] != other][:5]
        if not mates:
            continue
        items = "".join(
            f'<li><a href="/compatibility/{m["slug"]}/">{html.escape(m["partner_name"])}</a> — {m["score"]}/100</li>'
            for m in mates)
        cols.append(f"<h3>For {html.escape(name)}</h3><ul>{items}</ul>")
    if not cols:
        return ""
    heading = f"More Good Tank Mates for {a} and {b}" if v == "yes" else f"Safer Tank Mates for {a} and {b}"
    return (f'<section class="card"><h2>{html.escape(heading)}</h2>'
            f"<p>The highest-scoring compatible partners for each species in our compatibility data.</p>"
            f"{''.join(cols)}</section>\n      ")


def mates_index(pages: dict) -> dict[str, list[dict]]:
    idx = defaultdict(list)
    for slug, p in pages.items():
        if p["verdict"] != "yes":
            continue
        sa, sb = slug.split("-and-", 1)
        idx[sa].append({"slug": slug, "partner": sb, "partner_name": p["b"], "score": p["score"]})
        idx[sb].append({"slug": slug, "partner": sa, "partner_name": p["a"], "score": p["score"]})
    for lst in idx.values():
        lst.sort(key=lambda m: (-m["score"], m["partner_name"]))
    return idx


# ---------------------------------------------------------------- apply

def set_meta(page: str, title: str, desc: str) -> str:
    """Rewrite title/description in <title>, meta, OG/Twitter and the Article schema only.

    The old title is also the H1, the first H2 and the opening words of the
    body on these pages, so a global string replace would rewrite all of them.
    """
    t_attr, d_attr = html.escape(title, quote=True), html.escape(desc, quote=True)
    page = re.sub(r"<title>.*?</title>", lambda m: f"<title>{html.escape(title, quote=False)}</title>", page, count=1)
    for attr, key, val in (("name", "description", d_attr), ("property", "og:title", t_attr),
                           ("property", "og:description", d_attr), ("name", "twitter:title", t_attr),
                           ("name", "twitter:description", d_attr)):
        page = re.sub(rf'(<meta {attr}="{re.escape(key)}" content=")[^"]*(")',
                      lambda m: m.group(1) + val + m.group(2), page, count=1)

    def article(m: re.Match) -> str:
        data = json.loads(m.group(2))
        data["headline"], data["description"] = title, desc
        data["dateModified"] = TEST_DATE
        return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3)

    return re.sub(r'(<script type="application/ld\+json">)(\{"@context": "https://schema.org", "@type": "Article".*?)(</script>)',
                  article, page, count=1, flags=re.S)


def patch(slug: str, pages: dict, index: dict) -> str | None:
    path = COMPAT / slug / "index.html"
    page = path.read_text(encoding="utf-8")
    if 'class="quick-answer"' in page:
        return None
    p = pages[slug]
    v, a, b = p["verdict"], p["a"], p["b"]
    why = reason(page, v, a, b)

    page = set_meta(page, build_title(v, a, b), build_description(v, a, b, why))

    # Quick answer directly under the first H2 inside <main>.
    main = page.index("<main")
    h2_end = page.index("</h2>", main) + len("</h2>")
    page = page[:h2_end] + "\n      " + quick_answer(v, why, a, b) + page[h2_end:]

    card = mates_card(slug, v, a, b, pages, index)
    marker = "<h2>Related Compatibility Guides</h2>"
    if card and marker in page:
        page = page.replace(marker, card + marker, 1)

    page = re.sub(r"Updated [A-Z][a-z]+ \d{1,2}, 2026", f"Updated {TEST_DATE_HUMAN}", page, count=1)
    page = re.sub(r'"dateModified": "2026-\d\d-\d\d"', f'"dateModified": "{TEST_DATE}"', page)
    return page


def touch_sitemaps(slugs: set[str], dry: bool) -> int:
    n = 0
    for sm in SITEMAPS:
        s = sm.read_text(encoding="utf-8")
        def bump(m):
            nonlocal n
            n += 1
            return f"{m.group(1)}{TEST_DATE}{m.group(3)}"
        new = re.sub(
            r"(<(?:ns0:)?loc>https://www\.fishcareai\.com/compatibility/(?:"
            + "|".join(map(re.escape, slugs))
            + r")/</(?:ns0:)?loc>\s*<(?:ns0:)?lastmod>)([^<]+)(</(?:ns0:)?lastmod>)",
            bump, s)
        if not dry and new != s:
            sm.write_text(new, encoding="utf-8")
    return n


def apply(dry: bool) -> None:
    if not REPORT.exists():
        sys.exit(f"{REPORT} missing — run `select` first")
    with REPORT.open(encoding="utf-8") as fh:
        test = [r["slug"] for r in csv.DictReader(fh) if r["group"] == "test"]
    pages = load_pages()
    index = mates_index(pages)
    changed = []
    for slug in test:
        new = patch(slug, pages, index)
        if new is None:
            continue
        changed.append(slug)
        if not dry:
            (COMPAT / slug / "index.html").write_text(new, encoding="utf-8")
    bumped = touch_sitemaps(set(changed), dry) if changed else 0
    print(f"{'would patch' if dry else 'patched'} {len(changed)} of {len(test)} test pages; sitemap lastmod bumped {bumped}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("select")
    s.add_argument("export", type=Path)
    a = sub.add_parser("apply")
    a.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    select(args.export) if args.cmd == "select" else apply(args.dry_run)


if __name__ == "__main__":
    main()
