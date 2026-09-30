import requests, sys
BASE = "https://bdl.stat.gov.pl/api/v1"
HEADERS = {}  

term = sys.argv[1]
r = requests.get(f"{BASE}/variables/search",
                 params={"name": term, "format": "json", "page-size": 30},
                 headers=HEADERS)
r.raise_for_status()
for v in r.json().get("results", []):
    print(v["id"], "|", v.get("n1"), "|", v.get("n2"), "|", v.get("measureUnitName"), "|", v.get("level"))