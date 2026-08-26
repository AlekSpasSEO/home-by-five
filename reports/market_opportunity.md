# Market opportunity

Two things live in this file: the scoring method behind
`data/maidthis_market_opportunity.csv` and the dashboard, and the broader market sizing
for the company itself.

---

## Part 1: the MaidThis market opportunity score

### What was measured

46 markets, on 26 August 2026, from the city centroid on desktop:

- **Search volume and CPC** for ten keywords per market, Google Ads data via DataForSEO
- **Two Google Maps packs** per market, for `house cleaning service` and
  `airbnb cleaning service`, 20 results deep
- **One organic SERP** per market, `house cleaning services` plus the city name, 20 deep

Keyword set: house cleaning services, maid service, cleaning service, house cleaning near
me, apartment cleaning service, recurring house cleaning, airbnb cleaning service,
vacation rental cleaning, move out cleaning, deep cleaning service.

### The score

The brief asked for a score that does not simply reward large cities. A weighted sum of
six components cannot do that: a market with 80 monthly searches where MaidThis is
invisible will score highly on four of six components and rise to the top, which is
exactly wrong.

So the score is a **product of two halves**:

```
opportunity = potential x headroom

potential = demand x (0.60 + 0.25*commercial_value + 0.15*str_wedge)
headroom  = 0.40*competitive_headroom + 0.45*visibility_gap + 0.15*review_deficit
```

Inside potential, demand is a **multiplier rather than a weighted term**. CPC and
short-term-rental share are intensity ratios, not sizes. A market with 100 searches a
month and an expensive click is still a market with 100 searches a month. Making demand a
multiplier means near-zero demand drives the whole score to near zero, no matter how open
the market is.

Making the two halves a product also means a market that is already won scores low. That
is intended: LA Valley has the highest demand in the network and MaidThis ranks 2 on Maps,
so its opportunity score is modest. It is a market to defend, not a market to attack.

### Components

| Component | Definition | Why |
|---|---|---|
| `demand` | Log-scaled total monthly search volume, normalised across the network | Log scale so one metro cannot dominate purely on size |
| `commercial_value` | Volume-weighted CPC, normalised | Proxy for what a customer is worth locally |
| `str_wedge` | Airbnb and vacation-rental share of total demand, normalised | Where MaidThis is genuinely differentiated |
| `competitive_headroom` | Inverse of the median review count of the top 5 Maps competitors | Review equity is the hardest local asset to overtake |
| `visibility_gap` | 0 if MaidThis ranks in the Maps top 3, 0.45 for top 10, 0.75 for top 20, 1.0 if absent; plus 0.15 if absent from the organic top 20 | How far from where it should already be |
| `review_deficit` | MaidThis review count against the strongest profile in the pack | Distance to competitive review equity |

Each component is published per market in the CSV and in the dashboard detail panel, so
any weight can be argued with directly rather than taken on trust.

### Operating stage

Separate from the score, each market gets a stage from observed position:

- **LAUNCH**, no MaidThis profile found in the Maps top 20
- **GROW**, ranks in the top 10
- **DEFEND**, top 3 with 100 or more reviews
- **FIX**, in the top 20 but outside the top 10

Current split: 32 LAUNCH, 7 GROW, 6 DEFEND, 1 FIX.

### Headline results

| Metric | Value |
|---|---|
| Total tracked monthly demand | 48,960 |
| Median market demand | 505 |
| Largest market | LA Valley and Los Angeles, 5,330 |
| Median volume-weighted CPC | $13.79 |
| CPC range | $7.58 (Miami) to $35.38 |
| Median modelled cost per paid lead | $138 |
| Median STR share of demand | 4.0% |
| Maximum STR share | 20.0% |
| MaidThis visible in Maps pack | 14 of 46 |
| MaidThis in Maps top 3 | 8 of 46 |
| MaidThis in organic top 20 | 1 of 46 |

Top opportunity markets by score: Phoenix, Chicago, Atlanta, San Francisco, San Antonio,
Miami, Charlotte, Philadelphia, Tampa. All nine combine meaningful demand with no visible
Maps presence at the centroid.

### Known limitations, stated plainly

- **Single-centroid measurement.** A suburban territory scanned from a downtown centroid
  can be genuinely invisible in this test while trading well. Fishers IN, Flower Mound TX,
  King of Prussia PA, Spring Hill and Henry County GA are exactly that shape. A geo-grid
  scan would settle it and has not been run.
