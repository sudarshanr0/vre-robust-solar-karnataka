# Toy Problems for the Overcapacity Question

Six small, self-contained computational exercises, one per script in
`scripts/`. They run on synthetic data in seconds to minutes, need nothing but
numpy/scipy/pandas/matplotlib, and each one ends by printing what it found and
what it does not establish.

## Why toys, and what they are for

The overcapacity question does not need a capacity-expansion model to get
started. It needs to know, before any data is committed:

1. **Is the question well-posed?** Does it have an answer that is a number or a
   curve, rather than a definition dispute?
2. **Is the effect detectable?** If a mechanism cannot be seen in synthetic
   data where its strength is set by hand, it will not be seen in ERA5.
3. **Does the pipeline work?** The sizing loop, the reliability metric, the
   bootstrap — all of it should be debugged against a case with a known answer.
4. **What would falsify it?** A toy that cannot fail is not telling you
   anything.

A toy's job is to return a **sign and an order of magnitude**, and to fail
cheaply. None of the numbers below is a claim about Karnataka.

## The shared generator

All six read their data through `src.toy_climate.generate()`, which produces an
hourly record with three explicit climate-dynamical dials:

| Dial | Meaning | Why it is the dial |
|---|---|---|
| `lam` | spatial decorrelation length of the resource field (km) | sets whether geographic spread buys anything |
| `tau` | persistence timescale of unfavourable conditions (hours) | sets what storage has to bridge |
| `chi` | supply–demand coupling strength | the compound-event term |

The seasonal structure is deliberately South Asian: wind peaks in the monsoon
(the Somali jet), solar dips in the monsoon (cloud), and a semi-Markov *break*
process interrupts it with spells where wind collapses, solar recovers toward
clear-sky, and demand rises with the heat. A slow mode shifts the wind resource
and break frequency together on a multi-decadal cycle.

**Replacing `generate()` with ERA5-derived capacity factors is a one-file
change**, and it is the intended next step. Every script reads its data through
that single function for exactly that reason.

## Running them

```bash
pip install -r requirements.txt
```

```bash
cd scripts && python3 toy01_scaling_law.py
```

```bash
python3 tests/test_overbuild.py
```

Figures land in `reports/figures/`. Approximate runtimes: toys 1, 2 and 3 take
under 20 seconds; toys 4 and 5 take under a minute; toy 6 takes about two
minutes.

---

## The central definition

Everything turns on one normalisation, so it is worth stating precisely. The
**over-build ratio** is installed capacity divided by the capacity that would
exactly balance energy over the record:

```
r = K / K0,    where   K0 · mean(cf) = mean(demand)
```

So `r = 1` generates exactly as much energy as is consumed — and still fails
constantly, because the energy arrives at the wrong times. `r = 2` means twice
that, with the surplus curtailed. This is the same normalisation behind the
Perez lineage's 3.8–5.7× oversizing factors, which keeps the numbers here
comparable to theirs.

---

## Toy 1 — A scaling law for the over-build

`scripts/toy01_scaling_law.py` · Puzzle I · ~6 s

**Question.** Sweep the reliability target. How does the minimum over-build
needed to hold it grow, and what climate quantity sets the growth rate?

**Why it matters.** The literature reports over-build numbers case by case and
never fits the relationship across targets. Without the shape, every published
number is a point with no curve through it.

**Result.**

```
r = c · (1 − R)^(−b)      R² ≥ 0.98 across all cases
```

| λ (km) | b | reaches 99.9%? |
|---|---|---|
| 50 | 0.25 | yes |
| 150 | 0.35 | yes |
| 300 | 0.52 | yes |
| 800 | 0.87 | **no — diverges above 99.5%** |
| 3000 | 1.20 | **no — diverges above 98%** |

The exponent is set by the spatial decorrelation length, and it diverges: once
the field is coherent across the whole fleet, no over-build reaches 99%.
Persistence (τ) barely moves it.

**The non-obvious part.** τ being invisible is not a bug. With no storage,
unserved energy depends only on the *marginal* joint distribution of supply and
demand, not on the order the hours arrive in. Persistence can only cost you
something once you own a buffer it can outlast. So **a scaling law reported
without saying which reliability metric it targets is under-specified**,
because different metrics are sensitive to different climate quantities — the
same lesson Grochowicz, Bloomfield & Victoria (2025) reach over 80 ERA5 years,
where no single year is worst on both long-run and short-run stress.

