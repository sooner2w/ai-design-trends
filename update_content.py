"""
Monthly content refresh script for Breon.ai AI Design Trends site.
Called by GitHub Actions on the 1st of each month.
Requires: ANTHROPIC_API_KEY environment variable.

Targets the single-page index.html (redesign, July 2026). Stable hooks:
  - #updated-stamp / #footer-updated  — date stamps
  - #stat-using-ai, #stat-ai-fluency, #stat-agent-apps, #stat-job-growth — KPI tiles
  - <!-- SURVEY_CHART_START/END -->   — horizontal bar chart rows
  - <!-- SURVEY_TABLE_START/END -->   — the chart's table-view rows
  - #survey-note                      — one-line note under the chart
  - <!-- HIGHLIGHTS_START/END -->     — "what changed this month" card
"""

import os
import json
import re
from datetime import datetime, timedelta
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

CURRENT_MONTH = datetime.now().strftime("%B %Y")
NEXT_MONTH    = (datetime.now().replace(day=1) + timedelta(days=32)).strftime("%B %Y")
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")


def research_trends() -> dict:
    """Ask Claude to research current AI design trends and return structured data."""
    print(f"[{CURRENT_MONTH}] Researching latest AI design trends...")

    prompt = f"""You are a design industry researcher. Today is {CURRENT_MONTH}.

Research and return the most current data on how AI is reshaping UX and product design.

Return your findings as a JSON object with this exact structure:
{{
  "last_updated": "{CURRENT_MONTH}",
  "next_update": "{NEXT_MONTH}",
  "hero_stats": {{
    "using_ai": 94,
    "ai_fluency_req": 73,
    "agent_apps_pct": 40,
    "job_growth_pct": 16
  }},
  "survey_stats": [
    {{"label": "Use generative AI in their workflow", "pct": 94}},
    {{"label": "Say AI boosts their efficiency", "pct": 78}},
    {{"label": "Hiring managers requiring AI fluency", "pct": 73}},
    {{"label": "Cite unreliable output as top blocker", "pct": 62}},
    {{"label": "Use AI for wireframing", "pct": 58}}
  ],
  "survey_note": "One short sentence of context for the survey chart.",
  "monthly_highlights": [
    "One key development or change this month (1-2 sentences)",
    "Another notable update (1-2 sentences)"
  ]
}}

Field meanings:
- hero_stats.using_ai: % of designers using generative AI tools
- hero_stats.ai_fluency_req: % of hiring managers requiring AI fluency
- hero_stats.agent_apps_pct: % of enterprise apps expected to ship task-specific AI agents this year
- hero_stats.job_growth_pct: projected UX role growth (currently through 2034)
- survey_stats: exactly 5 rows, each a survey measure with an integer percentage,
  ordered largest to smallest

Update any numbers that have changed based on newly published research.
Add to monthly_highlights any notable AI+design news from this month.
Keep JSON valid — no trailing commas, no comments."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in Claude response:\n{raw}")

    data = json.loads(match.group())
    print(f"Research complete. {len(data.get('monthly_highlights', []))} highlights found.")
    return data


def read_index() -> str:
    with open(INDEX) as f:
        return f.read()


def write_index(html: str):
    with open(INDEX, "w") as f:
        f.write(html)


def esc(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def replace_between(html: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.DOTALL)
    if not pattern.search(html):
        print(f"WARNING: markers {start} .. {end} not found — skipped")
        return html
    return pattern.sub(start + "\n" + body + "\n" + end, html)


def update_dates(html: str, data: dict) -> str:
    html = re.sub(
        r'(<span class="stamp" id="updated-stamp">)Last updated [^·<]+· Next update [^·<]+·',
        rf'\g<1>Last updated {data["last_updated"]} · Next update {data["next_update"]} ·',
        html
    )
    html = re.sub(
        r'(<span id="footer-updated">)Updated [^·<]+·',
        rf'\g<1>Updated {data["last_updated"]} ·',
        html
    )
    print("Updated date stamps")
    return html


def update_hero_stats(html: str, data: dict) -> str:
    s = data["hero_stats"]
    subs = [
        ('stat-using-ai',   f'{s["using_ai"]}%'),
        ('stat-ai-fluency', f'{s["ai_fluency_req"]}%'),
        ('stat-agent-apps', f'{s["agent_apps_pct"]}%'),
    ]
    for el_id, value in subs:
        html = re.sub(
            rf'(<div class="value" id="{el_id}">)[^<]*(</div>)',
            rf'\g<1>{value}\g<2>',
            html
        )
    html = re.sub(
        r'(<div class="value" id="stat-job-growth">)[^<]*(<span class="delta">)',
        rf'\g<1>{s["job_growth_pct"]}%\g<2>',
        html
    )
    print("Updated hero KPI tiles")
    return html


def build_survey_rows(survey_stats: list) -> str:
    rows = []
    for item in survey_stats:
        label = esc(item["label"])
        pct = int(item["pct"])
        rows.append(
            f'''          <div class="hbar-row">
            <span class="cat">{label}</span>
            <div class="hbar-track"><div class="hbar" style="width:0" data-w="{pct}%" tabindex="0" role="img" aria-label="{label}: {pct} percent" data-tip-value="{pct}%" data-tip-label="{label}"><span class="hbar-val">{pct}%</span></div></div>
          </div>'''
        )
    return "\n".join(rows)


def build_survey_table(survey_stats: list) -> str:
    return "\n".join(
        f'                <tr><td>{esc(i["label"])}</td><td class="num">{int(i["pct"])}%</td></tr>'
        for i in survey_stats
    )


def update_survey_chart(html: str, data: dict) -> str:
    stats = data.get("survey_stats") or []
    if len(stats) != 5:
        print(f"WARNING: expected 5 survey_stats, got {len(stats)} — chart left unchanged")
        return html
    html = replace_between(html, "<!-- SURVEY_CHART_START -->", "<!-- SURVEY_CHART_END -->",
                           build_survey_rows(stats))
    html = replace_between(html, "<!-- SURVEY_TABLE_START -->", "<!-- SURVEY_TABLE_END -->",
                           build_survey_table(stats))
    note = data.get("survey_note")
    if note:
        html = re.sub(
            r'(<p class="axis-note" id="survey-note">)[^<]*(</p>)',
            rf'\g<1>{esc(note)}\g<2>',
            html
        )
    print("Updated survey chart, table view, and note")
    return html


def update_highlights(html: str, data: dict) -> str:
    highlights = data.get("monthly_highlights", [])
    if not highlights:
        return html
    items = "\n".join(f"        <li>{esc(h)}</li>" for h in highlights)
    card = f'''    <div class="highlights">
      <p class="hl-kicker">What changed this month · {esc(data["last_updated"])}</p>
      <ul>
{items}
      </ul>
    </div>'''
    html = replace_between(html, "<!-- HIGHLIGHTS_START -->", "<!-- HIGHLIGHTS_END -->", card)
    print(f"Injected {len(highlights)} monthly highlight(s)")
    return html


def main():
    print("=" * 50)
    print(f"Breon.ai Monthly Content Refresh — {CURRENT_MONTH}")
    print("=" * 50)

    data = research_trends()

    html = read_index()
    html = update_dates(html, data)
    html = update_hero_stats(html, data)
    html = update_survey_chart(html, data)
    html = update_highlights(html, data)
    write_index(html)

    print("=" * 50)
    print("Refresh complete. Changes staged for commit.")
    print("=" * 50)


if __name__ == "__main__":
    main()
