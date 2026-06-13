import pytest
from book_munger.nlp_pipeline import process

_ALLOWED_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN", "PRON", "CCONJ", "SCONJ", "ADP", "INTJ"}


def test_process_excludes_punctuation():
    result = list(process("Hello, world!"))
    assert all(pos != "PUNCT" for _, pos in result)


def test_process_excludes_whitespace():
    result = list(process("Hello  world"))
    assert all(pos != "SPACE" for _, pos in result)


def test_process_excludes_numbers():
    result = list(process("I have 42 books."))
    assert all(pos != "NUM" for _, pos in result)


def test_process_returns_only_allowed_pos():
    result = list(process("The quick brown fox jumps over the lazy dog."))
    assert all(pos in _ALLOWED_POS for _, pos in result)


def test_process_known_sentence():
    result = list(process("The dogs run."))
    assert ("dog", "NOUN") in result
    assert ("run", "VERB") in result


def test_process_lemma_is_lowercase():
    result = list(process("London is a city."))
    assert all(lemma == lemma.lower() for lemma, _ in result)


def test_process_lemmatises_verb():
    result = list(process("She was running."))
    lemmas = [lemma for lemma, pos in result if pos == "VERB"]
    assert "run" in lemmas


def test_process_lemmatises_noun():
    result = list(process("The geese flew."))
    lemmas = [lemma for lemma, pos in result if pos == "NOUN"]
    assert "goose" in lemmas


def test_process_model_cached():
    from book_munger.nlp_pipeline import _load_model
    _load_model.cache_clear()
    list(process("Hello world"))
    list(process("Another sentence"))
    info = _load_model.cache_info()
    assert info.misses == 1
    assert info.hits == 1
