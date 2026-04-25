# Sveitarstjórnarkosningar í Kópavogi 2026

Interactive website covering the 2026 Kópavogur municipal elections — party platforms, city finances, and a candidate map.

Deployed at: https://helgiskuli.github.io/x-26-kopavogur/

Election day: **16 May 2026**

## Pages

| File | URL slug | Description |
|------|----------|-------------|
| `index.html` | `/` | **Stefnumál** — party platform comparison and overview |
| `husnaedi.html` | `/husnaedi.html` | **Húsnæði** — housing and development |
| `velferd.html` | `/velferd.html` | **Velferð** — welfare and accessibility services |
| `midbaer.html` | `/midbaer.html` | **Miðbær** — town centre, culture, construction |
| `samgongur.html` | `/samgongur.html` | **Samgöngur** — transport and Borgarlína |
| `skolar.html` | `/skolar.html` | **Skólar** — preschools and primary schools |
| `stjornsysla.html` | `/stjornsysla.html` | **Stjórnsýsla** — governance, transparency, consultation |
| `fjarmal.html` | `/fjarmal.html` | **Fjármál** — 4-part city budget and financial analysis |
| `kort.html` | `/kort.html` | **Frambjóðendur** — interactive candidate map |
| `stefnumal.html` | `/stefnumal.html` | Redirect → `index.html` |

## Data files

### Runtime (loaded by the map page via fetch)
| File | Description |
|------|-------------|
| `data/frambjóðendur-x26-kopavogur.geojson` | 151 candidates with coordinates, party, and list rank |
| `data/sveitafelagsmork_kopavogur.geojson` | Municipal boundary polygon |

### Editorial (authoring tools — not rendered to users)
| File | Description |
|------|-------------|
| `data/parties.json` | Canonical party metadata: id, letter, name, color, leader, website |
| `data/sources.json` | Bibliography of sources used across all pages (43 entries) |
| `data/claims.json` | Fact-tracking journal: verifiable claims with source IDs and assessment |
| `data/fjarhagsgogn/` | Original municipal PDFs and extracted text (annual accounts 2022–2025, budget 2026, three-year plan 2027–2029) |

## Local development

All pages except the map can be opened directly from the filesystem.

The map page (`kort.html`) fetches GeoJSON from GitHub Pages, but falls back to bundled static data when opened via `file://`. A local server mirrors production exactly:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

GitHub Pages deployment bypasses Jekyll via `.nojekyll`, so the repository is published as plain static files.

## Scripts / harness

Four maintenance scripts live in `scripts/`:

```bash
# Regenerate <nav> in all HTML files from the canonical list (run after any nav change)
python3 scripts/sync-nav.py

# Validate all pages against the checklist before committing
python3 scripts/validate-page.py --all

# Cross-check claims.json source IDs and date consistency across pages
python3 scripts/audit-facts.py

# Safely merge a Claude Code agent worktree into the main tree
scripts/merge-worktree.sh <worktree-path>
```

All scripts run from the repo root and require only the Python standard library.

## Data sources

- Candidate lists: [Kópavogur — Auglýsing um framboðslista 2026](https://www.kopavogur.is/static/files/Kosningar/2026_sveitarstjornarkosningar/auglysing-um-frambodslista-2026.pdf)
- Address coordinates: [HMS staðfangaskrá](https://hms.is/gogn-og-maelabord/grunngogntilnidurhals/stadfangaskra)
- Property distribution: [Fasteignadreifing — ArcGIS Open Data](https://opin-gogn-luk-lukk.hub.arcgis.com/datasets/b535a730919a4272b21f0899c386c763_7/explore?location=64.047772,-21.757403,11)
- Annual accounts 2022–2025: Kópavogsbær official publications
- Budget 2026 and three-year plan 2027–2029: samþykkt af bæjarstjórn 25. nóvember 2025

## Data preparation

- Verified candidate list against official PDF; fixed name/address errors
- Cross-referenced staðfangaskrá to geocode each candidate's registered address
- Aggregated property room counts per grid cell for the heat map layer
- Municipal financial data extracted from PDFs and stored in `data/fjarhagsgogn/`
