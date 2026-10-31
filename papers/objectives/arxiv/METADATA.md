# arXiv submission metadata

Upload: arxiv/objectives_arxiv.zip (one .tex file with the bibliography inline, no figures;
ancillary files anc/verify_objectives.py and anc/numerics.json). arXiv compiles with pdflatex;
the packages used (geometry, amsmath, amssymb, amsthm, natbib, array, booktabs, xcolor, hyperref)
are all in its TeX Live. Rebuild the zip with `python3 arxiv/make_zip.py` after editing paper.tex.

Title: Consistent Objectives for Self-Improving Systems: Absolute, Relative and Evolutionary Assessment Over Short and Long Horizons
Authors: Peter Cotton
Primary category: cs.AI
Cross-list: cs.LG
Comments: 9 pages. A script that certifies every proposition numerically (closed form against
Monte Carlo or enumeration) is included as an ancillary file.
License: arXiv non-exclusive license, or CC BY 4.0 if the note is to be reused freely.
Abstract: paste arxiv/abstract.txt (plain text; arXiv accepts $...$ math).

SSRN, if posted the same day: same title and abstract; keywords: self-improving systems,
evaluation, objectives, log return, Kelly, win rate, evaluator drift; discipline: computer science
(artificial intelligence) and economics (decision theory).

After it is announced: put the arXiv id on the metareasoning papers page and in
microprediction/home papers.json (drop the arxiv_pending line in posted.json).
