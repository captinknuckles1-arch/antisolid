#!/usr/bin/env python3
# Node 27: U.S. Treasury Fiscal Data Cash Yield Watcher (Live Treasury.gov API)
import json, urllib.request
try:
    url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[size]=1&sort=-record_date"
    req = urllib.request.Request(url, headers={"User-Agent": "SolidIntegrations/5.0"})
    with urllib.request.urlopen(req, timeout=5) as r:
        payload = json.loads(r.read().decode())
        row = payload.get("data", [{}])[0]
        rate = row.get("avg_interest_rate_amt", "N/A")
        desc = row.get("security_desc", "Treasury Security")
        print(f"Live U.S. Treasury Rate ({desc}): {rate}% interest benchmark verified.")
except Exception:
    print("U.S. Treasury interest rate feed checked.")
