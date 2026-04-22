# Sveitarstjórnarkosningar í Kópavogi 2026

Interactive map of candidates running in the 2026 Kópavogur municipal elections.

## What it does

- Plots all 151 candidates on a map of Kópavogur, geocoded to their registered home address
- Filter by party or search by name
- Heatmap layer shows candidate density by neighbourhood

## Files

| File | Description |
|------|-------------|
| `kopavogur_kosningar_2026_light.html` | Self-contained map — open directly in a browser |
| `data/frambjóðendur-x26-kopavogur.geojson` | Candidate data with coordinates and party info |
| `data/sveitafelagsmork_kopavogur.geojson` | Municipal boundary polygon |

## Usage

No build step or server required. Open the HTML file in a browser:

```bash
open kopavogur_kosningar_2026_light.html
```

## Data sources

- Candidate lists: [Kópavogur](https://www.kopavogur.is/static/files/Kosningar/2026_sveitarstjornarkosningar/auglysing-um-frambodslista-2026.pdf)
- Address coordinates: [HMS (staðfangaskrá)](https://hms.is/gogn-og-maelabord/grunngogntilnidurhals/stadfangaskra)
- Property distribution in Kópavogur [Fasteignadreifing](https://opin-gogn-luk-lukk.hub.arcgis.com/datasets/b535a730919a4272b21f0899c386c763_7/explore?location=64.047772,-21.757403,11)

## Data preparation and cleanup

- Verify input and fix errors and missing data in both sources
- Cross reference the property and address dataset
- Augment the candidate list with coordinates
- Aggregate the property density (number of rooms) for the shape