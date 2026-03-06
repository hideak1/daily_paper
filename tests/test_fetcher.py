# tests/test_fetcher.py
import json
import pytest
from unittest.mock import patch, MagicMock
from fetcher import fetch_daily_papers, Paper


MOCK_API_RESPONSE = [
    {
        "paper": {
            "id": "2603.04304",
            "title": "Test Paper 1",
            "summary": "A paper about LLM inference optimization.",
            "authors": [{"name": "Alice"}, {"name": "Bob"}],
            "upvotes": 42,
            "publishedAt": "2026-03-04T17:22:16.000Z",
            "ai_keywords": ["LLM", "inference"],
            "ai_summary": "This paper optimizes LLM inference.",
            "githubRepo": "https://github.com/test/repo",
        }
    },
    {
        "paper": {
            "id": "2603.04305",
            "title": "Test Paper 2",
            "summary": "A paper about computer vision.",
            "authors": [{"name": "Charlie"}],
            "upvotes": 10,
            "publishedAt": "2026-03-04T18:00:00.000Z",
            "ai_keywords": ["vision", "CNN"],
            "ai_summary": "A vision paper.",
            "githubRepo": None,
        }
    },
]


def test_fetch_returns_paper_objects():
    with patch("fetcher.urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(MOCK_API_RESPONSE).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        papers = fetch_daily_papers()
        assert len(papers) == 2
        assert isinstance(papers[0], Paper)


def test_paper_fields_populated():
    with patch("fetcher.urllib.request.urlopen") as mock_urlopen:
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(MOCK_API_RESPONSE).encode()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_resp

        papers = fetch_daily_papers()
        p = papers[0]
        assert p.arxiv_id == "2603.04304"
        assert p.title == "Test Paper 1"
        assert p.authors == ["Alice", "Bob"]
        assert p.upvotes == 42
        assert p.github_repo == "https://github.com/test/repo"
        assert "LLM" in p.ai_keywords
