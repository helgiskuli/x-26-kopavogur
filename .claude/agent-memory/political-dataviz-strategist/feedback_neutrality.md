---
name: Neutrality pitfalls by page
description: Known asymmetric-data problems and framing risks encountered during the April 2026 audit
type: feedback
---

## General rule
Never render a chart where one or more parties appear to have a missing bar/cell unless the absence itself is the data point (e.g., "has not published a policy"). In that case, show a neutral placeholder ("Stefna ekki birt") — never leave a visual gap, which implies negative space.

## Per-page pitfalls

### skolar.html
The stance grid shows a nuanced range: D and B support Kópavogsmódelið, C/S gagnrýna framkvæmd, V endurskoðar, J gagnrýnir, M has different focus. Any visualization of "support level" risks creating an ordinal scale that embeds editorial judgment. Recommended approach: the coverage matrix (see strategy doc) uses binary presence/absence of a published stance position — never a scored ranking.

### samgongur.html
6 of 7 parties support Samgöngusáttmálinn; only M opposes. A simple for/against split visual would make M look isolated in a way the data supports but that could read as marginalizing. The existing .split-grid CSS component handles this well (3fr/2fr proportional columns). If used, label it factually: "Afstaða til Samgöngusáttmálans" not "Borgarlínu stuðningur" — the distinction matters because M opposes Borgarlína specifically, not necessarily all transport spending.

### husnaedi.html
3 of 7 parties have not published a housing policy (C, M, V explicitly flagged as missing). Any visual of party positions that includes these three must show "Stefna ekki birt" cells, not blank cells. Blank cells look like zero; "missing" is a distinct state.

### velferd.html
5 of 7 parties have no published welfare stance. The coverage matrix is particularly important here — it makes the absence legible rather than embarrassing for specific parties.

### midbaer.html
The 150 m.kr. vs 240 m.kr. cost comparison from Framsókn is an unverified party claim and must never be visualized as a factual chart. It may be cited in prose with "Grein frambjóðanda" tag only.

### fjarmal.html (existing charts)
Chart 1 dual series: "Skráð" vs. "Án lóðatekna" is a factual/analytical distinction, not a partisan one — this is fine. The current color choice (blue for recorded, red for without land income) works because red = risk, not party color.

### J (#b91c1c) vs S (#be123c) color collision
These two parties have visually indistinguishable red tones in any chart legend. Always add a secondary differentiator (e.g., different border style, letter label inside the data point, or tooltip-only differentiation with a written note in the legend).