**Falsifiable by.** Finding that real Indian capacity-factor fields give no
stable exponent, or an exponent uncorrelated with measured λ.

---

## Toy 2 — Where steel stops working

`scripts/toy02_where_steel_stops.py` · Puzzle I (saturation) · ~5 s

**Question.** Add storage. At what point does one more multiple of the fleet
stop buying reliability, and what buys it instead?

**Result.** Two elasticities, side by side:

- **Steel elasticity** `d log(unserved) / d log(over-build)` sits near −1.2 with
  no storage and drifts slowly to −1.5. Consistent with toy 1: elasticity =
  −1/b. Pure over-building does not hit a cliff; it just stays expensive.
  Doubling the fleet from 3× to 6× buys about 2.5× less unserved energy.
- **The first day of storage beats any doubling of the fleet.** At 3×
  over-build, 24 h of storage cuts unserved energy by over two orders of
  magnitude.

**The non-obvious part — storage and over-build are complements, not
substitutes.** Adding storage makes capacity *more* productive: the steel
elasticity steepens from −1.2 with no storage to −7 or worse with 24 h. With
nowhere to put the surplus, over-building only helps in hours when the deficit
is shallow; with a buffer, every surplus hour is banked against a later
deficit. So the Perez lineage's claim that over-build substitutes for storage is
a statement about **cost**, not physics, and it is conditional on the operating
point. van Eldik & van Sark's finding that the battery-only firm-kWh premium
rises with record length while the hydrogen-turbine scenario stays flat is the
same effect from the cost side.

**And τ is now dominant.** At 72 h of storage and 2× over-build, tripling τ
moves unserved energy from below the record's floor to 1.4×10⁻³. Short-duration
storage cannot tell two climates apart; long-duration storage is where the
monsoon's persistence structure shows up in the bill.

**A warning the toy produced about itself.** Deficit spells at 2× over-build
have a median of 5–7 h and a 99th percentile of 17 h — they are mostly *nights*.
A large part of what looks like a "resource drought" at low over-build is the
diurnal cycle, and real analyses that do not net out the diurnal term will
overstate how much of the problem is weather.

---

## Toy 3 — How many independent monsoons are in a 44-year record?

`scripts/toy03_independent_monsoons.py` · Puzzle II / the sampling spine · ~18 s

**Question.** What is the effective sample size of the joint resource record,
and what does the correction do to a return-period estimate?

**Why it matters.** This is the one place where the group's own supervisor has
published the machinery and nobody has pointed it at the resource field —
Seshadri (2018) on optimal spatial averaging, Prakash et al. (2019) on the
averaging error factor, Gangopadhyay et al. (2023) on Indian wind decorrelation.
The missing step is the **tail**.

**Result.** Ensemble of 14 seeds, 44-year records:

| Climate | N_eff (AR(1)) | N_eff (autocorr-sum) | N_eff/N | 1-in-50 CI widening |
|---|---|---|---|---|
| no decadal mode | 48.7 | 44.0 | 1.00 | 1.00× |
| 22-year mode | 13.2 | 9.8 | 0.22 | 2.16× |
| 60-year mode | 13.0 | 5.6 | 0.13 | 2.88× |

1. **A 44-year record is not 44 samples** — under a quarter of nominal with a
   22-year mode. The no-mode control returns the nominal length, which is the
   check that the estimator is not manufacturing a correction out of noise.
2. **The cheap estimator is biased in the flattering direction.** The AR(1)
   form reports roughly twice the autocorrelation-sum value once a mode is
   present, and the gap widens as the mode lengthens — AR(1) reads only lag 1,
   and a decadal mode puts its power at lags 2–10, where that estimator is
   blind.
3. **The correction at least doubles the error bar**, and the widening grows
   with the mode's timescale — the direction that matters, since PDO and AMO are
   the long ones.

**Why this is the cheapest paper in the programme.** No optimisation model, no
demand dataset, no new method. ERA5, the group's own spatial-averaging
machinery, and the discipline to apply it to the tail rather than the mean.

**The caveat that must be in the paper.** These estimators are noisy on 44
points; read the spread, not the median. The defensible claim is not "N_eff is
10" but "N_eff is materially below N, the correction is at least twofold and
grows with the mode's timescale, and the cheap estimator systematically
understates it."

---

## Toy 4 — The cost of sizing against the wrong decadal phase

`scripts/toy04_phase_flip_regret.py` · Puzzle II · ~42 s

**Question.** Size an over-build on one phase of a slow mode, operate it
through the opposite phase. How large is the regret, and what does hedging cost?

