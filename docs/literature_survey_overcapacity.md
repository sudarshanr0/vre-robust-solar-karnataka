# The Overcapacity Question — Working Literature Survey

**Scope.** How much excess wind and solar to build, of what kind, on what
timescale, and where the climate-dynamical limits of over-building lie — and
what the existing literature does and does not say about it.

**Status.** Working document, written to sit alongside the project's master
files rather than replace them. The *Ultra Thesis Literature Survey Enriched*
(MASTER_1) remains the authoritative register; the *Positioning Audit*
(MASTER_3) remains the authoritative statement of the novelty claim. This file
is the repository-side working copy: the version that the code in `scripts/`
is written against, and the one to update as toys return results.

**Last external check.** October 2026.

---

## 0. How to read this, and a note on provenance

The project's own standard is that claims about what a paper does and does not
assume should rest on first-hand reading, and that the difference between
reading a paper and reading about it should be stated rather than papered over.
This document keeps that standard by tagging every external claim:

| Tag | Meaning |
|---|---|
| **[corpus]** | In the project corpus. Identification and findings per MASTER_1/MASTER_3, which read these in full or in plain-language companion form. |
| **[verified]** | External, with a DOI or stable link recorded in MASTER_3's register. |
| **[search-only]** | Surfaced in the October 2026 external check for this document. Title, venue and headline finding come from search metadata; **full identification is not confirmed**, because this session's network policy blocks direct publisher access. Treat as a lead to retrieve, not as a citable fact. |
| **[toy]** | Established by the code in this repository, on synthetic data. A statement about the toy, not about Karnataka. |

Three papers in MASTER_3's register could not be retrieved in full text even
with library strategies — Raynaud et al. (2018), Dowling et al. (2020) and
Caglayan et al. (2021). Those flags carry forward here unchanged.

---

## 1. The claim, correctly scoped

The novelty claim has to be scoped before it meets a committee, because
unscoped it is one literature search from refutation — and the refutation would
land on the thesis's strongest contribution.

> Overcapacity sizing exists as an engineering-economic problem: the
> overbuild-and-curtail literature descending from Perez et al. (2019), and the
> weather-year robustness literature culminating in Grochowicz et al. (2023)
> and Gøtske et al. (2024). **Nobody has posed it as a climate-dynamics
> problem.** The engineering answers are conditional on stationarity and
> exchangeability assumptions their authors never examined, and those
> assumptions fail precisely in the tropical-monsoon regimes where the energy
> transition's stakes are highest.

This is strictly stronger than "nobody has studied overcapacity". It gives the
work a named adversary to beat rather than a void to fill, which is the better
position to defend.

**The self-assessment row should therefore read** "Present in engineering form
(Perez lineage; weather-year robustness school); **Absent as climate dynamics**
— the thesis's core novelty", not "Absent".

### 1.1 Is the claim still open? (October 2026 check)

Yes, as far as a targeted search can establish. A search for capacity-expansion
or robust-design work conditioning on ENSO, IOD, PDO or AMO phase, or otherwise
treating weather years as non-exchangeable, returned **no such study**. What it
returned instead was a cluster of recent papers refining *which* weather years
to use — representative-year selection, challenging-year representation,
weather-year-choice impact quantification **[search-only]** — all of which
operate inside the exchangeability assumption rather than questioning it. One
reports that as few as three weather years may suffice to represent 39 years of
net-load variability **[search-only]**, which is the exchangeability assumption
in its purest form: it presumes the 39 years are draws from one distribution
whose variability a subset can stand in for.

This matters for the risk register. MASTER_3 flags that the corrected claim
survives only while the exchangeability critique is accurate, and names the
Grochowicz, Bloomfield and Victoria groups as closest to closing it. As of this
check they have not. The window is open; it is not guaranteed to stay open.

---

## 2. Neighbour literature I — overbuilding as implicit storage

### What it settles

Over-building is economically rational at high renewable penetration;
curtailment should be designed for proactively rather than treated as a failure
mode; and the over-built fraction substitutes for storage — "implicit storage" —
at a fraction of battery cost.

- **Perez, Perez, Rábago & Putnam (2019)** **[verified]** — the founding paper.
  A Minnesota case study shows the firm-kWh premium (firm over unconstrained
  LCOE) collapsing from over 100 to 9 in the conservative cost case, and from
  64 to 7 in the optimistic one, at an optimal oversizing of **3.8–5.7×**.
  Geographic dispersion, a 5% gas allowance and wind–solar blending each cut the
  premium further, reaching 3.5 ¢/kWh — below the 2017 MISO wholesale price.
  A 100% PV US footprint would need ~4,500 GW, about 50 years of 2017-level
  global manufacturing. *DOI 10.1016/j.solener.2018.12.074*

- **van Eldik & van Sark (2026), PEIROCOM** **[verified]** — the most complete
  statement. 37 countries, 10 ERAA weather years. The base wind+solar+battery
  scenario has a firm-kWh premium of 3.72 at 55% curtailment; adding hydrogen
  turbines collapses it to 1.32 at 1.9% curtailment, with the turbines supplying
  only 7.5% of energy. **The critical result for this thesis** is the multi-year
  sensitivity test: over 1–15 climate years the battery-only premium *rises
  steeply with record length* while the hydrogen-turbine scenario stays flat.
  *MASTER_3 gives the corrected DOI as 10.1016/j.enconman.2025.120399.*

