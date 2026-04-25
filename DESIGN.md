# Design System — Kópavogur 2026

Reference for anyone adding new pages or sections. Every element documented here
already exists in at least one of the current HTML files. Reuse before inventing.

---

## Markmið

Síðan hjálpar kjósanda í Kópavogi að bera saman flokka, staðhæfingar og gögn.
Hún er ekki kosningaherferðasíða. Hún er greiningartæki.

- Gögn og tilvitnanir koma á undan ályktunum.
- Óljósleiki er merktur — hann er ekki þagaður yfir.
- Rödd síðunnar er gagnadrifin og hlutlæg, ekki málefnaleg.

---

## Design Tokens (CSS variables)

Paste the full `:root` block into every new page. The canonical set is:

```css
:root {
  --bg:          #f4f5f7;   /* page background */
  --bg-card:     #ffffff;   /* card/surface background */
  --border:      #e2e5ea;   /* default border */
  --border-light:#d1d5db;   /* subtler border (table totals etc.) */
  --text:        #1a1f2e;   /* body text */
  --text-muted:  #6b7280;   /* secondary text */
  --text-dim:    #9ca3af;   /* tertiary / metadata */
  --accent:      #3b64dc;   /* primary accent (links, active nav, eyebrows) */
  --neg:         #ef4444;   /* negative / deficit */
  --neg-dim:     rgba(239,68,68,0.1);
  --pos:         #059669;   /* positive / surplus */
  --pos-dim:     rgba(5,150,105,0.1);
  --warn:        #d97706;   /* warning / uncertainty */
  --font:        'DM Sans', system-ui, sans-serif;
  --mono:        'IBM Plex Mono', monospace;

  /* Party colors — used via inline style="background:var(--X)" */
  --b: #15803d;   /* Framsóknarflokkurinn */
  --c: #6d28d9;   /* Viðreisn */
  --d: #1d4ed8;   /* Sjálfstæðisflokkurinn */
  --j: #b91c1c;   /* Sósíalistaflokkur Íslands */
  --m: #b45309;   /* Miðflokkurinn */
  --s: #be123c;   /* Samfylkingin */
  --v: #0f766e;   /* Vinstri græn og óháð */
}
```

Tokens are defined in `assets/common.css` and linked from all content pages.
`kort.html` is self-contained and carries its own `:root` block.

**Rule:** always use a token; never hardcode a hex value in HTML `style=""` attributes
except for party colors (they come from GeoJSON `party_color` in `kort.html`).

---

## Typography

| Role | Size | Weight | Font | Notes |
|------|------|--------|------|-------|
| Page eyebrow | 11px | 400 | mono | uppercase, `letter-spacing: 0.1em`, `color: var(--accent)` |
| Page title h1 | `clamp(1.4rem, 4vw, 2rem)` | 600 | sans | `line-height: 1.25` |
| Page question | 15px | 500 | sans | italic, `color: var(--text)`, `max-width: 65ch` — issue pages only |
| Page description | 14px | 400 | sans | `color: var(--text-muted)`, `max-width: 60ch` |
| Section eyebrow | 10px | 400 | mono | uppercase, `letter-spacing: 0.12em`, `color: var(--text-dim)` |
| Section heading h2 | 1.05rem | 600 | sans | `color: var(--text)` |
| Section description | 13px | 400 | sans | `color: var(--text-muted)`, `max-width: 65ch` |
| Tag / badge label | 11px | 500 | mono | |
| Card metadata | 11px | 400 | mono | `color: var(--text-dim)` |
| Body in cards / callouts | 13px | 400 | sans | `color: var(--text-muted)`, `line-height: 1.7` |
| Monospace value (metrics) | varies | 600–700 | mono | |

---

## Layout

```css
main {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 5rem;
}
```

`kort.html` is a full-viewport exception; all other pages share this layout.

---

## Components

### Header

White bar, 52 px tall, `border-bottom: 1px solid var(--border)`.

