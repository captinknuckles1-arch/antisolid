#!/usr/bin/env python3
# Solid Integrations LLC - Authenticated SAM.gov Opportunities Monitor
import os
import json
import datetime
import urllib.request
import urllib.parse
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env_loader import load_dotenv, is_configured

def poll_sam_gov():
    load_dotenv()
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    uei = os.environ.get("SOLID_ENTITY_UEI", "XT2KK6DNSLR5")
    cage = os.environ.get("SOLID_ENTITY_CAGE", "20U61")

    if not is_configured("SAM_GOV_API_KEY"):
        print(f"[SAM_GOV] {ts} | STANDBY_AUTH | UEI {uei} (CAGE {cage}) ready. Populate SAM_GOV_API_KEY in .env for live federal solicitation pulls.")
        return

    api_key = os.environ["SAM_GOV_API_KEY"]
    now = datetime.datetime.now(datetime.timezone.utc)
    posted_from = (now - datetime.timedelta(days=30)).strftime("%m/%d/%Y")
    posted_to = now.strftime("%m/%d/%Y")
    params = urllib.parse.urlencode({
        "api_key": api_key,
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "limit": 3,
        "ptype": "o,p,k"
    })
    url = f"https://api.sam.gov/opportunities/v2/search?{params}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "SolidOS-MOC/3.2"})
        with urllib.request.urlopen(req, timeout=6) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            total = payload.get("totalRecords", 0)
            opps = payload.get("opportunitiesData", [])
            top_title = opps[0].get("title", "N/A")[:55] if opps else "No recent matches"
            print(f"[SAM_GOV_LIVE] {ts} | HTTP 200 | {total} active federal solicitations | Top: {top_title}")
    except Exception as e:
        print(f"[SAM_GOV_ERR] {ts} | Live API call failed ({e}) - holding local cache.")

if __name__ == "__main__":
    poll_sam_gov()
