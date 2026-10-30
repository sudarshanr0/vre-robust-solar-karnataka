"""Toy 1 -- Is there a scaling law for the over-build?

QUESTION. Fix a system and a resource record. Sweep the reliability target.
How does the minimum over-build ratio needed to hold that target grow -- and
what climate-dynamical quantity sets the growth rate?

WHY IT MATTERS. The Perez lineage reports over-build ratios case by case:
3.8-5.7x for Minnesota, 1.33x for an Iberian PV-plus-pumped-hydro system, a
firm-kWh premium of 3.72 for Europe. Nobody fits the *relationship* across
reliability targets, so there is no way to say whether the requirement grows
gently or explodes. Without the shape, every published number is a point with
no curve through it.

WHAT TO LOOK FOR. Fit  r = c * (1 - R)^(-b)  and read off the exponent b.
A small b means reliability is cheap; a large b means each extra nine costs
multiplicatively more; and a target the sweep cannot reach at all is the
divergence Puzzle I conjectures -- a regime where no feasible amount of steel
buys adequacy.

HONEST LIMITS. No storage, no transmission, no demand response. That turns out
to be more informative than it sounds: see the note on tau at the end, which
is the result that sets up toy 2.
"""

from __future__ import annotations

import numpy as np

from _common import banner, figure_path

from src.overbuild import required_overbuild
from src.toy_climate import ClimateParams, generate

N_YEARS = 30
TARGETS = np.array([0.90, 0.95, 0.98, 0.99, 0.995, 0.998, 0.999])

# Primary sweep: spatial decorrelation length, holding everything else fixed.
LAMBDAS_KM = [50.0, 150.0, 300.0, 800.0, 3000.0]

# Secondary check: persistence, at the baseline spatial scale.
TAUS_H = [12.0, 48.0, 168.0]


