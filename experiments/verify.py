"""Reproducible counterexamples for arXiv:2609.28999v2.

These are deterministic analytic and finite-grid checks, not quantum-hardware
experiments or an exhaustive audit. Run from any working directory.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "f895d195c935bcc9e3d0b14d2499f59aa497b8fcdce7d69f13fbc74d10301add"


def hadamard_probability(phase: np.ndarray, weights: np.ndarray) -> float:
    """Direct ancilla-zero norm after H, controlled exp(i phase), H."""
    component = np.sqrt(weights) * (1 + np.exp(1j * phase)) / 2
    return float(np.vdot(component, component).real)


def gaussian_weights(sigma: float, points: int = 4096):
    x = (np.arange(points) + .5) / points
    weights = np.exp(-.5 * ((x - .5) / sigma) ** 2)
    weights /= weights.sum()
    return x, weights


def geometry():
    sigma = .01
    angles = np.linspace(0, 2 * math.pi, 65537)
    dq, dp = sigma * np.cos(angles), sigma * np.sin(angles)
    velocity_difference = np.sin(2 * math.pi * (.5 + dp))
    rows = []
    for step in (0., 1e-6, 1e-4, 1e-3, .01, .03):
        raw_q = dq + step * velocity_difference
        delta_q, delta_p = float(np.max(abs(raw_q))), float(np.max(abs(dp)))
        raw_ratio = math.hypot(delta_q, delta_p) / (math.sqrt(2) * sigma)
        displacement_q = step * velocity_difference
        corrected_q = float(np.max(abs(displacement_q)))
        corrected_ratio = corrected_q / (math.sqrt(2) * sigma)
        exact_corrected = step * math.sin(2 * math.pi * sigma) / (math.sqrt(2) * sigma)
        assert raw_ratio >= 1 - 2e-14
        assert abs(corrected_ratio - exact_corrected) < 2e-14
        assert abs(raw_q[0] - sigma) < 2e-14
        rows.append({"dt": step, "sampled_raw_Delta_q": delta_q,
                     "raw_Delta_p": delta_p, "raw_Eq31_ratio": raw_ratio,
                     "raw_ratio_rigorous_lower_bound": 1.,
                     "corrected_displacement_ratio": corrected_ratio,
                     "exact_corrected_displacement_ratio": exact_corrected})
    assert abs(rows[0]["raw_Eq31_ratio"] - 1) < 1e-14
    assert rows[0]["corrected_displacement_ratio"] == 0
    # A compact symmetric packet has an exactly fixed mean for this shear.
    p = .5 + np.arange(-256, 257) / 4096
    w = np.exp(-.5 * ((p - .5) / sigma) ** 2)
    w /= w.sum()
    mean_velocity = float(w @ np.sin(2 * math.pi * p))
    assert abs(mean_velocity) < 1e-15
    return {"field": "F(q,p)=(sin(2*pi*p),0)",
            "Hamiltonian": "H=-cos(2*pi*p)/(2*pi)",
            "center": [.5, .5], "sigma": sigma,
            "directional_map": "Phi_dt(q,p)=(q+dt*sin(2*pi*p),p)",
            "boundary_sampling_points": len(angles),
            "analytic_obstruction": "The printed raw separation includes sigma*xi_i. At dt=0 each coordinate maximum equals sigma. For partial_i F_i=0, xi=e_i proves each directional maximum is at least sigma for all dt.",
            "candidate_repair": "Subtract the initial coordinate separation inside the absolute value. This displacement statistic vanishes as dt->0; no global stability theorem is claimed for it.",
            "compact_symmetric_packet_mean_velocity": mean_velocity, "rows": rows,
            "all_assertions_passed": True}


def phase_and_sampling():
    rows = []
    for sigma in (.01, .025, .05, .1):
        x, w = gaussian_weights(sigma)
        mean = float(w @ x)
        variance = float(w @ (x - mean) ** 2)
        z = w @ np.exp(2j * x)
        inferred = float(np.angle(z) / 2)
        references = np.array([.17, .47, .5, .53, .83])
        direct = np.array([hadamard_probability(2 * (x - a), w) for a in references])
        fringe = .5 + .5 * np.real(np.exp(-2j * references) * z)
        assert np.max(abs(direct - fringe)) < 2e-14
        assert abs(mean - .5) < 2e-14 and abs(inferred - mean) < 2e-14
        assert abs(z) < 1 and variance > 0
        alleged_shift = .5 * math.acos(1 - 2 * variance)
        shifted_model = np.cos(mean - references + alleged_shift) ** 2
        # Independently evaluate the paper's observable encoding, Eq. (32).
        encoded_mean = hadamard_probability(2 * np.arccos(np.sqrt(x)), w)
        assert abs(encoded_mean - mean) < 2e-14
        ancilla_variance = encoded_mean * (1 - encoded_mean)
        assert abs(ancilla_variance - .25) < 2e-14
        rows.append({"sigma_parameter": sigma, "actual_coordinate_variance": variance,
                     "arithmetic_mean": mean, "circular_phase_mean": inferred,
                     "phase_bias": inferred - mean, "fringe_contrast": float(abs(z)),
                     "characteristic_moment": [float(z.real), float(z.imag)],
                     "reference_phases": references.tolist(),
                     "direct_Hadamard_probabilities": direct.tolist(),
                     "characteristic_fringe_max_defect": float(np.max(abs(direct - fringe))),
                     "contrast_as_phase_shift": alleged_shift,
                     "constant_shift_model_max_defect": float(np.max(abs(shifted_model - direct))),
                     "Eq32_encoded_mean_probability": encoded_mean,
                     "ancilla_variance_per_shot": ancilla_variance,
                     "position_variance_per_shot": variance,
                     "ancilla_to_position_variance_ratio": ancilla_variance / variance,
                     "affine_observable_Hessian": 0.})
    return {"points": 4096, "encoding": "amplitudes sqrt(weights)",
            "exact_fringe": "P(a)=1/2+1/2*Re(exp(-2ia)*E exp(2iTheta))",
            "scope": "Positive variance need not cause phase bias. This does not remove nonlinear cloud-to-trajectory bias. Ancilla sampling and direct coordinate sampling have distinct variance constants.",
            "gaussian_rows": rows, "all_assertions_passed": True}


def nonidentifiability():
    # An explicit trigonometric null vector avoids an SVD-dependent sign choice.
    mu, a, b, eta = .5, .125, .0625, .1
    k = math.sin(2 * a) / math.sin(2 * b)
    support = mu + np.array([-a, -b, b, a])
    null = np.array([1 / k, -1., 1., -1 / k])
    first, second = np.full(4, .25) + eta * null, np.full(4, .25) - eta * null
    assert min(first.min(), second.min()) > 0
    assert abs(first.sum() - 1) < 1e-14 and abs(second.sum() - 1) < 1e-14
    z1, z2 = first @ np.exp(2j * support), second @ np.exp(2j * support)
    mean1, mean2 = float(first @ support), float(second @ support)
    assert abs(z1 - z2) < 1e-14 and abs(mean1 - mean2) > 1e-4
    phases = np.linspace(0, 1, 1001)
    p1 = .5 + .5 * np.real(np.exp(-2j * phases) * z1)
    p2 = .5 + .5 * np.real(np.exp(-2j * phases) * z2)
    assert np.max(abs(p1 - p2)) < 1e-14
    return {"support": support.tolist(), "k": k, "eta": eta,
            "null_vector": null.tolist(), "first_weights": first.tolist(),
            "second_weights": second.tolist(),
            "characteristic_moment_defect": float(abs(z1 - z2)),
            "sampled_complete_fringe_defect": float(np.max(abs(p1 - p2))),
            "first_arithmetic_mean": mean1, "second_arithmetic_mean": mean2,
            "mean_difference": abs(mean1 - mean2),
            "scope": "A single-frequency reference-phase scan cannot recover the arithmetic mean of an arbitrary bounded distribution. Direct Eq32 observable encoding remains available.",
            "all_assertions_passed": True}


def lv_calibration():
    beta, gamma = math.exp(-1 / 3), math.exp(.5)
    L = math.sqrt(2) * max(beta, gamma)
    H = math.sqrt(2) * max(beta, gamma)
    ratio = math.sqrt(2) * H / (2 * L)
    assert abs(ratio - 1 / math.sqrt(2)) < 1e-14
    assert abs(ratio - gamma / beta) > 1
    return {"domain": "[0,1]^2", "beta": beta, "gamma": gamma, "L": L, "H": H,
            "R_over_sigma_from_Eqs22_25": ratio,
            "Eq45_formula_gamma_over_beta": gamma / beta, "Eq45_printed_decimal": 2.29,
            "R_at_sigma_point01_from_definitions": .01 * ratio,
            "R_at_sigma_point01_from_printed_decimal": .0229,
            "scope": "Both row gradients and row Hessians have identical norms pointwise, so H=L. The correction changes calibration, not the qualitative success of this benchmark.",
            "all_assertions_passed": True}


def regularity():
    coefficient = 2 * math.sqrt(2 / math.pi)
    rows = []
    for sigma in (.08, .04, .02, .01):
        A = .5 / sigma
        conditional_exact = sigma**3 * coefficient * (1 - (1 + A*A / 2) * math.exp(-A*A / 2)) / math.erf(A / math.sqrt(2))
        zmax = min(A, 12.)
        z = np.linspace(-zmax, zmax, 40001)
        density = np.exp(-z*z / 2)
        numerical = float(np.trapezoid(abs(sigma * z)**3 * density, z) / np.trapezoid(density, z))
        assert abs(numerical - conditional_exact) < 2e-12 * sigma**3
        rows.append({"sigma": sigma, "exact_conditioned_mean_f": conditional_exact,
                     "independent_quadrature_mean_f": numerical,
                     "mean_over_sigma_cubed": conditional_exact / sigma**3,
                     "mean_over_sigma_fourth": conditional_exact / sigma**4})
    assert abs(rows[-1]["mean_over_sigma_cubed"] - coefficient) < 1e-14
    assert rows[-1]["mean_over_sigma_fourth"] > 7.9 * rows[0]["mean_over_sigma_fourth"]
    return {"observable": "f(x)=|x-.5|^3 on [0,1]", "regularity": "C2, bounded in [0,1/8]",
            "value_and_Hessian_at_mean": [0., 0.],
            "untruncated_Gaussian_expectation": "2*sqrt(2/pi)*sigma^3",
            "untruncated_coefficient": coefficient,
            "claim_under_test": "Eq35: O(||Sigma||^2)=O(sigma^4) remainder under only C2 regularity",
            "scope": "Conditioning a centered Gaussian to [0,1] changes the leading cubic expectation only by exponentially small tails.",
            "rows": rows, "all_assertions_passed": True}


def covariance_and_width():
    J = np.array([[0., 1.], [-1., 0.]])
    covariance = np.diag([4., 1.])
    correct, printed = J @ covariance + covariance @ J.T, J @ covariance + covariance @ J
    assert np.allclose(correct, correct.T) and not np.allclose(printed, printed.T)
    A = np.ones((2, 2)); Z = np.zeros((2, 2))
    dense = np.block([[Z, A], [A, Z]])
    v = np.ones(4) / 2
    initial = np.outer(v, v) + .01 * np.eye(4)
    actual_squared = float(np.linalg.norm(dense @ initial, 'fro') ** 2)
    missing_cross_terms = float(np.sum((dense[:, :, None] * initial[None, :, :]) ** 2))
    rowmax = float(np.max(np.linalg.norm(dense, axis=1)))
    main_L = math.sqrt(4) * rowmax
    t = .1
    eigenvalues, eigenvectors = np.linalg.eigh(dense)
    evolution = (eigenvectors * np.exp(t * eigenvalues)) @ eigenvectors.T
    final_norm = float(np.linalg.norm(evolution @ initial @ evolution.T, 'fro'))
    appendix_bound = float(np.linalg.norm(initial, 'fro') * math.exp(2 * rowmax * t))
    main_bound = float(np.linalg.norm(initial, 'fro') * math.exp(2 * main_L * t))
    assert actual_squared > 1.99 * missing_cross_terms
    assert final_norm > appendix_bound and final_norm < main_bound
    sigma, d = .04, 2
    written_width = math.sqrt(math.sqrt(d) * sigma)
    defined_width = math.sqrt((math.sqrt(d) * sigma*sigma) / math.sqrt(d))
    assert abs(defined_width - sigma) < 1e-14 and abs(written_width - sigma) > .1
    epsilon = .01
    scale = epsilon**2
    scaled_initial = scale * initial
    scaled_final = float(np.linalg.norm(evolution @ scaled_initial @ evolution.T, 'fro'))
    assert scaled_final > scale * appendix_bound
    return {"rotation": {"J": J.tolist(), "Sigma": covariance.tolist(),
                          "correct_derivative": correct.tolist(), "printed_derivative": printed.tolist()},
            "dense_linear_Hamiltonian": {"J": dense.tolist(), "Sigma0": initial.tolist(),
                                         "actual_J_Sigma_F_squared": actual_squared,
                                         "sum_with_missing_cross_terms": missing_cross_terms,
                                         "appendix_rowmax_L": rowmax, "main_Eq22_L": main_L,
                                         "time": t, "actual_covariance_norm": final_norm,
                                         "appendix_bound": appendix_bound, "main_L_bound": main_bound},
            "rescaled_local_example": {"epsilon": epsilon, "covariance_scale": scale,
                                        "actual_covariance_norm": scaled_final,
                                        "appendix_bound": scale * appendix_bound,
                                        "main_L_bound": scale * main_bound,
                                        "covariance_realization": "epsilon*(v*U0+sqrt(.01)*(U1,U2,U3,U4)), where independent Ui have mean0, variance1 and support[-sqrt(3),sqrt(3)]; add center(.5,.5,.5,.5). This compact distribution has covariance epsilon^2*(v*v^T+.01I).",
                                        "scope": "The linear matrix example can be localized and used on a short interval before any boundary crossing. It does not establish a compact nonlinear-flow theorem."},
            "Eq41_width": {"dimension": d, "isotropic_standard_deviation": sigma,
                            "sqrt_norm_Sigma_sqrt_F_as_written": written_width,
                            "defined_sigma_F": defined_width},
            "scope": "Appendix transpose and dimension-constant errors are repairable. This linear matrix example does not refute the main bound using the larger Eq22 constant; no compact nonlinear simulation is asserted.",
            "all_assertions_passed": True}


def complete_flow_uniform_remainder():
    """Selected coupled-width tests of the proved complete-flow remainder.

    The RK4 outputs are numerical approximations, checked with two internal
    resolutions. They do not certify an exact continuum solution or a maximum
    over the whole perturbation ball; the analytic proposition supplies that
    uniform statement.
    """
    def field(points):
        return np.sin(2 * math.pi * points[:, [1, 0]])

    def evolve(initial, total_time, steps):
        values = initial.copy()
        internal_dt = total_time / steps
        for _ in range(steps):
            k1 = field(values)
            k2 = field(values + .5 * internal_dt * k1)
            k3 = field(values + .5 * internal_dt * k2)
            k4 = field(values + internal_dt * k3)
            values += internal_dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        return values

    center = np.array([.31, .47])
    angles = 2 * math.pi * np.arange(128) / 128
    directions = np.column_stack((np.cos(angles), np.sin(angles)))
    M, J, H_vector = math.sqrt(2), 2 * math.pi, (2 * math.pi)**2
    K = H_vector * M + J**2
    gradient_norms = abs(2 * math.pi * np.cos(2 * math.pi * center[[1, 0]]))
    rows = []
    for h in (.01, .02, .04):
        normalized_bound = .5 * K * h*h * math.exp(J*h)
        for kappa in (.5, 1., 2.):
            sigma = kappa * h
            initial = np.vstack((center, center + sigma * directions))
            coarse = evolve(initial, h, 1024)
            fine = evolve(initial, h, 2048)
            endpoint_difference = float(np.max(np.linalg.norm(fine - coarse, axis=1)))
            assert endpoint_difference < 2e-11
            first_order = h * (field(initial)[1:] - field(initial)[0])
            increments = (fine[1:] - initial[1:]) - (fine[0] - initial[0])
            coarse_increments = (coarse[1:] - initial[1:]) - (coarse[0] - initial[0])
            remainder = increments - first_order
            coarse_remainder = coarse_increments - first_order
            measured = float(np.max(np.linalg.norm(remainder, axis=1)) / sigma)
            refinement_defect = float(np.max(np.linalg.norm(remainder - coarse_remainder, axis=1)) / sigma)
            measured_components = np.max(abs(increments), axis=0) / sigma
            component_bounds = h * gradient_norms + .5 * h * sigma * H_vector + normalized_bound
            assert measured > 1e-8
            assert measured < normalized_bound
            assert refinement_defect < 1e-8
            assert np.all(measured_components < component_bounds)
            center_euler_defect = float(np.linalg.norm(fine[0] - center - h * field(center[None, :])[0]))
            # This full flow has a substantial temporal correction; it is not
            # the one-generator shear whose increment equality is exact.
            assert center_euler_defect > h*h
            rows.append({"h": h, "kappa": kappa, "sigma": sigma,
                         "sampled_max_R_norm_over_sigma": measured,
                         "uniform_K_h2_expJh_over_2_bound": normalized_bound,
                         "measured_over_uniform_bound": measured / normalized_bound,
                         "R_over_sigma_h_squared": measured / h**2,
                         "max_endpoint_difference_1024_vs_2048": endpoint_difference,
                         "normalized_R_refinement_defect": refinement_defect,
                         "complete_flow_center_Euler_defect": center_euler_defect,
                         "sampled_component_increment_over_sigma": measured_components.tolist(),
                         "component_Taylor_plus_temporal_bounds": component_bounds.tolist()})
    return {"field": "F(q,p)=(sin(2*pi*p),sin(2*pi*q))",
            "Hamiltonian": "H=-cos(2*pi*p)/(2*pi)+cos(2*pi*q)/(2*pi)",
            "center": center.tolist(), "boundary_directions": 128,
            "integration": "Vectorized classical RK4, 1024 and 2048 internal steps per complete-flow trajectory",
            "global_constants": {"M": M, "J": J, "H_vector_bilinear_bound": H_vector, "K": K},
            "exact_identity": "R_h(x,delta)=int_0^h int_0^s [G(Phi_r(x+delta))-G(Phi_r(x))] dr ds, G=DF F",
            "analytic_bound": "||R_h(x,delta)||/sigma <= (H_vector*M+J^2)*h^2*exp(J*h)/2 for ||delta||<=sigma",
            "coupled_width_scope": "For sigma=kappa*h, curvature and complete-flow temporal terms are both O(h^2) after normalization and both must be retained.",
            "rows": rows,
            "scope": "Numerical precision comparison of selected complete-flow perturbations; not exact continuum execution, global reconstruction stability, or a Trotter-error theorem.",
            "all_assertions_passed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'results/verification.json')
    parser.add_argument('--log', type=Path)
    args = parser.parse_args()
    started = datetime.now(timezone.utc).isoformat()
    timer = time.perf_counter()
    checks = {"geometric_criterion": geometry(), "phase_and_sampling": phase_and_sampling(),
              "single_frequency_nonidentifiability": nonidentifiability(),
              "LV_calibration": lv_calibration(), "C2_remainder": regularity(),
              "covariance_and_width": covariance_and_width(),
              "complete_flow_uniform_remainder": complete_flow_uniform_remainder()}
    result = {"source_version": "arXiv:2609.28999v2", "source_pdf_sha256": SOURCE_SHA256,
              "python_version": platform.python_version(), "numpy_version": np.__version__,
              "scope": "Selected corrections, exact finite-grid algebra and analytic examples; no exhaustive audit, quantum hardware result, or speedup claim.",
              "checks": checks, "all_assertions_passed": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output = json.dumps(result, indent=2, allow_nan=False) + '\n'
    args.output.write_text(output, encoding='utf-8', newline='\n')
    logpath = args.log or args.output.parent / 'execution.log'
    codehash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    resulthash = hashlib.sha256(output.encode('utf-8')).hexdigest()
    log = '\n'.join([
        'AUTHOR-ENVIRONMENT EXECUTION RECORD',
        'Deterministic classical checks, not independent human peer review or third-party certification.',
        'Command: python -X utf8 experiments/verify.py',
        'Started UTC: ' + started,
        'Python: ' + sys.version.replace('\n', ' '),
        'Platform: ' + sys.platform,
        'NumPy: ' + np.__version__,
        'Script SHA-256: ' + codehash,
        *['PASS: ' + name for name in checks],
        'All assertions passed: true',
        'Exit status: 0',
        'Verification JSON SHA-256: ' + resulthash,
        'Elapsed seconds: %.6f' % (time.perf_counter() - timer),
        'Complete results follow:', output.rstrip(), ''
    ])
    logpath.parent.mkdir(parents=True, exist_ok=True)
    logpath.write_text(log, encoding='utf-8', newline='\n')
    print(json.dumps({'all_assertions_passed': True, 'groups': list(checks),
                      'results': str(args.output), 'execution_log': str(logpath)}))


if __name__ == '__main__':
    main()
