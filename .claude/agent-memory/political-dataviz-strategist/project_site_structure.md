---
name: Site structure and data inventory
description: Page roster, library availability, and quantitative data found in each page at time of first audit (April 2026)
type: project
---

Static GitHub Pages site. No build step, no framework. Chart.js 4.4.1 already loaded on fjarmal.html only (CDN: cloudflare). All other pages are pure HTML/CSS. Leaflet + Leaflet.heat on kort.html. common.css has: .metric-highlight, .metric-card, .fact-card, .stance-card, .status-grid, .split-grid, .callout, .tag-* — extensive component library already in place.

**Why:** Determines which library to recommend per page (Chart.js is free if you add one script tag; pure CSS is zero-cost).

**How to apply:** Always prefer CSS-only for simple ranked lists and proportion bars. Only recommend Chart.js for time series, grouped bars, or dual-axis charts that have 4+ data points per series.

## Quantitative data inventory by page

### fjarmal.html (already has Chart.js, 3 charts)
- Operating result 2022–2025 (actual) vs. without land income — grouped bar, already charted ✓
- Property tax rate A+C class 2022–2025 + revenue dual-axis — already charted ✓
- Capex 2022–2029 (actual + forecast) vs. depreciation line — already charted ✓
- Debt ratio 72% vs. 150% statutory limit — metric card ✓
- Equity ratio ~46% vs. 15% minimum — metric card ✓
- Debt per capita 1,396 þ.kr. — metric card ✓
- Interest burden 3% of revenue (down from 7%) — metric card ✓
- Net new borrowing 2026: 1,551 m.kr. — callout
- Operating surplus forecast 2026–2029: 343 / 429 / 414 / 494 m.kr. — metric cards ✓
- Mortgage mix: 84.5% indexed (avg 3.11%) vs 15.5% unindexed (avg 8.23%) — prose only, visualizable

### skolar.html
- Budget spend on education: 29,1 ma.kr. — metric-highlight ✓
- Kópavogsmódelið: 30 hrs/week free daycare — prose
- No numerical staffing, waiting-list, or attendance data available (explicitly flagged as missing)

### samgongur.html
- Fossvogsbrú: 270 m long, 8.3 ma.kr. cost, Mar 2026 – mid 2028 — prose in fact-card
- ASHB takeover: 1 July 2026; current 35,000 rides/day → projected 100,000 by 2040 — prose in fact-card
- Kópavogur contribution to Samgöngusáttmálinn: 325 m.kr./yr (from fjarmal.html note)
- Total Samgöngusáttmáll spend 2019–date: 1,412 m.kr. — from fjarmal.html

### husnaedi.html
- Vatnsendahvarf: ~500 units on 29 ha — prose
- Hamraborg/Fannborg: up to 550 units — prose
- Land income 2024: 3,151 m.kr.; 2025: 4,676 m.kr. — prose in fact-card
- Future forecast surplus 343–494 m.kr./yr (references fjarmal.html)

### velferd.html
- Oversupply of support hours: 500 hrs/month above authorised, cost 48 m.kr./yr — fact-card
- Waitlist demand: 500 additional hrs/month needed, cost 49 m.kr./yr — fact-card
- Disability transport shortfall: 8 m.kr. — fact-card
- Total welfare pressure: 97 m.kr./yr — prose

### midbaer.html
- Hamraborg: up to 550 units — fact-card
- Framsókn cultural centre: 150 m.kr./yr vs. Fannborg library 240 m.kr./yr — prose (party claim, unverified)
- Timeline of events 2021–2026 — already a CSS timeline ✓

### stjornsysla.html
- Open accounting since 2016 — prose
- No quantitative data available; policy-coverage matrix is the only viable visual
