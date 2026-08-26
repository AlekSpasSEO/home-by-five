"""Pull public search-market signals for every MaidThis market.

DataForSEO live endpoints accept ONE task per POST, so each market is its own call.
Results are appended to raw/market_signals.jsonl as they arrive, so an interrupted
run never loses paid calls and a re-run only fetches what is missing.

Measured cost per call, 2026-08-26:
  keywords_data/google_ads/search_volume/live  $0.090
  serp/google/maps/live/advanced               $0.002
  serp/google/organic/live/advanced            $0.0035
"""
import json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
from markets import KEYWORDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
codes = json.load(open(os.path.join(ROOT, "raw/location_codes.json")))
JSONL = os.path.join(ROOT, "raw/market_signals.jsonl")
MAPS_KWS = ["house cleaning service", "airbnb cleaning service"]
ORG_KW = "house cleaning services"
_lock = threading.Lock()


def done_keys():
    seen = set()
    if os.path.exists(JSONL):
        for line in open(JSONL, encoding="utf-8"):
            try:
                r = json.loads(line)
                p = r.get("payload")
                if isinstance(p, dict) and p.get("_error"):
                    continue
                # a search_volume payload is only complete when it holds every keyword row
                if r["kind"] == "sv" and not (isinstance(p, list) and len(p) >= 5):
                    continue
                seen.add((r["kind"], r["key"]))
            except Exception:
                pass
    return seen


def write(kind, key, payload):
    with _lock, open(JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"kind": kind, "key": key, "payload": payload}) + "\n")


def one(endpoint, payload, whole_result=False):
    d = dfs.call(endpoint, [payload])
    t = (d.get("tasks") or [{}])[0]
    if t.get("status_code") != 20000:
        return {"_error": t.get("status_message")}
    res = t.get("result") or []
    if whole_result:
        # search_volume returns one row per keyword, so keep the whole list
        return res
    return (res or [{}])[0] or {}


def run():
    seen = done_keys()
    jobs = []
    for s in codes:
        if ("sv", s) not in seen:
            jobs.append(("sv", s, "keywords_data/google_ads/search_volume/live",
                         {"keywords": KEYWORDS, "location_code": codes[s]["ads_code"],
                          "language_code": "en", "search_partners": False}))
        for kw in MAPS_KWS:
            if ("maps", f"{s}||{kw}") not in seen:
                jobs.append(("maps", f"{s}||{kw}", "serp/google/maps/live/advanced",
                             {"keyword": kw, "location_code": codes[s]["serp_code"],
                              "language_code": "en", "depth": 20}))
        if ("org", s) not in seen:
            jobs.append(("org", s, "serp/google/organic/live/advanced",
                         {"keyword": f"{ORG_KW} {codes[s]['city'].lower()}",
                          "location_code": codes[s]["serp_code"], "language_code": "en",
                          "device": "desktop", "depth": 20}))
    print(f"{len(jobs)} calls queued, already have {len(seen)}", flush=True)

    def work(job):
        kind, key, ep, payload = job
        try:
            res = one(ep, payload, whole_result=(kind == "sv"))
        except Exception as exc:
            res = {"_error": str(exc)}
        if kind == "maps":
            res = {"items": res.get("items") or [], "_error": res.get("_error")}
        elif kind == "org":
            res = {"item_types": res.get("item_types"),
                   "se_results_count": res.get("se_results_count"),
                   "items": res.get("items") or [], "_error": res.get("_error")}
        write(kind, key, res)
        return kind, key

    # search_volume is rate limited to 12 calls/min, so it runs throttled and serial
    sv_jobs = [j for j in jobs if j[0] == "sv"]
    other = [j for j in jobs if j[0] != "sv"]
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i, _ in enumerate(pool.map(work, other), 1):
            if i % 20 == 0:
                print(f"  serp {i}/{len(other)}  spend ${dfs.spent():.3f}", flush=True)
    for i, j in enumerate(sv_jobs, 1):
        work(j)
        print(f"  sv {i}/{len(sv_jobs)}  spend ${dfs.spent():.3f}", flush=True)
        if i < len(sv_jobs):
            time.sleep(0.5)
    print("total project spend: $%.4f" % dfs.spent(), flush=True)


if __name__ == "__main__":
    run()
