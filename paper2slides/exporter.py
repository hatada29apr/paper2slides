"""
Export utilities for Paper2Slides.
"""

from __future__ import annotations

from pathlib import Path

from paper2slides.models.paper import Paper


def export_paper_json(paper: Paper, output_path: str | Path) -> Path:
    """Export a Paper object as JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    json_text = paper.model_dump_json(indent=2)

    path.write_text(json_text, encoding="utf-8")

    return path