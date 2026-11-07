#!/usr/bin/env python3
"""
Executive Security Advisory PDF Compiler
Author: Lead Python Security Document Automation Architect
Engine: ReportLab (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable)
Input: FINAL_ADVISORY.md -> Output: EXECUTIVE_SECURITY_ADVISORY.pdf
"""

import os
import sys
import re
from datetime import datetime
from typing import List, Tuple, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_MD_FILE = os.path.join(WORKSPACE_DIR, "FINAL_ADVISORY.md")
OUTPUT_PDF_FILE = os.path.join(WORKSPACE_DIR, "EXECUTIVE_SECURITY_ADVISORY.pdf")

# ==============================================================================
# COLOR PALETTE (CORPORATE EXECUTIVE THEME)
# ==============================================================================
DARK_HEADER_BG = colors.HexColor("#1e242b")       # Dark charcoal header band
BADGE_RED = colors.HexColor("#cf222e")            # Restricted / High Risk badge
ACCENT_BLUE = colors.HexColor("#0969da")          # Primary corporate accent
BORDER_GRAY = colors.HexColor("#d0d7de")          # Table & separator grid lines
TABLE_HEADER_BG = colors.HexColor("#24292f")      # Table header background
CODE_BG = colors.HexColor("#f6f8fa")              # Code snippet background
TEXT_MAIN = colors.HexColor("#1f2328")            # Main body text
TEXT_MUTED = colors.HexColor("#57606a")           # Subtitles & metadata


