# Climate Variability, Diminishing Returns, and Robust Portfolios for Solar PV in Karnataka

Code and analysis for the overcapacity question: **how much excess wind and
solar to build, of what kind, on what timescale, and where the
climate-dynamical limits of over-building lie.**

The organising claim is that overcapacity sizing already exists as an
engineering-economic problem — the overbuild-and-curtail lineage after Perez et
al. (2019), and the weather-year robustness school after Grochowicz et al.
(2023) and Gøtske et al. (2024) — but **nobody has posed it as a
climate-dynamics problem**. Those engineering answers rest on stationarity and
exchangeability assumptions their authors never examined, and the assumptions
fail precisely in the tropical-monsoon regimes where the transition's stakes are
highest.

## Start here

| File | What it is |
|---|---|
| [`docs/literature_survey_overcapacity.md`](docs/literature_survey_overcapacity.md) | Working literature survey. The two neighbour literatures, the exchangeability critique, the four puzzles, the Indian layer, and the unused spatial-sampling machinery the group already owns. Provenance-tagged throughout. |
| [`docs/toy_problems.md`](docs/toy_problems.md) | Six toy problems with results, what each establishes, and what it does not. |
| `scripts/toy0*.py` | The toys themselves. Each prints its own question, results, and honest limits. |
| `src/toy_climate.py` | Synthetic monsoon-flavoured resource and demand generator, with λ, τ and χ as explicit dials. |
| `src/overbuild.py` | Over-build sizing, reliability metrics, CVaR, effective sample size, return levels. |

## Quick start

```bash
pip install -r requirements.txt
```

```bash
python3 tests/test_overbuild.py
```

```bash
cd scripts && python3 toy03_independent_monsoons.py
```

Figures are written to `reports/figures/`.

## The toys, in one line each

| Toy | Question | Headline result |
|---|---|---|
| 1 | Is there a scaling law for the over-build? | `r = c·(1−R)^(−b)`, R² ≥ 0.98, with **b set by the spatial decorrelation length** (0.25 → 1.20 as λ goes 50 → 3000 km) and **diverging** at large λ. |
| 2 | Where does steel stop working? | Persistence is **invisible without storage and dominant with it**. Storage and over-build are **complements**, not substitutes. |
| 3 | How many independent monsoons are in 44 years? | **~10** under a 22-year mode, **~6** under a 60-year mode. Return-level error bars widen **2.2–2.9×**. The cheap AR(1) estimator overstates by ~2×. |
| 4 | What does sizing against the wrong decadal phase cost? | A fleet sized in the favourable phase misses its target by **1.6–4.6×** the allowed unserved energy. Hedging costs **1.4–15%** more capacity. |
| 5 | Does the break's clear-sky solar hedge anything? | Worth **+2.4%** of the fleet, against **+4.7%** cost from the demand surge. The hedge is **entirely storage-mediated** and **erodes as the evening peak grows**. |
| 6 | What is the exchange rate between information and steel? | Perfect skill replaces **5.7%** of the fleet in a benign regime, **17.3%** near divergence. But returns to skill are **sharply concave** — the first 0.2 of correlation buys ~80% of the value. |

**Everything above is synthetic.** The toys exist to check that each question is
well-posed, that its effect is detectable, and that the pipeline works, before
real data is committed. No number here is a claim about Karnataka. See the "what
the toys do not establish" section in `docs/toy_problems.md`.

## Next step

Measure λ and τ for the Indian joint wind–solar capacity-factor field from
ERA5, by season and by active/break phase. Toys 1 and 2 show the sizing answer
hangs on those two quantities, and both are measurable before any optimisation
is run. That same data build also feeds toy 3's effective-sample-size result,
which is the cheapest route to a first paper.

`src.toy_climate.generate()` is the single seam where synthetic data enters —
every script reads through it, so swapping in ERA5 is a one-file change.

## Repository layout

```
src/        shared modules (toy_climate, overbuild, data_loading, features_cf)
scripts/    one runnable toy per file, plus _common.py for path setup
docs/       literature survey and toy-problem specifications
tests/      property tests for the toy machinery
data/       raw / processed / external  (git-ignored)
reports/    figures and draft report    (figures git-ignored)
notebooks/  exploratory work
```

## A note on file extensions

The original skeleton files were uploaded with a `.txt` suffix appended —
`README.md.txt`, `src/data_loading.py.txt`, `requirements.txt.txt` and so on.
`src/data_loading.py.txt` and `src/features_cf.py.txt` **cannot be imported**
in that state. New files in this branch use correct extensions; the older ones
are left untouched pending a decision on renaming them.
