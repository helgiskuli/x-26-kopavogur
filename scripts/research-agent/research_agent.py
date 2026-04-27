"""
Kópavogur Political Research Agent
===================================
Runs on a GitHub Actions heartbeat. Uses Gemini 3 Flash Preview with
Google Search grounding to find new political news about Kópavogur
municipal elections (May 16, 2026).

Free tier: Gemini 2.5 Flash (GA, 15 RPM / 1500 RPD)
At 1 run/day × 2 queries/run × 20 days = ~40 queries. Well within limits.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).parent.parent.parent


def load_dotenv(path: Path = _REPO_ROOT / ".env") -> None:
    """Load KEY=VALUE pairs from a .env file into os.environ (no-op if missing)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

MODEL = "gemini-2.5-flash"

# Parties and their known web presences — the agent checks these specifically
PARTIES = {
    "B": {"name": "Framsóknarflokkurinn", "url": "https://framsokn.is/sveitarfelog/kopavogur", "oddviti": "Orri Vignir Hlöðversson"},
    "C": {"name": "Viðreisn", "url": "https://vidreisn.is/kopavogur", "oddviti": "María Ellen Steingrímsdóttir"},
    "D": {"name": "Sjálfstæðisflokkurinn", "url": "https://xdkop.is", "oddviti": "Ásdís Kristjánsdóttir"},
    "J": {"name": "Sósíalistaflokkur Íslands", "url": "https://sosialistaflokkurinn.is", "oddviti": "Markús Candi"},
    "M": {"name": "Miðflokkurinn", "url": "https://midflokkurinn.is", "oddviti": "Einar Jóhannes Guðnason"},
    "S": {"name": "Samfylkingin", "url": "https://xs.is/samfylkingin-i-kopavogi1", "oddviti": "Jónas Már Torfason"},
    "V": {"name": "VG og óháð", "url": "https://vg.is/sveitarfelag/kopavogur/", "oddviti": "Anna Sigríður Hafliðadóttir"},
}

# Policy areas tracked on the site — agent looks for updates in these
POLICY_AREAS = [
    "skólamál og Kópavogsmódelið",
    "samgöngur og Borgarlína",
    "húsnæðismál og lóðir",
    "velferð og aðgengi",
    "stjórnsýsla og gagnsæi",
    "fjármál og fasteignagjöld",
    "miðbæjarframkvæmdir",
]

# Initial policy gaps — loaded from _data/tracked_updates.json if available,
# otherwise seeded from this default. Edit _data/tracked_updates.json manually
# to close a gap after confirming it's filled via a merged PR.
DEFAULT_GAPS = {
    "C": ["húsnæði", "velferð", "stjórnsýsla"],
    "M": ["húsnæði", "velferð", "stjórnsýsla", "samgöngur"],
    "V": ["velferð", "stjórnsýsla"],
    "S": ["velferð", "stjórnsýsla"],
}

TRACKED_FILE = _REPO_ROOT / "_data/tracked_updates.json"
DIGEST_FILE = _REPO_ROOT / "_data/latest_digest.md"
PR_BODY_FILE = _REPO_ROOT / "_data/pr_body.md"
UPDATES_DIR = _REPO_ROOT / "_updates"


# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def search_with_gemini(client: genai.Client, query: str, max_retries: int = 3) -> str:
    """Run a grounded search query via Gemini, with exponential backoff on 429s."""
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=query,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    temperature=0.3,
                ),
            )
            return response.text
        except Exception as e:
            is_rate_limit = any(s in str(e) for s in ("429", "RESOURCE_EXHAUSTED", "quota", "503", "UNAVAILABLE"))
            if is_rate_limit and attempt < max_retries - 1:
                wait = 30 * (2 ** attempt)  # 30s, 60s
                print(f"Rate limited. Bíð {wait}s (tilraun {attempt + 2}/{max_retries})...")
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# Research prompts
# ---------------------------------------------------------------------------

