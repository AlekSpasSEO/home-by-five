"""North Macedonia delivery-cost model and pod unit economics.

MODEL class throughout. Statutory inputs are FACT (source_ledger S031, S032, S034);
everything derived here is a calculation over stated assumptions.

Gross-up arithmetic, North Macedonia 2026
  contributions = 0.28 * gross      (pension 18.8 + health 7.5 + employment 1.2 + add. health 0.5)
  taxable       = gross - contributions - allowance   (allowance MKD 10,270/month)
  PIT           = 0.10 * max(0, taxable)
  net           = gross - contributions - PIT
  => gross      = (net - 0.1 * allowance) / 0.648

PwC states contributions are withheld from the employee's gross salary, so there is no
separate employer-side percentage and employer cost equals gross plus an administrative
buffer. Playroll disagrees and claims 16-18% on top. EMPLOYER_ADDON switches between the
two readings; the conflict is carried in reports/risk_register.md.

Cost structure separates two layers, which is what creates operating leverage:
  POD LAYER      scales linearly, one team per 40 accounts or territories
  COMPANY LAYER  grows in steps, shared across all pods
"""
import csv, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# FX captured 2026-08-26 from open.er-api.com
EUR_USD = 1.166986
EUR_MKD = 61.497
MKD_USD = EUR_USD / EUR_MKD

ALLOWANCE_MKD = 10270.0
CONTRIB_RATE = 0.28
PIT_RATE = 0.10
ADMIN_BUFFER = 1.05
EMPLOYER_ADDON = 0.00
CONTINGENCY = 0.10
POD_SIZE = 40                      # accounts or territories served by one pod


def gross_from_net(net_mkd):
    return (net_mkd - PIT_RATE * ALLOWANCE_MKD) / (1 - CONTRIB_RATE - PIT_RATE * (1 - CONTRIB_RATE))


def employer_usd(net_mkd):
    return gross_from_net(net_mkd) * (1 + EMPLOYER_ADDON) * ADMIN_BUFFER * MKD_USD


# Target NET monthly pay, set at or above the top of the MojaPlata self-reported ranges.
# The pitch is senior output, not cheapest labour.
ROLES = [
 ("Growth / Product Director (owner)", 140000, "Owns the client relationship, the model and the QA bar"),
 ("Senior Search Strategist",           90000, "Diagnosis, market strategy, senior judgement calls"),
 ("Automation / Data Engineer",         85000, "Pipelines, agents, dashboards, internal tooling"),
 ("QA Lead",                            70000, "Portfolio review, SLA enforcement, account health"),
 ("Paid Media Specialist",              65000, "Budget allocation, channel QA, creative testing"),
 ("Local SEO Specialist",               60000, "GBP, Maps, citations, local entity work"),
 ("Growth / Data Analyst",              60000, "Funnel analysis, reporting, market scorecards"),
 ("Content Strategist",                 50000, "Content planning, briefs, on-page"),
 ("Account / Project Coordinator",      45000, "Scheduling, client comms support, delivery tracking"),
 ("Junior SEO Executive",               35000, "Implementation, audits, repeatable execution"),
 ("VA / Operations Assistant",          32000, "Data entry, listings, admin, reporting prep"),
]
SALARY = {r: employer_usd(n) for r, n, _ in ROLES}

OVERHEAD_EUR = {
    "workspace_per_seat_month": 180,
    "equipment_per_seat_month": 1200 / 36,
    "recruiting_per_hire_amortised_month": 800 / 24,
    "software_base_month": 700,          # company-wide data, AI and reporting stack
    "software_per_pod_month": 320,       # incremental seats and rank/keyword volume per pod
    "accounting_payroll_month": 250,
    "connectivity_utilities_month": 150,
}
OVERHEAD_USD = {k: round(v * EUR_USD, 2) for k, v in OVERHEAD_EUR.items()}
EXPERT_BUDGET_PER_POD = 1500

