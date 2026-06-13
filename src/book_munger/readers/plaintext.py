from pathlib import Path

from .base import BaseReader

_START = "*** START OF THE PROJECT GUTENBERG EBOOK"
_END = "*** END OF THE PROJECT GUTENBERG EBOOK"


class PlainTextReader(BaseReader):
    def read(self) -> str:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = self.path.read_text(encoding="latin-1")

        start = raw.find(_START)
        end = raw.find(_END)

        if start != -1 and end != -1:
            after_marker = raw.index("\n", start) + 1
            return raw[after_marker:end].strip()

        return raw.strip()
