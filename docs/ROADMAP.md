# Roadmap

Future work items for the site. Ordered roughly by priority.

## After election day (May 16, 2026)

- [ ] Add election results page with final vote counts
- [ ] Disable research-heartbeat workflow (no longer needed)
- [ ] Archive the site as a static snapshot

## Next up

### ~~Automated update promoter~~ — implemented as a skill (2026-04-27)

Built as `/kopavogur-updates` (`.claude/skills/kopavogur-updates/SKILL.md`)
rather than a separate agent script. Invoked manually in a Claude Code session
after merging a research PR.

**What was built:**
- `applied_date` field on all `tracked_updates.json` entries (null = unapplied)
- `_data/latest_digest.md` contains only unapplied items with frontmatter — canonical skill input
- `_data/pr_body.md` contains only new items from the current run — used as PR body
- Skill handles filtering, page routing, HTML editing, validation, and marking items applied
- Gaps object in `tracked_updates.json` is pruned by the skill when a gap is genuinely filled

**What was skipped vs. original plan:**
- No automatic trigger on PR merge — skill is invoked manually (intentional: keeps a human in the loop)
- No separate `promoter_agent.py` script — the Claude Code skill replaces it

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