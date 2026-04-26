---
name: kopavogur-issue-page
description: Use when building a new issue page (málefnasíða) for the Kópavogur 2026 election site — husnaedi.html, velferd.html, midbaer.html, samgongur.html, skolar.html, or stjornsysla.html. Also use when refactoring an existing page into the 5-part structure.
---

# Kópavogur Issue Page Builder

## Overview

Every issue page on this site follows an identical 5-part editorial structure defined in DESIGN.md. The workflow is: read the content draft → scaffold HTML → verify the AGENTS.md checklist before declaring done.

**Governing files — read these first, every time:**
- `DESIGN.md` — components, tokens, typography, all HTML patterns
- `AGENTS.md` — non-negotiables and the page checklist
- `content/TEMPLATE.md` — the content model and slot definitions
- `content/<slug>.md` — the pre-written content for this page (if it exists)
- `research-output/content/0N-<slug>.md` — raw research material

---

## Workflow

### Step 1 — Read before writing

Read in this order:
1. `DESIGN.md` (full)
2. `AGENTS.md` (full)
3. `content/<slug>.md` if it exists; otherwise `research-output/content/0N-<slug>.md`
4. One existing issue page (e.g. `fjarmal.html`) to calibrate component use

Do not begin writing HTML until all four are read.

### Step 2 — Fill the content template

If `content/<slug>.md` does not exist, create it from `content/TEMPLATE.md` and populate:
- `kjarnaspurning` — one precise, answerable question (this becomes `page-question` in HTML)
- Party stance table (all 7 parties; mark `Stefna ekki birt` + `Óstaðfest` where unknown)
- Data section with sources named
- Uncertainty list
- Voter questions (3–6)
- Mat höfundar (2–4 sentences, explicitly labelled `Mín greining`)

### Step 3 — Scaffold the HTML

Copy the boilerplate from DESIGN.md. Use this exact head block:

```html
<!DOCTYPE html>
<html lang="is">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Kópavogur 2026 · [Síðutitill]</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/common.css">
<style>
  /* page-specific CSS only — check common.css before adding anything here */
</style>
</head>
```

### Step 4 — Follow the 5-part structure (order is fixed)

```
page-header  (eyebrow · h1 · page-question · page-desc)
─────────────────────────────────────────────────────
Section 1 · "Af hverju skiptir þetta máli"
  One callout or section-desc. No party positions yet.
<hr class="divider">
─────────────────────────────────────────────────────
Section 2 · "Hvað segja flokkarnir"
  stance-grid — one stance-card per party (all 7).
  Every stance-quote needs: — Nafn, Heimild, dagsetning
  Use stance-note + Óstaðfest tag when no primary source.
<hr class="divider">
─────────────────────────────────────────────────────
Section 3 · "Hvað segja gögnin"  [omit only if zero data exists]
  metric-highlight, metric-row, data-table, or chart-card.
  Every number needs a source in callout or sources block.
<hr class="divider">
─────────────────────────────────────────────────────
Section 4 · "Hvað er óljóst"    [omit only if zero uncertainty]
  callout.warn listing open questions, missing data,
  unpublished party positions.
<hr class="divider">
─────────────────────────────────────────────────────
Section 5 · "Spurningar til kjósanda"
  Plain <ol>. 3–6 questions. No answers. Always required.
<hr class="divider">
─────────────────────────────────────────────────────
Mat höfundar  (always last before sources)
  callout (default, not .pos or .neg)
  callout-title: "Mat höfundar" + tag.tag-dim "Mín greining"
  2–4 sentences. If evidence is inconclusive, say so.
<hr class="divider">
─────────────────────────────────────────────────────
Sources block
  section-eyebrow: "Heimildir"
  mono/text-dim paragraph, one source per line, format:
  Skjal · Tegund · Ár
```

### Step 5 — Update nav in every existing HTML file

