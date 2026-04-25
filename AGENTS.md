# AGENTS.md — Coding-agent rules for Kópavogur 2026

This file overrides any generic defaults. Follow every rule here exactly.
When in doubt: look at an existing page first, then mimic it.

---

## Non-negotiables

### 1. Icelandic UI
All visible text — headings, labels, nav items, button text, placeholder text,
aria-labels, footer copy — must be in Icelandic.
Do not introduce English strings into any `.html` file.

### 2. No framework, no build step
This is a plain-HTML/CSS/JS GitHub Pages site. There is no npm, no bundler,
no template engine, and no server-side rendering.
- Do not add `package.json`, `vite.config.*`, `webpack.config.*`, or any similar file.
- Do not import ES modules via bare specifiers — use CDN `<script src>` only,
  or inline `<script>` blocks.
- New pages are `.html` files in the repo root, not in a `src/` or `pages/` directory.

### 3. Consistent nav order
Every page header must contain exactly these nine links **in this order**:

```
Stefnumál | Húsnæði | Velferð | Miðbær | Samgöngur | Skólar | Stjórnsýsla | Fjármál | Frambjóðendur
```

The active page gets `class="active"` on its `<a>` tag.

**Never edit nav links manually in individual files.** Run `scripts/sync-nav.py` to regenerate nav in all pages from the canonical list in that script.

Use the canonical header markup from DESIGN.md, section "Header".

### 4. No unsourced claims
Every factual assertion that could be disputed must have a source.

- Numbers in metric cards → cite in the nearest `callout` or the sources section.
- Quotes in `stance-quote` elements → must include `— Name, Publication, date`.
- Party positions described without a direct quote → use `stance-note` and note
  "Heimild vantar" or "Stefna ekki birt" if the source is missing.
- Do not invent or paraphrase data. If you cannot find a primary source, omit the claim.

### 5. Reuse existing components
Before writing new CSS or new HTML patterns, check DESIGN.md.
Every card type, label style, and layout pattern is already defined there.

Required checks before adding new CSS:
1. Does a matching component exist? → Use it.
2. Does a CSS variable cover this color? → Use the variable.
3. Is this a one-off inline style? → Only acceptable for `background: var(--X)`
   on party badge/color elements.

If you must introduce a new component:
- Define it in a `<style>` block in the new page.
- Document it in DESIGN.md in the same PR.

---

## Adding a new issue page

Before writing HTML, fill in `content/<slug>.md` using `content/TEMPLATE.md`.
Complete the checklist in that file first, then build the HTML.

```
[ ] content/<slug>.md drafted and checklist ticked
[ ] File created as a .html in repo root (e.g., husnaedi.html)
[ ] DOCTYPE, lang="is", charset=UTF-8, viewport meta present
[ ] Google Fonts preconnect + DM Sans + IBM Plex Mono loaded
[ ] <link rel="stylesheet" href="assets/common.css"> in <head>
[ ] Header copied from DESIGN.md with correct active nav link
[ ] Nav updated in ALL other .html files to include the new page
[ ] page-header includes eyebrow, h1, page-question (Kjarnaspurning), page-desc
[ ] 5-part section structure followed (see DESIGN.md)
[ ] Every factual claim has a source_id matching data/sources.json
[ ] New sources added to data/sources.json; new claims to data/claims.json
[ ] Mat höfundar section present, labelled Mín greining
[ ] Sources block present before </main>
[ ] Footer present with ← and → links to adjacent pages
[ ] Page works when opened directly from filesystem (no server required)
[ ] No English text visible anywhere in the browser
[ ] No new dependencies added
```

---

## CSS rules

- Shared CSS is in `assets/common.css`. Link it with `<link rel="stylesheet" href="assets/common.css">`.
- Do not duplicate CSS that is already in `assets/common.css`. Page `<style>` blocks contain only page-specific components.
- `kort.html` is the exception: it is self-contained with its own `:root` block and does not link `assets/common.css`.
- Keep responsive breakpoints consistent: `640px` for grid collapses, `400px` for hiding nav.
- Do not add CSS frameworks (Tailwind, Bootstrap, etc.).

---

## JavaScript rules

- Only use vanilla JS. No React, Vue, Alpine, or other libraries.
- External libraries (Chart.js, Leaflet) are acceptable from cdnjs.cloudflare.com
  only when the functionality genuinely requires them.
- Do not add analytics, tracking, or third-party scripts.

---

## Git rules

- Commit messages in English (per git convention), content in Icelandic.
- Do not push directly to `main` without review when making structural changes.
- Each new issue page should be a separate PR from nav/CSS changes.

---

## What this site is not

- Not a campaign site. Content must be neutral and sourced.
- Not a data app. Keep interactivity minimal (kort.html is the exception).
- Not a design experiment. Do not redesign existing pages when adding new ones.
