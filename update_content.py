"""
Monthly content refresh script for Breon.ai AI Design Trends site.
Called by GitHub Actions on the 1st of each month.
Requires: ANTHROPIC_API_KEY environment variable.
"""

import os
import json
import re
from datetime import datetime, timedelta
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

CURRENT_MONTH = datetime.now().strftime("%B %Y")
NEXT_MONTH    = (datetime.now().replace(day=1) + timedelta(days=32)).strftime("%B %Y")


def research_trends() -> dict:
    """Ask Claude to research current AI design trends and return structured data."""
    print(f"[{CURRENT_MONTH}] Researching latest AI design trends...")

    prompt = f"""You are a design industry researcher. Today is {CURRENT_MONTH}.

Research and return the most current data on these topics for UX and product designers:
1. AI design tool adoption rates (percentage of designers using each tool)
2. Task time savings with AI (wireframing, prototyping, research, assets, handoff)
3. Key emerging trends in AI + UX design this month
4. New tools or major tool updates released this month
5. Updated statistics on UX job market and AI impact
6. Any new regulations or industry standards relevant to ethical AI design

Return your findings as a JSON object with this exact structure:
{{
  "last_updated": "{CURRENT_MONTH}",
  "next_update": "{NEXT_MONTH}",
  "tool_adoption": [
    {{"tool": "ChatGPT / LLMs", "pct": 93}},
    {{"tool": "Figma AI / Make", "pct": 78}},
    {{"tool": "Midjourney / DALL-E", "pct": 61}},
    {{"tool": "Adobe Firefly", "pct": 54}},
    {{"tool": "GitHub Copilot", "pct": 42}},
    {{"tool": "Google Stitch", "pct": 38}},
    {{"tool": "UX Pilot / Flowstep", "pct": 29}},
    {{"tool": "Runway (video AI)", "pct": 22}}
  ],
  "hero_stats": {{
    "using_ai": 93,
    "say_collab_impactful": 73,
    "job_growth_pct": 16,
    "distrust_ai_output": 40
  }},
  "task_times": [
    {{"task": "Wireframing", "before_h": 4.0, "after_h": 0.75}},
    {{"task": "Research Synthesis", "before_h": 6.0, "after_h": 2.0}},
    {{"task": "Asset Creation", "before_h": 3.5, "after_h": 0.5}},
    {{"task": "Prototyping", "before_h": 5.0, "after_h": 1.5}},
    {{"task": "Handoff Docs", "before_h": 2.5, "after_h": 0.75}}
  ],
  "monthly_highlights": [
    "One key development or change this month (1-2 sentences)",
    "Another notable update (1-2 sentences)"
  ],
  "new_sources": []
}}

Update any numbers that have changed based on newly published research.
Add to monthly_highlights any notable AI+design news from this month.
Keep JSON valid — no trailing commas, no comments."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    # Extract JSON from the response
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in Claude response:\n{raw}")

    data = json.loads(match.group())
    print(f"Research complete. {len(data.get('monthly_highlights', []))} highlights found.")
    return data


def pct_to_width(pct: int) -> int:
    """Convert percentage to CSS width percentage (max 100)."""
    return min(int(pct), 100)


def hours_to_width(hours: float, max_hours: float = 6.0) -> int:
    """Convert hours to percentage of max for bar chart."""
    return min(int((hours / max_hours) * 100), 100)


def build_hbar_html(tool_adoption: list) -> str:
    rows = []
    for item in tool_adoption:
        tool = item["tool"]
        pct  = item["pct"]
        css_class = "hbar-fill" if pct >= 50 else "hbar-fill dim"
        rows.append(f"""      <div class="hbar-row">
        <span class="hbar-label">{tool}</span>
        <div class="hbar-track"><div class="{css_class}" style="width:{pct_to_width(pct)}%"></div></div>
        <span class="hbar-val">{pct}%</span>
      </div>""")
    return "\n".join(rows)


def build_cbar_html(task_times: list) -> str:
    max_h = max(t["before_h"] for t in task_times)
    rows = []
    for item in task_times:
        task     = item["task"]
        before_h = item["before_h"]
        after_h  = item["after_h"]
        before_w = hours_to_width(before_h, max_h)
        after_w  = hours_to_width(after_h, max_h)
        before_label = f"{int(before_h)}h" if before_h == int(before_h) else f"{before_h}h"
        after_label  = f"{int(after_h)}h"  if after_h  == int(after_h)  else f"{after_h}h"
        rows.append(f"""        <div>
          <p class="cbar-group-label">{task}</p>
          <div class="cbar-row"><span class="cbar-year">2024</span><div class="cbar-track"><div class="cbar-fill-24" style="width:{before_w}%"></div></div><span class="cbar-val">{before_label}</span></div>
          <div class="cbar-row"><span class="cbar-year">2026</span><div class="cbar-track"><div class="cbar-fill-26" style="width:{after_w}%"></div></div><span class="cbar-val">{after_label}</span></div>
        </div>""")
    return "\n".join(rows)


def update_html_file(path: str, replacements: dict):
    """Apply regex-based replacements to an HTML file."""
    with open(path, "r") as f:
        content = f.read()
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(path, "w") as f:
        f.write(content)
    print(f"Updated: {path}")


def update_footer_dates(data: dict):
    """Update 'Last updated' and 'Next update' in all HTML footers."""
    footer_pattern = r'Last updated:.*?Next update:.*?(?=&nbsp;·&nbsp;)'
    footer_replace = f'Last updated: {data["last_updated"]} &nbsp;·&nbsp; Next update: {data["next_update"]} '

    for fname in ["index.html", "trends.html", "role-evolution.html", "sources.html"]:
        path = os.path.join(os.path.dirname(__file__), fname)
        if os.path.exists(path):
            with open(path) as f:
                html = f.read()
            html = re.sub(footer_pattern, footer_replace, html)
            with open(path, "w") as f:
                f.write(html)


def update_hero_stats(data: dict):
    """Update the 4 hero stat cards on index.html."""
    s = data["hero_stats"]
    path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(path) as f:
        html = f.read()

    # Replace stat numbers using surrounding context
    html = re.sub(
        r'(<span class="stat-num">)\d+(%</span>\s*<span class="stat-label">of designers already use)',
        rf'\g<1>{s["using_ai"]}%</span>\n      <span class="stat-label">of designers already use',
        html
    )
    html = re.sub(
        r'(<span class="stat-num">)\d+(%</span>\s*<span class="stat-label">say AI collaboration)',
        rf'\g<1>{s["say_collab_impactful"]}%</span>\n      <span class="stat-label">say AI collaboration',
        html
    )
    html = re.sub(
        r'(<span class="stat-num">)\d+(%</span>\s*<span class="stat-label">projected growth)',
        rf'\g<1>{s["job_growth_pct"]}%</span>\n      <span class="stat-label">projected growth',
        html
    )
    html = re.sub(
        r'(<span class="stat-num">)\d+(%</span>\s*<span class="stat-label">don)',
        rf'\g<1>{s["distrust_ai_output"]}%</span>\n      <span class="stat-label">don',
        html
    )

    with open(path, "w") as f:
        f.write(html)
    print("Updated hero stats on index.html")


def update_tool_adoption_chart(data: dict):
    """Replace the hbar rows in the trends page tool adoption chart."""
    hbar_html = build_hbar_html(data["tool_adoption"])
    path = os.path.join(os.path.dirname(__file__), "trends.html")
    with open(path) as f:
        html = f.read()

    html = re.sub(
        r'(<div class="hbar">\s*).*?(\s*</div>\s*<div class="chart-legend">)',
        rf'\g<1>\n{hbar_html}\n    \g<2>',
        html,
        flags=re.DOTALL
    )
    with open(path, "w") as f:
        f.write(html)
    print("Updated tool adoption chart in trends.html")


def update_task_times_chart(data: dict):
    """Replace the cbar content in trends.html."""
    cbar_html = build_cbar_html(data["task_times"])
    path = os.path.join(os.path.dirname(__file__), "trends.html")
    with open(path) as f:
        html = f.read()

    html = re.sub(
        r'(<div class="cbar">\s*).*?(\s*</div>\s*<div class="chart-legend">.*?Task Time)',
        rf'\g<1>\n{cbar_html}\n      \g<2>',
        html,
        flags=re.DOTALL
    )
    with open(path, "w") as f:
        f.write(html)
    print("Updated task time chart in trends.html")


def inject_monthly_highlights(data: dict):
    """Add monthly highlights callout near the top of index.html if highlights exist."""
    highlights = data.get("monthly_highlights", [])
    if not highlights:
        return

    items = "".join(f"<li>{h}</li>" for h in highlights)
    callout = f"""
  <!-- Monthly highlights injected by update_content.py -->
  <div style="background:#F0FDF4;border-left:4px solid #10B981;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:28px;">
    <p style="font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#065F46;margin-bottom:8px;">What changed this month ({data['last_updated']})</p>
    <ul style="list-style:none;padding:0;margin:0;">{items}</ul>
  </div>
"""
    path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(path) as f:
        html = f.read()

    # Insert before exec summary
    html = re.sub(
        r'(<!-- Monthly highlights.*?-->\s*<div[^>]*>.*?</div>\s*)?(<ol class="exec-list">)',
        callout + r'\2',
        html,
        flags=re.DOTALL
    )
    with open(path, "w") as f:
        f.write(html)
    print(f"Injected {len(highlights)} monthly highlight(s) into index.html")


def main():
    print("=" * 50)
    print(f"Breon.ai Monthly Content Refresh — {CURRENT_MONTH}")
    print("=" * 50)

    data = research_trends()

    update_footer_dates(data)
    update_hero_stats(data)
    update_tool_adoption_chart(data)
    update_task_times_chart(data)
    inject_monthly_highlights(data)

    print("=" * 50)
    print("Refresh complete. Changes staged for commit.")
    print("=" * 50)


if __name__ == "__main__":
    main()
