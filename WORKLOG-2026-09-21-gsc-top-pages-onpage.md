# On-page fixes for GSC high-impression / low-CTR pages — 2026-09-21

Input: 54 URLs from the GSC page report (impressions ≥ 100, CTR mostly 0%). Audited live with
`~/.claude/skills/onpage-audit/` (keyword = slug phrase; pages whose title uses a different
phrasing were re-run with the likelier query). Results:
`reports/onpage-audit-gsc-top-pages-2026-09-21.xlsx`.

Three URLs are legacy 301s still reported by GSC (`how-to-take-care-of-a-fish-for-beginners`,
`freshwater-fish-care` → `fish-care-for-beginners`; `tools/tank-size-calculator` →
`tools/aquarium-size-calculator`) — nothing to fix. `/species` (50.8: no canonical, H2 or JSON-LD)
and `/fish-health` (81.5: no JSON-LD) are species-app pages, not touched here.

## Edits (this repo) — local re-audit, slug keyword

| page | before | after | what changed |
|---|---|---|---|
| /guides/molly-fish-care/ | 88.5 | 94.7 | title 78→52 ch, description with keyword, intro + alt |
| /guides/angelfish-care/ | 87.8 | 95.5 | title 76→57, description 221→150, intro + alt |
| /guides/discus-fish-care-requirements/ | 71.8 | 95.5 | title/H1 now "Discus Fish Care Requirements: …" (was "Discus Fish Tank Setup"), description, intro, alt |
| /guides/koi-fish-care/ | 88.2 | 98.4 | title 72→55, H1 leads with "Koi Fish Care for Beginners", description, alt |
| /tools/fish-compatibility-checker/ | 72.1 | 92.2 | title 86→53, H1 leads with "Fish Compatibility Checker", description ≤160, page wrapped in `<main>` (the audit — and any landmark-aware crawler — was scoring the first 139-word `<article>` card as the whole page) |
| /tools/aquarium-size-calculator/ | 69.8 / 95.4* | 82.1 / 98.8* | title/H1 "Aquarium & Fish Tank Size Calculator" so both query forms are covered (*= "fish tank size calculator", the bigger query) |
| /guides/koi-fish-care/size-growth/ | 73.1 | 85.7 (91.4 for "how big do koi fish get") | title 70→51, H1 carries both phrasings, description, intro |
| /guides/koi-fish-care/feeding/ | 71.9 | 88.1 (89.3 "what to feed koi fish") | title 72→52 "Koi Fish Feeding Chart: What to Feed Koi Fish by Season", H1, intro |
| /guides/betta-fish-care/feeding/ | 69.8 | 86.6 (89.4 "what do betta fish eat") | title/H1 add "Betta Fish Feeding Guide", intro |
| /guides/betta-fish-care/tank-setup/ | 77.5 | 88.2 | H1 leads with "Betta Fish Tank Setup", intro |
| /guides/betta-fish-care/types/ | 84.4 | 90.7 | intro phrase (body had 0 occurrences) |
| /guides/betta-fish-care/male-vs-female/ | 75.2 | 89.4 | title/H1 → "Male vs Female Betta Fish", intro |
| /guides/betta-fish-care/temperature/ | 84.4 | 93.9 | intro phrase ×2 (density was 0.17%) |
| /guides/betta-fish-care/tank-mates/ | 89.3 | 92.3 | body phrase |
| /guides/corydoras-care-guide/ | 83.2 | 96.3 | title → "Corydoras Care Guide: …" (matches slug), H1, intro, alt |

Pattern on the betta/koi sub-pages: H1 was a question ("How Big Do Koi Fish Get?"), slug a noun
("size-growth"), and neither phrase appeared in the body. Each intro now states both.

Remaining `kw_alt` reds on betta/koi sub-pages: those pages have no photo besides the logo.
`dead_hrefs` = in-page TOC anchors (audit artefact). Sitemap lastmod bumped for the 15 URLs.
Nothing pushed by this log; no IndexNow.
