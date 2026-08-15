"""
generate_tank_size_pages.py
────────────────────────────
Generates /tanks/{size}-gallon-fish-tank/index.html for standard aquarium sizes.
Also generates /tanks/index.html cluster hub.

Run: python3 generate_tank_size_pages.py
"""

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
OUT  = REPO / "tanks"

# ── Tank data ─────────────────────────────────────────────────────────────────
TANKS = {
    5: {
        "slug": "5-gallon",
        "title_kw": "5 Gallon Fish Tank",
        "dims": {"l": 16, "w": 8, "h": 10, "notes": "Standard 5-gal (Aqueon/Marineland)"},
        "level": "beginner",
        "level_note": "Ideal single-species nano tank",
        "best_fish": [
            ("Betta Fish (1 male)", "/wiki/betta-fish/", "The definitive 5-gallon fish. One male betta thrives with a heater, gentle filter, and plants."),
            ("Cherry Shrimp (10–15)", "/wiki/cherry-shrimp/", "A shrimp colony is perfect: low bioload, entertaining to watch, excellent algae cleaners."),
            ("Nerite Snails (2–3)", "/wiki/nerite-snail/", "Algae-grazing snails that complement a betta or shrimp tank without overcrowding."),
            ("Endler's Livebearers (5–6)", "/wiki/guppy/", "Tiny, active, and colourful — endlers are one of the few schooling fish safe in 5 gallons."),
        ],
        "avoid": ["Goldfish (need 20+ gal)", "Neon Tetras (schooling, need 10+ gal)", "Guppies in groups (need 10+ gal)", "Any fish over 2 inches"],
        "filter": "Small sponge filter or hang-on-back rated up to 10 gal (e.g., Aqueon QuietFlow 10). Low flow is critical — bettas dislike strong currents.",
        "heater": "25 W adjustable submersible heater (Eheim Jäger or Fluval E25).",
        "lighting": "5–10W LED, 6–8 hrs per day. Low-light plants (java fern, anubias) thrive at this level.",
        "cycle_time": "3–4 weeks with a bacteria starter and daily ammonia dosing.",
        "stocking_rule": "In 5 gallons stick to a single species. The nitrogen cycle is fragile at this volume — one betta or a shrimp colony, not both.",
        "water_changes": "25–30% weekly for a betta; 15–20% every 10 days for a shrimp-only setup.",
        "cost_est": "$50–$120 all-in (tank, filter, heater, thermometer, conditioner, lid, light).",
        "faqs": [
            ("How many fish can you put in a 5 gallon tank?",
             "For a 5 gallon fish tank, a single betta fish is the ideal choice — it gets the full territory it needs. If you prefer community fish, a colony of 10–15 cherry shrimp or 5–6 endler's livebearers are the safest options. Avoid putting multiple species in a 5-gallon tank, as the small water volume makes parameter swings dangerous."),
            ("Is a 5 gallon tank good for a betta fish?",
             "Yes — a 5 gallon tank is the recommended minimum for a single male betta fish. It provides enough water volume to maintain stable temperature and water quality, and enough space for the betta to swim, explore, and display its fins. Tanks smaller than 5 gallons make it difficult to keep ammonia and nitrite at 0 ppm."),
            ("What filter should I use for a 5 gallon fish tank?",
             "Use a sponge filter or a small hang-on-back (HOB) filter rated up to 10 gallons. Aim for a turnover of about 3–5× the tank volume per hour (15–25 GPH). Avoid filters designed for large tanks — the flow will be too strong for bettas and too disruptive for shrimp."),
            ("Can goldfish live in a 5 gallon fish tank?",
             "No. A single fancy goldfish needs a minimum of 20 gallons; a single-tailed (comet) goldfish needs 55+ gallons. Goldfish produce a large amount of ammonia and grow to 6–12 inches. Keeping goldfish in a 5 gallon tank causes chronic stress, stunted growth, and shortened lifespan."),
        ],
    },
    10: {
        "slug": "10-gallon",
        "title_kw": "10 Gallon Fish Tank",
        "dims": {"l": 20, "w": 10, "h": 12, "notes": "Standard 10-gal (industry standard beginner tank)"},
        "level": "beginner",
        "level_note": "The classic beginner starter tank",
        "best_fish": [
            ("Betta Fish (1 male)", "/wiki/betta-fish/", "A betta in a 10-gallon gets more space and more stable water than in a 5-gallon — an upgrade worth making."),
            ("Neon Tetras (6–8)", "/wiki/neon-tetra/", "A small neon tetra school fits well and stays peaceful with most tank mates."),
            ("Guppies (6)", "/wiki/guppy/", "Three males or a 1M:2F trio make a colourful 10-gallon community."),
            ("Corydoras Catfish (4–6 pygmy)", "/wiki/pygmy-corydoras/", "Pygmy corydoras (not standard corys) are sized right for 10 gallons; keep in groups of 5+."),
            ("Cherry Shrimp (20–30)", "/wiki/cherry-shrimp/", "A heavily planted 10-gallon shrimp tank is a rewarding low-maintenance setup."),
            ("Ember Tetras (8–10)", "/wiki/ember-tetra/", "Tiny schooling fish that thrive in planted 10-gallon tanks."),
        ],
        "avoid": ["Angelfish (need tall 30+ gal)", "Goldfish (need 20+ gal)", "Oscar Fish (need 75+ gal)", "Tiger Barbs in groups (need 30+ gal)"],
        "filter": "Hang-on-back rated 20–30 gal (Aqueon QuietFlow 20 or Fluval C2) for proper cycling margin, or dual sponge filters.",
        "heater": "50 W adjustable heater. In a 10-gallon, temperature swings happen fast — use an adjustable model.",
        "lighting": "10–20 W LED, 8 hrs/day. Enough for java fern, hornwort, and low-demand live plants.",
        "cycle_time": "3–5 weeks. A 10-gallon is the ideal size for learning the nitrogen cycle.",
        "stocking_rule": "Apply the 1 inch of fish per gallon rule with caution — 10 gallons supports ≈6–8 small (1–1.5 in) fish maximum. Don't max out the rule; stable water matters more than headcount.",
        "water_changes": "20–25% weekly. With light stocking, every 10 days is acceptable.",
        "cost_est": "$80–$200 depending on whether you buy a starter kit or individual components.",
        "faqs": [
            ("How many fish can you put in a 10 gallon tank?",
             "A 10 gallon fish tank can comfortably house 6–8 small fish (1–1.5 inches adult size), such as neon tetras or ember tetras, or one betta with a few bottom-dwellers like pygmy corydoras. The 'one inch per gallon' rule is a rough guide — bioload, filtration quality, and maintenance schedule matter more than headcount."),
            ("What fish are best for a 10 gallon tank?",
             "The best fish for a 10 gallon tank are small schooling species: neon tetras (school of 6), ember tetras (school of 8), guppies (group of 6), or a single betta fish. Add pygmy corydoras as bottom-dwellers if you have a group of 5 or more. Avoid goldfish, angelfish, or any species that reaches over 3 inches."),
            ("Can I put goldfish in a 10 gallon tank?",
             "No — goldfish need a minimum of 20 gallons for a single fancy goldfish and 55+ gallons for a single comet or common goldfish. Goldfish grow to 6–12 inches, produce heavy ammonia, and will quickly foul a 10-gallon tank."),
            ("Do I need a heater in a 10 gallon fish tank?",
             "Yes, if you keep tropical fish (which most aquarium fish are). A 50W adjustable heater is ideal for a 10-gallon tank. Without a heater, room-temperature fluctuations can cause temperature swings that stress or kill tropical fish. The only exception is coldwater species like white cloud mountain minnows, which prefer 64–72°F without a heater."),
        ],
    },
    20: {
        "slug": "20-gallon",
        "title_kw": "20 Gallon Fish Tank",
        "dims": {"l": 24, "w": 12, "h": 16, "notes": "20 Long: 30×12×12; 20 High: 24×12×16"},
        "level": "beginner",
        "level_note": "Best beginner community tank size",
        "best_fish": [
            ("Neon Tetras (10–12)", "/wiki/neon-tetra/", "A full school of neons makes an electric display in a 20-gallon long."),
            ("Guppies (10–12)", "/wiki/guppy/", "A mixed group with 1M:2F ratio keeps a 20-gallon lively without constant fry pressure."),
            ("Corydoras Catfish (6)", "/wiki/corydoras/", "Emerald or peppered cories (standard size) fit a 20-gallon; they need groups of 6+."),
            ("Betta Fish (1) + Shrimp", "/wiki/betta-fish/", "A 20-gallon gives a betta room for plants and the space needed to keep snails or a cherry shrimp colony."),
            ("Harlequin Rasboras (8–10)", "/wiki/harlequin-rasbora/", "One of the best all-around schooling fish — peaceful, hardy, and visually striking."),
            ("Platy (8)", "/wiki/platy/", "A colony of platys in a 20-gallon manages breeding naturally through fry predation from the adults."),
        ],
        "avoid": ["Angelfish (need 30+ gal, prefer tall tanks)", "Oscar Fish (need 75+ gal)", "Rainbow Shark (need 55+ gal)", "Goldfish (high bioload)"],
        "filter": "HOB rated 40–50 gal (Aquaclear 50, Fluval C3) or a canister. Moderate flow (40–80 GPH) is ideal.",
        "heater": "75–100 W adjustable heater for reliable temperature stability.",
        "lighting": "20–30 W LED, 8–10 hrs/day. Supports a full planted community setup.",
        "cycle_time": "3–5 weeks. Easiest size to cycle because water volume buffers ammonia spikes better than a 10-gallon.",
        "stocking_rule": "A 20-gallon comfortably holds 1 inch of fish per gallon — that's roughly 12–15 small fish with good filtration. Aim for 80% of this max to keep parameters easy to manage.",
        "water_changes": "20–25% weekly. With light to moderate stocking, every 10–14 days is acceptable with a good filter.",
        "cost_est": "$120–$350 depending on kit vs. individual components; add planted-tank lighting for $50–$120 more.",
        "faqs": [
            ("How many fish can you put in a 20 gallon tank?",
             "A 20 gallon fish tank can hold approximately 10–15 small fish (1–2 inch adults) with good filtration and weekly water changes. A well-planted 20-gallon might house a school of 10 neon tetras, 6 corydoras, and 2–3 guppies. Always under-stock by 20% to allow for error — a 20-gallon is forgiving, but overcrowding collapses fast."),
            ("What is the best fish for a 20 gallon tank?",
             "The best fish for a 20 gallon tank are schooling fish like neon tetras or harlequin rasboras (8–10), combined with corydoras catfish (6) as bottom-dwellers. Alternatively, a single betta fish with 6–8 peaceful dither fish (ember tetras, pygmy corydoras) makes an excellent 20-gallon community. Avoid any fish over 4 inches."),
            ("Is a 20 gallon fish tank good for beginners?",
             "Yes — a 20 gallon fish tank is widely considered the ideal beginner community tank. It's big enough to maintain stable water parameters, supports a diverse community, and is still manageable in terms of space and cost. The 10-gallon is cheaper, but the 20-gallon is more forgiving of beginner mistakes."),
            ("What size filter do I need for a 20 gallon aquarium?",
             "A filter rated for 40–50 gallons works well for a 20 gallon tank, because aquarium filters are often rated under ideal (empty-tank) conditions. Popular choices are the AquaClear 50 or Fluval C3, both rated for tanks up to 50 gallons. This gives you headroom for moderate stocking and occasional missed maintenance."),
        ],
    },
    29: {
        "slug": "29-gallon",
        "title_kw": "29 Gallon Fish Tank",
        "dims": {"l": 30, "w": 12, "h": 18, "notes": "Standard 29-gal (30×12×18 in) — taller than the 30-gal long"},
        "level": "beginner",
        "level_note": "Taller than 20-gal — great for angelfish",
        "best_fish": [
            ("Angelfish (2–3 juveniles)", "/wiki/angelfish/", "The 18-inch height of a 29-gallon is the minimum for a pair of juvenile angelfish."),
            ("Neon Tetras (12–15)", "/wiki/neon-tetra/", "A large neon school around angelfish is a classic pairing — though juvenile angels may eat very small neons."),
            ("Dwarf Gourami (1 pair)", "/wiki/dwarf-gourami/", "A pair of dwarf gouramis adds colour to the mid-water column."),
            ("Corydoras (6)", "/wiki/corydoras/", "Bottom activity from a cory group balances the mid-level and top swimmers."),
            ("Harlequin Rasbora (10)", "/wiki/harlequin-rasbora/", "Active mid-level schooling fish that use all layers of the tank."),
        ],
        "avoid": ["Oscar Fish (need 75+ gal)", "Goldfish", "Rainbow Shark (one needs 55+ gal)", "Large cichlids"],
        "filter": "HOB rated 50–70 gal (AquaClear 70, Fluval C4) or a small canister. Taller tanks benefit from outlet placement near the surface.",
        "heater": "100–150 W adjustable heater.",
        "lighting": "30–40 W LED strip rated for planted tanks.",
        "cycle_time": "3–5 weeks.",
        "stocking_rule": "~15–18 small-to-medium fish with good filtration, or fewer medium fish (e.g., 2 angelfish + 12 tetras + 6 cories).",
        "water_changes": "20–25% weekly.",
        "cost_est": "$150–$400.",
        "faqs": [
            ("What fish can live in a 29 gallon tank?",
             "A 29 gallon fish tank is one of the best choices for a pair of juvenile angelfish, supported by a school of 12–15 neon or cardinal tetras and 6 corydoras catfish. The extra height compared to a 20-gallon long makes it uniquely suitable for tall-bodied fish like angelfish. Dwarf gouramis, harlequin rasboras, and cherry barbs are also excellent choices."),
            ("Is a 29 gallon tank good for angelfish?",
             "A 29 gallon fish tank is the minimum size for a single angelfish or a compatible pair of juvenile angelfish. The standard 18-inch height accommodates their tall bodies and fin length. However, a 55-gallon or larger is recommended as angelfish mature and become more territorial, especially if breeding."),
            ("How many neon tetras can I put in a 29 gallon tank?",
             "You can safely keep 12–15 neon tetras in a 29 gallon fish tank, provided filtration is adequate and you perform weekly 20–25% water changes. A school of 12 creates an impressive display while leaving room for bottom-dwellers like corydoras and a mid-level species like a dwarf gourami."),
            ("What filter is best for a 29 gallon aquarium?",
             "The AquaClear 70 or Fluval C4 (both rated up to 70 gallons) are popular choices for a 29 gallon fish tank, providing extra filtration capacity. An alternatively, an Oase BioMaster Thermo 250 canister filter handles the 29-gallon with ease and maintains steady temperature."),
        ],
    },
    40: {
        "slug": "40-gallon",
        "title_kw": "40 Gallon Fish Tank",
        "dims": {"l": 36, "w": 18, "h": 17, "notes": "40 Breeder: 36×18×17 in (most popular 40-gal footprint)"},
        "level": "beginner",
        "level_note": "The 40 Breeder is a hobbyist favourite",
        "best_fish": [
            ("Discus (2–3 juveniles)", "/wiki/discus/", "A 40-gallon breeder is a practical starting point for a discus colony with excellent filtration."),
            ("Angelfish (4–5)", "/wiki/angelfish/", "The wide footprint of the 40 breeder gives angelfish territory they need as they mature."),
            ("Rainbow Fish (8–10)", "/wiki/guppy/", "Boesemani or Australian rainbowfish shine in groups of 8+ in a 40-gallon."),
            ("Corydoras Catfish (8)", "/wiki/corydoras/", "A larger cory group shows natural shoaling behaviour and cleans up bottom waste efficiently."),
            ("Cherry Barb (10–12)", "/wiki/cherry-barb/", "A large school of cherry barbs makes a striking red display. Males colour up beautifully in groups."),
            ("German Blue Ram (1 pair)", "/wiki/angelfish/", "A breeding pair of rams in a 40 breeder is a classic setup; warm, soft water with corydoras companions."),
        ],
        "avoid": ["Oscar Fish (need 75+ gal)", "Full-grown koi (pond fish)", "Large plecos (need 75+ gal once grown)"],
        "filter": "Canister filter rated 80–100 gal (Fluval 307, Oase BioMaster 350) — the 40 breeder is often used for fish that need pristine water (discus, rams).",
        "heater": "150–200 W adjustable. Two 100 W heaters for redundancy is common in discus setups.",
        "lighting": "40–60 W LED. The wide footprint suits aquascaping layouts (Dutch, Iwagumi).",
        "cycle_time": "4–6 weeks. Larger tanks cycle more slowly but crash less dramatically.",
        "stocking_rule": "15–25 small-to-medium fish, or 5–8 medium fish (angelfish, discus) with supporting species.",
        "water_changes": "20–30% weekly, or 50% twice weekly for discus.",
        "cost_est": "$200–$600 for a community setup; $400–$1,200+ for a discus setup with a chiller.",
        "faqs": [
            ("What fish can live in a 40 gallon tank?",
             "A 40 gallon fish tank — particularly the popular 40 breeder (36×18×17 in) — is large enough for angelfish (4–5), discus (2–3 juveniles), rainbow fish (8–10), or a species tank with a pair of German blue rams and supporting corydoras. Its wide footprint is also popular for aquascaping, planted tanks, and breeding projects."),
            ("Is a 40 gallon tank good for discus?",
             "A 40 gallon fish tank is a viable starting size for 2–3 juvenile discus, but adult discus (8 inches) benefit from a 55-gallon minimum. Use a high-capacity canister filter, two heaters for redundancy, and perform 50% water changes twice weekly. Discus are sensitive to ammonia; a 40-gallon requires a mature biological filter before introducing them."),
            ("What is a 40 gallon breeder tank?",
             "A 40 gallon breeder tank (36×18×17 in) is a wide, shallow aquarium designed originally for breeding fish. Its wide footprint gives more bottom and mid-level territory than a tall 40-gallon, making it a favourite for community tanks, planted aquascapes, and pairs of cichlids. It holds 40 US gallons and is one of the most versatile tank sizes in the hobby."),
            ("What size filter do I need for a 40 gallon tank?",
             "For a 40 gallon fish tank, use a canister or HOB filter rated for 80–100 gallons. The Fluval 307 (rated up to 70 gal, but performs well beyond in practice) or the AquaClear 110 are popular choices. Over-filtering is rarely a problem and provides a safety buffer if you miss a water change."),
        ],
    },
    55: {
        "slug": "55-gallon",
        "title_kw": "55 Gallon Fish Tank",
        "dims": {"l": 48, "w": 13, "h": 20, "notes": "Standard 55-gal: 48×13×20 in"},
        "level": "intermediate",
        "level_note": "The classic community tank footprint",
        "best_fish": [
            ("Angelfish (5–6)", "/wiki/angelfish/", "A colony of angelfish in a 55 is visually stunning; the 20-inch height accommodates their tall body and fins."),
            ("Oscar Fish (1–2)", "/wiki/oscar/", "One oscar fits a 55-gallon; two need 100+ gallons due to territorial aggression."),
            ("Discus (5–6)", "/wiki/discus/", "A proper discus colony in a pristine 55-gallon with soft, warm water and frequent changes is achievable."),
            ("Rainbow Fish (12–15)", "/wiki/guppy/", "Large rainbow fish schools in a 55 create a shimmering, active display."),
            ("Clown Loach (4–5 juveniles)", "/wiki/clown-loach/", "Clown loaches reach 12 inches — a 55 is their minimum adult home; start with juveniles."),
            ("Goldfish (2–3 fancy)", "/wiki/goldfish/", "Two fancy goldfish in a 55 with a large canister filter is a comfortable, long-term home."),
        ],
        "avoid": ["Single-tailed goldfish (need 75+ gal)", "Two adult oscars (need 100+ gal)", "Koi (pond fish)"],
        "filter": "Large canister filter rated 100–150 gal (Fluval FX4, Eheim Classic 600) — the 55's long shape benefits from dual spray-bar outlet to distribute flow.",
        "heater": "200–300 W adjustable heater.",
        "lighting": "60–80 W LED. The 48-inch length suits dual-fixture lighting for aquascaping.",
        "cycle_time": "4–6 weeks. Add fish gradually in groups of 3–4 after the cycle is established.",
        "stocking_rule": "25–40 small fish, 10–15 medium fish, or 1–2 large fish with supporting smaller species.",
        "water_changes": "25% weekly for community tanks; 50% weekly for oscar or discus tanks.",
        "cost_est": "$250–$800 for a community setup. Oscar and discus setups run $400–$1,500+.",
        "faqs": [
            ("What fish can live in a 55 gallon tank?",
             "A 55 gallon fish tank supports a wide range of species: a colony of 5–6 angelfish, 1–2 oscar fish, a discus colony of 5–6 in pristine water, 2–3 fancy goldfish, or a large community of 25–30 small fish (tetras, rasboras, corydoras). The 48-inch length is a classic size for long-swimming species and aquascaping layouts."),
            ("How many fish can you put in a 55 gallon tank?",
             "A 55 gallon fish tank can hold approximately 25–35 small fish (1–2 inch adults) with excellent filtration and weekly water changes. With medium fish (3–5 inches), aim for 12–15 individuals. With large fish like oscars, limit to 1 fish per 55 gallons. Always under-stock by 10–20% relative to the theoretical maximum."),
            ("Can an Oscar live in a 55 gallon tank?",
             "A single oscar fish can live in a 55 gallon tank as a long-term home, but barely — oscar fish reach 12–14 inches and are heavy waste producers. A 75-gallon is better for one oscar; two oscars need 100+ gallons. If you already have an oscar in a 55, provide a large canister filter (rated 150+ gal) and perform 30–50% water changes weekly."),
            ("What size filter for a 55 gallon fish tank?",
             "For a 55 gallon fish tank, use a canister filter rated for 100–150 gallons. Top choices include the Fluval FX4 (rated 250 gal in practice), Eheim Professional 4+ 350, or SunSun HW-304. For heavy bioload species like oscars or goldfish, run two filters or size up to the Fluval FX6."),
        ],
    },
    75: {
        "slug": "75-gallon",
        "title_kw": "75 Gallon Fish Tank",
        "dims": {"l": 48, "w": 18, "h": 21, "notes": "Standard 75-gal: 48×18×21 in"},
        "level": "intermediate",
        "level_note": "Same length as 55 but 5 in wider — much more stable",
        "best_fish": [
            ("Oscar Fish (1, long-term home)", "/wiki/oscar/", "A single adult oscar is comfortable in a 75-gallon — the gold standard for oscar keepers."),
            ("Discus (6–8)", "/wiki/discus/", "A proper discus colony with south american biotope companions fits comfortably."),
            ("Clown Loach (5–6)", "/wiki/clown-loach/", "Adult clown loaches (up to 12 in) need the length and volume a 75-gallon provides."),
            ("Angelfish (6–8)", "/wiki/angelfish/", "A colony that can establish a natural pecking order with enough room to retreat."),
            ("Goldfish (3–4 fancy)", "/wiki/goldfish/", "A proper goldfish tank with powerful filtration and high water quality."),
        ],
        "avoid": ["Two adult oscars (need 100+ gal)", "Full-grown common or comet goldfish (need pond)", "Koi"],
        "filter": "High-capacity canister or sump; Fluval FX4 or FX6, Eheim Pro 4e 600. At 75 gallons, water quality is more stable, but a large filter pays dividends.",
        "heater": "250–300 W adjustable heater, or two 150 W units.",
        "lighting": "80–100 W LED for planted tanks; standard output for fish-only.",
        "cycle_time": "4–8 weeks. Add fish very slowly — a 75 takes longer to establish than a 55.",
        "stocking_rule": "30–50 small fish, or fewer large fish. Always work from your target bioload backward to filter selection.",
        "water_changes": "25–30% weekly. Oscar and goldfish tanks benefit from 50% weekly.",
        "cost_est": "$400–$1,200 for equipment; add $200–$500 for decor, plants, and livestock.",
        "faqs": [
            ("What fish are best for a 75 gallon tank?",
             "A 75 gallon fish tank is ideal for a single adult oscar fish, a discus colony of 6–8, 5–6 adult clown loaches, a colony of 6–8 angelfish, or 3–4 fancy goldfish with powerful filtration. Its wide 18-inch depth (vs 13 in on the 55) creates significantly more stable water chemistry and more swimming territory."),
            ("How many fish can you put in a 75 gallon tank?",
             "A 75 gallon fish tank can house approximately 30–45 small fish (1–2 inches), 15–20 medium fish (3–4 inches), or 1–2 large fish (10–14 inches) with supporting smaller species. The 5-inch extra width compared to a 55-gallon noticeably improves water stability and territory distribution."),
            ("Is a 75 gallon good for an Oscar?",
             "Yes — a 75 gallon fish tank is one of the best long-term homes for a single adult oscar. At 12–14 inches, an oscar needs the swimming length and water volume a 75-gallon provides. Use a Fluval FX4 or FX6 for filtration, perform 40–50% weekly water changes, and avoid adding other large or fin-nipping tank mates."),
            ("How heavy is a 75 gallon fish tank when full?",
             "A 75 gallon fish tank weighs approximately 850–900 lbs when full (water ~625 lbs, tank glass ~140 lbs, substrate ~80 lbs, decorations ~20–40 lbs). Place it on a dedicated aquarium stand rated for this weight, directly over floor joists. Avoid placing a 75-gallon on an upper floor without consulting a structural engineer."),
        ],
    },
    100: {
        "slug": "100-gallon",
        "title_kw": "100 Gallon Fish Tank",
        "dims": {"l": 60, "w": 18, "h": 20, "notes": "Common 100-gal: 60×18×20 in (dimensions vary by brand)"},
        "level": "intermediate",
        "level_note": "Large display tank for serious hobbyists",
        "best_fish": [
            ("Oscar Fish (2)", "/wiki/oscar/", "Two oscars can coexist in 100 gallons if introduced young together, with plenty of hiding spots."),
            ("Discus (8–10)", "/wiki/discus/", "A full discus colony with rummy nose tetras and corydoras in soft, warm water."),
            ("Clown Loach (6–8)", "/wiki/clown-loach/", "A proper clown loach group finally has the space for natural shoaling behaviour."),
            ("Saltwater Community", "/wiki/angelfish/", "100 gallons opens the door to marine setups: a FOWLR with tangs, wrasses, or a small reef."),
        ],
        "avoid": ["More than 2 adult oscars (fight risk)", "Koi (need ponds)"],
        "filter": "Sump system or dual large canisters (e.g., two Fluval FX4s, or an Eheim Pro 4e 600 + FX4). At 100 gallons, a sump with biological media is the professional approach.",
        "heater": "300–400 W adjustable, or two 200 W units.",
        "lighting": "High-output LED spread across 60 inches; dual fixtures for planted or reef tanks.",
        "cycle_time": "6–10 weeks. Large tanks cycle slowly — do not rush stocking.",
        "stocking_rule": "Calculate target bioload from adult fish sizes; 100 gallons supports large fish that would suffer in smaller tanks.",
        "water_changes": "25–35% weekly. With a large sump, the total water volume may be 120+ gallons.",
        "cost_est": "$800–$3,000+ depending on species and equipment quality.",
        "faqs": [
            ("What can you put in a 100 gallon fish tank?",
             "A 100 gallon fish tank opens the door to large species: two oscar fish, a full discus colony of 8–10, a large clown loach group, a large cichlid community, or the beginning of a marine fish-only setup. It also suits community tanks with 40–60 small fish in a planted aquascape."),
            ("How heavy is a 100 gallon fish tank?",
             "A 100 gallon fish tank weighs approximately 1,000–1,100 lbs when full (water ~835 lbs, tank ~180 lbs, substrate ~100 lbs, decorations). Always place on a rated aquarium stand over floor joists, and verify the floor load capacity before setup — this is especially important on upper floors."),
            ("What filter do I need for a 100 gallon fish tank?",
             "A 100 gallon fish tank benefits from a sump system (rated 150–200 gal total water volume) or two large canister filters running in parallel. Dual Fluval FX4s, a single FX6, or a Reef Octopus sump are all proven options. Aim for a combined flow rate of 800–1,200 GPH through the filter media."),
            ("Is a 100 gallon aquarium hard to maintain?",
             "A 100 gallon aquarium requires 25–35 weekly water changes (25–35 gallons of water per change), a large filtration system, and regular gravel vacuuming. However, the large water volume actually makes the system more stable and forgiving than smaller tanks — water parameters change slowly, giving you more time to respond to problems."),
        ],
    },
    125: {
        "slug": "125-gallon",
        "title_kw": "125 Gallon Fish Tank",
        "dims": {"l": 72, "w": 18, "h": 22, "notes": "Standard 125-gal: 72×18×22 in — 6 ft long"},
        "level": "intermediate",
        "level_note": "6-foot show tank — serious hobbyist territory",
        "best_fish": [
            ("Oscar Fish (2–3)", "/wiki/oscar/", "With 6 feet of swimming space, 2–3 oscars have territory to coexist — introduced young."),
            ("Large Cichlid Community", "/wiki/angelfish/", "Geophagus, severums, or a cichlid group from the same region can thrive in this space."),
            ("Discus (10–12)", "/wiki/discus/", "A show-quality discus colony with a complete biotope is achievable."),
            ("Marine Reef (beginner FOWLR)", "/wiki/angelfish/", "125 gallons is a premium starting size for a fish-only marine tank with live rock."),
        ],
        "avoid": ["Koi (pond fish)", "More than 3 adult oscars"],
        "filter": "Large sump system (30–40 gal sump), Fluval FX6, or external commercial filter. At this scale, a sump is strongly recommended.",
        "heater": "Two 300 W heaters for redundancy.",
        "lighting": "Dual high-output LED strips across 72 inches; essential for planted tanks or reef.",
        "cycle_time": "8–12 weeks for a new 125-gallon. Patience is essential.",
        "stocking_rule": "Start with 20% of planned stocking after the cycle; add fish monthly in small groups.",
        "water_changes": "30–40 gallons weekly (25–30% of total volume). Use a Python or pump-assisted system.",
        "cost_est": "$1,000–$5,000+ including stand, sump, lighting, and livestock.",
        "faqs": [
            ("What fish can you put in a 125 gallon tank?",
             "A 125 gallon fish tank is large enough for a 2–3 oscar cichlid community, a 10–12 discus colony with a full biotope setup, a large cichlid species tank, or the beginning of a serious marine (FOWLR) system. Its 6-foot length makes it a true show-piece tank."),
            ("How many fish can live in a 125 gallon aquarium?",
             "A 125 gallon fish tank can house approximately 50–70 small fish (1–2 inch adults), 25–35 medium fish (3–5 inches), or 3–4 large fish (10–14 inches). Work backward from your target species' adult size and bioload — large fish like oscars and discus are much harder on water quality than small schooling fish."),
            ("How much does it cost to set up a 125 gallon fish tank?",
             "Setting up a 125 gallon fish tank typically costs $1,000–$5,000+ depending on equipment choices and livestock. Budget for: tank + stand ($300–$600), large canister or sump system ($300–$800), two heaters ($80–$200), quality lighting ($150–$600), substrate and decor ($100–$400), and fish ($50–$2,000+ depending on species)."),
            ("Is a 125 gallon fish tank hard to maintain?",
             "A 125 gallon fish tank requires commitment — weekly water changes of 30–40 gallons, regular gravel vacuuming, filter maintenance every 4–6 weeks, and consistent water testing. However, like all large tanks, it is more stable than small tanks and more forgiving of missed maintenance. The biggest challenge is the physical labour of water changes."),
        ],
    },
}

