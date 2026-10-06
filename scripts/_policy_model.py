"""Shared content model and visual theme for the policy corpus generator.

Kept separate from the renderer and the content so both import the *same*
dataclass objects (otherwise ``isinstance`` checks across modules would fail).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

from reportlab.lib import colors

# --------------------------------------------------------------------------- #
# Facility identity (fictional) and shared visual theme.
# --------------------------------------------------------------------------- #

FACILITY = "Riverside Regional Medical Center"
FACILITY_SUB = "A 420-bed acute-care teaching hospital · Riverside, State"

_NAVY = colors.HexColor("#15314b")
_STEEL = colors.HexColor("#2c5d7c")
_LIGHT = colors.HexColor("#e7eef3")
_RULE = colors.HexColor("#b8c6d1")
_SEV1 = colors.HexColor("#fde0e0")
_SEV2 = colors.HexColor("#fdefd8")
_SEV3 = colors.HexColor("#e6f2e6")


Block = Union["Para", "Bullets", "Steps", "TableBlock", "Note"]


@dataclass
class Para:
    """A plain paragraph of body text."""

    text: str


@dataclass
class Bullets:
    """An unordered (bulleted) list."""

    items: list[str]


@dataclass
class Steps:
    """An ordered (numbered) list, for procedures."""

    items: list[str]


@dataclass
class TableBlock:
    """A grid table with a shaded header row.

    Attributes:
        headers (list[str]): Column header cells.
        rows (list[list[str]]): Body rows.
        col_widths (Optional[list[float]]): Optional explicit column widths.
        row_shades (Optional[list]): Optional per-row background colors.
    """

    headers: list[str]
    rows: list[list[str]]
    col_widths: Optional[list[float]] = None
    row_shades: Optional[list] = None


@dataclass
class Note:
    """A callout box for a critical, must-not-miss instruction."""

    text: str


@dataclass
class Section:
    """A numbered policy section."""

    title: str
    blocks: list[Block]


@dataclass
class PolicyDoc:
    """A full policy document.

    Attributes:
        number (str): Policy identifier, e.g. ``POL-EH-001``.
        title (str): Policy title.
        owner (str): Owning department.
        effective (str): Effective date.
        revised (str): Last revised date.
        review (str): Next scheduled review date.
        version (str): Version string.
        approved_by (str): Approving authority / committee.
        applies_to (str): Scope of who/where the policy applies.
        keywords (list[str]): Retrieval keywords/tags.
        sections (list[Section]): Ordered body sections.
    """

    number: str
    title: str
    owner: str
    effective: str
    revised: str
    review: str
    version: str
    approved_by: str
    applies_to: str
    keywords: list[str]
    sections: list[Section] = field(default_factory=list)
