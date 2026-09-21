#!/usr/bin/env python3
"""Render the hand-written "<species> health problems" hubs under /aquarium-fish-diseases/.

These replace the thin stubs that scripts/build-disease-hubs.py emits from a GSC coverage
export (that script now skips the slugs listed in HANDBUILT). Layout mirrors
/aquarium-fish-diseases/clownfish/ so the three hubs look like one family.

    python3 scripts/build-health-problem-hubs.py            # writes both hubs
    python3 scripts/build-health-problem-hubs.py discus     # one hub
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.fishcareai.com"
FH = SITE + "/fish-health/"

# The 30 symptom pages the species app publishes for every species, grouped the way
# /fish-health/fish/<species> groups them.
BEHAVIOUR = [
    ("not-eating", "Not Eating", "Refusing food for more than a day or two"),
    ("hiding", "Hiding", "Staying behind plants or in a corner all day"),
    ("lethargic", "Lethargic", "Hovering motionless, slow to react"),
    ("darting", "Darting", "Sudden bursts of frantic swimming"),
    ("rubbing", "Rubbing / Flashing", "Scraping the body on décor or substrate"),
    ("jumping", "Jumping", "Leaping at the surface or out of the tank"),
    ("aggressive", "Aggressive", "Chasing, nipping or pinning tank mates"),
    ("swimming-sideways", "Swimming Sideways", "Tilted or listing while swimming"),
    ("floating", "Floating", "Stuck at the surface, unable to dive"),
    ("sinking", "Sinking", "Resting on the bottom, unable to rise"),
    ("gasping", "Gasping", "Mouthing at the surface for air"),
    ("rapid-breathing", "Rapid Breathing", "Gill covers pumping fast at rest"),
    ("coughing", "Coughing", "Repeated jerky gill flushing"),
]
PHYSICAL = [
    ("white-spots", "White Spots", "Salt-grain dots on body or fins (ich)"),
    ("black-spots", "Black Spots", "Dark speckles or patches on the skin"),
    ("spots-on-fins", "Spots on Fins", "Marks confined to the fins"),
    ("pale-color", "Pale Color", "Washed-out body colour"),
    ("losing-color", "Losing Color", "Colour fading over days or weeks"),
    ("fuzzy-growth", "Fuzzy Growth", "Cotton-like tufts on skin or mouth"),
    ("mucus-coating", "Mucus Coating", "Cloudy or grey slime film over the body"),
    ("red-streaks", "Red Streaks", "Blood lines in fins or on the body"),
    ("missing-scales", "Missing Scales", "Bare patches where scales have lifted off"),
    ("bloated", "Bloated", "Swollen belly, sometimes with raised scales"),
    ("sunken-belly", "Sunken Belly", "Pinched, concave abdomen"),
    ("curled-body", "Curled Body", "Spine bent into a C or S shape"),
]
FINS_EYES = [
    ("fin-rot", "Fin Rot", "Ragged, milky or receding fin edges"),
    ("torn-fins", "Torn Fins", "Splits or bite marks in the fins"),
    ("clamped-fins", "Clamped Fins", "Fins held tight against the body"),
    ("cloudy-eyes", "Cloudy Eyes", "Milky film over one or both eyes"),
    ("bulging-eyes", "Bulging Eyes", "One or both eyes protruding (pop-eye)"),
]

HUBS: dict[str, dict] = {
    "discus": {
        "dir": "discus-diseases",
        "name": "Discus",
        "keyword": "discus health problems",
        "title": "Discus Health Problems: Symptoms, Diseases & Treatment",
        "description": "Discus health problems explained: hole-in-the-head, gill flukes, wasting, dark colour, ich and bloat. Match 30 symptom guides to causes and treatment.",
        "subtitle": "Match what you see on your discus to the likely cause, then use the 30 symptom guides and the disease guide to treat it.",
        "image": {"src": "/assets/discus/orange-patterned-discus-fish.jpg", "w": 800, "h": 734,
                  "alt": "Orange and white discus with clear eyes and full fins — the baseline to compare discus health problems against",
                  "caption": "A healthy discus is round, holds its fins open, shows bright colour and comes forward at feeding time. Any change from that baseline is the first sign of discus health problems."},
        "intro": [
            "Discus (<em>Symphysodon</em>) are the fish that most often end up on a symptom search. They come from warm, soft, very clean Amazon water, and almost every one of the common discus health problems traces back to a tank that drifted away from those conditions: nitrate creeping up between water changes, temperature slipping below 82°F, or a new fish bringing in gill flukes or intestinal parasites.",
            "This hub is the index for discus health problems on FishCare AI. Use the symptom finder to jump to the guide that matches what you see, read the short profiles of the diseases discus actually get, and run the pre-treatment checklist before you buy medication. For the long-form disease article see the <a href=\"/guides/discus-fish-care/diseases/\">discus fish diseases guide</a>; for the symptom-checker version see <a href=\"/fish-health/fish/discus\">discus health problems on the symptom checker</a>.",
        ],
        "urgent": "<strong>Treat as urgent:</strong> a discus that is dark, clamped and gasping at the surface, or one that has stopped eating for more than three days. Discus lose condition fast, and hole-in-the-head lesions and wasting are far easier to reverse early.",
        "diseases": [
            ("Hole-in-the-head (Hexamita)", "hexamita",
             "The signature discus disease. Small pits appear above the eyes and along the lateral line, the fish turns dark, produces white stringy faeces and stops eating. <em>Hexamita</em> flagellates are usually present at low levels; they bloom when nitrate is high or the fish is stressed. Treatment is metronidazole in a hospital tank (or medicated food if the fish still eats) plus large, frequent water changes.",
             ["not-eating", "sunken-belly", "losing-color"]),
            ("Gill flukes (Dactylogyrus)", "flukes",
             "Discus with gill flukes breathe fast, keep one gill cover shut, cough, and rub their heads on décor. Young fish and new imports are the usual carriers. Praziquantel is the standard treatment; repeat after a week because eggs survive the first dose.",
             ["rapid-breathing", "coughing", "rubbing", "gasping"]),
            ("Internal parasites and wasting", "wasting",
             "A discus that eats but loses weight, or one with a pinched belly, clear or white faeces and a knife-edge back, usually has tapeworms, <em>Capillaria</em> or <em>Hexamita</em> in the gut. Levamisole or praziquantel (worms) and metronidazole (flagellates) are chosen by the type of parasite, so look at the faeces before you medicate.",
             ["sunken-belly", "not-eating", "lethargic"]),
            ("Dark colour and stress", "dark",
             "Discus go black or very dark when water quality drops, when they are bullied, or in the first days after a move. On its own this is a warning, not a disease: test ammonia, nitrite and nitrate, check the pecking order, and give the fish cover. If the dark fish also clamps its fins and hides, look for the parasitic or bacterial causes above.",
             ["losing-color", "pale-color", "hiding", "clamped-fins"]),
            ("Bacterial infections: fin rot, ulcers, columnaris", "bacterial",
             "Ragged fins with a white edge, red streaks in the fins, open sores, or a white saddle across the back point to <em>Aeromonas</em>, <em>Pseudomonas</em> or <em>Flavobacterium</em>. These take hold on damaged or stressed fish; fix the water first, then use a broad-spectrum antibiotic in a hospital tank for anything beyond mild fin rot.",
             ["fin-rot", "red-streaks", "missing-scales", "fuzzy-growth"]),
            ("Ich (white spot) and velvet", "ich",
             "Discus are kept warm enough that ich cycles fast: salt-grain spots one day, flashing and clamped fins the next. Raise the temperature to 86°F, add aeration, and treat the whole tank with a malachite-green/formalin product or, if the tank has no invertebrates, copper. Velvet looks like gold dust and needs the same approach with the lights off.",
             ["white-spots", "spots-on-fins", "rubbing", "mucus-coating"]),
            ("Bloat, dropsy and swim-bladder trouble", "bloat",
             "A swollen belly on a discus is usually constipation from too much beef heart, or an internal bacterial infection once the scales start to stand out (dropsy). Floating, sinking or tilting comes from the swim bladder being squeezed by the same swelling. Fast the fish, feed blanched pea or daphnia, and move to Epsom salt plus antibiotics if scales lift.",
             ["bloated", "floating", "sinking", "swimming-sideways"]),
            ("Cloudy or bulging eyes", "eyes",
             "Cloudy eyes on discus follow a water-quality dip or a scrape; pop-eye behind both eyes usually means a systemic bacterial infection. Water changes fix the first; the second needs antibiotics.",
             ["cloudy-eyes", "bulging-eyes"]),
        ],
        "causes_h2": "Why Discus Get Sick: The Conditions Behind Most Discus Health Problems",
        "causes": [
            ("Temperature below 82°F", "Discus immune systems slow down in cool water. Keep 82–86°F (28–30°C) and use a heater with headroom; a 30°F drop from a failed heater over a winter night is a classic trigger for ich and Hexamita."),
            ("Nitrate above 20 ppm", "Discus are the least nitrate-tolerant common aquarium fish. Breeders change 25–50% daily; a display tank needs at least two 30% changes a week. Rising nitrate is the most common root of hole-in-the-head."),
            ("Hard, alkaline water", "Wild and most farmed discus do best at pH 6.0–7.0 and GH under 8°. Hard water is survivable but adds constant osmotic stress, which shows up as dark colour and slime coat problems."),
            ("Beef-heart-only diet", "Beef heart grows discus fast but is low in fibre and high in fat. Fed alone it causes constipation, bloat and fatty liver. Rotate with frozen bloodworm, brine shrimp, quality pellet and a vegetable-based mix; see the <a href=\"/guides/discus-fish-care/food/\">discus food guide</a>."),
            ("Crowding and pecking order", "Discus are a shoaling cichlid with a strict hierarchy. Fewer than five fish, or a tank under 55 gallons, lets one fish bully the rest into hiding and starving. Check the <a href=\"/guides/discus-fish-care/tank-size/\">discus tank size guide</a> and <a href=\"/calculators/discus-fish-tank-size/\">calculator</a>."),
            ("Unquarantined new fish", "Gill flukes, tapeworms and discus plague almost always arrive on a new fish. Quarantine every discus for four weeks and deworm during that time."),
        ],
        "checklist": [
            ("Test water:", "Ammonia 0 ppm, nitrite 0 ppm, nitrate under 20 ppm, pH 6.0–7.0, temperature 82–86°F. Compare to the <a href=\"/guides/discus-fish-care/requirements/\">discus water requirements</a>."),
            ("Look at the faeces:", "White, clear or stringy faeces point to internal parasites (metronidazole or a wormer); normal dark faeces rule most of them out."),
            ("Watch the gills:", "One gill cover held shut, or breathing over 100 beats a minute at rest, points to flukes or low oxygen rather than a bacterial problem."),
            ("Count who is sick:", "One fish hiding and dark is usually bullying or an internal parasite; every fish gasping is water or oxygen; spots spreading fish to fish is ich or velvet."),
            ("Set up a hospital tank:", "A bare 20-gallon tank at 86°F with an air stone and a seeded sponge filter lets you dose metronidazole, praziquantel or antibiotics without wrecking the display tank's filter."),
            ("Do not stack medications:", "Metronidazole, praziquantel, copper and antibiotics each stress the liver; treat the parasite you have identified, then reassess after five days."),
        ],
        "resources": [
            ("/fish-health/fish/discus", "Discus Health Problems: Symptom Checker", "Interactive version of this hub with every symptom guide."),
            ("/guides/discus-fish-care/diseases/", "Discus Fish Diseases Guide", "Long-form article on hole-in-the-head, flukes, wasting and ich."),
            ("/guides/discus-fish-care/requirements/", "Discus Water Requirements", "Temperature, pH, hardness and water-change schedule."),
            ("/guides/discus-fish-care/food/", "What to Feed Discus", "Diet rotation that prevents bloat and wasting."),
            ("/guides/discus-fish-care/tank-mates/", "Discus Tank Mates", "Which fish share warm, soft water without bringing disease."),
            ("/guides/discus-fish-care/beginners/", "Discus Care for Beginners", "The routine that keeps discus healthy from day one."),
            ("/compatibility/discus/", "Discus Compatibility", "Ranked pairings for a community discus tank."),
            ("/calculators/discus-fish-tank-size/", "Discus Tank Size Calculator", "How many discus a tank can hold."),
        ],
        "faq": [
            ("What are the most common discus health problems?",
             "Hole-in-the-head (Hexamita), gill flukes, internal parasites that cause wasting, and stress darkening are the four that account for most discus health problems in home tanks. Ich, bacterial fin rot and bloat from a beef-heart diet make up most of the rest. Almost all of them are triggered by nitrate creeping up or temperature dropping below 82°F."),
            ("Why is my discus turning black or dark?",
             "Dark colour is a stress signal. Test ammonia, nitrite and nitrate first, then check whether one fish is being bullied. A newly moved discus can stay dark for a week. If the fish is also clamped, hiding or refusing food, it is usually the start of Hexamita or an internal parasite and needs a closer look."),
            ("Why is my discus not eating?",
             "New discus often refuse food for several days; that is normal. An established discus that stops eating almost always has an internal parasite (Hexamita, tapeworm, Capillaria), gill flukes, or is being bullied off the food. Look at the faeces and the gills, and read the <a href=\"" + FH + "discus-not-eating\">discus not eating guide</a>."),
            ("How do I treat hole-in-the-head in discus?",
             "Metronidazole is the treatment: 250 mg per 10 gallons in a hospital tank every other day for three doses with a water change before each, or mixed into food if the fish still eats. At the same time drop nitrate below 10 ppm with daily water changes and raise the temperature to 86°F. Early pits heal in two to three weeks; deep lesions leave scars."),
            ("What temperature prevents discus diseases?",
             "82–86°F (28–30°C). Below 80°F discus immune function drops and Hexamita, ich and bacterial infections take hold. 86°F is also the treatment temperature for ich and metronidazole. Use two heaters on a discus tank so one failure does not chill the fish."),
            ("Can I treat sick discus in the main tank?",
             "Water-quality problems, stress darkening and mild ich can be handled in the display tank with water changes and heat. Metronidazole, praziquantel and antibiotics belong in a hospital tank: they are wasted in a large volume and damage the biological filter. Move the sick fish, not the medication."),
            ("How often should I change water on a discus tank?",
             "At least twice a week, 30% each time, on a display tank; daily on a grow-out tank. Discus health problems track nitrate more closely than any other number, so if nitrate is above 20 ppm before the next change, the schedule is not enough."),
            ("Is the discus plague real?",
             "Yes. \"Discus plague\" is a fast-spreading infection, thought to be viral with secondary bacteria, that makes every fish in the tank dark, slimy and clamped within days of a new addition. There is no direct treatment: keep water perfect, raise the temperature, treat the secondary infections and, above all, quarantine new fish for four weeks so it never arrives."),
        ],
    },
    "angelfish": {
        "dir": "angelfish-diseases",
        "name": "Angelfish",
        "keyword": "angelfish health problems",
        "title": "Angelfish Health Problems: Symptoms, Diseases & Treatment",
        "description": "Angelfish health problems explained: ich, fin rot, hexamita, internal parasites, swim bladder and bloat. Match 30 symptom guides to causes and treatment.",
        "subtitle": "Match what you see on your freshwater angelfish (Pterophyllum) to the likely cause, then use the 30 symptom guides to treat it.",
        "image": {"src": "/assets/angelfish/silver-angelfish-long-fins.png", "w": 1536, "h": 1024,
                  "alt": "Silver angelfish with intact trailing fins and clear eyes — the baseline to compare angelfish health problems against",
                  "caption": "A healthy angelfish holds its dorsal and anal fins fully extended, shows crisp stripes and clear eyes. Clamped fins, faded bars or ragged fin edges are the earliest angelfish health problems to catch."},
        "intro": [
            "Freshwater angelfish (<em>Pterophyllum scalare</em>) are hardier than discus but they are still Amazon cichlids, and most angelfish health problems come from the same three sources: water that has drifted cold, hard or high in nitrate; long fins that get torn and then infected; and parasites carried in by new fish. Tank-bred angelfish also inherit a few problems of their own, from Hexamita to the so-called angelfish virus.",
            "This hub is the index for angelfish health problems on FishCare AI. Use the symptom finder to jump to the guide that matches what you see, read the profiles of the diseases angelfish actually get, and run the checklist before you medicate. The <a href=\"/guides/angelfish-care/\">angelfish care guide</a> covers the routine that prevents most of them, and <a href=\"/fish-health/fish/angelfish\">angelfish health problems on the symptom checker</a> is the interactive version of this page. Marine angelfish (emperor, flame, French, Koran, bicolor) have their own hubs listed at the bottom.",
        ],
        "urgent": "<strong>Treat as urgent:</strong> an angelfish lying on its side, gasping at the surface with clamped fins, or with scales standing out from the body (dropsy). These progress within a day or two and need a hospital tank immediately.",
        "diseases": [
            ("Ich (white spot)", "ich",
             "The most common angelfish disease. Salt-grain spots on the fins first, then the body; the fish flashes against décor and clamps its fins. It usually follows a temperature drop or a new fish. Raise the temperature to 84–86°F, add aeration, and treat the whole tank for at least ten days so the free-swimming stage is killed.",
             ["white-spots", "spots-on-fins", "rubbing", "clamped-fins"]),
            ("Fin rot and torn fins", "fins",
             "Angelfish fins are long and easily damaged by nipping tank mates, sharp décor or a net. Once torn, <em>Aeromonas</em> or <em>Flavobacterium</em> turn the edge milky, then ragged and red. Clean water alone heals torn fins; fin rot with a white or red edge needs an antibacterial in a hospital tank.",
             ["fin-rot", "torn-fins", "red-streaks"]),
            ("Hexamita and hole-in-the-head", "hexamita",
             "Like discus, angelfish carry <em>Hexamita</em> at low levels and break down with it under stress: white stringy faeces, refusing food, a dark body and, later, pits on the head. Metronidazole in food or a hospital tank, with nitrate pulled below 20 ppm, resolves early cases.",
             ["not-eating", "sunken-belly", "losing-color", "hiding"]),
            ("Internal parasites (Capillaria, tapeworm)", "worms",
             "An angelfish that eats but stays thin, or passes clear or white faeces, usually has nematodes or tapeworms. Wild-caught and farm-raised fish both carry them. Levamisole (nematodes) or praziquantel (tapeworms) chosen after looking at the faeces; repeat in two weeks.",
             ["sunken-belly", "lethargic", "pale-color"]),
            ("Swim bladder and bloat", "bloat",
             "Floating head-up, sinking to the bottom or tilting sideways in angelfish is most often the swim bladder squeezed by a swollen gut: overfeeding dry food, constipation, or an internal infection. Fast for two days and feed a blanched pea or daphnia. If the belly swells and scales lift (dropsy), it is systemic and needs antibiotics plus Epsom salt.",
             ["floating", "sinking", "swimming-sideways", "bloated"]),
            ("Velvet (Oodinium) and gill flukes", "gills",
             "Rapid breathing, coughing and a fine gold-to-grey dust on the body point to velvet; rapid breathing with rubbing and no dust points to gill flukes. Velvet is treated like ich with the lights off; flukes need praziquantel.",
             ["rapid-breathing", "coughing", "gasping", "mucus-coating"]),
            ("Bacterial ulcers, pop-eye and cloudy eyes", "bacterial",
             "Missing scales with a red or white crater, one or both eyes bulging, or a milky eye all point to bacteria taking hold on a stressed fish. Cloudy eyes after a water-quality dip clear with water changes; ulcers and pop-eye need a hospital tank and a broad-spectrum antibiotic.",
             ["missing-scales", "bulging-eyes", "cloudy-eyes", "fuzzy-growth"]),
            ("Angelfish virus and aggression injuries", "virus",
             "\"Angelfish virus\" or angelfish plague is a fast-moving infection that arrives with new fish: every angelfish goes dark, slimy and clamped and hangs at the surface. There is no direct cure, only support and quarantine. Separately, angelfish pair up and defend territory, so many torn fins, black spots and missing scales are simply fight damage.",
             ["aggressive", "darting", "black-spots", "torn-fins"]),
        ],
        "causes_h2": "Why Angelfish Get Sick: The Conditions Behind Most Angelfish Health Problems",
        "causes": [
            ("Temperature swings", "Angelfish want a steady 76–82°F (24–28°C). Ich outbreaks almost always follow a drop of a few degrees from a failed heater, a cold water change or a winter room. See <a href=\"/guides/angelfish-temperature/\">angelfish temperature</a>."),
            ("Nitrate and stale water", "Angelfish tolerate nitrate up to about 40 ppm but Hexamita blooms and fins start to fray long before that. A weekly 25–30% change on a lightly stocked tank keeps nitrate under 20 ppm."),
            ("Tank too small or too short", "An adult angelfish is 6 inches tall with fins; a tank under 18 inches high or under 29 gallons for a pair means constant fin damage and fighting. Use the <a href=\"/calculators/angelfish-tank-size/\">angelfish tank size calculator</a>."),
            ("Fin-nipping tank mates", "Tiger barbs, serpae tetras and some danios shred angelfish fins, and every tear is a route for fin rot. The <a href=\"/guides/angelfish-tank-mates/\">angelfish tank mates guide</a> and <a href=\"/compatibility/angelfish/\">compatibility ranking</a> list the safe ones."),
            ("Pairs and aggression", "Two angelfish that pair off will bully the rest of the group, and a lone bullied fish stops eating and hides. Keep six or more, or a single pair; see <a href=\"/guides/are-angelfish-aggressive/\">are angelfish aggressive</a>."),
            ("Diet", "Flake-only diets lead to constipation and thin fish. Rotate quality pellet with frozen bloodworm, brine shrimp and daphnia; the <a href=\"/guides/what-do-angelfish-eat/\">angelfish diet guide</a> has a schedule."),
        ],
        "checklist": [
            ("Test water:", "Ammonia 0 ppm, nitrite 0 ppm, nitrate under 20 ppm, pH 6.5–7.5, temperature 76–82°F. Angelfish usually show cloudy eyes or clamped fins within a day of an ammonia spike."),
            ("Check the fins:", "Tears with clean edges are injury and heal on their own; milky or red edges are fin rot; white dots on the fins are ich."),
            ("Look at the faeces:", "White, clear or stringy faeces mean internal parasites and change the treatment completely."),
            ("Watch the group:", "One fish bullied into a corner is a social problem, not a disease; every fish gasping is oxygen or water; spots spreading fish to fish is ich or velvet."),
            ("Set up a hospital tank:", "A bare 10–20 gallon tank at 82°F with an air stone and a seeded sponge filter is where antibiotics, metronidazole and wormers go, never the display tank."),
            ("One treatment at a time:", "Identify the problem from the symptom guide, treat it, and reassess after five days before adding a second medication."),
        ],
        "resources": [
            ("/fish-health/fish/angelfish", "Angelfish Health Problems: Symptom Checker", "Interactive version of this hub with every symptom guide."),
            ("/guides/angelfish-care/", "Angelfish Care Guide", "Tank size, water parameters, diet and the routine that prevents disease."),
            ("/guides/angelfish-temperature/", "Angelfish Temperature", "The range that keeps ich and Hexamita away."),
            ("/guides/angelfish-tank-mates/", "Angelfish Tank Mates", "Which fish will not shred angelfish fins."),
            ("/guides/are-angelfish-aggressive/", "Are Angelfish Aggressive?", "Pairing, territory and how to stop bullying."),
            ("/guides/what-do-angelfish-eat/", "What Do Angelfish Eat", "Diet rotation that prevents bloat and thin fish."),
            ("/compatibility/angelfish/", "Angelfish Compatibility", "Ranked pairings for an angelfish community tank."),
            ("/calculators/angelfish-tank-size/", "Angelfish Tank Size Calculator", "How many angelfish a tank can hold."),
        ],
        "marine": [
            ("emperor-angelfish", "Emperor Angelfish"), ("flame-angelfish", "Flame Angelfish"),
            ("french-angelfish", "French Angelfish"), ("koran-angelfish", "Koran Angelfish"),
            ("bicolor-angelfish", "Bicolor Angelfish"),
        ],
        "faq": [
            ("What are the most common angelfish health problems?",
             "Ich, fin rot on torn fins, Hexamita (white stringy faeces, then hole-in-the-head), internal worms that keep a fish thin, and swim-bladder trouble from overfeeding cover most angelfish health problems in home tanks. Nearly all of them follow a temperature drop, rising nitrate, fin damage from tank mates, or a new fish that was not quarantined."),
            ("Why is my angelfish lying on its side or floating?",
             "A swollen gut pressing on the swim bladder is the usual cause: too much dry food, constipation, or an internal infection. Fast the fish for two days, then feed a blanched pea or daphnia. If the belly is swollen and the scales stand out, it is dropsy and needs antibiotics in a hospital tank. See the <a href=\"" + FH + "angelfish-swimming-sideways\">angelfish swimming sideways guide</a>."),
            ("Why are my angelfish's fins ragged or clamped?",
             "Ragged fins with clean tears are injury from tank mates or décor and regrow in clean water. A milky or red edge that keeps receding is fin rot and needs an antibacterial. Clamped fins on their own are stress, usually from a water-quality problem or the first stage of ich."),
            ("What does hole-in-the-head look like on an angelfish?",
             "Small pits above the eyes and along the lateral line, often with a dark body, refusal to eat and white stringy faeces. It is caused by Hexamita and made worse by nitrate. Treat with metronidazole and daily water changes; early pits heal within a few weeks."),
            ("What temperature prevents angelfish diseases?",
             "A steady 76–82°F (24–28°C). Angelfish tolerate the range, but a sudden drop of a few degrees is the most common trigger for ich. 84–86°F is the treatment temperature for ich and velvet; keep it there for the full course, not just until spots vanish."),
            ("Can I treat angelfish in the main tank?",
             "Ich, velvet and water-quality problems are treated in the display tank, because the parasite is in the whole tank. Antibiotics, metronidazole and wormers go in a hospital tank so they do not harm the filter or the other fish. Move the sick fish, not the medication."),
            ("Why is my angelfish turning black or losing its stripes?",
             "Angelfish change contrast with mood: bars fade when the fish is relaxed or asleep and darken when it is stressed or dominant. A fish that stays very dark, clamps its fins and hides is stressed by water quality, bullying or the start of Hexamita. Faded, washed-out colour with fast breathing points to velvet or poor water."),
            ("Is the angelfish virus real and can it be cured?",
             "Yes. Angelfish virus (angelfish plague) is a fast-spreading infection, thought to be viral, that turns every angelfish in a tank dark, slimy and listless within days of a new fish arriving. There is no cure; keep water perfect, raise the temperature slightly, treat secondary bacterial infections, and quarantine all new angelfish for four weeks so it never gets in."),
        ],
    },
}

CSS = (ROOT / "aquarium-fish-diseases" / "clownfish" / "index.html").read_text(encoding="utf-8")
CSS = CSS[CSS.index("<style>"): CSS.index("</style>") + len("</style>")]
EXTRA_CSS = """
<style>
figure.hero-photo { margin: 24px 0 0; }
figure.hero-photo img { width: 100%; max-width: 720px; height: auto; border-radius: 10px; border: 1px solid #1A3A5C; display: block; margin: 0 auto; }
figure.hero-photo figcaption { font-size: 0.9em; color: #7AAABE !important; margin-top: 10px; text-align: center; }
.disease-block { background: rgba(13,39,65,.5) !important; border: 1px solid #1A3A5C !important; border-radius: 8px; padding: 18px 20px; margin: 16px 0; }
.disease-block h3 { margin-top: 0; }
.symptom-card h3 { margin: 0 0 8px; color: #7ecaf5 !important; font-size: 1em; font-weight: 600; }
.disease-block .guide-links { margin-top: 10px; font-size: 0.92em; }
.disease-block .guide-links a { color: #7ecaf5 !important; text-decoration: none; margin-right: 12px; white-space: nowrap; font-weight: 500; }
section p a, .cause-list a, .faq-item a { color: #7ecaf5 !important; }
.disease-block .guide-links a:hover { text-decoration: underline; }
.cause-list { padding-left: 20px; color: #D8EAF5 !important; }
.cause-list li { margin: 10px 0; }
.cause-list li strong { color: #7ecaf5 !important; }
</style>"""


def symptom_table(species: str, name: str, rows: list[tuple[str, str, str]]) -> str:
    body = "".join(
        f'<tr><td><strong>{html.escape(label)}</strong></td><td>{html.escape(meaning)}</td>'
        f'<td><a href="{FH}{species}-{slug}">{html.escape(name)} {html.escape(label.lower())} →</a></td></tr>'
        for slug, label, meaning in rows
    )
    return (
        '<div class="table-wrapper"><table><thead><tr><th>Symptom</th><th>What it usually means</th><th>Guide</th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


def render(species: str) -> str:
    h = HUBS[species]
    name = h["name"]
    kw = h["keyword"]
    url = f'{SITE}/aquarium-fish-diseases/{h["dir"]}/'
    labels = {slug: label for slug, label, _ in BEHAVIOUR + PHYSICAL + FINS_EYES}
    all_pages = [(slug, label) for slug, label, _ in BEHAVIOUR + PHYSICAL + FINS_EYES]

    disease_blocks = "".join(
        f'<div class="disease-block" id="{anchor}"><h3>{title} in {name}</h3><p>{text}</p>'
        '<p class="guide-links"><strong>Symptom guides:</strong> '
        + " ".join(f'<a href="{FH}{species}-{s}">{html.escape(name)} {html.escape(labels[s].lower())} →</a>' for s in slugs)
        + "</p></div>"
        for title, anchor, text, slugs in h["diseases"]
    )
    causes = "".join(f"<li><strong>{html.escape(t)}</strong> — {body}</li>" for t, body in h["causes"])
    checklist = "".join(f"<li><strong>{html.escape(t)}</strong> {body}</li>" for t, body in h["checklist"])
    resources = "".join(
        f'<a href="{href}" class="symptom-card"><h3>{html.escape(title)}</h3><p>{html.escape(desc)}</p></a>'
        for href, title, desc in h["resources"]
    )
    marine = ""
    if h.get("marine"):
        cards = "".join(
            f'<a href="{SITE}/fish-health/fish/{slug}" class="symptom-card"><h3>{html.escape(n)} health problems</h4><p>Marine species — separate symptom guides</p></a>'
            for slug, n in h["marine"]
        )
        marine = f'<h3>Marine angelfish health problems (separate species)</h3><p>Saltwater angelfish are unrelated to <em>Pterophyllum</em> and have their own symptom hubs:</p><div class="symptom-grid">{cards}</div>'
    faq_html = "".join(
        f'<div class="faq-item"><strong>Q: {html.escape(q)}</strong><p>A: {a}</p></div>' for q, a in h["faq"]
    )
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in h["faq"]
        ],
    }
    item_list = {
        "@context": "https://schema.org", "@type": "ItemList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f"{name} {label}", "url": f"{FH}{species}-{slug}"}
            for i, (slug, label) in enumerate(all_pages)
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Aquarium Fish Diseases", "item": SITE + "/aquarium-fish-diseases/"},
            {"@type": "ListItem", "position": 3, "name": f"{name} Health Problems", "item": url},
        ],
    }
    collection = {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": h["title"], "url": url,
        "description": h["description"],
        "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + h["image"]["src"], "width": h["image"]["w"], "height": h["image"]["h"]},
        "publisher": {"@type": "Organization", "name": "FishCare AI", "url": SITE},
        "dateModified": "2026-09-21",
    }
    schemas = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(s, indent=2, ensure_ascii=False) + "\n</script>"
        for s in (breadcrumb, collection, item_list, faq_schema)
    )
    img = h["image"]
    intro = "".join(f"<p>{p}</p>" for p in h["intro"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{html.escape(h["title"])}</title>
<meta name="description" content="{html.escape(h["description"])}">
<link rel="canonical" href="{url}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/assets/fishcare-glass-redesign.css?v=20260908-artc-contrast">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(h["title"])}">
<meta property="og:description" content="{html.escape(h["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{img["src"]}">
<meta property="og:site_name" content="FishCare AI">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(h["title"])}">
<meta name="twitter:description" content="{html.escape(h["description"])}">
<meta name="twitter:image" content="{SITE}{img["src"]}">
{CSS}{EXTRA_CSS}
</head>
<body>

<nav aria-label="Skip to main content" style="position: absolute; top: -40px;">
  <a href="#main" style="background: #2A9CD8; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px;">Skip to main content</a>
</nav>

<div class="hero">
  <div class="con">
    <div class="breadcrumb">
      <a href="{SITE}">Home</a>
      <span>/</span>
      <a href="{SITE}/aquarium-fish-diseases/">Aquarium Fish Diseases</a>
      <span>/</span>
      <span>{name} Health Problems</span>
    </div>
    <h1>{html.escape(h["title"])}</h1>
    <p>{html.escape(h["subtitle"])}</p>
  </div>
</div>

<main id="main">
  <div class="con">

    <a href="{SITE}/aquarium-fish-diseases/" class="back-link">← Back to All Fish Diseases</a>

    <section>
      {intro}
      <div class="urgency-note">{h["urgent"]}</div>
      <figure class="hero-photo">
        <img src="{img["src"]}" alt="{html.escape(img["alt"])}" width="{img["w"]}" height="{img["h"]}" loading="eager" decoding="async">
        <figcaption>{html.escape(img["caption"])}</figcaption>
      </figure>
    </section>

    <section id="symptoms">
      <h2>{name} Health Problems by Symptom: Quick Finder</h2>
      <p>Every symptom below links to a dedicated {name.lower()} guide with causes, a diagnosis walk-through and treatment steps. Start with the sign that appeared first.</p>
      <h3>{name} behaviour and breathing symptoms</h3>
      {symptom_table(species, name, BEHAVIOUR)}
      <h3>{name} body, skin and colour symptoms</h3>
      {symptom_table(species, name, PHYSICAL)}
      <h3>{name} fin and eye symptoms</h3>
      {symptom_table(species, name, FINS_EYES)}
    </section>

    <section id="diseases">
      <h2>Most Common {name} Health Problems and Diseases</h2>
      <p>These are the conditions behind the symptoms above, in roughly the order a {name.lower()} keeper is likely to meet them.</p>
      {disease_blocks}
    </section>

    <section id="causes">
      <h2>{html.escape(h["causes_h2"])}</h2>
      <p>Very few {name.lower()} health problems start as a disease. They start as a husbandry gap that a parasite or bacterium then exploits. Close these and most of the list above never appears.</p>
      <ol class="cause-list">{causes}</ol>
    </section>

    <section id="checklist">
      <h2>Before You Treat {name} Health Problems: Checklist</h2>
      <div class="note"><strong>Rule out water quality first.</strong> Ammonia, nitrite, nitrate and temperature explain the majority of {name.lower()} symptoms. Medicating a fish whose real problem is the water wastes money and adds stress.</div>
      <ol style="color: #D8EAF5 !important;">{checklist}</ol>
    </section>

    <section id="resources">
      <h2>More {name} Health and Care Resources</h2>
      <div class="symptom-grid">{resources}</div>
      {marine}
    </section>

    <section id="faq">
      <h2>{name} Health Problems: Frequently Asked Questions</h2>
      {faq_html}
    </section>

    <section>
      <h2 id="sources-heading">Sources and Editorial Method</h2>
      <div class="sources">
        <p><strong>This guide draws on:</strong></p>
        <ul>
          <li><a href="https://www.merckvetmanual.com/exotic-and-laboratory-animals/aquarium-fish/management-of-aquarium-fish" target="_blank" rel="noopener">Merck Veterinary Manual – Management of Aquarium Fish</a></li>
          <li><a href="https://www.merckvetmanual.com/exotic-and-laboratory-animals/aquarium-fish/parasitic-diseases-of-fish" target="_blank" rel="noopener">Merck Veterinary Manual – Parasitic Diseases of Fish</a></li>
          <li><a href="https://www.merckvetmanual.com/exotic-and-laboratory-animals/aquarium-fish/bacterial-diseases-of-fish" target="_blank" rel="noopener">Merck Veterinary Manual – Bacterial Diseases of Fish</a></li>
          <li><a href="https://edis.ifas.ufl.edu/publication/FA004" target="_blank" rel="noopener">UF/IFAS Extension – Introduction to Freshwater Fish Parasites</a></li>
          <li><a href="https://www.woah.org/en/what-we-do/animal-health-and-welfare/aquatic-animals/" target="_blank" rel="noopener">World Organisation for Animal Health – Aquatic Animals</a></li>
          <li>The 30 {name.lower()} symptom guides on FishCare AI, which cite the sources above per condition</li>
        </ul>
        <p><strong>Last reviewed:</strong> September 2026 | <strong>Reviewed for:</strong> species-specific accuracy, symptom terminology, water-quality guidance and treatment ranges.</p>
        <p><strong>Not a substitute for professional diagnosis.</strong> This guide is educational. Consult an aquatic veterinarian for persistent or severe symptoms.</p>
      </div>
    </section>

    <section style="text-align: center; padding: 30px 0;">
      <p style="margin: 20px 0;">
        <a href="{SITE}/aquarium-fish-diseases/" style="display: inline-block; background: #2A9CD8 !important; color: white !important; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 1em;">← Back to All Fish Diseases Hub</a>
      </p>
      <p style="font-size: 0.9em; color: #7AAABE !important;">Browse guides for 200+ other fish species and 30 symptom categories</p>
    </section>

  </div>
</main>

{schemas}

<script src="/assets/site-compliance.js?v=20260824-dark-fix"></script>

</body>
</html>
"""


def strip_tags(s: str) -> str:
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s))


def main() -> None:
    targets = sys.argv[1:] or list(HUBS)
    for species in targets:
        out = ROOT / "aquarium-fish-diseases" / HUBS[species]["dir"] / "index.html"
        out.write_text(render(species), encoding="utf-8")
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
