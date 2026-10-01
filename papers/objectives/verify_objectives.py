"""Numerical certificates for the propositions in paper.tex.

Each check computes the same quantity two ways (closed form against Monte
Carlo or enumeration) and asserts agreement at a stated tolerance.
Run: python verify_objectives.py   (writes numerics.json)
"""
import json
import numpy as np
from scipy.stats import norm
from scipy.special import expit

rng = np.random.default_rng(20261001)
out = {}

# Proposition 1: improvement rewards telescope; path-dependent rewards do not.
n_versions, T = 12, 6
U = rng.normal(size=n_versions)
paths = rng.integers(0, n_versions, size=(5000, T + 1))
paths[:, 0] = 0
imp = (U[paths[:, 1:]] - U[paths[:, :-1]]).sum(axis=1)
assert np.allclose(imp, U[paths[:, -1]] - U[paths[:, 0]], atol=1e-12)
# a reward with no potential form: win rate against the predecessor.
# Feasibility graph: from 0 either jump to J (U=5) and then only stay, or
# climb a ladder 1,2,3,4 one unit at a time. Enumerate every feasible path
# of length 4 and compare the endpoint each reward selects.
import itertools
Ug = {"0": 0.0, "J": 5.0, "L1": 1.0, "L2": 2.0, "L3": 3.0, "L4": 4.0}
nxt = {"0": ["J", "L1"], "J": ["J"], "L1": ["L2"], "L2": ["L3"], "L3": ["L4"], "L4": ["L4"]}
def walks(v, k):
    if k == 0:
        yield [v]
        return
    for w in nxt[v]:
        for rest in walks(w, k - 1):
            yield [v] + rest
P = list(walks("0", 4))
score_imp = [sum(Ug[p[i + 1]] - Ug[p[i]] for i in range(4)) for p in P]
score_wr = [sum(expit(Ug[p[i + 1]] - Ug[p[i]]) for i in range(4)) for p in P]
end_imp, end_wr = P[int(np.argmax(score_imp))][-1], P[int(np.argmax(score_wr))][-1]
out["prop1_telescoping_max_abs_error"] = float(np.max(np.abs(imp - (U[paths[:, -1]] - U[0]))))
out["prop1_ladder_example"] = {"improvement_endpoint_U": Ug[end_imp], "win_rate_endpoint_U": Ug[end_wr],
                               "win_rate_jump_path": float(max(score_wr[i] for i, p in enumerate(P) if p[1] == "J")),
                               "win_rate_ladder_path": float(max(score_wr[i] for i, p in enumerate(P) if p[1] == "L1"))}
assert Ug[end_imp] == 5.0 and Ug[end_wr] == 4.0

# Proposition 2: win rate against the predecessor rewards splitting and churn.
D = np.linspace(0.01, 10, 1000)
one = expit(D)
two = 2 * expit(D / 2)
assert np.all(two > one) and np.all(two > 1) and np.all(one < 1)
out["prop2_min_gap_two_steps_minus_one"] = float((two - one).min())
# n steps of D/n: closed form n*sigma(D/n) vs simulated Bradley-Terry wins
Dtot, n = 2.0, 20
wins = (rng.random((200000, n)) < expit(Dtot / n)).sum(axis=1).mean()
out["prop2_n20_closed_form"] = float(n * expit(Dtot / n))
out["prop2_n20_monte_carlo"] = float(wins)
assert abs(wins - n * expit(Dtot / n)) < 0.02
out["prop2_one_step_D2"] = float(expit(Dtot))

# Proposition 3: win rate against a fixed anchor distorts risk attitude.
def anchored(m, s, ref=0.0, draws=2_000_000):
    u = m + s * rng.standard_normal(draws)
    return float(expit(u - ref).mean())
