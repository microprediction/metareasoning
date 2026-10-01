# metareasoning (view as [web page](https://metareasoning.microprediction.org))

Source for a curated map of research on metareasoning and self-improving research systems:
systems that decide what to compute, investigate or learn next, and that improve those decisions
from experience.

## The organising idea

A computation, query or experiment is worth running only if it might change a later decision.
Its value is

```
VOC(c) = E_c[ max_a E[U(a) | s·c] ] - max_a E[U(a) | s] - cost(c)
```

the expected utility of acting after the computation, less the utility of acting now, less its
cost. Metareasoning is the choice of computations by this quantity. Learned metareasoning
estimates it from logged histories, with resolved outcomes supplying the labels.

## Pages

| Page | Contents |
|---|---|
| `index.html` | The thesis, the state of play, further reading |
| `intro.html` | Object and meta level, the value of computation, neighbouring vocabularies, a reference architecture |
| `selection.html` | Classical metareasoning, information acquisition, metareasoning inside language models |
| `outcomes.html` | Proper scoring rules, forecasting benchmarks, training on resolved outcomes, delayed feedback |
| `agents.html` | Research agents, program search, quantitative research and trading agents, and their evaluations |
| `updating.html` | Self-improvement mechanisms: prompts, memory, code, weights |
| `data.html` | Relational deep learning, feature synthesis, text as data, weak supervision |
| `decisions.html` | Decision-focused learning, dynamic trading, off-policy evaluation, offline RL, causal estimation |
| `evaluation.html` | Data snooping, backtest overfitting, adaptive data analysis, leakage, look-ahead in language models |
| `bibliography.html` | Annotated bibliography, grouped by role |
| `papers.html` | Technical notes, with PDF, source and certificate |
| `implementations.html` | Open code, with repository status |
| `map.html` | d3 force-directed literature map, with the metareasoning literature inside a circle and a list of connections not yet made |
| `timeline.html` | d3 swimlane timeline across seven strands |

Plain static HTML with one shared `style.css`. No build step. KaTeX and d3 from CDN.

## Editorial rules

- Every arXiv identifier was resolved against the arXiv API and every journal DOI against Crossref;
  every GitHub URL was fetched. Repository statistics are as of 30 September 2026.
- Numbers are reported as the source reports them, with the benchmark they were measured on.
- Independent evaluations sit next to the results they test. Reported gains in this field often
  shrink under search-aware, leakage-safe evaluation.
- Gaps on the literature map are claims about absences, so each is written out with the searches
  behind it and a confidence level.

## Papers

`papers/objectives/` holds *Consistent Objectives for Self-Improving Systems*: `paper.tex`, and
`verify_objectives.py`, which checks every number in the note two ways and writes `numerics.json`.
The compiled PDF is served as `consistent-objectives.pdf`.

## Contributing

Open an issue or a PR. Useful contributions: a paper that belongs in the bibliography, a
correction to a date or a number, a gap edge that has since been closed, or a repository whose
maintenance status has changed.

## Deployment

GitHub Pages from the default branch, root directory. `CNAME` points at
`metareasoning.microprediction.org`.

## License

MIT — see `LICENSE`.
