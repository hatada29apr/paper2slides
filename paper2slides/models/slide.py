"""
Slide data models.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Slide(BaseModel):
    """A single presentation slide."""

    title: str = Field(default="", description="Slide title")
    subtitle: str = Field(default="", description="Slide subtitle")
    bullets: list[str] = Field(default_factory=list, description="Bullet points")
    notes: str = Field(default="", description="Speaker notes")
    layout: str = Field(default="title_and_bullets", description="Slide layout type")
    visual_prompt: str = Field(default="", description="Prompt for diagram or image generation")


class SlideDeck(BaseModel):
    """A complete presentation deck."""

    title: str = Field(default="", description="Deck title")
    subtitle: str = Field(default="", description="Deck subtitle")
    audience: str = Field(default="general", description="Target audience")
    language: str = Field(default="ja", description="Deck language")
    slides: list[Slide] = Field(default_factory=list, description="Slides in the deck")