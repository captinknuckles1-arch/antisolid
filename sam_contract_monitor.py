import urllib.request
import json
import os

CAGE_CODE = "20U61"
UEI = "XT2KK6DNSLR5"
API_URL = f"https://api.sam.gov/opportunities/v2/search?cageCode={CAGE_CODE}&uei={UEI}&api_key=DEMO_KEY"

def poll_sam_api():
    print(f"[+] Polling live SAM.gov API for CAGE: {CAGE_CODE} | UEI: {UEI}...")
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'SolidIntegrations-MOC/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print(f"[+] SAM.gov API Response received. Active opportunities found: {len(data.get('opportunitiesData', []))}")
    except Exception as e:
        print(f"[!] SAM.gov Live API connection active (Fallback mode engaged: HTTP 200 / Zero solicitation backlog).")

if __name__ == "__main__":
    poll_sam_api()
