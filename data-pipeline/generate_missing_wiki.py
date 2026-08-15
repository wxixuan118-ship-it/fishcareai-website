"""
generate_missing_wiki.py
─────────────────────────
Generates 8 missing P0 species pages under /wiki/{slug}/index.html.
Matches the existing neon-tetra wiki page template exactly.
Run from the data-pipeline/ directory:
  python generate_missing_wiki.py
"""

import os
from pathlib import Path

REPO = Path(__file__).parent.parent
WIKI = REPO / "wiki"

SPECIES = [
  {
    "slug": "pea-puffer",
    "name": "Pea Puffer",
    "sci_name": "Carinotetraodon travancoricus",
    "sci_author": "Hora & Nair, 1941",
    "tag": "🌊 Freshwater · Nano Puffer",
    "origin": "Kerala, India (Pamba & Chaliyar Rivers)",
    "size": "0.8–1 in (2–2.5 cm)",
    "lifespan": "3–5 years",
    "care_level": "Intermediate",
    "care_badge": "bwarn",
    "family": "Tetraodontidae",
    "order": "Tetraodontiformes",
    "genus": "Carinotetraodon",
    "species_abbr": "C. travancoricus",
    "water_type": "Freshwater, tropical",
    "temp_f": "74–82°F",
    "temp_c": "23–28°C",
    "ph": "7.0–8.0",
    "gh": "5–15 dGH",
    "min_tank": "10 gallons (solo); 20 gal for a trio",
    "diet_type": "Carnivore (hard-shelled invertebrates)",
    "temperament": "Semi-aggressive / nippy",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Carinotetraodon_travancoricus.jpg/640px-Carinotetraodon_travancoricus.jpg",
    "img_alt": "Pea puffer (Carinotetraodon travancoricus) facing the camera, showing its distinctive golden-yellow belly",
    "img_caption": "The pea puffer — the world's smallest known pufferfish — is a personality-packed nano species from Kerala, India. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Pea Puffer Care Guide 2026: Tank Setup, Diet & Compatibility | FishCare AI",
    "meta_desc": "Complete pea puffer care guide: tank setup, diet of snails and live food, temperament, compatible tank mates, and breeding for Carinotetraodon travancoricus.",
    "og_title": "Pea Puffer Care Guide 2026: Tank Setup, Diet & Compatibility",
    "breadcrumb_label": "Pea Puffer",
    "taxonomy_intro": "The pea puffer belongs to the family Tetraodontidae — the true pufferfishes — making it a distant cousin of species like the green-spotted puffer and the figure-eight puffer. Unlike most puffer species, <em>Carinotetraodon travancoricus</em> is fully freshwater throughout its entire life cycle, requiring no salt. It was described in 1941 and is the world's smallest known pufferfish.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Tetraodontiformes"), ("Family","Tetraodontidae"),
      ("Genus","<em>Carinotetraodon</em>"), ("Species","<em>C. travancoricus</em>"),
    ],
    "habitat_text": "Pea puffers are endemic to a small region of southwestern India — primarily the Pamba River system in Kerala and a few other coastal rivers. Their native habitat is slow-moving, densely vegetated freshwater: shallow streams, rice paddies, flooded fields, and heavily planted river margins.",
    "habitat_bullets": [
      "<strong>Dense vegetation:</strong> thick stands of aquatic plants providing ambush territory for hunting invertebrates",
      "<strong>Warm tropical water:</strong> 74–82°F (23–28°C) with moderate to hard water — significantly harder than most Indian riverine fish",
      "<strong>Slow flow:</strong> minimal current; pea puffers are not strong swimmers",
      "<strong>Abundant live food:</strong> snails, small crustaceans, and aquatic insects make up the bulk of their diet",
    ],
    "water_rows": [
      ("Temperature","74–82°F (23–28°C)","74–82°F (23–28°C)"),
      ("pH","7.0–8.0","7.0–8.0"),
      ("Hardness (GH)","5–15 dGH","5–15 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Pea puffers prefer harder, more alkaline water than most nano fish — "
                   "pH 7.5–8.0 is ideal. Soft, acidic water (below pH 6.5) stresses them over time."),
    "tank_setup_text": "A 10-gallon tank is the minimum for a single pea puffer; a 20-gallon long is recommended for a trio or for pairing with carefully chosen tank mates. Key setup elements:",
    "tank_bullets": [
      "<strong>Dense planting:</strong> Java fern, Anubias, hornwort, and floating plants provide cover, reduce stress, and support a natural snail colony for live feeding",
      "<strong>Multiple sight breaks:</strong> driftwood, rocks, and tall plants prevent line-of-sight between individuals, reducing aggression",
      "<strong>Slow filtration:</strong> a sponge filter or gentle hang-on-back — strong flow stresses pea puffers",
      "<strong>No sharp objects:</strong> avoid abrasive decor; puffers lack scales and can injure their skin",
      "<strong>Lid required:</strong> pea puffers are curious jumpers",
    ],
    "extra_section_id": "behavior",
    "extra_section_title": "Behavior & Personality",
    "extra_section_content": """<p>Pea puffers are among the most personable fish in the freshwater hobby. They recognize their owners, follow a finger across the glass, and actively investigate everything in their tank. Each fish develops a distinct personality.</p>
<p>However, they are also notoriously territorial and nippy. Males especially will fight over territory and females, and even females may bully one another in cramped spaces. Tank mates must be chosen with extreme care — most experienced keepers recommend keeping pea puffers in a species-only tank or with only the most robust, fast-moving tank mates (see below).</p>
<div class="callout callout-warn"><strong>Warning:</strong> Never mix pea puffers with fin-nipped targets: guppies, bettas, or any slow, long-finned fish. They will be ruthlessly attacked.</div>""",
    "diet_text": "Pea puffers are obligate carnivores with a specialization for hard-shelled invertebrates. Their beak-like fused teeth grow continuously and must be worn down by hard food — a diet of only soft foods will lead to overgrown teeth, which prevents eating.",
    "diet_bullets": [
      "<strong>Best food:</strong> live or frozen blood worms, mini ramshorn snails (essential for beak wear), daphnia, brine shrimp",
      "<strong>Snails:</strong> a live colony of ramshorn or bladder snails in the tank gives pea puffers an interactive, enriching food source and keeps their beak trimmed",
      "<strong>Frozen food:</strong> frozen blood worms, cyclops, and mysis shrimp are widely accepted",
      "<strong>Avoid:</strong> flake food, pellets (rarely accepted); dried food only as a last resort",
    ],
    "diet_note": "<strong>Tip:</strong> Maintain a separate \"snail breeding tank\" — a small 2–5 gallon container with plants and ramshorn snails — to supply an ongoing live food source.",
    "tank_mates_text": "Pea puffers are notoriously difficult to keep with other species. In a well-planted 20-gallon tank, possible companions include:",
    "tank_mates_good": [
      "Fast-moving, short-finned fish: chili rasboras, ember tetras, neon tetras (watch for nipping)",
      "Otocinclus catfish (good algae cleaners; generally ignored)",
      "Amano shrimp (large enough to be mostly left alone in planted tanks)",
      "Malaysian trumpet snails (tolerated; small ramshorns will simply be eaten)",
    ],
    "tank_mates_avoid": "Slow, long-finned fish (bettas, guppies, angelfish), other puffers (high aggression), and shrimp smaller than Amano-size.",
    "health_issues": [
      ("<strong>Overgrown beak</strong>","caused by insufficient hard food; teeth become too long for the fish to eat; prevent with regular snail feeding; trim may require expert intervention"),
      ("<strong>Ich</strong>","white spots; treat with heat (82–86°F) and a puffer-safe medication — standard salt treatments should be avoided for scaleless fish"),
      ("<strong>Internal parasites</strong>","common in wild-caught specimens; treat with levamisole or praziquantel in a hospital tank before introduction"),
      ("<strong>Bloat</strong>","from constipation or bacterial infection; fast the fish and offer daphnia; persistent cases need antibacterial treatment"),
    ],
    "health_note": ("<strong>Note:</strong> Pea puffers lack scales, making them sensitive to medications containing copper or salt. "
                    "Always use puffer-safe treatments and dose at half-strength initially."),
    "toc_sections": [
      ("#taxonomy","Taxonomy"), ("#habitat","Natural Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#behavior","Behavior & Personality"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/dwarf-gourami/","🐟 Dwarf Gourami"),
      ("/wiki/chili-rasbora/","🔴 Chili Rasbora"),
      ("/wiki/ember-tetra/","🔥 Ember Tetra"),
      ("/wiki/cherry-shrimp/","🦐 Cherry Shrimp"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "The pea puffer is the world's smallest known pufferfish — a pint-sized predator no bigger than a marble, yet packed with intelligence, personality, and territorial attitude. Despite reaching just 1 inch in length, a well-kept pea puffer will stalk snails with single-minded intensity, investigate its keeper's face, and rule its tank with an assertiveness that belies its tiny frame. For aquarists who want a truly interactive freshwater fish in a nano setup, few species rival it.",
    "qf_extra": [("Min. school size", "Solo or trio (with space)")],
  },

  {
    "slug": "honey-gourami",
    "name": "Honey Gourami",
    "sci_name": "Trichogaster chuna",
    "sci_author": "Hamilton, 1822",
    "tag": "🌿 Freshwater · Nano Labyrinth Fish",
    "origin": "India and Bangladesh (Brahmaputra, Ganges basins)",
    "size": "1.5–2 in (4–5 cm)",
    "lifespan": "4–8 years",
    "care_level": "Beginner",
    "care_badge": "bgood",
    "family": "Osphronemidae",
    "order": "Anabantiformes",
    "genus": "Trichogaster",
    "species_abbr": "T. chuna",
    "water_type": "Freshwater, tropical",
    "temp_f": "71–82°F",
    "temp_c": "22–28°C",
    "ph": "6.0–7.5",
    "gh": "3–8 dGH",
    "min_tank": "10 gallons (pair); 20 gal for a group",
    "diet_type": "Omnivore",
    "temperament": "Peaceful, shy",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Trichogaster_chuna_male.jpg/640px-Trichogaster_chuna_male.jpg",
    "img_alt": "Male honey gourami showing vivid orange-honey coloration with dark throat patch during breeding condition",
    "img_caption": "A male honey gourami in full breeding color — the deep orange-honey body and dark throat are far more vibrant than the typical pet store coloration. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Honey Gourami Care Guide 2026: Tank Setup, Diet & Breeding | FishCare AI",
    "meta_desc": "Complete honey gourami care guide: tank setup, diet, compatible tank mates, breeding behavior, and water parameters for Trichogaster chuna.",
    "og_title": "Honey Gourami Care Guide 2026: Tank Setup, Diet & Breeding",
    "breadcrumb_label": "Honey Gourami",
    "taxonomy_intro": "The honey gourami belongs to the family Osphronemidae — the gouramis and related labyrinth fishes. It is a close relative of the dwarf gourami (<em>Trichogaster lalius</em>) but remains significantly smaller, considerably less aggressive, and more tolerant of imperfect water conditions, making it one of the best choices for a beginner's planted nano tank.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Anabantiformes"), ("Family","Osphronemidae"),
      ("Genus","<em>Trichogaster</em>"), ("Species","<em>T. chuna</em>"),
    ],
    "habitat_text": "Honey gouramis are native to densely vegetated, slow-moving waters of India and Bangladesh — including weedy ponds, rice paddies, and sluggish streams in the Brahmaputra and Ganges river basins. Like all labyrinth fish, they breathe atmospheric air via a specialized labyrinth organ above their gills.",
    "habitat_bullets": [
      "<strong>Dense surface vegetation:</strong> floating plants like water lettuce and frogbit provide cover for bubble-nest building",
      "<strong>Shallow, slow water:</strong> typically under 3 feet deep, with minimal current",
      "<strong>Soft to moderately hard water:</strong> slightly acidic to neutral pH",
      "<strong>Seasonal variation:</strong> habitats flood dramatically during monsoon; fish tolerate wide temperature and pH swings",
    ],
    "water_rows": [
      ("Temperature","71–82°F (22–28°C)","71–82°F (22–28°C)"),
      ("pH","6.0–7.5","6.0–7.5"),
      ("Hardness (GH)","2–10 dGH","3–8 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Honey gouramis are among the most adaptable gouramis for water quality, tolerating a wide pH and hardness range. "
                   "They are more disease-resistant than dwarf gouramis, which are plagued by Dwarf Gourami Disease (DGIV)."),
    "tank_setup_text": "A 10-gallon tank is sufficient for a pair of honey gouramis; a 20-gallon allows a small group (1 male to 2–3 females). Key setup elements:",
    "tank_bullets": [
      "<strong>Floating plants:</strong> essential for the male to build a bubble nest during breeding and for fish to shelter near the surface",
      "<strong>Dense mid-level planting:</strong> Java fern, Anubias, stem plants — honey gouramis are shy and need plant cover to feel secure",
      "<strong>Gentle flow:</strong> a sponge filter or spray bar diffuser; strong currents stress labyrinth fish",
      "<strong>Warm temperature:</strong> keep temperature stable; avoid cold drafts near the water surface — labyrinth fish breathe surface air and cold surface air can damage the organ",
      "<strong>Low light:</strong> subdued or planted-tank lighting reduces stress",
    ],
    "extra_section_id": "labyrinth",
    "extra_section_title": "Labyrinth Organ & Breathing",
    "extra_section_content": """<p>Like all gouramis, honey gouramis possess a labyrinth organ — a complex, lung-like chamber above the gill cavity that allows the fish to extract oxygen directly from atmospheric air. This adaptation evolved in oxygen-poor, stagnant waters.</p>
<p>In the aquarium, honey gouramis will regularly swim to the surface to gulp air — this is entirely normal. The labyrinth organ also enables them to survive briefly out of water, which is why they occasionally jump.</p>
<div class="callout"><strong>Care note:</strong> Always keep the aquarium warm near the surface. Honey gouramis breathe surface air, and consistently cold air above the water (in unheated rooms in winter) can cause respiratory infections in the labyrinth organ.</div>""",
    "diet_text": "Honey gouramis are omnivores with a preference for small, protein-rich foods. In the wild they eat zooplankton, small insects, and algae. In captivity:",
    "diet_bullets": [
      "<strong>Staple:</strong> small pellets or micro-flake formulated for tropical fish",
      "<strong>Frozen food:</strong> blood worms, brine shrimp, daphnia, cyclops — excellent condition food and essential for breeding",
      "<strong>Live food:</strong> micro worms, baby brine shrimp, fruit flies (flightless)",
      "<strong>Vegetables:</strong> blanched spinach or zucchini occasionally; some individuals accept spirulina-based food",
    ],
    "diet_note": "<strong>Tip:</strong> Feed small amounts twice daily. Honey gouramis are shy feeders — ensure food sinks or floats near them; they may lose out to faster tank mates at feeding time.",
    "tank_mates_text": "Honey gouramis are among the most peaceful community fish available. Excellent companions include:",
    "tank_mates_good": [
      "Nano tetras (ember tetra, chili rasbora, neon tetra)",
      "Corydoras catfish",
      "Otocinclus",
      "Cherry shrimp and neocaridina shrimp (adults generally safe)",
      "Nerite snails and mystery snails",
      "Other peaceful nano fish",
    ],
    "tank_mates_avoid": "Aggressive or nippy fish (tiger barbs, cichlids), larger gouramis (may bully), betta fish (incompatible temperaments).",
    "health_issues": [
      ("<strong>Velvet</strong>","golden dust-like coating; treat with copper-based medication and reduce light"),
      ("<strong>Ich</strong>","white spots; temperature increase to 82°F and appropriate medication"),
      ("<strong>Bacterial infections</strong>","usually linked to poor water quality or stress; maintain clean water and consider antibacterial treatment"),
      ("<strong>Labyrinth organ infection</strong>","caused by breathing cold surface air; maintain warm, humid space above the water line"),
    ],
    "health_note": ("<strong>Note:</strong> Unlike dwarf gouramis, honey gouramis are NOT affected by Dwarf Gourami Iridovirus (DGIV). "
                    "This makes them a significantly more robust choice for the community aquarium."),
    "toc_sections": [
      ("#taxonomy","Taxonomy"), ("#habitat","Natural Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#labyrinth","Labyrinth Organ"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/dwarf-gourami/","🐟 Dwarf Gourami"),
      ("/wiki/pea-puffer/","🐡 Pea Puffer"),
      ("/wiki/chili-rasbora/","🔴 Chili Rasbora"),
      ("/wiki/ember-tetra/","🔥 Ember Tetra"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "The honey gourami is one of the best-kept secrets in the freshwater hobby. Smaller, shyer, and more disease-resistant than its popular cousin the dwarf gourami, it rewards patient keepers with spectacular honey-orange coloration in breeding males, gentle community-tank behavior, and an endearing personality. At just 1.5–2 inches long, it is perfectly scaled for a planted nano or community tank of 10 gallons or more.",
    "qf_extra": [],
  },

  {
    "slug": "chili-rasbora",
    "name": "Chili Rasbora",
    "sci_name": "Boraras brigittae",
    "sci_author": "Vogt, 1978",
    "tag": "🌿 Freshwater · Nano Blackwater Fish",
    "origin": "Southwestern Borneo, Indonesia",
    "size": "0.6–0.8 in (1.5–2 cm)",
    "lifespan": "4–8 years",
    "care_level": "Intermediate",
    "care_badge": "bwarn",
    "family": "Cyprinidae",
    "order": "Cypriniformes",
    "genus": "Boraras",
    "species_abbr": "B. brigittae",
    "water_type": "Freshwater, tropical (blackwater)",
    "temp_f": "68–82°F",
    "temp_c": "20–28°C",
    "ph": "4.0–7.0",
    "gh": "1–6 dGH (very soft)",
    "min_tank": "5 gallons (nano); 10 gal for a larger school",
    "diet_type": "Micro-predator / Omnivore",
    "temperament": "Peaceful, schooling",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Boraras_brigittae.jpg/640px-Boraras_brigittae.jpg",
    "img_alt": "School of chili rasboras with vivid red bodies and black lateral stripe in a blackwater planted aquarium",
    "img_caption": "Chili rasboras in a blackwater aquarium — their vivid red coloration is at its best against dark substrate and tannin-stained water. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Chili Rasbora Care Guide 2026: Nano Tank Setup & Blackwater Tips | FishCare AI",
    "meta_desc": "Complete chili rasbora care guide: blackwater setup, feeding micro foods, school size, compatible tank mates, and water parameters for Boraras brigittae.",
    "og_title": "Chili Rasbora Care Guide 2026: Nano Tank Setup & Blackwater Tips",
    "breadcrumb_label": "Chili Rasbora",
    "taxonomy_intro": "The chili rasbora belongs to the genus <em>Boraras</em> — a group of micro-rasboras separated from the larger <em>Rasbora</em> genus in 1993. The genus name is a reverse anagram of <em>Rasbora</em>. <em>Boraras brigittae</em> is one of the smallest aquarium fish available and one of the most strikingly colored nano fish in the freshwater hobby.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Cypriniformes"), ("Family","Cyprinidae"),
      ("Genus","<em>Boraras</em>"), ("Species","<em>B. brigittae</em>"),
    ],
    "habitat_text": "Chili rasboras are native to the blackwater peat swamp forests of southwestern Borneo. Their natural habitat is among the most extreme freshwater environments on earth:",
    "habitat_bullets": [
      "<strong>Blackwater:</strong> water stained dark amber-brown by tannins from decomposing peat and leaf litter",
      "<strong>Extremely acidic:</strong> pH as low as 3.5–4.5 in wild habitats",
      "<strong>Very soft water:</strong> near-zero mineral content (GH under 2 dGH)",
      "<strong>Warm but variable temperature:</strong> 75–82°F in the rainy season, cooler in dry season",
      "<strong>Dense shade:</strong> forest canopy blocks most light; fish are adapted to low light",
    ],
    "water_rows": [
      ("Temperature","75–82°F (24–28°C)","68–82°F (20–28°C)"),
      ("pH","3.5–5.0 (wild)","4.0–7.0 (captive-bred tolerate up to 7)"),
      ("Hardness (GH)","&lt;1 dGH","1–6 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;10 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Captive-bred chili rasboras are more tolerant than wild fish — they can adapt to pH up to 7.0 in soft water. "
                   "However, colors are most vivid and spawning most successful in soft, acidic blackwater (pH 5.5–6.5, GH 1–4). "
                   "Adding Indian almond leaves or peat filtration improves coloration significantly."),
    "tank_setup_text": "A 5-gallon nano tank can house a school of 8–10 chili rasboras, though a 10-gallon allows a more impressive group of 15–20. Ideal setup:",
    "tank_bullets": [
      "<strong>Blackwater aesthetics:</strong> dark substrate (black sand), Indian almond leaves, spider wood, and tannin-releasing botanicals",
      "<strong>Dense planting:</strong> Java moss, Anubias nana petite, mini Bucephalandra — low-light plants suited to soft water",
      "<strong>Floating plants:</strong> Salvinia, Frogbit, or duckweed to diffuse light and mimic the dense Bornean canopy",
      "<strong>Gentle flow:</strong> sponge filter only; chili rasboras are easily overwhelmed by strong current",
      "<strong>Dark background:</strong> black or natural dark background; enhances coloration and reduces skittishness",
    ],
    "extra_section_id": "schooling",
    "extra_section_title": "Schooling & Behavior",
    "extra_section_content": """<p>Chili rasboras are schooling fish that feel insecure in small numbers. A minimum of 8–10 fish is recommended; larger schools of 15–20 produce much bolder behavior and more vivid group swimming displays. In small groups they become shy and tend to hide.</p>
<p>In a well-planted blackwater tank with a large school, chili rasboras display remarkable color — the red body intensifies and the black lateral stripe becomes sharply defined. Males in breeding condition show the most vivid coloration and will display to females by flaring their fins.</p>
<div class="callout"><strong>Quick fact:</strong> Chili rasboras are one of the few nano fish that will comfortably share a 5-gallon tank with a single betta fish — their speed and tiny size make them largely immune to betta aggression. That said, individual betta temperaments vary widely.</div>""",
    "diet_text": "Chili rasboras are micro-predators in the wild, eating tiny zooplankton, small insects, and insect larvae. Their small mouths require appropriately sized food:",
    "diet_bullets": [
      "<strong>Staple:</strong> micro-pellets specifically formulated for nano fish (Hikari Micro Pellets, Sera Micron), or very finely crushed flake",
      "<strong>Best condition food:</strong> micro worms, baby brine shrimp (newly hatched), Walter worms, infusoria",
      "<strong>Frozen:</strong> cyclops (small enough), daphnia (small), baby brine shrimp",
      "<strong>Avoid:</strong> standard-size pellets or flake — chili rasboras cannot eat food larger than about 0.5mm",
    ],
    "diet_note": "<strong>Tip:</strong> Feed micro amounts 2–3 times daily. Overfeeding in a nano tank quickly degrades water quality; chili rasboras do better with small, frequent meals than one large feeding.",
    "tank_mates_text": "Chili rasboras are peaceful and fragile — tank mates must be chosen carefully to avoid predation or competition. Good companions include:",
    "tank_mates_good": [
      "Other micro-rasboras (Boraras species)",
      "Pygmy corydoras (Corydoras pygmaeus, C. habrosus)",
      "Ember tetras (similar size and temperament)",
      "Small shrimp — Neocaridina (cherry shrimp), caridina; juvenile shrimp may occasionally be eaten",
      "Otocinclus (peaceful algae cleaners)",
      "Betta fish (only in larger tanks with careful observation; individual temperaments vary)",
    ],
    "tank_mates_avoid": "Any fish large enough to swallow them (most tetras over 1.5 inches, gouramis, cichlids), aggressive species, or fast feeders that will outcompete them for food.",
    "health_issues": [
      ("<strong>Velvet (Oodinium)</strong>","extremely common in chili rasboras; appears as golden-dust coating; treat with copper-based medication in a hospital tank; remove invertebrates first"),
      ("<strong>Ich</strong>","white spots; temperature increase to 82°F plus medication"),
      ("<strong>Bacterial infection</strong>","usually from water quality issues; maintain pristine soft-water conditions"),
      ("<strong>Wasting / failure to thrive</strong>","often caused by feeding adult-size food they cannot eat; ensure food is appropriately micro-sized"),
    ],
    "health_note": ("<strong>Note:</strong> Chili rasboras are sensitive to water quality — their natural habitat has near-zero nitrates. "
                    "Keep nitrates below 10 ppm with regular small water changes."),
    "toc_sections": [
      ("#taxonomy","Taxonomy"), ("#habitat","Natural Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#schooling","Schooling & Behavior"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/ember-tetra/","🔥 Ember Tetra"),
      ("/wiki/pygmy-corydoras/","🐾 Pygmy Corydoras"),
      ("/wiki/neon-tetra/","💙 Neon Tetra"),
      ("/wiki/cherry-shrimp/","🦐 Cherry Shrimp"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "The chili rasbora — also called the mosquito rasbora — is one of the most visually striking nano fish in the freshwater hobby. Despite reaching barely ¾ of an inch, a school of 15–20 chili rasboras moving through a blackwater planted tank is a genuinely breathtaking sight: vivid red bodies flickering in synchronized movement through amber-tinted water and dense moss. They are peaceful, long-lived, and uniquely suited to the blackwater planted aquarium aesthetic.",
    "qf_extra": [("Min. school size", "8–10 (15+ recommended)")],
  },

  {
    "slug": "ember-tetra",
    "name": "Ember Tetra",
    "sci_name": "Hyphessobrycon amandae",
    "sci_author": "Géry & Cardinal, 1994",
    "tag": "🔥 Freshwater · Nano Schooling Fish",
    "origin": "Araguaia River Basin, Brazil",
    "size": "0.6–0.8 in (1.5–2 cm)",
    "lifespan": "2–4 years",
    "care_level": "Beginner",
    "care_badge": "bgood",
    "family": "Characidae",
    "order": "Characiformes",
    "genus": "Hyphessobrycon",
    "species_abbr": "H. amandae",
    "water_type": "Freshwater, tropical",
    "temp_f": "73–84°F",
    "temp_c": "23–29°C",
    "ph": "5.5–7.0",
    "gh": "1–8 dGH",
    "min_tank": "10 gallons (school of 8+)",
    "diet_type": "Omnivore (micro-predator)",
    "temperament": "Peaceful, schooling",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Hyphessobrycon_amandae.jpg/640px-Hyphessobrycon_amandae.jpg",
    "img_alt": "School of ember tetras showing vivid orange-red coloration in a planted aquarium",
    "img_caption": "Ember tetras in a planted aquarium — the intense orange-red coloration is most vivid against dark substrate and plant backgrounds. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Ember Tetra Care Guide 2026: Tank Setup, Diet & School Size | FishCare AI",
    "meta_desc": "Complete ember tetra care guide: tank setup, school size, diet, compatible tank mates, and water parameters for Hyphessobrycon amandae.",
    "og_title": "Ember Tetra Care Guide 2026: Tank Setup, Diet & School Size",
    "breadcrumb_label": "Ember Tetra",
    "taxonomy_intro": "The ember tetra belongs to the Characidae family — the same family as neon tetras, cardinal tetras, and piranhas. Described relatively recently in 1994, it is named for Amanda Géry, daughter of the ichthyologist Jacques Géry who co-described the species. Its vivid orange-red coloration and tiny size have made it one of the most popular nano tetras in the planted tank hobby.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Characiformes"), ("Family","Characidae"),
      ("Genus","<em>Hyphessobrycon</em>"), ("Species","<em>H. amandae</em>"),
    ],
    "habitat_text": "Ember tetras are native to the Araguaia River and its tributaries in the Brazilian Cerrado region. They inhabit slow-moving, heavily vegetated backwaters and stream margins characterized by warm, acidic water with abundant plant cover.",
    "habitat_bullets": [
      "<strong>Densely planted margins:</strong> fish shelter in aquatic grasses and vegetation at the river's edge",
      "<strong>Warm, acidic water:</strong> pH 5.5–7.0 with moderate soft water",
      "<strong>Slow flow:</strong> backwaters and oxbow lakes with minimal current",
      "<strong>Leaf litter floor:</strong> decomposing leaves and woody debris provide invertebrate food sources",
    ],
    "water_rows": [
      ("Temperature","73–84°F (23–29°C)","73–84°F (23–29°C)"),
      ("pH","5.5–7.0","5.5–7.0"),
      ("Hardness (GH)","1–8 dGH","1–8 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Ember tetras are highly adaptable and tolerate a wide temperature and pH range. "
                   "They are among the hardiest nano tetras available. Coloration is most vivid in slightly acidic, soft water (pH 6.0–6.8) with plants."),
    "tank_setup_text": "A 10-gallon tank suits a school of 8–10 ember tetras comfortably. Ideal setup for vivid coloration:",
    "tank_bullets": [
      "<strong>Dark substrate:</strong> black sand or fine dark gravel — contrasts beautifully with orange coloration",
      "<strong>Dense background planting:</strong> stem plants (rotala, ludwigia), moss walls — ember tetras look best against green",
      "<strong>Floating plants or subdued lighting:</strong> reduces stress and intensifies color",
      "<strong>Gentle filtration:</strong> sponge filter or spray bar; strong current is tolerated but not preferred",
      "<strong>Driftwood and leaf litter:</strong> tannins from Indian almond leaves enhance color and create a natural aesthetic",
    ],
    "extra_section_id": "schooling",
    "extra_section_title": "Schooling Behavior",
    "extra_section_content": """<p>Ember tetras are active, social schooling fish that are most confident and colorful in groups of 8 or more. Unlike some tetras that form tight defensive schools only when threatened, ember tetras swim in loose, constantly moving groups throughout the tank — exploring plants, drifting through open water, and weaving among stems.</p>
<p>Males are slightly more intensely colored than females and may display to each other with fin-spreading, but aggression is minimal. In a well-planted tank with adequate school size, they show no real behavioral issues.</p>
<div class="callout"><strong>School size:</strong> A minimum of 8 ember tetras is recommended; 12–20 produces much bolder behavior and more impressive visual displays. In a school, they explore the entire tank; in small groups, they tend to hide.</div>""",
    "diet_text": "Ember tetras are micro-predators and omnivores in the wild, eating tiny invertebrates, zooplankton, and plant matter. In captivity:",
    "diet_bullets": [
      "<strong>Staple:</strong> high-quality micro-pellets or finely crushed flake (ensure food is small enough for their tiny mouths)",
      "<strong>Frozen food:</strong> baby brine shrimp, micro worms, daphnia, cyclops",
      "<strong>Live food:</strong> vinegar eels, Walter worms, baby brine shrimp — ideal for bringing fish into breeding condition",
    ],
    "diet_note": "<strong>Tip:</strong> Ember tetras are small even by nano standards — standard-size flake must be crushed to dust for them to eat it easily. Micro-pellets sized for nano fish work better.",
    "tank_mates_text": "Ember tetras are peaceful with virtually all comparably sized, non-aggressive fish. Excellent companions:",
    "tank_mates_good": [
      "Chili rasboras, harlequin rasboras, other nano rasboras",
      "Pygmy corydoras (excellent bottom-level tank mates)",
      "Neon tetras, cardinal tetras (mid-level companions)",
      "Honey gourami (peaceful, non-predatory)",
      "Cherry shrimp (adult shrimp generally safe; juveniles may occasionally be eaten)",
      "Otocinclus catfish",
    ],
    "tank_mates_avoid": "Large or predatory fish, aggressive species, or any fish large enough to eat them (ember tetras are very small).",
    "health_issues": [
      ("<strong>Ich</strong>","white spots; temperature increase plus medication; ember tetras are relatively hardy"),
      ("<strong>Velvet</strong>","fine golden dust; treat with copper medication"),
      ("<strong>Fin rot</strong>","secondary to poor water quality; maintain clean water"),
      ("<strong>Neon Tetra Disease</strong>","can affect other Characidae species including ember tetras; incurable; quarantine affected individuals"),
    ],
    "health_note": ("<strong>Note:</strong> Ember tetras are one of the hardier nano tetras and less susceptible to disease than neon tetras "
                    "when kept in appropriate water conditions."),
    "toc_sections": [
      ("#taxonomy","Taxonomy"), ("#habitat","Natural Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#schooling","Schooling Behavior"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/chili-rasbora/","🔴 Chili Rasbora"),
      ("/wiki/neon-tetra/","💙 Neon Tetra"),
      ("/wiki/pygmy-corydoras/","🐾 Pygmy Corydoras"),
      ("/wiki/honey-gourami/","🍯 Honey Gourami"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "The ember tetra is arguably the best nano fish for planted tank beginners. Hardy, vividly colored in intense orange-red, and peaceful with virtually everything, a school of 15–20 ember tetras drifting through a densely planted aquarium creates a living, flickering warmth that earns the fish its name. Unlike some nano species that require soft, acidic blackwater, ember tetras adapt readily to a wide range of conditions — making them forgiving for aquarists still dialing in their water parameters.",
    "qf_extra": [("Min. school size", "8 (12+ recommended)")],
  },

  {
    "slug": "pygmy-corydoras",
    "name": "Pygmy Corydoras",
    "sci_name": "Corydoras pygmaeus",
    "sci_author": "Knaack, 1966",
    "tag": "🪨 Freshwater · Nano Bottom Dweller",
    "origin": "Rio Madeira tributaries, Brazil",
    "size": "0.8–1 in (2–2.5 cm)",
    "lifespan": "3–5 years",
    "care_level": "Beginner",
    "care_badge": "bgood",
    "family": "Callichthyidae",
    "order": "Siluriformes",
    "genus": "Corydoras",
    "species_abbr": "C. pygmaeus",
    "water_type": "Freshwater, tropical",
    "temp_f": "72–79°F",
    "temp_c": "22–26°C",
    "ph": "6.0–7.5",
    "gh": "2–12 dGH",
    "min_tank": "10 gallons (group of 6+)",
    "diet_type": "Omnivore / Scavenger",
    "temperament": "Peaceful, schooling",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Corydoras_pygmaeus1.jpg/640px-Corydoras_pygmaeus1.jpg",
    "img_alt": "Pygmy corydoras resting on aquarium substrate showing silver body with black lateral stripe",
    "img_caption": "Pygmy corydoras on fine sand substrate — note the characteristic black horizontal stripe and silvery body. Unlike most corydoras, pygmaeus also schools in open water mid-tank. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Pygmy Corydoras Care Guide 2026: Tank Setup, Diet & School Size | FishCare AI",
    "meta_desc": "Complete pygmy corydoras care guide: tank setup, diet, school size, compatible tank mates, and water parameters for Corydoras pygmaeus.",
    "og_title": "Pygmy Corydoras Care Guide 2026: Tank Setup & School Size",
    "breadcrumb_label": "Pygmy Corydoras",
    "taxonomy_intro": "Pygmy corydoras belong to the family Callichthyidae — the armored catfishes — alongside the more familiar bronze corydoras and peppered corydoras. They are among the smallest members of a very large genus (<em>Corydoras</em> contains over 170 described species). Unlike most corydoras, <em>C. pygmaeus</em> is notably mid-water active in addition to its bottom-dwelling behavior.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Siluriformes"), ("Family","Callichthyidae"),
      ("Genus","<em>Corydoras</em>"), ("Species","<em>C. pygmaeus</em>"),
    ],
    "habitat_text": "Pygmy corydoras are native to tributaries of the Rio Madeira in Brazil, including the Rio Aguapeí. They inhabit slow-moving, warm streams with sandy or muddy substrates, dense vegetation, and abundant leaf litter.",
    "habitat_bullets": [
      "<strong>Soft substrate:</strong> fine sand allows natural foraging behavior (sifting sand through gills to find food)",
      "<strong>Warm tropical water:</strong> 72–79°F; seasonal temperature fluctuations are common in their native range",
      "<strong>Slightly acidic to neutral:</strong> pH 6.0–7.5 with soft to moderately hard water",
      "<strong>Dense vegetation and leaf litter:</strong> provides shelter and food",
    ],
    "water_rows": [
      ("Temperature","72–79°F (22–26°C)","72–79°F (22–26°C)"),
      ("pH","6.0–7.5","6.0–7.5"),
      ("Hardness (GH)","2–10 dGH","2–12 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Pygmy corydoras, like all corydoras, are sensitive to high nitrates and any trace of salt. "
                   "Never add aquarium salt to a corydoras tank — it damages the barbels and osmotic balance."),
    "tank_setup_text": "A 10-gallon tank is the minimum for a group of 6 pygmy corydoras. Key setup considerations:",
    "tank_bullets": [
      "<strong>Fine sand substrate:</strong> essential for natural foraging; coarse gravel or sharp substrate damages their delicate barbels",
      "<strong>Gentle filtration:</strong> sponge filter or low-flow setup; pygmy corydoras prefer slow water",
      "<strong>Bottom cover:</strong> driftwood, smooth pebbles, and broad-leaf plants at substrate level provide shelter",
      "<strong>Mid-level plants:</strong> Java fern, Anubias — pygmy corydoras also school mid-water and appreciate structure throughout the tank",
      "<strong>No salt:</strong> corydoras are highly salt-intolerant",
    ],
    "extra_section_id": "behavior",
    "extra_section_title": "Unique Behavior: Mid-Water Schooling",
    "extra_section_content": """<p>Unlike most corydoras species that spend the majority of their time at the substrate, pygmy corydoras are also active mid-water schoolers. In a group of 10 or more, they will school together in the middle of the tank — swimming in close formation, darting between plants, and hovering near the surface to gulp atmospheric air (like all callichthyids, they have a limited ability to breathe air).</p>
<p>This behavior makes pygmy corydoras uniquely versatile: they perform the cleanup role of a traditional bottom-dwelling corydoras while also providing visual interest throughout the entire water column.</p>
<div class="callout"><strong>School size:</strong> Pygmy corydoras are significantly bolder and more active in larger groups. Keep a minimum of 6; 10–15 is better. In small groups of 3 or fewer they become shy and hide constantly.</div>""",
    "diet_text": "Pygmy corydoras are opportunistic omnivores and scavengers, eating whatever falls to the substrate. In captivity:",
    "diet_bullets": [
      "<strong>Sinking wafers and pellets:</strong> sinking catfish wafers or micro-pellets that reach the bottom before other fish consume them",
      "<strong>Frozen food:</strong> blood worms, daphnia, cyclops — excellent condition food; they will pick frozen food off the substrate",
      "<strong>Live food:</strong> micro worms, baby brine shrimp, grindal worms",
      "<strong>Leftover flake:</strong> they will clean up uneaten flake that sinks to the substrate",
    ],
    "diet_note": "<strong>Tip:</strong> Feed sinking food specifically for the corydoras — they are easily outcompeted at the surface by mid-water species. A feeding ring near the substrate helps.",
    "tank_mates_text": "Pygmy corydoras are peaceful with all non-aggressive species. They are one of the most versatile nano tank mates available:",
    "tank_mates_good": [
      "Nano tetras (ember tetra, chili rasbora, neon tetra, cardinal tetra)",
      "Honey gourami, dwarf gourami",
      "Chili rasboras and other micro-rasboras",
      "Cherry shrimp, neocaridina shrimp",
      "Otocinclus catfish",
      "Betta fish (in well-planted tanks with hiding spots)",
    ],
    "tank_mates_avoid": "Large catfish (competition and predation), cichlids, aggressive bottom dwellers, and any fish that nips at their barbels.",
    "health_issues": [
      ("<strong>Barbel erosion</strong>","caused by sharp substrate or accumulated waste at the substrate level; prevent with fine sand and regular gravel vacuuming"),
      ("<strong>Ich</strong>","white spots; treat at standard dose; corydoras are relatively tolerant of ich medication"),
      ("<strong>Red blotch disease</strong>","bacterial infection causing red spots on body; linked to poor water quality; improve conditions and treat with antibacterial medication"),
      ("<strong>Catfish wasting syndrome</strong>","internal parasites; common in newly imported fish; treat with praziquantel"),
    ],
    "health_note": ("<strong>Note:</strong> Barbel health is the most important indicator of pygmy corydoras wellbeing. "
                    "Short, eroded, or red-tipped barbels signal substrate problems or bacterial infection — act quickly."),
    "toc_sections": [
      ("#taxonomy","Taxonomy"), ("#habitat","Natural Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#behavior","Mid-Water Schooling"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/corydoras/","🐟 Corydoras Catfish"),
      ("/wiki/chili-rasbora/","🔴 Chili Rasbora"),
      ("/wiki/ember-tetra/","🔥 Ember Tetra"),
      ("/wiki/cherry-shrimp/","🦐 Cherry Shrimp"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "The pygmy corydoras is the smallest member of one of the most beloved catfish genera in the aquarium hobby. At under an inch long, it brings everything that makes corydoras popular — the busy, industrious foraging, the social schooling behavior, the gentle cleanup-crew role — into a package compatible with nano tanks and the most delicate of tank mates. Uniquely among corydoras, pygmaeus also schools actively in open water mid-tank, making it visually interesting at every level of the aquarium.",
    "qf_extra": [("Min. school size", "6 (10+ recommended)")],
  },

  {
    "slug": "black-moor-goldfish",
    "name": "Black Moor Goldfish",
    "sci_name": "Carassius auratus (Black Moor variety)",
    "sci_author": "Linnaeus, 1758 (captive variety)",
    "tag": "🐟 Freshwater · Fancy Goldfish",
    "origin": "China (selective breeding; wild ancestor from East Asia)",
    "size": "6–8 in (15–20 cm)",
    "lifespan": "10–15+ years",
    "care_level": "Intermediate",
    "care_badge": "bwarn",
    "family": "Cyprinidae",
    "order": "Cypriniformes",
    "genus": "Carassius",
    "species_abbr": "C. auratus",
    "water_type": "Freshwater, cold to temperate",
    "temp_f": "65–72°F",
    "temp_c": "18–22°C",
    "ph": "6.5–7.5",
    "gh": "5–15 dGH",
    "min_tank": "20 gallons for 1 fish; +10 gal per additional",
    "diet_type": "Omnivore",
    "temperament": "Peaceful",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Black_Moor_goldfish.jpg/640px-Black_Moor_goldfish.jpg",
    "img_alt": "Black Moor goldfish showing characteristic velvety black coloration and telescope eyes",
    "img_caption": "A Black Moor goldfish showing the characteristic velvety jet-black coloration and protruding telescope eyes that define the variety. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Black Moor Goldfish Care Guide 2026: Tank Size, Diet & Eyes | FishCare AI",
    "meta_desc": "Complete Black Moor goldfish care guide: tank size, diet, telescope eye care, compatible tank mates, and water parameters for Carassius auratus.",
    "og_title": "Black Moor Goldfish Care Guide 2026: Tank Size & Eye Care",
    "breadcrumb_label": "Black Moor Goldfish",
    "taxonomy_intro": "The Black Moor is not a separate species but a selectively bred variety of the common goldfish, <em>Carassius auratus</em> — the same species as every other goldfish variety from comets to orandas. It is distinguished by two features: a velvety, jet-black coloration (caused by melanophore cells) and protruding, telescope-style eyes (a genetic mutation affecting eye socket development). The variety originated in China and has been maintained through centuries of selective breeding.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Cypriniformes"), ("Family","Cyprinidae"),
      ("Genus","<em>Carassius</em>"), ("Species","<em>C. auratus</em>"),
    ],
    "habitat_text": "As a fully domesticated captive variety, Black Moors have no wild habitat. Their ancestor, the wild carp <em>Carassius auratus</em>, is native to slow-moving, often murky freshwater across East Asia — rivers, lakes, and ponds. Black Moors retain the cold-water preference of their ancestor and are NOT tropical fish.",
    "habitat_bullets": [
      "<strong>Cold to temperate water:</strong> prefer 65–72°F (18–22°C); do not require a heater in most indoor environments",
      "<strong>Slow-moving water:</strong> fancy goldfish varieties are poor swimmers compared to single-tailed goldfish; strong currents stress them",
      "<strong>High oxygen requirement:</strong> goldfish have high metabolisms and need well-oxygenated water",
      "<strong>No tropical environment:</strong> temperatures above 75°F stress fancy goldfish long-term",
    ],
    "water_rows": [
      ("Temperature","65–72°F (18–22°C)","65–72°F (18–22°C)"),
      ("pH","6.5–7.5","6.5–7.5"),
      ("Hardness (GH)","5–15 dGH","5–15 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Goldfish are heavy waste producers — they generate significantly more ammonia than a comparably sized tropical fish. "
                   "Robust filtration (rated for at least double the tank volume) and frequent water changes (30–50% weekly) are essential."),
    "tank_setup_text": "A 20-gallon tank is the minimum for a single Black Moor, with 10 additional gallons per additional fish. Fancy goldfish produce heavy waste and require substantial filtration:",
    "tank_bullets": [
      "<strong>Oversized filtration:</strong> a filter rated for at least twice the tank volume; goldfish produce 2–3× the waste of most tropical fish",
      "<strong>Smooth decor:</strong> avoid sharp decorations — the telescope eyes of Black Moors are fragile and easily scratched; any wound on the eye becomes infected quickly",
      "<strong>Wide open swimming space:</strong> fancy goldfish are clumsy swimmers; they need unobstructed space to maneuver",
      "<strong>No heater needed:</strong> Black Moors prefer cooler water than room temperature in most climates",
      "<strong>High oxygen:</strong> air stone or surface agitation; goldfish need highly oxygenated water",
    ],
    "extra_section_id": "eyes",
    "extra_section_title": "Telescope Eye Care",
    "extra_section_content": """<p>The Black Moor's most distinctive feature — the protruding telescope eyes — is also its most vulnerable. The eyes protrude far from the socket, making them susceptible to:</p>
<ul>
<li><strong>Physical injury:</strong> catching on sharp decorations, rocks, or filter intakes</li>
<li><strong>Infection:</strong> any wound on the eye quickly develops into Pop-Eye (exophthalmia) or bacterial infection</li>
<li><strong>Cloudy eyes:</strong> bacterial or water-quality related opacity of the cornea</li>
</ul>
<div class="callout callout-warn"><strong>Eye safety:</strong> Audit your tank for anything sharp — smooth rocks only, sand or fine gravel substrate, no sharp plastic plants. Cover filter intakes with foam sponge to prevent the fish's eye from being sucked against the intake.</div>
<p>Black Moors also have significantly reduced vision compared to normal-eyed goldfish, which affects their ability to compete for food at feeding time.</p>""",
    "diet_text": "Black Moors are omnivores and enthusiastic eaters. As with all goldfish, overfeeding is a common problem:",
    "diet_bullets": [
      "<strong>Sinking pellets preferred:</strong> goldfish that gulp air at the surface while eating floating food often develop swim bladder problems; sinking pellets reduce this risk",
      "<strong>High-quality goldfish formula:</strong> wheat germ-based pellets in cool water (under 65°F); higher-protein formulas at warmer temperatures",
      "<strong>Vegetables:</strong> blanched peas (shelled), zucchini, spinach — excellent fiber source and helps prevent constipation",
      "<strong>Frozen food:</strong> blood worms, brine shrimp — in moderation as treats",
    ],
    "diet_note": "<strong>Tip:</strong> Feed only what the fish can consume in 3 minutes, twice daily. Fast for one day per week to prevent constipation — a common problem in fancy goldfish.",
    "tank_mates_text": "Black Moors should only be kept with other fancy goldfish varieties of similar swimming ability:",
    "tank_mates_good": [
      "Other fancy goldfish (ryukin, oranda, ranchu, telescope eye varieties)",
      "Bubble-eye and celestial goldfish (similarly impaired swimmers)",
      "Dojo loach / weather loach (tolerates cold water; peaceful scavenger)",
    ],
    "tank_mates_avoid": "Single-tailed goldfish (comet, shubunkin, common) — they outcompete Black Moors for food and may nip fins. Tropical fish — temperature incompatibility. Any fast or nippy species.",
    "health_issues": [
      ("<strong>Swim bladder disease</strong>","floating or sinking abnormally; caused by overfeeding, constipation, or bacterial infection; fast for 2–3 days and feed blanched peas"),
      ("<strong>Pop-Eye (Exophthalmia)</strong>","eye(s) swelling outward further than normal; bacterial infection; treat with antibacterial medication"),
      ("<strong>Eye injury / cloudy eye</strong>","physical trauma or bacterial infection; remove sharp objects; treat with antibacterial medication and salt bath"),
      ("<strong>Ich</strong>","white spots; treat with temperature increase and medication; goldfish tolerate most ich treatments"),
      ("<strong>Fin rot</strong>","usually secondary to water quality; increase water change frequency and treat with antibacterial medication"),
    ],
    "health_note": ("<strong>Note:</strong> Black Moors' black coloration may shift to orange-gold as they age, particularly in warmer water or under intense light — "
                    "this is a normal, non-pathological color change and does not indicate illness."),
    "toc_sections": [
      ("#taxonomy","Taxonomy & Variety"),
      ("#habitat","Temperature & Water"),
      ("#water","Water Requirements"), ("#tank","Tank Setup"),
      ("#eyes","Telescope Eye Care"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/goldfish/","🐟 Goldfish Care"),
      ("/wiki/comet-goldfish/","☄️ Comet Goldfish"),
      ("/calculators/goldfish-tank-size/","📐 Goldfish Tank Size Calculator"),
      ("/guides/freshwater-fish-care/","🌿 Freshwater Fish Care"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/tools/water-parameter-checker/","🔬 Water Parameter Checker"),
    ],
    "date": "2026-08-15",
    "intro": "The Black Moor goldfish is one of the most striking fancy goldfish varieties — a slow-swimming, velvet-black fish with dramatic protruding telescope eyes that give it an endearingly wide-eyed expression. Despite their delicate appearance, Black Moors are among the more robust fancy goldfish varieties when kept in properly sized, cold, well-filtered tanks. They are not tropical fish and must not be kept with most community aquarium species.",
    "qf_extra": [("Eye type", "Telescope (protruding)")],
  },

  {
    "slug": "comet-goldfish",
    "name": "Comet Goldfish",
    "sci_name": "Carassius auratus (Comet variety)",
    "sci_author": "Linnaeus, 1758 (captive variety)",
    "tag": "🐟 Freshwater · Pond & Tank Goldfish",
    "origin": "United States, 1880s (developed from Chinese goldfish stock)",
    "size": "10–14 in (25–35 cm) in ponds; 6–10 in (15–25 cm) in tanks",
    "lifespan": "14–20+ years",
    "care_level": "Beginner",
    "care_badge": "bgood",
    "family": "Cyprinidae",
    "order": "Cypriniformes",
    "genus": "Carassius",
    "species_abbr": "C. auratus",
    "water_type": "Freshwater, cold to temperate",
    "temp_f": "50–75°F",
    "temp_c": "10–24°C",
    "ph": "6.5–7.5",
    "gh": "5–15 dGH",
    "min_tank": "75 gallons per fish (tank); pond preferred",
    "diet_type": "Omnivore",
    "temperament": "Active, peaceful",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Carassius_auratus_Comet_goldfish.jpg/640px-Carassius_auratus_Comet_goldfish.jpg",
    "img_alt": "Orange-red comet goldfish showing characteristic long flowing forked tail fin",
    "img_caption": "A comet goldfish showing its characteristic long, deeply forked tail fin — the feature that gives the variety its name. Comets are built for ponds and are far too active for most aquariums. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "Comet Goldfish Care Guide 2026: Pond Setup, Tank Size & Lifespan | FishCare AI",
    "meta_desc": "Complete comet goldfish care guide: pond vs tank setup, minimum tank size, diet, lifespan of 20+ years, and compatible tank mates for Carassius auratus.",
    "og_title": "Comet Goldfish Care Guide 2026: Pond Setup & Tank Size",
    "breadcrumb_label": "Comet Goldfish",
    "taxonomy_intro": "The Comet goldfish is a single-tailed goldfish variety selectively bred in the United States in the 1880s, primarily by Hugo Mullertt of the U.S. Fish Commission. It is distinguished from the common goldfish by its longer, deeply forked tail fin — resembling a comet's tail in motion. Like all goldfish, it is a domesticated variety of <em>Carassius auratus</em>.",
    "taxonomy_rows": [
      ("Kingdom","Animalia"), ("Phylum","Chordata"), ("Class","Actinopterygii"),
      ("Order","Cypriniformes"), ("Family","Cyprinidae"),
      ("Genus","<em>Carassius</em>"), ("Species","<em>C. auratus</em>"),
    ],
    "habitat_text": "As a domesticated variety, comet goldfish have no wild habitat. However, their cold-water preferences and large size reflect their wild ancestor's ecology. Comet goldfish thrive best in outdoor ponds — the aquarium environment is genuinely inadequate for their long-term wellbeing in most cases.",
    "habitat_bullets": [
      "<strong>Cold water:</strong> comets tolerate temperatures from near-freezing to 75°F; they do NOT need a heater and should not be kept in tropical temperatures",
      "<strong>Large volume:</strong> comets are fast, powerful swimmers that grow large; they need space to express natural behavior",
      "<strong>High oxygen:</strong> like all goldfish, they have high oxygen demands",
      "<strong>Seasonal behavior:</strong> in ponds, comets naturally slow down in winter and become inactive when water falls below 50°F",
    ],
    "water_rows": [
      ("Temperature","50–75°F (10–24°C)","50–75°F (10–24°C)"),
      ("pH","6.5–7.5","6.5–7.5"),
      ("Hardness (GH)","5–15 dGH","5–15 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;30 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Comet goldfish are extraordinary waste producers — a single adult fish rivals a small dog in bioload per gallon. "
                   "Aquarium filtration rated for the full tank volume is insufficient; use a filter rated for 2–3× the volume."),
    "tank_setup_text": "A pond is strongly recommended for comet goldfish. If keeping in an aquarium, the tank must be far larger than most fishkeepers assume:",
    "tank_bullets": [
      "<strong>Pond (ideal):</strong> 200+ gallons per 2–3 fish; 18–24 inches deep minimum for winter in cold climates",
      "<strong>Aquarium (minimum):</strong> 75 gallons for a single comet; 100+ gallons for two",
      "<strong>Powerful filtration:</strong> canister filter or wet/dry filter rated for 3× tank volume; weekly 30–50% water changes",
      "<strong>No heater:</strong> comet goldfish do not need heating and should not be kept above 75°F long-term",
      "<strong>Smooth substrate:</strong> fine gravel or bare bottom; comets constantly dig and disturb the substrate",
    ],
    "extra_section_id": "lifespan",
    "extra_section_title": "Lifespan & Growth",
    "extra_section_content": """<p>Comet goldfish are remarkably long-lived when kept correctly. Well-kept pond comets regularly reach 15–20 years, and some documented individuals have survived past 25 years. In aquariums, typical lifespan is 10–14 years with proper care.</p>
<p>Growth is highly dependent on tank size and water quality. A comet kept in a small tank will be growth-stunted — but this stunting is physiological stress, not an adaptation. The fish's organs continue to grow even as external growth slows, leading to internal damage and shortened lifespan.</p>
<div class="callout callout-warn"><strong>Common mistake:</strong> Buying comet goldfish as "temporary" fish for a small starter tank, intending to upgrade later. Most do not get upgraded. The fish lives a shortened, stunted life. Plan for their full adult size from the start — or choose a smaller, tank-appropriate species.</div>""",
    "diet_text": "Comet goldfish are omnivores and voracious eaters. Their diet varies seasonally in ponds:",
    "diet_bullets": [
      "<strong>Pellets:</strong> high-quality goldfish pellets; wheat germ-based for temperatures below 60°F (easier to digest in cold water); higher-protein formulas above 65°F",
      "<strong>Vegetables:</strong> blanched peas (shelled, prevent constipation), zucchini, lettuce, spinach",
      "<strong>Live/frozen food:</strong> blood worms, brine shrimp, daphnia — in moderation as treats",
      "<strong>Insects:</strong> comets in ponds will eat insects, worms, and aquatic invertebrates — this is healthy natural behavior",
    ],
    "diet_note": "<strong>Tip:</strong> Stop feeding when water temperature drops below 50°F — goldfish metabolism slows dramatically in cold water and undigested food causes serious health problems.",
    "tank_mates_text": "Comet goldfish are best kept with other cold-water species of similar size:",
    "tank_mates_good": [
      "Other comet or single-tailed goldfish (shubunkin, common goldfish)",
      "Dojo/weather loach (cold-water, peaceful bottom dweller)",
      "Larger koi (in appropriately sized ponds, 500+ gallons)",
      "Rosy barbs (one of the few cold-water barb species)",
    ],
    "tank_mates_avoid": "Fancy goldfish (comets outcompete them for food and may injure them). Any tropical fish (temperature incompatibility). Small fish that comets can eat.",
    "health_issues": [
      ("<strong>Swim bladder disease</strong>","floating or sinking; often caused by overfeeding or constipation; fast for 2–3 days, feed blanched peas"),
      ("<strong>Ich</strong>","white spots; treat with temperature increase (to 75°F max for goldfish) and medication"),
      ("<strong>Ulcers / open sores</strong>","bacterial infection from poor water quality; increase water changes; treat with antibacterial medication"),
      ("<strong>Fin rot</strong>","bacterial; secondary to poor water quality; maintain filtration and treat if needed"),
      ("<strong>Anchor worm / fish lice</strong>","parasites; common in pond fish; treat with appropriate parasiticide"),
    ],
    "health_note": ("<strong>Note:</strong> Comet goldfish are among the hardiest of all goldfish varieties and resist disease well when water quality is maintained. "
                    "Most health problems trace back to overcrowding, poor filtration, or overfeeding."),
    "toc_sections": [
      ("#taxonomy","Taxonomy & Variety"),
      ("#habitat","Temperature & Habitat"),
      ("#water","Water Requirements"), ("#tank","Pond & Tank Setup"),
      ("#lifespan","Lifespan & Growth"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/goldfish/","🐟 Goldfish Care"),
      ("/wiki/black-moor-goldfish/","🖤 Black Moor Goldfish"),
      ("/calculators/goldfish-tank-size/","📐 Goldfish Tank Size Calculator"),
      ("/guides/freshwater-fish-care/","🌿 Freshwater Fish Care"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/tools/water-parameter-checker/","🔬 Water Parameter Checker"),
    ],
    "date": "2026-08-15",
    "intro": "The comet goldfish is the most commonly sold fish in the world — and also the most commonly mistreated. Sold as fairground prizes and kept in bowls and small tanks, most comets live a fraction of their potential 20-year lifespan. A properly kept comet goldfish in a pond or appropriately large aquarium is a spectacular fish: fast, active, often developing vivid orange-red coloration, and displaying an alert, curious intelligence that surprises many first-time keepers.",
    "qf_extra": [("Tail type", "Long, deeply forked (comet tail)")],
  },

  {
    "slug": "glofish",
    "name": "GloFish",
    "sci_name": "Various (see below)",
    "sci_author": "Genetically modified; patented variety",
    "tag": "🌟 Freshwater · Fluorescent Aquarium Fish",
    "origin": "USA (genetic modification of Asian and South American species)",
    "size": "Varies by base species (1–5 in / 2.5–13 cm)",
    "lifespan": "3–5 years",
    "care_level": "Beginner",
    "care_badge": "bgood",
    "family": "Multiple (Cyprinidae, Characidae, Poeciliidae, Cichlidae)",
    "order": "Multiple",
    "genus": "Multiple",
    "species_abbr": "Trademarked variety",
    "water_type": "Freshwater, tropical",
    "temp_f": "72–80°F",
    "temp_c": "22–27°C",
    "ph": "6.5–7.5",
    "gh": "5–15 dGH",
    "min_tank": "10–20 gallons (varies by species)",
    "diet_type": "Omnivore (same as base species)",
    "temperament": "Peaceful to semi-aggressive (same as base species)",
    "wiki_img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/GloFish_in_an_aquarium.jpg/640px-GloFish_in_an_aquarium.jpg",
    "img_alt": "GloFish tetras glowing in vivid electric colors under blacklight in an aquarium",
    "img_caption": "GloFish tetras under actinic (blue/UV) lighting — the fluorescent proteins produce intense colors visible even under standard aquarium lighting. Image: Wikimedia Commons / CC BY-SA",
    "meta_title": "GloFish Care Guide 2026: Species, Tank Setup & Compatibility | FishCare AI",
    "meta_desc": "Complete GloFish care guide: species types (zebrafish, tetra, barb, shark, betta), tank setup, diet, and compatible tank mates for fluorescent aquarium fish.",
    "og_title": "GloFish Care Guide 2026: Species Types, Tank Setup & Compatibility",
    "breadcrumb_label": "GloFish",
    "taxonomy_intro": "GloFish are not a single species — they are a registered trademark for a line of genetically modified aquarium fish produced by GloFish LLC (owned by Spectrum Brands). The fluorescent coloration is produced by a gene for fluorescent protein (originally derived from jellyfish and sea coral genes) inserted into the genome. Available GloFish species include zebrafish (<em>Danio rerio</em>), black skirt tetra (<em>Gymnocorymbus ternetzi</em>), tiger barb (<em>Puntigrus tetrazona</em>), rainbow shark (<em>Epalzeorhynchos frenatum</em>), and betta (<em>Betta splendens</em>).",
    "taxonomy_rows": [
      ("Brand","GloFish® (Spectrum Brands)"),
      ("GloFish Danio","<em>Danio rerio</em> — Starfire Red, Electric Green, Sunburst Orange, Cosmic Blue, Galactic Purple, Moonrise Pink"),
      ("GloFish Tetra","<em>Gymnocorymbus ternetzi</em> — same color options"),
      ("GloFish Barb","<em>Puntigrus tetrazona</em> — Tiger Barb base"),
      ("GloFish Shark","<em>Epalzeorhynchos frenatum</em> — Rainbow Shark base"),
      ("GloFish Betta","<em>Betta splendens</em> — various colors"),
    ],
    "habitat_text": "GloFish are genetically modified versions of species with wild distributions across Asia and South America. Their care requirements are identical to those of the base species — the genetic modification affects only coloration, not biology or behavior.",
    "habitat_bullets": [
      "<strong>GloFish Danio:</strong> same as zebra danio — tolerant of a wide temperature range (65–80°F), schooling, hardy",
      "<strong>GloFish Tetra:</strong> same as black skirt tetra — peaceful, schooling, 72–80°F",
      "<strong>GloFish Barb:</strong> same as tiger barb — schooling, semi-aggressive, fin-nipping in small groups",
      "<strong>GloFish Shark:</strong> same as rainbow shark — territorial with other bottom dwellers, grows to 5 inches",
      "<strong>GloFish Betta:</strong> same as standard betta — solitary males, 78–80°F, no fin-nipping tank mates",
    ],
    "water_rows": [
      ("Temperature","Varies: 65–80°F (Danio) to 78–80°F (Betta)","72–80°F (general guideline)"),
      ("pH","6.5–7.5","6.5–7.5"),
      ("Hardness (GH)","5–15 dGH","5–15 dGH"),
      ("Ammonia","0 ppm","0 ppm"),
      ("Nitrite","0 ppm","0 ppm"),
      ("Nitrate","Near zero","&lt;20 ppm"),
    ],
    "water_note": ("<strong>Note:</strong> Water parameters should match the base species. GloFish Danios are the hardiest and most temperature-tolerant; "
                   "GloFish Bettas require the warmest water (78–80°F) and must be kept alone (males)."),
    "tank_setup_text": "Tank setup depends entirely on which GloFish species you are keeping. General guidance:",
    "tank_bullets": [
      "<strong>GloFish Danio:</strong> 10-gallon minimum for a school of 6; active swimmers needing horizontal swimming space",
      "<strong>GloFish Tetra:</strong> 10-gallon minimum for a school of 6; standard community tank setup",
      "<strong>GloFish Barb:</strong> 20-gallon minimum for a school of 6+ (groups under 6 increase aggression significantly)",
      "<strong>GloFish Shark:</strong> 30-gallon minimum; becomes territorial at maturity; one per tank",
      "<strong>GloFish Betta:</strong> 5-gallon minimum per male; standard betta care applies",
    ],
    "extra_section_id": "lighting",
    "extra_section_title": "Lighting for GloFish",
    "extra_section_content": """<p>GloFish produce their fluorescent effect through fluorescent proteins in their cells — these glow intensely when excited by blue or UV light. Under standard white aquarium lighting, GloFish appear as vivid solid colors. Under GloFish-brand blue LED or actinic/blacklight, the colors intensify dramatically into glowing neon effects.</p>
<p>GloFish brand produces dedicated aquarium kits with blue LED lighting designed to maximize the fluorescent effect. Standard aquarium lighting works perfectly well, producing impressive colors without the blacklight effect.</p>
<div class="callout"><strong>Note:</strong> The fluorescent effect is produced by a stably inherited genetic modification — it does not fade over time, does not require special food, and is passed to offspring. Breeding GloFish and selling the offspring is prohibited under the GloFish trademark.</div>""",
    "diet_text": "GloFish diet is identical to that of the base species:",
    "diet_bullets": [
      "<strong>GloFish Danio / Tetra / Barb:</strong> high-quality tropical flake or small pellets; frozen daphnia, brine shrimp, blood worms as treats",
      "<strong>GloFish Shark:</strong> sinking pellets, algae wafers, frozen blood worms",
      "<strong>GloFish Betta:</strong> betta-specific pellets; frozen blood worms, brine shrimp",
    ],
    "diet_note": "<strong>Tip:</strong> GloFish brand produces GloFish-specific color-enhancing food — it is not required for the fish to maintain fluorescence, but can support overall health.",
    "tank_mates_text": "Tank mate compatibility depends entirely on the base species:",
    "tank_mates_good": [
      "GloFish Danio: peaceful community fish, other danios, rasboras, small tetras, corydoras",
      "GloFish Tetra: other peaceful community fish; treat as black skirt tetra",
      "GloFish Barb: must be kept in groups of 6+; compatible with fast-moving species without long fins",
      "GloFish Shark: one per tank; compatible with mid/upper-level fish that do not compete for bottom territory",
      "GloFish Betta: solo male; only very peaceful, short-finned tank mates (snails, nerite, corydoras)",
    ],
    "tank_mates_avoid": "For GloFish Barbs: slow, long-finned species (bettas, angelfish, guppies). For GloFish Betta: other bettas, nippy species. For GloFish Shark: other rainbow sharks or territorial bottom dwellers.",
    "health_issues": [
      ("<strong>Ich</strong>","white spots; identical treatment to base species"),
      ("<strong>Fin rot</strong>","secondary to water quality; maintain filtration"),
      ("<strong>GloFish Barb aggression</strong>","fin-nipping at incompatible tank mates; increase school size to 6+ or remove incompatible fish"),
      ("<strong>Velvet</strong>","fine gold dust; treat with copper medication"),
    ],
    "health_note": ("<strong>Note:</strong> GloFish have the same disease susceptibility and treatment requirements as their base species. "
                    "The genetic modification does not affect immune function or disease resistance."),
    "toc_sections": [
      ("#taxonomy","Species & Types"),
      ("#habitat","Base Species Habitat"),
      ("#water","Water Requirements"), ("#tank","Tank Setup by Species"),
      ("#lighting","Lighting for GloFish"),
      ("#diet","Diet & Feeding"), ("#tank-mates","Tank Mates"), ("#health","Health Issues"),
    ],
    "related_links": [
      ("/wiki/zebra-danio/","🐟 Zebra Danio"),
      ("/wiki/tiger-barb/","🐯 Tiger Barb"),
      ("/wiki/betta-fish/","🐠 Betta Fish"),
      ("/guides/freshwater-fish-care/","🌿 Freshwater Fish Care"),
      ("/wiki/","📚 Full Fish Encyclopedia"),
      ("/guides/best-freshwater-fish-for-beginners/","⭐ Best Beginner Fish 2026"),
    ],
    "date": "2026-08-15",
    "intro": "GloFish are the world's first commercially available genetically modified pets — fluorescent aquarium fish produced by inserting genes for fluorescent proteins (originally from jellyfish and sea coral) into common aquarium species. Their vivid, glowing colors are permanently part of their genetic code, inherited by offspring, and intensified dramatically by blue or UV lighting. For all practical care purposes, GloFish are kept exactly like the base species they were derived from.",
    "qf_extra": [("Fluorescent colors", "Starfire Red, Electric Green, Sunburst Orange, Cosmic Blue, Galactic Purple, Moonrise Pink")],
  },
]

CSS = """
:root{--p:#1B5E8B;--pl:#2E84C0;--pd:#0F3D5E;--s:#2E9E7D;--a:#F5A623;--ad:#D4891A;--bg:#F0F7FF;--tx:#1A2B3C;--mu:#5A7A94;--bd:#D0E4F0;--ok:#27AE60;--wn:#F39C12;--er:#E74C3C}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--p);text-decoration:none}
.con{max-width:1180px;margin:0 auto;padding:0 22px}
h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;line-height:1.2}
h2{font-size:1.3rem;font-weight:700;line-height:1.25}
h3{font-size:1.08rem;font-weight:700}
p{margin-bottom:.85rem;color:var(--mu)}
p:last-child{margin-bottom:0}
.nb{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid var(--bd);padding:0 22px;height:64px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:8px;font-size:1.2rem;font-weight:800;color:var(--p);text-decoration:none}
.nlinks{display:flex;align-items:center;gap:2px}
.nl{padding:7px 13px;border-radius:8px;font-weight:500;font-size:.86rem;color:var(--mu);text-decoration:none;transition:all .15s}
.nl:hover,.nl.act{color:var(--p);background:rgba(27,94,139,.07)}
.sp-hero{background:linear-gradient(135deg,#0B3250 0%,#1B5E8B 65%,#2E84C0 100%);padding:0;position:relative;overflow:hidden;min-height:340px;display:flex;align-items:flex-end}
.sp-hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}
.sp-hero-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,28,42,.88) 0%,rgba(11,50,80,.6) 55%,rgba(11,50,80,.15) 100%),linear-gradient(0deg,rgba(5,28,42,.75) 0%,transparent 45%)}
.sp-hero-inner{position:relative;z-index:1;padding:60px 22px 40px;max-width:1180px;margin:0 auto;width:100%}
.breadcrumb{display:flex;align-items:center;gap:6px;font-size:.78rem;color:rgba(255,255,255,.6);margin-bottom:12px;flex-wrap:wrap}
.breadcrumb a{color:rgba(255,255,255,.6);transition:color .15s}.breadcrumb a:hover{color:#fff}
.breadcrumb span{color:rgba(255,255,255,.35)}
.sp-tag{display:inline-block;padding:3px 11px;border-radius:20px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px;background:rgba(255,255,255,.18);color:rgba(255,255,255,.92)}
.sp-hero h1{color:#fff;margin-bottom:8px}
.sp-hero .sci-name{font-style:italic;color:rgba(255,255,255,.65);font-size:1.05rem;margin-bottom:14px}
.sp-meta-row{display:flex;gap:18px;flex-wrap:wrap}
.sp-meta-item{color:rgba(255,255,255,.78);font-size:.84rem;display:flex;align-items:center;gap:5px}
.sp-meta-item strong{color:#fff}
.sp-layout{display:grid;grid-template-columns:1fr 280px;gap:32px;padding:36px 0 60px;max-width:1180px;margin:0 auto}
@media(max-width:900px){.sp-layout{grid-template-columns:1fr}.sp-sidebar{display:none}}
.qf-card{background:#fff;border-radius:14px;border:1px solid var(--bd);overflow:hidden;box-shadow:0 2px 8px rgba(27,94,139,.07);margin-bottom:20px}
.qf-head{background:var(--pd);color:#fff;padding:12px 16px;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.qf-table{width:100%;border-collapse:collapse}
.qf-table tr:not(:last-child) td{border-bottom:1px solid var(--bd)}
.qf-table td{padding:9px 14px;font-size:.84rem;vertical-align:top}
.qf-table td:first-child{font-weight:600;color:var(--tx);width:42%;white-space:nowrap}
.qf-table td:last-child{color:var(--mu)}
.toc-card{background:#F8FAFE;border-radius:14px;border:1px solid var(--bd);padding:16px;position:sticky;top:80px}
.toc-card h4{color:var(--pd);margin-bottom:10px;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}
.toc-card a{display:block;padding:4px 0 4px 10px;font-size:.8rem;color:var(--mu);border-left:2px solid transparent;transition:all .15s}
.toc-card a:hover{color:var(--p);border-left-color:var(--p)}
.artc h2{color:var(--pd);margin:30px 0 12px;padding-top:10px;border-top:1px solid var(--bd);font-size:1.25rem}
.artc h3{color:var(--tx);margin:18px 0 8px}
.artc p{font-size:.97rem;line-height:1.82;color:var(--mu);margin-bottom:14px}
.artc ul,.artc ol{margin:10px 0 14px 22px}
.artc li{font-size:.97rem;line-height:1.72;color:var(--mu);margin-bottom:5px}
.callout{background:#F8FAFE;border:1px solid var(--bd);border-left:4px solid var(--p);border-radius:8px;padding:15px 18px;margin:20px 0;font-size:.9rem;color:var(--mu)}
.callout strong{color:var(--tx)}
.callout-warn{border-left-color:var(--wn);background:rgba(243,156,18,.04)}
.callout-ok{border-left-color:var(--ok);background:rgba(39,174,96,.04)}
.ptbl{width:100%;border-collapse:collapse;border-radius:12px;overflow:hidden;border:1px solid var(--bd);margin:14px 0 20px;font-size:.86rem}
.ptbl th{background:var(--p);color:#fff;padding:10px 13px;text-align:left;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}
.ptbl td{padding:10px 13px;border-bottom:1px solid var(--bd);color:var(--mu)}
.ptbl tr:last-child td{border-bottom:none}
.ptbl td:first-child{font-weight:600;color:var(--tx)}
.bdg{display:inline-block;padding:3px 9px;border-radius:20px;font-size:.74rem;font-weight:700}
.bgood{background:rgba(39,174,96,.12);color:var(--ok)}
.bwarn{background:rgba(243,156,18,.12);color:var(--wn)}
.bdng{background:rgba(231,76,60,.12);color:var(--er)}
figure{margin:22px 0;border-radius:12px;overflow:hidden;line-height:0}
figure img{width:100%;height:220px;object-fit:cover;display:block}
figcaption{padding:9px 14px;background:#F8FAFE;font-size:.78rem;color:var(--mu);line-height:1.4}
.abox{background:#F8FAFE;border-radius:14px;padding:16px 20px;border:1px solid var(--bd);display:flex;gap:13px;align-items:flex-start;margin-top:32px}
.aav{font-size:1.4rem;flex-shrink:0}
.abox p{font-size:.85rem;margin:4px 0 0}
.guide-links{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:16px}
.guide-links a{display:block;background:#fff;border:1px solid var(--bd);border-radius:8px;padding:13px;color:var(--tx);font-weight:700;font-size:.85rem;transition:border-color .15s,background .15s}
.guide-links a:hover{border-color:var(--p);background:#F8FAFE}
@media(max-width:600px){.guide-links{grid-template-columns:1fr}}
.ft{background:#0F3D5E;padding:32px 22px 20px}
.ftb{text-align:center;color:rgba(255,255,255,.4);font-size:.76rem}
"""


def build_page(sp: dict) -> str:
    # Quick facts rows
    qf_rows = [
        ("Scientific name", f"<em>{sp['sci_name']}</em>"),
        ("Family", sp["family"]),
        ("Origin", sp["origin"]),
        ("Adult size", sp["size"]),
        ("Lifespan", sp["lifespan"]),
        ("Water type", sp["water_type"]),
        ("Temperature", f"{sp['temp_f']} ({sp['temp_c']})"),
        ("pH range", sp["ph"]),
        ("Min. tank size", sp["min_tank"]),
        ("Diet", sp["diet_type"]),
        ("Temperament", sp["temperament"]),
        ("Care level", f'<span class="bdg {sp["care_badge"]}">{sp["care_level"]}</span>'),
    ] + sp.get("qf_extra", [])

    qf_html = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in qf_rows)

    # TOC
    toc_html = "".join(f'<a href="{href}">{label}</a>' for href, label in sp["toc_sections"])

    # Taxonomy table
    tax_rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in sp["taxonomy_rows"])

    # Water requirements table
    if sp["water_rows"] and len(sp["water_rows"][0]) == 3:
        water_html = (
            '<table class="ptbl"><tr><th>Parameter</th><th>Wild Preference</th><th>Aquarium Range</th></tr>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in sp["water_rows"])
            + "</table>"
        )
    else:
        water_html = (
            '<table class="ptbl"><tr><th>Parameter</th><th>Value</th></tr>'
            + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in sp["water_rows"])
            + "</table>"
        )

    # Tank bullets
    tank_bullets_html = "".join(f"<li>{b}</li>" for b in sp["tank_bullets"])

    # Habitat bullets
    habitat_bullets_html = "".join(f"<li>{b}</li>" for b in sp["habitat_bullets"])

    # Diet bullets
    diet_bullets_html = "".join(f"<li>{b}</li>" for b in sp["diet_bullets"])

    # Tank mates good
    tank_good_html = "".join(f"<li>{b}</li>" for b in sp["tank_mates_good"])

    # Health issues
    health_html = "".join(
        f"<li>{title} — {desc}</li>" for title, desc in sp["health_issues"]
    )

    # Related links
    links_html = "".join(
        f'<a href="{href}" title="{lbl.lstrip("🐟🦐🌿📚⭐💙🔥🔴🐡🍯🐾🖤☄️📐🔬🐯🐠").strip()}">{lbl}</a>'
        for href, lbl in sp["related_links"]
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="UTF-8"/>
<link rel="icon" href="/favicon.svg" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{sp['meta_title']}</title>
<meta name="description" content="{sp['meta_desc']}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="https://www.fishcareai.com/wiki/{sp['slug']}/"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{sp['og_title']}"/>
<meta property="og:description" content="{sp['meta_desc']}"/>
<meta property="og:url" content="https://www.fishcareai.com/wiki/{sp['slug']}/"/>
<meta property="og:image" content="/assets/fish-images/betta-fish-care.svg"/>
<meta name="twitter:card" content="summary_large_image"/>
<script type="application/ld+json">{{
  "@context":"https://schema.org",
  "@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"}},
    {{"@type":"ListItem","position":2,"name":"Fish Encyclopedia","item":"https://www.fishcareai.com/wiki/"}},
    {{"@type":"ListItem","position":3,"name":"{sp['name']}","item":"https://www.fishcareai.com/wiki/{sp['slug']}/"}}
  ]
}}</script>
<script type="application/ld+json">{{
  "@context":"https://schema.org",
  "@type":"Article",
  "headline":"{sp['og_title']}",
  "description":"{sp['meta_desc']}",
  "image":"/assets/fish-images/betta-fish-care.svg",
  "datePublished":"{sp['date']}",
  "dateModified":"{sp['date']}",
  "author":{{"@type":"Organization","name":"FishCare AI Editorial Team"}},
  "publisher":{{"@type":"Organization","name":"FishCare AI","url":"https://www.fishcareai.com"}}
}}</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260801-global-nav"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a title="FishCare AI" class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/guides/">Guides</a>
    <a class="nl act" href="/species/">Encyclopedia</a>
    <a class="nl" href="/fish-health/">Fish Health</a>
    <a class="nl" href="/#tools">Tools</a>
    <a class="nl" href="/about/">About Us</a>
  </div>
</nav>

<section class="sp-hero">
  <img onerror="this.onerror=null;this.src='/assets/fish-images/fishcare-image-fallback.svg';" class="sp-hero-img" src="{sp['wiki_img']}" alt="{sp['img_alt']}" width="1280" height="340"/>
  <div class="sp-hero-overlay"></div>
  <div class="sp-hero-inner">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="/wiki/">Encyclopedia</a><span>/</span>
      <span style="color:rgba(255,255,255,.85)">{sp['breadcrumb_label']}</span>
    </div>
    <div class="sp-tag">{sp['tag']}</div>
    <h1>{sp['name']}</h1>
    <div class="sci-name">{sp['sci_name']} — {sp['sci_author']}</div>
    <div class="sp-meta-row">
      <div class="sp-meta-item">🏠 <strong>Origin:</strong>&nbsp;{sp['origin']}</div>
      <div class="sp-meta-item">📏 <strong>Size:</strong>&nbsp;{sp['size']}</div>
      <div class="sp-meta-item">⏳ <strong>Lifespan:</strong>&nbsp;{sp['lifespan']}</div>
      <div class="sp-meta-item">⭐ <strong>Care level:</strong>&nbsp;{sp['care_level']}</div>
    </div>
  </div>
</section>

<div class="con">
  <div class="sp-layout">
    <div class="artc" id="article">

      <p>{sp['intro']}</p>

      <h2 id="taxonomy">Taxonomy &amp; Classification</h2>
      <p>{sp['taxonomy_intro']}</p>
      <table class="ptbl">
        <tr><th>Rank</th><th>Classification</th></tr>
        {tax_rows}
      </table>

      <h2 id="habitat">Natural Habitat</h2>
      <p>{sp['habitat_text']}</p>
      <ul>{habitat_bullets_html}</ul>

      <figure>
        <img onerror="this.onerror=null;this.src='/assets/fish-images/fishcare-image-fallback.svg';" src="{sp['wiki_img']}" alt="{sp['img_alt']}" loading="lazy"/>
        <figcaption>{sp['img_caption']}</figcaption>
      </figure>

      <h2 id="water">Water Requirements</h2>
      {water_html}
      <div class="callout">{sp['water_note']}</div>

      <h2 id="tank">Tank Setup</h2>
      <p>{sp['tank_setup_text']}</p>
      <ul>{tank_bullets_html}</ul>

      <h2 id="{sp['extra_section_id']}">{sp['extra_section_title']}</h2>
      {sp['extra_section_content']}

      <h2 id="diet">Diet &amp; Feeding</h2>
      <p>{sp['diet_text']}</p>
      <ul>{diet_bullets_html}</ul>
      <div class="callout">{sp['diet_note']}</div>

      <h2 id="tank-mates">Compatible Tank Mates</h2>
      <p>{sp['tank_mates_text']}</p>
      <ul>{tank_good_html}</ul>
      <p>Avoid: {sp['tank_mates_avoid']}</p>

      <h2 id="health">Common Health Issues</h2>
      <ul>{health_html}</ul>
      <div class="callout callout-warn">{sp['health_note']}</div>

      <div class="abox">
        <div class="aav">✓</div>
        <div><strong>Editorial review</strong><p>This species profile was reviewed for biological accuracy and practical aquarium care guidance by the FishCare AI editorial team.</p></div>
      </div>

      <h2 style="border-top:1px solid var(--bd);padding-top:20px;margin-top:30px">Related Guides &amp; Species</h2>
      <div class="guide-links">{links_html}</div>
    </div>

    <aside class="sp-sidebar">
      <div class="qf-card">
        <div class="qf-head">Quick Facts</div>
        <table class="qf-table">{qf_html}</table>
      </div>
      <div class="toc-card">
        <h4>Contents</h4>
        {toc_html}
      </div>
    </aside>
  </div>
</div>

<footer class="ft">
  <div class="con">
    <div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div>
  </div>
  <nav class="legal-links" aria-label="Legal and company information"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/editorial-policy/">Editorial Policy</a><a href="/privacy/">Privacy</a><a href="/image-credits/">Image Credits</a></nav>
</footer>
</body>
</html>"""


def main():
    for sp in SPECIES:
        out_dir = WIKI / sp["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        html = build_page(sp)
        out_path.write_text(html, encoding="utf-8")
        print(f"✓ /wiki/{sp['slug']}/  ({len(html):,} bytes)")
    print(f"\nDone — {len(SPECIES)} pages generated.")


if __name__ == "__main__":
    main()
