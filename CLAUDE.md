# CLAUDE.md

## Project overview

Static GitHub Pages site for the 2026 Kópavogur municipal elections. No build step, no framework — plain HTML/CSS/JS. Deployed directly from the `main` branch.

## Site structure

### Published pages (all live)
- `index.html` — Stefnumál: party platform comparison and overview
- `husnaedi.html` — Húsnæði og uppbygging
- `velferd.html` — Velferð og aðgengi
- `midbaer.html` — Miðbær, menning og framkvæmdir
- `samgongur.html` — Samgöngur og Borgarlína
- `skolar.html` — Leikskólar og grunnskólar
- `stjornsysla.html` — Samráð, stjórnsýsla og gagnsæi
- `fjarmal.html` — Fjármál: 4-part financial analysis (distinct structure from issue pages)
- `kort.html` — Frambjóðendur: interactive candidate map (Leaflet + Leaflet.heat)
- `stefnumal.html` — redirect to `index.html` for old links

Each issue page (all except `index.html`, `fjarmal.html`, `kort.html`, `stefnumal.html`) follows the 5-part structure + Mat höfundar defined in DESIGN.md. Content is drafted in `content/<slug>.md` before HTML is written.

## Key conventions

- Language is Icelandic; all UI text, variable names in comments, and page titles are in Icelandic
- Nav order is canonical — **never edit nav links manually in individual files**. Run `scripts/sync-nav.py` instead. Current order: Stefnumál | Húsnæði | Velferð | Miðbær | Samgöngur | Skólar | Stjórnsýsla | Fjármál | Frambjóðendur
- Site title link in the header always goes to `index.html`
- Party colors are stored in `data/parties.json` and in the GeoJSON `party_color` property; do not hardcode them in JS logic
- Shared CSS lives in `assets/common.css`; page-specific CSS stays in inline `<style>` blocks

## Assets

- `assets/common.css` — shared design tokens, layout, components; linked from all pages except `kort.html`
- `assets/site.js` — shared JS utilities (Icelandic number formatting); load only when needed

## Data files

### GeoJSON (runtime — loaded via fetch())
- `data/frambjóðendur-x26-kopavogur.geojson` — candidate points (name, address, party, list_rank, party_color, coord_source)
- `data/sveitafelagsmork_kopavogur.geojson` — municipal boundary polygon

### Editorial data (authoring tools — not loaded at runtime by content pages)
- `data/parties.json` — canonical party metadata: id, letter, name, color, css_var, leader, website, coalition
- `data/sources.json` — bibliography of sources; `local_pdf` and `local_txt` fields point into `data/fjarhagsgogn/`
- `data/claims.json` — fact-tracking journal of party claims; fields include assessment and confidence — **internal only, never render confidence scores to users**
- `data/fjarhagsgogn/` — original municipal PDFs and extracted text: ársreikningar 2022–2025, fjárhagsáætlun 2026, þriggja ára áætlun 2027–2029, greinargerð 2026

The `densityData` heat map array in `kort.html` is derived from property room counts and is stored inline because it is pre-aggregated and not standard GeoJSON.

## Content model

Issue pages are planned in `content/<slug>.md` using `content/TEMPLATE.md`.
Fill the template completely (including checklist) before writing any HTML.

## Scripts / harness

Four maintenance scripts live in `scripts/`. Run from the repo root.

| Script | Purpose |
|--------|---------|
| `scripts/sync-nav.py` | Regenerate `<nav>` in all HTML files from the canonical list in the script. **Run after any nav change** instead of editing files manually. |
| `scripts/validate-page.py --all` | Check all pages against the AGENTS.md checklist: nav completeness, required sections, English artifacts, known typos. Run before every commit. |
| `scripts/audit-facts.py` | Cross-check `claims.json` source IDs against `sources.json`; verify known date/fact patterns are consistent across pages. |
| `scripts/merge-worktree.sh <path>` | Safely merge a Claude Code agent worktree: copies new HTML files, deduplicates JSON data files, runs sync-nav and validate. Use instead of manual merging. |

**Before merging any agent worktree:** `scripts/merge-worktree.sh <worktree-path>`

**Before every commit:** `python3 scripts/validate-page.py --all`

## Local development

`kort.html` and any page using `fetch()` require a local server:

```bash
python3 -m http.server 8000
```

All other pages can be opened directly from the filesystem.

## Deployment

GitHub Pages serves the `main` branch root. Push to `main` triggers automatic deployment. The GeoJSON filenames contain Icelandic characters (`ó`, `ð`) — this is intentional; GitHub Pages handles them correctly.

## Skills

- `/kopavogur-issue-page` — use when building or refactoring any issue page; enforces the AGENTS.md checklist and 5-part structure from DESIGN.md
