"""Toy 6 -- The exchange rate between information and steel.

QUESTION. A planner can buy insurance in two currencies: megawatts of
over-build, or forecast skill that lets a limited flexible resource be aimed at
the right hours. How many megawatts does one unit of skill replace -- and does
the exchange rate move as the system approaches the point where steel stops
working?

WHY IT MATTERS. Overcapacity is insurance bought in steel; a skilful two-to-
three-week forecast of break onset is insurance bought in information. It lets
an operator pre-position hydro, defer maintenance and contract demand response,
converting an unscheduled tail event into a scheduled one. The subseasonal-
forecast-value literature has never connected this to capacity planning, and
the capacity-planning literature assumes either perfect or zero foresight. The
closest precedent is Schmidt (2025), who shows the installed mix shifts by up
to a quarter (+25% solar, -20% onshore wind) purely as a function of the
foresight assumption, holding the resource fixed. That trades foresight against
*technology choice*; this trades it against *installed megawatts*, which is the
unit a regulator can act on.

The elegant conjecture is that the exchange rate diverges near the saturation
point: where steel stops working, information becomes the only remaining asset.
This toy tests it directly by running the same experiment in a benign regime
and in one near divergence.

MODEL. A flexible resource with a fixed annual energy budget and a power limit
-- think hydro plus demand response. It can be deployed in any hours, but only
so many of them. A forecast of skill rho ranks the hours; the budget is spent
on the top-ranked ones. rho = 1 is perfect foresight, rho = 0 is climatology.

HONEST LIMITS. Skill is imposed as a correlation with the true deficit, not
earned from a forecast model, so this prices skill rather than demonstrating
it. And the budget is deployed with a single global ranking, which is more
foresight over the *year* than any real operator has. Both make the numbers an
upper bound -- which is the right bound to compute first.
"""

from __future__ import annotations

import numpy as np

from _common import banner, figure_path

from src.overbuild import energy_balance_capacity, simulate
from src.toy_climate import ClimateParams, generate

N_YEARS = 16
N_FORECAST_DRAWS = 3
TARGET = 0.998
STORAGE_HOURS = 12.0
SKILLS = [0.0, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0]

# Flexible budget: 1% of annual energy, deployable at up to 15% of mean demand.
FLEX_ENERGY_SHARE = 0.01
FLEX_POWER_SHARE = 0.15

REGIMES = {
    "benign      (lam = 300 km)": dict(lam_wind_km=300.0, lam_solar_km=600.0),
    "near divergence (lam = 1500 km)": dict(lam_wind_km=1500.0, lam_solar_km=3000.0),
}


def forecast_signal(truth: np.ndarray, skill: float,
                    rng: np.random.Generator) -> np.ndarray:
    """A signal correlated with ``truth`` at approximately ``skill``.

    Standardise the truth, mix in independent noise in the proportion that
    gives the requested correlation. This is the cleanest way to impose a known
    skill without committing to any particular forecast system.
    """
    z = (truth - truth.mean()) / (truth.std() + 1e-12)
    if skill >= 1.0:
        return z
    noise = rng.standard_normal(truth.size)
    return skill * z + np.sqrt(max(1.0 - skill ** 2, 0.0)) * noise


def reliability_with_flex(cf, demand, capacity, skill, rng,
                          storage_hours=STORAGE_HOURS) -> float:
    """Reliability of a fleet plus a forecast-aimed flexible resource."""
    mean_d = demand.mean()
    storage = storage_hours * mean_d

    # The operator forecasts the *residual* deficit it will face, which depends
    # on the fleet it has built -- so the ranking is recomputed per capacity.
    base = simulate(cf, demand, capacity, storage_energy_mwh=storage)
    residual = base["unserved"]
    if residual.sum() <= 0:
        return base["reliability"]

    signal = forecast_signal(residual, skill, rng)
    flex_power = FLEX_POWER_SHARE * mean_d
    n_hours_affordable = int(FLEX_ENERGY_SHARE * demand.sum() / flex_power)
    n_hours_affordable = max(min(n_hours_affordable, demand.size), 1)

    chosen = np.argpartition(-signal, n_hours_affordable - 1)[:n_hours_affordable]
    boost = np.zeros_like(demand)
    boost[chosen] = flex_power

    # Deploying flexibility is equivalent to shaving demand in those hours.
    out = simulate(cf, np.maximum(demand - boost, 0.0), capacity,
                   storage_energy_mwh=storage)
    # Charge the unserved energy against the ORIGINAL demand, so that shaving
    # demand cannot flatter the metric by shrinking its denominator.
    return float(1.0 - out["unserved"].sum() / demand.sum())


