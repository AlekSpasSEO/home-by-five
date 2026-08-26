"""Build the hand-curated evidence datasets.

Every row carries an evidence class:
  FACT              direct primary evidence (FDD, company site, job post, founder statement)
  STRONG INFERENCE  several independent signals point the same way
  MODEL             our own calculation from stated assumptions

Rows sourced from the client's own prior FDD reading are tagged
"USER-SUPPLIED FDD EXTRACT" and carry Medium confidence unless a second
source corroborates them.
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCESSED = "2026-08-26"


def write(path, cols, rows):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})
    print("wrote %-46s %d rows" % (path, len(rows)))


# ---------------------------------------------------------------- source ledger
SL_COLS = ["id", "subject", "claim", "value", "evidence_class", "confidence",
           "source_name", "source_url", "publication_date", "accessed", "conflict_note"]

SOURCES = [
 ("S001", "MaidThis", "Unit count published by Franchise Business Review", "38 units",
  "FACT", "High", "Franchise Business Review",
  "https://franchisebusinessreview.com/top-franchises/maidthis/", "2026", ACCESSED,
  "Self-reported to FBR. Counts awarded units, not necessarily open-and-trading units."),
 ("S002", "MaidThis", "Entrepreneur franchise directory listing", "42 units",
  "FACT", "High", "Entrepreneur Franchise Directory",
  "https://www.entrepreneur.com/franchises/directory/maidthis-cleaning/336063", "2026", ACCESSED,
  "Higher than FBR's 38. Both are franchisor-supplied, captured at different dates."),
 ("S003", "MaidThis", "Franchise fee (Entrepreneur listing)", "$42,500",
  "FACT", "High", "Entrepreneur Franchise Directory",
  "https://www.entrepreneur.com/franchises/directory/maidthis-cleaning/336063", "2026", ACCESSED,
  "Older FDD summaries show $39,000. Fee appears to have risen."),
 ("S004", "MaidThis", "Royalty and ad royalty (Entrepreneur listing)", "6% royalty, 2% ad royalty",
  "FACT", "High", "Entrepreneur Franchise Directory",
  "https://www.entrepreneur.com/franchises/directory/maidthis-cleaning/336063", "2026", ACCESSED,
  "Consistent across FDD summaries. Brand fund may rise to 3%."),
 ("S005", "MaidThis", "Initial investment range (Entrepreneur listing)", "$68,300 - $79,900",
  "FACT", "High", "Entrepreneur Franchise Directory",
  "https://www.entrepreneur.com/franchises/directory/maidthis-cleaning/336063", "2026", ACCESSED,
  "Older FDD summaries show $49,550 - $67,650. Investment has risen with the fee."),
 ("S006", "MaidThis", "Founded / began franchising", "Founded 2013, franchising 2020",
  "FACT", "Medium", "Entrepreneur Franchise Directory",
  "https://www.entrepreneur.com/franchises/directory/maidthis-cleaning/336063", "2026", ACCESSED,
  "FBR says franchising began 2021. Another source says the current franchisor entity began "
  "offering on 2023-05-19. Likely reflects an entity restructure."),
 ("S007", "MaidThis", "2024 FDD date and franchisor FY2023 result",
  "FDD dated 2024-04-29; FY2023 net loss over $109,000; member deficit over $98,000",
  "FACT", "High", "Free FDD Library",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024", ACCESSED,
  "Independently corroborates the client's own FDD reading of a $109,354 FY2023 loss."),
 ("S008", "MaidThis", "2024 FDD Item 20 franchised outlets",
  "1 franchised at start of 2022, 13 franchised at end of 2023",
  "FACT", "High", "Free FDD Library",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024", ACCESSED,
  "Item 20 reports fiscal-year-end counts, so a 2024 FDD describes Dec-2023, not today."),
 ("S009", "MaidThis", "2025 FDD summary unit counts",
  "15 total units: 13 franchised, 2 company-owned",
  "FACT", "Medium", "FranchisePayback",
  "https://www.franchisepayback.com/franchise/maidthis", "2026", ACCESSED,
  "Third-party FDD summary, not the document itself. Same 13/2 split as the 2024 FDD, so "
  "this may be a stale copy of the earlier year."),
 ("S010", "MaidThis", "Item 19 average unit volume reported by third parties",
  "$139,090 yearly gross sales; owner-operator earnings $19,473 - $25,037",
  "FACT", "Low", "VettedBiz", "https://www.vettedbiz.com/franchises/maid-this", "2026", ACCESSED,
  "Conflicts with FranchiseOverview's '$1.1M average revenue, 2 units sampled'. The $1.1M "
  "figure is almost certainly the corporate/affiliate operation, not a franchisee average."),
 ("S011", "MaidThis", "Item 19 average revenue reported by third parties",
  "$1.1M average revenue, sample of 2 units",
  "FACT", "Low", "FranchiseOverview", "https://franchiseoverview.com/company/maidthis",
  "2026", ACCESSED,
  "Sample of 2 makes this an affiliate/company-operation figure, not a franchisee benchmark."),
 ("S012", "MaidThis", "Franchisor entity and formation",
  "MaidThis Franchising LLC, Nevada LLC formed 2019-12-02; HQ La Mirada, CA; began offering "
  "franchises 2023-05-19",
  "FACT", "Medium", "Oakscale / franchise registry summary",
  "https://www.oakscale.com/post/franchise-basics-where-to-find-free-franchise-disclosure-documents-fdds",
  "", ACCESSED, "The 2023 offering date conflicts with 2020/2021 franchising-start claims."),
 ("S013", "MaidThis", "Consumer-site market footprint",
  "453 indexed pages; 46 distinct city/market URL segments",
  "FACT", "High", "DataForSEO Labs relevant_pages for maidthis.com",
  "https://maidthis.com/", ACCESSED, ACCESSED,
  "Derived from search index, not from the franchisor. A live page does not prove an "
  "operating franchisee, and maidthis.com is behind a bot wall so the /locations/ page "
  "could not be read directly."),
 ("S014", "MaidThis", "Franchisee marketing spend, Item 19 cohort",
  "5 franchisees, FY2023: $1,022,742 revenue, $118,263 marketing = 11.56%",
  "FACT", "Medium", "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 19)",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024", ACCESSED,
  "Client's own reading of Item 19. Not independently re-derived here. Young-cohort data."),
 ("S015", "MaidThis", "Corporate/affiliate marketing intensity",
  "FY2023: $1,258,495 revenue, $65,777 marketing = 5.23%",
  "FACT", "Medium", "USER-SUPPLIED FDD EXTRACT (2024 FDD)",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024", ACCESSED,
  "Client's own reading. This is the mature-state benchmark the model leans on."),
 ("S016", "MaidThis", "Franchisor P&L, January to October 2024",
  "Royalty $113,577; Monthly Marketing Fee $149,398; Tech fee $38,000; Franchise fees "
  "$284,228; Total income $614,242; Net income $41,509",
  "FACT", "Medium", "USER-SUPPLIED FDD EXTRACT (2024 FDD, unaudited interim)",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024", ACCESSED,
  "Unaudited 10-month statement. The $149,398 marketing-fee line is the single most "
  "important number in this study and should be re-verified against the current FDD."),
 ("S017", "MaidThis", "Digital Marketing Package and local marketing requirement",
  "Digital package $750 - $1,500/month (2026 reading) or $1,097 - $1,500 (2024 reading); "
  "local marketing minimum is the greater of $1,000/month or 5% of Gross Sales",
  "FACT", "Low", "USER-SUPPLIED FDD EXTRACT",
  "https://www.freefddlibrary.com/franchises/maidthis", "2024/2026", ACCESSED,
  "NOT independently verified. No public FDD summary reachable in this run discloses a "
  "Digital Marketing Package line. Treat as the highest-priority item to confirm."),
 ("S018", "Vendor", "Lahav Media MaidThis case study",
  "32 locations referenced; Chattanooga: 33 page-one keywords, 34 organic leads, 0 to 368 "
  "organic visits in 2 months, #1 on Google Maps",
  "FACT", "High", "Lahav Media",
  "https://www.lahavmedia.com/case-studies/maidthis-page-one-in-two-months", "", ACCESSED,
  "Vendor-published, so the metrics are OWNED evidence, not independent verification."),
 ("S019", "Vendor", "David Lahav is both the Lahav Media founder and a MaidThis franchisee",
  "Founder and CEO of Lahav Media; owner of MaidThis Denver/Boulder; described as the first "
  "MaidThis franchisee",
  "STRONG INFERENCE", "High", "Crunchbase person profile + MaidThis Denver franchise "
  "testimonial video + Lahav Media podcast episode with Neel Parekh",
  "https://www.crunchbase.com/person/david-lahav", "", ACCESSED,
  "Three independent signals agree. This is a related-party relationship and it changes "
  "how the SEO vendor line can be renegotiated."),
 ("S020", "Vendor", "GBG Marketing MaidThis deployment and results",
  "33+ MaidThis locations; +39% conversion; STR lead costs down 75%; database generating "
  "$4,000+/month; 10-touch SMS/email/voicemail/human sequence",
  "FACT", "High", "GBG Marketing", "https://gbg.marketing/", "", ACCESSED,
  "Vendor-published (OWNED). The 33+ location figure is a useful independent cross-check "
  "on network size."),
 ("S021", "MaidThis", "Open Director of Marketing role",
  "$5k - $7k per month; owns Vendor Hub, paid budgets across franchisee markets, SEO vendor "
  "direction, KPI dashboards per market, quarterly marketing package refresh, AI deployment",
  "FACT", "High", "DynamiteJobs posting, updated 2026-08-10",
  "https://dynamitejobs.com/company/maidthiscleaning/remote-job/director-of-marketing-local-business-marketing",
  "2026-08-10", ACCESSED,
  "This job description is the clearest public statement of the problem being sold into."),
 ("S022", "MaidThis", "Stated operating bottleneck",
  "Surveyed 40+ franchise owners; the constraint was hiring cleaners, not leads; building an "
  "AI recruiting system",
  "FACT", "Medium", "ZenMaid Filthy Rich Cleaners podcast coverage of Neel Parekh",
  "https://www.zenmaid.com/magazine/scaling-cleaning-business-franchise-neel-parekh/", "",
  ACCESSED, "Founder statement reported by a third party. Corroborates the client's note."),
 ("S023", "MaidThis", "Customer review aggregate",
  "387 reviews, 4.7 average: 343 five-star, 20 four-star, 3 three-star, 11 two-star, 10 one-star",
  "FACT", "Medium", "Trustindex", "https://www.trustindex.io/reviews/maidthis.com", "2026",
  ACCESSED, "Aggregator, selection method not disclosed. Negative themes: incomplete "
  "cleans, quote-versus-charge disputes, scheduling and communication."),
 ("S024", "MaidThis", "Franchisee satisfaction evidence is thin",
  "FBR page states no satisfaction data available; ZeeScores has 3 anonymous reviews at 100/100",
  "FACT", "High", "Franchise Business Review + ZeeScores",
  "https://www.zeescores.com/franchise/maidthis-cleaning", "2026", ACCESSED,
  "n=3 anonymous. Awards (2025/2026 Top Culture, 2026 Top 200) are not satisfaction data."),
 ("S025", "PMNow", "Services, scale claim and contract terms",
  "500+ contractors served; Google Maps, website SEO, Local Service Ads, Google Ads; remote "
  "team with front office in North America and Europe; no long-term contracts, 30-day notice",
  "FACT", "High", "pmnow.biz", "https://pmnow.biz/", "", ACCESSED,
  "'500+ contractors' is cumulative, not an active client count."),
 ("S026", "PMNow", "Client review aggregate", "4.8/5 from 102 reviews",
  "FACT", "High", "Birdeye",
  "https://reviews.birdeye.com/pmnow-proven-marketing-now-166839520848816", "2026", ACCESSED,
  "Collected via a reputation tool the agency controls, so positively selected."),
 ("S027", "PMNow", "Entity and founders",
  "Proven Marketing Now LLC, 121 Newark Avenue Suite 591, Jersey City NJ 07302; founded by "
  "Eric and Michael",
  "FACT", "Medium", "Public business directories",
  "https://www.alignable.com/jersey-city-nj/pmnow-proven-marketing-now-2", "", ACCESSED, ""),
 ("S028", "PMNow", "Third-party firmographic estimates conflict sharply",
  "ZoomInfo 51-200 employees and under $5M revenue; Crunchbase 51-100; Prospeo 11-20; "
  "Clodura 11-50",
  "STRONG INFERENCE", "Low", "ZoomInfo / Crunchbase / Prospeo / Clodura",
  "https://www.zoominfo.com/c/proven-marketing-now/475768855", "2026", ACCESSED,
  "A 10x spread. These are scraped estimates, not filings. Do not quote any of them as fact."),
 ("S029", "PMNow", "Home-services agency retainer benchmarks",
  "SEO $1,000 - $3,500/month; HVAC SEO $1,500 - $5,000/month; full-service $2,500 - "
  "$12,000/month plus ad spend",
  "FACT", "Medium", "Hook Agency / BuiltRight Digital / PipelineOn published pricing guides",
  "https://hookagency.com/blog/digital-marketing-costs-for-home-service-businesses-in-2026/",
  "2026", ACCESSED, "Agency-published price guides, so upward-biased. Used only to bracket ARPA."),
 ("S030", "Method", "Jason Hennessey outsourcing-genius method",
  "Brings in world-class outside specialists to audit one client site, tests the findings, then "
  "applies what works across the whole client base; Hennessey Digital 100+ staff, $10M+ revenue",
  "FACT", "High", "Marketing Speak interview + Hennessey Digital",
  "https://www.marketingspeak.com/blueprint-to-scaling-an-seo-agency-with-jason-hennessey/",
  "", ACCESSED,
  "The specific '$5,000 per audit, $5k-$10k per month' budget figures in the client's brief "
  "were not located in this run. Treat the amounts as unverified."),
 ("S031", "Macedonia", "Statutory social contributions",
  "Pension and disability 18.8%, health 7.5%, employment 1.2%, additional health 0.5% = 28% "
  "of gross; min base 50% of national average salary, max base 16x",
  "FACT", "High", "PwC Worldwide Tax Summaries",
  "https://taxsummaries.pwc.com/north-macedonia/individual/other-taxes", "2026", ACCESSED,
  "PwC states these are withheld from the employee's gross salary. There is no separate "
  "employer-side add-on, so employer cost is approximately equal to gross."),
 ("S032", "Macedonia", "Personal income tax", "10% flat; personal allowance MKD 123,240/year "
  "(MKD 10,270/month)",
  "FACT", "High", "CountryTaxCalc North Macedonia guide",
  "https://www.countrytaxcalc.com/tax-guides/north-macedonia-tax-guide/", "2026", ACCESSED, ""),
 ("S033", "Macedonia", "Conflicting employer-cost claim",
  "Playroll states employer contributions add about 16-18% on top of gross",
  "FACT", "Low", "Playroll", "https://www.playroll.com/employment-cost/north-macedonia",
  "2026", ACCESSED,
  "Directly contradicts PwC. The salary model follows PwC and treats employer cost as equal "
  "to gross, then adds a 5% administrative buffer. If Playroll is right, pod cost rises "
  "roughly 16-18% and margins fall accordingly. Flagged in the risk register."),
 ("S034", "Macedonia", "National average net salary", "MKD 45,961 per month (Nov 2025)",
  "FACT", "High", "wage.is / national statistics aggregation", "https://wage.is/north-macedonia/",
  "2025-11", ACCESSED, "Used to sanity-check the gross-up formula."),
 ("S035", "Macedonia", "Role salary ranges, self-reported",
  "SEO analyst net MKD 24,400 - 59,614 (80% range, n=29); digital marketing specialist net "
  "MKD 28,419 - 62,574",
  "FACT", "Medium", "MojaPlata.mk",
  "https://www.mojaplata.mk/en/salaryinfo/marketing-advertising-pr/seo-analyst", "2026",
  ACCESSED, "Self-reported survey data, small samples, skews to the domestic market rather "
  "than export-facing employers."),
 ("S036", "Macedonia", "Skopje workspace cost",
  "Coworking desk EUR 10/day, private office EUR 25/day; Regus day office MKD 4,290/person/day",
  "FACT", "Medium", "coworkingskopje.com / Regus",
  "https://coworkingskopje.com/", "2026", ACCESSED,
  "Day rates. Monthly contracts are materially cheaper and should be negotiated directly."),
 ("S037", "MaidThis", "Chattanooga Maps pack, measured",
  "MaidThis Cleaning of Chattanooga ranks 3 with 4.9 stars and 142 reviews; Molly Maid of "
  "Chattanooga 4.6 with 276 reviews",
  "FACT", "High", "DataForSEO Google Maps SERP, keyword 'house cleaning service'",
  "https://api.dataforseo.com/", ACCESSED, ACCESSED,
  "Measured directly in this run. Cross-checks the Lahav Media #1-on-Maps claim, which no "
  "longer holds for this head term."),
]

write("research/source_ledger.csv", SL_COLS,
      [dict(zip(SL_COLS, s)) for s in SOURCES])


# ---------------------------------------------------------- vendor stack
VS_COLS = ["vendor", "service", "locations_deployed", "public_results_claimed",
           "estimated_scope", "public_pricing", "likely_pricing_range",
           "relationship_current_or_historical", "replacement_candidate",
           "should_we_keep_them", "why", "source", "evidence_class", "confidence"]

VENDORS = [
 dict(vendor="Lahav Media", service="Franchise / local SEO, location page builds, new-market launch SEO",
      locations_deployed="32 referenced in the case study",
      public_results_claimed="Chattanooga: 33 page-one keywords, 34 organic leads, 0 to 368 organic "
      "visits in 60 days, #1 on Google Maps; site-wide claims of +69% franchise-location traffic",
      estimated_scope="Per-location SEO programme plus new-location launch packages",
      public_pricing="Not published",
      likely_pricing_range="$500 - $1,500 per location per month (bracketed from published "
      "franchise-SEO market rates, not from any Lahav quote)",
      relationship_current_or_historical="Current, based on live case study and podcast ties",
      replacement_candidate="No, not initially",
      should_we_keep_them="KEEP, but put under measurement",
      why="Founder David Lahav also owns the MaidThis Denver/Boulder territory and is described as "
      "the first franchisee. Proposing to replace this vendor without knowing that would be a "
      "serious unforced error. The right move is to scorecard delivery against measured outcomes "
      "and let the data drive the conversation.",
      source="https://www.lahavmedia.com/case-studies/maidthis-page-one-in-two-months ; "
      "https://www.crunchbase.com/person/david-lahav",
      evidence_class="FACT (deployment) / STRONG INFERENCE (related party)", confidence="High"),
 dict(vendor="GBG Marketing", service="Lead conversion, CRM and lifecycle automation, "
      "SMS/email/voicemail sequences, Meta and Google Ads",
      locations_deployed="33+",
      public_results_claimed="+39% conversion; STR lead costs down 75%; database generating "
      "$4,000+/month; 10-touch multi-channel follow-up",
      estimated_scope="Network-wide conversion layer plus paid media for some locations",
      public_pricing="Not published",
      likely_pricing_range="$400 - $1,200 per location per month plus setup, or a platform fee "
      "plus per-location licence (bracketed, not quoted)",
      relationship_current_or_historical="Current, based on live case study",
      should_we_keep_them="KEEP the conversion system, AUDIT the attribution",
      replacement_candidate="No",
      why="A 10-touch speed-to-lead system is genuinely hard to rebuild and is the single "
      "highest-leverage asset in the stack. What needs auditing is whether the +39% is measured "
      "against a clean baseline and whether the claimed gains persist beyond the launch window.",
      source="https://gbg.marketing/", evidence_class="FACT", confidence="High"),
 dict(vendor="Google Ads / Meta (media)", service="Paid acquisition",
      locations_deployed="Network-wide, franchisee-funded",
      public_results_claimed="None published",
      estimated_scope="Local budgets set per territory inside the local marketing requirement",
      public_pricing="n/a, this is media, not a vendor fee",
      likely_pricing_range="Measured weighted CPC across the 46 markets is in this study's "
      "market dataset; modelled cost per lead sits at roughly 10x weighted CPC",
      relationship_current_or_historical="Current",
      replacement_candidate="No, media is never in scope of a per-location fee",
      should_we_keep_them="KEEP, but the buying must be capacity-aware",
      why="Media spend must stay a separate, transparent line. The value we add is deciding "
      "where the next dollar goes, not marking it up.",
      source="https://dynamitejobs.com/company/maidthiscleaning/remote-job/director-of-marketing-local-business-marketing",
      evidence_class="STRONG INFERENCE", confidence="Medium"),
 dict(vendor="Unnamed 'Vendor Hub' suppliers", service="Unknown mix, named only in the job posting",
      locations_deployed="Unknown",
      public_results_claimed="None",
      estimated_scope="The job posting explicitly lists managing 'our marketing vendor "
      "relationships and Vendor Hub' as a duty, which implies more than the two named vendors",
      public_pricing="Unknown", likely_pricing_range="Unknown",
      relationship_current_or_historical="Current",
      replacement_candidate="Unknown until the cost baseline exists",
      should_we_keep_them="Unknown",
      why="This is the largest single blind spot in the MaidThis analysis. The first 30 days of "
      "any engagement must produce the full vendor list with invoices.",
      source="https://dynamitejobs.com/company/maidthiscleaning/remote-job/director-of-marketing-local-business-marketing",
      evidence_class="FACT (that a Vendor Hub exists)", confidence="High"),
 dict(vendor="AI recruiting build", service="Cleaner recruitment funnel",
      locations_deployed="In progress",
      public_results_claimed="None yet",
      estimated_scope="Founder-led build addressing the stated top bottleneck",
      public_pricing="n/a", likely_pricing_range="n/a",
      relationship_current_or_historical="Current, internal",
      replacement_candidate="No",
      should_we_keep_them="SUPPORT IT, do not compete with it",
      why="Marketing that outruns cleaner capacity destroys review scores. The recruitment funnel "
      "is the constraint the acquisition system has to respect, so we should instrument it rather "
      "than own it.",
      source="https://www.zenmaid.com/magazine/scaling-cleaning-business-franchise-neel-parekh/",
      evidence_class="FACT", confidence="Medium"),
]
write("data/maidthis_vendor_stack.csv", VS_COLS, VENDORS)


# ---------------------------------------------------------- PMNow economics
PM_COLS = ["metric", "value", "evidence_class", "confidence", "source", "note"]
PMNOW = [
 dict(metric="Active clients", value="Well over 100 (management statement, unverified)",
      evidence_class="STRONG INFERENCE", confidence="Medium",
      source="Client-relayed management statement",
      note="Not published anywhere reachable. The public site says 500+ contractors served, "
      "which is cumulative, not active."),
 dict(metric="Contractors served historically", value="500+", evidence_class="FACT",
      confidence="High", source="https://pmnow.biz/", note="Cumulative marketing claim."),
 dict(metric="Accounts per strategist", value="35 - 45", evidence_class="STRONG INFERENCE",
      confidence="Medium", source="Client-relayed management statement",
      note="This is the single most important delivery ratio in the PMNow model and the basis "
      "for sizing a 40-account pod."),
 dict(metric="Employee count", value="11 to 200 depending on the data broker",
      evidence_class="STRONG INFERENCE", confidence="Low",
      source="ZoomInfo / Crunchbase / Prospeo / Clodura",
      note="A 10x spread across scraped sources. Unusable as a planning input."),
 dict(metric="Revenue estimate", value="Under $5M (ZoomInfo band); no filed figure exists",
      evidence_class="STRONG INFERENCE", confidence="Low",
      source="https://www.zoominfo.com/c/proven-marketing-now/475768855",
      note="Private LLC, no filings. Do not quote a point estimate."),
 dict(metric="Modelled revenue from client count and ARPA",
      value="100 active clients: $1.5M ARR at $1,250 ARPA, $2.4M at $2,000, $3.0M at $2,500",
      evidence_class="MODEL", confidence="Medium",
      source="This study",
      note="Bracketed by published home-services retainer ranges of $1,000 to $3,500 for SEO "
      "and $2,500 to $12,000 for full service."),
 dict(metric="Services", value="Google Maps, website SEO, Local Service Ads, Google Ads, "
      "conversion-focused websites", evidence_class="FACT", confidence="High",
      source="https://pmnow.biz/", note=""),
 dict(metric="Niche", value="HVAC, plumbing, electrical home-service contractors",
      evidence_class="FACT", confidence="High", source="https://pmnow.biz/", note=""),
 dict(metric="Contract terms", value="No long-term contracts, 30-day cancellation notice",
      evidence_class="FACT", confidence="High", source="https://pmnow.biz/",
      note="Month-to-month terms make silent-account churn the dominant commercial risk, which "
      "matches the stated management concern."),
 dict(metric="Client sentiment", value="4.8/5 from 102 Birdeye reviews", evidence_class="FACT",
      confidence="High",
      source="https://reviews.birdeye.com/pmnow-proven-marketing-now-166839520848816",
      note="OWNED collection channel. Positive but selection-biased. No independent negative "
      "cluster was found, which is itself a meaningful signal."),
 dict(metric="Stated internal concern", value="Maintaining quality on quiet accounts nobody is "
      "watching", evidence_class="STRONG INFERENCE", confidence="Medium",
      source="Client-relayed management statement",
      note="This is the actual product being bought: coverage, not cheaper labour."),
 dict(metric="External expert model", value="Adopted from Jason Hennessey's outsourcing-genius "
      "approach", evidence_class="STRONG INFERENCE", confidence="Medium",
      source="https://www.marketingspeak.com/blueprint-to-scaling-an-seo-agency-with-jason-hennessey/",
      note="The method is documented publicly. The specific dollar budgets quoted in the brief "
      "were not verifiable."),
 dict(metric="Success measure", value="Client-side call volume", evidence_class="STRONG INFERENCE",
      confidence="Medium", source="Client-relayed management statement",
      note="Rankings are not the currency. Any guarantee has to be phrased in call or lead terms "
      "where attribution exists."),
]
write("data/pmnow_economics.csv", PM_COLS, PMNOW)
