# daily-paper

Orchestrates the full daily paper tracking pipeline.

## Trigger

Use when asked to run the daily paper pipeline.

## Pipeline

Execute these steps in order:

### Step 1: Fetch papers from HuggingFace

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from fetcher import fetch_daily_papers
from db import PaperDB
import json, os

papers = fetch_daily_papers()
db = PaperDB(os.path.expanduser('~/PaperVault/papers.db'))
processed = db.get_all_processed_ids()
db.close()

candidates = [
    {'arxiv_id': p.arxiv_id, 'title': p.title, 'summary': p.summary,
     'ai_keywords': p.ai_keywords, 'upvotes': p.upvotes,
     'github_repo': p.github_repo, 'authors': p.authors}
    for p in papers if p.arxiv_id not in processed
]
print(json.dumps(candidates))
" > /tmp/paper_candidates.json
```

If the output is `[]` or empty, announce "No new papers today" and stop.

### Step 2: Filter papers

Read `/tmp/paper_candidates.json` and apply the paper-filter skill logic:
- Score each paper 0-10 on relevance to interest areas (LLM inference, Agent, Edge LLM)
- Select top 10 papers with score >= 5

If no papers pass the filter, announce "No relevant papers today" and stop.

### Step 3: Review each selected paper

For each selected paper, apply the paper-review skill logic:
1. Fetch ar5iv HTML (fallback to PDF)
2. Analyze the paper
3. Download ONE key figure to `~/PaperVault/assets/images/{arxiv_id}/`
4. Generate the structured Markdown note
5. Write the note to `~/PaperVault/Papers/{sanitized_title}.md`

### Step 4: Create daily index

Create `~/PaperVault/Daily/{YYYY-MM-DD}.md`:

```markdown
---
date: {YYYY-MM-DD}
---
# {YYYY-MM-DD} Paper Digest

1. [[Paper Title 1]] - {one-line summary}
2. [[Paper Title 2]] - {one-line summary}
...
```

### Step 5: Record in database

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from db import PaperDB
import os
db = PaperDB(os.path.expanduser('~/PaperVault/papers.db'))
db.mark_processed(arxiv_id='{id}', title='{title}', tags={tags})
db.close()
"
```

### Step 6: Summary

Print a summary:
- Number of candidates fetched
- Number that passed filter
- Titles of reviewed papers
- Any errors encountered

## Important Notes

- ALWAYS check SQLite for duplicates before processing
- Sanitize paper titles for filenames: remove special characters, limit length
- If ar5iv HTML fetch fails, fall back to PDF
- If a paper fails to process, skip it and continue with the rest
