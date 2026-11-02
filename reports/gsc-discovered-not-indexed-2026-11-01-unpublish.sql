-- Unpublish 8 fish-health pages from the GSC "Discovered - currently not indexed" export (2026-11-01).
-- Run in the Supabase SQL editor for fishcareai-species-app.
-- Cold-tail species only (threadfin rainbowfish, tropheus/venustus/turquoise, watchman goby, zebra pleco,
-- upside-down catfish): ~700-word template pages with no /aquarium-fish-diseases/ hub to carry the topic.
-- Every loader filters on published = true, so within ~1h (revalidate 3600) they drop out of
-- /fish-health/sitemap.xml and the species lists, and the pages 404.
-- The other 12 fish-health URLs in that export are left published on purpose - they are common species
-- (zebra danio, weather loach, white cloud mountain minnow, three-spot gourami, platy, yoyo/zebra loach).
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
