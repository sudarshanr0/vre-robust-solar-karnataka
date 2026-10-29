"""Toy 2 -- Where does steel stop working?

QUESTION. Toy 1 showed capacity alone cannot reach high reliability once the
resource field is spatially coherent. Add storage. Now: at what point does one
more multiple of the fleet stop buying reliability, and what buys it instead?

WHY IT MATTERS. "Diminishing returns to over-building" is asserted everywhere
in the literature and located nowhere. Nobody reports the penetration at which
marginal capacity credit collapses for a real system, or says what physical
feature of the climate fixes it. It is the single most important missing number
for the "limits of overcapacity" half of the thesis, and it is the number a
minister actually asks for.

WHAT TO LOOK FOR. Two elasticities, side by side:

    steel    elasticity  =  d log(unserved) / d log(over-build)
    duration elasticity  =  d log(unserved) / d log(storage hours)

Where the steel elasticity goes flat while the duration elasticity stays steep,
the binding constraint has switched from the *depth* of the deficit to its
*duration* -- and duration is something capacity cannot address at any price.

WHAT IS NEW RELATIVE TO TOY 1. Persistence (tau) was invisible there and is
dominant here. That contrast is the result, not an artefact: storage is the
only thing that makes the time-ordering of hours matter.

HONEST LIMITS. Reported unserved-energy fractions below about 1e-6 are at the
resolution floor of a 12-year hourly record -- about one unserved hour in the
whole run. They are printed as "<1e-6" rather than as zero, because zero would
be a claim the record cannot support. That floor is itself the subject of
toy 3.
"""

from __future__ import annotations

import numpy as np

from _common import banner, figure_path

from src.overbuild import energy_balance_capacity, simulate
from src.toy_climate import ClimateParams, generate

N_YEARS = 12
OVERBUILDS = np.array([1.25, 1.5, 2.0, 3.0, 4.0, 6.0, 9.0])
STORAGE_HOURS = np.array([0.0, 6.0, 24.0, 72.0, 240.0])
TAUS_H = [48.0, 168.0]
LAM_KM = 800.0  # the regime where toy 1 found capacity alone diverging

FLOOR = 1e-6


def fmt(x: float) -> str:
    if x < FLOOR:
        return "  <1e-6"
    return f"{x:7.1e}"


def unserved_grid(params: ClimateParams, seed: int) -> tuple[np.ndarray, dict]:
    rec = generate(n_years=N_YEARS, params=params, seed=seed)
    cf = rec.portfolio_cf(wind_weight=0.5)
    demand = rec.demand
    k0 = energy_balance_capacity(cf, demand)
    mean_d = demand.mean()

    grid = np.empty((STORAGE_HOURS.size, OVERBUILDS.size))
    for i, hours in enumerate(STORAGE_HOURS):
        for j, r in enumerate(OVERBUILDS):
            out = simulate(cf, demand, r * k0,
                           storage_energy_mwh=hours * mean_d,
                           storage_power_mw=0.5 * r * k0)
            grid[i, j] = out["unserved_energy_fraction"]

    # Deficit-spell durations with no storage, at a modest over-build: this is
    # the physical quantity storage has to outlast.
    out = simulate(cf, demand, 2.0 * k0)
    spells = _spell_lengths(out["unserved"] > 1e-9)
    stats = {
        "n_spells": spells.size,
        "median": float(np.median(spells)) if spells.size else np.nan,
        "p90": float(np.percentile(spells, 90)) if spells.size else np.nan,
        "p99": float(np.percentile(spells, 99)) if spells.size else np.nan,
        "max": int(spells.max()) if spells.size else 0,
    }
    return grid, stats


def _spell_lengths(flag: np.ndarray) -> np.ndarray:
    """Lengths of consecutive True runs."""
    if not flag.any():
        return np.array([], dtype=int)
    d = np.diff(flag.astype(np.int8))
    starts = np.flatnonzero(d == 1) + 1
    ends = np.flatnonzero(d == -1) + 1
    if flag[0]:
        starts = np.r_[0, starts]
    if flag[-1]:
        ends = np.r_[ends, flag.size]
    return ends - starts