# One delivery pod per 40 accounts. Three service tiers.
POD_SHAPES = {
 # MINIMAL mirrors the ratio PMNow says it already runs: one senior strategist owning
 # 35-45 accounts with junior and VA support. It is the honest floor, not an aspiration.
 "MINIMAL":  {"Senior Search Strategist": 1.0, "Junior SEO Executive": 1.0,
              "VA / Operations Assistant": 1.0},
 "LEAN":     {"Senior Search Strategist": 1.0, "Local SEO Specialist": 1.0,
              "Junior SEO Executive": 1.0, "VA / Operations Assistant": 1.0},
 "STANDARD": {"Senior Search Strategist": 1.0, "Local SEO Specialist": 1.0,
              "Growth / Data Analyst": 1.0, "Junior SEO Executive": 1.0,
              "VA / Operations Assistant": 1.0},
 "PREMIUM":  {"Senior Search Strategist": 1.0, "Local SEO Specialist": 1.0,
              "Growth / Data Analyst": 1.0, "Content Strategist": 0.5,
              "Paid Media Specialist": 0.5, "Junior SEO Executive": 1.0,
              "VA / Operations Assistant": 1.0},
}


def company_layer(n_pods):
    """Shared headcount. Grows in steps, which is where the leverage comes from."""
    fte = {"Growth / Product Director (owner)": 1.0}
    fte["QA Lead"] = 0.5 if n_pods <= 1 else (1.0 if n_pods <= 3 else 2.0)
    if n_pods >= 2:
        fte["Automation / Data Engineer"] = 1.0
    if n_pods >= 2:
        fte["Paid Media Specialist"] = fte.get("Paid Media Specialist", 0) + 0.5
    fte["Account / Project Coordinator"] = math.ceil(n_pods / 3) if n_pods >= 2 else 0.0
    return {k: v for k, v in fte.items() if v}


def model(shape_name, accounts, price, owner_salary_usd=None,
          expert_budget=EXPERT_BUDGET_PER_POD, workspace=True):
    shape = POD_SHAPES[shape_name]
    n_pods = accounts / POD_SIZE
    whole_pods = max(1, math.ceil(n_pods))

    pod_labour = sum(SALARY[r] * f for r, f in shape.items()) * n_pods
    pod_seats = sum(shape.values()) * n_pods

    comp = company_layer(whole_pods)
    comp_labour = 0.0
    for role, f in comp.items():
        rate = owner_salary_usd if (owner_salary_usd is not None and "Director" in role) else SALARY[role]
        comp_labour += rate * f
    comp_seats = sum(comp.values())

    seats = pod_seats + comp_seats
    overhead = (OVERHEAD_USD["workspace_per_seat_month"] * seats * (1 if workspace else 0)
                + OVERHEAD_USD["equipment_per_seat_month"] * seats
                + OVERHEAD_USD["recruiting_per_hire_amortised_month"] * seats
                + OVERHEAD_USD["software_base_month"]
                + OVERHEAD_USD["software_per_pod_month"] * n_pods
                + OVERHEAD_USD["accounting_payroll_month"]
                + OVERHEAD_USD["connectivity_utilities_month"])
    expert = expert_budget * n_pods
    subtotal = pod_labour + comp_labour + overhead + expert
    total = subtotal * (1 + CONTINGENCY)

    mrr = price * accounts
    gp = mrr - total
    return {
        "pod_shape": shape_name, "accounts": accounts, "price_per_account_usd": price,
        "pods": round(n_pods, 2), "people_fte": round(seats, 2),
        "pod_labour_usd": round(pod_labour), "company_labour_usd": round(comp_labour),
        "overhead_usd": round(overhead), "expert_budget_usd": round(expert),
        "contingency_usd": round(subtotal * CONTINGENCY),
        "delivery_cost_usd": round(total),
        "cost_per_account_usd": round(total / accounts, 2),
        "mrr_usd": round(mrr), "arr_usd": round(mrr * 12),
        "gross_profit_usd": round(gp),
        "gross_margin_pct": round(100 * gp / mrr, 1) if mrr else 0,
        "breakeven_price_usd": round(total / accounts, 2),
        "owner_salary_usd": round(owner_salary_usd if owner_salary_usd is not None
                                  else SALARY["Growth / Product Director (owner)"]),
        "accounts_per_strategist": round(accounts / max(1, sum(
            f for r, f in shape.items() if "Senior" in r) * n_pods), 1),
    }


