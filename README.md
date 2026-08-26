# Home By Five

Feasibility study, operating model and live workbench for a North Macedonia based growth
and search operations company serving US multi-location businesses, franchise systems and
agencies on a per-unit basis.

Anchor candidates: **MaidThis Franchise** and **Proven Marketing Now (PMNow)**.

Built 26 August 2026.

---

## The two apps

| | |
|---|---|
| **Workbench** | [`/`](https://alekspasseo.github.io/home-by-five/) &nbsp; The whole project in one place: verdict, live economics model with sliders, anchor analysis, offers, guarantees, risk register, market sizing, searchable evidence ledger, and the build plan |
| **Dashboard** | [`/dashboard/`](https://alekspasseo.github.io/home-by-five/dashboard/) &nbsp; Network performance for MaidThis and all 46 of its markets, from public sources only |

Both are static, self-contained and `noindex`. Nothing here depends on any client's
internal analytics, which is the point.

## The headline finding

**$300 per account or location per month does not work.** At the service level the brief
describes, modelled delivery cost is $420 to $571 per unit per month at a 40-unit book.
The only configuration where $300 clears cost is a three-person pod with no office, no
funded expert budget and the owner drawing $1,500 a month, above roughly 200 accounts.

**$450 works**, returning 11 percent gross margin at 40 units and 26 percent at 120, and
it is still far below what a US buyer already carries internally per account.

Full reasoning: [`EXECUTIVE_BRIEF.md`](EXECUTIVE_BRIEF.md).

## Repository layout

```
index.html               Workbench app
dashboard/index.html     Network performance dashboard
app/                     Styles, renderers, generated JSON bundles
data/                    Analysis datasets, CSV
research/                Source ledger, every externally sourced claim
reports/                 Long-form analysis
pipeline/                Python collectors and model builders
raw/                     Raw API responses and the DataForSEO cost log
EXECUTIVE_BRIEF.md       Decision-grade summary, fifteen questions answered
```

## Datasets

| File | Contents |
|---|---|
| `research/source_ledger.csv` | 37 externally sourced claims with evidence class, confidence, URL, date and an explanation of why sources conflict |
| `data/maidthis_locations.csv` | 46 markets with owner attribution where known, operating status confirmed by live GBP presence |
| `data/maidthis_market_opportunity.csv` | Search demand, CPC, Maps position, pack composition and opportunity score per market |
| `data/maidthis_vendor_stack.csv` | Every publicly identifiable vendor with a keep-or-replace recommendation and reasoning |
| `data/pmnow_economics.csv` | What is verifiable about PMNow and what is not |
| `data/macedonia_salary_model.csv` | Eleven roles, net to gross to fully loaded employer cost in MKD, EUR and USD |
| `data/unit_economics.csv` | 96 scenarios across four service tiers, four book sizes and six price points |

## Evidence classes

Never blended, anywhere in this repository.

- **FACT** &mdash; direct primary evidence: FDD, company site, job posting, founder
  statement, measured API response
- **STRONG INFERENCE** &mdash; several independent signals agreeing
- **MODEL** &mdash; our own calculation from explicitly stated assumptions

Claims taken from the client's own reading of the 2024 MaidThis FDD are tagged
`USER-SUPPLIED FDD EXTRACT` and carry Medium confidence unless corroborated independently.
Two were. The Digital Marketing Package line was not, and that gap is flagged everywhere it
matters.

## Reproducing the research

```bash
python pipeline/collect_markets.py      # resumable, hard budget cap in pipeline/dfs.py
python pipeline/build_datasets.py       # market opportunity + dashboard bundle
python pipeline/build_locations.py      # master location database
python pipeline/build_economics.py      # salary model + unit economics
python pipeline/build_evidence.py       # source ledger, vendor stack, PMNow
python pipeline/dfs.py                  # print spend against the cap
```

`pipeline/dfs.py` reads DataForSEO credentials from the HQDM secrets file, logs every call
to `raw/dfs_cost_log.jsonl` and to the shared HQDM cost log, and refuses to call the API
once $18 is reached.

**Research cost: $13.43** against $20 authorised, covering 46 markets with Google Ads
search volume, two Google Maps packs and one organic SERP each.

## Known gaps

Listed in full in `EXECUTIVE_BRIEF.md`. The four that matter most:

1. **The current MaidThis FDD has not been purchased.** The Digital Marketing Package and
   local marketing requirement figures are unverified, and every marketing-pool number
   downstream inherits that.
2. **Employer-cost conflict is unresolved.** PwC and Playroll disagree by 16 to 18 percent
   on North Macedonian employer cost. One phone call to a Skopje payroll firm settles it,
   and it moves every breakeven in the model.
3. **Maps measurement is single-centroid.** Suburban territories can be invisible at a
   downtown centroid while trading well. A geo-grid scan would settle it.
4. **No PMNow-internal number exists in this study.** Client count, ARPA, tenure, churn and
   consultant spend all have to come from the buyer.

---

Internal working document. Contains competitive analysis of two companies the author is in
commercial conversation with. Not for distribution.
