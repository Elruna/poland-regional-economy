import requests, pandas as pd, time, os

BASE = "https://bdl.stat.gov.pl/api/v1"
HEADERS = {}
YEARS = list(range(2015, 2025))

VARS = {
    "wage_nominal": {"id": "64428",  "level": 2},
    "unemployment": {"id": "461690", "level": 2},
}

def get_var(var_id, level):
    rows, page = [], 0
    while page < 20:  
        r = requests.get(f"{BASE}/data/by-variable/{var_id}",
                         params={"unit-level": level, "format": "json",
                                 "page-size": 100, "page": page, "year": YEARS},
                         headers=HEADERS, timeout=30)
        r.raise_for_status()
        j = r.json()
        for u in j.get("results", []):
            for v in u.get("values", []):
                rows.append((u["id"], u["name"], int(v["year"]), v.get("val")))
        print("  page", page, "rows so far", len(rows), flush=True)
        if "next" not in j.get("links", {}):
            break
        page += 1
        time.sleep(1)
    return pd.DataFrame(rows, columns=["unit_id", "region", "year", "value"])

for name, cfg in VARS.items():
    path = f"data/{name}.csv"
    if os.path.exists(path):
        print(name, "already downloaded, skipping")
        continue
    print("Fetching", name, flush=True)
    df = get_var(cfg["id"], cfg["level"])
    df.to_csv(path, index=False)
    print(name, df.shape, df["year"].min(), df["year"].max())