- **Minnesota Solar Pathways / Clean Power Research (2020)** **[verified]** —
  69,152 dispatch simulations across 14 MISO sub-regions. Implicit storage
  delivers more cost saving than either geographic dispersion or wind–solar
  hybridisation. Larger, more interconnected footprints cost consistently less.

- **Firm PV with pumped hydro, Iberia (2026)** **[search-only]** — reports a
  least-cost configuration at a PV oversizing factor of **1.33**, and that
  simplified modelling *underestimates* the firm-kWh premium by about 6%. The
  second finding is the interesting one: it says the lineage's own numbers are
  biased optimistic by model simplification, independently of any climate
  argument. Worth retrieving.

- **IEA PVPS Task 16, *Firm Power Generation* (2026)** **[search-only]** —
  institutional consolidation of the lineage; identifies overbuilding plus
  curtailment as a principal cost driver and as a substitute for seasonal
  storage. Useful as the citation that shows this is now established
  engineering practice rather than a fringe proposal.

### What it never asks

Every optimisation in the lineage conditions on a historical weather record
treated as the truth. None asks how the optimal over-build responds to the
*correlation structure* of the climate that generated the record. None
propagates non-stationarity — in mean, in tail, in regime occupancy — through to
the sizing decision. None distinguishes a record drawn from one decadal-mode
phase from one spanning several. And none operates in a monsoon-dominated
domain, where regime persistence and compound structure differ qualitatively
from the midlatitude Dunkelflaute.

The lineage answers *how much, given this weather*. The thesis asks *how much,
given this climate*. The gap between those two questions is the programme.

### A caveat the lineage's own numbers now force

The oversizing factors are not comparable across studies: 3.8–5.7× for
Minnesota PV-only, 1.33× for Iberian PV-plus-pumped-hydro, a premium of 3.72
falling to 1.32 for Europe depending on whether hydrogen turbines are present.
The spread is not disagreement — it is the *technology-conditioned* form of the
scaling law showing through. van Eldik and van Sark demonstrate this directly:
the exponent on record length depends on which flexibility options exist. So
any scaling law the thesis proposes must be stated as a family of curves indexed
by flexibility technology, not a single curve. **[toy]** Toy 2 reaches the same
conclusion from the physics side and sharpens it: storage and over-build behave
as *complements*, not substitutes, so "implicit storage" is a claim about cost
rather than about physics, and it is conditional on the operating point.

---

## 3. Neighbour literature II — weather-year robustness

This is the thesis's closest methodological neighbour and deserves a careful
genealogy, because it is where a referee will come from.

### Foundations (2016–2020)

| Work | What it establishes |
|---|---|
| **Bloomfield et al. (2016)** **[verified]** | 36 years of MERRA-derived GB data: baseload energy variability rising up to 1100% from no-wind to high-wind penetration. A bootstrap over sample length shows single-year estimates of required baseload capacity erring by ~50%, 10-year samples by ~15% — and the authors state explicitly that 36 years *still* likely underestimates true climate uncertainty. Flags that consecutive-year sampling worsens the underestimate through serial correlation. |
| **Pfenninger (2017)** **[verified]** | 42 time-resolution-reduction methods against 25 GB years. No method is best across years. Running all 25 years individually gives optimal capacities spanning a 30 GW range even after discarding the most extreme year. |
| **Staffell & Pfenninger (2018)** **[verified]** | First to model wind, solar *and* weather-sensitive demand jointly. Single-year error is metric-dependent: ±3% on peak demand, ±13% on minimum net demand, ±23% on hours of negative net demand. |
| **Collins et al. (2018)** **[verified]** | 30 European years in a constrained dispatch model. Country-level variability (GB up to 9×) exceeds continental. Several metrics scale roughly *linearly* with VRE penetration. |
| **Zeyringer et al. (2018)** **[verified]** | The clearest operational-failure demonstration: an 80% VRE GB system shows over 5% of hours with unmet demand when design year and operating year diverge. Transmission is a no-regret investment across all 10 years; storage and flexible generation are not. |
| **Schlachtberger et al. (2018)** **[verified]** | Total system cost strikingly *insensitive* to weather year (62.6–67.9 €/MWh over four years) while the technology *mix* shifts considerably. A four-year joint optimisation tracks the worst single year's cost almost exactly. |
| **Kumler et al. (2019)** **[verified]** | ERCOT: *capacity-value* interannual variability (up to 28.5% summer wind, 45.1% winter solar) vastly exceeds *generation* variability (~5%). Planning on average capacity value understates firm contribution by 2.2 GW. |
| **Raynaud et al. (2018)** **[verified, abstract only]** | Gives the field its event vocabulary: an "energy drought" is a period when combined renewables supply under 20% of demand. |
| **Dowling et al. (2020)** **[verified, secondary only]** | Cited downstream as establishing that VRE system costs are especially sensitive to long-duration storage cost, and that multi-year modelling is needed to capture long-duration effects. |

### Methods for tractability

- **Hilbers, Brayshaw & Gandy (2020)** **[verified]** — importance subsampling.
  Preserving the extreme days a preliminary run flags as costly, then clustering
  the remainder, beats k-medoids: a 48-day k-medoids design fails to meet 0.05%
  of demand on average, versus near-zero for importance subsampling, at roughly
  double the compute. The advantage *grows* with record length. The importance
  function — ranking time steps by realised cost — operationalises "which years
  matter" computably, and is the machinery Puzzle II needs before it can claim
  specific years are non-exchangeably more important.

