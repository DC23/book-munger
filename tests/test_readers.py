import zipfile
from pathlib import Path

import pytest

from book_munger.readers import HtmlReader, PlainTextReader, reader_for

# ---------------------------------------------------------------------------
# Helpers / constants
# ---------------------------------------------------------------------------

PG_TEXT_TEMPLATE = """\
The Project Gutenberg eBook of Lorem Ipsum

Some metadata here.

*** START OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

{body}

*** END OF THE PROJECT GUTENBERG EBOOK LOREM IPSUM ***

Some footer boilerplate.
"""

PG_HTML_TEMPLATE = """\
<html><body>
<div id="pg-header">Project Gutenberg header content</div>
<p>{body}</p>
<div id="pg-footer">Project Gutenberg footer content</div>
</body></html>
"""

BODY = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def utf8_txt(tmp_path):
    p = tmp_path / "lorem.txt"
    p.write_text(PG_TEXT_TEMPLATE.format(body=BODY), encoding="utf-8")
    return p


@pytest.fixture
def latin1_txt(tmp_path):
    p = tmp_path / "lorem_latin1.txt"
    body = "Voilà le café \xe9l\xe9gant"
    p.write_bytes(PG_TEXT_TEMPLATE.format(body=body).encode("latin-1"))
    return p


@pytest.fixture
def html_file(tmp_path):
    p = tmp_path / "lorem.html"
    p.write_text(PG_HTML_TEMPLATE.format(body=BODY), encoding="utf-8")
    return p


@pytest.fixture
def zip_file(tmp_path):
    html_content = PG_HTML_TEMPLATE.format(body=BODY)
    p = tmp_path / "lorem.zip"
    with zipfile.ZipFile(p, "w") as zf:
        zf.writestr("lorem.html", html_content)
    return p


@pytest.fixture
def html_no_pg_divs(tmp_path):
    p = tmp_path / "plain.html"
    p.write_text(f"<html><body><p>{BODY}</p></body></html>", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# reader_for() dispatch
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "suffix,expected",
    [
        (".txt", PlainTextReader),
        (".html", HtmlReader),
        (".htm", HtmlReader),
        (".zip", HtmlReader),
    ],
)
def test_reader_for_dispatches_by_suffix(tmp_path, suffix, expected):
    p = tmp_path / f"book{suffix}"
    p.touch()
    assert isinstance(reader_for(p), expected)


# ---------------------------------------------------------------------------
# PlainTextReader
# ---------------------------------------------------------------------------


def test_plain_text_reader_returns_body_strips_boilerplate(utf8_txt):
    text = PlainTextReader(utf8_txt).read()
    assert BODY in text
    assert "Project Gutenberg" not in text
    assert "START OF THE PROJECT GUTENBERG" not in text
    assert "END OF THE PROJECT GUTENBERG" not in text
    assert "footer boilerplate" not in text


def test_plain_text_reader_handles_latin1_encoding(latin1_txt):
    text = PlainTextReader(latin1_txt).read()
    assert "caf\xe9" in text
    assert "START OF THE PROJECT GUTENBERG" not in text


# ---------------------------------------------------------------------------
# HtmlReader
# ---------------------------------------------------------------------------


def test_html_reader_strips_pg_header_footer(html_file):
    text = HtmlReader(html_file).read()
    assert BODY in text
    assert "Project Gutenberg header content" not in text
    assert "Project Gutenberg footer content" not in text


def test_html_reader_reads_zip_file(zip_file):
    text = HtmlReader(zip_file).read()
    assert BODY in text
    assert "Project Gutenberg header content" not in text
    assert "Project Gutenberg footer content" not in text


def test_html_reader_tolerates_missing_pg_divs(html_no_pg_divs):
    text = HtmlReader(html_no_pg_divs).read()
    assert BODY in text
