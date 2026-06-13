import pytest
from book_munger.rankers.frequency import FrequencyRanker


@pytest.fixture
def ranker():
    return FrequencyRanker()


def test_top_n_returned_in_descending_order(ranker):
    counts = {"dog": 5, "cat": 3, "bird": 8}
    assert ranker.rank(counts, 2) == ["bird", "dog"]


def test_ties_broken_consistently(ranker):
    counts = {"apple": 2, "banana": 2, "cherry": 2}
    result = ranker.rank(counts, 3)
    assert sorted(result) == ["apple", "banana", "cherry"]
    assert result == ranker.rank(counts, 3)


def test_top_n_larger_than_vocabulary_returns_all(ranker):
    counts = {"run": 4, "walk": 2}
    result = ranker.rank(counts, 100)
    assert sorted(result) == ["run", "walk"]


def test_empty_counts_returns_empty_list(ranker):
    assert ranker.rank({}, 10) == []