# ── Shared CSS ────────────────────────────────────────────────────────────────
CSS = """:root{--p:#1B5E8B;--pl:#2E84C0;--pd:#0F3D5E;--s:#2E9E7D;--bg:#F0F7FF;--tx:#1A2B3C;--mu:#5A7A94;--bd:#D0E4F0;--ok:#27AE60;--wn:#F39C12;--er:#E74C3C}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--tx);line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--p);text-decoration:none}
.con{max-width:1100px;margin:0 auto;padding:0 22px}
h1{font-size:clamp(1.7rem,3.8vw,2.5rem);font-weight:800;line-height:1.2}
h2{font-size:1.2rem;font-weight:700}h3{font-size:1rem;font-weight:700}
p{margin-bottom:.85rem;color:var(--mu)}p:last-child{margin-bottom:0}
.nb{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid var(--bd);padding:0 22px;height:64px;display:flex;align-items:center;justify-content:space-between}
.brand img{height:36px;width:auto;display:block}
.nlinks{display:flex;gap:2px}.nl{padding:7px 13px;border-radius:8px;font-weight:500;font-size:.86rem;color:var(--mu);transition:all .15s}.nl:hover{color:var(--p);background:rgba(27,94,139,.07)}
.hero{background:linear-gradient(135deg,#051C2A,#0F3D5E,#1B5E8B);padding:52px 22px 44px;color:#fff}
.hero .con{max-width:1100px;margin:0 auto}
.breadcrumb{display:flex;gap:6px;font-size:.78rem;color:rgba(255,255,255,.55);margin-bottom:14px;flex-wrap:wrap}
.breadcrumb a{color:rgba(255,255,255,.7)}.breadcrumb a:hover{color:#fff}.breadcrumb span{color:rgba(255,255,255,.35)}
.tag{display:inline-block;padding:3px 11px;border-radius:20px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;background:rgba(255,255,255,.15);color:rgba(255,255,255,.9);margin-bottom:10px}
.hero h1{color:#fff;margin-bottom:8px}
.hero .sub{color:rgba(255,255,255,.75);font-size:1rem;margin-top:6px}
.dim-chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.dim-chip{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:8px;padding:7px 14px;color:#fff;font-size:.82rem;font-weight:600}
.dim-chip span{opacity:.7;font-weight:400;font-size:.76rem;display:block;margin-top:2px}
.layout{display:grid;grid-template-columns:1fr 270px;gap:28px;max-width:1100px;margin:32px auto 60px;padding:0 22px}
@media(max-width:860px){.layout{grid-template-columns:1fr}.sidebar{display:none}}
.card{background:#fff;border-radius:16px;border:1px solid var(--bd);padding:26px 28px;margin-bottom:20px;box-shadow:0 4px 16px rgba(27,94,139,.06)}
.card h2{color:var(--pd);margin-bottom:14px;padding-bottom:10px;border-bottom:1.5px solid var(--bd)}
.card p{font-size:.95rem;line-height:1.78}
.card ul,.card ol{margin:8px 0 12px 18px}
.card li{font-size:.94rem;line-height:1.7;color:var(--mu);margin-bottom:5px}
.fish-item{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid var(--bd)}
.fish-item:last-child{border-bottom:none}
.fish-badge{background:var(--pd);color:#fff;border-radius:6px;padding:4px 10px;font-size:.72rem;font-weight:700;white-space:nowrap;flex-shrink:0;margin-top:3px}
.fish-info h3{margin:0 0 4px;font-size:.93rem}
.fish-info p{margin:0;font-size:.85rem;line-height:1.65}
.setup-table{width:100%;border-collapse:collapse;font-size:.86rem;margin:10px 0}
.setup-table th{background:var(--p);color:#fff;padding:9px 13px;text-align:left}
.setup-table td{padding:9px 13px;border-bottom:1px solid var(--bd);color:var(--mu)}
.setup-table tr:nth-child(even) td{background:#F8FAFE}
.setup-table tr:last-child td{border-bottom:none}
.setup-table td:first-child{font-weight:600;color:var(--tx);width:32%}
.avoid-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.avoid-tag{background:rgba(231,76,60,.08);border:1px solid rgba(231,76,60,.2);border-radius:8px;padding:5px 12px;font-size:.8rem;color:#C0392B;font-weight:600}
.faq details{border-bottom:1px solid var(--bd);padding:12px 0}
.faq details:last-child{border-bottom:none}
.faq summary{font-weight:600;font-size:.92rem;color:var(--tx);cursor:pointer;list-style:none;padding-right:20px;position:relative}
.faq summary::after{content:'﹢';position:absolute;right:0;color:var(--mu)}
.faq details[open] summary::after{content:'﹣'}
.faq details p{margin:8px 0 0;font-size:.88rem;line-height:1.72;color:var(--mu)}
.cluster-nav a{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--bd);font-size:.83rem;color:var(--mu);font-weight:500}
.cluster-nav a:last-child{border-bottom:none}
.cluster-nav a:hover,.cluster-nav a.act{color:var(--p)}
.cluster-nav a.act{font-weight:700}
.cluster-nav .gal{font-size:.72rem;background:rgba(27,94,139,.08);padding:2px 7px;border-radius:20px;color:var(--p);font-weight:700;flex-shrink:0}
.cta-box{background:linear-gradient(135deg,#0F3D5E,#1B5E8B);border-radius:14px;padding:20px;color:#fff}
.cta-box h3{color:#fff;margin-bottom:6px}
.cta-box p{color:rgba(255,255,255,.8);font-size:.85rem;margin-bottom:14px}
.cta-box a{display:inline-flex;align-items:center;gap:6px;padding:8px 18px;background:#fff;color:var(--p);border-radius:8px;font-weight:700;font-size:.84rem}
.guide-links{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:12px}
.guide-links a{background:#fff;border:1px solid var(--bd);border-radius:8px;padding:10px 13px;color:var(--tx);font-weight:700;font-size:.82rem;transition:border-color .15s}
.guide-links a:hover{border-color:var(--p);background:#F0F7FF}
@media(max-width:540px){.guide-links{grid-template-columns:1fr}}
.level-badge{display:inline-block;padding:3px 12px;border-radius:20px;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:10px}
.badge-beginner{background:rgba(39,174,96,.15);color:#1E8449}
.badge-intermediate{background:rgba(243,156,18,.15);color:#B7770D}
.badge-advanced{background:rgba(231,76,60,.15);color:#922B21}
.ft{background:#0F3D5E;padding:28px 22px;margin-top:40px;text-align:center}
.ftb{color:rgba(255,255,255,.4);font-size:.76rem}"""

