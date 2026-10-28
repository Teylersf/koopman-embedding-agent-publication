# Selective primary-source evidence

These six short, attributed excerpts reproduce only the passages needed to
check the corrections. The full source archive, TeX file and original PDF are
not redistributed. The quoted material remains the work of Thibault Fredon,
Abhay K. Ram, Fabrice Debbasch, Julien Zylberman and Nuno F. Loureiro.

The source is the [versioned arXiv TeX archive](https://arxiv.org/src/2609.28999v2),
retrieved by one ordinary public request on 28 October 2026 (HTTP 200):

- Archive: 740,540 bytes; SHA-256
  `663a2a2296ad605607c47baa1854fafd76124593cb4f92bf8e209e76da6516e2`.
- Original file `Limit.tex`: 99,001 bytes; SHA-256
  `cd636885026f6567d9cfa922ac4d3f77f6f9bf25d6f5cf482ed775b282174112`.
- [PDF](https://arxiv.org/pdf/2609.28999v2): 959,353 bytes; SHA-256
  `f895d195c935bcc9e3d0b14d2499f59aa497b8fcdce7d69f13fbc74d10301add`.

Each text file preserves the original UTF-8 source lines after the marked
header. Numbers are 1-based original `Limit.tex` line numbers; blank and comment
lines count. Noncontiguous selections are explicitly marked. No published
assertion is inferred from commented-out text.

| Excerpt | Original lines | PDF locator | Primary HTML anchor |
|---|---|---|---|
| [Geometric definition and criterion](geometric-eq30-31.txt) | 789–825 | pp. 5–6, (30)–(31) | [(30)](https://arxiv.org/html/2609.28999v2#S4.E30), [(31)](https://arxiv.org/html/2609.28999v2#S4.E31) |
| [Coordinate after translation](appendix-c-coordinate.txt) | 1376–1384 | p. 13, (C1) and following definition | [Appendix C](https://arxiv.org/html/2609.28999v2#A3.p2) |
| [Observable expansion and sampling](observable-eq35-sampling.txt) | 888–904; 912 | p. 6, (35), assumptions and subsequent shot count | [(35)](https://arxiv.org/html/2609.28999v2#S5.E35) |
| [Reynolds definitions and LV calibration](reynolds-definitions-eq45.txt) | 653–674; 690–700; 1030–1037 | pp. 5, 7, (22)–(25), (45) | [(22)](https://arxiv.org/html/2609.28999v2#S4.E22), [(45)](https://arxiv.org/html/2609.28999v2#S6.E45) |
| [Fringe, variance and precision claim](grover-eqD8-D10.txt) | 1568–1607; 1614–1616 | pp. 14–15, (D8)–(D10) and subsequent prose | [D.3](https://arxiv.org/html/2609.28999v2#A4.SS3) |
| [Explicit closure assumptions](disclosed-closures.txt) | 561–565; 631–642 | p. 4, IV.B | [IV.2](https://arxiv.org/html/2609.28999v2#S4.SS2) |

The primary HTML converter renumbers appendix equations consecutively: its
`A3.E58` is PDF (C1), and `A4.E68`–`A4.E70` correspond to PDF (D8)–(D10).
The numbered PDF and exact TeX lines take precedence over converter numbering.

To verify independently, download the versioned archive into a local temporary
folder, then run from the repository root:

```text
python source-excerpts/verify.py PATH_TO_DOWNLOADED_ARCHIVE
```

The verifier checks the complete archive hash, reads `Limit.tex` without
extracting archive members to disk, checks its exact hash, and matches every
selected line and every excerpt-file hash against [manifest.json](manifest.json).
It makes no network requests. A hash mismatch means a different byte artifact;
it is not evidence by itself of a mathematical change.

The official [arXiv history](https://arxiv.org/abs/2609.28999v2) records v1 on
24 September 2026 and v2 on 25 September 2026, 21:21:38 UTC. The v2 PDF stamp
also says 25 September. The rendered
[Matilda record](https://matilda.science/work/e0280fa0-9dbb-4f04-8567-6b3b05efadff?l=en)
labels 29 September as both Publication date and Source last update for its
associated arXiv entry. It links to the unversioned arXiv record and does not
identify a separate revised manuscript. The inspected metadata explanation
does not define the mapping to arXiv revision dates. The manuscript uses the
versioned primary-record date; no distinct scientific revision is inferred from
the aggregator fields. [SOURCE.md](../SOURCE.md) records the exact labels.
No source author has been contacted and no author confirmation is claimed.
