from pathlib import Path

import pytest

from book_munger.writers.markdown import MarkdownWriter

RANKED = {
    "NOUN": ["sea", "night", "hand"],
    "VERB": ["sail", "swim", "walk"],
    "ADJ": ["dark", "cold", "old"],
}


@pytest.fixture
def writer():
    return MarkdownWriter()


def test_combined_creates_output_file(writer, tmp_path):
    out = tmp_path / "words.md"
    writer.write(RANKED, out)
    assert out.exists()


def test_combined_all_pos_appear(writer, tmp_path):
    out = tmp_path / "words.md"
    writer.write(RANKED, out)
    content = out.read_text()
    assert "Nouns" in content
    assert "Verbs" in content
    assert "Adjectives" in content


def test_combined_word_order_preserved(writer, tmp_path):
    out = tmp_path / "words.md"
    writer.write(RANKED, out)
    content = out.read_text()
    noun_positions = [content.index(w) for w in RANKED["NOUN"]]
    assert noun_positions == sorted(noun_positions)


def test_split_creates_one_file_per_pos(writer, tmp_path):
    out = tmp_path / "book.md"
    writer.write(RANKED, out, split=True)
    created = set(p.name for p in tmp_path.iterdir())
    assert created == {"book-nouns.md", "book-verbs.md", "book-adjectives.md"}


def test_split_file_has_header_and_words(writer, tmp_path):
    out = tmp_path / "book.md"
    writer.write({"NOUN": ["sea", "night", "hand"]}, out, split=True)
    content = (tmp_path / "book-nouns.md").read_text()
    assert content.startswith("# Nouns (3 words)\n")
    assert "sea\nnight\nhand\n" in content


def test_empty_ranked_writes_without_error(writer, tmp_path):
    out = tmp_path / "empty.md"
    writer.write({}, out)
    assert out.exists()


def test_invalid_path_raises_error(writer, tmp_path):
    bad = tmp_path / "nonexistent_dir" / "words.md"
    with pytest.raises((FileNotFoundError, OSError)):
        writer.write(RANKED, bad)