def elasticity(values: np.ndarray, knobs: np.ndarray) -> np.ndarray:
    """Local d log(values) / d log(knobs), by centred differences."""
    ok = values > FLOOR
    out = np.full(values.size, np.nan)
    idx = np.flatnonzero(ok)
    if idx.size < 2:
        return out
    ly = np.log(values[idx])
    lx = np.log(knobs[idx])
    out[idx] = np.gradient(ly, lx)
    return out


def main() -> None:
    banner(
        "TOY 2 -- Where steel stops working",
        "At what point does more capacity stop buying reliability,\n"
        "and what sets the ceiling?",
    )

    results = {}
    for tau in TAUS_H:
        params = ClimateParams(lam_wind_km=LAM_KM, lam_solar_km=2 * LAM_KM,
                               tau_wind_h=tau)
        grid, stats = unserved_grid(params, seed=5)
        results[tau] = (grid, stats)

        print(f"PERSISTENCE tau = {tau:.0f} h")
        print("-" * 78)
        print("  unserved energy fraction")
        print("  storage |" + "".join(f"{r:>8.2f}x" for r in OVERBUILDS))
        for i, hours in enumerate(STORAGE_HOURS):
            print(f"  {hours:>6.0f}h |" + "".join(fmt(v) + " " for v in grid[i]))
        print()
        print(f"  deficit spells at 2x over-build, no storage: "
              f"n={stats['n_spells']}, median={stats['median']:.0f}h, "
              f"p90={stats['p90']:.0f}h, p99={stats['p99']:.0f}h, max={stats['max']}h")
        print()

        print("  elasticities (more negative = still buying reliability)")
        print("           |  steel: dlogUE/dlog(over-build) at fixed storage")
        for i, hours in enumerate(STORAGE_HOURS):
            e = elasticity(grid[i], OVERBUILDS)
            cells = "".join(f"{v:>8.2f}" if np.isfinite(v) else f"{'--':>8}" for v in e)
            print(f"  {hours:>6.0f}h |{cells}")
        print("           |  duration: dlogUE/dlog(storage) at fixed over-build")
        dur = np.full_like(grid, np.nan)
        pos = STORAGE_HOURS > 0
        for j in range(OVERBUILDS.size):
            dur[pos, j] = elasticity(grid[pos, j], STORAGE_HOURS[pos])
        for i, hours in enumerate(STORAGE_HOURS):
            if not pos[i]:
                continue
            cells = "".join(f"{v:>8.2f}" if np.isfinite(v) else f"{'--':>8}" for v in dur[i])
            print(f"  {hours:>6.0f}h |{cells}")
        print()

    _exchange_rate(results)
    _plot(results)

    print()
    print("READING THE RESULT")
    print("-" * 78)
    print("""\
1. THE TOY REPRODUCES TOY 1'S EXPONENT, WHICH IS A USEFUL CHECK.
   With no storage the steel elasticity sits near -1.2, and toy 1 fitted
   b = 0.87 at this same lam. Those are the same statement: elasticity = -1/b.
   The two toys agree, so the power law is not an artefact of either.

2. STEEL ALONE HAS A POOR AND SLOWLY WORSENING RATE.
   Along the no-storage row the elasticity drifts from about -1.5 to -1.2, so
   each doubling of the fleet removes a smaller share of the remaining deficit
   than the last -- but gently. Pure over-building does not hit a cliff here;
   it just stays expensive. Doubling the fleet from 3x to 6x buys about a
   2.5x reduction in unserved energy. That is the honest baseline against which
   everything else should be priced.

3. THE FIRST DAY OF STORAGE IS WORTH MORE THAN ANY DOUBLING OF THE FLEET.
   At 3x over-build, 24 hours of storage cuts unserved energy by more than two
   orders of magnitude, against 2.5x for doubling the fleet. The reason is
   visible in the spell statistics: deficit spells at 2x over-build have a
   median of 5-7 hours and a 99th percentile of 17 hours, because most of them
   are simply nights. A buffer that spans a night converts the dominant failure
   mode out of existence. This is also a warning about the toy: a large part of
   what looks like a "resource drought" at low over-build is the diurnal cycle,
   and real analyses that do not net out the diurnal term will overstate how
   much of the problem is weather.

4. STORAGE AND OVER-BUILD ARE COMPLEMENTS, NOT SUBSTITUTES.
   This is the result that surprised me, and it cuts against the "implicit
   storage" framing. Adding storage makes capacity *more* productive, not less:
   the steel elasticity steepens from -1.2 with no storage to -7 or worse with
   24 hours. With nowhere to put the surplus, over-building only helps in the
   hours when the deficit is shallow; with a buffer, every surplus hour is
   banked against a later deficit. So the Perez lineage's claim that over-build
   substitutes for storage is a statement about *cost*, not about physics, and
   it is conditional on the operating point. van Eldik and van Sark's finding
   that the battery-only firm-kWh premium rises with record length while the
   hydrogen-turbine scenario stays flat is the same effect seen from the cost
   side.

5. PERSISTENCE SETS THE CEILING, AND ONLY STORAGE CAN SEE IT.
   tau was invisible in toy 1 and is dominant here, but specifically at the
   long-duration end: at 72 hours of storage and 2x over-build, tripling tau
   moves unserved energy from below the record's floor to 1.4e-3. Short-duration
   storage cannot tell the two climates apart; long-duration storage is where
   the persistence structure of the monsoon shows up in the bill. Sizing
   long-duration storage on a typical event is therefore sizing it to the wrong
   number -- the conclusion Ruhnau and Qvist (2022) reach for Germany, where the
   storage-defining period stretches to 9-12 weeks once consecutive scarce
   spells chain.

6. WHAT THIS MEANS FOR THE THESIS.
   At lam = 800 km, toy 1 found capacity alone could not reach 99.8% at any
   over-build. Here, 24 hours of storage reaches it comfortably. So the
   divergence toy 1 found is duration-driven, and "the limits of overcapacity"
   is precisely a statement about which measures address duration. That makes
   the saturation point a function of tau and lam -- both measurable from a
   reanalysis before any optimisation is run. The next step is to measure them
   for the Indian joint wind-solar field and see where the knee actually falls.""")


