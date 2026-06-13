import pytest
from book_munger.counter import count


def test_empty_input_returns_empty_dict():
    assert count([]) == {}


def test_single_token_creates_pos_bucket():
    result = count([("run", "VERB")])
    assert result == {"VERB": {"run": 1}}


def test_counts_accumulate_for_repeated_lemma():
    tokens = [("run", "VERB"), ("run", "VERB"), ("run", "VERB")]
    assert count(tokens) == {"VERB": {"run": 3}}


def test_multiple_lemmas_in_same_pos_bucket():
    tokens = [("run", "VERB"), ("walk", "VERB")]
    assert count(tokens) == {"VERB": {"run": 1, "walk": 1}}


def test_multiple_pos_buckets_are_separate():
    tokens = [("run", "VERB"), ("fast", "ADV")]
    assert count(tokens) == {"VERB": {"run": 1}, "ADV": {"fast": 1}}


def test_same_lemma_different_pos_counted_separately():
    tokens = [("run", "VERB"), ("run", "NOUN")]
    assert count(tokens) == {"VERB": {"run": 1}, "NOUN": {"run": 1}}


@pytest.mark.parametrize("tokens,expected", [
    (
        [("dog", "NOUN"), ("cat", "NOUN"), ("dog", "NOUN"), ("run", "VERB")],
        {"NOUN": {"dog": 2, "cat": 1}, "VERB": {"run": 1}},
    ),
    (
        [("the", "DET"), ("the", "DET"), ("a", "DET")],
        {"DET": {"the": 2, "a": 1}},
    ),
])
def test_mixed_token_accumulation(tokens, expected):
    assert count(tokens) == expected