When a new page is added, its nav link slots **between Stefnumál and Fjármál**. Update ALL of these files: `index.html`, `fjarmal.html`, `kort.html`, `stefnumal.html`, and every other issue page already in the root.

Nav order template (add new page between Stefnumál and Fjármál):
```html
<a href="index.html">Stefnumál</a>
<a href="husnaedi.html" [class="active"]>Húsnæði</a>   <!-- example -->
<a href="fjarmal.html">Fjármál</a>
<a href="kort.html">Frambjóðendur</a>
```

### Step 6 — Update data files

- Add new sources to `data/sources.json`
- Add new claims to `data/claims.json` (one record per verifiable assertion)
- Do not invent source IDs — match the format already in those files

### Step 7 — Verify the checklist (hard gate)

Do not report the page as done until every item below is ticked. Check each one explicitly against the file you just wrote.

```
[ ] content/<slug>.md drafted and all template slots filled
[ ] File is <slug>.html in repo root (not in a subdirectory)
[ ] DOCTYPE · lang="is" · charset=UTF-8 · viewport meta present
[ ] Google Fonts preconnect + DM Sans + IBM Plex Mono loaded
[ ] <link rel="stylesheet" href="assets/common.css"> in <head>
[ ] Header uses exact markup from DESIGN.md
[ ] Active nav link set on the current page only
[ ] Nav updated in ALL existing .html files
[ ] page-header has: eyebrow · h1 · page-question · page-desc
[ ] 5-part section structure present in correct order
[ ] Sections 1, 2, 5 and Mat höfundar always present
[ ] Every stance-quote includes — Nafn, Heimild, dagsetning
[ ] Paraphrased positions use stance-note + Óstaðfest tag
[ ] All 7 parties represented in Section 2 (mark unknown as Stefna ekki birt)
[ ] Every metric/number has a source
[ ] Mat höfundar uses default callout (not .pos or .neg)
[ ] Mat höfundar is labelled Mín greining
[ ] Sources block present before </main>
[ ] Footer present with ← prev and next → links
[ ] Page opens correctly from filesystem without a server
[ ] No English text visible in the browser
[ ] No new CSS framework, npm package, or build step introduced
[ ] New sources in data/sources.json
[ ] New claims in data/claims.json
```

---

## Source type taxonomy

Use these labels consistently in `stance-note`, source blocks, and `data/sources.json`:

| Label | When |
|---|---|
| `Formleg stefnuskrá` | Official party platform published for this election |
| `Grein frambjóðanda` | Op-ed or signed statement by a candidate |
| `Frétt/viðtal` | Coverage in Vísir, Mbl., RÚV, DV or equivalent |
| `Opinbert gagnaskjal` | Municipal report, budget, Hagstofa, audit |
| `Mín greining` | Site author's conclusions from primary sources |
| `Óstaðfest` | Position reported but not verifiable from primary source |

---

## Common mistakes

**Missing page-question.** The `page-question` (Kjarnaspurning) is required in the page-header on issue pages. It is not a subtitle — it is a precise, answerable question that defines the page's scope. Index.html is the only page that omits it.

**Party colors on non-badge elements.** Party color variables (`--b`, `--d`, etc.) are only valid on `.badge` elements and map markers. Never use them as backgrounds on callouts, section headers, or text blocks.

**Merging analysis with sourced fact.** If a sentence moves from quoting official data to an editorial conclusion, split it. Put conclusions in a `callout` titled "Mat höfundar" marked `Mín greining`.

**Forgetting the nav update.** Every existing HTML file needs the new nav link. This includes `stefnumal.html` (the redirect page). Check with `grep -l "<nav>" *.html` and update each one.

**Disabled issue-links with href="#".** If linking to a page not yet built, omit the `href` attribute entirely rather than using `href="#"`.

**Skipping the sources block.** Every page ends with a sources block before `</main>`. The footer `Heimild:` line is a summary — the sources block is the actual attribution.
