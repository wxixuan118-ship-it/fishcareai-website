# 2026-09-19 — Fish identification keyword cannibalization

Four URLs were rotating for the same "fish identification" queries with 0 clicks:
identify.fishcareai.com/ (23 imp), /fish-identification-chart (16), www/tools/fish-identification/ (12, already 301), /freshwater-fish-identification (4).

## Keyword → URL map
| Cluster | Owner |
|---|---|
| **what fish is this** (primary) — fish identifier / fish identification / identify fish as secondary | identify.fishcareai.com/ |
| fish identification chart (with pictures) | identify.fishcareai.com/fish-identification-chart |
| freshwater fish identification (chart / species) | identify.fishcareai.com/freshwater-fish-identification |
| www/tools/fish-identification/ | none — 301 to identify home (vercel.json + nginx.conf) |

## fish-identification-project (identify subdomain, repo wxixuan118-ship-it/fish-identification)
- Home: primary keyword stays "what fish is this" (title/H1 unchanged from the 2026-09-06 optimisation); description, opening paragraph and preview-img alt now carry the exact phrase, with "fish identification" as the secondary term (13 mentions). Preview img has width/height. Audit 95.1 (slug check is n/a on a homepage).
- /fish-identification-chart: H1 added, title "Fish Identification Chart with Pictures: 40 Species", photo column (40 Wikimedia CC/PD thumbnails in public/assets/chart/), habitat sub-chart cards, FAQ, WebPage+Breadcrumb+FAQ JSON-LD. Audit 98.4.
- /freshwater-fish-identification: rebuilt as a 33-species picture chart + body-shape and fin key + FAQ + JSON-LD; 473 → ~1,500 words. Audit 98.4.
- Other 8 subpages: hero H2 promoted to H1 (they had no H1).
- Deploy: hosted on Anysites (node server.js behind Caddy) — not Vercel; nothing pushed yet.

## fishcareai-website (this repo)
- Deleted tools/fish-identification/index.html (self-canonical duplicate behind the 301).
- guides/index.html: new "Fish identification" link block with exact-match anchors to the identify pages.
- Anchors "Fish Identify" → "Fish Identification" (home cards, 3 disease pages, build-disease-hubs.py).
- image-credits/index.html: 58 credit lines for the chart thumbnails.

- /saltwater-fish-identification: rebuilt as a 26-species picture chart + family key + fins/teeth key + regions + FAQ + JSON-LD. Audit 69.3 → 98.4.
- /reef-fish-identification: rebuilt as a 24-species picture chart + family key + depth tips + regions table + FAQ + JSON-LD. Audit 69.3 → 98.4.
- Six remaining subpages rebuilt as picture charts with a key, FAQ and WebPage+Breadcrumb+FAQ JSON-LD (all 69–75 → 98.4):
  /caribbean-fish-identification (21 sp.), /florida-fish-identification (26), /gulf-of-mexico-fish-identification (26),
  /salmon-identification (7 + gums/spots/tail table), /parrot-fish (12, both colour phases), /butterfly-fish (13 + care table).
- image-credits/index.html: 125 credit lines in total for the chart thumbnails (public/assets/chart/, 2.1 MB).

## Same day, part 2 — subdomain → subfolder
identify.fishcareai.com was starting from zero authority (subdomains do not inherit the root's links), and 242 www pages
linked the raw anysites host in the nav. The identifier now lives at **https://www.fishcareai.com/identify/**.

- www nginx.conf: `location ^~ /identify/` proxies to the identify app's anysites origin (same pattern as /species), sends
  `X-FishCare-Proxy: 1`; `/identify` and the old `/tools/fish-identification/` paths 301 to `/identify/`.
- identify app server.js: strips the `/identify` prefix; GET/HEAD on any host without the proxy header
  (identify.fishcareai.com, *.anysites.app) 301s to `https://www.fishcareai.com/identify<path>`; localhost untouched.
- All 11 pages: canonical/og/JSON-LD/internal links/asset paths/API path rewritten to `/identify/...`; WebSite schema → www.
- www: 247 files updated (`/identify/` in the sitewide nav instead of the anysites URL, no target=_blank), image credits,
  cluster generator scripts, site-compliance.js; `sitemaps/identify.xml` added to the sitemap index.
- Deploy order: identify app first, then www (the app's old-host redirect points at /identify/, which only exists once
  the www container has the new nginx.conf).