CLUSTER_SIZES = [5, 10, 20, 29, 40, 55, 75, 100, 125]

def cluster_nav_html(current_size):
    items = []
    for sz in CLUSTER_SIZES:
        t = TANKS[sz]
        is_act = "act" if sz == current_size else ""
        items.append(
            f'<a href="/tanks/{t["slug"]}-fish-tank/" class="{is_act}">'
            f'{sz} Gallon Fish Tank<span class="gal">{sz} gal</span></a>'
        )
    return "\n".join(items)


def make_page(size):
    t = TANKS[size]
    slug = t["slug"]
    kw = t["title_kw"]
    canon = f"https://www.fishcareai.com/tanks/{slug}-fish-tank/"
    title = f"{kw}: Best Fish, Setup, Stocking & Cost Guide | FishCare AI"
    desc  = (f"{kw} guide — best fish to keep, how many fish fit, required equipment, "
             f"setup cost, and stocking tips. Complete 2026 reference.")

    # Fish items
    fish_html = ""
    for name, wiki, desc_fish in t["best_fish"]:
        fish_html += (
            f'<div class="fish-item">'
            f'<span class="fish-badge">Recommended</span>'
            f'<div class="fish-info">'
            f'<h3><a href="{wiki}">{name}</a></h3>'
            f'<p>{desc_fish}</p>'
            f'</div></div>\n'
        )

    # Avoid list
    avoid_html = "".join(f'<span class="avoid-tag">❌ {a}</span>' for a in t["avoid"])

    # FAQs
    faqs_html = "\n".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>"
        for q, a in t["faqs"]
    )
    faq_schema_items = [
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q, a in t["faqs"]
    ]

    breadcrumb_json = json.dumps({
        "@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":"https://www.fishcareai.com/"},
            {"@type":"ListItem","position":2,"name":"Tank Size Guides","item":"https://www.fishcareai.com/tanks/"},
            {"@type":"ListItem","position":3,"name":kw,"item":canon},
        ]
    })
    article_json = json.dumps({
        "@context":"https://schema.org","@type":"Article",
        "headline":title,"description":desc,
        "datePublished":"2026-08-15","dateModified":"2026-08-15",
        "author":{"@type":"Organization","name":"FishCare AI Editorial Team"},
        "publisher":{"@type":"Organization","name":"FishCare AI","url":"https://www.fishcareai.com"}
    })
    faq_schema = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq_schema_items})

    dims = t["dims"]
    badge_cls = f'badge-{t["level"]}'

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
<link rel="canonical" href="{canon}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canon}"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{faq_schema}</script>
<style>{CSS}</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260815-tanks"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/guides/">Guides</a>
    <a class="nl" href="/wiki/">Encyclopedia</a>
    <a class="nl act" href="/tanks/">Tank Sizes</a>
    <a class="nl" href="/tools/tank-size-calculator/">Calculator</a>
  </div>
