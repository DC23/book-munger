from pathlib import Path

import pytest
from click.testing import CliRunner

from book_munger.cli import cli

# Synthetic text for integration tests — Lorem Ipsum with enough variety to
# produce tokens across multiple POS types.
_BODY = (
    "The quick brown fox jumps over the lazy dog. "
    "Beautiful things happen slowly. "
    "Dogs run fast and foxes jump quickly. "
    "A patient hunter waits silently in the dark forest."
)


@pytest.fixture
def txt_file(tmp_path):
    p = tmp_path / "sample.txt"
    p.write_text(_BODY, encoding="utf-8")
    return p


@pytest.fixture
def runner():
    return CliRunner()


# ---------------------------------------------------------------------------
# --help
# ---------------------------------------------------------------------------


def test_help_exits_cleanly(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output


# ---------------------------------------------------------------------------
# Basic invocation: produces a combined .md in the current working directory
# ---------------------------------------------------------------------------


def test_basic_invocation_creates_md_file(runner, txt_file, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(cli, [str(txt_file)])
        assert result.exit_code == 0, result.output
        assert (Path.cwd() / "sample.md").exists()


# ---------------------------------------------------------------------------
# --output directs output to a different directory
# ---------------------------------------------------------------------------


def test_output_option_writes_to_specified_directory(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(cli, [str(txt_file), "--output", str(out_dir)])
    assert result.exit_code == 0, result.output
    assert (out_dir / "sample.md").exists()


# ---------------------------------------------------------------------------
# --output-name overrides the filename stem
# ---------------------------------------------------------------------------


def test_output_name_overrides_filename_stem(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--output-name", "mytable"]
    )
    assert result.exit_code == 0, result.output
    assert (out_dir / "mytable.md").exists()


# ---------------------------------------------------------------------------
# --split produces one file per POS
# ---------------------------------------------------------------------------


def test_split_produces_per_pos_files(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(cli, [str(txt_file), "--output", str(out_dir), "--split"])
    assert result.exit_code == 0, result.output
    md_files = list(out_dir.glob("*.md"))
    assert len(md_files) > 1


# ---------------------------------------------------------------------------
# --html-report produces an HTML file alongside the word table
# ---------------------------------------------------------------------------


def test_html_report_creates_html_file(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--html-report"]
    )
    assert result.exit_code == 0, result.output
    assert (out_dir / "sample-report.html").exists()


# ---------------------------------------------------------------------------
# --stopwords filters words from the output
# ---------------------------------------------------------------------------


def test_stopwords_removes_specified_words(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    sw_file = tmp_path / "stopwords.txt"
    sw_file.write_text("fox\ndog\n", encoding="utf-8")
    result = runner.invoke(
        cli,
        [str(txt_file), "--output", str(out_dir), "--stopwords", str(sw_file)],
    )
    assert result.exit_code == 0, result.output
    out_md = (out_dir / "sample.md").read_text(encoding="utf-8")
    assert "fox" not in out_md
    assert "dog" not in out_md


# ---------------------------------------------------------------------------
# --ranker selects ranking strategy; frequency is a valid alternative
# ---------------------------------------------------------------------------


def test_ranker_frequency_flag_runs_without_error(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--ranker", "frequency"]
    )
    assert result.exit_code == 0, result.output


def test_ranker_unknown_exits_with_error(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--ranker", "bogus"]
    )
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# --pos filters to specified POS types
# ---------------------------------------------------------------------------


def test_pos_filter_limits_output_to_requested_pos(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--pos", "noun,adjective"]
    )
    assert result.exit_code == 0, result.output
    out_md = (out_dir / "sample.md").read_text(encoding="utf-8")
    assert "Nouns" in out_md or "Adjectives" in out_md
    assert "Verbs" not in out_md


def test_pos_filter_unknown_name_exits_with_error(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--pos", "boguspos"]
    )
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# --top-n limits words per POS
# ---------------------------------------------------------------------------


def test_top_n_limits_words_per_pos(runner, txt_file, tmp_path):
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    result = runner.invoke(
        cli, [str(txt_file), "--output", str(out_dir), "--top-n", "2", "--split"]
    )
    assert result.exit_code == 0, result.output
    for md_file in out_dir.glob("*.md"):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        # Header line + up to 2 word lines
        word_lines = [l for l in lines if l and not l.startswith("#")]
        assert len(word_lines) <= 2
