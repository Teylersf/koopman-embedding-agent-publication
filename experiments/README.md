# Reproduce the checks and figures

These deterministic classical calculations support selected corrections to
arXiv:2609.28999v2. They do not run quantum hardware, establish a speedup, or
constitute an exhaustive audit.

Checked environment: Python 3.12.14, NumPy 2.3.5, Matplotlib 3.11.2.

From the repository root:

```sh
python -m pip install numpy==2.3.5 matplotlib==3.11.2
python -X utf8 experiments/verify.py
python -X utf8 experiments/make_figures.py
```

`verify.py` runs seven groups and writes `results/verification.json` plus an
authentic author-environment execution record in `results/execution.log`.
The latter records the environment, script hash, assertion status, output hash,
and complete JSON. It is not independent human review or certification.

The groups cover:

1. The printed geometric measure's nonzero initial separation, its exact
   lower bound under the stated directional maps, and a candidate repair.
2. Direct finite-grid Hadamard amplitudes, a characteristic-function identity,
   symmetric packets with positive variance and zero phase bias, and the
   difference between ancilla and coordinate sampling variances.
3. Two explicit positive four-point distributions with identical entire
   reference-phase fringes but different arithmetic means.
4. The Lotka--Volterra Ehrenfest--Reynolds parameter computed from the source's
   own paired gradient/Hessian definitions.
5. A bounded C2 observable with a cubic rather than quartic Gaussian remainder,
   checked against an exact conditioned-Gaussian formula and independent
   numerical quadrature.
6. Supporting covariance-transpose, dimension-constant, and width-normalization
   inconsistencies. The larger main-text constant repairs the matrix bound;
   this example does not refute every main-text estimate.
7. A nontrivial complete conservative flow with packet width proportional to
   the time step. Vectorized RK4 refinement checks the numerical calculation;
   the width-uniform remainder estimate is proved separately in the paper.

All inputs are analytic or declared finite grids. No external dataset,
original-paper PDF, local account, network access, or other project directory
is required. Exact finite-grid algebra is evaluated up to floating-point
rounding. Geometry maxima are sampled on 65,537 boundary directions; the
lower bound of one and the candidate displacement value also have independent
analytic checks.

The plotting script generates publication figures as vector PDF and PNG:
`geometry-criterion` and `phase-inference`. PDF metadata credits Taylor Kalin.
`results/figure-manifest.json` records figure hashes and package versions.

To write an independent verification output without replacing the checked-in
record:

```sh
python -X utf8 experiments/verify.py --output /your/path/verification.json --log /your/path/execution.log
```

The verification JSON is deterministic in the checked environment. Execution
timestamps and elapsed time change between runs; PDF creation metadata also
changes. Cross-platform floating-point results may differ in final digits.
