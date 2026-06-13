import zipfile
from pathlib import Path

from bs4 import BeautifulSoup

from .base import BaseReader


class HtmlReader(BaseReader):
    def read(self) -> str:
        if self.path.suffix.lower() == ".zip":
            html = self._read_from_zip()
        else:
            html = self.path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")

        for div_id in ("pg-header", "pg-footer"):
            el = soup.find(id=div_id)
            if el is not None:
                el.decompose()

        return soup.get_text(separator="\n", strip=True)

    def _read_from_zip(self) -> str:
        with zipfile.ZipFile(self.path) as zf:
            names = zf.namelist()
            html_name = next(n for n in names if n.lower().endswith((".html", ".htm")))
            return zf.read(html_name).decode("utf-8")