- **Schyska et al. (2021)** **[verified]** — the misallocation metric: the extra
  cost of forcing a model optimised under one scenario to use another's
  capacities as a lower bound. A proven pseudometric, so it is mathematically
  well-behaved enough to build a scaling law on. Temporal resolution and
  weather-period choice matter far more than spatial resolution, and
  **2000–2006 is identified as measurably unrepresentative** — a direct
  precedent for *computing*, rather than asserting, that a weather window is
  unrepresentative.

- **Caglayan et al. (2021)** **[verified, secondary only]** — up to 20%
  weather-year cost variation for a European electricity/hydrogen system, plus
  an iterative averaging heuristic that Kebrich et al. show converges to a
  feasible but over-priced solution. Useful as a named baseline to beat.

### The current frontier

- **Ruhnau & Qvist (2022)** **[verified]** — the classic Dunkelflaute (≤2 weeks)
  is confirmed, but the storage-*defining* period extends to **9–12 weeks** once
  clustered scarce spells, storage losses and charging-rate limits are all
  counted. Single-year optimisation underestimates required storage by roughly
  half. Adding flexible bioenergy stretches the defining period past a year.
  *The relevant timescale for sizing storage is not fixed; it stretches as more
  flexibility is added.*

- **Grochowicz et al. (2023)** **[verified]** — intersects the near-optimal
  spaces of 41 single-year optimisations and finds a non-empty robust
  intersection at <1% extra cost over the worst single year. Near-optimal-space
  *volume* differs by a factor of **79** between the least and most restrictive
  years, while its *shape* stays broadly similar — weather-year difficulty
  behaves like a smooth scale factor, not a structural break. Only two years
  (1985, 1987) have individually-optimal designs already inside the robust
  intersection. The discussion explicitly calls for "a deeper understanding of
  which [weather developments] will limit flexibility and what events are
  defining."

- **Grochowicz, van Greevenbroek & Bloomfield (2024)** **[verified]** — uses
  electricity shadow prices rather than meteorological thresholds to identify
  system-defining events across 40 years. The resulting 32 events match
  traditional weather-regime classification only weakly: they occur during
  Scandinavian Blocking more than twice as often as climatology predicts, and
  resemble a fusion of blocking and negative-NAO structure rather than any named
  regime. A single week can account for 18–77% of a year's system cost.
  **Methodologically this is the template for Puzzle III**: let the system's own
  response define the events, *then* ask how well they match the atmospheric
  taxonomy — rather than assuming a taxonomy built for another climate.

- **Gøtske et al. (2024)** **[verified]** — 62 weather years, sector-coupled,
  3,844 design×operating-year combinations. Total cost varies only ±10% but
  resource adequacy ranges from **90% to 99.9%** depending on design year. The
  headline: the years causing the worst blackouts (1966, 1968, 1972) are *not*
  the years with the most extreme annual-average statistics — 1968's annual wind
  resource was above that of eight other years. The damage comes from short,
  compounding sub-annual events invisible to annual means.

- **Kebrich et al. (2025)** **[verified]** — formalises multi-year robust sizing
  as adaptive two-stage robust optimisation, with an iterative solve–stress–patch
  algorithm converging to a robust design at only **1.6–2.9%** above the
  theoretical lower bound. Using IRENA's recommended representative year instead
  underestimates true robust cost by **more than 10%**. The dominant failure mode
  is a named physical object — a *cold dark lull* — with one instance (1994)
  driving most of the required backup.

- **Schmidt (2025)** **[verified]** — SDDP adapted from hydropower inflow
  uncertainty to long-duration hydrogen storage under genuinely limited
  foresight. A realistically uncertain operator stockpiles defensively and
  shifts investment toward predictable solar and away from wind (**+25% solar,
  −20% onshore wind**, UK case) purely because of predictability, holding
  resource quality fixed. **The closest quantitative precedent for Puzzle IV
  anywhere in the corpus.**

- **Grochowicz, Bloomfield & Victoria (2025)** **[verified]** — 80 ERA5 years
  (1941–2021). About a third of total annual cost accrues during
  system-defining events occupying ~1% of hours. Backup technologies face
  structural financial risk: hydrogen fuel-cell capacity ranges from negligible
  in 2019/20 to 77 GW in 1965/66. **Critically, no single year among all 80 is
  worst on both long-term and short-term stress** — long-term metrics point to
  1962/63 and 1941/42, short-term to 1965/66. The correlation between a design
  year's own cost and its out-of-sample reliability is r = −0.86 for long-term
  stress and far weaker for short-term. The 1960s stand out as a persistently
  low-wind, high-demand *decade* — an empirical decadal signature the paper does
  not explain.

- **IEA, *Managing seasonal and interannual variability of renewables*
  (2023)** **[verified]** — four idealised climate-zone systems at 70–90% VRE.
  Hydropower's interannual coefficient of variation (26–62%) dwarfs wind's
  (3–9%) and solar's (6–17%) everywhere. A 12-year Polish sequence shows three
  wet years, two average, and **seven consecutive drought years** — genuine
  multi-year persistence, not scatter about a mean. The Tropical case study
  (wind–hydro co-drought in the rainy season) is the closest structural analogue
  to a monsoon regime anywhere in the corpus.

