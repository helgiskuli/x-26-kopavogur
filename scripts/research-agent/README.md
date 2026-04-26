# Kópavogur Research Heartbeat

Autonomous agent that monitors political news about Kópavogur municipal
elections (sveitarstjórnarkosningar 16. maí 2026) and opens PRs when new
content is found.

## Architecture

```
GitHub Actions cron (2×/day)
  → scripts/research_agent.py
    → Gemini 3 Flash Preview + Google Search grounding
    → compares against _data/tracked_updates.json
    → opens PR if new content detected
```

## Cost

**Free.** Uses the Gemini API free tier via Google AI Studio.

- Gemini 3 Flash Preview: 5,000 grounded search queries/month free
- Agent usage: ~120 queries/month (2 runs/day × ~3 queries × 20 days)
- No credit card required

## Why Gemini 3 Flash

Gemini 3 Flash Preview ranks **#4 on Miðeind's Icelandic LLM Leaderboard**
(85.97% average), ahead of GPT-5.4 and Claude Opus 4.6 on Icelandic
benchmarks. It's the best free option for Icelandic language work.

Leaderboard: https://huggingface.co/spaces/mideind/icelandic-llm-leaderboard

## Setup

### 1. Get a Gemini API key (2 minutes)

1. Go to https://aistudio.google.com/apikey
2. Sign in with any Google account
3. Click "Create API key"
4. Copy the key

### 2. Add the key to the repo (1 minute)

1. Repo → Settings → Secrets and variables → Actions
2. New repository secret: `GEMINI_API_KEY` = your key

### 3. Enable Actions write permissions (1 minute)

1. Settings → Actions → General
2. Workflow permissions → "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"
4. Save

### 4. Test

Actions → "Kópavogur Political Research Heartbeat" → Run workflow

## Files

| File | Purpose |
|------|---------|
| `scripts/research-agent/research_agent.py` | Main agent script |
| `scripts/research-agent/README.md` | This file |
| `.github/workflows/research-heartbeat.yml` | Cron schedule and CI |
| `_data/tracked_updates.json` | Persistent state (dedup + gap tracking) |
| `_data/latest_digest.md` | PR body content for latest run |
| `_updates/YYYY-MM-DD.md` | Daily update files (site-facing) |

## How it works

1. **Search 1:** Searches Icelandic news (RÚV, Vísir, MBL, DV) for
   Kópavogur election coverage
2. **Search 2:** Checks party homepages for new policy documents
3. **Dedup:** Compares findings against `_data/tracked_updates.json`
4. **Gap tracking:** Watches for parties filling known policy gaps and
   flags them with 🆕. Gaps auto-close when filled.
5. **PR:** Creates a branch and PR with a markdown digest

## Policy gap tracking

The agent tracks which parties haven't published positions in which policy
areas (based on the site's policy matrix). When a gap is filled, it's
automatically removed from `_data/tracked_updates.json`. You can also
manually edit the `gaps` object in that file.

Initial gaps (as of April 2026):
- Viðreisn (C): húsnæði, velferð, stjórnsýsla
- Miðflokkurinn (M): húsnæði, velferð, stjórnsýsla, samgöngur
- VG og óháð (V): velferð, stjórnsýsla
- Samfylkingin (S): velferð, stjórnsýsla

## Customization

- **Frequency:** Edit cron in the workflow. Default: `0 8,18 * * *` (8am/6pm UTC)
- **Model:** Change `MODEL` in the script. `gemini-2.5-flash` also works (ranked #16)
- **Stop date:** Disable or delete the workflow after May 16, 2026

## What to do with PRs

The agent finds raw material. You decide:
- Is this genuinely new?
- Does it warrant updating a site page?
- Which page and section does it belong on?

The PR provides findings. You do the editorial work.