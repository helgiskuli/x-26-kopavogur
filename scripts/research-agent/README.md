# Kópavogur Research Heartbeat

Autonomous agent that monitors political news about Kópavogur municipal
elections (sveitarstjórnarkosningar 16. maí 2026) and opens PRs when new
content is found.

## Architecture

```
GitHub Actions cron (2×/day, 09:00 and 18:00 UTC)
  → scripts/research-agent/research_agent.py
    → Gemini 2.5 Flash + Google Search grounding
    → compares against _data/tracked_updates.json
    → opens PR if new content detected
```

## Cost

**Free.** Uses the Gemini API free tier via Google AI Studio.

- Gemini 2.5 Flash: 1,500 grounded search queries/day free (15 RPM)
- Agent usage: ~2 queries/run × 2 runs/day × 20 days = ~80 queries/month
- No credit card required

## Why Gemini 2.5 Flash

Gemini 2.5 Flash ranks near the top of Miðeind's Icelandic LLM Leaderboard
and is the best free option for Icelandic language work with built-in
Google Search grounding.

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

### 4. Test via GitHub UI

Actions → "Kópavogur Political Research Heartbeat" → Run workflow

## Local development

Dependencies are managed with [uv](https://docs.astral.sh/uv/).

```bash
# Install uv if needed
brew install uv

# From repo root — generate lockfile (once, then commit it)
cd scripts/research-agent && uv lock && cd ../..

# Store your API key in the repo root (already gitignored)
echo 'GEMINI_API_KEY=your_key_here' > .env

# Run from the script directory
cd scripts/research-agent

# Preview prompts without making API calls
uv run python research_agent.py --dry-run

# Full local run (loads .env automatically, writes to _data/ and _updates/)
uv run python research_agent.py

# Use a non-default .env path
uv run python research_agent.py --env-file /path/to/.env
```

`--dry-run` never calls the API — it just prints both prompts to stdout. Useful
for tuning prompt wording without spending quota.

## Files

| File | Purpose |
|------|---------|
| `scripts/research-agent/research_agent.py` | Main agent script |
| `scripts/research-agent/pyproject.toml` | uv project + dependency declaration |
| `scripts/research-agent/uv.lock` | Pinned lockfile — commit this |
| `scripts/research-agent/README.md` | This file |
| `.github/workflows/research-heartbeat.yml` | Cron schedule and CI |
| `_data/tracked_updates.json` | Persistent state: all updates with `applied_date` tracking and `gaps` object |
| `_data/latest_digest.md` | Canonical skill input: unapplied items only, with frontmatter (`date`, `count_total`, `count_unapplied`) |
| `_data/pr_body.md` | PR body: new items from the current run only, no frontmatter |
| `_updates/YYYY-MM-DD.md` | Transactional archive: every item found on that date, appended across runs |

## How it works

1. **Search 1:** Party homepages — new policy documents, candidate announcements (slow-moving; runs first so it always completes)
2. **Search 2:** News articles + debates, interviews, radio/TV appearances, and events (merged into one call to reduce burst pressure on shared CI IPs)
3. **Dedup:** Compares findings against `_data/tracked_updates.json`
4. **URL verification:** Every new `source_url` is HTTP-checked before being written to state:
   - **404** → entry is dropped silently (hallucinated or dead link)
   - **403 / 5xx / timeout** → entry kept but flagged with `url_unverified: true` (some sites block automated requests)
   - **200** → kept as-is
   - First-party sites (`xdkop.is`, `kopavogur.is`) are trusted and skip the check
5. **Gap tracking:** Watches for parties filling known policy gaps and
   flags them with 🆕. Gaps auto-close when filled.
6. **PR:** Creates a branch and PR with a markdown digest

After the agent writes state, the CI step **Verify source URLs in queue** runs `scripts/verify-urls.py` against all unapplied entries as a second-pass audit. It uses `continue-on-error: true` so PR creation still proceeds, but any failures are visible in the Actions log.

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

- **Frequency:** Edit `cron` in the workflow. Default: `0 9,18 * * *` (9am and 6pm UTC)
- **Model:** Change `MODEL` in the script. Currently `gemini-2.5-flash`
- **Stop date:** Disable or delete the workflow after May 16, 2026

## What to do with PRs

Merge the PR to pull `_data/latest_digest.md` and `_data/tracked_updates.json`
into `main`, then run `/kopavogur-updates` in a Claude Code session. The skill
reads the digest, filters what's actionable, makes targeted HTML edits, and
marks applied items in `tracked_updates.json` with `applied_date`.