def build_news_prompt(gaps: dict) -> str:
    today = datetime.now(timezone.utc).strftime("%d. %B %Y")
    party_list = "\n".join(
        f"- {k}: {v['name']} (oddviti: {v['oddviti']}, vef: {v['url']})"
        for k, v in PARTIES.items()
    )
    areas = "\n".join(f"- {a}" for a in POLICY_AREAS)

    # Build dynamic gaps text from current state
    if gaps:
        gap_lines = []
        for letter, missing in gaps.items():
            if missing:
                name = PARTIES.get(letter, {}).get("name", letter)
                gap_lines.append(f"- {name} ({letter}): vantar stefnu um {', '.join(missing)}")
        gaps_text = "Þekktar eyður — framboð sem hafa EKKI birt stefnu:\n" + "\n".join(gap_lines)
    else:
        gaps_text = "Engar þekktar eyður eftir — öll framboð hafa birt stefnu í öllum málaflokkum."

    return f"""Dagsetning í dag: {today}
Sveitarstjórnarkosningar í Kópavogi eru 16. maí 2026.

Leitaðu að NÝJUSTU fréttum og uppfærslum um sveitarstjórnarkosningarnar í Kópavogi.
Þrengdu leitina að þessum áreiðanlegu fréttamiðlum með site: leitarstirkjum:
site:ruv.is OR site:visir.is OR site:mbl.is OR site:dv.is OR site:heimildin.is

Framboðin:
{party_list}

Málaflokkarnir sem við fylgjumst með:
{areas}

{gaps_text}

Skilaðu niðurstöðum á JSON formi og ENGU ÖÐRU (engin markdown, engar skýringar):
{{
  "updates": [
    {{
      "source_url": "slóð á heimild",
      "source_name": "nafn miðils eða flokks",
      "party_letter": "B/C/D/J/M/S/V eða null",
      "headline_is": "stutt lýsing á íslensku",
      "summary_is": "nánari lýsing á íslensku, 2-4 setningar",
      "policy_area": "málaflokkur ef við á",
      "category": "stefna|frambjodandi|umraeda|frettir|kosningaherferð",
      "fills_known_gap": true/false,
      "date": "ISO dagsetning ef þekkt"
    }}
  ],
  "has_updates": true/false,
  "search_summary": "stutt samantekt á íslensku um hvað fannst"
}}

Ef EKKERT nýtt fannst, skilaðu has_updates: false og tómum updates lista.
Skilgreindu "nýtt" sem eitthvað sem hefur birst á síðustu 48 klukkustundum.
Ekki skila gömlum fréttum eða upplýsingum sem þegar eru þekktar."""


def build_events_prompt() -> str:
    """Search for broadcast and event content: debates, interviews, appearances, press conferences."""
    return """Leitaðu að umræðum, viðtölum, kosningaviðburðum og kynningum tengdum
sveitarstjórnarkosningum í Kópavogi (16. maí 2026).

Þrengdu leitina að þessum lénum með site: leitarstirkjum:
site:ruv.is OR site:visir.is OR site:mbl.is OR site:dv.is OR site:heimildin.is

Einbeittu þér að þessum tegundum efnis — EKKI venjulegum fréttagreinum:
- Kosningaumræður í útvarpi eða sjónvarpi (t.d. RÚV, Bylgjan, Útvarp Saga)
- Viðtöl við oddvita eða frambjóðendur
- Kynningarfundir og opnir fundir (borgarbúafundir)
- Fréttatilkynningar frá framboðum
- Kosningaviðburðir og kynningar

Skilaðu niðurstöðum á sama JSON formi og áður.
Ef EKKERT nýtt, skilaðu has_updates: false.
Skilgreindu "nýtt" sem efni sem virðist hafa birst á síðustu 48 klukkustundum."""


def build_party_check_prompt() -> str:
    """Secondary search specifically checking party homepages for new content."""
    urls = "\n".join(f"- {v['name']}: {v['url']}" for v in PARTIES.values())

    return f"""Athugaðu hvort einhver þessara flokka hafi uppfært heimasíður sínar
með nýrri stefnuskrá, nýjum frambjóðendum eða öðru kosningatengdu efni
fyrir sveitarstjórnarkosningarnar í Kópavogi 16. maí 2026.

Leitaðu beint á heimasíðum flokkanna — notaðu site: leitarstirki þar sem við á:
{urls}

Skilaðu niðurstöðum á sama JSON formi og áður.
Ef EKKERT nýtt, skilaðu has_updates: false.
Skilgreindu "nýtt" sem efni sem virðist hafa birst á síðustu 48 klukkustundum."""


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_tracked() -> dict:
    if TRACKED_FILE.exists():
        try:
            data = json.loads(TRACKED_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise SystemExit(
                f"ERROR: {TRACKED_FILE} contains invalid JSON: {e}\n"
                "Fix the file manually or delete it to reset state."
            ) from e
        # Ensure gaps key exists (migration from older format)
        if "gaps" not in data:
            data["gaps"] = dict(DEFAULT_GAPS)
        return data
    return {"updates": [], "last_run": None, "gaps": dict(DEFAULT_GAPS)}


def save_tracked(data: dict):
    TRACKED_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_run"] = datetime.now(timezone.utc).isoformat()
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    # Round-trip verify before touching the file
    try:
        json.loads(serialized)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"save_tracked produced invalid JSON — not writing file: {e}") from e
    TRACKED_FILE.write_text(serialized, encoding="utf-8")


