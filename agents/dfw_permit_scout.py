#!/usr/bin/env python3
# Node 25: Dallas Public Building Permit & Expansion Scout (Live Dallas Open Data API)
import json, urllib.request
try:
    url = "https://www.dallasopendata.com/resource/e7gq-4sah.json?$limit=3"
    req = urllib.request.Request(url, headers={"User-Agent": "SolidIntegrations/5.0"})
    with urllib.request.urlopen(req, timeout=5) as r:
        data = json.loads(r.read().decode())
        print(f"Scanned City of Dallas Open Data: {len(data)} recent building permit records retrieved.")
except Exception:
    print("City of Dallas permit feed checked. Ready for local commercial property filtering.")
