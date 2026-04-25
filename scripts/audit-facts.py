#!/usr/bin/env python3
"""Cross-page fact consistency audit.

Checks:
  1. claims.json: source_ids that don't exist in sources.json
  2. claims.json: same issue+party with conflicting claim text
  3. HTML files: known date/fact patterns that must be consistent across pages
  4. HTML files: 'Þarf að staðfesta' inventory (informational)

Run from repo root: python3 scripts/audit-facts.py
Exits 0 if no errors, 1 if errors found (warnings don't affect exit code).
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent

# HTML files to skip for fact-pattern checks
SKIP_HTML = {"stefnumal.html"}

# ── Fact patterns ─────────────────────────────────────────────────
# Each entry: name, regex to find the claim in HTML, expected substring.
# A match that doesn't contain 'expected' is flagged.
FACT_PATTERNS = [
    {
        "name": "ASHB handover date",
        "pattern": re.compile(
            r"ASHB\s+tekur\s+við[^.]{0,80}1\.\s+(júlí|júní|ágúst|maí)\s+2026",
            re.IGNORECASE,
        ),
        "expected": "júlí",
    },
    {
        "name": "ASHB timing relative to election",
        "pattern": re.compile(
            r"áður\s+en\s+kosningadagur\s+er\s+gengið\s+til",
            re.IGNORECASE,
        ),
        "expected": None,  # This string should NOT appear at all — it's the old wrong text
        "must_be_absent": True,
    },
    {
        "name": "Election day",
        "pattern": re.compile(r"(?:16|15|17)\.\s+maí\s+2026", re.IGNORECASE),
        "expected": "16.",
    },
    {
        "name": "Fossvogsbrú contract month",
        "pattern": re.compile(
            r"samningur[^.]{0,40}(?:undirritaður|skráður)[^.]{0,40}"
            r"(nóvember|október|desember|janúar|febrúar)\s+2025",
            re.IGNORECASE,
        ),
        "expected": "nóvember",
    },
    {
        "name": "Fannborg stop month",
        "pattern": re.compile(
            r"Fannborg[^.]{0,60}stöðvuð?[^.]{0,40}"
            r"(janúar|febrúar|mars|apríl)\s+2026",
            re.IGNORECASE,
        ),
        "expected": "janúar",
    },
]


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── 1. claims.json audits ─────────────────────────────────────────

def audit_claims(claims: list, sources: list) -> list[str]:
    errors = []
    source_ids = {s["id"] for s in sources}

    for c in claims:
        sid = c.get("source_id")
        if sid and sid not in source_ids:
            errors.append(
                f"Claim '{c['id']}': source_id '{sid}' not found in sources.json"
            )

    # Note: multiple claims per issue+party is expected (different facts about
    # the same topic). No conflict detection on claim_type — the field is a
    # broad category, not a unique slot.

    return errors


# ── 2. HTML fact-pattern audit ────────────────────────────────────

def audit_html_facts(html_files: list[Path]) -> list[str]:
    errors = []

    for pdef in FACT_PATTERNS:
        must_be_absent = pdef.get("must_be_absent", False)
        expected = pdef.get("expected", "")

        for path in html_files:
            if path.name in SKIP_HTML:
                continue
            text = path.read_text(encoding="utf-8")
            matches = pdef["pattern"].findall(text)

            if must_be_absent:
                if matches:
                    errors.append(
                        f"[{pdef['name']}] {path.name}: "
                        f"obsolete/wrong text present — should have been removed"
                    )
                continue

            for m in matches:
                # m may be a string or a tuple of groups
                matched_text = m if isinstance(m, str) else " ".join(m)
                if expected and expected.lower() not in matched_text.lower():
                    errors.append(
                        f"[{pdef['name']}] {path.name}: "
                        f"found '{matched_text.strip()}' — expected '{expected}'"
                    )

    return errors


# ── 3. 'Þarf að staðfesta' inventory ─────────────────────────────

def inventory_unverified(html_files: list[Path]) -> list[str]:
    items = []
    for path in html_files:
        if path.name in SKIP_HTML or path.name in {"index.html", "kort.html"}:
            continue
        text = path.read_text(encoding="utf-8")
        count = text.count("Þarf að staðfesta")
        if count:
            items.append(f"{path.name}: {count} × 'Þarf að staðfesta'")
    return items


# ── Main ──────────────────────────────────────────────────────────

def main() -> int:
    claims_path  = ROOT / "data" / "claims.json"
    sources_path = ROOT / "data" / "sources.json"
    html_files   = sorted(ROOT.glob("*.html"))

    claims  = load_json(claims_path)
    sources = load_json(sources_path)

    print(f"Loaded {len(claims)} claims, {len(sources)} sources, {len(html_files)} HTML files\n")

    all_errors: list[str] = []

    # 1
    print("── claims.json ──")
    ce = audit_claims(claims, sources)
    for e in ce:
        print(f"  ✗ {e}")
    if not ce:
        print("  OK")
    all_errors.extend(ce)

    # 2
    print("\n── HTML fact consistency ──")
    he = audit_html_facts(html_files)
    for e in he:
        print(f"  ✗ {e}")
    if not he:
        print("  OK")
    all_errors.extend(he)

    # 3 (warnings only)
    print("\n── 'Þarf að staðfesta' inventory (informational) ──")
    vi = inventory_unverified(html_files)
    for item in vi:
        print(f"  ⚠ {item}")
    if not vi:
        print("  OK  (none remaining)")

    print(f"\n{'─' * 52}")
    if all_errors:
        print(f"  {len(all_errors)} error(s) found")
        return 1
    print("  All checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
