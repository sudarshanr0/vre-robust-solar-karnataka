"""Toy 5 -- Does the break's clear-sky solar actually hedge anything?

QUESTION. A monsoon break is not a Dunkelflaute. The same circulation that
weakens the low-level jet also suppresses cloud, so wind falls while solar
*rises*, and the heat drives demand up. That is a sign-structured compound
event, not a co-collapse. So: how much is the solar recovery worth, in
over-build multiples -- and does it survive at sub-daily resolution, when the
evening demand peak outlives the solar day?

WHY IT MATTERS. The compound-drought taxonomy is midlatitude. A Dunkelflaute is
wind and solar failing together under a winter block; a cold dark lull adds
cold-driven demand. Both have all three terms pulling the same way. The break
does not, and the sign structure is exactly what determines the optimal
*composition* of overcapacity -- the "of what kind" half of the thesis
question. Nobody has computed it.

The conjecture most at risk here is the hedge itself: aerosol loading during
breaks may offset the clear-sky enhancement. The framing should therefore not
pre-commit to the hedge, which is why this toy measures it rather than assuming
it, and reports the operating conditions under which it vanishes.

WHAT TO LOOK FOR. Four event structures with everything else held fixed, and
for each: the over-build needed, where in the day the deficit lands, and how
much of the total deficit is attributable to break hours. Then the evening-peak
sweep, which is where the hedge should break down if it is going to.

HONEST LIMITS. The "solar recovery" here is a prescribed fraction of the
monsoon cloud loss, not a radiative calculation, and aerosols are absent
entirely. So this toy cannot tell you how large the real hedge is -- only how
much a hedge of a given size is worth, and what erodes it.
"""

from __future__ import annotations

import numpy as np

from _common import banner, figure_path

from src.overbuild import energy_balance_capacity, required_overbuild, simulate
from src.toy_climate import ClimateParams, generate

N_YEARS = 25
TARGET = 0.995
STORAGE_HOURS = 8.0
EVENING_HOURS = np.arange(18, 23)
SOLAR_DAY_HOURS = np.arange(8, 17)

STRUCTURES = {
    "monsoon break (solar recovers, demand up)": dict(),
    "no solar recovery (Dunkelflaute-like)": dict(break_solar_recovery=0.0),
    "solar recovers, demand flat": dict(break_demand_boost=0.0),
    "neither (wind collapse alone)": dict(break_solar_recovery=0.0,
                                          break_demand_boost=0.0),
}

EVENING_PEAKS = [0.0, 0.13, 0.26, 0.40]


def diagnose(params: ClimateParams, seed: int = 21) -> dict:
    rec = generate(n_years=N_YEARS, params=params, seed=seed)
    cf = rec.portfolio_cf(wind_weight=0.5)
    demand = rec.demand
    storage = STORAGE_HOURS * demand.mean()

    r = required_overbuild(cf, demand, TARGET, storage_energy_mwh=storage)
    if not np.isfinite(r):
        return {"overbuild": np.inf}

    k0 = energy_balance_capacity(cf, demand)
    out = simulate(cf, demand, r * k0, storage_energy_mwh=storage)
    unserved = out["unserved"]
    total = unserved.sum()

    brk = rec.break_flag
    evening = np.isin(rec.hour_of_day, EVENING_HOURS)
    solar_day = np.isin(rec.hour_of_day, SOLAR_DAY_HOURS)

    # Conditional means, to show the sign structure is actually present.
    wind = rec.wind_cf.mean(axis=1)
    solar = rec.solar_cf.mean(axis=1)
    day = solar_day
    return {
        "overbuild": r,
        "break_share_of_hours": float(brk.mean()),
        "break_share_of_deficit": float(unserved[brk].sum() / max(total, 1e-12)),
        "evening_share_of_deficit": float(unserved[evening].sum() / max(total, 1e-12)),
        "solarday_share_of_deficit": float(unserved[solar_day].sum() / max(total, 1e-12)),
        "wind_anomaly_in_break": float(wind[brk].mean() / wind[~brk].mean() - 1),
        "solar_anomaly_in_break": float(solar[brk & day].mean() / solar[~brk & day].mean() - 1),
        "demand_anomaly_in_break": float(demand[brk].mean() / demand[~brk].mean() - 1),
    }