```html
<header>
  <div class="header-inner">
    <a class="site-title" href="index.html">Kópavogur <span>2026</span></a>
    <nav>
      <a href="index.html" [class="active"]>Stefnumál</a>
      <a href="fjarmal.html" [class="active"]>Fjármál</a>
      <a href="kort.html" [class="active"]>Frambjóðendur</a>
    </nav>
  </div>
</header>
```

Set exactly one `class="active"` to mark the current page.
Nav order is fixed: **Stefnumál → Fjármál → Frambjóðendur**.
New issue pages slot in between Stefnumál and Fjármál.

---

### Page Header block

```html
<div class="page-header">
  <p class="page-eyebrow">Flokkur · Apríl 2026</p>
  <h1>Fyrirsögn</h1>
  <p class="page-desc">Lýsing — hvað er á þessari síðu og hvaðan gögn koma.</p>
</div>
```

For issue pages, add a `page-question` between `h1` and `page-desc`:

```html
<div class="page-header">
  <p class="page-eyebrow">Málefni · Apríl 2026</p>
  <h1>Velferð og aðgengi</h1>
  <p class="page-question">Er þjónustuframboð Kópavogsbæjar í velferðarmálum í samræmi
  við lögbundnar skyldur, þörf íbúa og fjárhagslegt svigrúm?</p>
  <p class="page-desc">Heimild: ársreikningar, þjónustuskýrslur og afstaður flokkanna.</p>
</div>
```

`page-question` is the `Kjarnaspurning` from the content model — one precise, answerable
question that defines the scope of the page. It is not a subtitle; it is a claim about
what the page will actually resolve.

The eyebrow should identify the topic and a date or source reference.
The description must name the source(s) used on the page.

---

### Section pattern

Every thematic block follows this three-part header:

```html
<div class="section">
  <p class="section-eyebrow">Hluti 1 / 3</p>
  <h2>Fyrirsögn hluta</h2>
  <p class="section-desc">Ein eða tvær setningar sem setja hlutann í samhengi.</p>
  <!-- content cards / callouts -->
</div>
<hr class="divider">
```

---

### Issue page structure (5-part pattern)

Every new issue page must follow this editorial sequence. Use the section pattern
for each part; the order is fixed.

The `page-header` must include a `page-question` (the `Kjarnaspurning` from the
content model) between `h1` and `page-desc`. See the Page Header block component.

| # | Section eyebrow | Content |
|---|---|---|
| 1 | `Af hverju skiptir þetta máli` | One callout or `section-desc` explaining why this issue matters for the 2026 election. No party positions yet. |
| 2 | `Hvað segja flokkarnir` | Stance grid — one card per party with quote, tag, and source. |
| 3 | `Hvað segja gögnin` | Metric cards, charts, or data tables drawn from official sources. |
| 4 | `Hvað er óljóst` | A `callout warn` listing open questions, missing data, or positions not yet published. |
| 5 | `Spurningar til kjósanda` | A plain `<ol>` of questions voters should put to candidates. No answers. |
| — | `Mat höfundar` | See the Mat höfundar component. Always the last section before sources. |

Parts 3 and 4 may be omitted only if no relevant data or uncertainty exists.
Parts 5 and Mat are always required.

---

### Badge

A colored square with a party letter. Two sizes:

```html
<div class="badge badge-lg" style="background:var(--d)">D</div>   <!-- 38×38px -->
<div class="badge badge-sm" style="background:var(--d)">D</div>   <!-- 26×26px -->
```

Use `badge-lg` in party overview cards, `badge-sm` everywhere else.

---

### Tag

Inline pill for status, stance, or classification.

```html
<span class="tag tag-pos">Styður</span>
<span class="tag tag-neg">Gagnrýnir</span>
<span class="tag tag-warn">Endurskoðar</span>
<span class="tag tag-dim">Aðrar áherslur</span>
```

#### Source badge tags

Used alongside `.tag` to label the source type of a claim, quote, or metric. Color encodes reliability at a glance: blue = official, amber = interpretation, red = missing.

