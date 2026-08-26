# Risk register and guarantee design

---

## Part 1: risk register

Ranked by how much of the model each one destroys.

### R1. The $300 anchor becomes the ceiling
**Class** Commercial &middot; **Impact** Fatal to margin &middot; **Likelihood** High if
$300 has already been said aloud

Per-unit prices are almost never renegotiated upward inside a running contract. The first
number said out loud tends to become the number.

*Confirmation signal:* the buyer repeats $300 back as the expected price.
*Mitigation:* never put $300 in writing. Lead with the cost baseline and price after it
exists. If it has already been floated verbally, the recovery line is that it was an
instinct before the delivery unit was properly costed.

### R2. North Macedonian employer cost is 16 to 18 percent above gross
**Class** Cost model &middot; **Impact** Every breakeven rises by roughly that amount

PwC states contributions are withheld from the employee's gross, so employer cost equals
gross. Playroll states employers add 16 to 18 percent on top. They cannot both be right,
and this study follows PwC.

If Playroll is right, MINIMAL at 40 units breaks even nearer $465 than $399 and $450 stops
working at the smallest book worth signing.

*Confirmation signal:* a payroll firm's written quote.
*Mitigation:* obtain that quote before signing anything. `EMPLOYER_ADDON` in
`pipeline/build_economics.py` switches the model between the two readings in one line.

### R3. The measured coverage gap is a scanning artefact
**Class** Evidence &middot; **Impact** Removes the strongest quality argument

Every Maps position in this study is a single city-centroid desktop measurement of one head
term. Suburban territories can be genuinely invisible in that test while trading well.

*Confirmation signal:* a geo-grid scan of three suspect suburban territories finds MaidThis
ranking well off-centroid.
*Mitigation:* re-measure before presenting. Present as a question either way. The framing
"here are 32 markets where I cannot see you from the outside, which ones do you already
know about" is safe under both outcomes.

### R4. Anchors will not separate media and hard costs from the fee
**Class** Commercial &middot; **Impact** Price becomes meaningless, margin unknowable

*Confirmation signal:* the buyer asks for an all-in number including ad spend.
*Mitigation:* decline that structure. It is the one line that cannot bend.

### R5. Franchisee cooperation: 46 owners, not one buyer
**Class** Delivery &middot; **Impact** Silent cost overrun no model captures

Forty-six territories with forty-six owners is forty-six relationships. Franchisee
cooperation is outside our control and outside the franchisor's control too.

*Confirmation signal:* more than two hours a month per territory going to owner
coordination.
*Mitigation:* contract with the franchisor for corporate-layer work. Price owner-level
coordination separately or exclude it explicitly.

### R6. Cleaner capacity, not leads, is the real MaidThis constraint
**Class** Product fit &middot; **Impact** The offer answers the wrong question

Already confirmed by the founder's own public statement. Marketing that outruns fulfilment
capacity produces exactly the incomplete-clean and scheduling complaints visible in the
current review set.

*Mitigation:* lead with capacity-aware growth. Instrument the recruitment funnel, do not
compete with the founder's own AI recruiting build.

### R7. Key-person concentration on the owner
**Class** Operational &middot; **Impact** Caps growth at roughly two pods

*Confirmation signal:* the owner is still doing senior delivery above $30k MRR.
*Mitigation:* hire the second senior strategist at pod two, not pod three, and price the
service so it funds that hire before it is needed.

### R8. Single-client concentration
**Class** Commercial &middot; **Impact** One cancellation clause ends the company

PMNow operates on 30 days' notice. A pod built entirely for them inherits that notice
period as the company's own survival horizon.

*Confirmation signal:* one anchor exceeds 60 percent of MRR.
*Mitigation:* do not build past two pods for one client without a second anchor signed.

### R9. The anchor's real cost per account is already below $400
**Class** Commercial &middot; **Impact** Removes the savings argument entirely

*Confirmation signal:* they share the number and it starts with a 2 or a 3.
*Mitigation:* then sell coverage and QA rather than savings, and let the guarantee tier
carry the offer. This is survivable but it changes the whole conversation, which is why the
number has to be asked for first.

### R10. Vendor incumbency is a related party
**Class** Relationship &middot; **Impact** A consolidation pitch reads as an attack on a
franchisee

Already established: David Lahav founded Lahav Media and owns the Denver and Boulder
territory.

*Mitigation:* scorecard, never propose replacement. Let measurement lead the conversation.

### R11. Client-supplied FDD figures carry through the model unverified
**Class** Evidence &middot; **Impact** The marketing-pool sizing collapses if the Digital
Marketing Package line is wrong

Two headline figures from the client's FDD reading were independently corroborated. The
Digital Marketing Package line was not, and no public FDD summary reachable in this study
discloses it.

*Mitigation:* buy the current FDD before quoting any pool figure to anyone. Cheapest risk
reduction available.

### R12. Currency and wage inflation
**Class** Cost model &middot; **Impact** A few margin points a year

Revenue is in dollars, costs are in denars pegged to the euro. A 10 percent EUR/USD move is
a 10 percent margin move on a business running at 26 percent.

*Mitigation:* annual indexation clause tied to a published wage index, not to CPI.

---

## Part 2: guarantee design

**No ranking guarantees. No revenue guarantees.** Everything below is measured on inputs
inside our control, with the downside to us stated.

### Low risk

| Commitment | Measure | Remedy | Downside to us |
|---|---|---|---|
| Every unit receives a documented human review at least every 14 days | Timestamped review log, audited monthly | 5% fee credit per missed unit-month | Small. Fully in our control. Costs roughly 0.5 to 1 hour per unit per month, already in the pod model |
| Monthly reporting delivered by the fifth working day | Delivery timestamp | 2% fee credit per late month | Small, but forces month-end data discipline from day one |

### Balanced

| Commitment | Measure | Remedy | Downside to us |
|---|---|---|---|
| Approved work items shipped within 10 working days | Ticket open-to-close time | 10% fee credit below 90% adherence in a month | Moderate. Exposed to client-side approval delay, so the clock must stop while waiting on the client and that must be written into the contract |
| 95% of delivered items pass the published QA checklist first time | QA log with sampled independent re-check | 10% fee credit below threshold | Moderate. Requires a real QA layer, which is why a MINIMAL pod cannot honestly sell this tier |
| Complete invoice-level fully loaded cost per unit delivered within 60 days | The document itself | Full refund of the first 60 days | Low if the client shares invoices, total if they do not. Make client cooperation an explicit precondition |

### Aggressive

| Commitment | Measure | Remedy | Downside to us |
|---|---|---|---|
| An identified and agreed path to 15% reduction in controllable fulfilment cost per unit, without reducing agreed service levels | Agreed baseline against month-6 actuals | Fee reduced to cost until the target is met | High. Only offer after the baseline exists. **Never** offer before seeing invoices |
| Cost per qualified lead, where clean attribution exists | Client call tracking or CRM, agreed source definitions | Fee credit on a sliding scale | Very high. Gated by media budget, market conditions and, for MaidThis, cleaner capacity. Recommend against in year one |

### The sentence never to say in a first meeting

> "I will reduce your vendor costs."

You have not seen an invoice. The moment it is said it becomes a term of the deal, and
every later finding gets measured against a promise made blind.

Say instead:

> "Once the cost baseline exists, I am willing to tie part of my compensation to reducing
> controllable fulfilment cost per unit without reducing agreed service levels. Give me
> the first 30 days to establish what each unit actually costs you to service, and I will
> show you what can be consolidated, what should stay external, and what the target cost
> per unit should be."