def main():
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "app/data"), exist_ok=True)

    # salary table
    cols = ["role", "net_mkd_month", "gross_mkd_month", "employer_cost_mkd_month",
            "employer_cost_eur_month", "employer_cost_usd_month", "employer_cost_usd_year", "notes"]
    srows = []
    for role, net, note in ROLES:
        g = gross_from_net(net)
        e = g * (1 + EMPLOYER_ADDON) * ADMIN_BUFFER
        srows.append({"role": role, "net_mkd_month": round(net), "gross_mkd_month": round(g),
                      "employer_cost_mkd_month": round(e),
                      "employer_cost_eur_month": round(e / EUR_MKD),
                      "employer_cost_usd_month": round(e * MKD_USD),
                      "employer_cost_usd_year": round(e * MKD_USD * 12), "notes": note})
    with open(os.path.join(ROOT, "data/macedonia_salary_model.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(srows)
    print("wrote data/macedonia_salary_model.csv  %d roles" % len(srows))

    # scenario grid
    rows = []
    for shape in POD_SHAPES:
        for accounts in (40, 80, 120, 150):
            for price in (250, 300, 350, 400, 450, 500):
                rows.append(model(shape, accounts, price))
    with open(os.path.join(ROOT, "data/unit_economics.csv"), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote data/unit_economics.csv  %d scenarios" % len(rows))

    bundle = {
        "generated": "2026-08-26",
        "fx": {"eur_usd": EUR_USD, "eur_mkd": EUR_MKD, "mkd_usd": round(MKD_USD, 6),
               "captured": "2026-08-26", "source": "open.er-api.com"},
        "statutory": {"contribution_rate": CONTRIB_RATE, "pit_rate": PIT_RATE,
                      "monthly_allowance_mkd": ALLOWANCE_MKD,
                      "employer_addon": EMPLOYER_ADDON, "admin_buffer": ADMIN_BUFFER},
        "roles": [{"role": r, "net_mkd": n, "gross_mkd": round(gross_from_net(n)),
                   "employer_usd": round(SALARY[r]), "note": note} for r, n, note in ROLES],
        "overheads_usd": OVERHEAD_USD, "pod_shapes": POD_SHAPES, "pod_size": POD_SIZE,
        "expert_budget_per_pod_usd": EXPERT_BUDGET_PER_POD, "contingency": CONTINGENCY,
        "scenarios": rows,
    }
    json.dump(bundle, open(os.path.join(ROOT, "app/data/economics.json"), "w"), indent=1)
    print("wrote app/data/economics.json\n")

    tiers = list(POD_SHAPES)
    print("breakeven price per account, by tier and book size")
    print("  book | " + " | ".join("%8s" % t for t in tiers))
    for accounts in (40, 80, 120, 150, 200, 300):
        print("  %4d | " % accounts + " | ".join(
            "%8.0f" % model(t, accounts, 300)["cost_per_account_usd"] for t in tiers))
    print("")
    print("gross margin at $300 per account")
    for t in tiers:
        print("  %-9s" % t + "".join(
            " %6.1f%%" % model(t, a, 300)["gross_margin_pct"]
            for a in (40, 80, 120, 150, 200, 300)))
    print("")
    print("MINIMAL tier with every lever pulled: remote-first, expert budget billed")
    print("separately, owner drawing $1,500/month instead of a full director salary")
    for a in (40, 80, 120, 150, 200, 300):
        m = model("MINIMAL", a, 300, owner_salary_usd=1500, expert_budget=0, workspace=False)
        print("  %4d accounts  cost/acct $%6.2f  margin %6.1f%%  MRR $%s" %
              (a, m["cost_per_account_usd"], m["gross_margin_pct"], format(m["mrr_usd"], ",")))


if __name__ == "__main__":
    main()