| Class | Label | When to use |
|---|---|---|
| `tag-official` | `Opinbert gagnaskjal` / `Fjárhagsskjöl` | Municipal report, budget, Hagstofa, audit |
| `tag-party` | `Formleg stefnuskrá` / `Grein frambjóðanda` | Party platform or signed candidate statement |
| `tag-news` | `Frétt/viðtal` | Coverage in Vísir, Mbl., RÚV, DV or equivalent |
| `tag-analysis` | `Mín greining` | Site author's conclusions from primary sources |
| `tag-missing` | `Vantar heimild` | Claim exists but primary source is absent |
| `tag-unverified` | `Þarf að staðfesta` | Position reported but not verifiable |

```html
<span class="tag tag-official">Opinbert gagnaskjal</span>
<span class="tag tag-party">Grein frambjóðanda</span>
<span class="tag tag-news">Frétt/viðtal</span>
<span class="tag tag-analysis">Mín greining</span>
<span class="tag tag-missing">Vantar heimild</span>
<span class="tag tag-unverified">Þarf að staðfesta</span>
```

**Rule:** never use `tag-pos` / `tag-neg` for source labels — those signal data sentiment only.

---

### Party card (overview grid)

Used in the party listing section of `index.html`.

```html
<div class="party-grid">
  <div class="party-card">
    <div class="badge badge-lg" style="background:var(--d)">D</div>
    <div class="party-info">
      <div class="party-name">Flokkurinn</div>
      <div class="party-leader">Nafn oddvita</div>
      <a class="party-web" href="https://..." target="_blank" rel="noopener">url.is ↗</a>
    </div>
  </div>
</div>
```

---

### Stance card (party position grid)

Two-column grid (`stance-grid`) for comparing party positions on a topic.

```html
<div class="stance-grid">
  <div class="stance-card">
    <div class="stance-header">
      <div class="badge badge-sm" style="background:var(--d)">D</div>
      <span class="stance-pname">Flokkurinn</span>
      <span class="tag tag-pos">Styður</span>
    </div>
    <p class="stance-quote">„Tilvitnun." — Nafn, Heimild, dagsetning</p>
    <p class="stance-note">Frekari útskýring eða fyrirvari.</p>
  </div>
</div>
```

**Rule:** every `stance-quote` must include a specific source attribution.
If no direct quote is available, use `stance-note` only with a source reference.

---

### Split grid (for/against)

Two-column layout showing parties on opposite sides of a binary question.

```html
<div class="split-grid">
  <div class="split-col">
    <div class="split-head for">Styður</div>
    <div class="split-body">
      <div class="split-party">
        <div class="badge badge-sm" style="background:var(--d)">D</div>
        Flokkurinn
      </div>
      <div class="split-note">Heimild / fyrirvari</div>
    </div>
  </div>
  <div class="split-col">
    <div class="split-head against">Á móti</div>
    <div class="split-body">…</div>
  </div>
</div>
```

Column ratio: `3fr 2fr` when the "for" side dominates; invert as needed.

---

### Callout

Bordered highlight block. Four variants:

```html
<div class="callout">           <!-- default: accent left border -->
<div class="callout warn">      <!-- amber left border -->
<div class="callout neg">       <!-- red left border -->
<div class="callout pos">       <!-- green left border -->
```

```html
<div class="callout warn">
  <div class="callout-title">Fyrirsögn</div>
  <p>Texti — hér er heimild nauðsynleg ef um staðhæfingu er að ræða.</p>
</div>
```

---

### Metric highlight

Large KPI card used once per section to draw attention to a headline number.

```html
<div class="metric-highlight">
  <div class="metric-big" style="color:var(--neg)">−3 ma.</div>
  <div class="metric-label">
    Útskýring á tölunni og hvaðan hún kemur.
    <a href="fjarmal.html">Frekari greining →</a>
  </div>
</div>
```

---

### Metric card row

Small KPI cards in a four-column grid, used for time-series snapshots.

```html
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-year">2022</div>
    <div class="metric-value neg">−2.083</div>
    <div class="metric-sub">m.kr. — skráð</div>
  </div>
  …
</div>
```

Apply `.neg` or `.pos` to `.metric-value` for colour; omit for neutral.

---

### Status grid

Table-like list of parties with column indicators. Used for tracking policy
publication status.

