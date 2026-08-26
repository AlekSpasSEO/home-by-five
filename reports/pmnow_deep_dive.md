# PMNow deep dive

Prepared 26 August 2026. Citations in `research/source_ledger.csv`. Data in
`data/pmnow_economics.csv`.

---

## 1. What is verifiable

Proven Marketing Now LLC, 121 Newark Avenue Suite 591, Jersey City NJ 07302. Founded by
Eric and Michael. Serves HVAC, plumbing and electrical home-service contractors with
Google Maps optimisation, website SEO, Google Local Service Ads and Google Ads. Remote
team with front-office staff in North America and Europe. No long-term contracts, 30 days'
cancellation notice. Google Partner certified. Claims 500 or more contractors served,
which is a cumulative marketing claim, not an active client count.

Client sentiment: 4.8 out of 5 from 102 Birdeye reviews. Reviews collected through a
reputation tool the agency controls, so positively selected by construction. What is more
informative is what was not found: no independent negative cluster anywhere. No scam
thread, no ex-client pile-on, no complaint pattern in public communities.

**The product is not broken.** That single fact should reshape the entire approach. The
pitch is not "I will fix your agency". It is "I will protect the quality of the product
while lowering the cost of scaling it."

## 2. What is not verifiable, and the trap in it

Every third-party revenue and headcount estimate is a scraped guess about a private LLC
with no filings.

| Source | Employees | Revenue |
|---|---|---|
| ZoomInfo | 51 to 200 | Under $5M |
| Crunchbase | 51 to 100 | not stated |
| Prospeo | 11 to 20 | ~$1.63M quoted elsewhere |
| Clodura | 11 to 50 | not stated |

That is a tenfold spread on headcount. **None of these should be repeated as fact,
including the $1.63M figure.** Quoting a scraped estimate back to a founder who knows the
real number is the fastest way to lose credibility in a first meeting.

## 3. What can be modelled honestly

If active clients are "well over 100" as management states (STRONG INFERENCE, relayed, not
published):

| Average monthly account value | 100 clients | 130 clients |
|---|---|---|
| $1,250 | $1.50M ARR | $1.95M ARR |
| $1,500 | $1.80M ARR | $2.34M ARR |
| $2,000 | $2.40M ARR | $3.12M ARR |
| $2,500 | $3.00M ARR | $3.90M ARR |

Bracketed by published home-services retainer ranges of $1,000 to $3,500 a month for SEO
alone and $2,500 to $12,000 for full service including Google Ads and LSA management.
PMNow sells the fuller stack, so the middle to upper rows are more plausible. The point
estimate is unknowable from outside and should stay that way in conversation.

## 4. The delivery ratio, which is the whole deal

One strategist owns 35 to 45 accounts, supported by juniors and VAs (STRONG INFERENCE,
management statement). This is the single most important number in the file, because it
defines the unit and validates the pod shape.

Modelled against North Macedonian cost (MODEL, `data/unit_economics.csv`), a MINIMAL pod of
one senior strategist, one junior and one VA per 40 accounts costs **$399 per account per
month** at 40 accounts, falling to $333 at 120 and $304 at 200. Add a local SEO specialist
and an analyst, which is what the brief's service list actually describes, and it becomes
$515 at 40 and $448 at 120.

If PMNow's own fully loaded cost per account is above roughly $500, the savings argument
is strong. If it is below $400, there is no savings argument at all and the offer has to
survive on coverage and QA alone. **That number has to come from the buyer, and asking for
it is the first move.**

## 5. The actual problem being sold into

Management's stated concern is maintaining quality on quiet accounts, the ones nobody is
watching. Combined with month-to-month terms and 30 days' notice, this is not a soft
worry. It is the dominant commercial risk in the business:

- A month-to-month client who goes quiet is not renewing a decision, they are declining to
  cancel.
- On a book of 100-plus accounts with roughly three strategists, attention is rationed by
  whoever emails loudest.
- The accounts that churn are almost never the loud ones.