### The exchangeability critique — the hinge

Every study above treats weather years as exchangeable samples: pooled,
intersected, or iterated over, with robustness meaning feasibility across the
pool. Three assumptions hide inside that procedure.

1. **Stationarity.** The pooled record is treated as the future's distribution,
   though the transient circulation response and projected tail changes say
   otherwise.
2. **Exchangeability.** Years are interchangeable draws — but decadal modes
   (IOD, PDO, AMO) make the joint resource–demand distribution phase-dependent,
   so a forty-year record may sample only one or two phase combinations.
3. **Midlatitude geography.** The event taxonomy (Dunkelflaute, cold dark lulls)
   and the seasonal structure are European. Nothing engages monsoon regime
   persistence, active–break chronology, or the supply–demand compound of a
   break heatwave.

Each is a climate-dynamics question. Each maps to a puzzle in §5.

**The critique is now quotable rather than merely assertable.** Three
admissions from inside the school itself:

- Bloomfield et al. (2016) flag that consecutive-year sampling understates
  uncertainty through serial correlation — then never follow it into a
  decadal-mode analysis.
- Grochowicz et al. (2024) state that pinning down what makes certain years
  difficult "remains complicated and computationally expensive."
- Grochowicz et al. (2023) explicitly call for understanding "what events are
  defining."

Add Gøtske's finding that the worst blackout years are not the worst
annual-average years, and the IEA's real seven-year Polish drought run, and the
case rests on five independent empirical instances rather than one theoretical
argument.

---

## 4. The bridge the field asked for

**Craig et al. (2022), "Overcoming the disconnect between energy system and
climate modeling", *Joule* 6(7), 1405–1417** **[verified]** — a 21-author
perspective spanning both neighbour literatures (Bloomfield, Grochowicz, Kittel,
Zeyringer, Brayshaw among them). It diagnoses the disconnect structurally:
energy modellers are trained on single-year, historical, deterministic series
and want hourly validated data; climate modellers produce multi-decadal
ensembles at coarse resolution validated on meteorological skill, with no notion
of which variables or co-variabilities matter for grid stress. Its central
admission — that even satellite-era reanalyses are "too short to capture
multidecadal climate variability" — is the non-exchangeability claim stated from
*inside* the energy-modelling community.

Cite early and often. It converts the thesis framing from a private conviction
into a response to a published, multi-author call from the field's own centre of
gravity — and it is European-authored with zero monsoon content, so the thesis
is an instance of the agenda it calls for, in a domain its author list cannot
reach.

---

## 5. The hidden assumptions, as four puzzles

Each is unanswered in any literature, tractable with available tools, and would
change how planners or scientists act.

| # | Puzzle | The question | Hidden assumption it attacks |
|---|---|---|---|
| **I** | **A scaling law, and where it diverges** | How does the over-build needed to hold a reliability target scale with the resource decorrelation length λ, the persistence timescale τ, and the tail-dependence coefficient χ? Is there a compounding-duration threshold beyond which no feasible over-build buys adequacy? | Case-by-case numbers with no law |
| **II** | **Sizing against which climate?** | Decompose over-build uncertainty into decadal-phase variance versus interannual noise. Does an over-build sized under one IOD × PDO phase fail in the opposite phase, and by how much? | Exchangeability |
| **III** | **The grid-killer break as one object** | What is the four-variable dependence structure — wind, solar, hydro, demand — *conditional on monsoon-break phase*? Does break clear-sky solar self-hedge the wind collapse and demand surge, and does the hedge survive the evening peak? | Midlatitude geography |
| **IV** | **Information versus steel** | In a minimax or CVaR planning problem, how many megawatts of over-build does one unit of subseasonal forecast skill substitute for — and does the rate diverge near the Puzzle I threshold? | Perfect-or-zero foresight |

> *Puzzle I asks how much steel the climate demands and where steel stops
> working; Puzzle II asks against which climate the steel is sized; Puzzle III
> identifies the single atmospheric object that sets the worst case in South
> Asia; and Puzzle IV prices the only asset — information — that still works
> where steel does not.*

### A candidate fifth thread

The long-term/short-term resilience bifurcation in Grochowicz et al. (2025) —
that no single year is worst on both counts, and that low-utilisation backup
faces structural financial risk — does not map cleanly onto any of the four. It
recurs often enough across the frontier papers to deserve explicit treatment
inside Puzzle I: **a scaling law reporting one number for "required over-build"
without stating whether it targets long-run adequacy or short-run peak survival
risks being correct for one and silently wrong for the other.** **[toy]** Toys 1
and 2 reproduce exactly this hazard — the same climate yields different answers
depending on which reliability metric is used, and persistence is invisible to
one of them.

---

## 6. The Indian and monsoon-specific layer

- **Gangopadhyay & Seshadri (2024), *Applied Energy*** **[corpus]** — the
  Karnataka wind–solar–storage Pareto frontier. Rests on a **single weather
  year**, which is precisely the fragility the robustness school documents
  elsewhere, and the gap the first paper repairs.
- **Gangopadhyay & Seshadri (2026)** **[corpus]** — seasonal-balancing review:
  no single balancing technology suffices, and the right mix is climate-specific.
