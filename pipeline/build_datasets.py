"""Turn raw DataForSEO signals into the project's analysis datasets.

Outputs:
  data/maidthis_market_opportunity.csv
  app/data/markets.json          (dashboard bundle)

Everything produced here is MODEL class: a transparent calculation over
FACT-class inputs (search volume, CPC, Maps pack composition, organic positions).
"""
import csv, json, math, os, statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE = ["house cleaning services", "maid service", "cleaning service",
        "house cleaning near me", "apartment cleaning service", "recurring house cleaning"]
STR_KWS = ["airbnb cleaning service", "vacation rental cleaning"]
ONEOFF = ["move out cleaning", "deep cleaning service"]

# Market Opportunity Score, documented in reports/market_opportunity.md.
#
# The score is a PRODUCT of two halves, not a weighted sum of six things:
#
#   potential  how much money is actually on the table in this market
#   headroom   how much of it is still available to take
#
# A sum lets a market with almost no search demand score highly just because
# MaidThis is invisible there. A product cannot: near-zero demand drives the
# whole score to near zero, and a market already won drives it down too.
# Inside potential, demand is a MULTIPLIER rather than one weighted term. CPC and
# short-term-rental share are intensity ratios, not sizes: a market with 100 searches a
# month and an expensive click is still a market with 100 searches a month.
#   potential = demand * (0.60 + 0.25*commercial_value + 0.15*str_wedge)
W_POTENTIAL = {"demand": "multiplier", "commercial_value": 0.25, "str_wedge": 0.15}
POTENTIAL_FLOOR = 0.60
W_HEADROOM = {"competitive_headroom": 0.40, "visibility_gap": 0.45, "review_deficit": 0.15}
W = dict(W_POTENTIAL, **W_HEADROOM)


def load_signals():
    """Richest non-error record per key wins.

    Early collection runs stored only the first keyword row per market before the
    bug was fixed, so a later partial record must never overwrite a complete one.
    """
    sig = {"sv": {}, "maps": {}, "org": {}}
    path = os.path.join(ROOT, "raw/market_signals.jsonl")
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        p = r["payload"]
        if isinstance(p, dict) and p.get("_error"):
            continue
        prev = sig[r["kind"]].get(r["key"])
        if r["kind"] == "sv":
            if isinstance(prev, list) and not (isinstance(p, list) and len(p) >= len(prev)):
                continue
        sig[r["kind"]][r["key"]] = p
    return sig


def is_maidthis(item):
    blob = " ".join(str(item.get(k) or "") for k in ("domain", "title", "url"))
    return "maidthis" in blob.lower()


def pack_stats(items, top=5):
    reviews, ratings = [], []
    for it in items[:top]:
        r = it.get("rating") or {}
        if r.get("votes_count"):
            reviews.append(r["votes_count"])
        if r.get("value"):
            ratings.append(r["value"])
    strong = sum(1 for it in items[:20] if ((it.get("rating") or {}).get("votes_count") or 0) >= 200)
    return {"median_reviews": int(statistics.median(reviews)) if reviews else 0,
            "max_reviews": max(reviews) if reviews else 0,
            "avg_rating": round(statistics.mean(ratings), 2) if ratings else None,
            "strong_competitors": strong}


def find_maidthis(items):
    for it in items:
        if is_maidthis(it):
            r = it.get("rating") or {}
            return {"rank": it.get("rank_absolute"), "rating": r.get("value"),
                    "reviews": r.get("votes_count"), "title": it.get("title")}
    return {"rank": None, "rating": None, "reviews": None, "title": None}


def norm(v, lo, hi):
    if hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))


