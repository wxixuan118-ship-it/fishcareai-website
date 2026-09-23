# Compatibility cluster: wrong facts, wrong scores — 2026-09-23

Trigger: `/compatibility/betta-fish-and-rosy-barb/` published **"✅ Compatible — 78/100"** for a
pairing with no shared temperature range, on a page whose own comparison table read
"Temperament: ❌ Risk" three lines above a card saying "✅ No major compatibility issues identified
for this pair."

## 1. Root causes

**Data.** The 60 species added by `generate_compatibility_pages_v2.py` came from `08_raw.json`, a
Gemini enrichment pass that was never fact-checked. Rosy barb was stored as `size_cm: "5-7"`,
`schooling: false`, `min_tank_liters: 20`, `temp 22-28°C`. Seriously Fish gives 100 mm SL,
a shoal of 8-10, ~90 l, and **16-24°C** — a cool-water fish, not a tropical one. 180 of the 200
records carried `schooling: false`, including every Corydoras and most tetras.

**Parsers.**
- `_number()` used `re.search`, taking the *lower* bound of every size range. 198 of 200 records
  store a range, so adult size was systematically understated across the catalogue
  (rosy barb published as a 2.0-inch fish).
- `_temperament()` joined *every* value in the behaviour dict, so `activity_level: "moderate"`
  matched the "moderate" keyword and graded peaceful shoalers as semi-aggressive.

**Scoring.** Temperature, pH and temperament were weighted inputs with no floor, so a fatal
mismatch could be outvoted by four benign ones. Nothing ever wrote a temperament mismatch into
`issues`, which is why the Caution Points card fell back to its "no major issues" filler.
`water: "coldwater"` (goldfish, koi) was compared like saltwater-vs-freshwater, so 156 pages told
readers that two freshwater fish "require different water types".

**Copy.** The verdict paragraph hardcoded "neither poses a major aggression risk to the other" on
every page scoring 75+, and the aggression FAQ quoted `issues[0]` — often a pH note. The visible
byline was pinned to "Updated August 18, 2026".

## 2. Fixes

