# Reproduce the correction checks

From this repository root, with Python 3.12:

```sh
python -m pip install -r requirements.txt
python -X utf8 experiments/verify.py
python -X utf8 experiments/make_figures.py
```

The executable names and paths match the canonical execution log. The six
verification groups and figure calculations use declared analytic inputs and
finite grids. No account, original-paper PDF, external dataset, network access,
or adjacent canonical checkout is needed to run them.

The `experiments/`, `figures/`, `results/`, and `requirements.txt` files were
copied byte-for-byte from the canonical Taylor Kalin repository. See
`adapter-checks.json` for hashes. Running the commands regenerates output and
timestamps; compare numerical JSON fields rather than expecting identical
execution timestamps or PDF metadata.

The copied `results/artifact-manifest.json` is the **canonical** artifact
inventory. It intentionally includes canonical paths such as `paper/main.pdf`
that are not copied here. The canonical PDF and source are available at
https://github.com/Teylersf/koopman-embedding-corrections/releases/tag/v1.1.0.
The agent package's actual copied files are inventoried by `adapter-checks.json`.

`prepare_packages.py` is a packaging utility, separate from numerical
reproduction. It requires the adjacent canonical checkout and writes local
AgentPub/AAES payloads without authentication, API submission, or Git operations.
It verifies that all mathematical segments and proof headings are retained.
Before a later submission, rerun it with verified review/publication context:

```sh
python reproduction/prepare_packages.py --publishfun-state published --publishfun-public-id VERIFIED_PF_ID --airaxiv-public-id VERIFIED_AIRAXIV_ID
```

Only use actual verified identifiers. While the context says `under_review` or `revision_requested`,
the review-sequence gate is false and the agent venues must wait.
