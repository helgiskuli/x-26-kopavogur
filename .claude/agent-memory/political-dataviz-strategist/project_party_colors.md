---
name: Party color system
description: Canonical party CSS variables and hex values; never hardcode hex in chart config — use these vars
type: project
---

Seven parties registered for Kópavogur 2026. Colors are canonical and stored in data/parties.json; CSS variables are declared in common.css :root.

| Letter | Party | CSS var | Hex |
|--------|-------|---------|-----|
| B | Framsóknarflokkurinn | --b | #15803d |
| C | Viðreisn | --c | #6d28d9 |
| D | Sjálfstæðisflokkurinn | --d | #1d4ed8 |
| J | Sósíalistaflokkur Íslands | --j | #b91c1c |
| M | Miðflokkurinn | --m | #b45309 |
| S | Samfylkingin | --s | #be123c |
| V | Vinstri græn og óháð | --v | #0f766e |

Coalition structure: D+B = majority. C, J, M, S, V = minority/opposition.

**In Chart.js:** use getComputedStyle(document.documentElement).getPropertyValue('--b').trim() to resolve CSS vars at runtime. Do not hardcode hex values in JS — they would diverge if colors ever change.

**Neutrality note:** J (#b91c1c) and S (#be123c) are visually very similar red tones. On charts where both appear, add a pattern or shape encoding as a secondary differentiator, or note the similarity in the chart legend.
