"""
Paper data models.

This module defines the internal representation of a scientific paper.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Section(BaseModel):
    """A section of a scientific paper."""

    title: str = Field(default="", description="Section title")
    level: int = Field(default=1, description="Heading level")
    content: str = Field(default="", description="Section body text")


class Figure(BaseModel):
    """A figure in a scientific paper."""

    number: int | None = Field(default=None, description="Figure number")
    caption: str = Field(default="", description="Figure caption")
    page: int | None = Field(default=None, description="Page number")


class Table(BaseModel):
    """A table in a scientific paper."""

    number: int | None = Field(default=None, description="Table number")
    caption: str = Field(default="", description="Table caption")
    page: int | None = Field(default=None, description="Page number")


class Reference(BaseModel):
    """A bibliographic reference."""

    text: str = Field(default="", description="Reference text")


class Paper(BaseModel):
    """Structured representation of a scientific paper."""

    title: str = Field(default="", description="Paper title")
    authors: list[str] = Field(default_factory=list, description="Paper authors")
    abstract: str = Field(default="", description="Paper abstract")
    sections: list[Section] = Field(default_factory=list)
    figures: list[Figure] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    references: list[Reference] = Field(default_factory=list)