**Result.** Target 99.5%, 12 h storage, phases split by tercile of the index:

| phase amplitude | regret (× the allowance) | hedge cost | pooled design |
|---|---|---|---|
| 8% | 1.6× | +1.4% capacity | 1.2× |
| 15% | 2.5× | +5.7% capacity | 1.4× |
| 25% | 4.6× | +15% capacity | 1.8× |

1. **The regret shows up in reliability, not cost** — the same asymmetry Gøtske
   et al. (2024) report across weather years, where cost moves ±10% while
   adequacy moves from 90% to 99.9%. A cost-only sensitivity study will conclude
   the problem is small; adequacy is where the damage lands.
2. **The hedge is a good trade, and its price scales with the mode.** About 1%
   extra capacity at an 8% amplitude, ~15% at 25% — and it removes the failure
   entirely. At the low end this matches Kebrich et al.'s 1.6–2.9% robustness
   premium across 40 German weather years. At the high end it stops being a
   rounding error, which is when a planner needs to be told.
3. **Pooling helps, but by accident.** The pooled design — what the field does
   today — lands between the two phase-specific designs. It is not catastrophic,
   because a long record does contain bad-phase years. But it weights them by
   how often they *happened to occur in the sample* rather than by how bad they
   are, so a record that happens to over-sample a benign phase inherits that
   bias silently, with no diagnostic in current practice that would reveal it.

**Honest limit.** The phase is known exactly here, which flatters any
phase-aware strategy. Read the numbers as the value available *given perfect
phase knowledge* — an upper bound, and the right one to compute first, because
if it is small the line of enquiry can be dropped cheaply.

---

## Toy 5 — Does the break's clear-sky solar actually hedge anything?

`scripts/toy05_break_sign_structure.py` · Puzzle III · ~27 s

**Question.** A monsoon break is not a Dunkelflaute: wind falls while solar
*rises* and demand surges. How much is the solar recovery worth, and does it
survive the evening peak?

**Result.** Four event structures, everything else held fixed, target 99.5%:

| structure | over-build | break share of deficit |
|---|---|---|
| monsoon break (solar recovers, demand up) | 3.186× | 25.2% |
| no solar recovery (Dunkelflaute-like) | 3.262× | 29.5% |
| solar recovers, demand flat | 3.043× | 15.4% |
| wind collapse alone | 3.093× | 19.0% |

Decomposition: the **solar recovery is worth +0.077× (+2.4%)**; the **demand
surge costs +0.143× (+4.7%)**. The net of a monsoon break against a bare wind
collapse is still **adverse**.

**The real finding — the hedge is entirely storage-mediated.** Essentially none
of the deficit (0.0–0.2%) falls during the solar day. Of course it does not: at
3× over-build the daytime is comfortably covered, and what fails is the night.
So the break's clear-sky solar cannot meet any unserved demand *directly*. Every
unit of its value arrives through storage, by charging a buffer discharged after
sunset. That is a sharper and more testable claim than "solar partly offsets the
wind collapse": the worth of the hedge should scale with installed storage
duration and vanish as duration goes to zero.

**And it erodes as the evening peak grows:**

| evening peak | hedge worth | evening share of deficit |
|---|---|---|
| 0% | +0.099× | 1.7% |
| 13% | +0.087× | 1.7% |
| 26% | +0.077× | 2.0% |
| 40% | +0.066× | 2.7% |

A third of the hedge's value gone. India's demand shape is moving toward a
sharper evening peak as air-conditioning and electric cooking spread, so **the
hedge is worth most now and less later** — the opposite of the direction the
framing needs, and worth saying out loud before a committee says it first.

**Honest limit.** The solar recovery is a prescribed fraction of the monsoon
cloud loss, not a radiative calculation, and **aerosols are absent entirely**.
So this cannot say how large the real hedge is — only what a hedge of a given
size is worth, and what erodes it. The conjecture most at risk is the hedge
itself: aerosol loading during breaks may offset the clear-sky enhancement, so
the framing should not pre-commit to it.

---

## Toy 6 — The exchange rate between information and steel

`scripts/toy06_information_vs_steel.py` · Puzzle IV · ~2 min

**Question.** How many megawatts of over-build does one unit of forecast skill
replace, and does the rate steepen near the saturation point?

**Model.** A flexible resource with a fixed annual energy budget (1% of annual
energy) and a power limit (15% of mean demand) — hydro plus demand response. A
forecast of skill ρ ranks the hours; the budget is spent on the top-ranked ones.
ρ = 1 is perfect foresight, ρ = 0 is climatology.

