# AI Design Trends in UX for 2026 — Breon.ai

A research report website covering how AI is reshaping the UX and product design profession. Updated automatically every 30 days via GitHub Actions.

**July 2026:** redesigned as a single-page report (`index.html`) — dark/light mode, interactive charts with table views, refreshed 2026 content.

## Pages

| Page | URL |
|------|-----|
| Full report (trends, data, role evolution, sources) | `/index.html` (sections: `#trends`, `#data`, `#roles`, `#sources`) |
| Work With Me | `/work-with-me.html` |
| Legacy URLs (`/trends.html`, `/role-evolution.html`, `/sources.html`) | redirect to the matching section of `index.html` |

## 30-Day Auto-Update

Content is refreshed automatically on the **1st of each month** via GitHub Actions.

### How it works
1. GitHub Actions runs `.github/workflows/monthly-update.yml` on a cron schedule
2. It calls `update_content.py`, which uses the Claude API to re-research current trends
3. Updated stats, survey figures, and monthly highlights are written back into `index.html` via stable markers (`<!-- SURVEY_CHART_START -->`, `<!-- HIGHLIGHTS_START -->`, element IDs like `#stat-using-ai`)
4. Changes are committed and pushed automatically — GitHub Pages redeploys in ~1 minute

### Setup (one-time)

**Step 1 — Add your Anthropic API key as a GitHub secret:**
1. Go to your repo on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `ANTHROPIC_API_KEY`
5. Value: your key from console.anthropic.com

**Step 2 — Enable GitHub Pages:**
1. Go to repo Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `root`
4. Click Save

Your site will be live at: `https://YOUR-USERNAME.github.io/REPO-NAME/`

**Step 3 — Set up Formspree for email subscriptions:**
1. Sign up free at [formspree.io](https://formspree.io)
2. Create a new form — set the email to your inbox
3. Copy your form ID (looks like `xpzgkwrb`)
4. In `index.html`, replace `FORM_ID` in the form action URL with your actual ID

## Manual update

To trigger a content refresh manually:
1. Go to GitHub repo → Actions tab
2. Select "Monthly Content Refresh"
3. Click "Run workflow"

## Project

Part of [Breon.ai](https://breon.ai) — a personal AI site by Brandon Breon.
