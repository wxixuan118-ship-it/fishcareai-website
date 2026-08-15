"""
11_fish_health_ai_enrich.py
────────────────────────────
AI-enriches blank fish_health_content rows using ZhipuAI (glm-4-flash).
Fetches species context (water params, diet, behavior) to produce
species-specific content for every fish × problem pair.
Applies a quality gate before setting published=True.

Usage:
  python 11_fish_health_ai_enrich.py [--limit N] [--slug SLUG]

Options:
  --limit N    Process at most N rows (default: all)
  --slug SLUG  Process only the row with this slug (e.g. betta-not-eating)
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Optional
from zhipuai import ZhipuAI
from supabase import create_client

# ── Load .env file from this directory ───────────────────────────────────────
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

# ── Config ────────────────────────────────────────────────────────────────────
SUPABASE_URL  = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY  = os.environ.get("SUPABASE_SERVICE_KEY", "")
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY or "paste-your" in SUPABASE_KEY:
    sys.exit(
        "ERROR: Open data-pipeline/.env and fill in SUPABASE_SERVICE_KEY.\n"
        "Find it at: Supabase Dashboard → Project Settings → API → service_role"
    )
if not ZHIPU_API_KEY or "paste-your" in ZHIPU_API_KEY:
    sys.exit(
        "ERROR: Open data-pipeline/.env and fill in ZHIPU_API_KEY.\n"
        "Get a free key at: https://open.bigmodel.cn/"
    )

zhipu_client = ZhipuAI(api_key=ZHIPU_API_KEY)
client = create_client(SUPABASE_URL, SUPABASE_KEY)

MODEL = "glm-4-flash"
DELAY = 0.6

# ── Quality gate thresholds ───────────────────────────────────────────────────
MIN_INTRO_LEN  = 150
MIN_CAUSES     = 3
MIN_DIAG_STEPS = 3
MIN_TREAT_STEPS = 3
MIN_FAQ        = 3

# ── Prompt ────────────────────────────────────────────────────────────────────
SYSTEM = (
    "You are a professional aquarium veterinarian and fish care writer. "
    "Generate accurate, species-specific fish health diagnosis content. "
    "Respond with valid JSON only — no markdown fences, no explanation."
)

def build_prompt(fish: dict, prob: dict) -> str:
    env = fish.get("environment") or {}
    beh = fish.get("behavior") or {}
    return f"""Write a detailed diagnosis guide for this fish health problem.
The content MUST be specific to this species — not generic.

FISH:
  Common name: {fish.get('common_name', 'Unknown')}
  Scientific name: {fish.get('scientific_name', '')}
  Water type: {fish.get('water_type', 'freshwater')}
  Temperature: {env.get('temp_min_c', 24)}–{env.get('temp_max_c', 28)}°C
  pH: {env.get('ph_min', 6.5)}–{env.get('ph_max', 7.5)}
  Behavior: {beh.get('temperament', 'peaceful')}
  Care level: {fish.get('difficulty_level', 'beginner')}

PROBLEM:
  Name: {prob.get('problem_name', '')}
  Category: {prob.get('category', '')}
  Description: {prob.get('description', '')}
  Urgency: {prob.get('urgency', 'monitor')}

Return ONLY this JSON (no extra keys):
{{
  "intro": "3–4 sentences specific to {fish.get('common_name','this fish')} covering why this problem happens, how serious it is, and what the owner should know first — minimum 200 characters",
  "common_causes": [
    {{"title": "string", "detail": "1–2 sentences", "likelihood": "high"}}
  ],
  "diagnosis_steps": [
    {{"step": 1, "action": "string", "detail": "string", "tool": "optional tool name or null"}}
  ],
  "treatment_steps": [
    {{"step": 1, "action": "string", "detail": "string"}}
  ],
  "prevention": "2–3 sentences specific to {fish.get('common_name','this fish')}",
  "when_to_seek_help": "1–2 sentences about when to consult a vet",
  "faq": [
    {{"q": "Question a {fish.get('common_name','fish')} owner would ask", "a": "Practical answer"}}
  ],
  "meta_title": "Why Is My {fish.get('common_name','Fish')} {prob.get('problem_name','')}? Causes & Solutions",
  "meta_description": "150–160 char SEO description mentioning {fish.get('common_name','')} and {prob.get('problem_name','').lower()}"
}}