- **Gangopadhyay, Seshadri & Toumi (2023)** **[corpus]** — spatial decorrelation
  and aggregation smoothing of Indian wind, plus diurnal-phase complementarity,
  including smoothing that does not depend on distance.
- **Dijkstra, Bloomfield & Hunt (2025), *Advances in Geosciences* 65, 127**
  **[verified]** — weather patterns responsible for renewable-energy droughts
  over India. Droughts defined as wind-plus-solar potential in the **lowest
  2.5%** of climatology, from ERA5-derived synthetic production, **1979–2022**.
  Events **cluster in winter** (commonly November–February), the longest
  historical event is **nine days**, and north India shows **poor wind–solar
  complementarity**.
- **Hunt & Bloomfield** **[corpus]** — deficit days cluster in November and
  December; surplus days run at 3.7 per year concentrated late May to early
  August, *inside* the monsoon; longest surplus run nine consecutive days (June
  1984). Reports **+0.12 deficit-solar-days per year in July–August, p = 0.01** —
  the only significant trend in their extreme-day record — and explicitly
  declines to explain it.
- **van der Most et al.** **[corpus]** — temporal compounding: season-chaining
  defeats storage.
- **Venkataramana et al. (2025)** **[corpus]** — India's 500 GW target hinges on
  inter-regional transmission and balancing.
- **Masiwal, Jha, Singh and colleagues** **[corpus]** — active–break dynamics,
  intraseasonal oscillations, low-pressure systems, Somali jet energetics: the
  physical machine behind the South Asian tail, and the group's home terrain.

### The uncomfortable finding, stated plainly

For **today's** fleet — wind-heavy and southern — the monsoon is when the grid
is comfortable. Deficit days cluster in November and December. Both Hunt &
Bloomfield (historical stress test) and Dijkstra et al. (weather-pattern
classification) reach this by different methods. So the "grid-killer break"
becomes a grid event chiefly *through demand*, and demand is where the data is
thinnest and the climate science least distinctive.

The defence is available and reasonable: today's fleet is wind-heavy, and as
solar share and cooling demand both grow, the break-compound event plausibly
becomes dominant. But note what kind of argument that is — **a projection
argument, not an observational one** — and it should be presented as such.
**[toy]** Toy 5 supports the projection reading and sharpens the mechanism: the
break's solar recovery is worth something, but it is worth *less* as the evening
peak grows, and India's demand shape is moving toward a sharper evening peak.

**A live illustration, October 2026** **[search-only]**: press reporting
describes an Indian power deficit deepening as weak wind generation compounded a
hydro slump following poor monsoon rains — a 5.8 GW shortfall against 232 GW
demand on 3 October, with maximum available wind down by nearly a third. Not
evidence for a paper, but a reminder that the compound wind–hydro failure mode
is not hypothetical, and a useful motivating anecdote.

---

## 7. The sampling problem — and the group's unused machinery

This is the most consequential finding in the project's own reassessment
(MASTER_6, Part B3), and it reframes the whole programme.

The supervisor has a sustained published line — four papers across a decade — on
how much independent information a spatial climate field over India contains:

| Paper | What it establishes |
|---|---|
| **Seshadri (2018), *Spatial Statistics*** **[corpus]** | Optimal spatial averaging: how the correlation structure between locations sets the variance of a regional average, and how to weight to minimise error. |
| **Prakash, Seshadri, Srinivasan & Pai (2019), *J. Hydrometeorology*** **[corpus]** | The *averaging error factor* — one number combining a field's spatial variability with the number of available samples. Applied to Indian monsoon rainfall. |
| **Mitra & Seshadri (2019)** **[corpus]** | Spatially and temporally coherent rainfall anomalies over India, against the location-wise approach that treats each point independently. |
| **Gangopadhyay, Seshadri & Toumi (2023)** **[corpus]** | Spatial decorrelation and aggregation smoothing of Indian wind. |

**What has never been done.** Nobody has applied the averaging-error-factor and
coherence machinery to the **joint wind–solar resource field, in the tail rather
than the variance**, to obtain the effective sample size for energy-relevant
extremes. Gangopadhyay treats the variance of aggregate wind output; Prakash
treats the uncertainty of a monthly rainfall mean. The extreme-value question —
*how many independent monsoons a 44-year record contains for the purpose of
estimating a once-in-fifty-year compound deficit* — sits exactly in the gap
between them.

This is not importing an outside method. It is the obvious continuation of a
line the group already owns, aimed at the question the supervisor keeps
returning to.

### The external machinery that completes it

The classical effective-sample-size literature supplies the estimators
**[search-only]**: Anderson (1971) and Trenberth (1984) for autocorrelation-based
effective sample size; Thiébaux & Zwiers (1984) comparing estimators; Zwiers &
von Storch (1995) on the consequences for significance testing; Bretherton et
al. (1999) for the autocorrelation-sum form. None has been applied to a joint
resource tail.

Two further leads **[search-only]**:

- A drought-threshold study reports that **even with 1,000 effectively
  independent samples, the uncertainty on a 50-year return period is about
  ±20 years**, and argues that threshold-based drought severity/duration
  analyses become meaningless when threshold errors are large. This is the
  most directly quotable external support for the effective-sample-size
  argument, and it is from hydrology rather than energy — so it is not already
  in the energy literature's bloodstream.
- Ensemble boosting for return-period estimation in climate models (2025) — a
  method for the regime where the record is shortest, which is where Puzzle I's
  divergence question lives.