def _exchange_rate(results: dict) -> None:
    """Compare what a doubling of the fleet buys against what storage buys.

    Both are expressed as the factor by which unserved energy falls, which is
    the only currency the two are commensurable in.
    """
    print("EXCHANGE RATE -- what a doubling of the fleet buys, versus storage")
    print("-" * 78)
    print("  Both expressed as the factor by which unserved energy falls.")
    print()
    j3 = int(np.flatnonzero(np.isclose(OVERBUILDS, 3.0))[0])
    j6 = int(np.flatnonzero(np.isclose(OVERBUILDS, 6.0))[0])
    for tau, (grid, _) in results.items():
        print(f"  tau = {tau:.0f} h, starting from 3x over-build and no storage")
        base = grid[0, j3]
        doubled = grid[0, j6]
        print(f"    double the fleet (3x -> 6x), no storage    : "
              f"{base / doubled:>7.1f}x less unserved energy")
        for i, hours in enumerate(STORAGE_HOURS):
            if hours == 0:
                continue
            val = grid[i, j3]
            if val <= FLOOR:
                print(f"    add {hours:>4.0f}h storage, fleet unchanged       : "
                      f"  >{base / FLOOR:>6.0f}x  (past the record's floor)")
            else:
                print(f"    add {hours:>4.0f}h storage, fleet unchanged       : "
                      f"{base / val:>7.1f}x less unserved energy")
        print()


def _plot(results: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), sharey=True)
    for ax, (tau, (grid, _)) in zip(axes, results.items()):
        for i, hours in enumerate(STORAGE_HOURS):
            y = np.maximum(grid[i], FLOOR / 2)
            ax.loglog(OVERBUILDS, y, "o-", lw=2, label=f"{hours:.0f} h storage")
        ax.axhline(FLOOR, color="k", ls=":", lw=1)
        ax.text(OVERBUILDS[0], FLOOR * 1.3, "record resolution floor",
                fontsize=8, color="k")
        ax.set_xlabel(r"over-build ratio  $K/K_0$")
        ax.set_title(f"persistence $\\tau$ = {tau:.0f} h")
        ax.grid(alpha=0.3, which="both")
    axes[0].set_ylabel("unserved energy fraction")
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle("Flat curves mean steel has stopped working", y=1.00)
    fig.tight_layout()
    path = figure_path("toy02_where_steel_stops.png")
    fig.savefig(path, dpi=140)
    print(f"[figure] {path}")


if __name__ == "__main__":
    main()
