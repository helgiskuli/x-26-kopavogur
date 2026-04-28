"""
Kópavogur Political Research Agent
===================================
Runs on a GitHub Actions heartbeat. Uses Gemini 3 Flash Preview with
Google Search grounding to find new political news about Kópavogur
municipal elections (May 16, 2026).

Free tier: Gemini 2.5 Flash (GA, 15 RPM / 1500 RPD)
At 2 runs/day × 2 queries/run × 20 days = ~80 queries. Well within limits.
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

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
    """Run a grounded search query via Gemini, with exponential backoff on 429/503."""
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
            err = str(e)
            is_503 = any(s in err for s in ("503", "UNAVAILABLE"))
            is_429 = any(s in err for s in ("429", "RESOURCE_EXHAUSTED", "quota"))
            if (is_503 or is_429) and attempt < max_retries - 1:
                # 503 (regional overload) typically outlasts a 429 burst limit —
                # start from 120s instead of 30s so we clear the overload window.
                base = 120 if is_503 else 30
                wait = base * (2 ** attempt) + random.random() * 10
                kind = "503 Unavailable" if is_503 else "429 Rate limit"
                print(f"{kind}. Bíð {wait:.0f}s (tilraun {attempt + 2}/{max_retries})...")
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# Research prompts
# ---------------------------------------------------------------------------


def build_events_and_news_prompt(gaps: dict) -> str:
    """Combined search: written news articles + broadcast/event content.

    Merging these two searches into one call halves the number of grounded
    requests per run, reducing burst pressure on shared CI IPs.
    """
    today = datetime.now(timezone.utc).strftime("%d. %B %Y")
    party_list = "\n".join(
        f"- {k}: {v['name']} (oddviti: {v['oddviti']})"
        for k, v in PARTIES.items()
    )
    areas = "\n".join(f"- {a}" for a in POLICY_AREAS)

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

Leitaðu að NÝJUSTU fréttum, umræðum og viðburðum um sveitarstjórnarkosningarnar í Kópavogi.
Þrengdu leitina að þessum áreiðanlegu fréttamiðlum með site: leitarstirkjum:
site:ruv.is OR site:visir.is OR site:mbl.is OR site:dv.is OR site:heimildin.is

Framboðin:
{party_list}

Málaflokkarnir sem við fylgjumst með:
{areas}

{gaps_text}

Leitaðu að báðum þessum tegundum efnis:
1. Venjulegar fréttagreinar um stefnu, frambjóðendur og kosningamál
2. Umræður, viðtöl og viðburðir:
   - Kosningaumræður í útvarpi eða sjónvarpi (t.d. RÚV, Bylgjan, Útvarp Saga)
   - Viðtöl við oddvita eða frambjóðendur
   - Kynningarfundir og opnir fundir (borgarbúafundir)
   - Fréttatilkynningar frá framboðum

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
# URL verification
# ---------------------------------------------------------------------------

# These domains are first-party or municipal — skip HTTP verification
_TRUSTED_DOMAINS = {"xdkop.is", "kopavogur.is"}


def _check_url(url: str, timeout: int = 10) -> int | None:
    """Return HTTP status code, or None on connection error.

    Tries HEAD first; falls back to GET on 405 (method not allowed).
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; research-bot/1.0)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code == 405:
                continue
            return e.code
        except Exception:
            return None
    return None


def filter_verified_urls(updates: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split updates into (kept, dropped) based on HTTP reachability of source_url.

    - 200 → kept as-is
    - 404 → dropped (hallucinated or dead link)
    - 403 / 5xx / timeout → kept with url_unverified=True (bot-blocked or flaky)
    - Trusted domains (xdkop.is, kopavogur.is) → skip check, always kept

    Deduplicates URLs before checking — many entries may share one source.
    """
    to_check: dict[str, int | None] = {}
    for u in updates:
        url = u.get("source_url", "")
        if not url:
            continue
        domain = urlparse(url).netloc.lstrip("www.")
        if domain not in _TRUSTED_DOMAINS:
            to_check[url] = None

    if to_check:
        print(f"  🔗 Staðfesti {len(to_check)} einstaka slóð(ir)...")
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {pool.submit(_check_url, url): url for url in to_check}
            for fut in as_completed(futures):
                url = futures[fut]
                to_check[url] = fut.result()

    kept: list[dict] = []
    dropped: list[dict] = []
    for u in updates:
        url = u.get("source_url", "")
        if not url or url not in to_check:
            kept.append(u)
            continue
        status = to_check[url]
        if status == 404:
            print(f"  ✂️  404 — sleppt: {u.get('headline_is', url)}")
            dropped.append(u)
        elif status == 200:
            kept.append(u)
        else:
            print(f"  ⚠️  {status} — óstaðfest, heldur: {u.get('headline_is', url)}")
            flagged = dict(u)
            flagged["url_unverified"] = True
            kept.append(flagged)

    return kept, dropped


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

    time.sleep(60)

    # Search 2: News articles + events/debates combined (reduces grounded calls from 3→2)
    print("🔍 Leita að fréttum, umræðum og kosningaviðburðum...")
    try:
        raw2 = search_with_gemini(client, build_events_and_news_prompt(tracked.get("gaps", {})))
        result2 = parse_response(raw2)
        search_summary_parts.append(result2.get("search_summary", ""))

        for u in result2.get("updates", []):
            if not is_duplicate(u, tracked["updates"]) and not is_duplicate(u, all_new):
                all_new.append(u)
    except Exception as e:
        print(f"WARNING: News/events search failed: {e}")

    # Results
    if not all_new:
        print("✅ Ekkert nýtt fannst.")
        save_tracked(tracked)  # Update last_run timestamp
        return

    print(f"📰 Fann {len(all_new)} nýjar uppfærslur — staðfesti slóðir...")
    all_new, dropped_404 = filter_verified_urls(all_new)
    if dropped_404:
        print(f"  Sleppti {len(dropped_404)} uppfærslu(m) með bilaðar slóðir (404).")
    if not all_new:
        print("✅ Ekkert nýtt eftir slóðastaðfestingu.")
        save_tracked(tracked)
        return

    print(f"📰 {len(all_new)} uppfærslu(r) samþykktar:")
    for u in all_new:
        gap = " [FYLLI EYÐU]" if u.get("fills_known_gap") else ""
        unverified = " [ÓSTAÐFEST]" if u.get("url_unverified") else ""
        print(f"  → {u.get('party_letter', '?')}: {u.get('headline_is', '?')}{gap}{unverified}")

    for u in all_new:
        u.setdefault("applied_date", None)

    tracked["updates"].extend(all_new)
    save_tracked(tracked)

    summary = " ".join(s for s in search_summary_parts if s)
    write_digest(all_new, summary, tracked["updates"])

    print("✅ Búið að skrifa uppfærslur og PR-texta.")


def dry_run(tracked: dict) -> None:
    print("=" * 60)
    print("PROMPT 1 — Heimasíður flokkanna")
    print("=" * 60)
    print(build_party_check_prompt())
    print()
    print("=" * 60)
    print("PROMPT 2 — Fréttir, umræður og viðburðir (sameinað)")
    print("=" * 60)
    print(build_events_and_news_prompt(tracked.get("gaps", {})))


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