#!/usr/bin/env python3
# Solid Integrations LLC - v5.1 Kinetic Neural Brain & Dallas Live Data Server
import os
import re
import sys
import json
import time
import sqlite3
import datetime
import threading
import subprocess
import urllib.request
from urllib.parse import urlparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from env_loader import load_dotenv, get_auth_summary, is_configured

HOST = "127.0.0.1"
PORT = 8787
LOG_BUFFER = []
ACTIVE_PULSES = []
STATE_LOCK = threading.Lock()

SWARM_NODES = [
    {"id": 0, "path": "agents/moc_controller.py", "name": "Central Brain", "group": "CORE", "desc": "Coordinates all 30 agents and routes tasks across your laptop and cloud."},
    {"id": 1, "path": "agents/enforcer_agent.py", "name": "The Enforcer", "group": "PROTECT", "desc": "Enforces your contracts, late payment rules, and the $4.2M IP recovery target."},
    {"id": 2, "path": "agents/invoice_collections_agent.py", "name": "Cash Collector", "group": "MONEY", "desc": "Tracks real money paid by clients and follows up on unpaid bills."},
    {"id": 3, "path": "agents/b2b_retainer_closer.py", "name": "Deal Closer", "group": "MONEY", "desc": "Packages monthly service plans for Dallas-Fort Worth industrial clients."},
    {"id": 4, "path": "agents/treasury_yield_tickler.py", "name": "Crypto & Cash Ticker", "group": "MONEY", "desc": "Pulls live Bitcoin & Dogecoin prices straight from Coinbase."},
    {"id": 5, "path": "agents/treasury_rate_watcher.py", "name": "U.S. Treasury Watcher", "group": "MONEY", "desc": "Pulls official U.S. government interest rates from Treasury.gov."},
    {"id": 6, "path": "agents/subcontract_arbitrage_agent.py", "name": "Contract Margin Finder", "group": "MONEY", "desc": "Finds profitable spread on federal subcontracts under CAGE 20U61."},
    {"id": 7, "path": "agents/forfeiture_auction_sniper.py", "name": "Auction Sniper", "group": "MONEY", "desc": "Checks government surplus auctions (GSA) for cheap trucks and shop gear."},
    {"id": 8, "path": "agents/grant_sbirs_harvester.py", "name": "Free Grant Finder", "group": "MONEY", "desc": "Looks for Department of Energy grants that do not require giving up ownership."},
    {"id": 9, "path": "agents/tax_shield_optimizer.py", "name": "Lance's Tax Shield", "group": "PROTECT", "desc": "Tracks equipment write-offs and intellectual property tax rules."},
    {"id": 10, "path": "agents/dfw_permit_scout.py", "name": "Dallas Permit Scout", "group": "MONEY", "desc": "Pulls real street addresses and declared values from City of Dallas Open Data."},
    {"id": 11, "path": "agents/texas_business_verifier.py", "name": "Texas Business Checker", "group": "PROTECT", "desc": "Checks the Texas state business registry to verify local companies."},
    {"id": 12, "path": "agents/patent_trademark_watchdog.py", "name": "IP & Brand Watchdog", "group": "PROTECT", "desc": "Protects Solid Integrations names, code, and ownership paperwork."},
    {"id": 13, "path": "agents/equipment_resale_pricer.py", "name": "Shop & Auto Pricer", "group": "OPS", "desc": "Checks resale values on exotic cars, engines, and shop equipment."},
    {"id": 14, "path": "agents/client_onboarding_concierge.py", "name": "Client Welcome Desk", "group": "MONEY", "desc": "Prepares W-9 forms, company info, and invoice links for new buyers."},
    {"id": 15, "path": "agents/legal_brokerage_agent.py", "name": "Contract Writer", "group": "PROTECT", "desc": "Drafts plain-English service agreements and non-disclosure forms."},
    {"id": 16, "path": "agents/dfw_lead_scraper.py", "name": "Industrial Lead Finder", "group": "MONEY", "desc": "Maps out 42 industrial districts across Dallas-Fort Worth."},
    {"id": 17, "path": "agents/sam_gov_monitor.py", "name": "Federal Contract Radar", "group": "MONEY", "desc": "Connects to SAM.gov using your UEI (XT2KK6DNSLR5) to find federal work."},
    {"id": 18, "path": "agents/ercot_arbitrage.py", "name": "Texas Power Monitor", "group": "OPS", "desc": "Watches Texas electricity prices to spot cheap charging and high selling times."},
    {"id": 19, "path": "agents/grid_arbitrage_vanguard.py", "name": "Battery Trader", "group": "OPS", "desc": "Signals when to charge batteries (low price) and sell power back (high price)."},
    {"id": 20, "path": "agents/federal_compliance_sentinel.py", "name": "DOE Meeting Prep", "group": "PROTECT", "desc": "Keeps notes ready for your Department of Energy call with Kent Hibben."},
    {"id": 21, "path": "agents/outlook_comms.py", "name": "Email Watcher", "group": "OPS", "desc": "Watches solid.lp@outlook.com for client messages and meeting links."},
    {"id": 22, "path": "agents/can_bus_fleet.py", "name": "Auto & Fleet Tech", "group": "OPS", "desc": "Stores diagnostic and custom build plans (Suburban, Maserati Ghibli)."},
    {"id": 23, "path": "agents/synthetic_supply_agent.py", "name": "Parts & Steel Buyer", "group": "OPS", "desc": "Tracks prices on raw steel, welding supplies, and car parts."},
    {"id": 24, "path": "agents/inventory_tracker.py", "name": "Tool & Shop Tracker", "group": "OPS", "desc": "Keeps a list of your physical shop tools and hardware inventory."},
    {"id": 25, "path": "agents/neural_marketing_swarm.py", "name": "Video & Brand Maker", "group": "MONEY", "desc": "Creates brutalist green-and-black promotional videos and graphics."},
    {"id": 26, "path": "agents/agent_firewall.py", "name": "Security Bouncer", "group": "PROTECT", "desc": "Checks incoming files and blocks suspicious traffic."},
    {"id": 27, "path": "agents/quantum_defense_agent.py", "name": "Password & Key Guard", "group": "PROTECT", "desc": "Locks your .env secret keys and checks file safety."},
    {"id": 28, "path": "agents/gcp_provisioner.py", "name": "Cloud Helper", "group": "OPS", "desc": "Prepares backup cloud computers so your MacBook Air doesn't overheat."},
    {"id": 29, "path": "agents/voice_handler.py", "name": "Voice Assistant", "group": "OPS", "desc": "Lets you trigger actions with simple everyday commands."}
]

