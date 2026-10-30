"""Synthetic monsoon-flavoured resource and demand generator.

The toy problems in ``scripts/`` need a resource field whose *climate-dynamical*
knobs are explicit and controllable, because the whole point of the overcapacity
question is how the sizing answer depends on them. Reanalysis gives you one
realisation of one correlation structure; this module gives you a dial for each.

Three knobs matter, and they are named after the quantities in Puzzle I:

``lam``
    Spatial decorrelation length of the resource field. Short ``lam`` means
    sites fail independently and geographic spread buys a lot; long ``lam``
    means the whole fleet fails together and spread buys nothing.
``tau``
    Persistence (e-folding) timescale of unfavourable conditions, in hours.
    This is what storage has to bridge.
``chi``
    Strength of the coupling between low supply and high demand -- the
    compound-event term. Set it to zero and supply and demand are independent;
    raise it and the bad hours line up.

The seasonal structure is deliberately South Asian rather than midlatitude:
wind peaks during the monsoon (the Somali jet), solar dips during the monsoon
(cloud), and a semi-Markov *break* process interrupts the monsoon with spells
in which wind collapses, solar recovers toward clear-sky, and demand rises with
the heat. That sign structure -- solar *up* while wind is *down* -- is the thing
that distinguishes a monsoon break from a Dunkelflaute, and toy 5 exists to
measure what it is worth.

Nothing here is calibrated to Karnataka. It is calibrated to be *qualitatively*
right and fully controllable, so that a result which depends on a knob can be
seen to depend on it. Replacing ``generate()`` with ERA5-derived capacity
factors is the intended next step, and every toy script reads its data through
that one function for exactly that reason.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import signal

HOURS_PER_DAY = 24
DAYS_PER_YEAR = 365
HOURS_PER_YEAR = HOURS_PER_DAY * DAYS_PER_YEAR


@dataclass
class ClimateParams:
    """Knobs for the synthetic climate.

    Defaults are a plausible southern-Indian setting: eight sites spread over
    ~700 km, wind decorrelating over a few hundred km, unfavourable spells
    persisting a couple of days, and a moderate supply--demand compound.
    """

    n_sites: int = 8
    site_spacing_km: float = 100.0

    # --- Puzzle I's three quantities -------------------------------------
    lam_wind_km: float = 300.0   # spatial decorrelation length, wind
    lam_solar_km: float = 600.0  # solar decorrelates more slowly (synoptic cloud)
    tau_wind_h: float = 48.0     # persistence of wind anomalies
    tau_solar_h: float = 18.0    # persistence of cloud anomalies
    chi: float = 0.45            # supply--demand coupling strength, in [0, 1)

    # --- marginal resource levels ----------------------------------------
    wind_cf_mean: float = 0.30
    wind_cf_spread: float = 0.18
    solar_cf_peak: float = 0.72   # clear-sky peak-hour capacity factor
    monsoon_cloud_loss: float = 0.42  # fractional solar loss in active monsoon

    # --- monsoon and break structure -------------------------------------
    monsoon_start_doy: int = 152  # ~1 June
    monsoon_end_doy: int = 273    # ~30 September
    monsoon_wind_boost: float = 0.55  # fractional wind gain in the monsoon
    break_rate_per_season: float = 2.6   # expected number of break onsets
    break_mean_duration_d: float = 7.0
    break_wind_drop: float = 0.55     # fractional wind loss during a break
    break_solar_recovery: float = 0.80  # fraction of cloud loss recovered
    break_demand_boost: float = 0.14   # fractional demand gain during a break

    # --- demand -----------------------------------------------------------
    demand_base_mw: float = 10_000.0
    demand_evening_peak: float = 0.26   # fractional evening bump
    demand_heat_sensitivity: float = 0.22

    # --- decadal mode ------------------------------------------------------
    # Sign convention: a POSITIVE phase is favourable. It raises the wind
    # resource and suppresses break onsets together, so the mode has a coherent
    # effect on system stress rather than two terms that cancel. Flip the signs
    # of both shifts to study a mode whose terms oppose each other -- which is
    # itself a live question for the IOD, where the rainfall and circulation
    # responses need not favour the grid in the same direction.
    phase_wind_shift: float = 0.10       # fractional wind gain at phase = +1
    phase_break_rate_shift: float = -0.6  # change in break onsets at phase = +1
    phase_period_years: float = 22.0      # full cycle length of the slow mode

    def site_positions(self) -> np.ndarray:
        return np.arange(self.n_sites) * self.site_spacing_km


@dataclass
class ClimateRecord:
    """Hourly output of :func:`generate`.

    ``wind_cf`` and ``solar_cf`` are ``(n_hours, n_sites)`` capacity factors in
    [0, 1]. ``demand`` is in MW. ``break_flag`` and ``phase`` are the latent
    states, exposed because several toys condition on them -- which is cheating
    relative to reality, and is the point: a toy that needs the true state tells
    you how much skill a real diagnostic would have to reach.
    """

    wind_cf: np.ndarray
    solar_cf: np.ndarray
    demand: np.ndarray
    break_flag: np.ndarray
    phase: np.ndarray
    year: np.ndarray
    hour_of_day: np.ndarray
    doy: np.ndarray
    params: ClimateParams = field(default_factory=ClimateParams)

    @property
    def n_hours(self) -> int:
        return self.demand.size

    def portfolio_cf(self, wind_weight: float = 0.5,
                     site_weights: np.ndarray | None = None) -> np.ndarray:
        """Capacity factor of a wind/solar portfolio, equally spread by default.

        ``wind_weight`` is wind's share of installed capacity. The result is the
        capacity factor of one aggregate "fleet MW", so multiplying it by an
        installed capacity gives generation directly.
        """
        if site_weights is None:
            site_weights = np.full(self.params.n_sites, 1.0 / self.params.n_sites)
        site_weights = np.asarray(site_weights, dtype=float)
        site_weights = site_weights / site_weights.sum()
        wind = self.wind_cf @ site_weights
        solar = self.solar_cf @ site_weights
        return wind_weight * wind + (1.0 - wind_weight) * solar


def _ar1_field(n_hours: int, corr: np.ndarray, tau_h: float,
               rng: np.random.Generator) -> np.ndarray:
    """An AR(1)-in-time, spatially correlated standard Gaussian field.

    Returns ``(n_hours, n_sites)`` with unit marginal variance, lag-1
    autocorrelation ``exp(-1/tau_h)`` and spatial correlation ``corr``.
    """
    n_sites = corr.shape[0]
    a = np.exp(-1.0 / max(tau_h, 1e-6))
    chol = np.linalg.cholesky(corr + 1e-10 * np.eye(n_sites))
    innov = rng.standard_normal((n_hours, n_sites)) @ chol.T
    scale = np.sqrt(1.0 - a * a)
    # The recursion out[t] = a*out[t-1] + scale*innov[t] is a one-pole IIR
    # filter; lfilter runs it in C, which matters because the toys regenerate
    # these fields dozens of times. zi is chosen so out[0] == innov[0], giving
    # unit marginal variance from the first sample rather than after burn-in.
    zi = innov[0] * (1.0 - scale)
    out, _ = signal.lfilter([scale], [1.0, -a], innov, axis=0,
                            zi=zi[None, :])
    return out


def _spatial_corr(positions: np.ndarray, lam_km: float) -> np.ndarray:
    d = np.abs(positions[:, None] - positions[None, :])
    return np.exp(-d / max(lam_km, 1e-6))


def _break_series(n_years: int, p: ClimateParams,
                  phase_year: np.ndarray,
                  rng: np.random.Generator) -> np.ndarray:
    """Daily 0/1 break flag, semi-Markov within each monsoon season.

    Onsets are Poisson with a rate that depends on the decadal phase; durations
    are geometric with mean ``break_mean_duration_d``. Breaks only occur inside
    the monsoon window, which is what makes them a monsoon object rather than a
    generic low-wind spell.
    """
    flag = np.zeros(n_years * DAYS_PER_YEAR, dtype=bool)
    for y in range(n_years):
        rate = p.break_rate_per_season + p.phase_break_rate_shift * phase_year[y]
        rate = max(rate, 0.1)
        n_onsets = rng.poisson(rate)
        season = np.arange(p.monsoon_start_doy, p.monsoon_end_doy)
        if n_onsets == 0 or season.size == 0:
            continue
        onsets = rng.choice(season, size=n_onsets, replace=True)
        for onset in onsets:
            dur = 1 + rng.geometric(1.0 / p.break_mean_duration_d)
            lo = y * DAYS_PER_YEAR + onset
            hi = min(lo + int(dur), (y + 1) * DAYS_PER_YEAR)
            flag[lo:hi] = True
    return flag


def generate(n_years: int = 44, params: ClimateParams | None = None,
             seed: int = 0) -> ClimateRecord:
    """Generate an hourly synthetic record.

    The default 44 years is not an accident: it is the length of the ERA5-era
    record the Indian energy-drought papers use, and toy 3 exists to ask how
    many independent monsoons that actually contains.
    """
    p = params or ClimateParams()
    rng = np.random.default_rng(seed)

    n_hours = n_years * HOURS_PER_YEAR
    hour = np.arange(n_hours)
    hour_of_day = hour % HOURS_PER_DAY
    day = hour // HOURS_PER_DAY
    doy = day % DAYS_PER_YEAR
    year = day // DAYS_PER_YEAR

    # Decadal mode: a smooth slow oscillation in [-1, 1], plus a little noise so
    # phases are not perfectly periodic. This stands in for IOD/PDO/AMO phase.
    phase_year = np.sin(2 * np.pi * np.arange(n_years) / p.phase_period_years)
    phase_year = phase_year + 0.25 * rng.standard_normal(n_years)
    phase_year = np.clip(phase_year, -1.5, 1.5)

    break_daily = _break_series(n_years, p, phase_year, rng)
    break_flag = np.repeat(break_daily, HOURS_PER_DAY)
    phase = np.repeat(phase_year, HOURS_PER_YEAR)

    positions = p.site_positions()
    z_wind = _ar1_field(n_hours, _spatial_corr(positions, p.lam_wind_km),
                        p.tau_wind_h, rng)
    z_solar = _ar1_field(n_hours, _spatial_corr(positions, p.lam_solar_km),
                         p.tau_solar_h, rng)

    in_monsoon = (doy >= p.monsoon_start_doy) & (doy < p.monsoon_end_doy)

    # --- wind -------------------------------------------------------------
    wind_mean = np.full(n_hours, p.wind_cf_mean)
    wind_mean = wind_mean * (1.0 + p.monsoon_wind_boost * in_monsoon)
    wind_mean = wind_mean * (1.0 - p.break_wind_drop * break_flag)
    wind_mean = wind_mean * (1.0 + p.phase_wind_shift * phase)
    wind_cf = np.clip(wind_mean[:, None] + p.wind_cf_spread * z_wind, 0.0, 1.0)

    # --- solar ------------------------------------------------------------
    # Clear-sky diurnal shape: a half-sine over a 12-hour day.
    solar_clear = np.clip(np.sin(np.pi * (hour_of_day - 6) / 12.0), 0.0, None)
    cloud_loss = p.monsoon_cloud_loss * in_monsoon
    cloud_loss = cloud_loss * (1.0 - p.break_solar_recovery * break_flag)
    solar_mean = p.solar_cf_peak * solar_clear * (1.0 - cloud_loss)
    # Cloud noise is multiplicative and only bites when the sun is up.
    cloud_noise = np.clip(1.0 + 0.30 * z_solar, 0.0, 1.35)
    solar_cf = np.clip(solar_mean[:, None] * cloud_noise, 0.0, 1.0)

    # --- demand -----------------------------------------------------------
    # Evening peak that outlives the solar day -- the sub-daily detail that
    # decides whether the break's solar recovery actually hedges anything.
    evening = np.exp(-0.5 * ((hour_of_day - 19.5) / 2.4) ** 2)
    shape = 1.0 + p.demand_evening_peak * evening
    seasonal = 1.0 + p.demand_heat_sensitivity * np.cos(
        2 * np.pi * (doy - 120) / DAYS_PER_YEAR)
    demand = p.demand_base_mw * shape * seasonal
    demand = demand * (1.0 + p.break_demand_boost * break_flag)

    # The compound term: tie demand to the *negative* of the wind anomaly, so
    # that chi > 0 makes low-supply hours also high-demand hours. chi = 0
    # recovers an independent demand series.
    if p.chi > 0:
        z_mean = z_wind.mean(axis=1)
        z_mean = (z_mean - z_mean.mean()) / (z_mean.std() + 1e-12)
        demand = demand * (1.0 - p.chi * 0.12 * z_mean)

    demand = demand * (1.0 + 0.04 * rng.standard_normal(n_hours))
    demand = np.maximum(demand, 1e-6)

    return ClimateRecord(
        wind_cf=wind_cf, solar_cf=solar_cf, demand=demand,
        break_flag=break_flag, phase=phase, year=year,
        hour_of_day=hour_of_day, doy=doy, params=p,
    )


def annual_stress_index(rec: ClimateRecord, wind_weight: float = 0.5) -> np.ndarray:
    """One number per year: how hard that year is for the fleet.

    Defined as the mean ratio of demand to available supply-per-installed-MW,
    so a large value means a year in which the resource was poor *relative to*
    the demand it had to serve. This is the quantity toy 3 asks for the
    effective sample size of, and toy 4 ranks years by.
    """
    cf = rec.portfolio_cf(wind_weight=wind_weight)
    years = np.unique(rec.year)
    out = np.empty(years.size)
    for i, y in enumerate(years):
        m = rec.year == y
        out[i] = rec.demand[m].sum() / max(cf[m].sum(), 1e-9)
    return out
