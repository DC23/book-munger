import pytest
from book_munger.filter import apply_stopwords


@pytest.fixture()
def sample_counts():
    return {
        "NOUN": {"dog": 3, "cat": 1, "the": 5},
        "VERB": {"run": 2, "be": 4},
    }


def test_none_path_returns_counts_unchanged(sample_counts):
    result = apply_stopwords(sample_counts, None)
    assert result == sample_counts


def test_none_path_is_identity_not_copy(sample_counts):
    result = apply_stopwords(sample_counts, None)
    assert result is sample_counts


def test_stopword_removed_from_all_pos_buckets(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("dog\nrun\n")
    result = apply_stopwords(sample_counts, sw)
    assert "dog" not in result["NOUN"]
    assert "run" not in result["VERB"]


def test_non_stopword_lemmas_preserved(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("dog\n")
    result = apply_stopwords(sample_counts, sw)
    assert result["NOUN"]["cat"] == 1
    assert result["VERB"]["run"] == 2
    assert result["VERB"]["be"] == 4


def test_comment_lines_in_stopword_file_ignored(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("# this is a comment\ndog\n# another comment\n")
    result = apply_stopwords(sample_counts, sw)
    assert "dog" not in result["NOUN"]
    assert result["NOUN"]["cat"] == 1


def test_blank_lines_in_stopword_file_ignored(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("\n\ndog\n\n\n")
    result = apply_stopwords(sample_counts, sw)
    assert "dog" not in result["NOUN"]
    assert result["NOUN"]["cat"] == 1


def test_uppercase_stopword_entry_matches_lowercase_lemma(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("DOG\nRUN\n")
    result = apply_stopwords(sample_counts, sw)
    assert "dog" not in result["NOUN"]
    assert "run" not in result["VERB"]


def test_stopword_not_in_counts_is_a_no_op(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("elephant\n")
    result = apply_stopwords(sample_counts, sw)
    assert result == sample_counts


def test_empty_stopword_file_returns_all_counts(tmp_path, sample_counts):
    sw = tmp_path / "stopwords.txt"
    sw.write_text("")
    result = apply_stopwords(sample_counts, sw)
    assert result == sample_counts
