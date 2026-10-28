# Prior work and contribution boundaries

Checked on 28 October 2026 using primary papers, official arXiv records,
publisher pages, and DOI registration metadata. A bounded exact-identifier/title
search did not identify a dedicated correction to arXiv:2609.28999. This is not
an exhaustive novelty search and does not establish priority over every earlier
discussion or unpublished communication.

## Closest methodological sources

- **Fredon et al., arXiv:2609.28999v2.** This is the direct correction target.
  It already distinguishes cloud-to-trajectory error, sampling error, and
  inference error, and explicitly states Gaussian and constant-covariance
  approximations. The new note must preserve those disclosures.
- **Joseph, Physical Review Research 2, 043102 (2020).** KvN unitary simulation
  and amplitude-estimation-based observable readout predate the target paper.
  The correction does not introduce the general idea of simulating a phase-space
  distribution or estimating its observables. Relevant full-text discussion:
  resource comparison and observable estimation.
- **Zylberman et al., arXiv:2508.15691v2.** The related transport construction
  provides state preparation, split evolution, and measurement context. The
  present note addresses geometric and readout claims in the later embedding
  paper, not an exhaustive re-audit of this transport work.
- **Brassard-Hoyer-Mosca-Tapp, Contemporary Mathematics 305, 53-74 (2002).**
  Theorem 12 supplies the standard amplitude-estimation guarantee for the encoded
  success probability. Its oracle involves coherent preparation and inverse
  operations; its query count is not an end-to-end guarantee for every PDE
  implementation.
- **Aaronson-Rall, SOSA 2020, 24-32; checked arXiv v6.** Section 3/Theorem 3
  gives a QFT-free amplitude-estimation formulation with preparation-unitary
  access. The paper's v6 record says it repairs earlier algebra. Do not quote
  the older theorem numbering or constants as if they were checked unchanged.
- **Rall, Physical Review A 102, 022408 (2020).** Lemma 5 is a standard
  observable-estimation result under block-encoding and state-preparation
  assumptions. It establishes that the chosen observable expectation is the
  estimand; the correction's alternative mean encoding is not a new amplitude
  estimation algorithm.
- **Rall, Quantum 5, 566 (2021); checked arXiv v4.** Coherent estimation has
  access-model and state-preservation requirements distinct from independent
  shot sampling. This source supports keeping query accounting separate from
  circuit-generation, state-preparation, and full-solver costs.
- **Montanaro, Proceedings of the Royal Society A 471, 20150301 (2015);
  checked arXiv v3.** Variance-aware estimation concerns the variance of the
  actual random output. This is relevant to distinguishing a coordinate sample
  from a Bernoulli ancilla, rather than replacing one variance by another.
- **Mardia and Jupp, Directional Statistics, Wiley (publisher-listed 1999),
  DOI [10.1002/9780470316979](https://doi.org/10.1002/9780470316979).**
  Chapter 2, *Summary Statistics*, pp. 13–24, covers directional location,
  concentration/dispersion, and trigonometric moments. The circular mean and
  resultant interpretation is established directional-statistics context;
  this correction's contribution is its application to the source's precise
  phase-floor argument and its explicit counterexamples. Publisher metadata and
  the chapter contents were inspected, but the full chapter could not be read
  through the ordinary public PDF link, which redirected to the abstract page.
  The manuscript therefore includes its own mathematical derivation rather than
  relying on an unchecked quotation or theorem from the book.

## Contribution of this note

The contribution is source-specific: an exact obstruction to the printed
geometric criterion, exact interpretation and counterexamples for the proposed
phase fringe, corrected sampling and numerical parameter calculations, and
regularity/covariance repairs supported by reproducible examples. Elementary
flow expansions, characteristic-function identities, Gaussian moments, and
ordinary amplitude estimation are standard ingredients. No general novelty is
claimed for those ingredients or for the broad KvN framework.

The source-specific statements must be tied to v2. A rigorous repair of a
definition or estimator is distinct from proving that the original practical
benchmarks fail. The latter would require consistent original initializations,
implementation details, and grid/time refinement; their qualitative plots alone
do not establish that stronger claim.

## Exact source and date verification

The [selective source archive evidence](../source-excerpts/README.md) links all
central criticism to the exact arXiv v2 `Limit.tex`, including the explicit
post-translation coordinate definition at line 1380, and preserves the source's
Gaussian/constant-covariance disclosures. The original archive and source file
have independently checkable SHA-256 hashes; whole source files are not
redistributed. The official v2 history and PDF stamp state 25 September 2026.
The rendered Matilda record labels 29 September as both Publication date and
Source last update for its associated arXiv entry. That entry links to the same
unversioned arXiv record and does not identify a separate revision. Its metadata
documentation does not specify how those date fields map to arXiv's revision
history; no distinct scientific revision is inferred. Exact labels and access
details are recorded in [SOURCE.md](../SOURCE.md). No source authors were
contacted, and no author confirmation or unpublished revision knowledge is claimed.