**Result.** Target 99.8%, 12 h storage, averaged over 3 forecast realisations:

| skill | benign (λ=300 km) | near divergence (λ=1500 km) |
|---|---|---|
| 0.00 | 2.593× | 5.509× |
| 0.20 | 2.480× | 4.708× |
| 0.60 | 2.449× | 4.588× |
| 1.00 | 2.445× | 4.553× |
| **fleet saved by perfect skill** | **5.7%** | **17.3%** |

1. **Information is priceable in megawatts**, which is a number a regulator can
   act on in a way a Brier score is not.
2. **The conjecture survives.** Near divergence the same budget of the same
   information saves three times the fleet fraction it saves in the benign
   regime — because each avoided deficit hour is worth more when the steel
   alternative is priced on a steeper curve. "Where steel stops working,
   information becomes the only remaining asset" holds, and the mechanism is
   just the ratio of two marginal costs, one of which diverges.
3. **But returns to skill are sharply concave, which contradicted the
   expectation.** Moving from climatology to a correlation of just 0.2 captures
   roughly 80% of everything perfect foresight would deliver. The mechanism is
   not an artefact: the flexible budget is small, the deficit hours are numerous
   relative to it, so the operator does not need to find *the* worst hours, only
   to land in the bad part of the distribution. Precision of aim is cheap and
   quickly stops mattering.

   **The policy reading is the opposite of the one a forecasting programme would
   prefer.** The case for subseasonal prediction of break onset does not rest on
   pushing skill toward perfection; it rests on getting *any* usable signal, and
   then on enlarging the flexible budget that signal aims. If this survives on
   real data, the binding constraint is **flexibility, not forecast quality** —
   a finding about where to spend money.

**Honest limit.** This prices skill; it does not demonstrate it. Skill is
imposed as a correlation with the true residual deficit, and deployment uses one
global ranking over the whole record — more foresight than any operator has.
Both inflate the result, so these are upper bounds. The honest version needs
real MJO/BSISO-conditioned break-onset skill, a rolling decision window, and a
flexible resource respecting reservoir dynamics. Schmidt's SDDP machinery, built
for hydropower inflow uncertainty, is the natural tool and the natural
comparison.

**Run it last** — it consumes the others' outputs: the saturation point from
toy 2 sets where the rate steepens, the phase structure from toy 4 sets what is
predictable at long lead, and the break's sign structure from toy 5 sets what
the flexible resource has to cover. But know now what it needs, because that
determines what the earlier papers must report.

---

## What the toys do not establish

Worth repeating, because it is the easiest thing to lose track of:

- **Nothing here is calibrated to Karnataka.** The generator is qualitatively
  monsoon-like and quantitatively arbitrary.
- **λ, τ and χ are dials, not measurements.** Measuring them for the real
  Indian joint wind–solar field is step 1 of the real work, and it is the single
  highest-leverage task because toys 1 and 2 show the sizing answer hangs on
  them.
- **Aerosols are absent**, so toy 5 cannot size the real solar hedge.
- **Toy 6's skill is imposed, not earned**, and its foresight is unrealistic, so
  its numbers are upper bounds.
- **Reliability below ~10⁻⁶ is at the resolution floor** of the record lengths
  used. The toys print `<1e-6` rather than zero, because zero would be a claim
  the record cannot support — and that floor is itself what toy 3 is about.

Treat every number as an order of magnitude and a *sign*. That is what a toy is
for.

---

## Suggested order of work

1. **Toy 3 first.** Fastest, lowest risk, and it is the group's own question
   answered with the group's own machinery. Convert it to ERA5 and it is close
   to a paper.
2. **Toys 1 and 2 in parallel**, once λ and τ are measured for the real field.
   They share the same data build as toy 3, so construct the gridded
   capacity-factor field once and all three fall out of it.
3. **Toy 4** as the constructive half of the non-exchangeability critique,
   with IOD/PDO/AMO indices replacing the synthetic sine.
4. **Toy 5** once break chronologies and satellite irradiance are in hand, so
   the aerosol term is present rather than assumed away. Follow Grochowicz et
   al. (2024): let the system's own response pick the events first, *then* ask
   how well they match the active–break taxonomy — that ordering matters more
   here than in Europe, because no grid-relevant event taxonomy for South Asia
   exists to import.
5. **Toy 6 last**, consuming the rest.