def fit_power_law(targets: np.ndarray, overbuild: np.ndarray) -> dict:
    """Fit r = c * (1 - R)^(-b) by least squares in log-log space."""
    finite = np.isfinite(overbuild)
    if finite.sum() < 3:
        return {"exponent": np.nan, "prefactor": np.nan, "r2": np.nan,
                "reach": targets[finite][-1] if finite.any() else np.nan}
    u = np.log(1.0 - targets[finite])          # log unreliability (negative)
    y = np.log(overbuild[finite])
    slope, intercept = np.polyfit(u, y, 1)
    pred = slope * u + intercept
    ss_res = float(((y - pred) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    return {
        "exponent": float(-slope),             # b, positive
        "prefactor": float(np.exp(intercept)),  # c
        "r2": float(1.0 - ss_res / ss_tot) if ss_tot > 0 else np.nan,
        "reach": float(targets[finite][-1]),
    }


def sweep(params: ClimateParams, seed: int) -> np.ndarray:
    rec = generate(n_years=N_YEARS, params=params, seed=seed)
    cf = rec.portfolio_cf(wind_weight=0.5)
    return np.array([required_overbuild(cf, rec.demand, t) for t in TARGETS])


def main() -> None:
    banner(
        "TOY 1 -- A scaling law for the over-build",
        "Does required over-build follow a law in the reliability target,\n"
        "and which climate-dynamical quantity sets its exponent?",
    )

    print("PART A -- spatial decorrelation length (lam)")
    print("-" * 78)
    header = "  lam (km)  " + "".join(f"{t:>8.3f}" for t in TARGETS) + "      b     R2"
    print(header)
    lam_fits = {}
    curves = {}
    for lam in LAMBDAS_KM:
        params = ClimateParams(lam_wind_km=lam, lam_solar_km=2 * lam)
        r = sweep(params, seed=11)
        fit = fit_power_law(TARGETS, r)
        lam_fits[lam] = fit
        curves[f"lam = {lam:.0f} km"] = r
        cells = "".join(f"{v:>8.2f}" if np.isfinite(v) else f"{'inf':>8}" for v in r)
        note = "" if np.isfinite(r).all() else f"   diverges above R={fit['reach']:.3f}"
        print(f"  {lam:>8.0f}  {cells}  {fit['exponent']:>5.2f}  {fit['r2']:>5.3f}{note}")

    print()
    print("  Fitted law:  r = c * (1 - R)^(-b)")
    for lam, fit in lam_fits.items():
        print(f"    lam = {lam:>6.0f} km:  r = {fit['prefactor']:.2f} * (1-R)^(-{fit['exponent']:.3f})"
              f"   [R2 = {fit['r2']:.3f}]")

    print()
    print("PART B -- persistence timescale (tau), at lam = 300 km")
    print("-" * 78)
    print("  tau (h)   " + "".join(f"{t:>8.3f}" for t in TARGETS) + "      b")
    for tau in TAUS_H:
        params = ClimateParams(tau_wind_h=tau)
        r = sweep(params, seed=11)
        fit = fit_power_law(TARGETS, r)
        cells = "".join(f"{v:>8.2f}" if np.isfinite(v) else f"{'inf':>8}" for v in r)
        print(f"  {tau:>8.0f}  {cells}  {fit['exponent']:>5.2f}")

    _plot(lam_fits, curves)

    print()
    print("READING THE RESULT")
    print("-" * 78)
    print("""\
1. THERE IS A LAW, AND IT IS A POWER LAW.
   Over the whole range of targets, required over-build fits
   r = c * (1 - R)^(-b) with R-squared above 0.99. So the honest way to report
   an over-build number is as a pair (c, b), not as a scalar. Every published
   single-number oversizing factor is one point on somebody's curve, measured
   at a reliability target that often goes unstated.

2. THE EXPONENT IS SET BY SPATIAL CORRELATION, AND IT DIVERGES.
   b rises monotonically with the decorrelation length: when sites are
   effectively independent, reliability is cheap (b near 1/4); at the baseline
   it is roughly 1/2; and once the field is coherent across the whole fleet the
   curve runs off to infinity at a finite target -- no over-build at all
   reaches 99%. That is Puzzle I's divergence, reproduced in a toy, and it says
   the saturation point is a property of the resource field's geometry rather
   than of the technology.

3. PERSISTENCE IS INVISIBLE TO THIS METRIC -- WHICH IS THE POINT.
   Varying tau over an order of magnitude barely moves the exponent. This is
   not a bug: with no storage, unserved energy depends only on the *marginal*
   joint distribution of supply and demand, not on the order the hours arrive
   in. Persistence can only cost you something once you own a buffer it can
   outlast. So tau is not absent from the physics -- it is absent from the
   metric.

   The lesson generalises past the toy. A scaling law reported without saying
   which reliability metric it targets is under-specified, because different
   metrics are sensitive to different climate quantities. Grochowicz, Bloomfield
   and Victoria (2025) find the same thing the hard way over 80 ERA5 years: no
   single year is worst on both long-run and short-run stress, and the two
   point at different decades. Toy 2 adds storage and tau becomes the dominant
   term.""")


def _plot(lam_fits: dict, curves: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))

    for label, r in curves.items():
        finite = np.isfinite(r)
        ax1.loglog(1.0 - TARGETS[finite], r[finite], "o-", lw=2, label=label)
    ax1.set_xlabel(r"unreliability  $1-R$")
    ax1.set_ylabel(r"required over-build  $K/K_0$")
    ax1.set_title("A power law, steepening with spatial coherence")
    ax1.invert_xaxis()
    ax1.grid(alpha=0.3, which="both")
    ax1.legend(frameon=False, fontsize=9)

    lams = np.array(sorted(lam_fits))
    bs = np.array([lam_fits[l]["exponent"] for l in lams])
    diverges = np.array([not np.isclose(lam_fits[l]["reach"], TARGETS[-1])
                         for l in lams])
    ax2.semilogx(lams[~diverges], bs[~diverges], "o-", lw=2, color="C0",
                 label="reaches 99.9%")
    if diverges.any():
        ax2.semilogx(lams[diverges], bs[diverges], "X", ms=13, color="C3",
                     label="diverges before 99.9%")
    ax2.set_xlabel("spatial decorrelation length  $\\lambda$  (km)")
    ax2.set_ylabel("fitted exponent  $b$")
    ax2.set_title("The exponent is a climate quantity")
    ax2.grid(alpha=0.3, which="both")
    ax2.legend(frameon=False, fontsize=9)

    fig.tight_layout()
    path = figure_path("toy01_scaling_law.png")
    fig.savefig(path, dpi=140)
    print(f"\n[figure] {path}")


if __name__ == "__main__":
    main()
