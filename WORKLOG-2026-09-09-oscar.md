# Oscar Fish Keyword Coverage Audit — 2026-09-09

77 supplied keywords mapped to pages. **16 new cluster pages** created under
`/guides/oscar-fish-care/`; existing pages marked ✅ 已覆盖.

Generator: `data-pipeline/generate_oscar_cluster.py` (re-runnable, idempotent).
The pillar `/guides/oscar-fish-care/index.html` was **not** overwritten — it
received a "The Oscar Fish Care Series" block plus 16 contextual deep links,
matching how the koi pillar was handled.

---

## 1. Already covered (existing pages)

| Page | Status | Keywords served |
|---|---|---|
| `/guides/oscar-fish-care/` | ✅ 已覆盖 (updated) | oscar fish · oscar fish care · how to care for oscar fish · oscar fish care guide |
| `/calculators/oscar-fish-tank-size/` | ✅ 已覆盖 | oscar fish tank size (calculator intent) |
| `/compatibility/oscar/` | ✅ 已覆盖 | oscar tank mates hub, 90 pairing pages |
| `/aquarium-fish-diseases/oscar-diseases/` | ✅ 已覆盖 | oscar disease index (thin — 1 item, auto-generated) |
| `/species/oscar` | ✅ 已覆盖 | species profile (proxied species app) |
| `/guides/oscar-care-guide/` | ✅ noindex + 301 → pillar | duplicate; removed from `sitemaps/guides.xml` |

### Pairing keywords already covered by `/compatibility/*`

| Keyword | Existing page |
|---|---|
| oscar fish and angelfish | `/compatibility/angelfish-and-oscar/` |
| oscar fish and pleco | `/compatibility/bristlenose-pleco-and-oscar/` (+ clown-pleco, zebra-pleco) |
| oscar fish and goldfish | `/compatibility/goldfish-and-oscar/` |
| oscar fish and discus | `/compatibility/discus-and-oscar/` |
| oscar fish and arowana | `/compatibility/oscar-and-silver-arowana/` |
| oscar fish and green terror | `/compatibility/green-terror-cichlid-and-oscar/` |
| oscar fish and silver dollar | `/compatibility/oscar-and-silver-dollar/` |
| oscar fish and catfish | `/compatibility/glass-catfish-and-oscar/` |
| oscar fish and bichir | `/compatibility/oscar-and-senegal-bichir/` |

---

## 2. New pages created (16)

| # | URL | Primary keywords |
|---|---|---|
| 1 | `/guides/oscar-fish-care/tank-size/` | oscar fish tank size · oscar fish tank · oscar fish aquarium |
| 2 | `/guides/oscar-fish-care/water-parameters/` | oscar fish water temperature · oscar fish temperature · oscar fish water parameters · oscar fish pH |
| 3 | `/guides/oscar-fish-care/food/` | oscar fish food · what do oscar fish eat · what to feed oscar fish · best food for oscar fish · how often to feed oscar fish · oscar fish feeding · oscar fish feeding chart |
| 4 | `/guides/oscar-fish-care/size-growth/` | oscar fish size · how big do oscar fish get · oscar fish growth rate |
| 5 | `/guides/oscar-fish-care/lifespan/` | oscar fish lifespan · how long do oscar fish live |
| 6 | `/guides/oscar-fish-care/types/` | types of oscar fish · oscar fish colors · tiger / albino / red / black / white / lemon / long fin oscar fish |
| 7 | `/guides/oscar-fish-care/male-vs-female/` | male vs female oscar fish · oscar fish male or female |
| 8 | `/guides/oscar-fish-care/breeding/` | oscar fish breeding · oscar fish eggs · oscar fish mating · baby oscar fish · pregnant oscar fish |
| 9 | `/guides/oscar-fish-care/tank-mates/` | oscar fish tank mates · best tank mates for oscar fish · what fish can live with oscar fish · oscar + parrot fish / blood parrot / cichlids / jack dempsey / convict cichlid (no compat pages exist) |
| 10 | `/guides/oscar-fish-care/behavior/` | oscar fish aggressive · oscar fish fighting · oscar fish jumping |
| 11 | `/guides/oscar-fish-care/diseases/` | oscar fish diseases · oscar fish parasites · oscar fish fin rot · oscar fish cloudy eye |
| 12 | `/guides/oscar-fish-care/hole-in-the-head/` | oscar fish hole in the head |
| 13 | `/guides/oscar-fish-care/white-spots/` | oscar fish white spots |
| 14 | `/guides/oscar-fish-care/not-eating/` | oscar fish not eating · oscar fish lying on bottom · oscar fish hiding |
| 15 | `/guides/oscar-fish-care/color-change/` | oscar fish losing color · oscar fish turning white · oscar fish turning black · oscar fish black spots |
| 16 | `/guides/oscar-fish-care/swimming-problems/` | oscar fish bloated · oscar fish swollen belly · oscar fish swimming sideways · oscar fish swimming upside down · oscar fish gasping for air |

---

## 3. On-page SEO audit checklist (all 16 pages)

- Unique `<title>` ≤ 60 chars, primary keyword front-loaded — verified
- Unique `meta description` 120–160 chars — verified
- Exactly one `<h1>`, keyword-bearing; H2/H3 hierarchy with stable anchor IDs
- Self-referencing `rel=canonical`; `robots: index,follow,max-image-preview:large`
- OG + Twitter card tags with an absolute `og:image`
- 3 valid JSON-LD blocks per page: `BreadcrumbList` (4 levels), `Article`, `FAQPage`
- Visible FAQ section mirroring the FAQ schema (6–7 Q&As per page)
- Breadcrumb trail in markup matching the schema
- Internal linking: cluster-nav sidebar (18 links), in-body contextual links,
  "Related Oscar Fish Guides and Tools" block, tool sidebar
- No link points at a redirecting URL (`/wiki/oscar/` 301s to the pillar, so
  the species-profile link targets `/species/oscar` instead)
- Tables wrapped in `.tblwrap` for horizontal scroll on mobile; responsive grid
- HTML structure validated (no unclosed/stray tags); no console errors
- `sitemaps/guides.xml`: 16 URLs added, pillar `lastmod` bumped to 2026-09-09,
  the noindex `/guides/oscar-care-guide/` entry removed

---

## 4. Not done / follow-ups

- `/compatibility/` pages for **blood parrot cichlid**, **jack dempsey**,
  **convict cichlid**, **common pleco** and **pictus catfish** do not exist.
  These keywords are served by sections on the tank-mates page. Creating real
  pairing pages requires adding those species to the compatibility dataset,
  which regenerates the whole matrix — separate task.
- `/aquarium-fish-diseases/oscar-diseases/` is auto-generated by
  `scripts/build-disease-hubs.py` and currently lists a single symptom page.
  It would benefit from being re-run once more `/fish-health/oscar-*` pages exist.
- `guides/index.html` still lists two cards pointing at the same pillar URL
  ("Oscar Fish Care" and "Oscar Care Guide") — pre-existing duplication.
