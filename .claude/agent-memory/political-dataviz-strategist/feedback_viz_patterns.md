---
name: Visualization patterns that work on this site
description: Chart types and CSS patterns proven or assessed to render cleanly in this no-build static site context
type: feedback
---

## What works well

**CSS bar charts (rate rows):** The .rate-bar-row / .bar-track / .bar-fill pattern in fjarmal.html renders cleanly and needs no JS. Ideal for ranked comparisons with 4–8 rows.

**Chart.js grouped bars with zero line:** Implemented in fjarmal.html chart1. Rendering is crisp. The trick: use `grid.color: ctx => ctx.tick.value === 0 ? zeroLine : gridColor` to highlight the zero baseline without distorting the scale.

**Chart.js dual-axis (bar + line):** Chart2 in fjarmal.html demonstrates this works well. Keep the secondary axis on the right, use a contrasting line color (accent vs. warn), and suppress the secondary grid lines (`grid: { display: false }`).

**Metric cards (.metric-card / .metric-highlight):** Already in common.css. Use for KPI callouts — headline number + label + source context. Works well at the top of a section to anchor a chart.

**CSS timeline (midbaer.html):** The border-left + ::before dot pattern is already implemented. Good for event sequences. Do not over-use — reserve for chronological narratives.

**Stance-coverage matrix:** Not yet implemented but assessed as the highest-impact addition across issue pages. Pure HTML table with colored badge cells. No JS needed.

## What to avoid

**Pie charts:** Never on this site. 7 parties = too many segments. Use stacked bars or waffle grids instead.

**Radar/spider charts:** Visually appealing but encode relative positioning in a way that implies meaningful cardinal distances between policy positions. Too much framing risk in a political context.

**Animation without a reason:** Chart.js animations are enabled by default. Keep them on fjarmal.html (it feels appropriate for a financial analysis page) but suppress or minimize on issue pages where the chart is secondary to text.

**Dual-series grouped bars for party comparisons:** If one party has missing data, a grouped bar creates a visual gap that draws attention to that party specifically. Use a dot plot or table instead, where absent data is shown as a dash or "Stefna ekki birt" text cell.

## Implementation notes

- Chart.js is already on CDN for fjarmal.html only. To use it on other pages, add the same script tag: `<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>`
- CSS var resolution in Chart.js: `getComputedStyle(document.documentElement).getPropertyValue('--b').trim()`
- All tooltip callbacks should use Icelandic number formatting: `v.toLocaleString('is-IS')`
- Font for chart labels: already set globally in fjarmal.html — `Chart.defaults.font.family = "'IBM Plex Mono', monospace"` and `Chart.defaults.font.size = 11`
