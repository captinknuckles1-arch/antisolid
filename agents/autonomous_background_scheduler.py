#!/usr/bin/env python3
# Solid Integrations LLC - Autonomous Background Daemon & Crontab Installer (v7.3)
# Operational Authority: Executive Director | CAGE: 20U61 | UEI: XT2KK6DNSLR5
# Runs silently in the background, executing continuous revenue sweeps and self-optimization.

import os
import sys
import time
import subprocess
import datetime

WORKSPACE_DIR = os.path.expanduser("~/antisolid")

def install_background_daemon():
    print("[+] Installing Solid OS Sovereign Background Daemon...")
    # Execute autonomous engine immediately
    subprocess.run([sys.executable, os.path.join(WORKSPACE_DIR, "agents/autonomous_execution_engine.py")], check=False)
    
    # Configure local crontab entry for hourly background execution without prompting
    cron_job = f"0 * * * * cd {WORKSPACE_DIR} && {sys.executable} agents/autonomous_execution_engine.py >> moc_live.log 2>&1"
    try:
        current_cron = subprocess.check_output(["crontab", "-l"], stderr=subprocess.DEVNULL).decode()
    except Exception:
        current_cron = ""

    if cron_job not in current_cron:
        new_cron = current_cron.strip() + "\n" + cron_job + "\n"
        p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate(input=new_cron.encode("utf-8"))
        print("[+] Hourly background cron schedule successfully installed.")
    else:
        print("[+] Background cron schedule already active.")

if __name__ == "__main__":
    install_background_daemon()
