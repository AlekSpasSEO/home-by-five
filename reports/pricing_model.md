# Pricing model

MODEL class throughout. Inputs are FACT-class statutory rates and observed market costs.
Reproduce with `python pipeline/build_economics.py`. Live version in the Model tab of the
workbench.

---

## 1. What a person actually costs in North Macedonia

The single most misunderstood input in this business.

North Macedonia levies **28 percent social contributions on gross salary** (pension and
disability 18.8, health 7.5, employment 1.2, additional health 0.5) plus a **10 percent
flat personal income tax**, with a monthly personal allowance of MKD 10,270.

PwC states these contributions are withheld from the employee's gross salary, meaning
there is no separate employer-side percentage on top. Employer cost therefore equals gross
plus payroll administration.

```
contributions = 0.28 * gross
taxable       = gross - contributions - allowance
PIT           = 0.10 * taxable
net           = gross - contributions - PIT
=> gross      = (net - 0.1 * allowance) / 0.648
```

Sanity check: the national average net salary of MKD 45,961 implies a gross of MKD 69,342,
which matches published average gross salary. The formula holds.

**Conflict to resolve before signing anything.** Playroll states employer contributions
add about 16 to 18 percent on top of gross. PwC and Playroll cannot both be right. This
study follows PwC. If Playroll is correct, every breakeven below rises by roughly that
percentage and $450 stops working at 40 units. `EMPLOYER_ADDON` in
`pipeline/build_economics.py` switches between the two readings. **Get a written quote
from a Skopje payroll firm. It is a single phone call and it moves the whole model.**

## 2. Salary table

Target net pay is set at or above the top of the self-reported MojaPlata ranges, because
the product is senior output. FX captured 26 August 2026 at 1.167 EUR/USD and 61.497
EUR/MKD.

| Role | Net MKD/mo | Gross MKD/mo | Employer cost USD/mo | USD/yr |
|---|---|---|---|---|
| Growth / Product Director (owner) | 140,000 | 214,465 | $4,273 | $51,279 |
| Senior Search Strategist | 90,000 | 137,304 | $2,736 | $32,830 |
| Automation / Data Engineer | 85,000 | 129,588 | $2,582 | $30,985 |
| QA Lead | 70,000 | 106,440 | $2,121 | $25,449 |
| Paid Media Specialist | 65,000 | 98,724 | $1,967 | $23,604 |
| Local SEO Specialist | 60,000 | 91,008 | $1,813 | $21,759 |
| Growth / Data Analyst | 60,000 | 91,008 | $1,813 | $21,759 |
| Content Strategist | 50,000 | 75,576 | $1,506 | $18,069 |
| Account / Project Coordinator | 45,000 | 67,860 | $1,352 | $16,224 |
| Junior SEO Executive | 35,000 | 52,427 | $1,045 | $12,534 |
| VA / Operations Assistant | 32,000 | 47,798 | $952 | $11,428 |

Full table with EUR: `data/macedonia_salary_model.csv`.

**This is not cheap labour.** A senior strategist at $2,736 a month fully loaded is
roughly a third of a US equivalent, not a tenth. The pitch that survives contact with a
sophisticated buyer is a European cost base plus senior US-market judgement, not a rate
card.

## 3. Overheads

| Item | EUR/month | USD/month | Basis |
|---|---|---|---|
| Workspace per seat | 180 | $210 | Skopje private-office seat on a monthly contract |
| Equipment per seat | 33 | $39 | EUR 1,200 kit amortised over 36 months |
| Recruiting per hire | 33 | $39 | EUR 800 amortised over 24 months |
| Software base (company) | 700 | $817 | Rank and keyword data, AI, reporting, PM |
| Software per pod | 320 | $373 | Incremental seats and data volume |
| Accounting and payroll | 250 | $292 | |
| Connectivity and utilities | 150 | $175 | |

Plus **$1,500 per pod per month reserved for outside expert audits** and **10 percent
contingency** for turnover, sick cover and overrun. Both are real costs that most
back-of-envelope agency models omit, which is why most back-of-envelope agency models are
wrong.

## 4. Cost structure: two layers

This is where operating leverage comes from, and it is the reason the answer changes with
scale.

