# MaidThis deep dive

Prepared 26 August 2026. Citations in `research/source_ledger.csv`. Market data in
`data/maidthis_market_opportunity.csv` and `data/maidthis_locations.csv`.

---

## 1. How many locations are there, actually

Six sources give six different answers, and the disagreement is informative rather than
sloppy.

| Source | Figure | As of | Evidence class | Why it differs |
|---|---|---|---|---|
| 2024 FDD, Item 20 | 1 franchised at start of 2022, 13 at end of 2023 | FY2023 | FACT | Item 20 always reports the prior fiscal year end, never today |
| FranchisePayback FDD summary | 15 total, 13 franchised, 2 company | "2025 FDD" | FACT, low confidence | Same 13/2 split as the 2024 FDD, so likely a stale copy |
| Lahav Media case study | 32 locations | Undated | FACT | Vendor's count of locations it works on, not the system total |
| GBG Marketing | 33 or more locations | Undated | FACT | Same caveat |
| Franchise Business Review | 38 units | 2026 | FACT | Franchisor-supplied, captured at some point in 2026 |
| Entrepreneur directory | 42 units | 2026 | FACT | Franchisor-supplied, captured later |
| Search index, this study | 46 distinct market URL segments | 26 Aug 2026 | FACT | A live page is not a live business |

**Working number: 38 to 46 awarded or launched territories, of which 14 are confirmed
trading by the presence of a live Google Business Profile in the Maps pack.**

Awarded is not launched. Launched is not trading. A location page is not a franchisee.
Anyone quoting a single number for this network is quoting a number they have not checked.

There is also an entity question worth resolving. MaidThis Franchising LLC is described as
a Nevada LLC formed 2 December 2019 that began offering franchises on 19 May 2023, while
Entrepreneur says franchising began in 2020 and FBR says 2021. That pattern usually
indicates a restructure of the franchisor entity. It matters because it determines which
FDD governs current franchisees.

## 2. What we measured, and what it shows

46 markets, ten keywords each, Google Ads volume and CPC, two Google Maps packs per
market and one organic SERP per market, all pulled on 26 August 2026 from the city
centroid on desktop.

| Metric | Value |
|---|---|
| Market URL segments tracked | 46 |
| MaidThis GBP visible in top 20 Maps, head term | 14 |
| Of those, in the top 3 | 8 |
| Not visible in the Maps pack at all | 32 |
| maidthis.com in organic top 20 for its own city term | 1 of 46 |
| Total tracked monthly search demand | 48,960 |
| Median market demand | 505 per month |
| Median volume-weighted CPC | $13.79 (range $7.58 to $35.38) |
| Median modelled cost per paid lead | $138 (MODEL, CPC at 10% click-to-lead) |
| Median MaidThis GBP reviews where visible | 134 |
| Median top-5 competitor review count | 85 |
| Median short-term-rental share of demand | 4.0% (max 20.0%) |

### The coverage finding

Thirty-two of forty-six market pages show no MaidThis profile in the top 20 Maps results
for the category head term. One of forty-six ranks organically in the top 20 for its own
city term.

**This must be presented as a question, not an accusation.** A single-centroid desktop
scan of one head term will legitimately miss a franchisee whose territory is a suburb 25
miles from downtown. Markets in this dataset such as Fishers IN, Flower Mound TX, King of
Prussia PA, Spring Hill and Henry County GA are exactly that shape. Fishers, scanned at
its own centroid, ranks number 1.

What the finding does establish is that an outsider spending $13 on public data can raise
32 specific questions about a 40-plus market network in an afternoon. Whether the answer
to each is "already known and fine" or "nobody has looked", the ability to ask is the
product.

### The short-term-rental finding

This one cuts against the company's own positioning, which is why it matters.

Airbnb and vacation-rental cleaning terms are a **median of 4 percent** of tracked local
search demand, reaching 20 percent in the strongest market. The STR wedge is genuine as
brand positioning and as a customer segment, and it is clearly a strong acquisition
channel through the platforms themselves. But it is not where local search volume lives.
An offer built primarily on STR search demand is built on a small base.

## 3. Unit economics, from the FDD

Where these figures come from the client's own reading of the 2024 FDD they are marked
accordingly. Two were independently corroborated in this study; the rest were not.

### Fees

