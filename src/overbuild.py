"""Sizing an over-build, and the statistics needed to know what it bought.

Everything here is deliberately small enough to read in one sitting. The
overcapacity question does not need a capacity-expansion model to get started;
it needs an unambiguous definition of "over-build ratio", an unambiguous
reliability metric, and an honest account of how much the record can support.
Those are the three things this module provides.

A note on the central definition, because the literature is loose about it. The
**over-build ratio** here is installed capacity divided by the capacity that
would exactly balance energy over the record:

    r = K / K0,   where  K0 * mean(cf) = mean(demand)

So ``r = 1`` is a fleet that generates exactly as much energy as is consumed,
and would still fail constantly because the energy arrives at the wrong times.
``r = 2`` means twice that, with the surplus curtailed. This is the same
normalisation the Perez lineage uses for its 3.8--5.7x oversizing factors,
which makes the numbers here comparable to theirs.
"""

from __future__ import annotations

import numpy as np

# --------------------------------------------------------------------------
# Dispatch and reliability
# --------------------------------------------------------------------------


def energy_balance_capacity(cf: np.ndarray, demand: np.ndarray) -> float:
    """The installed capacity ``K0`` at which generation equals demand in total."""
    return float(demand.sum() / max(cf.sum(), 1e-12))


def simulate(cf: np.ndarray, demand: np.ndarray, capacity: float,
             storage_energy_mwh: float = 0.0,
             storage_power_mw: float | None = None,
             round_trip_efficiency: float = 0.85) -> dict:
    """Dispatch a fleet of ``capacity`` MW against ``demand``, with storage.

    Greedy dispatch: serve demand from generation, charge storage with the
    surplus, discharge it against any deficit. Anything still unserved is
    unserved energy; anything still surplus is curtailed. No transmission, no
    unit commitment, no foresight -- all of which are the right omissions for a
    toy whose question is about the climate rather than the market.

    Returns a dict with ``unserved`` and ``curtailed`` hourly arrays plus the
    scalar summaries the toys actually report.
    """
    gen = capacity * cf
    net = gen - demand

    if storage_energy_mwh <= 0:
        unserved = np.maximum(-net, 0.0)
        curtailed = np.maximum(net, 0.0)
    else:
        p_max = storage_power_mw if storage_power_mw is not None else storage_energy_mwh / 4.0
        eta = np.sqrt(round_trip_efficiency)  # split evenly over charge/discharge
        soc = storage_energy_mwh * 0.5
        unserved = np.empty_like(demand)
        curtailed = np.empty_like(demand)
        for t in range(net.size):
            x = net[t]
            if x >= 0:
                room = (storage_energy_mwh - soc) / eta
                charge = min(x, p_max, room)
                soc += charge * eta
                unserved[t] = 0.0
                curtailed[t] = x - charge
            else:
                need = -x
                avail = soc * eta
                discharge = min(need, p_max, avail)
                soc -= discharge / eta
                unserved[t] = need - discharge
                curtailed[t] = 0.0

    total = demand.sum()
    return {
        "unserved": unserved,
        "curtailed": curtailed,
        "unserved_energy_fraction": float(unserved.sum() / total),
        "reliability": float(1.0 - unserved.sum() / total),
        "loss_of_load_hours_fraction": float((unserved > 1e-9).mean()),
        "curtailed_fraction": float(curtailed.sum() / max(gen.sum(), 1e-12)),
    }


def reliability_at(cf: np.ndarray, demand: np.ndarray, overbuild: float,
                   **kwargs) -> float:
    """Reliability (1 - unserved energy fraction) at a given over-build ratio."""
    k0 = energy_balance_capacity(cf, demand)
    return simulate(cf, demand, overbuild * k0, **kwargs)["reliability"]


def required_overbuild(cf: np.ndarray, demand: np.ndarray, target: float,
                       lo: float = 1.0, hi: float = 60.0,
                       tol: float = 1e-3, max_iter: int = 40,
                       **kwargs) -> float:
    """Smallest over-build ratio reaching ``target`` reliability, by bisection.

    Returns ``np.inf`` when ``hi`` cannot reach the target -- which is not a
    numerical failure but the substantive answer to Puzzle I's divergence
    question, and the toys treat it as a result rather than an error.
    """
    if reliability_at(cf, demand, hi, **kwargs) < target:
        return np.inf
    if reliability_at(cf, demand, lo, **kwargs) >= target:
        return lo
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        if reliability_at(cf, demand, mid, **kwargs) >= target:
            hi = mid
        else:
            lo = mid
        if hi - lo < tol:
            break
    return float(hi)


