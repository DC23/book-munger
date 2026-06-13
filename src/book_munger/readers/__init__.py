from pathlib import Path

from .base import BaseReader
from .html import HtmlReader
from .plaintext import PlainTextReader


def reader_for(path: Path) -> BaseReader:
    if path.suffix.lower() in (".html", ".htm", ".zip"):
        return HtmlReader(path)
    return PlainTextReader(path)
