"""Evaluate the 2026-09-28 GSC experiments: test vs control, before vs after.

Covers both experiments that launched on 2026-09-28:
  compatibility  reports/compat-ctr-test-2026-09-28.csv   (verdict-first titles)
  fish-health    reports/fish-health-deep-test-2026-09-28.csv (researched rewrites)

Input is a GSC Performance export made in *compare* mode (Date -> Compare), so
the "网页"/"Pages" sheet carries clicks, impressions and position for both
ranges. Either one unfiltered export or one per URL filter works; rows from
several files are merged. The range with the later start date is "post".

  python3 -I data-pipeline/ab_test_eval.py <gsc-compare.xlsx> [more.xlsx ...]

Each group's change is read against its own control: the site-wide CTR moves
with seasonality and index changes, so only the test-vs-control difference is
the effect. The 95% interval on "lift" (test CTR ratio / control CTR ratio)
comes from resampling pages, which respects that a few pages carry most clicks.
"""

from __future__ import annotations

import csv
import random
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPORTS = Path(__file__).resolve().parent.parent / "reports"
TESTS = {
    "compatibility": "compat-ctr-test-2026-09-28.csv",
    "fish-health": "fish-health-deep-test-2026-09-28.csv",
}
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
BOOT = 5000


def read_xlsx(path):
    """Minimal .xlsx reader (no openpyxl on this machine): {sheet: [[cell]]}."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    out = {}
    for sheet in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS):
        target = rels[sheet.get(REL)].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        rows = []
        for r in ET.fromstring(z.read(target)).iter("{%s}row" % NS["m"]):
            row = []
            for c in r.findall("m:c", NS):
                col = 0
                for ch in re.match(r"[A-Z]+", c.get("r", "A")).group():
                    col = col * 26 + ord(ch) - 64
                row.extend([None] * (col - 1 - len(row)))
                v = c.find("m:v", NS)
                if c.get("t") == "s":
                    row.append(shared[int(v.text)])
                elif c.get("t") == "inlineStr":
                    row.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
                else:
                    row.append(v.text if v is not None else None)
            rows.append(row)
        out[sheet.get("name")] = rows
    return out


def norm(url):
    return url.split("#")[0].split("?")[0].rstrip("/").lower()


def load_pages(paths):
    pages, ranges = {}, set()
    for path in paths:
        book = read_xlsx(path)
        sheet = next(v for k, v in book.items() if "网页" in k or "Pages" in k)
        head = sheet[0]

        def cols(*words):  # [pre, post] by the start date in the header
            idx = [i for i, h in enumerate(head) if i and h and any(w in h for w in words)]
            if len(idx) != 2:
                sys.exit(f"{path}: not a compare export (headers: {head})")
            return sorted(idx, key=lambda i: tuple(int(x) for x in re.findall(r"\d+", head[i])[:3]))

        ci, ii, pi = cols("点击次数", "Clicks"), cols("展示", "Impressions"), cols("排名", "Position")
        ranges.add(tuple(re.sub(r"\s*(点击次数|Clicks)\s*", "", head[i]).strip() for i in ci))
        for r in sheet[1:]:
            if not r or not r[0]:
                continue
            f = lambda i: float(r[i] or 0) if i < len(r) else 0.0
            pages[norm(r[0])] = {
                "c0": f(ci[0]), "c1": f(ci[1]), "i0": f(ii[0]), "i1": f(ii[1]),
                "p0": f(pi[0]), "p1": f(pi[1]),
            }
    return pages, ranges


def totals(rows):
    s = {k: sum(r[k] for r in rows) for k in ("c0", "c1", "i0", "i1")}
    s["ctr0"] = s["c0"] / s["i0"] if s["i0"] else 0.0
    s["ctr1"] = s["c1"] / s["i1"] if s["i1"] else 0.0
    s["pos0"] = sum(r["p0"] * r["i0"] for r in rows) / s["i0"] if s["i0"] else 0.0
    s["pos1"] = sum(r["p1"] * r["i1"] for r in rows) / s["i1"] if s["i1"] else 0.0
    return s


def lift(test, ctrl):
    t, c = totals(test), totals(ctrl)
    if not (t["ctr0"] and c["ctr0"] and c["ctr1"]):
        return None
    return (t["ctr1"] / t["ctr0"]) / (c["ctr1"] / c["ctr0"])


def boot_ci(test, ctrl, rng):
    draws = []
    for _ in range(BOOT):
        v = lift(rng.choices(test, k=len(test)), rng.choices(ctrl, k=len(ctrl)))
        if v is not None:
            draws.append(v)
    draws.sort()
    return draws[int(0.025 * len(draws))], draws[int(0.975 * len(draws))]


def report(label, test, ctrl, rng):
    print(f"\n  {label}")
    print(f"    {'':8} {'pages':>5}  {'impressions':>17}  {'clicks':>11}  {'CTR':>15}  {'position':>11}")
    for name, rows in (("test", test), ("control", ctrl)):
        s = totals(rows)
        print(f"    {name:8} {len(rows):>5}  {s['i0']:>7.0f} -> {s['i1']:>7.0f}  {s['c0']:>4.0f} -> {s['c1']:>4.0f}  "
              f"{s['ctr0']:>6.2%} -> {s['ctr1']:>6.2%}  {s['pos0']:>4.1f} -> {s['pos1']:>4.1f}")
    t, c = totals(test), totals(ctrl)
    did = (t["ctr1"] - t["ctr0"]) - (c["ctr1"] - c["ctr0"])
    imp = (t["i1"] / t["i0"]) / (c["i1"] / c["i0"]) if t["i0"] and c["i0"] and c["i1"] else None
    l = lift(test, ctrl)
    if l is None:
        print("    too few clicks to compare")
        return
    lo, hi = boot_ci(test, ctrl, rng)
    sig = "significant" if lo > 1 or hi < 1 else "not significant"
    print(f"    CTR diff-in-diff {did * 100:+.2f}pp | CTR lift vs control {l - 1:+.0%} "
          f"(95% CI {lo - 1:+.0%} to {hi - 1:+.0%}, {sig})"
          + (f" | impressions vs control {imp - 1:+.0%}" if imp else ""))


def main(paths):
    pages, ranges = load_pages(paths)
    rng = random.Random(20260928)
    for rng_pair in sorted(ranges):
        print(f"pre {rng_pair[0]}  |  post {rng_pair[1]}")
    for name, fn in TESTS.items():
        with open(REPORTS / fn) as fh:
            groups = list(csv.DictReader(fh))
        print(f"\n=== {name} ===")
        found = {g: [r for r in groups if r["group"] == g and norm(r["url"]) in pages] for g in ("test", "control")}
        for g in ("test", "control"):
            print(f"  {g}: {len(found[g])}/{sum(r['group'] == g for r in groups)} pages in export")
        rows = {g: [pages[norm(r["url"])] for r in found[g]] for g in found}
        report("all pages", rows["test"], rows["control"], rng)
        if "verdict" in groups[0]:
            for verdict in sorted({r["verdict"] for r in groups}):
                sub = {g: [pages[norm(r["url"])] for r in found[g] if r["verdict"] == verdict] for g in found}
                report(f"verdict = {verdict}", sub["test"], sub["control"], rng)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