def build():
    sig = load_signals()
    codes = json.load(open(os.path.join(ROOT, "raw/location_codes.json")))
    rows = []

    for slug, meta in codes.items():
        sv = sig["sv"].get(slug) or []
        kv = {r["keyword"]: r for r in sv if isinstance(r, dict) and r.get("keyword")}

        def vol(names):
            return sum((kv.get(n, {}).get("search_volume") or 0) for n in names)

        total = vol(CORE + STR_KWS + ONEOFF)
        core, strv, oneoff = vol(CORE), vol(STR_KWS), vol(ONEOFF)
        cpcs = [((kv[k].get("cpc") or 0), (kv[k].get("search_volume") or 0)) for k in kv
                if kv[k].get("cpc")]
        wsum = sum(v for _, v in cpcs) or 1
        wcpc = round(sum(c * v for c, v in cpcs) / wsum, 2) if cpcs else 0.0
        comp = [kv[k].get("competition_index") for k in kv
                if kv[k].get("competition_index") is not None]
        comp_idx = round(statistics.mean(comp), 1) if comp else None

        gen_items = (sig["maps"].get(slug + "||house cleaning service") or {}).get("items") or []
        str_items = (sig["maps"].get(slug + "||airbnb cleaning service") or {}).get("items") or []
        ps = pack_stats(gen_items)
        mt_gen = find_maidthis(gen_items)
        mt_str = find_maidthis(str_items)

        org = sig["org"].get(slug) or {}
        org_rank = None
        for it in org.get("items") or []:
            if it.get("type") == "organic" and "maidthis" in (it.get("domain") or "").lower():
                org_rank = it.get("rank_group")
                break
        types = org.get("item_types") or []

        rows.append({
            "slug": slug, "market": meta["display"], "city": meta["city"], "state": meta["state"],
            "market_type": meta["type"],
            "data_complete": bool(sv) and bool(gen_items),
            "total_msv": total, "core_msv": core, "str_msv": strv, "oneoff_msv": oneoff,
            "str_share_pct": round(100 * strv / total, 1) if total else 0,
            "weighted_cpc_usd": wcpc, "competition_index": comp_idx,
            "maps_rank_general": mt_gen["rank"], "maps_rank_str": mt_str["rank"],
            "gbp_rating": mt_gen["rating"] or mt_str["rating"],
            "gbp_reviews": mt_gen["reviews"] or mt_str["reviews"],
            "gbp_title": mt_gen["title"] or mt_str["title"],
            "pack_median_reviews": ps["median_reviews"], "pack_max_reviews": ps["max_reviews"],
            "pack_avg_rating": ps["avg_rating"], "strong_competitors_20": ps["strong_competitors"],
            "organic_rank_city_term": org_rank,
            "serp_has_local_pack": "local_pack" in types,
            "serp_has_paid": "paid" in types,
            "serp_item_types": "|".join(types),
        })

    scored = [r for r in rows if r["data_complete"]]
    vols = [r["total_msv"] for r in scored] or [1]
    lo_v, hi_v = math.log10(max(1, min(vols))), math.log10(max(vols) or 1)
    cpc_vals = [r["weighted_cpc_usd"] for r in scored] or [0]
    med_rev = [r["pack_median_reviews"] for r in scored] or [0]
    max_rev = max([r["pack_max_reviews"] for r in scored] or [1]) or 1
    max_wedge = max([r["str_share_pct"] for r in scored] or [1]) or 1

    for r in rows:
        demand = norm(math.log10(max(1, r["total_msv"])), lo_v, hi_v)
        commercial = norm(r["weighted_cpc_usd"], min(cpc_vals), max(cpc_vals))
        wedge = norm(r["str_share_pct"], 0, max_wedge)
        headroom = 1 - norm(r["pack_median_reviews"], min(med_rev), max(med_rev) or 1)

        mr = r["maps_rank_general"]
        if mr is None:
            vis = 1.0
        elif mr <= 3:
            vis = 0.0
        elif mr <= 10:
            vis = 0.45
        else:
            vis = 0.75
        if r["organic_rank_city_term"] is None:
            vis = min(1.0, vis + 0.15)

        deficit = 1 - norm(r["gbp_reviews"] or 0, 0, max_rev)

        parts = {"demand": demand, "commercial_value": commercial, "str_wedge": wedge,
                 "competitive_headroom": headroom, "visibility_gap": vis,
                 "review_deficit": deficit}
        for k, v in parts.items():
            r["score_" + k] = round(v * 100, 1)
        potential = parts["demand"] * (POTENTIAL_FLOOR
                                      + W_POTENTIAL["commercial_value"] * parts["commercial_value"]
                                      + W_POTENTIAL["str_wedge"] * parts["str_wedge"])
        head = sum(W_HEADROOM[k] * parts[k] for k in W_HEADROOM)
        r["score_potential"] = round(potential * 100, 1)
        r["score_headroom"] = round(head * 100, 1)
        r["opportunity_score"] = round(potential * head * 100, 1)
        # absolute view: monthly searches in this market that MaidThis is not positioned for
        r["uncaptured_msv"] = int(round(r["total_msv"] * vis))

        gbp_rev = r["gbp_reviews"] or 0
        if mr is None:
            r["status"] = "LAUNCH"
        elif mr <= 3 and gbp_rev >= 100:
            r["status"] = "DEFEND"
        elif mr <= 10:
            r["status"] = "GROW"
        else:
            r["status"] = "FIX"

        # MODEL: paid cost per lead at an assumed 10% click-to-lead rate
        r["model_cpl_usd"] = round(r["weighted_cpc_usd"] / 0.10, 2) if r["weighted_cpc_usd"] else None

    rows.sort(key=lambda x: -x["opportunity_score"])

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "app/data"), exist_ok=True)
    with open(os.path.join(ROOT, "data/maidthis_market_opportunity.csv"), "w",
              newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    competitors, keywords = {}, {}
    for slug in codes:
        items = (sig["maps"].get(slug + "||house cleaning service") or {}).get("items") or []
        competitors[slug] = [{
            "rank": it.get("rank_absolute"), "name": it.get("title"), "domain": it.get("domain"),
            "rating": (it.get("rating") or {}).get("value"),
            "reviews": (it.get("rating") or {}).get("votes_count"),
            "category": it.get("category"), "is_maidthis": is_maidthis(it),
        } for it in items[:10]]
        keywords[slug] = [{
            "keyword": r.get("keyword"), "volume": r.get("search_volume"),
            "cpc": r.get("cpc"), "competition": r.get("competition"),
        } for r in (sig["sv"].get(slug) or []) if isinstance(r, dict) and r.get("keyword")]

    json.dump({"generated": "2026-08-26", "weights": W,
               "weights_potential": W_POTENTIAL, "weights_headroom": W_HEADROOM,
               "markets": rows,
               "competitors": competitors, "keywords": keywords},
              open(os.path.join(ROOT, "app/data/markets.json"), "w"), indent=1)

    print("built %d markets (%d fully scored)" % (len(rows), len(scored)))
    for r in rows[:10]:
        print("  %-28s %5.1f  %-7s msv %5d  maps %s" %
              (r["market"], r["opportunity_score"], r["status"], r["total_msv"],
               r["maps_rank_general"]))


if __name__ == "__main__":
    build()
