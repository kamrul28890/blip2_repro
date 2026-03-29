# Term Paper Draft

This folder contains an ACL-style anonymous draft of the term paper:

- `term_paper.tex`
- `term_paper.bib`
- `acl.sty`
- `acl_natbib.bst`

## Build

From the `paper/` directory:

```powershell
pdflatex term_paper.tex
bibtex term_paper
pdflatex term_paper.tex
pdflatex term_paper.tex
```

The expected output is `term_paper.pdf`.

## Content Coverage

The draft includes:

- critique of all three selected papers,
- explanation of why BLIP-2 was chosen,
- implementation details,
- experimental setup,
- quantitative comparison against the BLIP-2 paper,
- qualitative failure analysis,
- discussion of compute and reproducibility.
