# paper-review

Deep analysis of a single academic paper, producing a structured Obsidian note.

## Trigger

Use when given an arXiv paper URL or ID to analyze.

## Instructions

1. Fetch the paper content:
   - First try ar5iv HTML: `https://ar5iv.labs.arxiv.org/html/{arxiv_id}`
   - If unavailable, fall back to PDF: `https://arxiv.org/pdf/{arxiv_id}`
2. Read and analyze the full paper
3. Download ONE key figure (architecture diagram or core method illustration) to `~/PaperVault/assets/images/{arxiv_id}/fig1.png` using Bash (curl/wget). Skip if no informative figure exists.
4. Generate a structured Markdown note following the template below

## Output Template

The output MUST be a complete Markdown file with this exact structure. Target 800-1200 words total.

```markdown
---
arxiv_id: "{arxiv_id}"
title: "{title}"
authors: [{authors}]
date: {today's date YYYY-MM-DD}
tags: [{relevant tags}]
status: unread
url: "https://arxiv.org/abs/{arxiv_id}"
github: "{github_url or empty}"
---

## What Problem Does This Solve?

{What problem does this paper address? 2-3 sentences.}

## Why Is This a Problem?

{Why are existing methods insufficient? What's the pain point? 2-3 sentences on motivation.}

## How Was This Solved Before?

{What are the mainstream prior approaches? List 1-3, one sentence each on their idea and limitation.}

## How Do They Solve It?

{Core insight in one sentence + key mechanism explaining how it works. No formulas. 1-2 paragraphs.}

![[assets/images/{arxiv_id}/fig1.png]]
*{Figure description}*

## Pros and Cons

{2-3 pros, 1-2 cons, concise bullet points}

## How Well Does It Work?

{Pick 1-2 most representative benchmarks, give specific numbers and baseline comparison.}

## Related Work

- [[Paper Title]] - {how it relates}

## Potential Applications

- {Practical application scenarios}

## Code Repository

{GitHub link if available, or "Not available"}
```

## Key Rules

- Write everything in English
- Target 800-1200 words total — tell a story, not a laundry list
- Only download ONE key figure (architecture or core method diagram), skip filler
- For "How Do They Solve It": focus on core insight + key mechanism (how it works), NO formulas or pseudocode
- For "How Well Does It Work": pick 1-2 most representative benchmarks with specific numbers, not exhaustive listing
- For Related Work, search ~/PaperVault/Papers/ for existing notes and use [[wikilinks]] to link
- Tags should be lowercase, hyphenated (e.g., llm-inference, speculative-decoding, multi-agent)