class NumberedCanvas(canvas.Canvas):
    """Generates two-pass 'Page X of Y' dynamic footers and running header rules."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_MUTED)

        # Footer divider line
        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.5)
        self.line(36, 32, letter[0] - 36, 32)

        # Running Footer text
        footer_text = "SYNDICATE SECURITY HOLDINGS  |  CONFIDENTIAL & PROPRIETARY  |  TLP:AMBER"
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(36, 22, footer_text)
        self.drawRightString(letter[0] - 36, 22, page_str)
        self.restoreState()


def build_styles():
    """Constructs strict typographical hierarchy using standard Helvetica and Courier."""
    styles = getSampleStyleSheet()

    # Base typography
    styles.add(ParagraphStyle(
        name="DocTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=DARK_HEADER_BG,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="PortSectionHeading",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=ACCENT_BLUE,
        spaceBefore=12,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="SubHeading",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=DARK_HEADER_BG,
        spaceBefore=8,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="SubSubHeading",
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=TEXT_MUTED,
        spaceBefore=6,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="CorporateBody",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN,
        spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="CorporateBullet",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_MAIN,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    ))
    styles.add(ParagraphStyle(
        name="CodeBlockText",
        fontName="Courier",
        fontSize=7.5,
        leading=10,
        textColor=DARK_HEADER_BG
    ))
    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        name="TableCell",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=TEXT_MAIN
    ))
    styles.add(ParagraphStyle(
        name="TableCellBold",
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=TEXT_MAIN
    ))

    return styles


def create_header_band(printable_width: float) -> Table:
    """
    Creates a full-width dark gray corporate header band with classification badge.
    """
    left_html = (
        '<b><font size="12" color="#ffffff" face="Helvetica-Bold">SYNDICATE SECURITY HOLDINGS</font></b><br/>'
        '<font size="7.5" color="#94a3b8" face="Helvetica">CYBER THREAT AUDIT & INCIDENT ADVISORY DIVISION</font>'
    )
    right_html = (
        '<para align="right">'
        '<b><font size="8.5" color="#ff4d4f" face="Helvetica-Bold">[ RESTRICTED / HIGH RISK ]</font></b><br/>'
        '<font size="7" color="#cbd5e1" face="Helvetica">CLASSIFICATION: TLP:AMBER STRICT</font>'
        '</para>'
    )

    left_p = Paragraph(left_html, ParagraphStyle(name="HLeft", fontName="Helvetica", leading=14))
    right_p = Paragraph(right_html, ParagraphStyle(name="HRight", fontName="Helvetica", leading=12))

    table_data = [[left_p, right_p]]
    col_widths = [printable_width * 0.65, printable_width * 0.35]

    header_table = Table(table_data, colWidths=col_widths)
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), DARK_HEADER_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    return header_table


def format_inline_markdown(text: str) -> str:
    """Converts bold, italics, and inline code to ReportLab Paragraph XML."""
    # Convert bold+italic ***text*** -> <b><i>text</i></b>
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Convert bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert italic *text* -> <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert inline code `text` -> <font face="Courier">text</font>
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#cf222e">\1</font>', text)
    # Handle & safely
    text = text.replace(" & ", " &amp; ")
    return text


def build_code_flowable(code_content: str, printable_width: float, styles) -> Table:
    """Encapsulates firewall commands / code snippets in a Courier monospace card."""
    clean_lines = [line.rstrip() for line in code_content.strip().splitlines()]
    safe_text = "<br/>".join([line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;") for line in clean_lines])
    p = Paragraph(safe_text, styles["CodeBlockText"])

    code_table = Table([[p]], colWidths=[printable_width])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_GRAY),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return code_table


def parse_markdown_to_flowables(md_content: str, printable_width: float, styles) -> List[Any]:
    """
    Parses Markdown text and compiles it into structured ReportLab Flowables
    with custom tables, typography, and prominent horizontal separators.
    """
    flowables = []
    lines = md_content.splitlines()
    i = 0
    total_lines = len(lines)

    in_code_block = False
    code_buffer = []

    in_table = False
    table_raw_rows = []

    def flush_table():
        nonlocal in_table, table_raw_rows
        if not table_raw_rows:
            in_table = False
            return

        # Determine column count
        col_count = max(len(r) for r in table_raw_rows)
        # Calculate widths proportionally (e.g. 25%, 35%, 40%)
        if col_count == 3:
            col_widths = [printable_width * 0.28, printable_width * 0.36, printable_width * 0.36]
        elif col_count == 4:
            col_widths = [printable_width * 0.25, printable_width * 0.25, printable_width * 0.30, printable_width * 0.20]
        else:
            col_widths = [printable_width / col_count] * col_count

        formatted_table_data = []
        for row_idx, row in enumerate(table_raw_rows):
            formatted_row = []
            for col_idx, cell in enumerate(row):
                cell_text = format_inline_markdown(cell.strip())
                if row_idx == 0:
                    formatted_row.append(Paragraph(cell_text, styles["TableHeader"]))
                elif col_idx == 0:
                    formatted_row.append(Paragraph(cell_text, styles["TableCellBold"]))
                else:
                    formatted_row.append(Paragraph(cell_text, styles["TableCell"]))
            # Pad if shorter
            while len(formatted_row) < col_count:
                formatted_row.append(Paragraph("", styles["TableCell"]))
            formatted_table_data.append(formatted_row)

        rep_table = Table(formatted_table_data, colWidths=col_widths)
        t_style = [
            ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]
        # Alternate row background
        for r_i in range(1, len(formatted_table_data)):
            if r_i % 2 == 0:
                t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), colors.HexColor("#f8fafc")))
            else:
                t_style.append(('BACKGROUND', (0, r_i), (-1, r_i), colors.white))

        rep_table.setStyle(TableStyle(t_style))
        flowables.append(Spacer(1, 4))
        flowables.append(rep_table)
        flowables.append(Spacer(1, 8))

        table_raw_rows = []
        in_table = False

    while i < total_lines:
        line = lines[i].rstrip()

        # 1. Code blocks (```)
        if line.startswith("```"):
            if in_code_block:
                # Flush code block
                flowables.append(Spacer(1, 4))
                flowables.append(build_code_flowable("\n".join(code_buffer), printable_width, styles))
                flowables.append(Spacer(1, 6))
                code_buffer = []
                in_code_block = False
            else:
                if in_table:
                    flush_table()
                in_code_block = True
                code_buffer = []
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # 2. Tables (| ... |)
        if line.startswith("|") and line.endswith("|"):
            raw_cells = [c.strip() for c in line.split("|")[1:-1]]
            # Skip separator line like | :--- | :--- |
            if all(set(c).issubset({"-", ":", " "}) for c in raw_cells):
                i += 1
                continue
            in_table = True
            table_raw_rows.append(raw_cells)
            i += 1
            continue
        elif in_table:
            flush_table()

        # 3. Horizontal Separator (---)
        if line.strip() in ("---", "***", "___"):
            flowables.append(Spacer(1, 6))
            # Prominent horizontal separator rule
            flowables.append(HRFlowable(
                width="100%",
                thickness=1.5,
                color=ACCENT_BLUE,
                spaceBefore=8,
                spaceAfter=12
            ))
            i += 1
            continue

        # 4. Headings
        if line.startswith("# "):
            flowables.append(Spacer(1, 10))
            flowables.append(Paragraph(format_inline_markdown(line[2:].strip()), styles["DocTitle"]))
            i += 1
            continue

        if line.startswith("## "):
            heading_text = line[3:].strip()
            # If this is a Port assessment section (Port 22, Port 80, etc.), insert prominent divider
            if "port" in heading_text.lower():
                flowables.append(HRFlowable(
                    width="100%",
                    thickness=2.0,
                    color=DARK_HEADER_BG,
                    spaceBefore=14,
                    spaceAfter=8
                ))
            flowables.append(Paragraph(format_inline_markdown(heading_text), styles["PortSectionHeading"]))
            i += 1
            continue

        if line.startswith("### "):
            flowables.append(Paragraph(format_inline_markdown(line[4:].strip()), styles["SubHeading"]))
            i += 1
            continue

        if line.startswith("#### "):
            flowables.append(Paragraph(format_inline_markdown(line[5:].strip()), styles["SubSubHeading"]))
            i += 1
            continue

        # 5. Bullet Lists (*, -, 1.)
        bullet_match = re.match(r"^(\*|-|\d+\.)\s+(.+)$", line)
        if bullet_match:
            bullet_prefix = bullet_match.group(1)
            bullet_body = bullet_match.group(2)
            if bullet_prefix in ("*", "-"):
                formatted_bullet = f"&bull;&nbsp; {format_inline_markdown(bullet_body)}"
            else:
                formatted_bullet = f"<b>{bullet_prefix}</b> {format_inline_markdown(bullet_body)}"
            flowables.append(Paragraph(formatted_bullet, styles["CorporateBullet"]))
            i += 1
            continue

        # 6. Standard Paragraph / Metadata
        stripped = line.strip()
        if stripped:
            flowables.append(Paragraph(format_inline_markdown(stripped), styles["CorporateBody"]))
        else:
            flowables.append(Spacer(1, 3))

        i += 1

    if in_table:
        flush_table()

    return flowables


def compile_pdf_direct(input_path: str, output_path: str):
    """Compiles a specific markdown file directly to a target PDF path."""
    with open(input_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    margin = 36
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    printable_width = letter[0] - (margin * 2)
    styles = build_styles()

    story = []
    story.append(create_header_band(printable_width))
    story.append(Spacer(1, 10))

    parsed_flowables = parse_markdown_to_flowables(md_text, printable_width, styles)
    story.extend(parsed_flowables)

    doc.build(story, canvasmaker=NumberedCanvas)


def compile_pdf():
    print("=" * 75)
    print("      EXECUTIVE SECURITY ADVISORY // PDF AUTOMATION COMPILER        ")
    print("=" * 75)

    # 1. Discover or verify source markdown
    target_md = INPUT_MD_FILE
    if not os.path.exists(target_md):
        # Look for any recent FINAL_ADVISORY_*.md
        candidates = [f for f in os.listdir(WORKSPACE_DIR) if f.startswith("FINAL_ADVISORY") and f.endswith(".md")]
        if candidates:
            target_md = os.path.join(WORKSPACE_DIR, sorted(candidates)[-1])
            print(f"[*] Default FINAL_ADVISORY.md not found. Selected active artifact: {os.path.basename(target_md)}")
        else:
            print("[-] FATAL: No FINAL_ADVISORY.md file located in workspace.", file=sys.stderr)
            sys.exit(1)

    print(f"[*] Reading Source Markdown: {target_md}")
    compile_pdf_direct(target_md, OUTPUT_PDF_FILE)

    print(f"[+] Compilation Complete!")
    print(f"[+] Executive PDF Generated : {OUTPUT_PDF_FILE}")
    print(f"[+] File Size               : {os.path.getsize(OUTPUT_PDF_FILE):,} bytes")
    print("=" * 75)


if __name__ == "__main__":
    compile_pdf()