`data-pipeline/generate_compatibility_pages_v2.py`
- `V2_FACTS`: verified sci name, temperature, pH, adult size, min group, min tank, swim zone,
  `eats_small` and water type for all 60 v2 species. Freshwater figures from Seriously Fish
  species profiles (44 scraped, scientific names confirmed against each profile's own title);
  the 5 species SF does not cover and the 11 marine species use standard hobby references.
  Temperament and group size are editorial calls from each profile's behaviour section.
  The old derivations remain as the fallback for any unchecked slug.
- `_number()` takes the top of a range; `_temperament()` reads only `temperament` and
  `aggression_level`.
- Blocking gates, all applied before the verdict and all writing a reason into `issues`:
  no shared temperature → cap 38; ranges meeting within 3°F → cap 52; pH ranges that miss → cap 52;
  pH overlap under 0.4 → cap 65; temperament ≤15 → cap 38; ≤30 → cap 58.
- Coldwater × tropical is no longer treated as a different water type; it states the temperature
  constraint and lets the overlap score decide (goldfish + weather loach now scores 98).
- The discus/cardinal-tetra editorial override runs *after* the caps, not before them.
- `rebuild_sitemap()` detected that `sitemap.xml` is now a `<sitemapindex>`; appending `<url>`
  nodes to it would have produced an invalid sitemap. It refreshes `lastmod` in
  `sitemaps/compatibility-*.xml` as a text substitution instead.

`data-pipeline/generate_compatibility_pages.py`
- Verdict paragraph describes the actual temperaments and, for caution/incompatible pages, quotes
  the real findings instead of "some combination of water parameter differences, size mismatch,
  or temperament issues".
- Aggression FAQ quotes the behaviour issue, not `issues[0]`. Temperature FAQ gives both ranges
  instead of the bare string "No overlap".
- `UPDATED` / `UPDATED_HUMAN` drive the byline and `dateModified`.

## 3. Pipeline order

`generate_compatibility_pages_v2.py` → `upgrade_compatibility_pilot.py` → `upgrade_compatibility_onpage.py`

The pilot script matches the generator's raw `<h2>Compatibility Overview</h2>` and rewrites the
title; the on-page script then skips those 34 pages because their title no longer matches its v1
pattern. Running on-page first makes the pilot script fail with
`Expected one overview replacement, found 0`.

## 4. Result

4,099 pair pages + 91 hubs rebuilt. 1,104 of 4,095 pairs changed verdict
(compatible 1,451 → 1,464, caution 862 → 810, incompatible 1,782 → 1,821; the totals move less
than the individual pages do, because fixing `_temperament` raised as many pairs as the new caps
lowered). Betta × rosy barb: **Compatible 78 → Not Compatible 38**, citing the 76-82°F / 61-75°F
split and the aggressive/peaceful mismatch.

| check | before | after |
|---|---|---|
| "❌ Risk" + "No major compatibility issues identified" | 593 | 0 |
| "❌ Risk" + "neither poses a major aggression risk" | 221 | 0 |
| "Aquarium species" instead of a scientific name | 4,099 | 0 |
| table shows "❌ No overlap" yet verdict is Compatible | 13 | 0 |
| byline stamped "August 18, 2026" | 4,099 | 0 |

On-page SEO from the 2026-09-20 pass is intact: 30-page random sample, audit mean 90.6 → 91.7,
minimum 90.2, no page regressed more than 1 point. The two hand-built pages
(`betta-fish-and-amano-shrimp`, `betta-fish-and-ghost-shrimp`) and `koi-and-pleco` /
`koi-and-turtles` are outside the generator and untouched.

## 5. SERP copy: stop answering the question in the snippet (2026-09-24)

The description template gave the whole page away — "Betta Fish and Rosy Barb compatibility: not
compatible, score 38/100" — so a searcher had no reason to click. Titles were already questions and
did not leak, and the 34 pilot pages already used a question-plus-specific-risk description; the
other 4,065 pages now follow that pattern.

`upgrade_compatibility_onpage.build_description()` and the generator's `meta_desc` both produce:

> Can {A} and {B} share a tank? Compare their temperature, pH, temperament and adult size, plus the
> tank size both species need.

with three shorter fallbacks for long species names. `verdict` and `score` stay in the signature
because the caller passes them and the pilot pass shares the shape.

`koi-and-pleco` and `koi-and-turtles` are hand-built pages outside the 91-species catalogue, so no
pipeline stage refreshes them; their descriptions were rewritten by hand to match (both name the
actual risk on the page — pleco rasping at koi slime coat, turtles biting fins).

Scan of all 4,190 pair pages and hubs: **0** titles, meta descriptions, `og:description` or
`twitter:description` contain a verdict word or an `n/100` score. Description lengths 128-160
(median 146), every one carries the exact "A and B" phrase except the three known display-name
outliers (`corydoras-and-oscar`, and the two hand-built betta-shrimp pages). Audit mean on the same
30-page sample is unchanged at 91.7.

**Still answers the question in the SERP: the FAQPage JSON-LD.** Its first answer opens "Generally
not recommended." and Google can surface that in rich results and AI Overviews. It was left alone
deliberately — Google's structured-data guidelines require FAQ answers to be complete, so a
deliberately vague one risks the markup being ignored, and it would be a worse page for the reader
who does click. If the snippet leak matters more than the markup, the honest option is to drop the
FAQPage block from these pages rather than to hollow out the answers.

## 6. Not done

- `08_raw.json` itself is unchanged. `V2_FACTS` shadows it for the compatibility cluster, but the
  same 180 `schooling: false` records and 198 truncated size ranges still feed anything else that
  reads that file — the `/species/` encyclopedia and `/wiki/` pages should be checked next.
- Species `desc` paragraphs still come from the enrichment pass. They are not wrong so much as
  generic; the rosy barb's still opens "known for its vibrant coloration and peaceful nature"
  without mentioning that it is a cool-water shoaler.
- The predation rule (`size ratio ≥ 3` + `eats_small`) is unchanged. It puts goldfish × rosy barb
  at 32 on a 3.08 ratio, which is the rule working as written but close enough to the boundary to
  be worth revisiting.
