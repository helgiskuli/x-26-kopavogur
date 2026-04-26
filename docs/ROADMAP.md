# Roadmap

Future work items for the site. Ordered roughly by priority.

## After election day (May 16, 2026)

- [ ] Add election results page with final vote counts
- [ ] Disable research-heartbeat workflow (no longer needed)
- [ ] Archive the site as a static snapshot

## Next up

### Automated update promoter

A second agent (`scripts/promoter/promoter_agent.py`) that takes approved
entries from `tracked_updates.json` and generates page edits automatically,
opening a PR for human review.

**Flow:**
1. Research agent PR merged → promoter triggers (automatic or `workflow_dispatch`)
2. Reads entries where `promoted: false`
3. Routes each entry to the correct page via `policy_area` → page mapping
4. Uses Claude API to generate HTML following the existing design system
5. Opens a PR with proposed page additions — human reviews, tweaks, merges

**Key design decisions:**
- Trigger: automatic on research PR merge vs manual `workflow_dispatch`
- HTML generation: Claude API (understands design system, not template-based)
- Entries without `policy_area` (polls, general news) are skipped and flagged
- Add `promoted: false` flag to `research_agent.py` for all future entries
- Backfill existing 17 entries as `promoted: true` (promoted manually 2026-04-26)

**Why Claude API over Gemini for this step:**
Gemini handles grounded web search; Claude is better at following a complex
design system from examples. The promoter needs to place content in the right
section of a page — that requires understanding stance cards, callouts, and
the 5-part page structure.

## Before election day (if time permits)

### "Hvað er nýtt" page

Add a `/nyjtt.html` page that renders updates from `_updates/*.md` files
in reverse chronological order. This would give the site a "what changed
since I last looked" feed — useful for the two primary readers (us).

Implementation notes:
- The research agent already writes `_updates/YYYY-MM-DD.md` files with
  frontmatter (date, count) and structured content
- Simplest approach: a static HTML page with a JS fetch that reads an
  index file listing available update files, or just hardcode links
- If using Jekyll or another SSG: the `_updates/` files would render
  automatically as a collection
- The page should show date, headline, party tag, and policy area for
  each update, with a link to the relevant site page

### Source reliability indicator

Show which source reported each claim on the site. RÚV > Vísir/MBL > DV
in terms of editorial standards. Could be a small tag next to cited
party positions.

### Comparison tool

Interactive side-by-side comparison of two parties' positions across all
policy areas. Would use the existing data structure on each topic page.