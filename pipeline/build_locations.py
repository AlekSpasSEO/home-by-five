"""Build the MaidThis master location database.

Method, and its limits:
  maidthis.com sits behind a bot-challenge wall, so the /locations/ page could not be
  read directly. The market list is instead reconstructed from the search index via
  DataForSEO Labs relevant_pages (453 indexed pages, 46 distinct city URL segments).
  Operating status is then confirmed independently by looking for a live MaidThis
  Google Business Profile in the Maps pack for each market.

  A live location page proves a page exists. A live GBP with reviews proves someone is
  trading. Only the second is treated as evidence of an operating territory.

Owner attribution comes from the client's own reading of the 2024 FDD Item 20 franchisee
list plus public franchise announcements. Names are carried at Medium confidence and are
not independently re-verified here, except David Lahav.
"""
import csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCESSED = "2026-08-26"

# Owner attributions the client extracted from the 2024 FDD Item 20 franchisee list and
# from public MaidThis franchise announcements. slug -> (owner, background, territories,
# award/launch note, evidence)
OWNERS = {
 "denver": ("David Lahav", "Founder and CEO of Lahav Media, the SEO vendor in the MaidThis "
            "stack; described as the first MaidThis franchisee; also holds Austin", 2,
            "https://www.crunchbase.com/person/david-lahav", "High"),
 "austin": ("David Lahav", "Same owner as Denver/Boulder; multi-unit", 2,
            "https://www.crunchbase.com/person/david-lahav", "Medium"),
 "miami": ("Christopher Rodriguez", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "st-petersburg-clearwater": ("Orlando Reyes", "", 1,
                              "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "tampa": ("Megan Hodges", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "west-palm-beach": ("Maddy McDermott", "", 1,
                     "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "charlotte": ("Priyank Faldu", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "durham": ("Willem Heetderks", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "wilmington": ("Louie Pullen", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "myrtle-beach": ("Dan Blaker", "", 1, "USER-SUPPLIED FDD EXTRACT (2024 FDD Item 20)", "Medium"),
 "saltlakecity": ("Brian Boyle", "Bought Salt Lake City in 2022 and Provo in 2024; multi-unit", 2,
                  "USER-SUPPLIED, public franchisee statement", "Medium"),
 "chicago": ("Brandon Cleeton and Sarah Osmun", "Announced publicly as new owners of MaidThis "
             "Cleaning Chicago", 1, "USER-SUPPLIED, public MaidThis announcement", "Medium"),
 "flower-mound": ("Matthew (surname not public)", "Described publicly as a real-estate investor", 1,
                  "USER-SUPPLIED, public MaidThis announcement", "Low"),
}

# Markets where the client's brief names a sub-territory that has no separate URL segment.
EXTRA_NOTES = {
 "denver": "Boulder CO is served from this territory (maidthis.com/denver/boulder-co/)",
 "saltlakecity": "Provo UT reported as a second territory under the same owner, no separate URL",
 "los-angeles": "Corporate / affiliate operation, not a franchised territory",
}


def build():
    mk = json.load(open(os.path.join(ROOT, "app/data/markets.json")))
    rows = []
    for m in sorted(mk["markets"], key=lambda x: (x["state"], x["city"])):
        slug = m["slug"]
        owner, background, terr, ev, conf = OWNERS.get(slug, ("", "", "", "", "Low"))
        gbp_found = m["gbp_reviews"] is not None or m["maps_rank_general"] is not None

        if m["market_type"] == "corporate":
            status = "CORPORATE / AFFILIATE"
        elif gbp_found:
            status = "OPERATING"
        else:
            status = "AWARDED OR NOT YET VISIBLE"

        rows.append({
            "location_name": m["gbp_title"] or ("MaidThis " + m["market"]),
            "city": m["city"], "state": m["state"], "territory": m["market"],
            "consumer_url": "https://maidthis.com/%s/" % slug,
            "launch_date_estimate": "",
            "franchise_award_date": "",
            "owner_name": owner,
            "owner_linkedin": "",
            "owner_background": background,
            "single_or_multi_unit": ("multi" if (terr or 0) and terr > 1 else
                                     ("single" if owner else "unknown")),
            "number_of_territories_owned": terr or "",
            "status_operating_awarded_unknown": status,
            "gbp_rating": m["gbp_rating"] or "",
            "gbp_reviews": m["gbp_reviews"] or "",
            "maps_rank_house_cleaning": m["maps_rank_general"] if m["maps_rank_general"] else "",
            "maps_rank_airbnb_cleaning": m["maps_rank_str"] if m["maps_rank_str"] else "",
            "opportunity_score": m["opportunity_score"],
            "operating_status_evidence": (
                "Live MaidThis GBP found in the Maps pack (DataForSEO, %s)" % ACCESSED
                if gbp_found else
                "Location page indexed but no MaidThis GBP found in the top 20 Maps results"),
            "evidence_url": ev or "https://maidthis.com/%s/" % slug,
            "evidence_date": ACCESSED,
            "confidence": conf if owner else ("High" if gbp_found else "Medium"),
            "notes": EXTRA_NOTES.get(slug, ""),
        })

    cols = list(rows[0].keys())
    path = os.path.join(ROOT, "data/maidthis_locations.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    operating = sum(1 for r in rows if r["status_operating_awarded_unknown"] == "OPERATING")
    awarded = sum(1 for r in rows if r["status_operating_awarded_unknown"].startswith("AWARDED"))
    named = len({r["owner_name"] for r in rows if r["owner_name"]})
    multi = sum(1 for r in rows if r["single_or_multi_unit"] == "multi")

    summary = {"market_pages": len(rows), "operating_confirmed": operating,
               "awarded_or_not_visible": awarded, "corporate": 1,
               "named_owners": named, "multi_unit_owners": multi,
               "method": "URL segments from the search index, operating status confirmed "
                         "by live GBP presence in the Maps pack"}
    json.dump(summary, open(os.path.join(ROOT, "app/data/locations_summary.json"), "w"), indent=1)

    print("wrote data/maidthis_locations.csv  %d rows" % len(rows))
    print("  operating (GBP confirmed): %d" % operating)
    print("  page exists, no GBP found: %d" % awarded)
    print("  named owners: %d, multi-unit: %d" % (named, multi))


if __name__ == "__main__":
    build()
