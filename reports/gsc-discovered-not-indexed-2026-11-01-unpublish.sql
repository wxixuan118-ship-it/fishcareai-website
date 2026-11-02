-- Unpublish 8 fish-health pages from the GSC "Discovered - currently not indexed" export (2026-11-01).
-- Run in the Supabase SQL editor for fishcareai-species-app.
-- Cold-tail species only (threadfin rainbowfish, tropheus/venustus/turquoise, watchman goby, zebra pleco,
-- upside-down catfish): ~700-word template pages with no /aquarium-fish-diseases/ hub to carry the topic.
-- Every loader filters on published = true, so within ~1h (revalidate 3600) they drop out of
-- /fish-health/sitemap.xml and the species lists, and the pages 404.
-- variatus-platy-pale-color is in the list although the platy is a common species: the page itself drew
-- 11 impressions and 1 click in 3 months, so it is cold on its own terms.
-- The other 12 fish-health URLs in that export are left published on purpose - they are common species
-- (zebra danio, weather loach, white cloud mountain minnow, three-spot gourami, yoyo/zebra loach).
--
-- NOTE (2026-11-02): the 404 is produced by RETIRED_HEALTH_SLUGS in fishcareai-species-app
-- lib/consolidated.ts, which is where the 2026-10-30 batch was actually retired. The 8 slugs below were
-- added there on 2026-11-02. This statement is the matching database cleanup - useful so the rows stop
-- being counted as published, but not required for the pages to drop out.
-- Undo: run the same statement with published = true.
UPDATE fish_health_content SET published = false WHERE slug IN (
  'threadfin-rainbowfish-losing-color',
  'tropheus-cichlid-sinking',
  'turquoise-rainbowfish-floating',
  'upside-down-catfish-bloated',
  'variatus-platy-pale-color',
  'venustus-cichlid-sinking',
  'watchman-goby-rubbing',
  'zebra-pleco-bulging-eyes'
);
