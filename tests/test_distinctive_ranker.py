import pytest
from unittest.mock import patch
from book_munger.rankers.distinctive import DistinctivenessRanker


@pytest.fixture
def ranker():
    return DistinctivenessRanker()


def test_empty_counts_returns_empty_list(ranker):
    assert ranker.rank({}, 10) == []


def test_top_n_larger_than_vocabulary_returns_all(ranker):
    counts = {"quasar": 3, "nebula": 2}
    result = ranker.rank(counts, 100)
    assert sorted(result) == ["nebula", "quasar"]


def test_rare_word_outranks_common_word_at_same_count(ranker):
    # "rare" has low zipf (0.5), "common" has high zipf (6.0); same corpus count
    # distinctive score: rare = 10/0.5 = 20.0, common = 10/6.0 ≈ 1.67
    zipf_values = {"rare": 0.5, "common": 6.0}
    with patch("book_munger.rankers.distinctive.zipf_frequency", side_effect=lambda w, lang: zipf_values[w]):
        result = ranker.rank({"rare": 10, "common": 10}, 2)
    assert result == ["rare", "common"]


def test_unknown_word_zipf_zero_ranked_maximally(ranker):
    # word unknown to wordfreq returns zipf=0.0, score becomes inf — should rank first
    zipf_values = {"xyzzyblorf": 0.0, "common": 5.0}
    with patch("book_munger.rankers.distinctive.zipf_frequency", side_effect=lambda w, lang: zipf_values[w]):
        result = ranker.rank({"xyzzyblorf": 1, "common": 100}, 2)
    assert result[0] == "xyzzyblorf"


def test_ties_broken_consistently(ranker):
    # all words have the same distinctiveness score — result should be identical across calls
    zipf_values = {"alpha": 2.0, "beta": 2.0, "gamma": 2.0}
    counts = {"alpha": 4, "beta": 4, "gamma": 4}
    with patch("book_munger.rankers.distinctive.zipf_frequency", side_effect=lambda w, lang: zipf_values[w]):
        result1 = ranker.rank(counts, 3)
        result2 = ranker.rank(counts, 3)
    assert sorted(result1) == ["alpha", "beta", "gamma"]
    assert result1 == result2
