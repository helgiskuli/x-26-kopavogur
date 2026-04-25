#!/usr/bin/env bash
# Merge a Claude Code agent worktree back into the main working tree.
#
# Usage: scripts/merge-worktree.sh <worktree-path>
#
# What it does:
#   1. Copies new HTML files from the worktree (skips files that already exist
#      and are identical; prints a DIFF warning for diverged files).
#   2. Merges data/sources.json and data/claims.json by id-deduplication.
#   3. Runs sync-nav.py to ensure nav is consistent across all pages.
#   4. Runs validate-page.py --all as a post-merge sanity check.

set -euo pipefail

WORKTREE="${1:-}"
if [[ -z "$WORKTREE" ]]; then
    echo "Usage: $0 <worktree-path>" >&2
    exit 1
fi
if [[ ! -d "$WORKTREE" ]]; then
    echo "Error: '$WORKTREE' is not a directory." >&2
    exit 1
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"
WORKTREE="$(cd "$WORKTREE" && pwd)"

echo "Merging: $WORKTREE"
echo "Into:    $REPO"
echo ""

# ── 1. HTML files ─────────────────────────────────────────────────
echo "── HTML files ──"
shopt -s nullglob
for src in "$WORKTREE"/*.html; do
    name="$(basename "$src")"
    dest="$REPO/$name"
    if [[ ! -f "$dest" ]]; then
        cp "$src" "$dest"
        echo "  NEW   $name"
    elif diff -q "$src" "$dest" > /dev/null 2>&1; then
        echo "  SAME  $name"
    else
        echo "  DIFF  $name  ← review manually (not copied)"
    fi
done

# ── 2. JSON data files ────────────────────────────────────────────
echo ""
echo "── JSON data ──"

merge_json() {
    local label="$1" wt_file="$2" main_file="$3"
    if [[ ! -f "$wt_file" ]]; then
        echo "  SKIP  $label (not in worktree)"
        return
    fi
    python3 - "$wt_file" "$main_file" "$label" <<'PYEOF'
import json, sys
wt_path, main_path, label = sys.argv[1], sys.argv[2], sys.argv[3]
wt   = json.loads(open(wt_path,   encoding="utf-8").read())
main = json.loads(open(main_path, encoding="utf-8").read())
main_ids = {s["id"] for s in main}
new = [s for s in wt if s["id"] not in main_ids]
if new:
    main.extend(new)
    open(main_path, "w", encoding="utf-8").write(
        json.dumps(main, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"  MERGED {label} (+{len(new)} entries)")
else:
    print(f"  OK     {label} (no new entries)")
PYEOF
}

merge_json "sources.json" "$WORKTREE/data/sources.json" "$REPO/data/sources.json"
merge_json "claims.json"  "$WORKTREE/data/claims.json"  "$REPO/data/claims.json"

# ── 3. Sync nav ───────────────────────────────────────────────────
echo ""
echo "── Nav sync ──"
cd "$REPO"
python3 scripts/sync-nav.py

# ── 4. Validate all pages ─────────────────────────────────────────
echo ""
echo "── Validation ──"
python3 scripts/validate-page.py --all || {
    echo ""
    echo "  Validation found errors — fix before committing." >&2
    exit 1
}

echo ""
echo "Merge complete. Commit when ready."