below_tight, below_wide = anchored(-3, 0.1), anchored(-3, 1.0)
above_tight, above_wide = anchored(3, 0.1), anchored(3, 1.0)
assert below_wide > below_tight and above_wide < above_tight
out["prop3_below_anchor"] = {"sd_0.1": below_tight, "sd_1.0": below_wide}
out["prop3_above_anchor"] = {"sd_0.1": above_tight, "sd_1.0": above_wide}

# Proposition 4: selection of the realised maximum rewards variance.
mu1, mu2, s2 = 0.0, 0.5, 1.0
for s1 in (0.5, 1.0, 2.0, 4.0):
    closed = norm.cdf((mu1 - mu2) / np.hypot(s1, s2))
    z = rng.standard_normal((2, 1_000_000))
    mc = float(np.mean(mu1 + s1 * z[0] > mu2 + s2 * z[1]))
    assert abs(mc - closed) < 2e-3
    out[f"prop4_win_prob_trailer_sd_{s1}"] = {"closed": float(closed), "mc": mc}
# K equal-mean candidates, one with higher sd: share of wins
K = 10
sds = np.ones(K); sds[0] = 2.0
draws = rng.standard_normal((400000, K)) * sds
mean_better = draws.copy(); mean_better[:, 1] += 0.5
out["prop4_K10_win_share_high_variance"] = float(np.mean(np.argmax(draws, 1) == 0))
out["prop4_K10_win_share_high_variance_vs_better_mean"] = {
    "high_variance": float(np.mean(np.argmax(mean_better, 1) == 0)),
    "better_mean": float(np.mean(np.argmax(mean_better, 1) == 1))}

# Proposition 5: compounding relative selection picks the largest E log R.
# A: R in {1.6, 0.5} w.p. 1/2 -> E R = 1.05, E log R < 0
# B: R in {1.1, 0.95} w.p. 1/2 -> E R = 1.025, E log R > 0
ra, rb = np.array([1.6, 0.5]), np.array([1.1, 0.95])
glog = {"A": float(np.log(ra).mean()), "B": float(np.log(rb).mean())}
mean_r = {"A": float(ra.mean()), "B": float(rb.mean())}
assert mean_r["A"] > mean_r["B"] and glog["A"] < 0 < glog["B"]
steps, paths_n = 400, 20000
coin = rng.random((paths_n, steps)) < 0.5
logA = np.where(coin, np.log(1.6), np.log(0.5)).sum(1)
logB = np.where(rng.random((paths_n, steps)) < 0.5, np.log(1.1), np.log(0.95)).sum(1)
out["prop5_E_R"] = mean_r
out["prop5_E_log_R"] = glog
out["prop5_share_B_exceeds_half_fraction"] = float(np.mean(logB > logA))
out["prop5_median_log_wealth_A_per_step"] = float(np.median(logA) / steps)
out["prop5_expected_wealth_A_after_400"] = float(mean_r["A"] ** steps)
assert out["prop5_share_B_exceeds_half_fraction"] > 0.999

# Proposition 6: measured improvement = anchored change minus evaluator drift.
Tn = 50
theta = rng.normal(size=Tn + 1)
phi = [lambda x, a=a, b=b: a * x + b for a, b in
       zip(1 + 0.1 * rng.normal(size=Tn + 1), np.cumsum(0.05 + 0.02 * rng.normal(size=Tn + 1)))]
measured = sum(phi[t](theta[t + 1]) - phi[t](theta[t]) for t in range(Tn))
drift = sum(phi[t + 1](theta[t + 1]) - phi[t](theta[t + 1]) for t in range(Tn))
rhs = phi[Tn](theta[Tn]) - phi[0](theta[0]) - drift
assert abs(measured - rhs) < 1e-10
out["prop6_identity_error"] = float(abs(measured - rhs))
# a self-judging system: version never changes, evaluator inflates by 0.05/step
flat = sum((0.0 + 0.05 * (t + 1)) - (0.0 + 0.05 * t) for t in range(Tn))
out["prop6_flat_system_score_gain_under_drift"] = float(flat)

json.dump(out, open(__file__.replace("verify_objectives.py", "numerics.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
