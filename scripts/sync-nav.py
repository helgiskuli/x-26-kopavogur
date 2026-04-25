#!/usr/bin/env python3
"""Synchronise <nav> blocks across all site HTML files from a single source.

Run from repo root: python3 scripts/sync-nav.py [--dry-run]

This is the authoritative source for nav order. Edit NAV_ENTRIES here,
then run the script — never edit nav links manually in individual files.
"""

import sys
from pathlib import Path

# Canonical nav order — edit here to add/reorder pages
NAV_ENTRIES = [
    ("index.html",       "Stefnumál"),
    ("husnaedi.html",    "Húsnæði"),
    ("velferd.html",     "Velferð"),
    ("midbaer.html",     "Miðbær"),
    ("samgongur.html",   "Samgöngur"),
    ("skolar.html",      "Skólar"),
    ("stjornsysla.html", "Stjórnsýsla"),
    ("fjarmal.html",     "Fjármál"),
    ("kort.html",        "Frambjóðendur"),
]

# Pages skipped entirely (redirect stubs, etc.)
SKIP_FILES = {"stefnumal.html"}


def build_nav(active_file: str, nav_class: str = "", indent: str = "    ") -> str:
    """Return a complete <nav>…</nav> block including its indentation."""
    class_attr = f' class="{nav_class}"' if nav_class else ""
    inner = indent + "  "
    lines = [f"{indent}<nav{class_attr}>"]
    for href, label in NAV_ENTRIES:
        active = ' class="active"' if href == active_file else ""
        lines.append(f'{inner}<a href="{href}"{active}>{label}</a>')
    lines.append(f"{indent}</nav>")
    return "\n".join(lines)


def sync_file(path: Path, dry_run: bool = False) -> str:
    """Return 'fixed', 'ok', or 'skip'."""
    text = path.read_text(encoding="utf-8")

    nav_class = "header-nav" if 'class="header-nav"' in text else ""
    nav_open_tag = f'<nav class="{nav_class}">' if nav_class else "<nav>"
    nav_close_tag = "</nav>"

    start = text.find(nav_open_tag)
    if start == -1:
        print(f"  WARN  {path.name}: no <nav> block found")
        return "skip"

    end = text.find(nav_close_tag, start)
    if end == -1:
        print(f"  WARN  {path.name}: unclosed <nav>")
        return "skip"
    end += len(nav_close_tag)

    # Detect indentation: characters between the preceding newline and <nav>
    line_start = text.rfind("\n", 0, start) + 1
    indent = text[line_start:start]

    # Replace from the start of the nav's line through end of </nav>
    new_nav = build_nav(path.name, nav_class, indent)
    new_text = text[:line_start] + new_nav + text[end:]

    if new_text == text:
        print(f"  OK    {path.name}")
        return "ok"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
        print(f"  FIXED {path.name}")
    else:
        print(f"  DIFF  {path.name}  (dry-run — not written)")
    return "fixed"


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    root = Path(__file__).parent.parent
    html_files = sorted(root.glob("*.html"))

    fixed = 0
    for path in html_files:
        if path.name in SKIP_FILES:
            print(f"  SKIP  {path.name}")
            continue
        result = sync_file(path, dry_run)
        if result == "fixed":
            fixed += 1

    suffix = " (dry-run)" if dry_run else ""
    print(f"\n  {fixed} file(s) updated{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