| Item | Value | Source |
|---|---|---|
| Franchise fee | $39,000 (older summaries) rising to $42,500 (Entrepreneur, 2026) | FACT |
| Royalty | 6% of Gross Sales | FACT, consistent across sources |
| Brand / ad fund | 2% of Gross Sales, may rise to 3% | FACT |
| Initial investment | $49,550 to $67,650 rising to $68,300 to $79,900 | FACT |
| Local marketing requirement | Greater of $1,000/month or 5% of Gross Sales | USER-SUPPLIED FDD EXTRACT, **not verified** |
| Digital Marketing Package | $1,097 to $1,500/month (2024 reading), $750 to $1,500 (2026 reading) | USER-SUPPLIED FDD EXTRACT, **not verified** |
| Technology fee | Present, amount not confirmed | USER-SUPPLIED FDD EXTRACT |

**The Digital Marketing Package is the single most load-bearing unverified number in this
study.** No public FDD summary reachable in this run discloses it. Every marketing-pool
estimate downstream of it inherits that uncertainty. Buy the current FDD before quoting
any pool figure to anyone.

### Item 19 marketing intensity

From the client's reading of the 2024 FDD, five franchisees with full-year 2023 data:

| Franchisee | Revenue | Marketing | Marketing % |
|---|---|---|---|
| 1 | $464,508 | $43,459 | 9.4% |
| 2 | $219,945 | $17,869 | 8.1% |
| 3 | $139,090 | $32,434 | 23.3% |
| 4 | $106,999 | $11,151 | 10.4% |
| 5 | $92,200 | $13,350 | 14.5% |
| **Total** | **$1,022,742** | **$118,263** | **11.56%** |

Weighted marketing intensity 11.56 percent, median 10.4 percent. Against the corporate
and affiliate operation in the same year: $1,258,495 revenue on $65,777 marketing, or
**5.23 percent**.

The gap between 11.6 percent for young franchisees and 5.2 percent for the mature
operation is the most useful commercial idea in the whole MaidThis file. It reframes the
offer away from "more leads" and toward "compress the time a new territory spends at
launch-phase acquisition economics."

Two honest caveats. n=5 is a small cohort. And the mature 5.2 percent belongs to a
company-operated business in its founding market with a decade of brand equity, which no
new franchisee can replicate on any timetable.

### Franchisor financials

| Line | FY2023 | Jan to Oct 2024 |
|---|---|---|
| Total income | $319,449 | $614,242 |
| Royalty revenue | | $113,577 |
| Monthly Marketing Fee | | $149,398 |
| Technology fee | | $38,000 |
| Franchise fee income | | $284,228 |
| Independent contractors | | $46,091 |
| Consulting and coaching | | $59,882 |
| Marketing and advertising expense | | $238,869 |
| Payroll (wages) | | $64,215 |
| Net result | Loss of $109,354 | Profit of $41,509 |

FY2023 net loss above $109,000 and negative member's equity above $98,000 were
independently corroborated. The interim 2024 columns come from the client's reading and
are unaudited.

Two observations. **Franchise fee income was 46 percent of total income** in the 2024
interim period, which means this franchisor was still being funded primarily by selling
franchises rather than by royalties on operating ones. And the Monthly Marketing Fee line
of $149,398 over ten months, roughly $14,940 a month, is the closest thing to proof that a
centrally administered marketing pool exists.

## 4. Systemwide sales, modelled

There is no published systemwide sales figure. Any number is a MODEL.

The 2024 FDD sets minimum annual sales requirements of $50,000 in year 1, $125,000 in year
2, $250,000 in year 3, $375,000 in year 4 and $400,000 in year 5 onward (client-supplied,
unverified). With 38 to 46 territories of mixed maturity:

| Scenario | Active units | AUV | Systemwide sales |
|---|---|---|---|
| LOW | 34 | $180,000 | $6.1M |
| BASE | 40 | $260,000 | $10.4M |
| HIGH | 46 | $360,000 | $16.6M |

Cross-check: VettedBiz reports $139,090 yearly gross sales as an average, which is far
below the LOW AUV here and closer to a year-2 franchisee. FranchiseOverview reports "$1.1M
average revenue, sample of 2 units", which is almost certainly the corporate operation
rather than a franchisee benchmark. Neither should be quoted as a franchisee AUV.