</nav>

<header class="hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="/">Home</a><span>/</span>
      <a href="/tanks/">Tank Size Guides</a><span>/</span>
      <span>{kw}</span>
    </div>
    <div class="tag">🪣 Tank Size Guide</div>
    <span class="level-badge {badge_cls}">{t['level'].title()}</span>
    <h1>{kw}: Best Fish, Setup &amp; Stocking Guide</h1>
    <p class="sub">{t['level_note']} — complete 2026 reference for fish selection, stocking, equipment, and cost.</p>
    <div class="dim-chips">
      <div class="dim-chip">{size} US Gallons<span>≈ {round(size*3.785)} litres</span></div>
      <div class="dim-chip">{dims['l']}″ × {dims['w']}″ × {dims['h']}″<span>L × W × H (standard)</span></div>
      <div class="dim-chip">{dims['notes']}<span>Footprint note</span></div>
      <div class="dim-chip">~{round((size*8.34 + size*0.7 + 20))} lbs full<span>Approx. filled weight</span></div>
    </div>
  </div>
</header>

<div class="layout">
  <main>
    <div class="card">
      <h2>Best Fish for a {kw}</h2>
      <p>These species are well-suited to a {size}-gallon aquarium in terms of adult size, bioload, and behaviour.</p>
      {fish_html}
    </div>

    <div class="card">
      <h2>Fish to Avoid in a {kw}</h2>
      <p>These species require more space, produce too much waste, or have specific needs that a {size}-gallon cannot meet long-term.</p>
      <div class="avoid-list">{avoid_html}</div>
    </div>

    <div class="card">
      <h2>Stocking &amp; Water Change Guidelines</h2>
      <p><strong>Stocking:</strong> {t['stocking_rule']}</p>
      <p><strong>Water changes:</strong> {t['water_changes']}</p>
      <p><strong>Cycle time:</strong> {t['cycle_time']}</p>
    </div>

    <div class="card">
      <h2>Equipment for a {kw}</h2>
      <table class="setup-table">
        <tr><th>Equipment</th><th>Recommendation</th></tr>
        <tr><td>Filter</td><td>{t['filter']}</td></tr>
        <tr><td>Heater</td><td>{t['heater']}</td></tr>
        <tr><td>Lighting</td><td>{t['lighting']}</td></tr>
        <tr><td>Estimated Setup Cost</td><td>{t['cost_est']}</td></tr>
      </table>
    </div>

    <div class="card faq">
      <h2>Frequently Asked Questions</h2>
      {faqs_html}
    </div>

    <div class="card">
      <h2>Related Guides &amp; Tools</h2>
      <div class="guide-links">
        <a href="/tools/tank-size-calculator/">📐 Volume Calculator</a>
        <a href="/tools/fish-compatibility-checker/">✅ Compatibility Checker</a>
        <a href="/compatibility/">🐠 Fish Compatibility Guides</a>
        <a href="/wiki/">📖 Species Encyclopedia</a>
        <a href="/guides/">📋 Fish Care Guides</a>
        <a href="/tools/water-parameter-checker/">💧 Water Parameter Checker</a>
      </div>
    </div>
  </main>

  <aside class="sidebar">
    <div class="card cta-box" style="padding:18px 20px;margin-bottom:16px">
      <h3>📐 Volume Calculator</h3>
      <p>Enter your tank dimensions to get exact gallons and litres.</p>
      <a href="/tools/tank-size-calculator/">Open Calculator →</a>
    </div>
    <div class="card" style="padding:18px 20px;margin-bottom:16px">
      <h2 style="font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--pd);border:none;padding:0;margin-bottom:10px">Tank Size Guides</h2>
      <div class="cluster-nav">
        {cluster_nav_html(size)}
      </div>
    </div>
    <div class="card" style="padding:18px 20px">
      <h3 style="margin-bottom:8px">Quick Facts</h3>
      <table style="width:100%;font-size:.82rem;border-collapse:collapse">
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Volume</td><td style="text-align:right;font-weight:700;border-bottom:1px solid var(--bd)">{size} US gal</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Litres</td><td style="text-align:right;font-weight:700;border-bottom:1px solid var(--bd)">≈ {round(size*3.785)} L</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Length</td><td style="text-align:right;font-weight:700;border-bottom:1px solid var(--bd)">{dims['l']}″</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Width</td><td style="text-align:right;font-weight:700;border-bottom:1px solid var(--bd)">{dims['w']}″</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu);border-bottom:1px solid var(--bd)">Height</td><td style="text-align:right;font-weight:700;border-bottom:1px solid var(--bd)">{dims['h']}″</td></tr>
        <tr><td style="padding:5px 0;color:var(--mu)">Level</td><td style="text-align:right;font-weight:700;text-transform:capitalize">{t['level']}</td></tr>
      </table>
    </div>
  </aside>
