# Algae Control cluster — 2026-09-19

Five pages from a user-supplied keyword table (27 keywords: 5 primary, 22 secondary). Coverage check
(`coverage.py`, live sitemap + repo): 3 covered, 12 partial, 12 new before this build.

Generator: `~/.claude/skills/fishcare-page/` with config `data-pipeline/clusters/algae/cluster.json`.
Keyword → URL map: `reports/algae-keyword-url-map.xlsx`.

---

## 1. Cannibalization check (before building)

| Existing page | Finding | Decision |
|---|---|---|
| `/species/siamese-algae-eater` (species app, live) | title "Siamese Algae Eater Care Guide" | New page targets a different intent: identification / true SAE vs flying fox vs chinese algae eater. No "care guide" in its title; links to the species profile. |
| `/species/chinese-algae-eater` (live) | species profile | "chinese algae eater fish" kept as a secondary keyword on the SAE page; linked, not rebuilt. |
| `/wiki/black-beard-algae/` | 176 words, noindex, not in live sitemap | Replaced by `/guides/black-beard-algae/`; stub deleted, 301 added in `vercel.json`, internal links repointed (home, wiki index, aquarium planner, guides hub). |
| `/wiki/brown-algae/`, `/wiki/blue-green-algae/`, `/wiki/green-water-algae/` | 160–184 words, noindex | Left as-is (noindex). Brown and blue-green algae covered as sections of the BBA guide. Their hub cards removed (they pointed at noindex stubs). |
| `/wiki/hair-algae/` | 1,537 words, indexed | "hairline algae" not rebuilt — one row in the BBA comparison table + link. Backlink block added. |
| `/tools/aquarium-equipment-calculator/` | filter GPH sizing | Canister guide links to it for the flow calculation; no overlap. |

## 2. Pages built

| URL | Primary keyword (vol / KD) | Secondary keywords | Score |
|---|---|---|---|
| `/guides/algae-eater-fish/` (pillar) | algae eater fish (8,100 / 19) | what eats algae · algae eaters · fish that clean tanks · aquarium algae eaters · algae eating aquarium fish · freshwater algae eaters · best algae eaters | 100 |
| `/guides/algae-eater-fish/siamese-algae-eaters/` | siamese algae eaters (1,600 / 15) | sae algae eater · chinese algae eater fish | 100 |
| `/guides/how-to-get-rid-of-algae-in-fish-tank/` | how to get rid of algae in fish tank (1,300 / 18) | aquarium algae control · aquarium algae control drops · tank algae control · remove algae in fish tank | 100 |
| `/guides/black-beard-algae/` | black beard algae (2,900 / 11) | black brush algae · black algae in fish tank · brown algae in fish tank · brown algae aquarium · green blue algae in aquarium · hairline algae · macro algae | 100 |
| `/guides/canister-filter/` | filtration canister (4,400 / 16) | tank canister filter · what type of fish tanks do aquariums use | 97.2 |

## 3. On-page audit (`audit.py cluster.json`, round 3)

```
/guides/algae-eater-fish/                        100.0  words 2009 · density 0.90% · focus 74.2%
/guides/algae-eater-fish/siamese-algae-eaters/   100.0  words 1547 · density 1.94% · focus 74.2%
/guides/how-to-get-rid-of-algae-in-fish-tank/    100.0  words 1704 · density 2.11% · focus 70.5%
/guides/black-beard-algae/                       100.0  words 1861 · density 2.58% · focus 73.4%
/guides/canister-filter/                          97.2  words 1784 · density 1.35% · focus 63.2%
   🟡 kw_url: slug is canister-filter (natural phrase) not filtration-canister — kept on purpose
   🟡 topic focus 63% — the "what type of fish tanks do aquariums use" H2 is a target keyword, kept
```

## 4. Images

- `assets/encyclopedia/real/algae-eater-fish-wikimedia-real.jpg` — Otocinclus.JPG, CC BY-SA 4.0 (pillar hero)
- `assets/encyclopedia/real/siamese-algae-eaters-wikimedia-real.jpg` — Crossocheilus.jpg, CC BY-SA 4.0
- `assets/encyclopedia/real/chinese-algae-eater-fish-wikimedia-real.jpg` — Algae eater (2341779669).jpg, CC BY-SA 2.0
- `assets/encyclopedia/real/black-beard-algae-wikimedia-real.jpg` — Compsopogon coeruleus (freshwater red alga) on aquarium plants, CC BY 4.0
- `assets/encyclopedia/real/canister-filter-wikimedia-real.jpg` — Potfilter.JPG, CC BY-SA 3.0
- credits appended to `/image-credits/`
- 5 SVG charts in `assets/guides/algae/` (regenerate with `data-pipeline/clusters/algae/charts.sh`)

## 5. Wiring

- `sitemaps/guides.xml` +5, `sitemap.xml` lastmod bumped
- `guides/index.html` → "Algae control" section rebuilt: Algae Eater Fish · How to Get Rid of Algae · Black Beard Algae · Siamese Algae Eaters · Hair Algae · Canister Filter Guide; ItemList positions 41–45 added
- backlink blocks (`<!--fishcare-page:algae-->`) on: `/wiki/hair-algae/`, `/guides/otocinclus-care-guide/`, `/guides/bristlenose-pleco-care-guide/`, `/guides/nerite-snail-care-guide/`, `/guides/amano-shrimp-care-guide/`, `/guides/pleco-care-guide/` — all six re-audited, scores up 1.0–1.6, none dropped
- `vercel.json`: 301 `/wiki/black-beard-algae/` → `/guides/black-beard-algae/`

## 6. Not done

- Nothing committed or pushed; `npm run indexnow` not run.
- `/wiki/brown-algae/`, `/wiki/blue-green-algae/`, `/wiki/green-water-algae/` stubs still exist (noindex). Candidates for a redirect to `/guides/black-beard-algae/#other-types` or their own pages later.
