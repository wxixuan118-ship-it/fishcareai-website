# On-page audit + template fixes: compatibility & fish-health — 2026-09-20

Input: GSC page export (`fishcareai.com-Performance-on-Search-2026-09-20.xlsx`, 24 h) — all
`/compatibility/` and `/fish-health/` pages with position ≤ 20: **921 pages** (462 compatibility,
459 fish-health). Audited with `~/.claude/skills/onpage-audit/` (keyword = slug phrase:
`corydoras-and-guppy` → "corydoras and guppy", `neon-tetra-hiding` → "neon tetra hiding",
hub `/compatibility/koi/` → "koi tank mates"). Per-page results: `reports/onpage-audit-compat-fishhealth-2026-09-20.xlsx`.

Audit script fix: H1s inside `<header class="hero">` (outside `<main>`) were invisible to the
scorer, so all 445 pair pages were being marked "no H1". Patched to fall back to the whole document.

---

## 1. Findings by template

| Template | n | mean before | template faults |
|---|---|---|---|
| compatibility pair `/a-and-b/` | 445 | 74.6 | title 72–74 chars (truncates at 60); "A and B" phrase never in title/H1/H2/description; only `<img>` is the logo; 8 generic H2s → topic focus 33% |
| compatibility hub `/koi/` | 17 (91 on site) | 63.5 | no JSON-LD, no image, one paragraph, "koi tank mates" absent from body |
| fish-health symptom | 456 | 72.5 | title inverted ("Hiding Constantly in Neon Tetra?" vs query "neon tetra hiding"); H2→H4 skips (cause cards, TOC, CTAs); `#related` TOC anchor with no target; no outbound sources; 1.3–1.7 s TTFB (`cache-control: no-store`, every request hits Postgres) |
| fish-health species hub `/fish/x` | 3 | 71.3 | 162 words, no H2, no paragraph |

Technical checks (canonical, robots, viewport, HTTPS, CSR, JSON-LD validity) were green everywhere.

## 2. Compatibility fixes (this repo, applied)

`data-pipeline/upgrade_compatibility_onpage.py` — in-place patch of the rendered HTML (the v2
generator's raw catalogue is not in this checkout, and 39 pilot pages were hand-edited after
generation; those are skipped by pattern and untouched).

- 4,060 pair pages: title → `Can A and B Live Together? Compatibility Guide` (≤60, shorter fallbacks),
  H1 → `Can A and B Live Together?`, description rewritten with verdict + score, OG/Twitter/Article
  schema kept in sync, first H2 → `A and B Compatibility Overview`, last H2 → `Tank Size for A and B`,
  one photo per species in Species Profiles (480 px webp thumbs in `assets/compatibility/thumbs/`,
  built from `assets/encyclopedia/real/`; snails/shrimp have no photo). `corydoras` uses the slug
  form in title copy because the display name "Corydoras Catfish" splits the phrase.
- 91 hubs: intro section with photo + two paragraphs, list H2 → `X Tank Mates Ranked by Compatibility`,
  BreadcrumbList + CollectionPage JSON-LD.
- `sitemaps/compatibility-*.xml` lastmod → 2026-09-20.

Re-audit of the same 462 pages: pair mean **74.6 → 91.2** (430/445 in the 90s), hub mean
**63.5 → 93.2**. Remaining sub-90 pages are the untouched pilot set (corydoras-and-goldfish 67.6,
corydoras-and-oscar 69.3, angelfish-and-goldfish 77.5) and the boilerplate-density artifact.

Not fixed (content, not template): ~480-word bodies with the Overview paragraph duplicated verbatim
into FAQ answer 1; "Caution Points" showing "✅ No major issues" as filler; no outbound sources.

## 3. Fish-health fixes (species-app repo, branch `seo/title-and-heading-fixes`, NOT deployed)

Commits `3172999` (template) and `d352826` (ISR) on top of the unmerged `3972b30`. Verified with
`tsc` and `next build` (no DATABASE_URL); rendered with stubbed data → 87–89 on the audit
(real 650-word bodies should land ~90).

- `lib/fish-health-meta.ts`: subject = species name + problem *slug* phrase ("Neon Tetra Hiding
  Constantly", "Guppy Torn Fins", "Oscar White Spots (Ich)"); title/H1/description/alt/breadcrumb
  and three H2s lead with it.
- Cause cards + CTA boxes H4 → H3; TOC label no longer a heading; TOC built from rendered sections.
- Editorial note cites Merck Vet Manual + UF/IFAS.
- `/fish-health/fish/<species>`: H2 + intro paragraph.
- `revalidate = 3600` replaces `force-dynamic` on both routes (nothing prerenders at build).

Follow-ups outside the template: species `common_name` in the DB splits the slug phrase for
`platy` (Southern Platyfish), `weather-fish` (Dojo Loach), `otocinclus` (Otocinclus Catfish),
`rainbow-fish` (Rainbowfish), `betta-imbellis` (Crescent Betta) — those pages score 58–62 and
will stay there until the name or slug changes.