EXEC_COUNTS = {n["path"]: 0 for n in SWARM_NODES}
LAST_OUTPUT = {n["path"]: "Ready and waiting." for n in SWARM_NODES}

LIVE_EXTERNAL = {
    "btc_usd": None,
    "doge_usd": None,
    "treasury_rate": "Checking...",
    "last_updated": "Just now"
}

ERCOT_24H_REFERENCE = [
    {"hour": "12 AM", "price": 24.50, "zone": "North Texas (Dallas)", "note": "Overnight wind power is high; electricity is cheap. Best time to CHARGE batteries."},
    {"hour": "2 AM",  "price": 21.80, "zone": "North Texas (Dallas)", "note": "Lowest demand of the night. Ideal window to fill battery banks at rock-bottom cost."},
    {"hour": "4 AM",  "price": 23.10, "zone": "North Texas (Dallas)", "note": "Pre-dawn cheap power window."},
    {"hour": "6 AM",  "price": 34.60, "zone": "North Texas (Dallas)", "note": "Morning wake-up ramp as homes and factories turn on."},
    {"hour": "8 AM",  "price": 42.20, "zone": "North Texas (Dallas)", "note": "Commercial buildings open across DFW; hold battery charge."},
    {"hour": "10 AM", "price": 38.90, "zone": "North Texas (Dallas)", "note": "West Texas solar farms kick in, keeping midday prices moderate."},
    {"hour": "12 PM", "price": 44.50, "zone": "North Texas (Dallas)", "note": "Noon air-conditioning and industrial load building."},
    {"hour": "2 PM",  "price": 50.17, "zone": "North Texas (Dallas)", "note": "Afternoon heat builds; approaching profitable sell threshold ($55/MWh)."},
    {"hour": "4 PM",  "price": 68.40, "zone": "North Texas (Dallas)", "note": "High afternoon demand! Price is above $55 — SELL stored battery power to the grid."},
    {"hour": "6 PM",  "price": 94.20, "zone": "North Texas (Dallas)", "note": "PEAK PROFIT WINDOW: Solar drops off while everyone is home. Maximum payout for selling power."},
    {"hour": "8 PM",  "price": 62.10, "zone": "North Texas (Dallas)", "note": "Evening demand still above $55; finish discharging batteries for profit."},
    {"hour": "10 PM", "price": 33.40, "zone": "North Texas (Dallas)", "note": "Grid cools down for the night; switch back to standby."}
]

