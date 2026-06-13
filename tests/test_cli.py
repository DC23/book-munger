import zipfile

import pytest
from click.testing import CliRunner

from book_munger.cli import cli

BODY = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

PG_TEXT = f"""\
The Project Gutenberg eBook of Lorem Ipsum

*** START OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

{BODY}

*** END OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

Footer boilerplate.
"""


def test_help_exits_cleanly():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_process_command_reads_txt_file(tmp_path):
    p = tmp_path / "book.txt"
    p.write_text(PG_TEXT, encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(cli, ["process", str(p)])
    assert result.exit_code == 0
    assert BODY in result.output
