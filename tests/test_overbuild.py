"""Tests for the toy machinery.

These check properties that must hold for the toys' conclusions to mean
anything -- monotonicity of reliability in capacity, the energy-balance
normalisation, the effective-sample-size estimators against cases with known
answers, and the generator's sign structure. Run with ``pytest tests`` or
``python tests/test_overbuild.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.overbuild import (autocorrelation, cvar, effective_sample_size,
                           energy_balance_capacity, gumbel_return_level,
                           required_overbuild, simulate)
from src.toy_climate import ClimateParams, annual_stress_index, generate


def _small_record(**kw):
    return generate(n_years=3, params=ClimateParams(**kw), seed=0)


# --------------------------------------------------------------------------
# Dispatch and sizing
# --------------------------------------------------------------------------


def test_energy_balance_capacity_balances_energy():
    rec = _small_record()
    cf = rec.portfolio_cf()
    k0 = energy_balance_capacity(cf, rec.demand)
    assert np.isclose((k0 * cf).sum(), rec.demand.sum(), rtol=1e-9)


def test_reliability_is_monotone_in_capacity():
    rec = _small_record()
    cf = rec.portfolio_cf()
    k0 = energy_balance_capacity(cf, rec.demand)
    rel = [simulate(cf, rec.demand, r * k0)["reliability"]
           for r in [1.0, 1.5, 2.0, 4.0, 8.0]]
    assert all(b >= a - 1e-12 for a, b in zip(rel, rel[1:])), rel


def test_storage_never_hurts():
    rec = _small_record()
    cf = rec.portfolio_cf()
    k0 = energy_balance_capacity(cf, rec.demand)
    without = simulate(cf, rec.demand, 2.0 * k0)["reliability"]
    with_storage = simulate(cf, rec.demand, 2.0 * k0,
                            storage_energy_mwh=12 * rec.demand.mean())["reliability"]
    assert with_storage >= without - 1e-12


def test_energy_is_conserved():
    """Generation must equal served energy plus curtailment plus losses."""
    rec = _small_record()
    cf = rec.portfolio_cf()
    k0 = energy_balance_capacity(cf, rec.demand)
    cap = 2.0 * k0
    out = simulate(cf, rec.demand, cap)
    served = rec.demand.sum() - out["unserved"].sum()
    assert np.isclose((cap * cf).sum(), served + out["curtailed"].sum(), rtol=1e-9)


def test_required_overbuild_achieves_its_target():
    rec = _small_record()
    cf = rec.portfolio_cf()
    target = 0.98
    r = required_overbuild(cf, rec.demand, target)
    assert np.isfinite(r)
    k0 = energy_balance_capacity(cf, rec.demand)
    assert simulate(cf, rec.demand, r * k0)["reliability"] >= target


def test_required_overbuild_reports_infeasibility():
    """A target beyond the search range returns inf rather than a wrong answer."""
    rec = _small_record(lam_wind_km=5000.0, lam_solar_km=5000.0)
    cf = rec.portfolio_cf()
    assert required_overbuild(cf, rec.demand, 0.99999, hi=3.0) == np.inf


# --------------------------------------------------------------------------
# Risk and sampling statistics
# --------------------------------------------------------------------------


def test_cvar_picks_out_the_tail():
    x = np.arange(100.0)
    # The worst 10% of 0..99 is 90..99, mean 94.5.
    assert np.isclose(cvar(x, 0.90), 94.5)
    assert cvar(x, 0.90) > np.mean(x)


def test_autocorrelation_starts_at_one():
    rng = np.random.default_rng(0)
    ac = autocorrelation(rng.standard_normal(500), 5)
    assert np.isclose(ac[0], 1.0)
    assert np.all(np.abs(ac[1:]) < 0.3)


def test_effective_sample_size_of_white_noise_is_near_n():
    rng = np.random.default_rng(1)
    x = rng.standard_normal(2000)
    for method in ("ar1", "sum"):
        n_eff = effective_sample_size(x, method)
        assert 0.75 * x.size < n_eff < 1.3 * x.size, (method, n_eff)


def test_effective_sample_size_falls_for_persistent_series():
    """A known AR(1): N_eff should approach the analytic N(1-rho)/(1+rho)."""
    rho = 0.8
    rng = np.random.default_rng(2)
    n = 4000
    x = np.empty(n)
    x[0] = rng.standard_normal()
    for t in range(1, n):
        x[t] = rho * x[t - 1] + np.sqrt(1 - rho ** 2) * rng.standard_normal()
    expected = n * (1 - rho) / (1 + rho)
    assert 0.6 * expected < effective_sample_size(x, "ar1") < 1.6 * expected
    assert effective_sample_size(x, "sum") < 0.5 * n


def test_return_level_ci_widens_with_smaller_effective_n():
    rng = np.random.default_rng(3)
    maxima = rng.gumbel(loc=10.0, scale=2.0, size=44)
    naive = gumbel_return_level(maxima, 50, seed=0)
    corrected = gumbel_return_level(maxima, 50, n_effective=11.0, seed=0)
    assert np.isclose(naive["return_level"], corrected["return_level"])
    assert corrected["ci_width"] > 1.4 * naive["ci_width"]


# --------------------------------------------------------------------------
# The generator's structure
# --------------------------------------------------------------------------


def test_capacity_factors_are_in_range():
    rec = _small_record()
    for field in (rec.wind_cf, rec.solar_cf):
        assert field.min() >= 0.0 and field.max() <= 1.0
    assert rec.demand.min() > 0.0


def test_solar_is_zero_at_night():
    rec = _small_record()
    night = np.isin(rec.hour_of_day, [0, 1, 2, 3, 23])
    assert rec.solar_cf[night].max() == 0.0


def test_break_has_the_monsoon_sign_structure():
    """Wind down, solar up, demand up -- the thing that is not a Dunkelflaute."""
    rec = generate(n_years=6, seed=4)
    brk = rec.break_flag
    assert brk.any() and not brk.all()
    day = np.isin(rec.hour_of_day, np.arange(9, 16))
    wind = rec.wind_cf.mean(axis=1)
    solar = rec.solar_cf.mean(axis=1)
    assert wind[brk].mean() < wind[~brk].mean()
    assert solar[brk & day].mean() > solar[~brk & day].mean()
    assert rec.demand[brk].mean() > rec.demand[~brk].mean()


def test_breaks_only_occur_inside_the_monsoon():
    rec = generate(n_years=6, seed=5)
    p = rec.params
    assert rec.doy[rec.break_flag].min() >= p.monsoon_start_doy
    assert rec.doy[rec.break_flag].max() < p.monsoon_end_doy


def test_spatial_correlation_responds_to_lambda():
    near = generate(n_years=2, params=ClimateParams(lam_wind_km=50.0), seed=6)
    far = generate(n_years=2, params=ClimateParams(lam_wind_km=5000.0), seed=6)

    def end_to_end(rec):
        a, b = rec.wind_cf[:, 0], rec.wind_cf[:, -1]
        return float(np.corrcoef(a, b)[0, 1])

    assert end_to_end(near) < 0.3 < end_to_end(far)


def test_decadal_mode_induces_annual_autocorrelation():
    with_mode = generate(n_years=44, params=ClimateParams(phase_period_years=22.0),
                         seed=7)
    without = generate(
        n_years=44,
        params=ClimateParams(phase_wind_shift=0.0, phase_break_rate_shift=0.0),
        seed=7)
    ac_with = autocorrelation(annual_stress_index(with_mode), 1)[1]
    ac_without = autocorrelation(annual_stress_index(without), 1)[1]
    assert ac_with > 0.25
    assert ac_with > ac_without + 0.2


def test_favourable_phase_is_actually_favourable():
    """Positive phase must raise wind and suppress breaks together."""
    rec = generate(n_years=60, seed=8)
    years = np.unique(rec.year)
    phase = np.array([rec.phase[rec.year == y].mean() for y in years])
    lo, hi = np.quantile(phase, [1 / 3, 2 / 3])
    good = np.isin(rec.year, years[phase >= hi])
    bad = np.isin(rec.year, years[phase <= lo])
    assert rec.wind_cf[good].mean() > rec.wind_cf[bad].mean()
    assert rec.break_flag[good].mean() < rec.break_flag[bad].mean()


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as exc:
                failures += 1
                print(f"FAIL  {name}: {exc}")
    print()
    print(f"{failures} failure(s)")
    sys.exit(1 if failures else 0)