def record_log(agent_name, text):
    ts = datetime.datetime.now().strftime("%I:%M:%S %p")
    with STATE_LOCK:
        LOG_BUFFER.insert(0, {"ts": ts, "agent": agent_name, "text": text})
        if len(LOG_BUFFER) > 60:
            LOG_BUFFER.pop()

def refresh_external_apis():
    load_dotenv()
    try:
        r1 = urllib.request.urlopen(urllib.request.Request("https://api.coinbase.com/v2/prices/BTC-USD/spot", headers={"User-Agent": "SolidOS/5.1"}), timeout=4)
        LIVE_EXTERNAL["btc_usd"] = float(json.loads(r1.read().decode())["data"]["amount"])
        r2 = urllib.request.urlopen(urllib.request.Request("https://api.coinbase.com/v2/prices/DOGE-USD/spot", headers={"User-Agent": "SolidOS/5.1"}), timeout=4)
        LIVE_EXTERNAL["doge_usd"] = float(json.loads(r2.read().decode())["data"]["amount"])
    except Exception:
        pass

    try:
        u = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates?page[size]=1&sort=-record_date"
        rt = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "SolidOS/5.1"}), timeout=4)
        row = json.loads(rt.read().decode()).get("data", [{}])[0]
        LIVE_EXTERNAL["treasury_rate"] = f"{row.get('avg_interest_rate_amt', 'N/A')}% ({row.get('security_desc', 'Treasury')})"
    except Exception:
        pass

    LIVE_EXTERNAL["last_updated"] = datetime.datetime.now().strftime("%I:%M:%S %p")

def get_cached_dallas_permits():
    cache_file = "dallas_permits_cache.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def get_laptop_health():
    batt = "Unknown"
    source = "AC Power"
    try:
        out = subprocess.check_output(["pmset", "-g", "batt"], stderr=subprocess.DEVNULL).decode()
        source = "Running on Battery" if "Battery Power" in out else "Plugged into Wall"
        m = re.search(r"(\d+)%", out)
        if m:
            batt = f"{m.group(1)}%"
    except Exception:
        pass
    return {"battery": batt, "source": source}

def get_money_facts():
    conn = sqlite3.connect("solid_revenue_ledger.db")
    cur = conn.cursor()
    cur.execute("SELECT stream_id, stream_name, target_annual_budget, verified_collected_cash, verified_open_invoices FROM revenue_streams")
    streams = cur.fetchall()
    conn.close()

    total_target = sum(s[2] for s in streams)
    total_collected = sum(s[3] for s in streams)
    total_invoiced = sum(s[4] for s in streams)

    sec_per_year = 365.25 * 86400.0
    target_per_sec = total_target / sec_per_year

    return {
        "stated_valuation_goal": 14500000.00,
        "stated_annual_target": total_target,
        "stated_ip_recovery_goal": 4200000.00,
        "verified_cash_collected": total_collected,
        "verified_open_invoices": total_invoiced,
        "target_per_second": target_per_sec,
        "streams": [
            {"id": s[0], "name": s[1], "target": s[2], "collected": s[3], "invoiced": s[4]}
            for s in streams
        ]
    }

