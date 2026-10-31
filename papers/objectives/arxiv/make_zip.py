#!/usr/bin/env python3
"""Rebuild the arXiv upload: paper.tex at the top level, certificates under anc/."""
import shutil, zipfile
from pathlib import Path
here = Path(__file__).resolve().parent
src = here.parent
with zipfile.ZipFile(here / "objectives_arxiv.zip", "w", zipfile.ZIP_DEFLATED) as z:
    z.write(src / "paper.tex", "paper.tex")
    z.write(src / "verify_objectives.py", "anc/verify_objectives.py")
    z.write(src / "numerics.json", "anc/numerics.json")
print("wrote", here / "objectives_arxiv.zip")