**Pod layer, scales linearly.** One delivery team per 40 accounts or territories.

| Tier | Composition per 40 units |
|---|---|
| MINIMAL | Senior strategist, junior, VA. Deliberately mirrors PMNow's own observed ratio |
| LEAN | Adds a local SEO specialist |
| STANDARD | Adds a growth and data analyst. This is what the brief's service list requires |
| PREMIUM | Adds half a content strategist and half a paid media specialist |

**Company layer, grows in steps.** Director at 1.0 FTE always. QA lead at 0.5 for one pod,
1.0 for two or three, 2.0 above. Automation engineer from pod two. Half a paid media
specialist from pod two. One coordinator per three pods.

At 40 units the company layer is roughly $5,300 a month against a $12,000 MRR at $300.
That single line is why small books do not work.

## 5. Breakeven price per unit per month

| Book size | MINIMAL | LEAN | STANDARD | PREMIUM |
|---|---|---|---|---|
| 40 | $399 | $457 | $515 | $571 |
| 80 | $396 | $454 | $512 | $568 |
| 120 | $333 | $391 | $448 | $504 |
| 150 | $337 | $395 | $453 | $508 |
| 200 | $304 | $362 | $420 | $475 |
| 300 | $277 | $335 | $393 | $448 |

The step at 80 to 120 is where the second pod's fixed additions get absorbed. The plateau
between 120 and 150 is the third pod arriving before its accounts do.

## 6. Gross margin at various prices

| Configuration | MRR | Cost | Margin |
|---|---|---|---|
| MINIMAL, 40 @ $300 | $12,000 | $15,971 | -33.1% |
| MINIMAL, 40 @ $450 | $18,000 | $15,971 | **+11.3%** |
| MINIMAL, 120 @ $450 | $54,000 | $39,930 | **+26.1%** |
| MINIMAL, 200 @ $300 | $60,000 | $60,817 | -1.4% |
| LEAN, 120 @ $450 | $54,000 | $46,864 | **+13.2%** |
| STANDARD, 40 @ $500 | $20,000 | $20,593 | -3.0% |
| STANDARD, 120 @ $500 | $60,000 | $53,798 | +10.3% |
| STANDARD, 200 @ $500 | $100,000 | $83,931 | +16.1% |
| Stripped MINIMAL, 40 @ $300 | $12,000 | $10,230 | +14.7% |

"Stripped" means no office, no funded expert budget, and the owner drawing $1,500 a month
instead of a director's salary. It is the only way $300 works at 40 units, and it is not a
company.

## 7. The recommendation

**Open at $450 per unit per month with a 40-unit minimum commitment, MINIMAL to LEAN
scope, with a written path to $550 to $600 as scope widens to STANDARD.**

Reasoning:

- $450 clears cost at the smallest book worth signing and reaches a real margin at 120.
- $450 is still far below what a US buyer carries internally per account, so the savings
  argument survives without heroics.
- Pricing at $300 and hoping to raise later does not work. Per-unit prices are almost
  never renegotiated upward inside a running contract, and the first number said out loud
  becomes the ceiling.

**Never send $300 in writing.** If it has already been floated verbally, the recovery line
is: that was my instinct before I had costed the delivery unit properly, and I would rather
give you a number I can honour for three years than one I have to renegotiate in six
months.

## 8. What would change these numbers

| Change | Effect on breakeven |
|---|---|
| Playroll employer-cost reading is correct | All figures rise roughly 16 to 18 percent |
| Remote-first, no office | Falls roughly 6 to 8 percent |
| Expert budget billed to client separately | Falls roughly 8 to 10 percent at 40 units |
| Owner on a $1,500 draw instead of full salary | Falls roughly 18 percent at 40 units, 6 percent at 120 |
| Pod size raised from 40 to 50 units | Falls roughly 15 percent, at real quality risk |
| MKD strengthens 10 percent against USD | Rises roughly 10 percent |

The last row deserves attention. Revenue is in dollars and costs are in denars, which are
pegged to the euro. A 10 percent EUR/USD move is a 10 percent margin move on a business
running at 26 percent. An annual indexation clause tied to a published wage index is not
optional.