def fire_agent(node):
    path = node["path"]
    if not os.path.exists(path):
        return False, "Agent file not found."
    try:
        out = subprocess.check_output([sys.executable, path], stderr=subprocess.STDOUT, timeout=7).decode().strip()
        clean = out.splitlines()[-1] if out else f"{node['name']} finished check."
        clean = re.sub(r"^\[[^\]]+\]\s*\S*\s*\|\s*", "", clean)
        EXEC_COUNTS[path] = EXEC_COUNTS.get(path, 0) + 1
        LAST_OUTPUT[path] = clean
        with STATE_LOCK:
            ACTIVE_PULSES.append({"from": 0, "to": node["id"], "ts": time.time(), "label": node["name"]})
            if len(ACTIVE_PULSES) > 25:
                ACTIVE_PULSES.pop(0)
        record_log(node["name"], clean)
        return True, clean
    except Exception as e:
        return False, str(e)

def background_brain_loop():
    refresh_external_apis()
    idx = 1
    while True:
        node = SWARM_NODES[idx % len(SWARM_NODES)]
        fire_agent(node)
        if idx % 6 == 0:
            refresh_external_apis()
        idx += 1
        time.sleep(2.5)

class BrainServer(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _json(self, obj, code=200):
        b = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/api/state":
            money = get_money_facts()
            laptop = get_laptop_health()
            auth = get_auth_summary()
            permits = get_cached_dallas_permits()
            nodes_out = []
            for n in SWARM_NODES:
                nodes_out.append({
                    "id": n["id"],
                    "path": n["path"],
                    "name": n["name"],
                    "group": n["group"],
                    "desc": n["desc"],
                    "runs": EXEC_COUNTS.get(n["path"], 0),
                    "last_output": LAST_OUTPUT.get(n["path"], "Ready.")
                })
            with STATE_LOCK:
                logs_copy = list(LOG_BUFFER)
                pulses_copy = [x for x in ACTIVE_PULSES if time.time() - x["ts"] < 4.0]
            return self._json({
                "money": money,
                "external": LIVE_EXTERNAL,
                "dallas_permits": permits,
                "ercot_curve": ERCOT_24H_REFERENCE,
                "laptop": laptop,
                "auth": auth,
                "nodes": nodes_out,
                "pulses": pulses_copy,
                "logs": logs_copy
            })
        if p.path == "/" or p.path == "/index.html":
            self.path = "/moc_telemetry_dashboard.html"
        return super().do_GET()

    def do_POST(self):
        p = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length).decode("utf-8")) if length > 0 else {}

        if p.path == "/api/fire_node":
            node_id = int(body.get("id", 0))
            for n in SWARM_NODES:
                if n["id"] == node_id:
                    ok, msg = fire_agent(n)
                    return self._json({"ok": ok, "name": n["name"], "output": msg})
            return self._json({"ok": False, "output": "Agent not found"}, 404)

        if p.path == "/api/log_real_money":
            amt = float(body.get("amount", 0))
            div = body.get("division", "DFW_INDUSTRIAL")
            kind = body.get("kind", "payment")
            desc = body.get("desc", "Logged by Lance")
            now_str = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
            conn = sqlite3.connect("solid_revenue_ledger.db")
            cur = conn.cursor()
            if kind == "payment":
                cur.execute("UPDATE revenue_streams SET verified_collected_cash = verified_collected_cash + ? WHERE stream_id = ?", (amt, div))
                cur.execute("INSERT INTO real_payments_log (timestamp_utc, division, description, amount_usd) VALUES (?, ?, ?, ?)", (now_str, div, desc, amt))
                record_log("Cash Ledger", f"Logged real payment of ${amt:,.2f} in {div}.")
            else:
                cur.execute("UPDATE revenue_streams SET verified_open_invoices = verified_open_invoices + ? WHERE stream_id = ?", (amt, div))
                record_log("Invoice Ledger", f"Added open invoice of ${amt:,.2f} to {div}.")
            conn.commit()
            conn.close()
            return self._json({"ok": True})

        return self._json({"ok": False}, 404)

if __name__ == "__main__":
    t = threading.Thread(target=background_brain_loop, daemon=True)
    t.start()
    srv = HTTPServer((HOST, PORT), BrainServer)
    print(f"[+] Solid Integrations v5.1 Kinetic Brain Server running on http://{HOST}:{PORT}")
    srv.serve_forever()