### What the toy establishes

**[toy]** Toy 3 (`scripts/toy03_independent_monsoons.py`) runs this on
synthetic data with a known answer:

| Climate | N | N_eff (AR(1)) | N_eff (autocorr-sum) | N_eff/N | 1-in-50 CI widening |
|---|---|---|---|---|---|
| no decadal mode | 44 | 48.7 | 44.0 | 1.00 | 1.00× |
| 22-year mode | 44 | 13.2 | 9.8 | 0.22 | 2.16× |
| 60-year mode | 44 | 13.0 | 5.6 | 0.13 | 2.88× |

Three things fall out, all of which should survive the move to real data:

1. **A 44-year record is not 44 samples.** With a 22-year mode the effective
   sample size is under a quarter of nominal; with a 60-year mode, an eighth.
   The no-mode control returns the nominal length, which is the check that the
   estimator is not manufacturing a correction out of noise.
2. **The cheap estimator is biased in the flattering direction.** The AR(1)
   form reports roughly twice the effective sample size of the
   autocorrelation-sum form once a decadal mode is present, and the gap widens
   as the mode lengthens — because AR(1) reads only lag 1, and a decadal mode
   puts its power at lags 2–10 where that estimator is blind. *The more decadal
   structure a record has, the more the convenient estimator understates the
   problem.*
3. **The correction at least doubles the error bar**, and the widening grows
   with the mode's timescale — the direction that matters, since the modes of
   interest (PDO, AMO) are the long ones.

---

## 8. Where the work should start

Two honest orderings exist in the project's own documents, and they disagree.
Both are recorded here because the disagreement is the live strategic question.

**MASTER_3's ordering** (publication-vehicle logic): Puzzle II first, as the
critique-plus-fix whose structure is fully specified and whose data are public;
Puzzle I in parallel as the flagship; Puzzle III second; Puzzle IV last,
consuming the others' outputs.

**MASTER_6's ordering** (group-fit logic): the overcapacity question survives as
the *motivation and policy payoff* but stops being the deliverable. The spine
becomes the spatial statistics of the Indian resource field — effective sample
size in the tail, §7 above — and the flagship becomes a climate-science
attribution paper on the significant July–August solar-deficit trend that Hunt
& Bloomfield leave unexplained. The reasoning: none of the three originally
planned papers is a climate-science paper, and a CAOS committee is entitled to
ask where the atmospheric science is.

**These are more compatible than they look.** Puzzle II *is* the
effective-sample-size question wearing energy clothes: non-exchangeability and
effective sample size are the same statement about the same autocorrelation
structure. Toy 3 computes it as a sampling result; toy 4 computes it as a
sizing result. The same analysis supports both framings, and the choice is about
which journal it is written for — which is a decision that can be deferred until
the numbers exist.

**What to resolve first**, per MASTER_6 Part H, because it moves more of the
architecture than anything else:

1. **Demand-data reality.** What Grid-India and CEA load data can actually be
   obtained — resolution, years, state-level or national. If monthly national
   totals, the compound supply–demand chapter waits. If hourly Karnataka back to
   ~2015, it moves up.
2. **Ask directly why the spatial-sampling line was never pointed at the
   resource field.** Four papers, one supervisor, a decade, a repeatedly stated
   concern about effective sample size — and no connection to wind or solar.
   Either the connection is obvious and assumed, in which case the spine is
   immediately endorsed, or there is a technical reason it does not carry over
   that is worth knowing before six months are spent. One meeting de-risks the
   entire spine.

---

## 9. What the toys establish, and what they do not

Full specifications are in [`toy_problems.md`](toy_problems.md); code is in
`scripts/`. Everything here is **[toy]** — synthetic data, controlled knobs, no
claim about Karnataka. Their purpose is to check that each puzzle is
well-posed, that the effect it predicts is detectable, and that the analysis
pipeline works, *before* real data is committed to.

| Toy | Finding | Bearing on the literature |
|---|---|---|
| 1 | Required over-build fits **r = c·(1−R)^(−b)**, R² ≥ 0.98, with **b rising from 0.25 to 1.20 as λ rises from 50 km to 3000 km** — and diverging (no reachable target) at large λ. | Converts case-study numbers into a curve. Published single oversizing factors are one point each, often at an unstated reliability target. |
| 2 | τ is **invisible** without storage and **dominant** with it. Storage and over-build are **complements**: 24 h of storage steepens the steel elasticity from −1.2 to −7. At 3× over-build, 24 h of storage beats *doubling the fleet* by two orders of magnitude. | "Implicit storage" is a cost claim, not a physical one. Supports van Eldik & van Sark's technology-conditioned record-length effect. |
| 3 | 44 years contains **~10 independent samples** under a 22-year mode, **~6** under a 60-year mode; the AR(1) estimator overstates by ~2×; the 1-in-50 CI widens 2.2–2.9×. | Every confidence interval in the robustness school assumes exchangeable annual draws. |
| 4 | A fleet sized in the favourable phase misses its 99.5% target by **1.6× to 4.6×** the allowed unserved energy when the phase flips. Hedging on the hard phase costs **1.4% to 15%** more capacity. Pooling helps but does not close the gap. | The phase analogue of Kebrich's 1.6–2.9% robustness premium. Does not exist in the literature. |
| 5 | The break's solar recovery is worth **+0.077× of the fleet (+2.4%)**; the demand surge costs **+0.143× (+4.7%)**, so the net is adverse. **Essentially none of the deficit falls during the solar day**, so the hedge is entirely storage-mediated — and it loses a third of its value as the evening peak grows from 0% to 40%. | Shows a Dunkelflaute template would over-size an Indian fleet, and that the sign-structure question is about *composition*, not magnitude. |
| 6 | Perfect forecast skill replaces **5.7%** of the fleet in a benign regime and **17.3%** near divergence — the conjectured steepening. But returns to skill are **sharply concave**: the first 0.2 of correlation captures ~80% of all available value. | Prices information in megawatts. The concavity suggests the binding constraint is *flexible capacity*, not forecast quality. |

