#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

PILLARS = {
    "tech": {
        "title": "Why Modern AI Crashes Legacy Infrastructure",
        "hook": "Your company wants to plug an LLM straight into production. Here is why that is an operational disaster waiting to happen.",
        "body": "When an API talks to power grids, municipal transit, or SCADA systems, every single packet must be deterministic. If an AI agent hallucinates an output by 0.1 percent, relays trip, switches lock down, and systems fail. You cannot connect stochastic AI to legacy infrastructure without a deterministic logic firewall.",
        "cta": "Build deterministic infrastructure that does not break at solid-integrations.polsia.io. Link in bio.",
        "tags": ["#systemsengineering", "#infrastructure", "#scada", "#devops", "#techtok"]
    },
    "comedy": {
        "title": "When the Client Demands AI in Excel",
        "hook": "Tell me you work in enterprise IT without telling me you work in enterprise IT.",
        "body": "The client wants autonomous AI agents deployed before Q4. You ask to inspect their tech stack and discover their entire billing engine is an Excel spreadsheet from 2011 running on an OptiPlex under Kevin's desk. Kevin retired in March. The root password is taped to the mousepad.",
        "cta": "Fix your real architecture at solid-integrations.polsia.io before Kevin's PC dies.",
        "tags": ["#techhumor", "#programming", "#developer", "#sysadmin", "#softwareengineer"]
    },
    "action": {
        "title": "The 14-Second Power Grid Failure",
        "hook": "This single desynchronized API call almost took down 40 percent of the regional grid.",
        "body": "At 2:14 AM, automated generation telemetry slipped out of frequency tolerance. In under 14 seconds, 1,200 megawatts tripped offline. Legacy relays fought modern battery storage algorithms because neither had a unified deterministic logic layer.",
        "cta": "See how mission-critical networks protect their data pathways at solid-integrations.polsia.io.",
        "tags": ["#engineeringdisasters", "#cybersecurity", "#powergrid", "#techfail"]
    }
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pillar", choices=["tech", "comedy", "action"], default="tech")
    parser.add_argument("--topic", default="Infrastructure Resilience")
    parser.add_argument("--output", default="./drafts/")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    template = PILLARS.get(args.pillar, PILLARS["tech"])

    date_str = datetime.now().strftime("%Y-%m-%d")
    out_filename = os.path.join(args.output, f"{date_str}_{args.pillar}.json")

    data = {
        "date": date_str,
        "pillar": args.pillar,
        "topic": args.topic,
        "title": template["title"],
        "full_text": f"{template['hook']} {template['body']} {template['cta']}",
        "tags": template["tags"],
        "website": "https://solid-integrations.polsia.io/"
    }

    with open(out_filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[✓] Script generated successfully: {out_filename}")

if __name__ == "__main__":
    main()