Rules:
- intro: MUST be at least 200 characters. Write 3–4 complete sentences — this is NOT optional.
- common_causes: 3–5 items, likelihood = high | medium | low, ordered high→low
- diagnosis_steps: 3–5 numbered steps, step field is integer
- treatment_steps: 3–5 numbered steps, step field is integer
- faq: 3–5 question-answer pairs
- References to {fish.get('common_name','')} must reflect its actual water/diet/behavior traits
- tool field in diagnosis_steps: string or null, never omit the key"""


def parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def quality_check(content: dict) -> tuple[bool, list[str]]:
    issues = []
    if not content.get("intro") or len(content["intro"]) < MIN_INTRO_LEN:
        issues.append(f"intro too short (<{MIN_INTRO_LEN} chars, got {len(content.get('intro',''))})")
    if len(content.get("common_causes", [])) < MIN_CAUSES:
        issues.append(f"only {len(content.get('common_causes',[]))} causes (need {MIN_CAUSES})")
    if len(content.get("diagnosis_steps", [])) < MIN_DIAG_STEPS:
        issues.append(f"only {len(content.get('diagnosis_steps',[]))} diagnosis steps (need {MIN_DIAG_STEPS})")
    if len(content.get("treatment_steps", [])) < MIN_TREAT_STEPS:
        issues.append(f"only {len(content.get('treatment_steps',[]))} treatment steps (need {MIN_TREAT_STEPS})")
    if len(content.get("faq", [])) < MIN_FAQ:
        issues.append(f"only {len(content.get('faq',[]))} FAQ items (need {MIN_FAQ})")
    return len(issues) == 0, issues


def fetch_pending_rows(limit: Optional[int], slug: Optional[str]) -> list[dict]:
    q = (
        client.table("fish_health_content")
        .select("""
            id, slug,
            species:fish_id (
              common_name, scientific_name, water_type,
              difficulty_level, environment, behavior
            ),
            health_problems:problem_id (
              problem_name, category, description, urgency
            )
        """)
        .eq("published", False)
    )
    if slug:
        q = q.eq("slug", slug)
    if limit:
        q = q.limit(limit)
    res = q.execute()
    return res.data or []


def call_zhipu(fish: dict, prob: dict, attempts: int = 3) -> Optional[dict]:
    for attempt in range(1, attempts + 1):
        try:
            response = zhipu_client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user",   "content": build_prompt(fish, prob)},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            return parse_json(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(f"    PARSE ERROR (attempt {attempt}): {e}")
            if attempt < attempts:
                time.sleep(2)
        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "429" in str(e):
                wait = 30 * attempt
                print(f"    RATE LIMIT (attempt {attempt}): waiting {wait}s")
                time.sleep(wait)
                continue
            print(f"    API ERROR (attempt {attempt}): {e}")
            if attempt < attempts:
                time.sleep(3)
    return None


def enrich_row(row: dict) -> bool:
    fish = row.get("species") or {}
    prob = row.get("health_problems") or {}

    content = call_zhipu(fish, prob)
    if content is None:
        return False

    passed, issues = quality_check(content)
    if not passed:
        print(f"    QUALITY FAIL — {'; '.join(issues)}")
        return False

    for step in content.get("diagnosis_steps", []):
        step.setdefault("tool", None)

    update = {
        "intro":             content.get("intro"),
        "common_causes":     content.get("common_causes", []),
        "diagnosis_steps":   content.get("diagnosis_steps", []),
        "treatment_steps":   content.get("treatment_steps", []),
        "prevention":        content.get("prevention"),
        "when_to_seek_help": content.get("when_to_seek_help"),
        "faq":               content.get("faq", []),
        "meta_title":        content.get("meta_title"),
        "meta_description":  content.get("meta_description"),
        "published":         True,
    }

    try:
        client.table("fish_health_content").update(update).eq("id", row["id"]).execute()
    except Exception as e:
        print(f"    DB WRITE ERROR: {e}")
        return False

    return True


BATCH_SIZE = 1000  # Supabase max rows per request


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Max rows to process in total")
    parser.add_argument("--slug",  type=str, default=None, help="Process only this slug")
    args = parser.parse_args()

    total_ok = total_fail = total_processed = 0
    batch_num = 0

    while True:
        remaining = None
        if args.limit is not None:
            remaining = args.limit - total_processed
            if remaining <= 0:
                break

        fetch_limit = min(BATCH_SIZE, remaining) if remaining is not None else BATCH_SIZE
        rows = fetch_pending_rows(fetch_limit, args.slug)

        if not rows:
            break

        batch_num += 1
        print(f"\n── Batch {batch_num} ({len(rows)} rows) ──")

        ok = fail = 0
        for i, row in enumerate(rows, 1):
            slug = row.get("slug", "?")
            fish_name = (row.get("species") or {}).get("common_name", "?")
            prob_name = (row.get("health_problems") or {}).get("problem_name", "?")
            print(f"[{total_processed + i}/{(args.limit or '?')}] {slug} ({fish_name} — {prob_name})")
            success = enrich_row(row)
            if success:
                print(f"    published ✓")
                ok += 1
            else:
                fail += 1
            if i < len(rows):
                time.sleep(DELAY)

        total_ok   += ok
        total_fail += fail
        total_processed += len(rows)
        print(f"Batch {batch_num} done. Published: {ok}  Failed: {fail}")

        if args.slug:
            break

    print(f"\n═══ All done. Total published: {total_ok}  Failed: {total_fail} ═══")


if __name__ == "__main__":
    main()