**What they do not establish.** Nothing here is calibrated to Karnataka. The
synthetic generator is qualitatively monsoon-like and quantitatively arbitrary;
λ, τ and χ are dials rather than measurements; aerosols are absent, so toy 5
cannot say how large the real solar hedge is; toy 6 imposes skill as a
correlation rather than earning it, and deploys flexibility with more foresight
than any operator has, so its numbers are upper bounds. Treat every number as
an order of magnitude and a *sign*, which is what a toy is for.

---

## 10. Immediate next steps

1. **Measure λ and τ for the Indian joint wind–solar capacity-factor field**
   from ERA5, by season and by active/break phase. These are the two quantities
   toys 1 and 2 show the sizing answer hangs on, and both are measurable before
   any optimisation is run. This is also the data build that §7's spine needs,
   so it is the single highest-leverage task.
2. **Replace `src/toy_climate.generate()` with ERA5-derived capacity factors.**
   Every script reads its data through that one function specifically so this
   substitution is a one-file change.
3. **Run toy 3 on the real record** with IOD, PDO and AMO indices in place of
   the synthetic sine. Deliverable: the effective sample size of the Indian
   joint resource tail, and the correction factor for published return levels.
4. **Read in full, before the claim is defended**: Perez et al. (2019), van
   Eldik & van Sark (2026), the Grochowicz–Gøtske–Kebrich cluster, and Craig et
   al. (2022). The scoped claim in §1 rests on first-hand knowledge of what
   those papers assume, and provenance honesty requires that the assessment be
   the candidate's own.
5. **Retrieve the [search-only] items**, especially the Iberian pumped-hydro
   paper (its claim that simplified modelling understates the firm-kWh premium
   by 6% is a methodological criticism of the lineage from inside it) and the
   classical effective-sample-size references, which the spine will cite
   directly.
6. **Resolve the two questions in §8** — demand-data reality, and why the
   spatial-sampling line was never pointed at the resource field.

---

## Reference register

Full identification for **[corpus]** entries lives in MASTER_1's register, which
remains authoritative. **[verified]** entries carry DOIs recorded in MASTER_3's
register. **[search-only]** entries are leads, listed with what is known.

### External, verified

1. Perez, M., Perez, R., Rábago, K.R., Putnam, M. (2019). Overbuilding &
   curtailment: the cost-effective enablers of firm PV generation. *Solar
   Energy* 180, 412–422. doi:10.1016/j.solener.2018.12.074
2. van Eldik & van Sark (2026). Firm wind and solar photovoltaic power with
   proactive curtailment: a European analysis (PEIROCOM). *Energy Conversion and
   Management*. doi:10.1016/j.enconman.2025.120399 *(DOI per MASTER_3's
   correction)*
3. Clean Power Research / CESA (2020–21). Minnesota Solar Pathways: MISO Solar
   Potential Analysis.
4. Craig, M.T., Wohland, J., Stoop, L.P., *et al.* (2022). Overcoming the
   disconnect between energy system and climate modeling. *Joule* 6(7),
   1405–1417. doi:10.1016/j.joule.2022.05.010
5. Bloomfield, H.C., Brayshaw, D.J., Shaffrey, L.C., Coker, P.J., Thornton,
   H.E. (2016). *Environmental Research Letters* 11, 124025.
   doi:10.1088/1748-9326/11/12/124025
6. Pfenninger, S. (2017). *Applied Energy* 197, 1–13.
   doi:10.1016/j.apenergy.2017.03.051
7. Staffell, I., Pfenninger, S. (2018). *Energy* 145, 65–78.
   doi:10.1016/j.energy.2017.12.051
8. Collins, S., Deane, P., Ó Gallachóir, B., Pfenninger, S., Staffell, I.
   (2018). *Joule* 2(10), 2076–2090. doi:10.1016/j.joule.2018.06.020
9. Zeyringer, M., Price, J., Fais, B., Li, P.-H., Sharp, E. (2018). *Nature
   Energy* 3, 395–403. doi:10.1038/s41560-018-0128-x
10. Schlachtberger, D.P., Brown, T., Schäfer, M., Schramm, S., Greiner, M.
    (2018). *Energy* 163, 100–114. doi:10.1016/j.energy.2018.08.070
11. Raynaud, D., Hingray, B., François, B., Creutin, J.D. (2018). *Renewable
    Energy* 125, 578–589. doi:10.1016/j.renene.2018.02.130 — **full text not
    retrieved**
12. Kumler, A., Losada Carreño, I., Craig, M.T., Hodge, B.-M., Cole, W.,
    Brancucci, C. (2019). *Environmental Research Letters* 14, 044032.
    doi:10.1088/1748-9326/aaf935
