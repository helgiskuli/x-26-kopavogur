#!/usr/bin/env python3
"""Validate issue pages and shared pages against the AGENTS.md checklist.

Usage:
  python3 scripts/validate-page.py husnaedi.html fjarmal.html
  python3 scripts/validate-page.py --all

Exits 0 if all pages pass, 1 if any errors are found.
Warnings are informational and do not affect the exit code.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Pages that are not 5-part issue pages (skip issue-specific checks).
# fjarmal.html uses its own 4-part financial structure, not the standard template.
NON_ISSUE_PAGES = {"index.html", "fjarmal.html", "kort.html", "stefnumal.html"}

# All nav hrefs that must appear in every page
ALL_NAV_HREFS = [
    "index.html", "husnaedi.html", "velferd.html", "midbaer.html",
    "samgongur.html", "skolar.html", "stjornsysla.html",
    "fjarmal.html", "kort.html",
]

# Party letters that must appear as badges in Section 2 of every issue page
PARTY_LETTERS = ["B", "C", "D", "J", "M", "S", "V"]

# The three mandatory section eyebrows for issue pages
REQUIRED_EYEBROWS = [
    "Af hverju skiptir þetta máli",
    "Hvað segja framboðin",
    "Spurningar til kjósanda",
]

# English-coded strings that should never appear in an HTML file
ENGLISH_ARTIFACTS = [
    "primary-tilvitnun",
    "primary-tilvitnanir",
    "ferlaadministration",
]

# Known Icelandic typos / malformed strings
KNOWN_TYPOS = [
    "núlllínu",
    "uppfærslulyktir",
    "íbúasamráðsferlir",
    "afstaðar flokkanna",
    "hagsmunatekniskum sjónarmiðum",
]


def _err(errors, msg):   errors.append(("ERROR", msg))
def _warn(errors, msg):  errors.append(("WARN",  msg))


def validate(path: Path) -> list[tuple[str, str]]:
    """Return list of (level, message) tuples. Empty = pass."""
    findings = []
    text = path.read_text(encoding="utf-8")
    is_issue = path.name not in NON_ISSUE_PAGES

    # ── Head ───────────────────────────────────────────────────────
    if "<!DOCTYPE html>" not in text:
        _err(findings, "Missing <!DOCTYPE html>")
    if 'lang="is"' not in text:
        _err(findings, 'Missing lang="is" on <html>')
    if 'charset="UTF-8"' not in text and "charset=UTF-8" not in text:
        _err(findings, "Missing charset=UTF-8")
    if 'name="viewport"' not in text:
        _err(findings, "Missing viewport meta")

    if path.name != "kort.html":
        if "fonts.googleapis.com" not in text:
            _err(findings, "Missing Google Fonts link")
        if "assets/common.css" not in text:
            _err(findings, "Missing <link rel=stylesheet href=assets/common.css>")

    # ── Nav completeness ───────────────────────────────────────────
    for href in ALL_NAV_HREFS:
        if f'href="{href}"' not in text:
            _err(findings, f"Nav missing: {href}")

    # Active link for this file
    active_re = re.compile(
        rf'href="{re.escape(path.name)}"[^>]*class="active"'
        rf'|class="active"[^>]*href="{re.escape(path.name)}"'
    )
    if not active_re.search(text):
        _warn(findings, f"No class=\"active\" on the nav link for {path.name}")

    # ── Issue-page structure ───────────────────────────────────────
    if is_issue:
        if 'class="page-question"' not in text:
            _err(findings, "Missing page-question (kjarnaspurning)")

        for eyebrow in REQUIRED_EYEBROWS:
            if eyebrow not in text:
                _err(findings, f"Missing required section eyebrow: '{eyebrow}'")

        if "Mat höfundar" not in text:
            _err(findings, "Missing 'Mat höfundar' section")
        if "Mín greining" not in text:
            _err(findings, "Mat höfundar not labelled 'Mín greining'")
        if "Heimildir" not in text:
            _err(findings, "Missing Heimildir sources block")

        # All 7 party badges in Section 2
        for letter in PARTY_LETTERS:
            if f">{letter}</div>" not in text:
                _warn(findings, f"Party badge possibly missing: {letter}")

    # ── Footer direction links ─────────────────────────────────────
    if path.name not in {"index.html", "kort.html", "stefnumal.html"}:
        if "←" not in text and "&larr;" not in text:
            _warn(findings, "Footer missing ← previous link")
        if "→" not in text and "&rarr;" not in text:
            _warn(findings, "Footer missing → next link")

    # ── English artifacts ─────────────────────────────────────────
    for artifact in ENGLISH_ARTIFACTS:
        if artifact in text:
            _err(findings, f"English artifact present: '{artifact}'")

    # ── Known typos ───────────────────────────────────────────────
    for typo in KNOWN_TYPOS:
        if typo in text:
            _err(findings, f"Known typo present: '{typo}'")

    return findings


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a for a in sys.argv[1:] if a.startswith("-")]

    if "--all" in flags:
        paths = sorted(ROOT.glob("*.html"))
    elif args:
        paths = [ROOT / a for a in args]
    else:
        print(__doc__)
        return 1

    total_errors = 0
    for path in paths:
        findings = validate(path)
        errors   = [m for level, m in findings if level == "ERROR"]
        warnings = [m for level, m in findings if level == "WARN"]
        status   = "FAIL" if errors else ("WARN" if warnings else "OK  ")
        print(f"\n[{status}]  {path.name}")
        for msg in errors:
            print(f"       ✗  {msg}")
        for msg in warnings:
            print(f"       ⚠  {msg}")
        total_errors += len(errors)

    print(f"\n{'─' * 52}")
    if total_errors:
        print(f"  {total_errors} error(s) — fix before merging")
        return 1
    print(f"  All {len(paths)} page(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