</div>

<footer class="ft">
  <div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div>
  <nav class="legal-links"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


def make_index():
    """Generate /tanks/index.html — the cluster hub."""
    cards_html = ""
    for sz in CLUSTER_SIZES:
        t = TANKS[sz]
        badge_cls = f'badge-{t["level"]}'
        fish_preview = ", ".join(f[0].split("(")[0].strip() for f in t["best_fish"][:3])
        cards_html += (
            f'<a href="/tanks/{t["slug"]}-fish-tank/" '
            f'style="display:block;background:#fff;border:1px solid var(--bd);border-radius:14px;'
            f'padding:20px 22px;transition:border-color .15s,box-shadow .15s;color:var(--tx)">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
            f'<h2 style="border:none;padding:0;margin:0;font-size:1.1rem">{sz} Gallon Tank</h2>'
            f'<span class="level-badge {badge_cls}" style="margin:0">{t["level"].title()}</span>'
            f'</div>'
            f'<p style="font-size:.85rem;margin:0 0 10px">{t["level_note"]}</p>'
            f'<p style="font-size:.78rem;color:var(--mu);margin:0">Best fish: {fish_preview}…</p>'
            f'<div style="display:flex;gap:10px;margin-top:12px;flex-wrap:wrap">'
            f'<span style="font-size:.75rem;background:rgba(27,94,139,.08);padding:3px 10px;border-radius:20px;color:var(--p);font-weight:600">{t["dims"]["l"]}×{t["dims"]["w"]}×{t["dims"]["h"]} in</span>'
            f'<span style="font-size:.75rem;background:rgba(27,94,139,.08);padding:3px 10px;border-radius:20px;color:var(--p);font-weight:600">≈ {round(sz*3.785)} L</span>'
            f'</div></a>\n'
        )

    return f"""<!DOCTYPE html>
<html lang="en" data-adsense-content="true">
<head>
<meta charset="utf-8"/>
<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Fish Tank Size Guide 2026: 5, 10, 20, 55, 75 Gallon Tanks | FishCare AI</title>
<meta name="description" content="Complete fish tank size guides for 5, 10, 20, 29, 40, 55, 75, 100 and 125 gallon aquariums — best fish, stocking numbers, equipment, setup cost, and water change schedule."/>
<meta name="robots" content="index,follow"/>
<link rel="canonical" href="https://www.fishcareai.com/tanks/"/>
<style>{CSS}
.hero{{background:linear-gradient(135deg,#051C2A,#0F3D5E,#1B5E8B);padding:60px 22px;color:#fff;text-align:center}}
.hero h1{{color:#fff;margin-bottom:12px}}
.hero p{{color:rgba(255,255,255,.75);max-width:560px;margin:0 auto 20px;font-size:1rem}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:1100px;margin:40px auto 60px;padding:0 22px}}
@media(max-width:800px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:500px){{.grid{{grid-template-columns:1fr}}}}
.grid a:hover{{border-color:var(--p)!important;box-shadow:0 8px 24px rgba(27,94,139,.12)}}
.tool-cta{{background:#fff;border:1px solid var(--bd);border-radius:16px;padding:28px;text-align:center;max-width:600px;margin:0 auto 40px}}
.tool-cta h2{{color:var(--pd);border:none;padding:0;margin-bottom:8px}}
.tool-cta p{{margin-bottom:16px}}
.tool-cta a{{display:inline-flex;align-items:center;gap:6px;padding:11px 24px;background:var(--p);color:#fff;border-radius:10px;font-weight:700;font-size:.94rem}}
</style>
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260815-tanks"/>
<meta name="google-adsense-account" content="ca-pub-6697313643773879">
<script defer src="/assets/site-compliance.js?v=20260812-fish-health"></script>
</head>
<body>
<nav class="nb">
  <a class="brand" href="/"><img class="fishcare-logo-img" src="/assets/fishcare-logo.svg" alt="FishCare AI" width="142" height="36"/></a>
  <div class="nlinks">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/guides/">Guides</a>
    <a class="nl" href="/wiki/">Encyclopedia</a>
    <a class="nl act" href="/tanks/">Tank Sizes</a>
    <a class="nl" href="/tools/tank-size-calculator/">Calculator</a>
  </div>
</nav>

<header class="hero">
  <div class="tag">🪣 Tank Size Guides</div>
  <h1>Fish Tank Size Guide 2026</h1>
  <p>Comprehensive guides for every standard aquarium size — best fish, stocking numbers, required equipment, setup cost, and water change schedule.</p>
</header>

<div class="con" style="padding-top:32px">
  <div class="tool-cta">
    <h2>📐 Tank Volume Calculator</h2>
    <p>Know your tank's exact dimensions? Get precise gallons and litres in seconds.</p>
    <a href="/tools/tank-size-calculator/">Open Volume Calculator →</a>
  </div>
</div>

<div class="grid">
{cards_html}
</div>

<footer class="ft">
  <div class="ftb">© 2026 FishCare AI. Practical freshwater fish care guides and tools.</div>
  <nav class="legal-links"><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a></nav>
</footer>
</body>
</html>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Generate individual tank pages
    for size in CLUSTER_SIZES:
        t = TANKS[size]
        page_dir = OUT / f"{t['slug']}-fish-tank"
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(make_page(size), encoding="utf-8")
        print(f"  ✓ /tanks/{t['slug']}-fish-tank/")

    # Generate hub index
    (OUT / "index.html").write_text(make_index(), encoding="utf-8")
    print(f"  ✓ /tanks/ (hub)")

    print(f"\nDone — {len(CLUSTER_SIZES)} tank size pages + hub.")


if __name__ == "__main__":
    main()
