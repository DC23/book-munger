from pathlib import Path

import pytest

from book_munger.reporters.html import render

COUNTS = {
    "NOUN": {"sea": 42, "night": 31, "hand": 19},
    "VERB": {"sail": 17, "swim": 9, "walk": 5},
}
RANKED = {
    "NOUN": ["sea", "night", "hand"],
    "VERB": ["sail", "swim", "walk"],
}


def test_creates_output_file(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out)
    assert out.exists()


def test_known_lemmas_appear_in_output(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out)
    content = out.read_text()
    for lemma in ["sea", "night", "hand", "sail", "swim", "walk"]:
        assert lemma in content


def test_rank_order_matches_ranked_list(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out)
    content = out.read_text()
    noun_positions = [content.index(lemma) for lemma in RANKED["NOUN"]]
    assert noun_positions == sorted(noun_positions)


def test_summary_stats_are_correct(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out)
    content = out.read_text()
    total_tokens = sum(sum(p.values()) for p in COUNTS.values())
    vocab_size = sum(len(p) for p in COUNTS.values())
    assert str(total_tokens) in content
    assert str(vocab_size) in content


def test_ranker_name_appears_when_provided(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out, ranker_name="FrequencyRanker")
    assert "FrequencyRanker" in out.read_text()


def test_ranker_name_absent_when_empty(tmp_path):
    out = tmp_path / "report.html"
    render(COUNTS, RANKED, out, ranker_name="")
    assert "FrequencyRanker" not in out.read_text()


def test_invalid_path_raises_error(tmp_path):
    bad = tmp_path / "nonexistent_dir" / "report.html"
    with pytest.raises((FileNotFoundError, OSError)):
        render(COUNTS, RANKED, bad)