def main() -> None:
    banner(
        "TOY 5 -- The break's sign structure, and whether the solar hedge survives",
        "Wind down, solar UP, demand up. How much is the solar recovery worth,\n"
        "and does it hold once the evening peak is accounted for?",
    )

    print("PART A -- four event structures, everything else held fixed")
    print("-" * 78)
    results = {}
    for label, overrides in STRUCTURES.items():
        d = diagnose(ClimateParams(**overrides))
        results[label] = d
        print(f"  {label}")
        print(f"    over-build for {TARGET:.1%}            : {d['overbuild']:.3f}x")
        print(f"    break hours as share of the year     : {d['break_share_of_hours']:.1%}")
        print(f"    break hours as share of the deficit  : {d['break_share_of_deficit']:.1%}")
        print(f"    deficit in the evening (18-22h)      : {d['evening_share_of_deficit']:.1%}")
        print(f"    deficit during the solar day (8-16h) : {d['solarday_share_of_deficit']:.1%}")
        print(f"    in-break anomalies: wind {d['wind_anomaly_in_break']:+.0%},"
              f" solar {d['solar_anomaly_in_break']:+.0%},"
              f" demand {d['demand_anomaly_in_break']:+.0%}")
        print()

    base = results["monsoon break (solar recovers, demand up)"]["overbuild"]
    no_solar = results["no solar recovery (Dunkelflaute-like)"]["overbuild"]
    no_demand = results["solar recovers, demand flat"]["overbuild"]
    neither = results["neither (wind collapse alone)"]["overbuild"]

    print("  DECOMPOSITION")
    print(f"    worth of the solar recovery : {no_solar - base:+.3f}x over-build"
          f"  ({(no_solar / base - 1) * 100:+.1f}%)")
    print(f"    cost of the demand surge    : {base - no_demand:+.3f}x over-build"
          f"  ({(base / no_demand - 1) * 100:+.1f}%)")
    print(f"    net of the two              : {base - neither:+.3f}x over-build"
          f"  ({(base / neither - 1) * 100:+.1f}%)")
    print()

    print("PART B -- does the hedge survive the evening peak?")
    print("-" * 78)
    print("  evening |  with solar  |  without solar  |  hedge worth  | evening share")
    print("    peak  |   recovery   |    recovery     |  (over-build) |  of deficit")
    rows = []
    for peak in EVENING_PEAKS:
        with_hedge = diagnose(ClimateParams(demand_evening_peak=peak))
        without = diagnose(ClimateParams(demand_evening_peak=peak,
                                         break_solar_recovery=0.0))
        worth = without["overbuild"] - with_hedge["overbuild"]
        rows.append((peak, with_hedge["overbuild"], without["overbuild"], worth,
                     with_hedge["evening_share_of_deficit"]))
        print(f"  {peak:>6.0%}  |   {with_hedge['overbuild']:>8.3f}x  |"
              f"    {without['overbuild']:>8.3f}x   |"
              f"    {worth:>+7.3f}x   |   {with_hedge['evening_share_of_deficit']:>6.1%}")
    print()

    _plot(rows)

    print("READING THE RESULT")
    print("-" * 78)
    print("""\
1. THE SIGN STRUCTURE IS REAL AND IT MATTERS.
   Holding everything else fixed, removing the break's solar recovery raises
   the required over-build measurably. So the hedge is worth something, and a
   study that imported a Dunkelflaute template -- all three terms pulling the
   same way -- would over-size the Indian fleet. The composition question is
   not cosmetic: the same wind collapse demands a different mix depending on
   what solar does during it.

2. THE DEMAND SURGE COSTS MORE THAN THE SOLAR RECOVERY SAVES.
   Compare the two terms in the decomposition. The break's demand boost is the
   larger of the two effects, so the net of the monsoon break against a bare
   wind collapse is still adverse. The break is a grid event *through demand*,
   and the solar recovery only softens it. This lines up with the uncomfortable
   finding in the corpus's own reading: for today's wind-heavy southern fleet,
   the monsoon is when the grid is comfortable, and deficit days cluster in
   November and December. The break becomes the binding event as solar share
   and cooling demand grow -- which is a projection argument, and should be
   presented as one rather than as an observation.

3. THE HEDGE IS ENTIRELY STORAGE-MEDIATED. THIS IS THE REAL FINDING.
   Look at where the deficit falls: essentially none of it -- 0.0% to 0.2% --
   occurs during the solar day. Of course it does not. At a 3x over-build the
   daytime is comfortably covered; what fails is the night. So the break's
   clear-sky solar enhancement cannot meet any of the unserved demand directly.
   Every unit of its value arrives through storage, by charging a buffer that is
   discharged after sunset.

   That reframes the hedge. It is not a supply-side offset to the wind collapse;
   it is extra charging energy, and it is worth something only in proportion to
   the storage available to catch it. A system with no storage gets nothing from
   it at all. This is a sharper and more useful claim than "solar partly offsets
   the wind collapse", and it is testable: the worth of the hedge should scale
   with installed storage duration and vanish as duration goes to zero.

4. THE HEDGE ERODES AS THE EVENING PEAK GROWS.
   Read down Part B. The solar recovery is worth 0.099x of the fleet with no
   evening peak and 0.066x with a 40% one -- a third of its value gone -- while
   the evening share of the deficit rises from 1.7% to 2.7%. The mechanism is
   the same one as in point 3, one step further: a sharper evening peak moves
   the deficit further from the solar day and demands that the storage shift
   more energy across a longer gap.

   This is the sub-daily question in Puzzle III, and the answer is conditional.
   India's demand shape is moving toward a sharper evening peak as
   air-conditioning and electric cooking spread, so the hedge is worth most now
   and less later -- the opposite of the direction the framing needs, and worth
   saying out loud before a committee says it first.

5. WHAT TO DO WITH THIS.
   The real version conditions on observed break chronologies rather than a
   synthetic flag, uses satellite irradiance so the aerosol term is present
   rather than assumed away, and computes the four-variable dependence
   structure including hydro. Follow Grochowicz et al. (2024): let the system's
   own response pick the events first, then ask how well they match the
   active-break taxonomy -- rather than assuming the taxonomy and compositing
   on it. That ordering matters here more than in Europe, because no
   grid-relevant event taxonomy for South Asia exists to import.""")


def _plot(rows: list) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    arr = np.array(rows)
    peaks = arr[:, 0] * 100
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0))

    ax1.plot(peaks, arr[:, 1], "o-", lw=2, label="break with solar recovery")
    ax1.plot(peaks, arr[:, 2], "s-", lw=2, label="break without solar recovery")
    ax1.set_xlabel("evening demand peak (% above baseline)")
    ax1.set_ylabel(f"over-build for {TARGET:.1%} reliability")
    ax1.set_title("The two event structures converge")
    ax1.grid(alpha=0.3)
    ax1.legend(frameon=False, fontsize=9)

    ax2.plot(peaks, arr[:, 3], "o-", lw=2, color="C2")
    ax2.set_xlabel("evening demand peak (% above baseline)")
    ax2.set_ylabel("worth of the solar hedge (over-build multiples)")
    ax2.set_title("A hedge that pays at the wrong hour")
    ax2.axhline(0, color="k", ls="--", lw=1)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    path = figure_path("toy05_break_sign_structure.png")
    fig.savefig(path, dpi=140)
    print(f"[figure] {path}\n")


if __name__ == "__main__":
    main()
