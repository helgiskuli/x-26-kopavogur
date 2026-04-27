---
name: kopavogur-updates
description: Use when the user wants to apply, evaluate, or review new research updates for the Kópavogur 2026 election site. Triggers on phrases like "evaluate the updates", "apply the digest", "what needs updating", "new additions in _data/_updates", "process the research results", or any mention of updating the HTML pages from the research pipeline output. This skill governs the full workflow: read the data files, filter what's actionable, check current page coverage, make targeted HTML edits, and mark applied items.
---

# Kópavogur Updates Workflow

Apply new research output from `_data/latest_digest.md` and `_data/tracked_updates.json` into the live HTML pages.

`_data/latest_digest.md` is the **canonical input** — it contains only unapplied items from the latest run. `_updates/YYYY-MM-DD.md` files are the transactional archive; do not read them as part of this workflow.

---

## Step 1 — Read the data

Read both files in parallel:

1. **`_data/latest_digest.md`** — narrative digest of unapplied items. Check the frontmatter `date` field to confirm it's from the current run. If the file is stale (more than 24 hours old), flag this to the user before proceeding.

2. **`_data/tracked_updates.json`** — structured research output. Each entry has:
   - `headline_is` — Icelandic headline
   - `summary_is` — summary of the content
   - `policy_area` — which topic(s) it covers
   - `category` — `frettir`, `stefna`, or `umraeda`
   - `party_letter` — which party (null = multi-party or neutral)
   - `fills_known_gap` — true if the research agent flagged this as filling a documented gap
   - `applied_date` — ISO date if already incorporated into an HTML page; null if not yet applied
   - `source_url`, `source_name`, `date`

   Also read the top-level `gaps` object — a dict of `party_letter → [topic, ...]` listing known documentation holes per party:
   ```json
   "gaps": { "C": ["húsnæði", "velferð"], "M": ["húsnæði", "stjórnsýsla"] }
   ```

---

## Step 2 — Filter: what's actually actionable

Work only with entries where `applied_date` is null. From those, apply this filter:

**Act on:**
- `fills_known_gap: true` — highest priority; these fill documented holes in existing pages
- Any entry where `party_letter` + `policy_area` matches a known gap in the top-level `gaps` object — treat as high priority even if `fills_known_gap` is false
- `category: "stefna"` — party policy positions with a named source
- `category: "umraeda"` items that contain a **substantive policy claim** (a party position, a specific number, a comparative claim, or a rebuttal with policy content)

**Skip:**
- Pure debate drama: interpersonal incidents, tone of debate, who interrupted whom
- Administrative/logistics news: kjörskrá, election dates, office hours
- Polling/survey results — no polling section exists on any current page
- Items where `policy_area` is null and `fills_known_gap` is false — likely general news

**When in doubt:** if the item tells a reader something new and checkable about what a party would *do* in office, it's worth adding. If it tells them something about *campaign atmosphere*, skip it.

---

## Step 3 — Map policy area → HTML page

| policy_area keyword | page |
|---|---|
| skólamál, Kópavogsmódelið, leikskól, grunnskól | `skolar.html` |
| velferð, aðgengi, heimgreiðsl, örorku, aldraðir | `velferd.html` |
| samgöngur, Borgarlína, Fossvogsbrú, ASHB | `samgongur.html` |
| fjármál, fasteignagjöld, ársreikningur, skuldir | `fjarmal.html` |
| stjórnsýsla, gagnsæi, samráð, lýðræði | `stjornsysla.html` |
| húsnæði, uppbygging, skipulag | `husnaedi.html` |
| miðbær, menning, torg, framkvæmdir | `midbaer.html` |

A single update can touch multiple pages — act on all that apply.

---

## Step 4 — Check current coverage before editing

For each actionable item and its target page, grep for the key subject before touching anything:

```bash
grep -n "<party name or key term>" <page>.html | head -20
```

If the substance is already there (even if worded differently), mark the item as applied (Step 7) and move on — do not edit. If it's partially there (e.g. one side of a debate is covered but not the rebuttal), add only the missing piece.

---

## Step 5 — Make targeted edits

Edit only what's missing. Match the surrounding HTML style exactly — same component patterns, same CSS classes, same Icelandic prose register.

**Tagging conventions** (use the correct tag for every claim):
- `<span class="tag tag-news">Frétt/viðtal</span>` — verified news report or interview
- `<span class="tag tag-unverified">Óstaðfest</span>` — a claim that needs cross-checking
- `<span class="tag tag-missing">Vantar heimild</span>` — acknowledged gap, no source found yet
- `<span class="tag tag-dim">...</span>` — neutral label (party name, topic, date)

**Source attribution** — always include publication and date. For news articles and interviews, link the publication name:
```html
<a href="https://visir.is/..." style="color:inherit">Vísir</a>, 26. apríl 2026
```
For opinion pieces or general debate summaries where a single article URL doesn't cleanly apply, cite without a link:
```html
<span style="font-size:11px;color:var(--text-dim);font-family:var(--mono);display:block;margin-top:0.4rem">
  Vísir, 26. apríl 2026
</span>
```
The `source_url` field in `tracked_updates.json` is the URL to use.

**Party stances** — if updating a `stance-card` that currently says "Vantar heimild", remove the missing tag, update the header tag to `tag-news` (or appropriate), replace the placeholder text with the actual position, and keep the card structure intact.

**Comparative/contested claims** (e.g. "lowest property taxes in the capital area") — present them as attributable assertions with `tag-unverified`, and add a brief caveat note explaining what would be needed to verify them. Never present a party's comparative claim as established fact.

**Do not:**
- Change nav, header, or footer (run `sync-nav.py` if nav ever needs changing)
- Add hardcoded party colors — use CSS vars (`var(--d)`, `var(--s)`, etc.)
- Render `confidence` scores from `claims.json` to users
- Translate content into English

---

## Step 6 — Validate

After all edits:

```bash
python3 scripts/validate-page.py --all
```

All pages must pass. The pre-existing warning on `stefnumal.html` (no active nav link) is expected — ignore it.

---

## Step 7 — Mark applied items

For every entry that was acted on (either edited into a page, or confirmed already covered), update `_data/tracked_updates.json` by setting `applied_date` to today's ISO date on that entry. Match entries by `source_url`.

Read the file, update in memory, write back with `json.dumps(..., ensure_ascii=False, indent=2)`. Do not alter any other fields.

If a `fills_known_gap: true` item was successfully applied, also consider whether the corresponding party+topic should be removed from the top-level `gaps` object. Remove it if the page now has substantive coverage for that party/topic combination.

---

## Step 8 — Report

Give a compact summary:

- Which pages were edited and why (one line each)
- Which items were already covered and marked applied (one line each)
- Which updates were skipped and why (one line each)
- Any remaining gaps the data didn't fill (flag for the next research run)
