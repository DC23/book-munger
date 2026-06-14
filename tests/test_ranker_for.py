import pytest

from book_munger.rankers import ranker_for
from book_munger.rankers.distinctive import DistinctivenessRanker
from book_munger.rankers.frequency import FrequencyRanker


def test_ranker_for_frequency_returns_frequency_ranker():
    assert isinstance(ranker_for("frequency"), FrequencyRanker)


def test_ranker_for_distinctive_returns_distinctiveness_ranker():
    assert isinstance(ranker_for("distinctive"), DistinctivenessRanker)


def test_ranker_for_unknown_raises_value_error():
    with pytest.raises(ValueError, match="unknown"):
        ranker_for("unknown")