def is_duplicate(update: dict, existing: list[dict]) -> bool:
    """Check if an update is already tracked (by headline similarity)."""
    # Reject Gemini grounding redirect URLs — they are not real article links
    url = update.get("source_url", "")
    if "vertexaisearch.cloud.google.com" in url:
        return True

    new_headline = update.get("headline_is", "").lower().strip()
    if not new_headline:
        return True  # Skip empty headlines

    for prev in existing:
        prev_headline = prev.get("headline_is", "").lower().strip()
        # Exact match or one is substring of the other
        if new_headline == prev_headline:
            return True
        if len(new_headline) > 20 and len(prev_headline) > 20:
            if new_headline in prev_headline or prev_headline in new_headline:
                return True
    return False


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _format_update_block(u: dict) -> list[str]:
    """Render one update entry as markdown lines (shared by digest and archive)."""
    party = u.get("party_letter", "")
    party_tag = f"**[{party}]** " if party else ""
    gap_tag = " 🆕 _Fylli þekkta eyðu_" if u.get("fills_known_gap") else ""
    lines = [f"#### {party_tag}{u['headline_is']}{gap_tag}\n"]
    lines.append(f"{u.get('summary_is', '')}\n")
    source = u.get("source_url") or u.get("source_name", "")
    if source:
        lines.append(f"_Heimild: {source}_\n")
    lines.append("")
    return lines