def required_overbuild_with_flex(cf, demand, skill, rng,
                                 lo=1.0, hi=40.0, iters=22) -> float:
    k0 = energy_balance_capacity(cf, demand)
    if reliability_with_flex(cf, demand, hi * k0, skill, rng) < TARGET:
        return np.inf
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if reliability_with_flex(cf, demand, mid * k0, skill, rng) >= TARGET:
            hi = mid
        else:
            lo = mid
    return float(hi)


def main() -> None:
    banner(
        "TOY 6 -- The exchange rate between information and steel",
        f"How much over-build does forecast skill replace, at a {TARGET:.1%} target,\n"
        "and does the rate steepen near the saturation point?",
    )

    print(f"Flexible resource: {FLEX_ENERGY_SHARE:.0%} of annual energy, "
          f"deployable at {FLEX_POWER_SHARE:.0%} of mean demand.")
    print(f"Storage: {STORAGE_HOURS:.0f} h.   Reliability target: {TARGET:.1%}.")
    print()

    all_rows = {}
    for label, overrides in REGIMES.items():
        params = ClimateParams(**overrides)
        rec = generate(n_years=N_YEARS, params=params, seed=31)
        cf = rec.portfolio_cf(wind_weight=0.5)
        demand = rec.demand

        rows = []
        for skill in SKILLS:
            # Average over several forecast realisations: with one draw the
            # curve is visibly noisy, and a non-monotonic exchange rate would
            # be an artefact of that noise rather than a finding.
            draws = [required_overbuild_with_flex(
                cf, demand, skill, np.random.default_rng(900 + k))
                for k in range(N_FORECAST_DRAWS)]
            finite = [d for d in draws if np.isfinite(d)]
            rows.append((skill, float(np.mean(finite)) if finite else np.inf))
        all_rows[label] = rows

        r0 = rows[0][1]
        print(f"{label}")
        print("-" * 78)
        print("   skill |  over-build needed | saved vs zero skill | per 0.1 skill")
        for i, (skill, r) in enumerate(rows):
            if not np.isfinite(r):
                print(f"   {skill:>5.2f} |        unreachable  |                     |")
                continue
            saved = r0 - r if np.isfinite(r0) else np.nan
            if i == 0:
                rate = ""
            else:
                prev_s, prev_r = rows[i - 1]
                d_skill = skill - prev_s
                rate_val = (prev_r - r) / d_skill * 0.1 if np.isfinite(prev_r) else np.nan
                rate = f"   {rate_val:>+6.3f}x" if np.isfinite(rate_val) else ""
            saved_txt = f"{saved:>+8.3f}x" if np.isfinite(saved) else "       --"
            print(f"   {skill:>5.2f} |         {r:>8.3f}x  |          {saved_txt}  |{rate}")

        finite = [(s, r) for s, r in rows if np.isfinite(r)]
        if len(finite) >= 2 and np.isfinite(r0):
            total = r0 - finite[-1][1]
            print()
            print(f"  Perfect skill replaces {total:.3f}x of the fleet "
                  f"({total / r0 * 100:.1f}% of the zero-skill build).")
            print(f"  Average exchange rate: {total / 1.0 * 0.1:.3f}x of the fleet "
                  f"per 0.1 of skill.")
        print()

    _plot(all_rows)

    print("READING THE RESULT")
    print("-" * 78)
    print("""\
1. INFORMATION IS PRICEABLE IN MEGAWATTS, AND THE UNIT IS USABLE.
   The table converts forecast skill into over-build multiples -- the exchange
   rate the thesis proposes. That is a number a regulator can act on in a way
   that a Brier score is not: it says how much steel a forecasting programme is
   worth, in the same currency as the steel.

2. THE RETURNS TO SKILL ARE SHARPLY CONCAVE -- A LITTLE SKILL BUYS MOST OF IT.
   This is the result that contradicted my expectation. The per-0.1-skill
   column is largest at the very bottom of the skill range and then collapses:
   moving from climatology to a correlation of just 0.2 captures the large
   majority of everything perfect foresight would deliver, and the remaining
   0.8 of correlation adds little.

   The mechanism is worth stating because it is not an artefact. The flexible
   budget is small, so it can only cover a modest number of hours; the deficit
   hours are numerous relative to that budget; and therefore the operator does
   not need to identify *the* worst hours, only to land somewhere in the bad
   part of the distribution. Precision of aim is cheap to achieve and quickly
   stops mattering.

   The policy reading is the opposite of the one a forecasting programme would
   prefer. The case for subseasonal prediction of break onset does not rest on
   pushing skill toward perfection; it rests on getting *any* usable signal, and
   then on enlarging the flexible budget that signal aims. If this survives on
   real data, the binding constraint is flexibility, not forecast quality -- and
   that is a finding about where to spend money.

3. THE CONJECTURE SURVIVES, IN THE FORM THAT MATTERS.
   Compare the two regimes. In the benign regime the flexible resource saves a
   modest fraction of the fleet. Near divergence, where toy 1 showed capacity
   alone running away, the same budget of the same information saves a larger
   fraction -- because each avoided deficit hour is worth more when the steel
   alternative is priced on a steeper curve. So "where steel stops working,
   information becomes the only remaining asset" holds, and its mechanism is
   not mysterious: the exchange rate is the ratio of two marginal costs, and it
   moves when one of them diverges.

4. THE CAVEAT THAT HAS TO TRAVEL WITH THE NUMBER.
   This prices skill; it does not demonstrate it. The skill is imposed as a
   correlation with the true residual deficit, and the deployment uses one
   global ranking over the whole record -- more foresight than any operator
   has. Both inflate the result, so these are upper bounds. The honest version
   needs real MJO/BSISO-conditioned break-onset skill, a rolling decision
   window, and a flexible resource whose energy budget respects reservoir
   dynamics. Schmidt's SDDP machinery, built for hydropower inflow uncertainty,
   is the natural tool and the natural comparison.

5. WHY THIS GOES LAST.
   The exchange rate consumes the other toys' outputs: the saturation point
   from toy 2 sets where the rate steepens, the phase structure from toy 4 sets
   what is predictable at long lead, and the break's sign structure from toy 5
   sets what the flexible resource has to cover. Run it last, but know now what
   it needs, because that determines what the earlier papers must report.""")


