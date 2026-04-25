# CLAUDE.md

## Project overview

Static GitHub Pages site for the 2026 Kópavogur municipal elections. No build step, no framework — plain HTML/CSS/JS. Deployed directly from the `main` branch.

## Site structure

### Published pages
- `index.html` — Stefnumál: party platform comparison and overview
- `fjarmal.html` — Fjármál: city finances analysis
- `kort.html` — Frambjóðendur: interactive candidate map (Leaflet + Leaflet.heat)
- `stefnumal.html` — redirect to `index.html` for old links

### Planned issue pages (PR4 onward)
- `husnaedi.html` — Húsnæði og uppbygging
- `velferd.html` — Velferð og aðgengi
- `midbaer.html` — Miðbær, menning, framkvæmdir
- `samgongur.html` — Samgöngur og Borgarlína
- `skolar.html` — Leikskólar og grunnskólar
- `stjornsysla.html` — Samráð, stjórnsýsla, gagnsæi

Each issue page follows the 5-part structure + Mat höfundar defined in DESIGN.md.
Content is drafted in `content/<slug>.md` before HTML is written.

## Key conventions

- Language is Icelandic; all UI text, variable names in comments, and page titles are in Icelandic
- Consistent nav order across all pages: **Stefnumál | Fjármál | Frambjóðendur** — issue pages slot between Stefnumál and Fjármál
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

## Local development

`kort.html` and any page using `fetch()` require a local server:

```bash
python3 -m http.server 8000
```

`index.html` and `fjarmal.html` can be opened directly from the filesystem.

## Deployment

GitHub Pages serves the `main` branch root. Push to `main` triggers automatic deployment. The GeoJSON filenames contain Icelandic characters (`ó`, `ð`) — this is intentional; GitHub Pages handles them correctly.

## Skills

- `/kopavogur-issue-page` — use when building or refactoring any issue page; enforces the AGENTS.md checklist and 5-part structure from DESIGN.md