This is a coverage problem, and coverage is exactly what a pod with a QA layer sells.

## 6. The Hennessey method, and the version worth building

Jason Hennessey describes bringing in world-class outside specialists to audit a single
client site, testing what they find, then applying what works across the whole client
base. He calls the practice outsourcing genius. Hennessey Digital grew from a small
consultancy to a $10M-plus business with 100-plus staff on the back of it.

The specific budget figures in circulation, five to ten thousand a month and roughly five
thousand per audit, could not be verified in this study. **Do not repeat them as fact.**
The method is safe to reference; the amounts are not.

The upgrade worth proposing is not a cheaper expert. It is a system that stops the same
lesson being bought twice:

```
EXPERT ENGAGEMENT
  recording, transcript, artefacts, raw audit output
      |
HYPOTHESIS EXTRACTION
  each recommendation restated as a testable claim with a predicted metric
      |
TEST COHORT
  applied to a matched sample of accounts, with a holdout
      |
MEASUREMENT
  did the predicted metric move, on what timescale, under what conditions
      |
SOP
  what worked becomes a written procedure a junior can execute
      |
AUTOMATION AND QA RULE
  the SOP becomes a checklist item and, where possible, a scripted check
      |
PORTFOLIO ROLLOUT
  applied across the book, monitored, with stated conditions where it does not apply
      |
KNOWLEDGE BASE
  the next expert starts by reading what the previous five recommended,
  what was tested, what worked, and under which conditions it failed
```

The commercial argument to a founder who already believes in expert consulting is not
"spend less on experts". It is "the fourth expert you hire should cost you less to absorb
than the first one did, and right now it costs exactly the same."

Two things this system must not do. It must not position us as a replacement for the
experts, because the expert bench is part of the founder's identity and product. And it
must not promise that every audit yields a portfolio-wide win, because most do not. The
value is in knowing which ones did, and never re-testing the ones that did not.

## 7. Why PMNow is the better first anchor

| | MaidThis | PMNow |
|---|---|---|
| Unit already defined | Roughly | Yes, a client account |
| Delivery ratio known | No | Yes, 35 to 45 per strategist |
| Buyer names the problem themselves | Their stated pain is cleaner hiring | Yes, quality on quiet accounts |
| Decision makers | Franchisor plus 40-plus franchisees | One |
| Repeatability across units | 46 heterogeneous territories | 40 similar contractor accounts |
| Churn mechanic | Franchisee dissatisfaction, slow | 30-day notice, fast |
| Case-study value to us | Very high | Moderate |

PMNow is the better first customer because the work is repeatable and the buyer is one
person who has already articulated the pain. MaidThis is the better second customer and a
far better case study.

## 8. The four numbers to get from management

Nothing in this file substitutes for these, and all four are single questions:

1. **Fully loaded fulfilment cost per account per month.** Determines whether a savings
   argument exists at all.
2. **Average client monthly retainer.** Determines what fraction of their revenue our fee
   represents, and therefore how much resistance the price will meet.
3. **Average client tenure and monthly churn.** Determines what a coverage guarantee is
   actually worth to them in dollars.
4. **Annual outside consultant and vendor spend.** Determines whether the expert-capture
   system is a headline feature or a footnote.

## 9. Risks specific to this anchor

- **Concentration.** One pod for PMNow is 100 percent of revenue at the start. A 30-day
  cancellation clause on their side becomes a 30-day cancellation clause on the whole
  company. Do not build past two pods for them without a second anchor signed.
- **Their cost may already be low.** Covered above. Ask first, price second.
- **Quality attribution.** If results are ultimately judged on client call volume, a pod
  can execute perfectly and still be blamed for a market downturn or a media budget cut.
  Phrase the guarantee in coverage and QA terms, never in call terms, until attribution is
  jointly agreed in writing.
- **Their team may resist.** An external pod taking 40 accounts is a threat to whoever
  currently owns them internally. Ask early who loses scope, and plan for that
  conversation rather than discovering it in month two.
