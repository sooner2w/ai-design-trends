# Monthly refresh instructions

Followed by the scheduled cloud agent on the 1st of each month, and by any human or
Claude session doing the refresh by hand.

## Purpose — this governs every judgement call

This site is a **credibility artefact for its author's job search** as a product
designer working in AI. A hiring manager may click any citation on the page.

Therefore: **source quality matters more than volume of content, and an
unsourceable stat is worse than no stat.** When in doubt, cut the number.

## Structure

- **`index.html` is the entire report.** Single page.
- **Every other `.html` file is legacy — do not edit them.**
- **Do not run `update_content.py`.** It is stale and generates unsourced content.
- Content markers inside `index.html`:
  `HIGHLIGHTS_START/END`, `SURVEY_CHART_START/END`, `SURVEY_TABLE_START/END`
- Date strings live in six places: `<title>`, the meta description, `.eyebrow`,
  `#updated-stamp`, `.hl-kicker`, `#footer-updated`.

## Tasks

### 1. Roll the date

Get the current month and year from the system date. Update all six date locations.
Set "Next update" to the following month. **The month must be unmistakable in all
six places** — the author has been explicit about this.

### 2. Rewrite "What changed this month"

Research what genuinely changed in AI and design/UX over the last ~30 days using
web search. Replace the list between `HIGHLIGHTS_START/END` with **2–4 items**.

Each item must be:
- A real, datable development — a named report, a shipped product capability, a
  regulatory change — with a specific figure or date attached.
- Written for a senior design audience: **what it means for designers**, not a
  press-release summary.

No vague filler ("AI continues to transform design"). If only two things really
happened, write two items.

### 3. Audit every number on the page

For each figure in the KPI tiles, trend-card signals, charts and tables: find the
primary source and confirm the number. If a figure cannot be traced to a primary
source, **replace or remove it** — do not leave it because it looks good.

Keep the KPI tiles, chart and table internally consistent. A number appearing in
two places must match.

### 4. Sources

The sources list must contain **primary sources only**:
- First-party research reports (Figma/NewtonX, Autodesk, Nielsen Norman Group)
- Named analyst firms citing their own research (Gartner)
- Academic and institutional research that publishes its methodology (e.g. the Figma
  randomised trial on arXiv) — not preliminary findings that withhold their data
- Government statistics (US BLS)
- Official regulatory texts (EUR-Lex)

**Banned — never reintroduce these.** SEO statistics aggregators and content farms:
gitnux, mockflow, branex, zeeframes, stan.vision, fuselabcreative, and anything of
that kind. They were the origin of three wrong headline stats found in the
September 2026 audit. **Never cite research.breon.ai itself** — the report citing
itself was a real defect on the page.

Update the source count in `#updated-stamp` to match the actual number of entries.

### 5. Verify, commit, push

- Check no stale month name survives anywhere in `index.html`.
- Check the HTML is well-formed and no markers were destroyed.
- Commit with a message summarising content changes AND any stat corrections made.
- Push to `main`. GitHub Pages deploys automatically; allow 1–3 minutes.
- Confirm live with a cache-busted fetch of `https://research.breon.ai/`.

## Context worth knowing

- The market-size chart ($1.2B 2023 → $15.7B 2030) is a **third-party projection,
  not primary research**, and is labelled as such on the page. Keep that caveat.
- The September 2026 audit corrected: designer genAI adoption 95%/94% → **72%**
  (Figma *State of the Designer 2026*, NewtonX, n=906); "16% UX role growth through
  2034" → BLS actually reports **7.5%** for 2024–34; and removed two unverifiable
  claims ("75% of hiring managers require AI fluency", "2,000+ AI liability claims").
- The **October 2026 audit** corrected: the Gartner "30% of new apps adaptive by end of
  2026" signal had **no primary Gartner source** and was replaced with the traceable
  "more than 20% of digital workplace apps by 2028" press release; "35% faster
  prototyping with AI tools" was **not what the research said** — the 35% is the gain
  product *managers* got in Figma's randomised trial, while designers showed no
  significant aggregate saving, so the signal now reports the 26% interaction-prototype
  figure; "56% of open UX roles are senior, only 25% junior" was untraceable and was
  removed; BLS has **re-based its projection to 5% for 2025–35** (was 7.5% for 2024–34);
  and the Figma 72% and 91% figures were **mislabelled** — 72% is "use generative AI",
  not daily use, and 91% covers quality of output only, not "quality and speed".
- **MIT Project NANDA was dropped in October 2026.** Its official PDF
  (`nanda.media.mit.edu/ai_report_2025.pdf`) now redirects to the group overview page,
  the report self-describes as preliminary and non-peer-reviewed, and the 95% figure is
  under active methodological criticism including calls for retraction. Do not
  reintroduce the 95% pilot-failure stat without a retrievable primary source. The old
  `mlq.ai` mirror is dead (404) — never cite mirrors for it.
- Two independent surveys now cover designer adoption and must not be conflated:
  **Figma / NewtonX** (n=906) gives 72% using generative AI plus the sentiment figures;
  **Designer Fund / Foundation Capital** (n=900+) gives the daily/weekly split (75% / 91%).
  Both report a 91% — Figma's is output quality, Designer Fund's is weekly use. Keep a
  bare second 91% out of the tiles, signals and axis note so the two never collide.
- Do not add any reference to Side B Studio or sideb.studio. The two properties are
  deliberately kept separate.
