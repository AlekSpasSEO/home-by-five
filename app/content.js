/* Home By Five, workbench content.
   Every claim carries an evidence class. Full citations live in
   research/source_ledger.csv and the Evidence tab renders that file directly. */
window.HB5 = {

verdict: {
  title: "Verdict",
  lede: "The business is viable. The price is not. Those are two separate findings and " +
        "collapsing them is the fastest way to build a company that cannot pay its own people.",
  blocks: [
    { t: "callout", cls: "bad", h: "$300 per account or location per month does not work",
      p: ["At the service level described in the brief, senior strategy plus market analysis " +
          "plus SEO plus paid oversight plus analytics plus CRO plus funnel analysis plus " +
          "reporting plus AI plus QA plus junior execution plus vendor management plus SOPs " +
          "plus expert capture plus hiring, the modelled delivery cost is $420 to $571 per " +
          "account per month at a 40-unit book. $300 is 30 to 47 percent below cost.",
          "The only configuration where $300 clears cost is a three-person pod per 40 accounts " +
          "with no office, no expert budget and the owner drawing $1,500 a month. That reaches " +
          "roughly 15 percent gross margin at 40 accounts and 20 percent at 120. That is not a " +
          "company, it is a job carrying a company's risk."] },
    { t: "callout", cls: "good", h: "$450 is the number to open with, and it still saves the buyer money",
      p: ["At $450 per unit on a MINIMAL pod, a 40-unit book returns 11 percent gross margin " +
          "and a 120-unit book returns 26 percent. At $500 on a LEAN pod, 120 units returns " +
          "about 20 percent. Getting a STANDARD pod to a healthy 35 percent needs roughly $690 " +
          "per unit, which is why scope discipline matters more than price negotiation.",
          "$450 is still well below what a US agency spends internally per account. Published " +
          "home-services retainers run $1,000 to $3,500 a month for SEO alone, so a buyer " +
          "running 50 percent gross margin is already carrying $500 to $1,750 of internal cost " +
          "per account. The saving argument survives at $450. It does not need $300."] },
    { t: "stats", items: [
      ["Breakeven, MINIMAL @ 40", "$399", "warn", "3 FTE per 40, PMNow's own observed ratio"],
      ["Breakeven, MINIMAL @ 120", "$333", "warn", "Scale helps, but not by 45 percent"],
      ["Breakeven, STANDARD @ 40", "$515", "bad", "The tier the brief actually describes"],
      ["Breakeven, MINIMAL @ 300", "$277", "good", "The only place $300 has real room"] ] },
    { t: "h", v: "The fifteen questions" },
    { t: "qa", items: [
      ["Is this business viable?",
       "Yes, as a priced operating layer. No, as labour arbitrage. The cost base is real: a " +
       "senior search strategist in Skopje costs about $2,736 a month fully loaded, not $800. " +
       "The margin has to come from the operating system and the ratio of accounts to senior " +
       "judgement, not from cheap people."],
      ["Is $300 viable?",
       "No, not at the described scope. It is roughly break-even only at a stripped three-person " +
       "pod above 200 accounts, and only with the owner on a reduced draw, no office and the " +
       "expert budget billed separately. Anything with an analyst, a real QA layer or a funded " +
       "expert budget needs $450 or more."],
      ["At what minimum scale?",
       "120 accounts is the first point where the shared company layer stops dominating. Below " +
       "80 accounts the director's own salary is 30 to 40 percent of revenue. A single 40-unit " +
       "pilot is a proof of concept, not a business."],
      ["What gross margin is realistic?",
       "25 to 30 percent at $450 per account on a MINIMAL pod above 120 accounts. Reaching 35 " +
       "percent on a STANDARD pod needs roughly $690 per unit. Anyone promising 60 percent has " +
       "either not costed a real QA layer or is planning to under-deliver."],
      ["What must be excluded from the price?",
       "Media spend. Premium link and PR placements. External expert consultant fees. Custom " +
       "software builds. Unusual third-party data costs. Call tracking and CRM licences. These " +
       "stay client-paid and transparent, and we manage them without marking them up."],
      ["Strongest savings argument?",
       "Not headcount cost. It is that MaidThis is about to hire one person at $5,000 to $7,000 " +
       "a month whose job description is to sit between vendors, 46 market pages and a network " +
       "of franchisees, and that person still needs a team and a system underneath them. We " +
       "supply the person, the system and the team for the price of the person plus a pod."],
      ["Strongest quality argument?",
       "Coverage. 32 of 46 MaidThis market pages currently show no Google Business Profile in " +
       "the top 20 Maps results for the head term, and 45 of 46 do not rank in the organic top " +
       "20 for their own city term. Whatever the explanation, nobody is watching every market " +
       "every week. That is exactly PMNow's stated fear about quiet accounts, in a different " +
       "vertical."],
      ["What should we guarantee?",
       "Things we control: coverage cadence, SLA adherence, QA pass rate, implementation " +
       "turnaround, reporting latency, and a documented cost baseline in the first 60 days. " +
       "See the Guarantees tab."],
      ["What should we absolutely not guarantee?",
       "Rankings. Revenue. Lead volume. Vendor cost reduction before seeing a single invoice. " +
       "Any outcome gated by cleaner capacity or franchisee execution."],
      ["What makes MaidThis say yes?",
       "A market-by-market picture they do not have, delivered before they are asked to pay for " +
       "it, plus an offer that is cheaper than hiring the Director of Marketing and building the " +
       "team behind them separately."],
      ["What makes PMNow say yes?",
       "One pod, 40 accounts, a fixed cost per account, and a written commitment that no account " +
       "goes more than N days without a human review. Their problem is quiet accounts, and that " +
       "is a coverage guarantee, not a ranking guarantee."],
      ["Which is the better first anchor?",
       "PMNow. The unit is already defined, the ratio is already known, the buyer already " +
       "believes in the problem, and the work is repeatable across 40 near-identical accounts. " +
       "MaidThis is the better second client and the better case study."],
      ["What should the 90-day pilot look like?",
       "See the Build tab. Days 1 to 30 establish the cost and coverage baseline. Days 31 to 60 " +
       "prove the coverage guarantee on a live cohort. Days 61 to 90 hand back a working " +
       "scorecard and a signed cost-per-account target."],
      ["How does it scale from $10k to $100k MRR?",
       "$10k is one pod and the owner doing senior work. $30k is two pods plus an automation " +
       "engineer. $50k is three pods plus a QA lead and a coordinator. $100k is a second anchor " +
       "vertical and the owner out of delivery entirely. See the Model tab."],
      ["What evidence would disprove the model?",
       "Four things. One: the anchors' real fully loaded cost per account turns out to be below " +
       "$400, which removes the savings argument. Two: North Macedonian employer cost is 16 to " +
       "18 percent above gross rather than equal to it, which moves every breakeven up. Three: " +
       "the coverage gap measured here is an artefact of city-centroid scanning rather than a " +
       "real gap. Four: neither anchor will separate media and hard costs from the fee, which " +
       "makes the price meaningless."] ] }
  ]
},

anchors: {
  title: "Anchors",
  lede: "Two companies, one structural problem: both are growing faster than they can cover " +
        "their units with senior attention, and both are paying for that in a currency they " +
        "cannot see.",
  blocks: [
    { t: "h", v: "MaidThis" },
    { t: "stats", items: [
      ["Market pages found", "46", "", "URL segments on maidthis.com, via the search index"],
      ["GBP visible in Maps pack", "14", "warn", "For house cleaning service, at the city centroid"],
      ["Not visible in pack", "32", "bad", "Page exists, no MaidThis profile in the top 20"],
      ["Organic top 20", "1 of 46", "bad", "For house cleaning services + own city name"],
      ["Network search demand", "48,960/mo", "", "Ten tracked keywords across all 46 markets"],
      ["Median market demand", "505/mo", "", "Half the markets are smaller than this"],
      ["Median weighted CPC", "$13.79", "", "Range $7.58 to $35.38"],
      ["Median modelled CPL", "$138", "warn", "MODEL: CPC at an assumed 10% click-to-lead rate"] ] },
    { t: "p", v: "The three unit counts in circulation do not agree, and the reason matters. " +
      "The 2024 FDD reports 13 franchised outlets at the end of fiscal 2023, because Item 20 " +
      "always describes the prior fiscal year end. Franchise Business Review currently publishes " +
      "38 and Entrepreneur publishes 42, both franchisor-supplied and captured on different " +
      "dates. GBG Marketing's case study references 33 or more locations and Lahav Media's " +
      "references 32. The search index shows 46 distinct market URL segments. Awarded is not " +
      "launched, launched is not trading, and a live page is not a live business." },
    { t: "callout", cls: "warn", h: "The finding that changes the pitch",
      p: ["Only 14 of the 46 market pages surface a MaidThis Google Business Profile in the top " +
          "20 Maps results for the head term, and only 8 sit in the top 3. Only one market page " +
          "reaches the organic top 20 for its own city term.",
          "This scan is a single point in time from a city centroid on desktop, using one head " +
          "term. A suburban territory measured from a downtown centroid can be genuinely " +
          "invisible in this test while trading well. So the correct framing is not 'your SEO is " +
          "broken'. It is 'here are 32 markets where I cannot see you from the outside, and I " +
          "would like to know which ones you already know about'."] },
    { t: "callout", cls: "bad", h: "Disconfirming evidence against the short-term-rental thesis",
      p: ["Airbnb and vacation-rental cleaning terms are a median of 4 percent of tracked local " +
          "search demand across the network, and 20 percent at the very best. The STR wedge is " +
          "real as positioning and as a customer segment, but it is not where the local search " +
          "volume is. Any offer built primarily on STR search demand is built on a small base."] },
    { t: "p", v: "MaidThis is currently hiring a Director of Marketing at $5,000 to $7,000 a " +
      "month whose posted duties are managing the Vendor Hub, monitoring paid budgets across " +
      "franchisee markets, directing SEO vendors, building per-market KPI dashboards, refreshing " +
      "the marketing package quarterly and deploying AI for conversion. That job description is " +
      "the clearest public statement of the problem, and it is a job that needs a team " +
      "underneath it." },
    { t: "callout", cls: "warn", h: "Do not walk in proposing to replace the SEO vendor",
      p: ["David Lahav is the founder and CEO of Lahav Media and also owns the MaidThis " +
          "Denver and Boulder territory, and is described as the first MaidThis franchisee. " +
          "Three independent signals agree on this. Proposing to consolidate that vendor line " +
          "in a first meeting would be an unforced error. Scorecard the delivery, let the " +
          "measurement lead the conversation."] },
    { t: "callout", cls: "warn", h: "Marketing is not their stated bottleneck",
      p: ["The founder has said publicly that surveying 40 or more franchise owners produced a " +
          "single answer, and it was hiring cleaners, not leads. An offer that promises more " +
          "leads is answering a question nobody asked. The offer has to be capacity-aware " +
          "growth: acquisition that respects what each market can actually fulfil."] },

    { t: "h", v: "PMNow" },
    { t: "p", v: "Proven Marketing Now LLC, Jersey City, serving HVAC, plumbing and electrical " +
      "contractors with Google Maps, website SEO, Local Service Ads and Google Ads. The public " +
      "site claims 500 or more contractors served, which is cumulative rather than active. " +
      "Client sentiment is strong: 4.8 from 102 Birdeye reviews, with no independent negative " +
      "cluster found anywhere. Terms are month to month with 30 days' notice." },
    { t: "callout", cls: "bad", h: "Every third-party revenue and headcount figure is unusable",
      p: ["ZoomInfo says 51 to 200 employees and under $5M revenue. Crunchbase says 51 to 100. " +
          "Prospeo says 11 to 20. Clodura says 11 to 50. That is a tenfold spread of scraped " +
          "guesses about a private LLC with no filings. None of it should be repeated as fact, " +
          "including the $1.63M figure quoted in the brief.",
          "What can be modelled honestly: at 100 active clients, ARR is $1.5M at $1,250 average " +
          "monthly account value, $2.4M at $2,000, $3.0M at $2,500. Published home-services " +
          "retainers run $1,000 to $3,500 for SEO alone and $2,500 to $12,000 for full service, " +
          "so the plausible band is wide and the point estimate is unknowable from outside."] },
    { t: "callout", cls: "good", h: "Why PMNow is the better first anchor",
      p: ["The unit is already defined and the ratio is already known: one strategist owns 35 to " +
          "45 accounts. The buyer has already named the problem out loud, which is quality on " +
          "accounts nobody is watching. Month-to-month terms make silent churn the dominant " +
          "commercial risk, and coverage is precisely what a pod sells. Forty near-identical " +
          "HVAC and plumbing accounts are far more repeatable than 46 heterogeneous franchise " +
          "territories with 46 different owners."] },
    { t: "p", v: "The Jason Hennessey outsourcing-genius method is documented publicly: bring " +
      "in a world-class outside specialist, have them audit one client site, test the findings, " +
      "then apply what works across the whole book. The specific budget figures quoted in the " +
      "brief, five to ten thousand a month and five thousand per audit, could not be verified " +
      "and should not be repeated back to anyone as fact. The method itself is safe to reference." }
  ]
},

offers: {
  title: "Offers",
  lede: "Two offers, same machine, different unit. Both quote a price that clears cost, with " +
        "the $300 anchor shown against it so the gap is visible rather than hidden.",
  blocks: [
    { t: "h", v: "Offer A, MaidThis Growth Operations Unit" },
    { t: "kv", items: [
      ["Unit", "One active territory"],
      ["Brief's hypothesis", "$300 per territory per month"],
      ["Modelled breakeven at 46 units, LEAN", "about $454"],
      ["Recommended price", "$450 per active territory, minimum 30 units billed"],
      ["Contract MRR at 46 units", "$20,700"],
      ["Versus the open role", "$5,000 to $7,000 a month for one person, who still needs a team"] ] },
    { t: "list", h: "In scope", items: [
      "Per-market scorecard: demand, visibility, review equity, competitive position, funnel",
      "Vendor scorecarding and monthly performance review against measured outcomes",
      "Local search and Maps programme management across all active territories",
      "Paid media oversight and budget allocation recommendations, media itself excluded",
      "Landing page and conversion work on franchise location pages",
      "Reporting, anomaly detection and quarterly market plans",
      "Capacity-aware acquisition planning once cleaner-supply data is available",
      "The pod: strategy, local SEO, analysis, junior execution, QA, management, tooling, office"] },
    { t: "list", h: "Explicitly excluded and billed transparently at cost", items: [
      "All paid media spend",
      "Premium link and digital PR placements",
      "External expert consultant fees",
      "Custom software development",
      "Call tracking, CRM and third-party licences held in the client's name",
      "Unusual data costs beyond the standard research stack"] },
    { t: "callout", cls: "warn", h: "The honest weakness in Offer A",
      p: ["46 territories with 46 different owners is 46 relationships, not one. Franchisee " +
          "cooperation is not in our control and is not in the franchisor's control either. " +
          "Price this at a per-territory rate but scope the work at the corporate layer, or the " +
          "pod will drown in owner-by-owner coordination that no model accounts for."] },

    { t: "h", v: "Offer B, PMNow Search Fulfilment Pod" },
    { t: "kv", items: [
      ["Unit", "One active client account"],
      ["Brief's hypothesis", "$300 per account per month"],
      ["Modelled breakeven at 40 accounts, MINIMAL", "about $399"],
      ["Modelled breakeven at 120 accounts, MINIMAL", "about $333"],
      ["Recommended opening price", "$450 per account, minimum 40 accounts billed, " +
        "11% margin at 40 rising to 26% at 120"],
      ["Path to $300", "Only at 200 or more accounts on a stripped pod, and only if the expert " +
        "budget is billed separately"] ] },
    { t: "list", h: "In scope", items: [
      "Senior diagnosis on onboarding and on a fixed review cadence",
      "Local search strategy, GBP and Maps programme, citations and entity work",
      "Technical QA and implementation against a published checklist",
      "Content planning and internal linking",
      "Reporting and account health monitoring with proactive escalation",
      "Consultant findings translated into SOPs, tested, then rolled across the book",
      "Portfolio QA: every account reviewed by a human on a committed cadence"] },
    { t: "callout", cls: "good", h: "The line that sells Offer B",
      p: ["\"Your risk is not that the work is bad. It is that on a month-to-month book, an " +
          "account can go quiet for eight weeks before anyone notices, and by then the " +
          "cancellation is already written. I will guarantee that no account in my pod goes " +
          "more than fourteen days without a human review, and I will report the exceptions " +
          "to you myself.\""] }
  ]
},

guarantees: {
  title: "Guarantees",
  lede: "No ranking guarantees. No revenue guarantees. Everything below is measured on inputs " +
        "we control, with the downside to us stated plainly.",
  blocks: [
    { t: "table", head: ["Tier", "Commitment", "Measure", "Remedy", "Downside to us"], rows: [
      ["LOW RISK", "Coverage cadence: every account or territory receives a documented human " +
        "review at least every 14 days", "Timestamped review log, audited monthly",
        "5% fee credit per missed account-month", "Small. Fully within our control. Costs " +
        "roughly 0.5 to 1 hour per account per month, already in the pod model."],
      ["LOW RISK", "Reporting latency: monthly reporting delivered by the fifth working day",
        "Delivery timestamp", "2% fee credit per late month",
        "Small, but it forces month-end data discipline from day one."],
      ["BALANCED", "Implementation turnaround: approved work items shipped within 10 working days",
        "Ticket open-to-close time", "10% fee credit if under 90% adherence in a month",
        "Moderate. Exposed to client-side approval delays, so the clock must stop while waiting " +
        "on the client and that must be written into the contract."],
      ["BALANCED", "QA pass rate: 95% of delivered items pass the published QA checklist first time",
        "QA log with a sampled independent re-check", "10% fee credit below threshold",
        "Moderate. Requires a real QA layer, which is why the MINIMAL pod cannot honestly sell " +
        "this tier."],
      ["BALANCED", "Cost baseline: a complete, invoice-level fully loaded cost per account or " +
        "territory delivered within 60 days", "The document itself",
        "Full refund of the first 60 days if not delivered",
        "Low if the client shares invoices, total if they do not. Make client cooperation an " +
        "explicit precondition."],
      ["AGGRESSIVE", "Controllable cost reduction: an identified and agreed path to a 15% " +
        "reduction in controllable fulfilment cost per unit without reducing agreed service levels",
        "Agreed baseline versus month 6 actuals",
        "Fee reduced to cost until the target is met",
        "High. Only offer this after the baseline exists. Never offer it before seeing invoices."],
      ["AGGRESSIVE", "Cost per qualified lead, where clean attribution exists",
        "Client call tracking or CRM, agreed source definitions", "Fee credit on a sliding scale",
        "Very high. Gated by media budget, market conditions and, for MaidThis, cleaner " +
        "capacity. Recommend against in year one."] ] },
    { t: "callout", cls: "bad", h: "Never say this in a first meeting",
      p: ["\"I will reduce your vendor costs.\" You have not seen an invoice. The moment you " +
          "say it, it becomes the term of the deal and every later finding is measured against " +
          "a promise you made blind.",
          "Say instead: once the cost baseline exists, part of my compensation can be tied to " +
          "reducing controllable fulfilment cost per unit without reducing agreed service levels."] }
  ]
},

risks: {
  title: "Risks",
  lede: "Ranked by how much of the model each one destroys.",
  blocks: [
    { t: "table", head: ["#", "Risk", "Class", "Impact", "What would confirm it", "Mitigation"], rows: [
      ["R1", "The $300 anchor becomes the negotiating ceiling because it was floated first",
        "Commercial", "Fatal to margin",
        "The client repeats $300 back as the expected number",
        "Never send $300 in writing. Lead with the cost baseline, price after it exists."],
      ["R2", "North Macedonian employer cost is 16 to 18 percent above gross rather than equal to it",
        "Cost model", "Every breakeven moves up by roughly the same percentage",
        "PwC and Playroll disagree. An accountant's quote settles it in one call",
        "Get a written quote from a Skopje payroll firm before signing anything. The model has " +
        "a switch for this."],
      ["R3", "The measured coverage gap is a scanning artefact, not a real gap",
        "Evidence", "Removes the strongest quality argument",
        "Grid-scan a suburban territory and find MaidThis ranking well off-centroid",
        "Re-measure three suspect markets with a proper geo-grid before presenting the finding. " +
        "Present it as a question, never as an accusation."],
      ["R4", "Anchors will not separate media and hard costs from the per-unit fee",
        "Commercial", "Makes the price meaningless and the margin unknowable",
        "Client asks for an all-in number including ad spend",
        "Walk away from all-in pricing. It is the single line that cannot bend."],
      ["R5", "Franchisee cooperation, 46 owners rather than one buyer",
        "Delivery", "Silent cost overrun that no model captures",
        "More than two hours a month per territory going to owner coordination",
        "Contract with the franchisor for corporate-layer work. Price owner-level coordination " +
        "separately or exclude it."],
      ["R6", "Cleaner capacity, not leads, is the real MaidThis constraint",
        "Product fit", "An acquisition offer answers the wrong question",
        "Already confirmed by the founder's own public statement",
        "Lead with capacity-aware growth. Instrument the recruitment funnel, do not compete " +
        "with the founder's own build."],
      ["R7", "Key-person concentration on the owner",
        "Operational", "Caps growth at roughly two pods",
        "The owner is still doing senior delivery above $30k MRR",
        "Second senior strategist hired at pod two, not pod three. Budget for it in the price."],
      ["R8", "Single-client concentration",
        "Commercial", "One 30-day cancellation ends the company",
        "One anchor is more than 60 percent of MRR",
        "Do not build past two pods for one client without a second anchor signed."],
      ["R9", "PMNow's real fully loaded cost per account is already below $400",
        "Commercial", "Removes the savings argument entirely",
        "They share the number and it starts with a 2 or a 3",
        "Then sell coverage and QA, not savings. The guarantee tier carries the offer instead."],
      ["R10", "Vendor incumbency is a related party",
        "Relationship", "A consolidation pitch reads as an attack on a franchisee",
        "Already established for Lahav Media and Denver",
        "Scorecard, never propose replacement. Let measurement lead."],
      ["R11", "Client-supplied FDD figures carry through the whole financial model unverified",
        "Evidence", "The marketing-pool sizing collapses if the digital package line is wrong",
        "A current FDD showing no Digital Marketing Package line",
        "Buy the current FDD before quoting the pool. It is the cheapest risk reduction available."],
      ["R12", "Currency and wage inflation in North Macedonia",
        "Cost model", "Margin erosion of a few points a year",
        "Average salary growth outpacing the contracted fee",
        "Annual indexation clause tied to a published wage index, not to CPI."] ] }
  ]
},

market: {
  title: "Market size",
  lede: "Who else buys this, and how many of them there are. Every figure here is a MODEL " +
        "built on stated assumptions, not a market research purchase.",
  blocks: [
    { t: "stats", items: [
      ["TAM, modelled", "$3.1B", "", "US multi-location and agency fulfilment spend addressable " +
        "by a per-unit operating layer"],
      ["SAM, modelled", "$210M", "", "Organisations of 40 to 300 units or accounts, English " +
        "speaking, search-led acquisition"],
      ["Beachhead ICP", "~1,800 firms", "accent", "US home-services and local SEO agencies with " +
        "50 to 500 clients, plus franchise systems of 20 to 300 units"],
      ["Average account value", "$18k to $60k/yr", "", "40 to 120 units at $450 per unit"] ] },
    { t: "p", v: "The TAM figure is built bottom-up and should be treated as an order of " +
      "magnitude, not a number. Assume roughly 3,000 US agencies serving 50 or more local " +
      "clients and roughly 3,500 franchise systems with 20 or more units. If the addressable " +
      "fulfilment layer is worth $450 per unit per month and the median organisation carries 90 " +
      "units, that is about $486,000 a year per organisation of total fulfilment spend, of which " +
      "the operating layer is a fraction. The honest read is that the market is far larger than " +
      "this company can ever serve, and the constraint is delivery capacity, not demand." },
    { t: "h", v: "Buyer profiles, ranked by fit" },
    { t: "table", head: ["Segment", "Unit", "Why they buy", "Trigger event", "Fit"], rows: [
      ["Local SEO and home-services agencies, 50 to 500 clients", "Client account",
        "Senior judgement does not scale with headcount, and quiet accounts churn",
        "A strategist quits, or a churn spike", "Best"],
      ["Franchise systems, 20 to 300 units", "Territory",
        "Fragmented vendor stack and no per-market view",
        "Hiring a first or second marketing leader", "Strong"],
      ["Multi-location home services, HVAC, plumbing, roofing, restoration", "Location",
        "Acquisition cost varies wildly by branch and nobody knows why",
        "A private equity roll-up or a new CFO", "Strong"],
      ["Dental and med spa groups", "Practice",
        "High CPC, high LTV, weak local search discipline",
        "DSO acquisition or a new group marketing hire", "Good"],
      ["Legal networks and multi-office firms", "Market",
        "Extreme CPC makes small efficiency gains large in dollars",
        "New market entry", "Good, but crowded with incumbents"],
      ["Cleaning franchises other than the anchor", "Territory",
        "Same problem, same shape, and a case study already exists",
        "Competitive pressure from a franchisor that fixed it", "Good, watch conflicts"] ] },
    { t: "callout", cls: "warn", h: "On the request for 100 named lookalike companies",
      p: ["Not delivered in this version, and deliberately so. A list of 100 names assembled " +
          "from directory scraping would look like research and behave like noise, and this " +
          "study is built on a rule that nothing gets presented as fact unless it was verified. " +
          "The pipeline to build it properly is specified in the Build tab: a DataForSEO " +
          "Business Listings sweep by category and unit count, filtered against live franchise " +
          "registries. That sweep bills per result, so it needs its own budget decision before " +
          "it runs."] }
  ]
},

build: {
  title: "Build",
  lede: "What happens next, in order, and what is still missing from this study.",
  blocks: [
    { t: "h", v: "The 90-day pilot" },
    { t: "table", head: ["Window", "Objective", "Deliverable", "Gate"], rows: [
      ["Days 1 to 30", "See everything",
        "Invoice-level vendor map, fully loaded cost per unit, per-unit coverage baseline, " +
        "funnel definition agreed",
        "If the client will not share invoices, stop here and say so"],
      ["Days 31 to 60", "Prove coverage",
        "Every unit reviewed by a human on the committed cadence, exceptions reported weekly, " +
        "first scorecard live",
        "Coverage adherence above 95%, or the guarantee tier drops"],
      ["Days 61 to 90", "Hand over the machine",
        "Working scorecard, documented SOPs, signed cost-per-unit target, agreed pricing for " +
        "the ongoing term",
        "A signed number, not a compliment"] ] },
    { t: "h", v: "What this study does not yet contain" },
    { t: "list", items: [
      "The current MaidThis FDD. Everything about the Digital Marketing Package, the local " +
        "marketing requirement and the 2025 or 2026 Item 19 and Item 20 tables rests on the " +
        "client's own reading of the 2024 document. Buying the current FDD is the single " +
        "cheapest risk reduction available and should happen before any pool sizing is quoted.",
      "Demographic and short-term-rental overlays per market. The US Census ACS API now " +
        "requires a key, so population, household count, median income and tenure split were " +
        "not collected. pipeline/collect_demographics.py is stubbed and needs a free key.",
      "Geo-grid Maps scanning. Every Maps position here is a single city-centroid measurement. " +
        "Suburban territories can be invisible at the centroid while trading well.",
      "The 100-company lookalike list. Specified, not built. Needs its own DataForSEO budget.",
      "Any PMNow-internal number. Client count, ARPA, tenure, churn and consultant spend are " +
        "all unknown from outside and all four have to come from the buyer.",
      "A written payroll quote from a Skopje accountant to settle the employer-cost conflict."] },
    { t: "h", v: "Running the pipeline" },
    { t: "code", v: [
      "# resolve markets, pull search volume, Maps packs and organic SERPs",
      "python pipeline/collect_markets.py       # resumable, hard budget cap in pipeline/dfs.py",
      "",
      "# rebuild every dataset from raw signals",
      "python pipeline/build_datasets.py        # market opportunity + dashboard bundle",
      "python pipeline/build_locations.py       # master location database",
      "python pipeline/build_economics.py       # salary model + unit economics",
      "python pipeline/build_evidence.py        # source ledger, vendor stack, PMNow",
      "",
      "# check spend against the cap",
      "python pipeline/dfs.py"].join("\n") },
    { t: "callout", cls: "good", h: "DataForSEO spend on this study",
      p: ["$13.43 against the $20 authorised on the HQDM account. Every call is logged to " +
          "raw/dfs_cost_log.jsonl and to the shared HQDM cost log, and pipeline/dfs.py refuses " +
          "to call the API once $18 is reached."] }
  ]
}
};
