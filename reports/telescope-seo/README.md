# Telescope goldfish on-page SEO delivery

Prepared 2026-09-09. The 79 supplied keywords map to 14 new English static pages (76 keywords) and one existing local Black Moor profile (3 keywords). New pages have not been deployed. Public requests to the Black Moor URL and proposed telescope pillar returned HTTP 403; this is not evidence of a 404, successful publication or indexation. See live-check.json.

## Files

- URL-MAPPING.md: all keywords, destination URLs and status.
- index.html: non-indexable local review table with working preview links.
- coverage.json: machine-readable mapping.
- audit.json: checks for all 14 new pages.
- ../../data-pipeline/telescope-cluster.json: editable page content.
- ../../data-pipeline/generate_telescope_cluster.py: repeatable generator.
- ../../scripts/audit-telescope.cjs: automated audit.

## Changes and validation

New pages have unique titles (25–60 characters) and descriptions (120–160 characters), exactly one H1, semantic sections, matching visible breadcrumbs and BreadcrumbList, self-canonical URLs, indexable robots metadata, Article and matching FAQ JSON-LD, OG/Twitter tags, visible references and editorial attribution. Date modified is used without inventing a publication date. Character lengths are editorial checks, not Google ranking rules.

All new pages are static HTML and linked from the cluster navigation. Discovery links were added to the guide index, general goldfish guide and Black Moor profile. The 14 URLs were appended to the guides sitemap without replacing unrelated entries. Existing uncommitted changes were preserved.

Command: node scripts/audit-telescope.cjs
Result: 14 pages, 0 errors. Checks include relative and absolute local internal links, fragment targets, unique IDs, sitemap membership, metadata and FAQ/schema consistency.

Browser QA: care pillar inspected at desktop width and 390px mobile width; tank-mates page also checked at 390px. Both mobile pages had document scrollWidth equal to clientWidth (390), with no horizontal page overflow. Review table contains 79 rows.

Existing Black Moor content was retained with a small discovery-link addition; the full existing page was not included in the 14-page certification. Existing photo assets are reused only for social-card metadata, labelled as general goldfish imagery; no generic fish photograph is presented as a telescope specimen.

## Limits

This is a local on-page audit, not a live technical crawl, Core Web Vitals measurement, veterinary review, Google indexing confirmation or ranking guarantee. FAQ markup does not guarantee a rich result. The existing site contains broader care recommendations that may differ from the new telescope-specific editorial guidance; unrelated articles were not rewritten. Published source recommendations differ, and the new pages explicitly identify planning assumptions and telescope-specific evidence gaps.
