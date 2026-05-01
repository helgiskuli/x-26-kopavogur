# Roadmap

Future work items for the site. Ordered roughly by priority.

## After election day (May 16, 2026)

- [ ] Add election results page with final vote counts
- [ ] Disable research-heartbeat workflow (no longer needed)
- [ ] Archive the site as a static snapshot

## Next up — TOP PRIORITY

### Visual party comparison page (`yfirlit.html`)

A new condensed overview page replacing walls of text with visual summaries.
Feedback from readers: current issue pages are too verbose.

**Agreed approach (from dataviz-strategist session, 2026-05-01):**

1. **Coverage matrix** (pure HTML table, existing tag classes) — 7 parties × 6 issue areas,
   three states per cell: Staðfest / Hlutvis / Ekki birt. Core utility of the page.
2. **Borgarlína split** (copy `.split-grid` pattern from `samgongur.html`) — clearest binary
   in the election, no new components needed.
3. **Leikskólagjöld position strip** (3-column CSS grid, no JS) — anchored to S's published
   50.000 kr./mánuð cap; categorical placement, not a ranking.
4. **Party grid footer** — already in `common.css`, zero new work.

**Do NOT use:** radar/spider charts (require editorial scoring, illegible with 7 parties),
grouped bar charts for policy positions, stacked coalition bars.

**Before building — editorial work needed first:**
Draft the matrix cell values (Staðfest / Hlutvis / Ekki birt) for each of the 42 cells
by checking `content/*.md` and the current issue page HTML. ~30–45 min of editorial work,
then implementation is straightforward.

**V coverage note:** V has least published material; use `tag-dim` for missing cells,
add a footnote naming the date and explaining that "Ekki birt" reflects documentation
availability, not policy absence. One sentence on the "Fyrir Kópavog" partnership
breakdown (March 31 2026) gives context.

**Nav:** Add `Yfirlit` to the nav via `scripts/sync-nav.py` once the page is ready.

---

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

## Stretch goals (in order)

### 1. `yfirlit.html` — see TOP PRIORITY above

### 2. Pólitískt spurningakeppni (`spurningar.html`)

A voting advice application (VAA): user answers ~10–15 questions on local issues,
system compares answers to encoded party positions, shows best match.

**Depends on:** `yfirlit.html` first — the editorial work of scoring each party per issue
for the coverage matrix produces ~80% of the JSON needed for the quiz scoring.

**Technical approach (all client-side, no server):**
- `data/quiz.json` — questions + party scores per question (e.g. -2 to +2 scale)
- Pure JS similarity calculation (weighted dot product or cosine similarity)
- Results as a ranked bar chart (Chart.js, existing dependency)
- Optional: weight sliders so users can mark which issues matter most to them

**Good question candidates** (sharp differentiators with verifiable source):
- Borgarlína (M: strong no; S/D/B/C/J: yes; V: unclear)
- Leikskólagjöld hámark 50.000 kr. (S: yes; D/B: defend status quo; others: vague)
- Félagslegt húsnæði (S: strong yes; others: general support or no position)
- Skuldir bæjarsjóðs (S/M/C: reduce; D/B: defend current approach)
- Samráð íbúa (C/S/V: strong emphasis; D/B: less prominent)

**Key editorial challenge:**
Every party score on every question is a judgment call that can be contested.
Methodology must be documented publicly on the page (which source, which quote,
who made the call). Questions must be framed neutrally — test each one by asking
"does this question favor a particular answer?"

**V/J coverage caveat:**
Parties with sparse published material get "staðfest ekki" (no stated position)
rather than a neutral score of 0, which would artificially match them to
neutral users. The results page must show which parties had no stated position
on which questions.

**Check first:** Whether RÚV's Kosningavísir covers 2026 municipal elections at
the Kópavogur level — if so, link to it instead. A local quiz is only worth
building if it covers Kópavogur-specific issues (leikskólagjöld, Kórinn, Borgarlína)
that a national tool would miss.

---

## Harness / structural improvements (from 2026-05-01 retrospective)

### 1. PDF detection in the research agent

Both Viðreisn and Samfylkingin published manifestos the pipeline missed. In
Samfylkingin's case a linked PDF on the same page contained substantially more
than the web summary. The agent fetches page text but doesn't detect linked PDFs.

**Fix:** Add a step to the research agent that checks party `website` URLs for
`<a href="*.pdf">` links and adds them to a "manual review needed" list in the
digest. The PDF can then be fetched and compared against the web summary.

### 2. Structured `manifesto_url` field in `parties.json`

Currently "has a manifesto been published?" lives in a freetext `note` field —
that's what went stale for both Viðreisn and Samfylkingin. A structured
`manifesto_url` field (null until published) would make it machine-checkable:
the research agent can monitor it, `validate-page.py` can cross-reference it
against page content, and it becomes the canonical source for citations.

### 3. Gaps reconciliation after manual manifesto updates

Manual manifesto updates (like today's) bypass the `/kopavogur-updates` skill,
so the `gaps` object in `_data/tracked_updates.json` can remain stale —
the next research run may re-flag gaps as open even after they've been filled.

**Fix:** Add a note to `CLAUDE.md` that manual manifesto updates must be
followed by a gaps reconciliation pass (either via `/kopavogur-updates` or
by manually pruning the gaps object). Consider a `scripts/sync-gaps.py` helper.

### 4. Use a branch for large parallel-edit sessions

Today we worked directly on `main` and hit a conflict when the research bot
merged a PR mid-session. The conflict was trivial but will recur. For sessions
involving large parallel edits, starting in a short-lived branch and merging
at the end eliminates this risk entirely. `scripts/merge-worktree.sh` already
handles the merge correctly.

### 5. Pre-check before spawning second-pass agents

In the second-pass update today, 2 of 5 agents found all content already
present from the first pass. A quick `grep` for key phrases before launching
would have saved those agents. Pattern: before spawning a second-pass agent,
grep the target file for one or two distinctive strings from the new content.

---

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