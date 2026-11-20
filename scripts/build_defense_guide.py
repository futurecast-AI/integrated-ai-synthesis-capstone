from pathlib import Path
import subprocess

from docx import Document
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
doc = Document()
section = doc.sections[0]
section.top_margin = section.bottom_margin = Inches(.7)
normal = doc.styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(10)
normal.paragraph_format.space_after = Pt(5)
for line in (ROOT / "DEFENSE_UPDATE.md").read_text().splitlines():
    if not line.strip():
        continue
    if line.startswith("# "):
        doc.add_heading(line[2:], 0)
    elif line.startswith("## "):
        doc.add_heading(line[3:], 1)
    elif line.startswith("### "):
        doc.add_heading(line[4:], 2)
    else:
        doc.add_paragraph(line.replace("**", "").replace("`", ""))
doc.core_properties.title = "Project 7 — Revised Study Guide and Adversarial Answers"
doc.core_properties.author = "AI Foundations (Edward Hickman)"
target = ROOT / "outputs/Project_7_Revised_Defense_Guide.docx"
doc.save(target)
subprocess.run(["libreoffice", "-env:UserInstallation=file:///tmp/synthesis-defense-office",
                "--headless", "--convert-to", "pdf", "--outdir", str(target.parent), str(target)], check=True)