# --------------------------------------------------------------------------
# Risk measures
# --------------------------------------------------------------------------


def cvar(losses: np.ndarray, alpha: float = 0.95) -> float:
    """Conditional value at risk: mean of the worst ``1 - alpha`` of losses.

    Takes losses (larger is worse), so to use it on a benefit, pass the
    negative. With a small sample this is a noisy estimator, and toy 3's
    effective-sample-size result is the reason to care about that.
    """
    losses = np.asarray(losses, dtype=float)
    if losses.size == 0:
        return float("nan")
    q = np.quantile(losses, alpha)
    tail = losses[losses >= q]
    return float(tail.mean()) if tail.size else float(q)


# --------------------------------------------------------------------------
# How much the record can support
# --------------------------------------------------------------------------


def autocorrelation(x: np.ndarray, max_lag: int | None = None) -> np.ndarray:
    """Biased sample autocorrelation at lags 0..max_lag."""
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    n = x.size
    if max_lag is None:
        max_lag = n - 1
    max_lag = min(max_lag, n - 1)
    denom = np.dot(x, x)
    if denom <= 0:
        return np.r_[1.0, np.zeros(max_lag)]
    return np.array([np.dot(x[: n - k], x[k:]) / denom for k in range(max_lag + 1)])


def effective_sample_size(x: np.ndarray, method: str = "sum") -> float:
    """Effective number of independent samples in an autocorrelated series.

    Two classical estimators, both of which the climate literature has used for
    decades on means and neither of which anyone has applied to the joint
    wind--solar resource tail:

    ``"ar1"``
        ``N * (1 - rho) / (1 + rho)`` with ``rho`` the lag-1 autocorrelation.
        The Trenberth (1984) form. Cheap, and right if the series really is
        AR(1).
    ``"sum"``
        ``N / (1 + 2 * sum_k rho_k)``, truncated at the first non-positive
        ``rho_k`` (Bretherton et al. 1999). Makes no AR(1) assumption, which
        matters when a decadal mode puts power at lags the AR(1) form cannot
        see.

    Returns a float that may exceed ``N`` for an anti-persistent series; callers
    that need a sample size should clip it themselves.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    if n < 3:
        return float(n)
    rho = autocorrelation(x, max_lag=min(n // 2, n - 1))
    if method == "ar1":
        r = float(np.clip(rho[1], -0.99, 0.99))
        return float(n * (1.0 - r) / (1.0 + r))
    if method == "sum":
        total = 0.0
        for k in range(1, rho.size):
            if rho[k] <= 0:
                break
            total += rho[k]
        return float(n / (1.0 + 2.0 * total))
    raise ValueError(f"unknown method: {method!r}")


def gumbel_return_level(maxima: np.ndarray, return_period: float,
                        n_effective: float | None = None,
                        n_boot: int = 2000, seed: int = 0) -> dict:
    """Return level and bootstrap CI for block maxima, via a Gumbel fit.

    A Gumbel (GEV with shape fixed at zero) is the deliberately conservative
    choice for a toy: with a few dozen blocks the shape parameter is barely
    identified, and pretending otherwise is exactly the overconfidence toy 3 is
    about.

    ``n_effective`` is the point of the function. Pass it and the bootstrap
    resamples ``n_effective`` values instead of ``N``, which widens the interval
    by roughly ``sqrt(N / n_effective)``. That widening is the correction a
    persistent record demands and the literature's intervals omit.
    """
    maxima = np.asarray(maxima, dtype=float)
    n = maxima.size
    rng = np.random.default_rng(seed)

    def fit(sample: np.ndarray) -> float:
        # Method of moments for the Gumbel: beta = s * sqrt(6)/pi, mu = m - g*beta
        s = sample.std(ddof=1)
        beta = s * np.sqrt(6.0) / np.pi
        mu = sample.mean() - 0.5772156649 * beta
        return float(mu - beta * np.log(-np.log(1.0 - 1.0 / return_period)))

    point = fit(maxima)
    m = int(round(n_effective)) if n_effective is not None else n
    m = max(m, 3)
    draws = np.array([fit(rng.choice(maxima, size=m, replace=True))
                      for _ in range(n_boot)])
    return {
        "return_level": point,
        "ci_low": float(np.quantile(draws, 0.025)),
        "ci_high": float(np.quantile(draws, 0.975)),
        "ci_width": float(np.quantile(draws, 0.975) - np.quantile(draws, 0.025)),
        "n_used": m,
    }
