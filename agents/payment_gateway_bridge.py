#!/usr/bin/env python3
# Solid Integrations LLC - Secure Payment Gateway & Ledger Bridge (v7.0)
# Operational Authority: Executive Director | CAGE: 20U61 | UEI: XT2KK6DNSLR5
# Connects webhook callbacks & checkout events to solid_revenue_ledger.db

import os
import sys
import json
import sqlite3
import datetime
import hashlib
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_PATH = "solid_revenue_ledger.db"

def init_payment_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS gateway_transactions (
        txn_id TEXT PRIMARY KEY,
        timestamp_utc TEXT,
        gateway TEXT,
        amount_usd REAL,
        customer_email TEXT,
        division TEXT,
        status TEXT,
        raw_payload TEXT
    )
    """)
    conn.commit()
    conn.close()

def record_gateway_payment(txn_id, gateway, amount, email, division, raw_json):
    init_payment_tables()
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        # 1. Log transaction
        cur.execute(
            "INSERT OR REPLACE INTO gateway_transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (txn_id, now_utc, gateway, amount, email, division, "SETTLED", raw_json)
        )
        # 2. Automatically credit settled cash in SQLite revenue ledger
        cur.execute(
            "UPDATE revenue_streams SET verified_collected_cash = verified_collected_cash + ?, updated_utc = ? WHERE stream_id = ?",
            (amount, now_utc, division)
        )
        # 3. Log into system notifications for real-time dashboard toast pop-up
        cur.execute(
            "INSERT INTO system_notifications (timestamp_utc, severity, title, message) VALUES (?, ?, ?, ?)",
            (now_utc, "SUCCESS", f"Automated Payment Received ({gateway})", f"Cleared ${amount:,.2f} from {email} into {division}.")
        )
        conn.commit()
        print(f"[GATEWAY_BRIDGE] SUCCESS: Logged ${amount:,.2f} transaction {txn_id} from {email} into {division}.")
        return True
    except Exception as e:
        print(f"[GATEWAY_BRIDGE] ERROR: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        
        try:
            payload = json.loads(raw_body)
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        # Determine gateway type (Stripe vs PayPal webhook schema)
        gateway = self.headers.get("X-Gateway-Type", "stripe").lower()
        
        if gateway == "stripe":
            # Handle Stripe checkout.session.completed event
            event_type = payload.get("type", "")
            if event_type == "checkout.session.completed":
                obj = payload.get("data", {}).get("object", {})
                txn_id = obj.get("id", f"stripe_{int(time.time())}")
                amount = float(obj.get("amount_total", 0)) / 100.0  # Stripe amounts are in cents
                email = obj.get("customer_details", {}).get("email", "client@solidintegrations.org")
                metadata = obj.get("metadata", {})
                division = metadata.get("division", "DFW_INDUSTRIAL")
                
                success = record_gateway_payment(txn_id, "Stripe", amount, email, division, raw_body)
                if success:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status": "recorded"}')
                    return
        elif gateway == "paypal":
            # Handle PayPal PAYMENT.CAPTURE.COMPLETED event
            event_type = payload.get("event_type", "")
            if "COMPLETED" in event_type:
                resource = payload.get("resource", {})
                txn_id = resource.get("id", f"paypal_{int(time.time())}")
                amount_obj = resource.get("amount", {})
                amount = float(amount_obj.get("value", 0.0))
                payer = resource.get("payer", {}).get("email_address", "client@solidintegrations.org")
                division = resource.get("custom_id", "DFW_INDUSTRIAL")
                
                success = record_gateway_payment(txn_id, "PayPal", amount, payer, division, raw_body)
                if success:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status": "recorded"}')
                    return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status": "ignored_event"}')

if __name__ == "__main__":
    init_payment_tables()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test hook execution
        record_gateway_payment("test_txn_999", "Stripe", 12500.00, "lancept@live.com", "DFW_INDUSTRIAL", '{"test": true}')
    else:
        print("[+] Payment Gateway Bridge initialized. Ready for Stripe/PayPal webhooks.")
