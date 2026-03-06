# tests/test_db.py
import os
import tempfile
import pytest
from db import PaperDB


@pytest.fixture
def db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    paper_db = PaperDB(path)
    yield paper_db
    paper_db.close()
    os.unlink(path)


def test_is_processed_returns_false_for_new_paper(db):
    assert db.is_processed("2603.04304") is False


def test_mark_processed_and_check(db):
    db.mark_processed(
        arxiv_id="2603.04304",
        title="Test Paper",
        tags=["LLM", "inference"],
    )
    assert db.is_processed("2603.04304") is True


def test_is_processed_returns_false_for_different_id(db):
    db.mark_processed(
        arxiv_id="2603.04304",
        title="Test Paper",
        tags=["LLM"],
    )
    assert db.is_processed("2603.99999") is False


def test_duplicate_mark_processed_does_not_error(db):
    db.mark_processed(arxiv_id="2603.04304", title="Test", tags=[])
    db.mark_processed(arxiv_id="2603.04304", title="Test", tags=[])
    assert db.is_processed("2603.04304") is True


def test_get_all_processed_ids(db):
    db.mark_processed(arxiv_id="2603.00001", title="A", tags=[])
    db.mark_processed(arxiv_id="2603.00002", title="B", tags=[])
    ids = db.get_all_processed_ids()
    assert ids == {"2603.00001", "2603.00002"}
