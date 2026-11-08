#!/usr/bin/env python3
# Solid Integrations LLC - Automated Invoice Dispatch & Accounts Receivable Collector
import sqlite3, datetime
ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
conn = sqlite3.connect("solid_revenue_ledger.db")
cur = conn.cursor()
cur.execute("SELECT SUM(pending_receivables), SUM(settled_ytd) FROM revenue_streams")
pending, settled = cur.fetchone()
conn.close()
print(f"[COLLECTIONS] {ts} | Settled Cash YTD: ${settled:,.2f} | Actively collecting ${pending:,.2f} in open invoices.")
