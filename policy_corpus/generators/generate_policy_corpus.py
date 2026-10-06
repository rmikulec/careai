"""Generate a corpus of realistic hospital policy PDFs for testing.

This script builds a set of formal, multi-section hospital policy documents and
renders each to a PDF under ``policy_corpus/documents/``. The documents are
*test fixtures* for the Incident Reporting Agent: their prose deliberately
carries the kind of facts
the agent must retrieve and reason over — severity criteria, time-bound
notification deadlines, required immediate actions, and documentation fields.

The facility ("Riverside Regional Medical Center") and all names are fictional.
Regulatory anchors (OSHA 29 CFR 1910.1030, CMS 42 CFR 482.13, The Joint
Commission Universal Protocol / Sentinel Event policy, NQF SREs, NCC MERP,
NPIAP staging, EMTALA, etc.) are real so retrieval and grounding behave against
plausible content.

Run:
    python policy_corpus/generators/generate_policy_corpus.py
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from _policy_model import (
    FACILITY,
    Bullets,
    Note,
    Para,
    PolicyDoc,
    Steps,
    TableBlock,
    _LIGHT,
    _NAVY,
    _RULE,
    _STEEL,
)
from policy_content import build_corpus

logger = logging.getLogger(__name__)

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


# --------------------------------------------------------------------------- #
# Rendering.
# --------------------------------------------------------------------------- #


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles: dict[str, ParagraphStyle] = {}
    styles["title"] = ParagraphStyle(
        "title",
        parent=base["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        textColor=_NAVY,
        spaceAfter=2,
        alignment=TA_LEFT,
    )
    styles["facility"] = ParagraphStyle(
        "facility",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.white,
    )
    styles["facility_sub"] = ParagraphStyle(
        "facility_sub",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        textColor=_LIGHT,
    )
    styles["h2"] = ParagraphStyle(
        "h2",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=_NAVY,
        spaceBefore=12,
        spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "body",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        spaceAfter=5,
        alignment=TA_LEFT,
    )
    styles["list"] = ParagraphStyle(
        "list",
        parent=styles["body"],
        spaceAfter=2,
    )
    styles["meta_label"] = ParagraphStyle(
        "meta_label",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        textColor=_NAVY,
    )
    styles["meta_value"] = ParagraphStyle(
        "meta_value",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        textColor=colors.black,
    )
    styles["cell"] = ParagraphStyle(
        "cell",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
    )
    styles["cell_head"] = ParagraphStyle(
        "cell_head",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
    )
    styles["note"] = ParagraphStyle(
        "note",
        parent=styles["body"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        textColor=_NAVY,
        spaceAfter=0,
    )
    return styles


def _header_footer(doc_number: str) -> Callable:
    """Build an onPage callback that stamps the running footer."""

    def _draw(canvas, doc) -> None:  # type: ignore[no-untyped-def]
        canvas.saveState()
        canvas.setStrokeColor(_RULE)
        canvas.setLineWidth(0.5)
        canvas.line(0.9 * inch, 0.72 * inch, 7.6 * inch, 0.72 * inch)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#6b7a86"))
        canvas.drawString(
            0.9 * inch,
            0.56 * inch,
            f"{FACILITY} · {doc_number}",
        )
        canvas.drawCentredString(
            4.25 * inch,
            0.56 * inch,
            "CONFIDENTIAL — Uncontrolled when printed. Verify current version "
            "in the Policy Management System.",
        )
        canvas.drawRightString(
            7.6 * inch,
            0.56 * inch,
            f"Page {doc.page}",
        )
        canvas.restoreState()

    return _draw


def _masthead(st: dict[str, ParagraphStyle], doc: PolicyDoc) -> Table:
    """The top banner: facility identity bar + title + metadata grid."""
    bar = Table(
        [
            [
                Paragraph(FACILITY, st["facility"]),
                Paragraph("POLICY & PROCEDURE", st["facility_sub"]),
            ]
        ],
        colWidths=[4.7 * inch, 2.0 * inch],
    )
    bar.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), _NAVY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ]
        )
    )

    def kv(label: str, value: str):
        return [Paragraph(label, st["meta_label"]), Paragraph(value, st["meta_value"])]

    meta = Table(
        [
            kv("Policy Number", doc.number) + kv("Owner / Department", doc.owner),
            kv("Effective Date", doc.effective) + kv("Version", doc.version),
            kv("Last Revised", doc.revised) + kv("Next Review", doc.review),
            kv("Approved By", doc.approved_by) + kv("Applies To", doc.applies_to),
        ],
        colWidths=[1.05 * inch, 2.3 * inch, 1.05 * inch, 2.3 * inch],
    )
    meta.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, _RULE),
                ("BACKGROUND", (0, 0), (0, -1), _LIGHT),
                ("BACKGROUND", (2, 0), (2, -1), _LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return bar, meta


def _render_table(st: dict[str, ParagraphStyle], tb: TableBlock, width: float) -> Table:
    headers = [Paragraph(h, st["cell_head"]) for h in tb.headers]
    body = [[Paragraph(c, st["cell"]) for c in row] for row in tb.rows]
    data = [headers] + body
    widths = tb.col_widths or [width / len(tb.headers)] * len(tb.headers)
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), _STEEL),
        ("GRID", (0, 0), (-1, -1), 0.4, _RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if tb.row_shades:
        for i, shade in enumerate(tb.row_shades, start=1):
            if shade is not None:
                style.append(("BACKGROUND", (0, i), (-1, i), shade))
    t.setStyle(TableStyle(style))
    return t


def _build_flowables(st: dict[str, ParagraphStyle], doc: PolicyDoc, width: float):
    bar, meta = _masthead(st, doc)
    flow: list = [
        bar,
        Spacer(1, 6),
        Paragraph(doc.title, st["title"]),
        Spacer(1, 4),
        meta,
        Spacer(1, 10),
    ]

    for i, section in enumerate(doc.sections, start=1):
        flow.append(Paragraph(f"{i}.&nbsp;&nbsp;{section.title}", st["h2"]))
        for block in section.blocks:
            if isinstance(block, Para):
                flow.append(Paragraph(block.text, st["body"]))
            elif isinstance(block, Bullets):
                flow.append(
                    ListFlowable(
                        [
                            ListItem(Paragraph(x, st["list"]), leftIndent=10)
                            for x in block.items
                        ],
                        bulletType="bullet",
                        bulletChar="•",
                        bulletColor=_STEEL,
                        leftIndent=14,
                    )
                )
                flow.append(Spacer(1, 4))
            elif isinstance(block, Steps):
                flow.append(
                    ListFlowable(
                        [
                            ListItem(Paragraph(x, st["list"]), leftIndent=10)
                            for x in block.items
                        ],
                        bulletType="1",
                        bulletFormat="%s.",
                        bulletColor=_NAVY,
                        leftIndent=16,
                    )
                )
                flow.append(Spacer(1, 4))
            elif isinstance(block, TableBlock):
                flow.append(_render_table(st, block, width))
                flow.append(Spacer(1, 6))
            elif isinstance(block, Note):
                note_tbl = Table(
                    [
                        [
                            Paragraph(
                                '<font color="#b5641e">IMPORTANT — </font>'
                                + block.text,
                                st["note"],
                            )
                        ]
                    ],
                    colWidths=[width],
                )
                note_tbl.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, -1),
                                colors.HexColor("#fff6e5"),
                            ),
                            ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#e0a93b")),
                            ("LEFTPADDING", (0, 0), (-1, -1), 8),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ]
                    )
                )
                flow.append(note_tbl)
                flow.append(Spacer(1, 6))
    return flow


def render(doc: PolicyDoc, out_dir: Path) -> tuple[Path, int]:
    """Render a single policy to a PDF.

    Args:
        doc (PolicyDoc): The policy content model.
        out_dir (Path): Destination directory.

    Returns:
        tuple[Path, int]: The path to the written PDF and its page count.
    """
    slug = doc.number.lower().replace("-", "_")
    safe_title = "".join(c if c.isalnum() or c.isspace() else " " for c in doc.title)
    name_part = "_".join(safe_title.lower().split()[:5])
    out_path = out_dir / f"{slug}_{name_part}.pdf"

    st = _styles()
    page_w, page_h = letter
    left = right = 0.9 * inch
    frame = Frame(
        left,
        0.9 * inch,
        page_w - left - right,
        page_h - 0.9 * inch - 1.0 * inch,
        id="body",
    )
    template = PageTemplate(
        id="main", frames=[frame], onPage=_header_footer(doc.number)
    )
    pdf = BaseDocTemplate(
        str(out_path),
        pagesize=letter,
        pageTemplates=[template],
        title=f"{doc.number} {doc.title}",
        author=FACILITY,
        subject=", ".join(doc.keywords),
    )
    pdf.build(_build_flowables(st, doc, frame.width))
    return out_path, pdf.page


def _write_index(rows: list[tuple[PolicyDoc, str, int]]) -> None:
    """Write the documents/README.md: an auto-generated index of the corpus."""
    lines = [
        "# Policy Corpus (test fixtures)",
        "",
        "Synthetic but regulation-accurate hospital policy PDFs for testing the "
        "Incident Reporting Agent's retrieval, grounding, severity, and "
        "notification logic. The facility (&ldquo;Riverside Regional Medical "
        "Center&rdquo;) and all names are fictional; the cited standards (OSHA, "
        "CMS, The Joint Commission, NQF, CDC, FDA, HIPAA, NPIAP, EMTALA, AABB, "
        "ISMP, NCC MERP, etc.) are real.".replace("&ldquo;", "“").replace(
            "&rdquo;", "”"
        ),
        "",
        "Every policy shares one severity scale &mdash; **SEV-1 / SEV-2 / SEV-3 "
        "/ Near Miss** &mdash; defined in `POL-RM-013` and referenced by every "
        "other policy, with concrete, time-bound notification deadlines stated "
        "in prose for the agent to extract.".replace("&mdash;", "—"),
        "",
        "Regenerate with:",
        "",
        "```bash",
        "python policy_corpus/generators/generate_policy_corpus.py",
        "```",
        "",
        f"**{len(rows)} policies.** Index below is auto-generated on each run.",
        "",
        "| Policy # | Title | Owner | Pages | File |",
        "|---|---|---|---|---|",
    ]
    for doc, filename, pages in sorted(rows, key=lambda r: r[0].number):
        title = doc.title.replace("|", "/")
        owner = doc.owner.replace("|", "/")
        lines.append(f"| {doc.number} | {title} | {owner} | {pages} | `{filename}` |")
    lines.append("")
    (DOCUMENTS_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    corpus = build_corpus()
    rows: list[tuple[PolicyDoc, str, int]] = []
    total_pages = 0
    for policy in corpus:
        path, pages = render(policy, DOCUMENTS_DIR)
        rows.append((policy, path.name, pages))
        total_pages += pages
        logger.info("wrote %s (%d pp)", path.relative_to(DOCUMENTS_DIR.parent), pages)
    _write_index(rows)
    logger.info(
        "\n%d policy PDFs (%d pages) written to %s/ + README.md index",
        len(rows),
        total_pages,
        DOCUMENTS_DIR.name,
    )


if __name__ == "__main__":
    main()
