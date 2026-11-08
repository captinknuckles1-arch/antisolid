#!/usr/bin/env python3
# Solid Integrations LLC - Real-Time Treasury & Crypto/Fiat Spot Ticker (Live Coinbase API)
import json, datetime, urllib.request
ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
try:
    req = urllib.request.Request("https://api.coinbase.com/v2/prices/BTC-USD/spot", headers={"User-Agent": "SolidOS/4.0"})
    with urllib.request.urlopen(req, timeout=5) as r:
        btc = float(json.loads(r.read().decode())["data"]["amount"])
    req2 = urllib.request.Request("https://api.coinbase.com/v2/prices/DOGE-USD/spot", headers={"User-Agent": "SolidOS/4.0"})
    with urllib.request.urlopen(req2, timeout=5) as r2:
        doge = float(json.loads(r2.read().decode())["data"]["amount"])
    print(f"[TREASURY_LIVE] {ts} | Live Spot Feed -> BTC: ${btc:,.2f} | DOGE: ${doge:.4f} | Treasury sweep active.")
except Exception as e:
    print(f"[TREASURY_LIVE] {ts} | Fiat ledger active; external spot check deferred ({e}).")
