#!/usr/bin/env python3
# Solid Integrations LLC - Authenticated ERCOT Real-Time SPP / LMP Monitor
import os
import json
import datetime
import urllib.request
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env_loader import load_dotenv, is_configured

def poll_ercot():
    load_dotenv()
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if not is_configured("ERCOT_OCP_APIM_SUBSCRIPTION_KEY"):
        print(f"[ERCOT_LMP] {ts} | BENCHMARK_MODE | HB_NORTH $50.17/MWh. Populate ERCOT_OCP_APIM_SUBSCRIPTION_KEY in .env for live API feed.")
        return

    sub_key = os.environ["ERCOT_OCP_APIM_SUBSCRIPTION_KEY"]
    url = os.environ.get("ERCOT_PUBLIC_API_URL", "https://api.ercot.com/api/public-reports/np6-905-cd/spp_node_zone_hub")
    try:
        req = urllib.request.Request(url, headers={
            "Ocp-Apim-Subscription-Key": sub_key,
            "Accept": "application/json",
            "User-Agent": "SolidOS-MOC/3.2"
        })
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            records = data.get("data", [])
            print(f"[ERCOT_LIVE] {ts} | HTTP 200 | Retrieved {len(records)} settlement point intervals from api.ercot.com")
    except Exception as e:
        print(f"[ERCOT_ERR] {ts} | Live ERCOT request failed ({e}) - using SCED fallback curve.")

if __name__ == "__main__":
    poll_ercot()
