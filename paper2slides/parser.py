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
        """Extract abstract text using a simple rule-based approach."""
        lower_text = text.lower()

        start = lower_text.find("abstract")
        if start == -1:
            return ""

        intro = lower_text.find("introduction", start)
        if intro == -1:
            return text[start:start + 2000].strip()

        return text[start:intro].strip()

    def parse(self, pdf_path: str | Path) -> Paper:
        """Parse a PDF into a Paper object."""
        doc = self.load_pdf(pdf_path)
        text = self.extract_text(doc)

        return Paper(
            title=self.extract_title(doc),
            abstract=self.extract_abstract(text),
        )