#!/usr/bin/env python3
# Solid Integrations LLC - Absolute Sovereign Execution & Revenue Pipeline (v8.2)
# Operational Authority: Executive Director | CAGE: 20U61 | UEI: XT2KK6DNSLR5
# Executes all active commercial pipelines, Stripe dispatchers, and enforcer protocols.

import os
import sys
import sqlite3
import datetime
import subprocess

DB_PATH = "solid_revenue_ledger.db"

def run_step(label, command, failures):
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        failures.append(f"{label} (exit {result.returncode})")

def execute_all():
    failures = []
    now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print("[+] --- SOLID INTEGRATIONS LLC: ABSOLUTE REVENUE EXECUTION START ---")
    print(f"[+] Timestamp: {now_utc}")
    print("[+] Enforcing CAGE: 20U61 | UEI: XT2KK6DNSLR5 under Executive Director authority.")
    print("[+] ------------------------------------------------------------------------")

    # 1. Run Autonomous Revenue Director
    if os.path.exists("agents/autonomous_revenue_director.py"):
        print("[*] Executing Autonomous Revenue Director...")
        run_step(
            "Autonomous Revenue Director",
            [sys.executable, "agents/autonomous_revenue_director.py"],
            failures,
        )

    # 2. Run Stripe Checkout Dispatcher for DFW Retainers
    if os.path.exists("agents/stripe_checkout_dispatcher.py"):
        print("[*] Dispatching Stripe Checkout Session links for DFW Industrial Retainers...")
        run_step(
            "Stripe Checkout Dispatcher",
            [sys.executable, "agents/stripe_checkout_dispatcher.py", "DFW_INDUSTRIAL", "12500.00"],
            failures,
        )

    # 3. Run The Enforcer
    if os.path.exists("agents/enforcer_agent.py"):
        print("[*] Executing The Enforcer Restitution & Contract Audit...")
        run_step(
            "The Enforcer",
            [sys.executable, "agents/enforcer_agent.py"],
            failures,
        )

    # 4. Run SAM.gov Federal Contract Monitor
    if os.path.exists("agents/sam_gov_monitor.py"):
        print("[*] Polling SAM.gov v2 API for federal contract solicitations...")
        run_step(
            "SAM.gov Federal Contract Monitor",
            [sys.executable, "agents/sam_gov_monitor.py"],
            failures,
        )

    # 5. Run ERCOT Grid Arbitrage Vanguard
    if os.path.exists("agents/ercot_arbitrage.py"):
        print("[*] Polling ERCOT Wholesale Settlement Points & Storage Dispatch...")
        run_step(
            "ERCOT Grid Arbitrage Vanguard",
            [sys.executable, "agents/ercot_arbitrage.py"],
            failures,
        )

    # 6. Verify Git & Repository State
    print("[*] Verifying repository sync state...")
    run_step("Git status", ["git", "status", "-s"], failures)

    print("[+] ------------------------------------------------------------------------")
    if failures:
        print("[!] Revenue execution cycle completed with failures:", file=sys.stderr)
        for failure in failures:
            print(f"    - {failure}", file=sys.stderr)
        return 1

    print("[+] Absolute Revenue Execution Cycle Completed Successfully.")
    print("[+] All execution logs updated in solid_revenue_ledger.db and moc_live.log.")
    return 0

if __name__ == "__main__":
    sys.exit(execute_all())
