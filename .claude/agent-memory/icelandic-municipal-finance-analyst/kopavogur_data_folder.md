---
name: Kópavogur fjárhagsgögn folder
description: Location and inventory of Kópavogsbær financial PDFs used for fact-checking campaign claims
type: reference
---

Kópavogsbær financial PDFs live at `/Users/helgi/github/private/x-26-kopavogur/data/fjarhagsgogn/`.
Contents as of 2026-04-24:
- `arsreikningur-2022.pdf` — samstæðuársreikningur A+B (audited)
- `arsreikningur-2023.pdf` — samstæðuársreikningur A+B (audited)
- `arsreikningur-2024.pdf` — samstæðuársreikningur A+B (audited); contains Roðahvarf/Vatnsendahvarf lot allocation note
- `arsreikningur-2025.pdf` — samstæðuársreikningur A+B (dags. 16. apríl 2026, tilbúinn til endurskoðunar; endurskoðandi áritar við seinni umræðu 12. maí 2026)
- `fjarhagsaaetlun-2026.pdf` — 2026 budget (seinni umræða 2025-11-25); 2025 column is "Áætlun m/viðaukum" NOT actuals
- `greinargerd-2026.pdf` — explanatory memo for 2026 budget; contains 2025 forecast prose (útsvar ≈ 37.5 ma.kr., fasteignagjöld ≈ 9.7 ma.kr. samtals)
- `thriggja-ara-aaetlun-2027-2029.pdf` — 3-year plan

AR25 was added to the folder 2026-04-24 and extracted to `arsreikningur-2025.txt` via pdfplumber. 2025 actuals can be sourced from there. The 2024 comparative column in AR25 matches AR24 exactly — no restatement.

Text extraction: `pdfplumber` works (installed via `pip install --user --break-system-packages pdfplumber`). Extracted `.txt` siblings already exist next to each PDF for grep-based analysis.
