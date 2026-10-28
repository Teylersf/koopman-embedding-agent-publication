# Source and scope

The object examined is **arXiv:2609.28999v2**, by Thibault Fredon, Abhay K. Ram,
Fabrice Debbasch, Julien Zylberman, and Nuno F. Loureiro, *On the numerical
limitations of dual Koopman von Neumann embeddings for solving conservative
nonlinear ordinary differential equations on quantum computers*.

- [Versioned abstract](https://arxiv.org/abs/2609.28999v2)
- [Versioned PDF](https://arxiv.org/pdf/2609.28999v2)
- [Versioned HTML](https://arxiv.org/html/2609.28999v2)
- [Versioned TeX archive](https://arxiv.org/src/2609.28999v2)
- First submission: 24 September 2026; v2 revision: 25 September 2026,
  21:21:38 UTC. The v2 PDF stamp also states 25 September.
- PDF length: 17 pages; byte length: 959,353.
- SHA-256: `f895d195c935bcc9e3d0b14d2499f59aa497b8fcdce7d69f13fbc74d10301add`.
- The user-supplied PDF and a fresh download of the versioned arXiv PDF are
  byte-identical.

On 28 October 2026, the official arXiv record still listed v2 as its latest
version and did not list a journal reference. A bounded search of the exact
identifier/title with correction and erratum terms did not identify a dedicated
correction. That search does not establish that none exists. No claim is made
about an unexamined manuscript, future revision, or version of record.

No source author has been contacted, and no author confirmation is claimed.
The rendered
[Matilda work page](https://matilda.science/work/e0280fa0-9dbb-4f04-8567-6b3b05efadff?l=en),
checked on 28 October 2026, displays `Created date: 2026/09/25` and
`Matilda last update: 2026/10/01`. Its one associated arXiv entry
(`arxiv-arxiv_oai:arXiv.org:2609.28999`) displays:

- `Created date: 2026/09/25`
- `Publication date: 2026/09/29`
- `Source last update: 2026/09/29`
- `Matilda last update: 2026/09/30`

That entry links to the unversioned arXiv abstract and PDF, not a separately
identified revised manuscript. Matilda's
[metadata explanation](https://matilda.science/faq#i206) says version metadata
are displayed when available from the original data source; the inspected
explanation does not specify how these date fields map to arXiv revision
history. A fresh check of the official arXiv record still listed v2 revised
25 September 2026, 21:21:38 UTC, with no later revision or journal reference.
The v2 PDF stamp also states 25 September. We do not infer a distinct scientific
revision, announcement date, or harvesting event from the aggregator fields.

## Independent TeX provenance

One ordinary public request to the versioned source archive returned HTTP 200
on 28 October 2026. It supplied 740,540 bytes with SHA-256
`663a2a2296ad605607c47baa1854fafd76124593cb4f92bf8e209e76da6516e2`.
The archive's original `Limit.tex` is 99,001 bytes with SHA-256
`cd636885026f6567d9cfa922ac4d3f77f6f9bf25d6f5cf482ed775b282174112`.
Local extraction checked member paths, rejected unsafe paths/links, and selected
only TeX/bibliography files. No archive or whole source file is published here.

The [selective excerpts](source-excerpts/README.md) preserve 165 original source
lines in six short files, with explicit omissions, original filenames and
line numbers, primary HTML anchors, and [checksums](source-excerpts/manifest.json).
The [independent verifier](source-excerpts/verify.py) checks a separately obtained
archive and matches every excerpt against the exact `Limit.tex` bytes without
extracting archive members to disk. Source comments are not treated as published
assertions. In particular, active source line 1380 explicitly defines
`x_i(x,t)` as the coordinate value after a translation; it does not define it as
the displacement alone.

Equation references in this note use the **PDF numbering**. The HTML converter
renumbers some appendix equations, so a different HTML equation number is not
itself an error in the original work. Targeted formulas and assumptions were
checked against the PDF's rendered pages as well as extracted text.
The targeted passages were subsequently checked against the exact original TeX.

The central target passages are:

| PDF location | Subject | Exact TeX evidence |
|---|---|---|
| pp. 5-6, Eqs. (30)-(31); p. 13, Eq. (C1) | Geometric separation definition and small-deformation criterion | [789–825](source-excerpts/geometric-eq30-31.txt), [1376–1384](source-excerpts/appendix-c-coordinate.txt) |
| pp. 14-15, Eqs. (D8)-(D10) and following prose | Phase fringe, variance, and claimed inference limit | [1568–1607, 1614–1616](source-excerpts/grover-eqD8-D10.txt) |
| p. 6, Section V after Eq. (35) | Sampling-cost covariance prefactor | [912](source-excerpts/observable-eq35-sampling.txt) |
| pp. 5 and 7, Eqs. (22)-(25), (45) | Ehrenfest-Reynolds definitions and Lotka-Volterra calibration | [653–674, 690–700, 1030–1037](source-excerpts/reynolds-definitions-eq45.txt) |
| p. 6, Eq. (35) and preceding regularity assumption | Gaussian observable expansion and remainder | [888–904](source-excerpts/observable-eq35-sampling.txt) |
| p. 4, Section IV.B | Disclosed Gaussian and constant-covariance assumptions | [561–565, 631–642](source-excerpts/disclosed-closures.txt) |
| p. 12, Appendix B.2 | Covariance evolution and matrix-norm estimate | Rendered PDF and original TeX inspected; no additional excerpt redistributed |

The original paper correctly identifies the distinction between the evolution
of a probability distribution and that of its mean. Its Gaussian/moment closure
and constant-covariance approximation are explicitly disclosed. This correction
does not count those disclosed assumptions as newly discovered errors, and does
not claim that the Koopman-von Neumann framework or all quantum nonlinear-ODE
solvers fail.

The original PDF is not redistributed in this repository. Its arXiv license is
the perpetual nonexclusive distribution license, not a blanket license for a
third party to relicense it. Short attributed quotations and targeted formulas
support the mathematical criticism; the new manuscript, proofs, code, and plots
are separate work.

# Primary references checked

The bibliography contains nine relevant primary works. Full-text PDFs of the
eight papers were opened and the portions used in the manuscript were inspected.
For the added directional-statistics book, publisher metadata and the Chapter 2
table of contents were checked; the full chapter was not accessible from the
ordinary public publisher link. Bibliographic DOIs and publication metadata were
checked against official arXiv/publisher records and Crossref registration
metadata where applicable. This distinction is an access limit, not a claim to
have read unavailable text.

| Key | Work and verified identifier | Role |
|---|---|---|
| `original` | Fredon et al., arXiv:2609.28999v2 | Audited source |
| `bhmt` | Brassard et al. (2002), DOI [10.1090/conm/305/05215](https://doi.org/10.1090/conm/305/05215) | Standard amplitude estimation, Theorem 12 |
| `aaronsonrall` | Aaronson and Rall (2020), DOI [10.1137/1.9781611976014.5](https://doi.org/10.1137/1.9781611976014.5); checked arXiv:1908.10846v6 | QFT-free amplitude estimation, Section 3 |
| `rall` | Rall (2020), DOI [10.1103/PhysRevA.102.022408](https://doi.org/10.1103/PhysRevA.102.022408); arXiv:2004.06832v3 | Observable estimation, Lemma 5 |
| `joseph` | Joseph (2020), DOI [10.1103/PhysRevResearch.2.043102](https://doi.org/10.1103/PhysRevResearch.2.043102); arXiv:2003.09980v4 | KvN simulation and observable estimation context |
| `transport` | Zylberman et al., arXiv:2508.15691v2 | Related split transport construction |
| `rallcoherent` | Rall (2021), DOI [10.22331/q-2021-10-19-566](https://doi.org/10.22331/q-2021-10-19-566); checked arXiv:2103.09717v4 | Coherent estimation assumptions and query accounting |
| `montanaro` | Montanaro (2015), DOI [10.1098/rspa.2015.0301](https://doi.org/10.1098/rspa.2015.0301); checked arXiv:1504.06987v3 | Variance-aware mean estimation and sampling distinction |
| `directional` | Mardia and Jupp, *Directional Statistics*, DOI [10.1002/9780470316979](https://doi.org/10.1002/9780470316979); Chapter 2, pp. 13–24 | Established directional/circular-statistics context; publisher metadata and chapter contents inspected |

Wiley's DOI page and Crossref registration list the directional-statistics book
as 1999, and Wiley's catalogue lists the hardcover in November 1999. The
bibliography follows that primary publisher year. The standard resultant/circular
mean distinction is not claimed as a new discovery; the manuscript supplies its
own exact fringe derivation and source-specific counterexamples. The publisher's
[Chapter 2 page](https://onlinelibrary.wiley.com/doi/10.1002/9780470316979.ch2)
identifies location, concentration/dispersion, and trigonometric moments as its
topics; the attempted public PDF request redirected to the abstract page.

The optional arXiv DOI field was omitted from the source bibliography and its
submission link field. The official arXiv page identifies this DOI as issued
through DataCite. A Crossref-only lookup failure does not establish an invalid
DOI; the versioned arXiv URL remains the canonical locator for this audit.

Version distinctions matter: Aaronson-Rall v6 explicitly corrects an earlier
algebraic error and numbers its amplitude-estimation statement Theorem 3.
Rall's 2021 publisher page identifies v3 as the published version and v4 as a
later benchmarking correction. Montanaro v3 corrects a total-variation-distance
complexity result. This note uses those works for their specified estimation
results and does not equate their checked preprints with every published detail.

The source-specific counterexamples are the contribution of this correction.
The characteristic-function identity, elementary covariance identities,
Taylor estimates, and standard amplitude-estimation algorithms are not claimed
as new general theory.
