# Paper Tracker

Automated daily paper tracking system powered by [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Fetches trending papers from HuggingFace, filters by research interest, generates structured analysis notes, and stores them in an [Obsidian](https://obsidian.md) vault.

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌───────────┐
│  HuggingFace │────▶│ Filter by    │────▶│ Deep Review  │────▶│ Obsidian  │
│  Daily Papers│     │ Interest     │     │ Each Paper   │     │ Vault     │
│  API         │     │ (Claude)     │     │ (Claude)     │     │           │
└─────────────┘     └──────────────┘     └──────────────┘     └───────────┘
     50 papers          Top 10             Structured          ~/PaperVault/
     via API          relevance           800-1200 word        Papers/
                      scoring             narrative notes      Daily/
```

Every day at 8:00 AM, the pipeline:

1. **Fetches** ~50 trending papers from the [HuggingFace Daily Papers API](https://huggingface.co/papers)
2. **Deduplicates** against a local SQLite database to skip already-processed papers
3. **Filters** the top 10 most relevant papers using Claude, scored by interest area
4. **Reviews** each selected paper — reads the full text, downloads a key figure, and writes a structured note
5. **Indexes** all reviewed papers in a daily digest note with wikilinks
6. **Records** processed papers in SQLite to avoid future duplicates

## Research Interests

The filter is configured to surface papers about:

- **LLM Inference** — optimization, serving, quantization, speculative decoding, KV cache, batching
- **Agents** — autonomous agents, tool use, planning, multi-agent systems, evaluation
- **Edge LLM** — on-device deployment, mobile inference, model compression, pruning, distillation

Edit [`skills/paper-filter/skill.md`](skills/paper-filter/skill.md) to customize interests.

## Paper Note Structure

Each paper note follows a narrative structure designed for fast comprehension:

| Section | Purpose |
|---------|---------|
| **What Problem Does This Solve?** | The problem statement |
| **Why Is This a Problem?** | Motivation and pain points of existing methods |
| **How Was This Solved Before?** | 1-3 prior approaches with limitations |
| **How Do They Solve It?** | Core insight + key mechanism (no formulas) |
| **Pros and Cons** | Strengths and weaknesses |
| **How Well Does It Work?** | 1-2 key benchmarks with specific numbers |
| **Related Work** | Wikilinks to related papers in the vault |
| **Potential Applications** | Practical use cases |

## Prerequisites

- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** — CLI installed and authenticated
- **[Obsidian](https://obsidian.md)** — for viewing the generated vault
- **Python 3.9+** — for the fetcher and database modules

## Quick Start

```bash
./install.sh
```

The install script will:

1. Check prerequisites (Claude Code, Python 3)
2. Create the Obsidian vault at `~/PaperVault/`
3. Set up Claude Code skills
4. Install a daily schedule (launchd on macOS, cron on Linux)
5. Run tests to verify everything works

Then open `~/PaperVault` as a vault in Obsidian.

### Run manually

```bash
./run_daily.sh
```

### Check logs

```bash
cat ~/PaperVault/logs/$(date +%Y-%m-%d).log
```

### Custom vault location

```bash
PAPERVAULT_DIR=~/my-vault ./install.sh
```

## Managing the Schedule

```bash
# Check status (macOS)
launchctl list | grep papertracker

# Pause
launchctl unload ~/Library/LaunchAgents/com.papertracker.daily.plist

# Resume
launchctl load ~/Library/LaunchAgents/com.papertracker.daily.plist

# Remove permanently
rm ~/Library/LaunchAgents/com.papertracker.daily.plist
```

## Project Structure

```
paper-tracker/
├── install.sh                   # One-command setup
├── run_daily.sh                 # Pipeline trigger script
├── db.py                        # SQLite dedup database
├── fetcher.py                   # HuggingFace API client
├── skills/
│   ├── daily-paper/skill.md     # Orchestration skill
│   ├── paper-filter/skill.md    # Interest-based filtering skill
│   └── paper-review/skill.md    # Paper analysis skill
└── tests/
    ├── test_db.py
    └── test_fetcher.py

~/PaperVault/                    # Obsidian vault (created by install.sh)
├── Daily/                       # Daily digest notes
├── Papers/                      # Individual paper notes
├── assets/images/               # Downloaded figures
├── logs/                        # Pipeline run logs
└── papers.db                    # SQLite database
```

## Running Tests

```bash
python3 -m pytest tests/ -v
```

## Customization

| What | Where |
|------|-------|
| Research interests & filter count | [`skills/paper-filter/skill.md`](skills/paper-filter/skill.md) |
| Note template & structure | [`skills/paper-review/skill.md`](skills/paper-review/skill.md) |
| Pipeline steps | [`skills/daily-paper/skill.md`](skills/daily-paper/skill.md) |
| Schedule time | `~/Library/LaunchAgents/com.papertracker.daily.plist` |
| Vault location | Set `PAPERVAULT_DIR` env var before running `install.sh` |

## License

MIT
