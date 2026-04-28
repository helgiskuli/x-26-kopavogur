#!/usr/bin/env python3
"""Verify that source_url entries in _data/tracked_updates.json are reachable.

Usage:
  python3 scripts/verify-urls.py              # check unapplied entries only (default)
  python3 scripts/verify-urls.py --all        # check every entry
  python3 scripts/verify-urls.py --verbose    # show passing URLs too

Exits 0 if no broken links (404) found, 1 otherwise.
403/5xx/timeout are reported as warnings but do not affect the exit code —
some sites (mbl.is) block automated HEAD/GET requests despite being live.
"""

import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
TRACKED_FILE = ROOT / "_data/tracked_updates.json"

_TIMEOUT = 12
_WORKERS = 8
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; link-checker/1.0)"}


def check_url(url: str) -> tuple[str, int | str]:
    """Return (url, status_code) or (url, error_description).

    Tries HEAD first; falls back to GET on 405.
    """
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=_HEADERS, method=method)
            with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
                return url, resp.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code == 405:
                continue
            return url, e.code
        except Exception as e:
            return url, f"ERR: {type(e).__name__}"
    return url, "ERR: no response"


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Verify source URLs in tracked_updates.json")
    parser.add_argument("--all", action="store_true", help="Check all entries, not just unapplied")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show passing URLs too")
    args = parser.parse_args()

    if not TRACKED_FILE.exists():
        print(f"ERROR: {TRACKED_FILE} not found", file=sys.stderr)
        return 1

    data = json.loads(TRACKED_FILE.read_text(encoding="utf-8"))
    updates = data.get("updates", [])

    if not args.all:
        updates = [u for u in updates if not u.get("applied_date")]
        scope = "unapplied"
    else:
        scope = "all"

    # Deduplicate: map url -> list of headlines (many entries share one source)
    url_to_headlines: dict[str, list[str]] = {}
    for u in updates:
        url = u.get("source_url", "").strip()
        if url:
            url_to_headlines.setdefault(url, []).append(u.get("headline_is", "?"))

    if not url_to_headlines:
        print(f"✅ No {scope} entries with URLs to check.")
        return 0

    print(f"Checking {len(url_to_headlines)} unique URL(s) across {len(updates)} {scope} entries...\n")

    ok: list[str] = []
    broken: list[tuple[str, int, list[str]]] = []
    unverified: list[tuple[str, int | str, list[str]]] = []

    with ThreadPoolExecutor(max_workers=_WORKERS) as pool:
        futures = {pool.submit(check_url, url): url for url in url_to_headlines}
        for fut in as_completed(futures):
            url, status = fut.result()
            headlines = url_to_headlines[url]
            domain = urlparse(url).netloc

            if status == 200:
                ok.append(url)
                if args.verbose:
                    print(f"  ✅ 200  {url}")
            elif status == 404:
                broken.append((url, status, headlines))
            else:
                unverified.append((url, status, headlines))

    # --- Summary ---
    if broken:
        print(f"❌ {len(broken)} broken URL(s) — 404 Not Found:\n")
        for url, status, headlines in sorted(broken):
            print(f"  {url}")
            for h in headlines:
                print(f"    → {h}")
        print()

    if unverified:
        print(f"⚠️  {len(unverified)} URL(s) could not be verified (non-404 — may be bot protection):\n")
        for url, status, headlines in sorted(unverified):
            print(f"  [{status}]  {url}")
            for h in headlines:
                print(f"    → {h}")
        print()

    if not broken and not unverified:
        print(f"✅ All {len(ok)} URL(s) returned 200.")
    elif not broken:
        print(f"✅ No broken links. {len(unverified)} URL(s) unverifiable (see above).")
    else:
        print(f"Run complete: {len(ok)} OK, {len(broken)} broken, {len(unverified)} unverifiable.")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