13. Dowling, J.A., *et al.* (2020). *Joule* 4, 1907–1928.
    doi:10.1016/j.joule.2020.07.007 — **full text not retrieved**
14. Hilbers, A.P., Brayshaw, D.J., Gandy, A. (2020). Importance subsampling for
    power system planning under multi-year demand and weather uncertainty.
    *Proc. PMAPS 2020*, IEEE.
15. Caglayan, D.G., *et al.* (2021). *International Journal of Hydrogen Energy*
    46(57), 29376–29390. — **full text not retrieved; DOI unresolved in
    MASTER_3's register**
16. Schyska, B.U., Kies, A., Schlott, M., von Bremen, L., Medjroubi, W. (2021).
    The sensitivity of power system expansion models. *Joule* 5(10), 2606–2624.
17. Ruhnau, O., Qvist, S. (2022). *Environmental Research Letters* 17, 044018.
    doi:10.1088/1748-9326/ac4dc8
18. Grochowicz, A., van Greevenbroek, K., Benth, F.E., Zeyringer, M. (2023).
    *Energy Economics* 118, 106496. doi:10.1016/j.eneco.2022.106496
19. Grochowicz, A., van Greevenbroek, K., Bloomfield, H.C. (2024).
    *Environmental Research Letters* 19, 054038. doi:10.1088/1748-9326/ad374a
20. Gøtske, E.K., Andresen, G.B., Neumann, F., Victoria, M. (2024). *Nature
    Communications* 15, 10680. doi:10.1038/s41467-024-54853-3
21. Kebrich, S., Engelhardt, F., Franzmann, D., Büsing, C., Linßen, J.,
    Heinrichs, H. (2025). Robust capacity expansion modelling for renewable
    energy systems under weather and demand uncertainty. arXiv:2504.06750
22. Schmidt (2025). On long-duration storage, weather uncertainty and limited
    foresight. arXiv:2505.12538
23. Grochowicz, A., Bloomfield, H.C., Victoria, M. (2025). Resilience metrics to
    guide back-up investments in the power system during extreme weather.
    arXiv:2508.05163
24. International Energy Agency (2023). *Managing seasonal and interannual
    variability of renewables*.
25. Dijkstra, Bloomfield & Hunt (2025). Identifying weather patterns responsible
    for renewable energy droughts over India. *Advances in Geosciences* 65,
    127. https://adgeo.copernicus.org/articles/65/127/2025/

### Leads from the October 2026 check — identification unconfirmed

26. *Firm power generation with photovoltaic overbuilding and pumped hydro
    storage* (2026). Iberian case; least-cost PV oversizing factor 1.33;
    simplified modelling understates the firm-kWh premium by ~6%.
    ScienceDirect pii S0360544225014422.
27. IEA PVPS Task 16, *Firm Power Generation 2026*. Overbuilding plus
    curtailment as a principal cost driver and substitute for seasonal storage.
28. *Quantifying the impacts of weather year selection on power sector capacity
    expansion models* (2025). ScienceDirect pii S0360544225046213.
29. *Representing net load variability in electricity system capacity expansion
    models accounting for challenging weather-years* (2024). ScienceDirect pii
    S0360544224041240.
30. *Bridging the climate to energy data gap: simulated annealing for
    representative climate year selection*. Reports that as few as three
    weather years may represent 39 years of variability.
31. Effective-sample-size lineage: Anderson (1971); Trenberth (1984); Thiébaux
    & Zwiers (1984); Zwiers & von Storch (1995); Bretherton et al. (1999).
32. *100 Years of Data is not Enough to Establish Reliable Drought Thresholds*.
    Reports ±20 years of uncertainty on a 50-year return period even with 1,000
    effectively independent samples.
33. *Estimating return periods for extreme events in climate models through
    Ensemble Boosting* (2025). *Weather and Climate Dynamics* 6, 1147.
34. Press reporting, October 2026: Indian power deficit deepening on weak wind
    plus post-monsoon hydro slump; 5.8 GW shortfall against 232 GW demand on
    3 October.

### Corpus anchors leaned on here

Gangopadhyay & Seshadri (2024, *Applied Energy*); Gangopadhyay & Seshadri
(2026); Gangopadhyay, Seshadri & Toumi (2023); Seshadri (2018, *Spatial
Statistics*); Prakash, Seshadri, Srinivasan & Pai (2019, *J. Hydrometeorology*);
Mitra & Seshadri (2019); Pham, Cole & Gagnon (2024, NREL); Newbery & Chyong
(2025, EPRG); Hirth (2013, *Energy Economics*); Denholm et al. (2013, NREL);
van der Most et al.; Bracken et al. (2025); Wang et al. (2025, *Nature
Communications*); Sun et al. (2026); Kittel et al.; Hunt & Bloomfield (2024);
Venkataramana et al. (2025); Masiwal, Dixit & Seshadri (2023, 2025); Jha,
Nanjundiah & Seshadri (2026); Singh, Bala & Seshadri (2026); Seshadri & Dixit
(2022); Seshadri (2017); Coles (2001).

---

*Assessments of what external sources do and do not assume are to be verified by
first-hand reading before any claim resting on them is presented to the
committee. Items tagged **[search-only]** have not been read at all and are
recorded as leads.*
