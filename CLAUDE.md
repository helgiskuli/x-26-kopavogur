# CLAUDE.md

## Project overview

Static GitHub Pages site for the 2026 Kópavogur municipal elections. No build step, no framework — plain HTML/CSS/JS. Deployed directly from the `main` branch.

## Site structure

- `index.html` — landing page, party platform comparison (Stefnumál)
- `fjarmal.html` — city finances page (Fjármál)
- `kort.html` — interactive candidate map (Frambjóðendur), uses Leaflet + Leaflet.heat
- `stefnumal.html` — redirect to `index.html` for old links
- `data/` — GeoJSON files loaded by `kort.html` via `fetch()`

## Key conventions

- Language is Icelandic; all UI text, variable names in comments, and page titles are in Icelandic
- Consistent nav order across all pages: **Stefnumál | Fjármál | Frambjóðendur**
- Site title link in the header always goes to `index.html`
- Party colors are stored in the GeoJSON `party_color` property; do not hardcode them in JS logic

## Local development

`kort.html` uses `fetch()` for GeoJSON, so a local server is required:

```bash
python3 -m http.server 8000
```

`index.html` and `fjarmal.html` can be opened directly from the filesystem.

## Data files

- `data/frambjóðendur-x26-kopavogur.geojson` — candidate points (name, address, party, list_rank, party_color, coord_source)
- `data/sveitafelagsmork_kopavogur.geojson` — municipal boundary polygon

The `densityData` heat map array in `kort.html` is derived from property room counts and is stored inline (not in `data/`) because it is pre-aggregated and not a standard GeoJSON format.

## Deployment

GitHub Pages serves the `main` branch root. Push to `main` triggers automatic deployment. The GeoJSON filenames contain Icelandic characters (`ó`, `ð`) — this is intentional; GitHub Pages handles them correctly.
