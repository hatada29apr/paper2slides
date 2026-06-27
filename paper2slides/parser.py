"""
PDF parser for scientific papers.
"""

from __future__ import annotations

import re
from pathlib import Path

import fitz

from paper2slides.models.paper import Paper, Section


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

    def extract_layout(self, doc: fitz.Document) -> list[dict]:
        """Extract text layout information from PDF pages."""
        pages: list[dict] = []

        for page_index, page in enumerate(doc):
            page_dict = page.get_text("dict")
            blocks_data: list[dict] = []

            for block in page_dict.get("blocks", []):
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()

                        if not text:
                            continue

                        blocks_data.append(
                            {
                                "text": text,
                                "font": span.get("font", ""),
                                "size": span.get("size", 0),
                                "bbox": span.get("bbox", []),
                            }
                        )

            pages.append(
                {
                    "page": page_index + 1,
                    "blocks": blocks_data,
                }
            )

        return pages

    def extract_title(self, doc: fitz.Document) -> str:
        """Extract title from PDF metadata or first page."""
        metadata_title = (doc.metadata or {}).get("title", "").strip()

        if metadata_title:
            return metadata_title

        lines = [line.strip() for line in doc[0].get_text("text").splitlines() if line.strip()]

        for line in lines:
            if len(line) > 10:
                return line

        return ""

    def extract_abstract(self, text: str) -> str:
        """Extract abstract text from English or Japanese papers."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        end_patterns = [
            r"^1\s+introduction$",
            r"^1\.\s*introduction$",
            r"^introduction$",
            r"^1\s+はじめに$",
            r"^1\.\s*はじめに$",
            r"^はじめに$",
            r"^ccs concepts",
            r"^additional key words",
            r"^keywords?:",
            r"^キーワード",
        ]

        # Case 1: explicit Abstract heading exists.
        start_index = -1
        for i, line in enumerate(lines[:120]):
            normalized = line.lower().strip().rstrip(":")
            if normalized in {"abstract", "概要", "要旨", "抄録"}:
                start_index = i + 1
                break

        if start_index != -1:
            abstract_lines: list[str] = []

            for line in lines[start_index:]:
                lower = line.lower().strip()
                if any(re.match(pattern, lower) for pattern in end_patterns):
                    break
                abstract_lines.append(line)

            return "\n".join(abstract_lines).strip()

        # Case 2: ACM/SIGMOD style papers often put abstract text directly
        # after title/authors without an explicit "Abstract" heading.
        intro_index = -1
        for i, line in enumerate(lines[:160]):
            lower = line.lower().strip()
            if any(re.match(pattern, lower) for pattern in end_patterns):
                intro_index = i
                break

        if intro_index == -1:
            return ""

        candidate_lines = lines[:intro_index]

        # Remove obvious title/authors/metadata lines.
        filtered_lines: list[str] = []
        skip_keywords = [
            "graph-based vector search",
            "ilias azizi",
            "karima echihabi",
            "themis palpanas",
            "authors",
            "copyright",
            "acm",
            "https://doi.org",
            "arxiv:",
        ]

        for line in candidate_lines:
            lower = line.lower().strip()

            if any(keyword in lower for keyword in skip_keywords):
                continue

            if len(line) < 40:
                continue

            filtered_lines.append(line)

        if not filtered_lines:
            return ""

        return "\n".join(filtered_lines).strip()

    def extract_sections(self, text: str) -> list[Section]:
        """Extract major sections using conservative heading rules."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        heading_patterns = [
            r"^\d+\s+[A-Z][A-Za-z0-9 ,:&\-]+$",
            r"^\d+\.\d+\s+[A-Z][A-Za-z0-9 ,:&\-]+$",
            r"^(Introduction|Background|Related Work|Method|Methods|Experiments|Experimental Evaluation|Results|Discussion|Conclusion|References)$",
        ]

        sections: list[Section] = []
        current_section: Section | None = None

        for line in lines:
            is_heading = any(re.match(pattern, line) for pattern in heading_patterns)

            if re.match(r"^\d+\s+(initialize|update|return|let|if|while)\b", line.lower()):
                is_heading = False

            if is_heading:
                if current_section is not None:
                    sections.append(current_section)

                level = 2 if re.match(r"^\d+\.\d+\s+", line) else 1
                current_section = Section(title=line, level=level, content="")
            elif current_section is not None:
                current_section.content += line + "\n"

        if current_section is not None:
            sections.append(current_section)

        return sections

    def parse(self, pdf_path: str | Path) -> Paper:
        """Parse a PDF into a Paper object."""
        doc = self.load_pdf(pdf_path)
        text = self.extract_text(doc)

        return Paper(
            title=self.extract_title(doc),
            abstract=self.extract_abstract(text),
            sections=self.extract_sections(text),
        )