Under BASE, royalty at 6 percent is roughly $624,000 a year and the brand fund at 2
percent is roughly $208,000. If the Digital Marketing Package is real and averages $1,100
across 40 units, the package pool is roughly $528,000 a year. **All three of those numbers
are MODEL, and the third is MODEL built on an unverified FACT.**

## 5. Vendor stack

Full detail in `data/maidthis_vendor_stack.csv`.

**Lahav Media**, SEO. Publishes a MaidThis case study referencing 32 locations, with
Chattanooga results of 33 page-one keywords, 34 organic leads and 0 to 368 organic visits
in 60 days, plus a claimed number 1 position on Google Maps.

Two things about this vendor matter more than the metrics.

First, **David Lahav is both the founder and CEO of Lahav Media and the owner of the
MaidThis Denver and Boulder territory**, described as the first MaidThis franchisee.
Crunchbase, a MaidThis Denver franchise testimonial video and a Lahav Media podcast
episode with Neel Parekh all point the same way. This is a related-party relationship.
Walking into a first meeting proposing to consolidate this vendor line would be an
unforced error of the first order.

Second, the Chattanooga Maps claim no longer holds for the head term. Measured on 26
August 2026, MaidThis Cleaning of Chattanooga ranks **3** for "house cleaning service"
with 4.9 stars and 142 reviews, behind Clean Concepts and Scenic City Cleaning Company,
with Molly Maid of Chattanooga at 4.6 and 276 reviews in position 5. Rank 3 is a good
result. It is not rank 1, and the case study is undated.

**GBG Marketing**, conversion and lifecycle. Claims deployment across 33 or more MaidThis
locations, a 39 percent conversion improvement, short-term-rental lead costs down 75
percent, a database generating $4,000 or more a month and a 10-touch SMS, email, voicemail
and human follow-up sequence. All vendor-published, therefore OWNED evidence.

A 10-touch speed-to-lead system is genuinely hard to rebuild and is the highest-leverage
asset in the stack. Keep it. What needs auditing is whether the 39 percent is measured
against a clean baseline and whether the gain persists past the launch window.

**The Vendor Hub.** The open job posting explicitly lists managing "our marketing vendor
relationships and Vendor Hub" as a duty, which implies more suppliers than the two that
publish case studies. This is the largest single blind spot in the MaidThis file and the
first thing any engagement must resolve.

## 6. Sentiment

Tagged OWNED where the company controls the collection channel, INDEPENDENT otherwise.

**Customers (INDEPENDENT aggregation, OWNED collection).** Trustindex aggregates 387
reviews at 4.7: 343 five-star, 20 four-star, 3 three-star, 11 two-star, 10 one-star. The
distribution is healthy. The recent negatives are consistent and operationally specific:
surface-level cleaning against a deep-clean booking, items in scope not touched, quoted
price against charged price, and cleaners arriving off-schedule or with unannounced extra
people. One reviewer alleges review solicitation tied to cleaner bonuses, which is a
single unverified claim but worth knowing about.

Selection-bias warning: Trustindex aggregates whatever a business connects, so this is not
a random sample.

**Franchisees (thin).** Franchise Business Review's own page states no satisfaction data
is available. ZeeScores carries three anonymous franchisee reviews at 100 out of 100. The
2025 and 2026 Top Culture awards and the 2026 Top 200 listing are recognitions, not
satisfaction datasets. **n=3 anonymous is not evidence of franchisee satisfaction.** It is
the absence of a public complaint cluster, which is meaningfully different and much weaker.

**Former franchisees.** One ZeeScores reviewer describes selling a San Antonio franchise
and still praising the support model. No terminations or transfers could be independently
verified without the current FDD Item 20.

**Cleaners and employees.** No usable public dataset found. Given that hiring is the
stated bottleneck, this is a real gap.

## 7. The bottleneck that reframes everything

The founder has said publicly that surveying 40 or more franchise owners about what was
holding them back produced one answer, and it was not leads. It was hiring cleaners, and
he is building an AI recruiting system to address it.

An offer that promises more leads answers a question nobody asked. Worse, it actively
damages the business: the customer-review negatives above are exactly what happens when
acquisition outruns fulfilment capacity. Every incomplete clean and every scheduling
failure in that review set is a capacity story, not a marketing story.

The correct offer is **capacity-aware growth**: acquisition that is throttled per market
by what that market can actually fulfil, with the recruitment funnel instrumented rather
than owned. Do not compete with the founder's own build. Measure it and feed it.
