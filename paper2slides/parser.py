"""
PDF parser for scientific papers.
"""

from pathlib import Path

import fitz

from paper2slides.models.paper import Paper


class PaperParser:
    """Parser for scientific paper PDFs."""

    def load_pdf(self, pdf_path: str | Path) -> fitz.Document:
        """Open a PDF document."""
        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        if path.stat().st_size == 0:
            raise ValueError(f"PDF is empty: {path}")

        return fitz.open(path)

    def extract_text(self, doc: fitz.Document) -> str:
        """Extract plain text from all pages."""
        pages: list[str] = []

        for page in doc:
            pages.append(page.get_text("text"))

        return "\n".join(pages).strip()

    def extract_title(self, doc: fitz.Document) -> str:
        """Extract title from PDF metadata or first page."""
        metadata_title = (doc.metadata or {}).get("title", "").strip()

        if metadata_title:
            return metadata_title

        first_page_text = doc[0].get_text("text").splitlines()

        for line in first_page_text:
            cleaned = line.strip()
            if len(cleaned) > 10:
                return cleaned

        return ""

    def extract_abstract(self, text: str) -> str:
        """Extract abstract text from English or Japanese papers."""
        keywords = [
            "abstract",
            "概要",
            "要旨",
            "抄録",
            "summary",
        ]

        end_keywords = [
            "1 introduction",
            "1. introduction",
            "introduction",
            "1 はじめに",
            "1. はじめに",
            "はじめに",
            "キーワード",
            "keywords",
        ]

        lower_text = text.lower()

        start = -1
        matched_keyword = ""

        for keyword in keywords:
            index = lower_text.find(keyword.lower())
            if index != -1:
                start = index
                matched_keyword = keyword
                break

        if start == -1:
            return ""

        search_area = lower_text[start + len(matched_keyword):]

        end_positions = []
        for keyword in end_keywords:
            index = search_area.find(keyword.lower())
            if index != -1:
                end_positions.append(index)

        if end_positions:
            end = start + len(matched_keyword) + min(end_positions)
            return text[start:end].strip()

        return text[start:start + 2000].strip()

    def parse(self, pdf_path: str | Path) -> Paper:
        """Parse a PDF into a Paper object."""
        doc = self.load_pdf(pdf_path)
        text = self.extract_text(doc)

        return Paper(
            title=self.extract_title(doc),
            abstract=self.extract_abstract(text),
        )