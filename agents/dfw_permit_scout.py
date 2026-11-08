#!/usr/bin/env python3
# Solid Integrations LLC - Node 10: Dallas Commercial Permit Scout
# Operational Authority: MOC | CAGE: 20U61 | UEI: XT2KK6DNSLR5
# Source: City of Dallas Open Data (https://www.dallasopendata.com/resource/e7gq-4sah.json)

import os
import json
import urllib.request
import urllib.parse

def fetch_dallas_permits():
    # Query City of Dallas Socrata SODA endpoint
    # Target active commercial, industrial, electrical, and master permits with real addresses
    query_params = urllib.parse.urlencode({
        "$limit": 5,
        "$where": "street_address IS NOT NULL",
        "$order": ":id DESC"
    })
    url = f"https://www.dallasopendata.com/resource/e7gq-4sah.json?{query_params}"
    headers = {
        "User-Agent": "SolidIntegrations-MOC/5.1 (Lance T. Pullen; Dallas TX)",
        "Accept": "application/json"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            records = json.loads(resp.read().decode("utf-8"))
            if not records:
                print("City of Dallas Open Data returned 0 records for query.")
                return []

            parsed = []
            for r in records:
                addr = r.get("street_address", "Unknown Address").strip()
                zip_c = r.get("zip_code", "").strip()
                full_addr = f"{addr}, Dallas, TX {zip_c}".strip(", ")
                p_type = r.get("permit_type", "Commercial / Industrial Permit")
                desc = r.get("work_description", "General Construction").strip()
                p_num = r.get("permit_number", "N/A")
                date_str = r.get("issued_date", "")

                raw_val = r.get("value")
                if raw_val is not None and str(raw_val).strip() and str(raw_val) != "0":
                    try:
                        val_str = f"${float(raw_val):,.2f}"
                    except Exception:
                        val_str = f"${raw_val}"
                else:
                    raw_area = r.get("area")
                    if raw_area and str(raw_area) != "0":
                        val_str = f"Not Declared ({raw_area} sq ft)"
                    else:
                        val_str = "Not Declared on City Filing"

                parsed.append({
                    "address": full_addr,
                    "permit_type": p_type,
                    "description": desc,
                    "value": val_str,
                    "permit_number": p_num,
                    "date": date_str
                })

            # Save the live raw JSON for the daemon and web dashboard
            with open("dallas_permits_cache.json", "w", encoding="utf-8") as f:
                json.dump(parsed, f, indent=2)

            top = parsed[0]
            print(f"Scanned City of Dallas Open Data: {top['address']} | {top['permit_type']} | Value: {top['value']}")
            return parsed

    except Exception as e:
        print(f"City of Dallas permit feed check: {e}")
        return []

if __name__ == "__main__":
    fetch_dallas_permits()
