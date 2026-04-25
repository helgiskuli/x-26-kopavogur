# Sveitarstjórnarkosningar í Kópavogi 2026

Interactive website covering the 2026 Kópavogur municipal elections — party platforms, city finances, and a candidate map.

Deployed at: https://helgiskuli.github.io/x-26-kopavogur/

## Pages

| File | URL | Description |
|------|-----|-------------|
| `index.html` | `/` | **Stefnumál** — party platform comparison |
| `fjarmal.html` | `/fjarmal.html` | **Fjármál** — city budget and financial overview |
| `kort.html` | `/kort.html` | **Frambjóðendur** — candidate map |
| `stefnumal.html` | `/stefnumal.html` | Redirect → `index.html` |

## Data files

| File | Description |
|------|-------------|
| `data/frambjóðendur-x26-kopavogur.geojson` | 151 candidates with coordinates and party info |
| `data/sveitafelagsmork_kopavogur.geojson` | Municipal boundary polygon |

## Local development

All pages can be opened directly from the filesystem.

The map page fetches GeoJSON on GitHub Pages, but falls back to bundled static data when opened via `file://`.
Running a local server is still useful if you want to mirror production behavior exactly:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

GitHub Pages deployment bypasses Jekyll via `.nojekyll`, so the repository is published as plain static files.

## Data sources

- Candidate lists: [Kópavogur — Auglýsing um framboðslista 2026](https://www.kopavogur.is/static/files/Kosningar/2026_sveitarstjornarkosningar/auglysing-um-frambodslista-2026.pdf)
- Address coordinates: [HMS staðfangaskrá](https://hms.is/gogn-og-maelabord/grunngogntilnidurhals/stadfangaskra)
- Property distribution: [Fasteignadreifing — ArcGIS Open Data](https://opin-gogn-luk-lukk.hub.arcgis.com/datasets/b535a730919a4272b21f0899c386c763_7/explore?location=64.047772,-21.757403,11)

## Data preparation

- Verified candidate list against official PDF; fixed name/address errors
- Cross-referenced staðfangaskrá to geocode each candidate's registered address
- Aggregated property room counts per grid cell for the heat map layer