```html
<div class="status-grid">
  <div class="status-row">
    <div class="status-party">
      <div class="badge badge-sm" style="background:var(--d)">D</div>
      <div>
        <div class="status-name">Flokkurinn</div>
        <div class="status-url">url.is</div>
      </div>
    </div>
    <div class="status-cols">
      <div class="status-col">
        <div class="status-col-label">Heimasíða</div>
        <span class="tag tag-pos">Virk</span>
      </div>
    </div>
  </div>
</div>
```

---

### Chart card

Wrapper for a `<canvas>` Chart.js element.

```html
<div class="chart-card">
  <div class="chart-legend">
    <div class="leg"><div class="leg-dot" style="background:#3b64dc"></div>Merkimiði</div>
  </div>
  <div class="chart-wrap" style="height:260px">
    <canvas id="chartId" role="img" aria-label="Lýsing á gögnum">Gögn: …</canvas>
  </div>
</div>
```

Always include `role="img"` and `aria-label` with a plain-text data summary.

---

### Data table

```html
<table class="data-table">
  <thead>
    <tr><th>Dálkur</th>…</tr>
  </thead>
  <tbody>
    <tr>
      <td>Lýsing</td>
      <td class="neg">−1.234 m.kr.</td>
      <td><span class="tag tag-neg">Halli</span></td>
    </tr>
    <tr class="total-row">
      <td>Samtals</td>…
    </tr>
  </tbody>
</table>
```

---

### Fact card

Presents a single verified fact with a source badge. Use inside a `.fact-grid` for multiple facts side by side.

```html
<div class="fact-grid">
  <div class="fact-card">
    <p class="fact-body">Kópavogsmódelið innleitt haustið 2023 — sex tímar gjaldfrjáls leikskóli á dag.</p>
    <div class="fact-source">
      <span class="tag tag-official">Opinbert gagnaskjal</span>
    </div>
  </div>
</div>
```

**Rule:** every `fact-card` must have at least one source badge in `.fact-source`.

---

### Uncertainty card

Use `callout.warn` with a descriptive title. No separate CSS class is needed.

```html
<div class="callout warn">
  <div class="callout-title">Hvað vantar?</div>
  <p>
    [Flokkur X] hefur ekki birt formlega stefnu um þetta mál.
    <span class="tag tag-missing">Vantar heimild</span>
  </p>
</div>
```

---

### Question list

Numbered voter questions in Section 5 ("Spurningar til kjósanda"). Plain `<ol>` with `.question-list`. No answers — questions only.

```html
<ol class="question-list">
  <li>Hvernig hyggst flokkurinn fjármagna…?</li>
  <li>Hvaða breytingar eru fyrirhugaðar á…?</li>
</ol>
```

---

### Source block

Every page must end with a source attribution section before `</main>`.

```html
<div class="section">
  <p class="section-eyebrow">Heimildir</p>
  <p style="font-size:13px;color:var(--text-dim);font-family:var(--mono);line-height:1.8">
    Heimild A · Heimild B<br>
    Dagsetning · Fyrirvari ef við á
  </p>
</div>
```

---

### Mat höfundar (editorial assessment)

The final section of every issue page. Always the last section before the sources
block. Uses the existing `callout` component — no new CSS required.

Rules:
- Always present on issue pages. Never omit it.
- Kept short: 2–4 sentences.
- Must be explicitly labelled `Mín greining` so readers know it is analysis, not fact.
- Never use `callout.pos` or `callout.neg` — those signal data polarity, not editorial
  conclusions. Use the default `callout` (accent border).
- If the evidence is genuinely inconclusive, say so — do not force a verdict.

```html
<div class="section">
  <p class="section-eyebrow">Mat höfundar</p>
  <h2>Niðurstaða</h2>
  <div class="callout">
    <div class="callout-title">
      Mat höfundar
      <span class="tag tag-dim" style="margin-left:0.5rem">Mín greining</span>
    </div>
    <p>
      Gögnin benda til þess að [X], en þar sem [Y flokkur/flokkur] hefur ekki birt
      formlega stefnu er erfitt að gera fulla samanburð. Kjósandinn þarf að spyrja
      sérstaklega um [Z].
    </p>
  </div>
</div>
```