def write_digest(new_updates: list[dict], search_summary: str, all_tracked: list[dict]):
    """Write the canonical digest and the transactional archive entry.

    latest_digest.md — canonical input for the update skill. Contains only
    unapplied items (applied_date is None/missing) so the skill never
    re-processes already-incorporated content.

    _updates/YYYY-MM-DD.md — full transactional archive. Contains every item
    found in this run regardless of applied status. Append if the file exists
    (multiple runs per day).
    """
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    # Unapplied items across the full tracked list (not just this run's new items)
    unapplied = [u for u in all_tracked if not u.get("applied_date")]

    DIGEST_FILE.parent.mkdir(parents=True, exist_ok=True)

    # --- latest_digest.md (canonical skill input, unapplied only, with frontmatter) ---
    digest_lines = [
        "---",
        f"date: {now.isoformat()}",
        f"count_total: {len(all_tracked)}",
        f"count_unapplied: {len(unapplied)}",
        "---",
        "",
        f"## Rannsóknarsamantekt {now.strftime('%d.%m.%Y %H:%M')} UTC\n",
        f"{search_summary}\n",
        f"### {len(unapplied)} óúrvinnsluð uppfærsla(r)\n",
    ]
    for u in unapplied:
        digest_lines.extend(_format_update_block(u))
    DIGEST_FILE.write_text("\n".join(digest_lines), encoding="utf-8")

    # --- pr_body.md (PR body only: new items from this run, no frontmatter) ---
    pr_lines = [
        f"## Rannsóknarsamantekt {now.strftime('%d.%m.%Y %H:%M')} UTC\n",
        f"{search_summary}\n",
        f"### {len(new_updates)} nýjar uppfærslur\n",
    ]
    for u in new_updates:
        pr_lines.extend(_format_update_block(u))
    PR_BODY_FILE.write_text("\n".join(pr_lines), encoding="utf-8")

    # --- _updates/YYYY-MM-DD.md (archive, new items from this run only) ---
    UPDATES_DIR.mkdir(parents=True, exist_ok=True)
    update_path = UPDATES_DIR / f"{date_str}.md"

    site_lines = [
        "---",
        f"date: {now.isoformat()}",
        f"count: {len(new_updates)}",
        "---",
        "",
    ]
    for u in new_updates:
        party = u.get("party_letter", "")
        party_tag = f"[{party}] " if party else ""
        site_lines.append(f"## {party_tag}{u['headline_is']}")
        cat = u.get("category", "")
        area = u.get("policy_area", "")
        meta_parts = [x for x in [cat, area] if x]
        if meta_parts:
            site_lines.append(f"*{' · '.join(meta_parts)}*")
        site_lines.append("")
        site_lines.append(u.get("summary_is", ""))
        source = u.get("source_url") or u.get("source_name", "")
        if source:
            site_lines.append(f"\n[Heimild]({source})")
        site_lines.append("")

    mode = "a" if update_path.exists() else "w"
    with open(update_path, mode, encoding="utf-8") as f:
        if mode == "a":
            f.write("\n---\n\n")
        f.write("\n".join(site_lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_response(raw: str) -> dict:
    """Extract JSON from Gemini response, handling fences and preamble text."""
    text = raw.strip()
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"WARNING: Failed to parse JSON: {e}")
        print(f"Raw response:\n{raw[:500]}")
        return {"updates": [], "has_updates": False, "search_summary": "Villa í svari frá Gemini"}


def main():
    client = get_client()
    tracked = load_tracked()

    all_new = []
    search_summary_parts = []

    # Search 1: Party homepages (slow-moving but high-value — run first)
    print("🔍 Athuga heimasíður flokkanna...")
    try:
        raw1 = search_with_gemini(client, build_party_check_prompt())
        result1 = parse_response(raw1)
        search_summary_parts.append(result1.get("search_summary", ""))

        for u in result1.get("updates", []):
            if not is_duplicate(u, tracked["updates"]):
                all_new.append(u)
    except Exception as e:
        print(f"WARNING: Party check failed: {e}")

    time.sleep(15)

    # Search 2: Debates, interviews, events, press conferences
    print("🔍 Leita að umræðum, viðtölum og kosningaviðburðum...")
    try:
        raw2 = search_with_gemini(client, build_events_prompt())
        result2 = parse_response(raw2)
        search_summary_parts.append(result2.get("search_summary", ""))

        for u in result2.get("updates", []):
            if not is_duplicate(u, tracked["updates"]) and not is_duplicate(u, all_new):
                all_new.append(u)
    except Exception as e:
        print(f"WARNING: Events search failed: {e}")

    time.sleep(15)

    # Search 3: Written news articles (most frequent, runs last)
    print("🔍 Leita að fréttum um Kópavogskosningar...")
    try:
        raw3 = search_with_gemini(client, build_news_prompt(tracked.get("gaps", {})))
        result3 = parse_response(raw3)
        search_summary_parts.append(result3.get("search_summary", ""))

        for u in result3.get("updates", []):
            if not is_duplicate(u, tracked["updates"]) and not is_duplicate(u, all_new):
                all_new.append(u)
    except Exception as e:
        print(f"WARNING: News search failed: {e}")

    # Results
    if not all_new:
        print("✅ Ekkert nýtt fannst.")
        save_tracked(tracked)  # Update last_run timestamp
        return

    print(f"📰 Fann {len(all_new)} nýjar uppfærslur!")
    for u in all_new:
        gap = " [FYLLI EYÐU]" if u.get("fills_known_gap") else ""
        print(f"  → {u.get('party_letter', '?')}: {u.get('headline_is', '?')}{gap}")

    for u in all_new:
        u.setdefault("applied_date", None)

    tracked["updates"].extend(all_new)
    save_tracked(tracked)

    summary = " ".join(s for s in search_summary_parts if s)
    write_digest(all_new, summary, tracked["updates"])

    print("✅ Búið að skrifa uppfærslur og PR-texta.")


def dry_run(tracked: dict) -> None:
    print("=" * 60)
    print("PROMPT 1 — Fréttaleit")
    print("=" * 60)
    print(build_news_prompt(tracked.get("gaps", {})))
    print()
    print("=" * 60)
    print("PROMPT 2 — Heimasíður flokkanna")
    print("=" * 60)
    print(build_party_check_prompt())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kópavogur research agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print prompts without calling the API",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        metavar="FILE",
        help="Path to .env file (default: .env in repo root)",
    )
    args = parser.parse_args()

    load_dotenv(Path(args.env_file) if args.env_file else _REPO_ROOT / ".env")

    if args.dry_run:
        dry_run(load_tracked())
    else:
        main()