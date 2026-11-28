#!/usr/bin/env python3
"""Render a PageSpeed audit JSON as a PDF. Requires ReportLab.

Input fields:
    title, ai_credit: non-empty strings
    runs: list of {"page": "...", "strategy": "...",
                   "captured_at": "... with timezone", "report_url": "https://pagespeed.web.dev/analysis/..."}
    sections: list of {"heading": "...", "paragraphs": ["...", "..."]}

The first run is the labeled footer reference. Use null when a timestamp or
report link is unavailable. Include all audit details in sections as plain text.
Optional labels map: sources, reference, missing_time, missing_link.
"""
import argparse
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

REPOSITORY = "https://github.com/lulubumps/pagespeed-audit-skill"
AUTHOR_CREDIT = "Skill desarrollada por Lulubumps"


def report_url(value):
    if not value:
        return None
    url = urlsplit(value)
    if (url.scheme != "https" or url.netloc != "pagespeed.web.dev"
            or not url.path.startswith("/analysis/")):
        raise ValueError("Use a verified PageSpeed Insights report URL")
    return value


def build(report, output):
    styles = getSampleStyleSheet()
    styles["BodyText"].leading = 15
    styles["BodyText"].spaceAfter = 8
    styles["Heading2"].textColor = colors.HexColor("#174EA6")
    labels = {
        "sources": "Mediciones y fuentes",
        "reference": "Test PSI de referencia",
        "missing_time": "fecha y hora no disponibles",
        "missing_link": "enlace no disponible",
        **report.get("labels", {}),
    }
    runs = report["runs"]
    urls = [report_url(run.get("report_url")) for run in runs]
    reference = runs[0] if runs else {}
    source_url = urls[0] if urls else None
    ai_credit = report["ai_credit"]
    if not ai_credit.strip():
        raise ValueError("Specify the AI actually used")
    story = [Paragraph(escape(report["title"]), styles["Title"])]

    for section in report["sections"]:
        story.append(Paragraph(escape(section["heading"]), styles["Heading2"]))
        for paragraph in section["paragraphs"]:
            story.append(Paragraph(escape(paragraph).replace("\n", "<br/>"), styles["BodyText"]))

    story.append(Paragraph(escape(labels["sources"]), styles["Heading2"]))
    for run, link in zip(runs, urls):
        stamp = run.get("captured_at") or labels["missing_time"]
        source = f"{run['page']} · {run['strategy']} · {stamp}"
        story.append(Paragraph(escape(source), styles["BodyText"]))
        link_text = ('<link href="' + escape(link, quote=True) + '" color="#174EA6">'
                     + escape(link) + "</link>") if link else escape(labels["missing_link"])
        story.append(Paragraph(link_text, styles["BodyText"]))
        story.append(Spacer(1, 4))

    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=48, rightMargin=48,
                            topMargin=48, bottomMargin=82, title=report["title"],
                            author=ai_credit)

    def footer(canvas, document):
        canvas.saveState()
        left = document.leftMargin
        right = A4[0] - document.rightMargin
        canvas.setStrokeColor(colors.HexColor("#D0D9E6"))
        canvas.line(left, 66, right, 66)
        canvas.setFont("Helvetica", 8)
        date = reference.get("captured_at") or labels["missing_time"]
        lines = [
            (f"{labels['reference']} · {date}", source_url),
            (ai_credit, source_url),
            (AUTHOR_CREDIT, REPOSITORY),
        ]
        for (label, link), y in zip(lines, (53, 41, 29)):
            canvas.setFillColor(colors.HexColor("#174EA6" if link else "#334155"))
            canvas.drawString(left, y, label)
            if link:
                width = canvas.stringWidth(label, "Helvetica", 8)
                canvas.linkURL(link, (left, y - 2, left + width, y + 8), relative=0)
        canvas.setFillColor(colors.HexColor("#334155"))
        canvas.drawRightString(right, 29, str(document.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(json.loads(args.input.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
