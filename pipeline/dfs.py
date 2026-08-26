"""DataForSEO client with a hard spend cap.

Budget rule for this project: never exceed BUDGET_USD across the whole run.
Every call is logged to raw/dfs_cost_log.jsonl and to the shared HQDM log.
"""
import base64, json, os, sys, time, urllib.request, urllib.error
try:
    import tomllib
except ImportError:
    import tomli as tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = r"C:/Users/User/Desktop/HQDM/Secrets/dataforseo.toml"
HQDM_LOG = r"C:/Users/User/Desktop/HQDM/Secrets/dataforseo_cost_log.jsonl"
LOCAL_LOG = os.path.join(ROOT, "raw", "dfs_cost_log.jsonl")
BUDGET_USD = 18.00   # hard cap, user authorised max $20

_cfg = tomllib.load(open(SECRETS, "rb"))["dataforseo"]
_AUTH = base64.b64encode(f"{_cfg['login']}:{_cfg['password']}".encode()).decode()


def spent():
    total = 0.0
    if os.path.exists(LOCAL_LOG):
        for line in open(LOCAL_LOG, encoding="utf-8"):
            try:
                total += json.loads(line).get("cost_usd", 0) or 0
            except Exception:
                pass
    return round(total, 6)


def _log(endpoint, cost, status, meta):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "project": "home-by-five", "endpoint": endpoint,
           "cost_usd": cost, "status": status, "meta": meta}
    for path in (LOCAL_LOG, HQDM_LOG):
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec) + "\n")
        except Exception:
            pass


def call(endpoint, payload, retries=2):
    """POST to a DataForSEO v3 endpoint. payload = list of task dicts."""
    already = spent()
    if already >= BUDGET_USD:
        raise SystemExit(f"BUDGET STOP: ${already:.2f} spent, cap ${BUDGET_USD:.2f}")
    url = f"https://api.dataforseo.com/v3/{endpoint}"
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Basic " + _AUTH, "Content-Type": "application/json"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read().decode())
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt == retries:
                _log(endpoint, 0.0, "error", {"error": str(exc)})
                raise
            time.sleep(3 * (attempt + 1))
    cost = data.get("cost", 0.0) or 0.0
    _log(endpoint, cost, data.get("status_message", "?"),
         {"tasks": len(payload), "run": round(already + cost, 4)})
    return data


def results(data):
    """Flatten task results, skipping failed tasks."""
    out = []
    for task in data.get("tasks") or []:
        if task.get("status_code") != 20000:
            out.append({"_error": task.get("status_message"), "_data": task.get("data")})
            continue
        for r in task.get("result") or []:
            out.append(r)
    return out


if __name__ == "__main__":
    print(f"spent so far on this project: ${spent():.4f} (cap ${BUDGET_USD})")