The `Mín greining` tag in the callout title serves as a persistent visual reminder
that what follows is interpretation, not quotation.

---

### Footer

```html
<footer>
  <a href="index.html">← Stefnumál</a>
  &nbsp;·&nbsp;
  Kópavogur 2026 · [Síðutitill]
  &nbsp;·&nbsp;
  Heimild: [stutt lýsing]
  &nbsp;·&nbsp;
  <a href="kort.html">Frambjóðendur →</a>
</footer>
```

---

## Source labels and citation rules

### Source type taxonomy

Every claim must carry one of these six labels. Use them as inline `tag-dim` tags
in `stance-note` elements or in the sources section at the bottom of the page.

| Label | Íslenska | When to use |
|---|---|---|
| `Formleg stefnuskrá` | Formal policy document | Official party platform published on the party's own site for this election |
| `Grein frambjóðanda` | Candidate article | Op-ed, blog post, or statement written and signed by the candidate |
| `Frétt/viðtal` | News / interview | Coverage in Vísir, DV, Mbl., RÚV, Bylgjan, or equivalent |
| `Opinbert gagnaskjal` | Official data document | Municipal annual report, budget, statistics from Hagstofa, audit |
| `Mín greining` | Editorial analysis | Conclusions drawn by this site from primary sources — must be clearly separated from quoted facts |
| `Óstaðfest` | Unconfirmed | Position reported but not verifiable from a primary source; use `stance-note`, not `stance-quote` |

Usage in a stance card:

```html
<p class="stance-note">
  Endurskoða Kópavogsmódelið í þágu foreldra og barna.
  <span class="tag tag-dim">Grein frambjóðanda</span>
</p>
```

Usage in the sources section:

```
Samstæðuársreikningur Kópavogsbæjar 2025 · Opinbert gagnaskjal
Vísir, 20. apríl 2026 · Frétt/viðtal
Útreikningur höfundar á lóðatekjum · Mín greining
```

### General rules

- Every factual claim in a `stance-quote` needs an attribution: `— Nafn, Miðill, dagsetning`.
- Every number in a metric card or data table needs a source in the nearest `callout`
  or in the footer sources section.
- Use `stance-note` (not `stance-quote`) for paraphrased or unverified positions.
- `Mín greining` claims must be visually separated from sourced facts — use a
  `callout` with a clearly labeled title such as "Mat höfundar".
- Do not mix `Mín greining` and `Opinbert gagnaskjal` in the same sentence without signalling the shift.

---

## Writing style

- Language: Icelandic throughout. No English in UI text, labels, or headings.
- Tone: neutral and factual. Present party positions without endorsing them.
- Numbers: Icelandic decimal comma (`1.234,5`); currency as `m.kr.` (milljónar króna)
  or `ma.kr.` (milljarðar króna).
- Dates: `16. maí 2026` (day. month year).
- Quotes: Icelandic quotation marks `„…"`.
- Avoid adjectives that evaluate parties; stick to verbs (`styður`, `gagnrýnir`,
  `endurskoðar`, `leggur til`).

### Forðast — things to avoid

**Nýtt layout fyrir hvern kafla.** Every issue page uses the same 5-part structure
and the same components. Do not invent a new visual treatment because the topic
feels different.

**Langar tilvitnanir.** A `stance-quote` should be one to three sentences. If the
source material is longer, paraphrase it in `stance-note` and label it
`Mín greining` or `Frétt/viðtal` as appropriate.

**Flokkslitaðar hliðar.** Party colors are used only in badges and map markers —
never as background colors on text blocks, callouts, or section headers.
A `callout.pos` means positive financial outlook; it does not mean "D+B are right".
Color signals data sentiment, not political alignment.

**Að blanda staðreyndum og mati án merkingar.** If a paragraph moves from a quoted
fact to an editorial conclusion, split it. Put the conclusion in a separate
`callout` titled "Mat höfundar" and mark it `Mín greining`.
Never let analysis appear to carry the authority of a primary source.
