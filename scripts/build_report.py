import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Inches
from docx.text.paragraph import Paragraph
from lxml import etree

from paper_content import AUTHOR, REFERENCES, SECTIONS, TITLE


ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("template", type=Path)
args = parser.parse_args()
body_words = len(" ".join(content for _, content in SECTIONS).split())
all_words = len((" ".join(h + " " + c for h, c in SECTIONS)
                 + " References " + " ".join(r for r, _ in REFERENCES)).split())
assert 1500 <= body_words <= 2000
assert all_words <= 2000
doc = Document(args.template)
patterns = [deepcopy(p._p) for p in doc.paragraphs]
styles = doc.styles.element.xml
section = etree.tostring(doc.sections[0]._sectPr, method="c14n", exclusive=True)
headers = {str(p.partname): p.blob for p in doc.part.package.parts
           if "header" in p.content_type or "footer" in p.content_type}
body = doc._element.body
for child in list(body):
    if child is not doc.sections[0]._sectPr:
        body.remove(child)


def append(index, text=""):
    element = deepcopy(patterns[index])
    paragraph = Paragraph(element, doc._body)
    properties = deepcopy(paragraph.runs[0]._r.rPr) if paragraph.runs else None
    for child in list(element):
        if child is not element.pPr:
            element.remove(child)
    body.insert(len(body) - 1, element)
    paragraph = Paragraph(element, doc._body)
    run = paragraph.add_run(text)
    if properties is not None:
        run._r.insert(0, properties)
    return paragraph


def page_break():
    append(13).runs[0].add_break(WD_BREAK.PAGE)


cover = {4: TITLE, 6: AUTHOR, 7: "Udacity", 8: "Project 7 — Integrative Industry Synthesis"}
for index in range(11):
    append(index, cover.get(index, ""))
page_break()
append(14, TITLE)
markdown = f"# {TITLE}\n\n{AUTHOR}\n\n"
for heading, content in SECTIONS:
    append(19, heading)
    for paragraph in content.split("\n\n"):
        append(15, paragraph)
    markdown += f"## {heading}\n\n{content}\n\n"
page_break()
append(19, "Figure 1")
append(1).runs[0].add_picture(str(ROOT / "outputs/architecture_diagram.png"), width=Inches(6.5))
caption = ("Note. Project 6's LLM selects actions within enforced guards for "
           "Project 3's model; predictions feed Project 2-style statistical "
           "interpretation. Findings, failures and budget limits retain human "
           "authority. No automatic allocation or source-data edits occur.")
append(15, caption)
page_break()
append(37, "References")
markdown += "## References\n\n"
for reference, italic_span in REFERENCES:
    p = append(38)
    properties = deepcopy(p.runs[0]._r.rPr)
    for run in list(p.runs):
        p._p.remove(run._r)
    before, after = reference.split(italic_span, 1)
    for value, italic in [(before, False), (italic_span, True), (after, False)]:
        run = p.add_run(value)
        if properties is not None:
            run._r.insert(0, deepcopy(properties))
        run.italic = italic
    markdown += reference + "\n\n"
doc.core_properties.title = TITLE
doc.core_properties.author = AUTHOR
doc.core_properties.subject = cover[8]
doc.core_properties.comments = "AI assistance disclosed. Instructor and due date not supplied."
assert doc.styles.element.xml == styles
assert etree.tostring(doc.sections[0]._sectPr, method="c14n", exclusive=True) == section
assert headers == {str(p.partname): p.blob for p in doc.part.package.parts
                   if "header" in p.content_type or "footer" in p.content_type}
doc.save(ROOT / "module_summary.docx")
(ROOT / "module_summary.md").write_text(markdown.rstrip() + "\n")
subprocess.run(["libreoffice", "-env:UserInstallation=file:///tmp/synthesis-report-office",
                "--headless", "--convert-to", "pdf", "--outdir", str(ROOT),
                str(ROOT / "module_summary.docx")], check=True)
(ROOT / "outputs/report_template_audit.json").write_text(json.dumps({
    "template_url": "https://docs.google.com/document/d/1cv_MjQVKnGc9sbaYiOUna2155jMEvUxACwyDax-XYWI/edit",
    "template_sha256": hashlib.sha256(args.template.read_bytes()).hexdigest(),
    "styles_preserved": True, "section_preserved": True, "headers_preserved": True,
    "body_words_whitespace": body_words,
    "body_headings_and_references_words_whitespace": all_words,
    "full_visible_document_words_including_cover_and_caption": len(" ".join(p.text for p in doc.paragraphs).split()),
    "omitted_fields": ["Instructor", "Due date"],
    "pdf_font": "Liberation Sans substitutes for retained Arial DOCX styles",
}, indent=2) + "\n")
print("Body words:", body_words, "| including headings/references:", all_words)
