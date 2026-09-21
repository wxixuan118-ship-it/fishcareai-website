# Discus / angelfish "health problems" hubs rebuilt — 2026-09-21

Input: on-page audit of the three "<species> health problems" clusters
(`reports/onpage-audit-health-problems-clownfish-discus-angelfish-2026-09-21.xlsx`, 85 pages).
The discus and angelfish hubs under `/aquarium-fish-diseases/` were 180–190-word stubs from
`scripts/build-disease-hubs.py` (GSC-coverage driven: 2 and 1 linked symptom pages), titled
"X Diseases" with zero occurrences of the target phrase — **52.5 / 100** each.

## Built

`scripts/build-health-problem-hubs.py` — content dict per species + renderer on the
`/aquarium-fish-diseases/clownfish/` CSS. Re-run it to regenerate; edit the dict, not the HTML.

| page | before | after | words |
|---|---|---|---|
| `/aquarium-fish-diseases/discus-diseases/` | 52.5 | **96.7** | 2,388 |
| `/aquarium-fish-diseases/angelfish-diseases/` | 52.5 | **96.7** | 2,427 |

Keyword: `<species> health problems` (secondary `<species> diseases`). Title
"Discus Health Problems: Symptoms, Diseases & Treatment"; H1 same; description 150 chars.
Remaining yellows are structural: slug is `-diseases` (kept — URL is live and linked), topic
focus 60–63% (30-row symptom tables), photo is jpg/png not webp.

Sections: intro + urgent-note + photo → symptom finder (3 tables, all 30 `/fish-health/<species>-<symptom>`
pages) → 8 disease profiles each linking its symptom guides → husbandry causes → pre-treatment
checklist → resources (species-app hub `/fish-health/fish/<species>`, guides cluster, compatibility,
calculator; angelfish also links the 5 marine-angelfish species hubs) → 8 FAQ → sources.
JSON-LD: BreadcrumbList, CollectionPage (+primaryImageOfPage), ItemList (30), FAQPage.

Photos reuse assets already live on the guide pages (`/assets/discus/orange-patterned-discus-fish.jpg`,
`/assets/angelfish/silver-angelfish-long-fins.png`); no new uploads, no image-credits change.

Template note: the clownfish hub never loads `/assets/fishcare-glass-redesign.css`, so the nav
that `site-compliance.js` injects renders as an unstyled link row (live too). The new hubs load
the stylesheet. Its `body:has(.hero) .links a` rule paints links off-white, hence the
`guide-links` class name.

## Wiring

- `scripts/build-disease-hubs.py`: `HANDBUILT = {"discus", "angelfish"}` — skipped on regeneration.
- `aquarium-fish-diseases/index.html`: the two cards now read "30 symptom guides".
- `assets/disease-search-index.json`: +57 entries so the hub search box finds every discus/angelfish symptom.
- `sitemaps/static.xml`: both hubs added (they were in no sitemap), lastmod 2026-09-21.
- Backlinks: `/guides/discus-fish-care/diseases/` tools card → discus hub;
  `/guides/angelfish-care/` "Common Health Problems" → angelfish hub.

Not done: clownfish hub (68.3) still titled "Clownfish Diseases"; species-app template items
from the audit (H1 "Discus Aggressive ? Causes" spacing, cause-card H3s, TTFB) live in the other repo.
Nothing pushed, no IndexNow.