- **One head term for Maps.** Two keywords, not a full category sweep.
- **Desktop only.** Mobile packs differ, sometimes materially, for local intent.
- **Local search volumes are directionally useful, not precise.** Google Ads city-level
  volumes are bucketed and noisy at small volumes. Rank position and pack composition are
  far more reliable signals than the volume figures.
- **No demographic or short-term-rental supply overlay.** The US Census ACS API now
  requires a key, so population, household count, median income and tenure split were not
  collected. `pipeline/collect_demographics.py` is stubbed for this.
- **No cleaner-supply or capacity data.** Which, given that hiring is the stated
  bottleneck, is the most consequential gap in the whole dataset. It can only come from
  the client.

---

## Part 2: market size for the company

All MODEL class. Built bottom-up from stated assumptions, not purchased research.

### TAM

Assume roughly 3,000 US agencies serving 50 or more local clients, and roughly 3,500
franchise systems with 20 or more units. Take a median of about 90 units per organisation
and an addressable operating-layer value of $450 per unit per month.

That gives roughly $486,000 a year of addressable operating-layer spend per organisation,
across about 6,500 organisations, for a theoretical ceiling in the low billions. The
honest read: **the market is far larger than this company can ever serve, and the binding
constraint is delivery capacity, not demand.** Precision here would be false precision.

### SAM

Organisations of 40 to 300 units, English-speaking, search-led acquisition, with an
existing in-house or agency fulfilment cost high enough that $450 per unit is a saving.
Call it 10 to 15 percent of the TAM population, so roughly 700 to 1,000 organisations.

### Beachhead ICP

**US home-services and local-SEO agencies with 50 to 500 clients**, plus **franchise
systems of 20 to 300 units in home services, cleaning, restoration and wellness**.
Roughly 1,800 firms.

### Buyer profiles

| Segment | Unit | Why they buy | Trigger event | Fit |
|---|---|---|---|---|
| Local SEO and home-services agencies, 50 to 500 clients | Client account | Senior judgement does not scale with headcount, quiet accounts churn | A strategist quits, or a churn spike | Best |
| Franchise systems, 20 to 300 units | Territory | Fragmented vendor stack, no per-market view | Hiring a first or second marketing leader | Strong |
| Multi-location home services | Location | Acquisition cost varies by branch and nobody knows why | PE roll-up, or a new CFO | Strong |
| Dental and med spa groups | Practice | High CPC, high LTV, weak local search discipline | DSO acquisition or a new group marketing hire | Good |
| Legal networks | Market | Extreme CPC makes small efficiency gains large in dollars | New market entry | Good, crowded with incumbents |
| Other cleaning franchises | Territory | Same problem, same shape, case study already exists | Competitive pressure | Good, watch conflicts |

### Commercial parameters

| Parameter | Estimate | Basis |
|---|---|---|
| Average account value | $18,000 to $60,000 a year | 40 to 120 units at $450 |
| Sales cycle | 8 to 16 weeks | Involves finance and delivery leadership |
| Buyer role | Founder, COO, or VP of Marketing | Never a marketing manager: they lose scope |
| Trigger events | Senior departure, churn spike, roll-up, new marketing leader, vendor failure | |
| Pain signal | "I do not know what is happening on half our accounts" | |
| Competitive alternatives | Hire in-house, white-label agencies, offshore BPO, freelance networks, do nothing | |

The real competitor is **do nothing**, and after that **hire one more person**. The
open MaidThis Director of Marketing role is a live example of exactly that alternative
being chosen right now.

### On the 100-company lookalike list

Not built, deliberately.

Assembling 100 names from directory scraping would look like research and behave like
noise, and this study runs on a rule that nothing is presented as fact unless it was
verified. The method to build it properly:

1. DataForSEO Business Listings sweep by category (`cleaning_service`,
   `hvac_contractor`, `plumber`, `dental_clinic`, `medical_spa`) filtered to multi-location
   brands
2. Cross-reference against live state franchise registries for unit counts
3. Filter to 20 to 300 units and verify each brand's current marketing stack from its own
   site and job postings
4. Score by trigger-event evidence: open marketing roles, recent funding, recent
   acquisitions

**Business Listings bills per result, not per call**, and a single national sweep has
previously cost more than $30. It needs its own budget decision before it runs, which is
why it is specified here rather than executed.