def _plot(all_rows: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.0))
    for label, rows in all_rows.items():
        s = np.array([r[0] for r in rows])
        v = np.array([r[1] for r in rows])
        ok = np.isfinite(v)
        ax1.plot(s[ok], v[ok], "o-", lw=2, label=label.split("(")[0].strip())
        if ok.any():
            ax2.plot(s[ok], (v[ok][0] - v[ok]) / v[ok][0] * 100, "o-", lw=2,
                     label=label.split("(")[0].strip())

    ax1.set_xlabel("forecast skill (correlation with the true deficit)")
    ax1.set_ylabel(f"over-build needed for {TARGET:.1%}")
    ax1.set_title("Skill substitutes for steel")
    ax1.grid(alpha=0.3)
    ax1.legend(frameon=False, fontsize=9)

    ax2.set_xlabel("forecast skill")
    ax2.set_ylabel("fleet saved (% of the zero-skill build)")
    ax2.set_title("The rate is steeper where steel is dearer")
    ax2.grid(alpha=0.3)
    ax2.legend(frameon=False, fontsize=9)

    fig.tight_layout()
    path = figure_path("toy06_information_vs_steel.png")
    fig.savefig(path, dpi=140)
    print(f"[figure] {path}\n")


if __name__ == "__main__":
    main()
