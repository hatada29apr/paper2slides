"""
Paper data models.

This module defines the internal representation of a scientific paper.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class Section(BaseModel):
    """A section of a scientific paper."""

    title: str = Field(..., description="Section title")
    level: int = Field(default=1, description="Heading level")
    content: str = Field(default="", description="Section body")


class Figure(BaseModel):
    """A figure in the paper."""

    number: int
    caption: str = ""


class Table(BaseModel):
    """A table in the paper."""

    number: int
    caption: str = ""


class Reference(BaseModel):
    """A bibliographic reference."""

    text: str


class Paper(BaseModel):
    """Scientific paper."""

    title: str = ""
    authors: List[str] = Field(default_factory=list)
    abstract: str = ""
    sections: List[Section] = Field(default_factory=list)
    figures: List[Figure] = Field(default_factory=list)
    tables: List[Table] = Field(default_factory=list)
    references: List[Reference] = Field(default_factory=list)