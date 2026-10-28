"""Generate the two scientific figures from explicit finite-grid calculations."""
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from verify import gaussian_weights

ROOT = Path(__file__).resolve().parents[1]


def main():
    out = ROOT / 'figures'
    out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 9,
                         'axes.labelsize': 9, 'axes.titlesize': 9,
                         'legend.fontsize': 7.7, 'xtick.labelsize': 8,
                         'ytick.labelsize': 8, 'pdf.fonttype': 42,
                         'mathtext.fontset': 'dejavuserif', 'axes.spines.top': False,
                         'axes.spines.right': False, 'savefig.dpi': 220})
    metadata = {'Author': 'Taylor Kalin',
                'Subject': 'Deterministic counterexamples for arXiv:2609.28999v2',
                'CreationDate': datetime.now(timezone.utc)}

    sigma = .01
    angles = np.linspace(0, 2 * math.pi, 65537)
    dq, dp = sigma * np.cos(angles), sigma * np.sin(angles)
    velocity_difference = np.sin(2 * math.pi * (.5 + dp))
    steps = np.linspace(0, .03, 151)
    raw = np.array([math.hypot(float(np.max(abs(dq + t * velocity_difference))), sigma)
                    / (math.sqrt(2) * sigma) for t in steps])
    repaired = steps * math.sin(2 * math.pi * sigma) / (math.sqrt(2) * sigma)
    fig, ax = plt.subplots(figsize=(6.3, 3.1), constrained_layout=True)
    ax.plot(steps, raw, color='#a52a2a', linewidth=2, label='Printed raw-separation measure')
    ax.plot(steps, repaired, color='#156a9c', linewidth=2, label='Candidate displacement measure')
    ax.axhline(.1, color='#555555', linestyle='--', linewidth=1, label='Published numerical guideline: 0.1')
    ax.axhline(1, color='#a52a2a', linestyle=':', linewidth=.8)
    ax.set(xlabel=r'Time step $\Delta t$', ylabel='Normalized separation / displacement',
           xlim=(0, .03), ylim=(-.03, 1.12))
    ax.text(.002, .83, r'$F(q,p)=(\sin 2\pi p,0)$' + '\n' + r'$x=(1/2,1/2),\ \sigma=0.01$', fontsize=9)
    ax.legend(loc='center right', frameon=False)
    ax.grid(axis='y', alpha=.2)
    fig.savefig(out / 'geometry-criterion.pdf', metadata={**metadata, 'Title': 'Raw separation and displacement criterion'})
    fig.savefig(out / 'geometry-criterion.png')
    plt.close(fig)

    references = np.linspace(.25, .75, 501)
    fig, (left, right) = plt.subplots(1, 2, figsize=(6.6, 3.15), constrained_layout=True)
    colors = ('#19749d', '#d57514', '#763a8f')
    for sigma, color in zip((.025, .05, .1), colors):
        x, weights = gaussian_weights(sigma)
        z = weights @ np.exp(2j * x)
        probabilities = .5 + .5 * np.real(np.exp(-2j * references) * z)
        left.plot(references, probabilities, linewidth=1.6, color=color, label=r'$\sigma=%.3g$' % sigma)
    left.axvline(.5, color='#555555', linewidth=.8, linestyle='--')
    left.set(title='(a) Same maximum, reduced contrast', xlabel=r'Reference phase $a$',
             ylabel=r'Ancilla probability $P_0(a)$', xlim=(.25, .75), ylim=(.927, 1.003))
    left.legend(loc='lower center', frameon=True, framealpha=.96, edgecolor='none')
    widths = np.linspace(.005, .1, 100)
    shifts, errors = [], []
    for sigma in widths:
        x, weights = gaussian_weights(float(sigma))
        mean = float(weights @ x)
        variance = float(weights @ (x - mean) ** 2)
        shifts.append(.5 * math.acos(1 - 2 * variance))
        errors.append(abs(float(np.angle(weights @ np.exp(2j * x)) / 2) - mean))
    right.plot(widths, shifts, color='#a52a2a', linewidth=1.8, label='Contrast reinterpreted as phase shift')
    right.plot(widths, errors, color='#156a9c', linewidth=2, label='Actual phase bias')
    right.set(title='(b) The phase-shift model fails', xlabel=r'Gaussian width parameter $\sigma$',
              ylabel='Phase error / alleged phase shift', xlim=(0, .102), ylim=(-.005, .11))
    right.legend(loc='upper left', frameon=False, fontsize=6.9)
    for ax in (left, right):
        ax.grid(alpha=.18)
    fig.savefig(out / 'phase-inference.pdf', metadata={**metadata, 'Title': 'Contrast loss without a phase shift'})
    fig.savefig(out / 'phase-inference.png')
    plt.close(fig)

    paths = [out / (stem + ext) for stem in ('geometry-criterion', 'phase-inference') for ext in ('.pdf', '.png')]
    manifest = {'matplotlib_version': matplotlib.__version__, 'numpy_version': np.__version__,
                'scope': 'Exact finite-grid Gaussian characteristic moments and a sampled shear-boundary maximum. Candidate displacement statistic is not asserted to be a global stability theorem.',
                'figures': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
    (ROOT / 'results/figure-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'figures_created': len(paths), 'matplotlib_version': matplotlib.__version__,
                      'files': [p.relative_to(ROOT).as_posix() for p in paths]}))


if __name__ == '__main__':
    main()
