# fetcher.py
from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass, field

HF_API_URL = "https://huggingface.co/api/daily_papers"


@dataclass
class Paper:
    arxiv_id: str
    title: str
    summary: str
    authors: list[str]
    upvotes: int
    published_at: str
    ai_keywords: list[str] = field(default_factory=list)
    ai_summary: str = ""
    github_repo: str | None = None

    @property
    def arxiv_url(self) -> str:
        return f"https://arxiv.org/abs/{self.arxiv_id}"

    @property
    def ar5iv_url(self) -> str:
        return f"https://ar5iv.labs.arxiv.org/html/{self.arxiv_id}"

    @property
    def pdf_url(self) -> str:
        return f"https://arxiv.org/pdf/{self.arxiv_id}"


def fetch_daily_papers() -> list[Paper]:
    with urllib.request.urlopen(HF_API_URL) as resp:
        data = json.loads(resp.read())

    papers = []
    for entry in data:
        p = entry["paper"]
        papers.append(Paper(
            arxiv_id=p["id"],
            title=p["title"],
            summary=p.get("summary", ""),
            authors=[a["name"] for a in p.get("authors", [])],
            upvotes=p.get("upvotes", 0),
            published_at=p.get("publishedAt", ""),
            ai_keywords=p.get("ai_keywords", []),
            ai_summary=p.get("ai_summary", ""),
            github_repo=p.get("githubRepo"),
        ))
    return papers
