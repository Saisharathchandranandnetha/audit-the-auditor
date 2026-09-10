"""Build a self-contained HTML and a Google-Docs-importable DOCX manuscript."""
from __future__ import annotations

import base64
import html
from pathlib import Path
import re

import mistune
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report"


def plain(tokens):
    return "".join(" " if t["type"] in ("softbreak", "linebreak") else t.get("raw", plain(t.get("children", []))) for t in tokens)


def inline(paragraph, tokens):
    for token in tokens:
        kind = token["type"]
        if kind == "link":
            url = token["attrs"]["url"]
            link = OxmlElement("w:hyperlink")
            rid = paragraph.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
            link.set(qn("r:id"), rid)
            run = OxmlElement("w:r")
            props = OxmlElement("w:rPr")
            color = OxmlElement("w:color")
            color.set(qn("w:val"), "195A80")
            props.append(color)
            run.append(props)
            text = OxmlElement("w:t")
            text.text = plain(token.get("children", []))
            run.append(text)
            link.append(run)
            paragraph._p.append(link)
        elif kind in ("strong", "emphasis"):
            run = paragraph.add_run(plain(token.get("children", [])))
            run.bold = kind == "strong"
            run.italic = kind == "emphasis"
        elif kind == "codespan":
            run = paragraph.add_run(token.get("raw", ""))
            run.font.name = "Consolas"
            run.font.size = Pt(9)
        elif kind in ("softbreak", "linebreak"):
            paragraph.add_run(" " if kind == "softbreak" else "\n")
        elif kind == "image":
            path = (REPORT / token["attrs"]["url"]).resolve()
            paragraph.add_run().add_picture(str(path), width=Inches(6.2))
        else:
            paragraph.add_run(token.get("raw", plain(token.get("children", []))))


def blocks(doc, tokens):
    for token in tokens:
        kind = token["type"]
        if kind == "blank_line":
            continue
        if kind == "heading":
            doc.add_heading(plain(token.get("children", [])), level=min(token["attrs"]["level"], 4))
        elif kind in ("paragraph", "block_text"):
            p = doc.add_paragraph()
            inline(p, token.get("children", []))
        elif kind == "block_code":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(token["raw"].rstrip())
            run.font.name = "Consolas"
            run.font.size = Pt(8)
        elif kind == "list":
            style = "List Number" if token.get("attrs", {}).get("ordered") else "List Bullet"
            for item in token["children"]:
                children = item.get("children", [])
                for i, child in enumerate(children):
                    if child["type"] in ("block_text", "paragraph"):
                        p = doc.add_paragraph(style=style if i == 0 else None)
                        inline(p, child.get("children", []))
                    else:
                        blocks(doc, [child])
        elif kind == "table":
            head = next(t for t in token["children"] if t["type"] == "table_head")
            body = next(t for t in token["children"] if t["type"] == "table_body")
            table = doc.add_table(rows=1, cols=len(head["children"]))
            table.style = "Light Shading Accent 1"
            header = OxmlElement("w:tblHeader")
            table.rows[0]._tr.get_or_add_trPr().append(header)
            for cell, source in zip(table.rows[0].cells, head["children"]):
                inline(cell.paragraphs[0], source.get("children", []))
            for row in body["children"]:
                cells = table.add_row().cells
                for cell, source in zip(cells, row["children"]):
                    inline(cell.paragraphs[0], source.get("children", []))
            for row in table.rows:
                row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(8)
            doc.add_paragraph()
        elif kind == "block_quote":
            p = doc.add_paragraph(style="Quote")
            p.add_run(plain(token.get("children", [])))
        else:
            raise ValueError(f"Unsupported manuscript block: {kind}")


def main():
    summary = (REPORT / "executive_summary.md").read_text()
    main_text = (REPORT / "main_writeup.md").read_text()
    renderer = mistune.create_markdown(plugins=["table"])
    body = renderer(summary) + '<div class="page-break"></div>' + renderer(main_text)
    def embed(match):
        source = match.group(1)
        path = (REPORT / source).resolve()
        if not path.is_relative_to(ROOT) or not path.exists():
            raise ValueError(f"Invalid local manuscript image: {source}")
        mime = "image/png" if path.suffix == ".png" else "image/svg+xml"
        return f'src="data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"'
    body = re.sub(r'src="([^"]+)"', embed, body)
    css = """body{font:11pt/1.45 Georgia,serif;color:#182027;max-width:850px;margin:50px auto;padding:0 25px}
    h1,h2,h3{font-family:Arial,sans-serif;line-height:1.18;break-after:avoid}h1{font-size:23pt}h2{font-size:17pt}h3{font-size:13pt}
    table{border-collapse:collapse;width:100%;font:9pt/1.3 Arial,sans-serif;margin:16px 0}th,td{border:1px solid #bcc4cb;padding:7px;text-align:left}th{background:#edf2f4}
    img{max-width:100%;height:auto}pre{background:#f3f5f6;padding:12px;white-space:pre-wrap;font-size:9pt}code{font-size:.87em}a{color:#195a80}
    .page-break{break-before:page;margin-top:60px}@page{size:A4;margin:18mm} @media print{body{margin:0;padding:0;max-width:none} .page-break{margin:0} tr,img{break-inside:avoid}}"""
    (REPORT / "submission.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Audit the Auditor</title><style>' + css + '</style><body>' + body + '</body></html>')

    doc = Document()
    section = doc.sections[0]
    section.top_margin = section.bottom_margin = Inches(.75)
    section.left_margin = section.right_margin = Inches(.8)
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.08
    for name in ["Heading 1", "Heading 2", "Heading 3"]:
        doc.styles[name].font.color.rgb = RGBColor.from_string("1B4E65")
    doc.core_properties.title = "Audit the Auditor: A Coding-Agent Monitoring Audit"
    doc.core_properties.author = "MATS applicant — AI-assisted research draft"
    doc.core_properties.subject = "Retrospective measurement audit; applicant review required"
    footer = section.footer.paragraphs[0]
    footer.add_run("Page ")
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    parser = mistune.create_markdown(renderer="ast", plugins=["table"])
    blocks(doc, parser(summary))
    main_start = len(doc.paragraphs)
    blocks(doc, parser(main_text))
    doc.paragraphs[main_start].paragraph_format.page_break_before = True
    doc.save(REPORT / "submission.docx")
    print(f"Wrote {REPORT / 'submission.docx'} and standalone submission.html")


if __name__ == "__main__":
    main()
