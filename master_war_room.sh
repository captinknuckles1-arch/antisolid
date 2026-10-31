#!/bin/bash

# Configuration
EVIDENCE_DIR="./privileged"
LEDGER="$EVIDENCE_DIR/evidence_ledger.txt"
LOG_FILE="infringements.json"

echo "[$(date)] Starting Agentic Sweep..."

# Phase 1: The Hunter (Patlytics API)
# We hit the 2026 'Scan' endpoint to check for our logic hashes in Starlink V3 firmware.
RESPONSE=$(curl -s -X POST "https://api.patlytics.ai/v2/infringement/scan" \
     -H "Authorization: Bearer $PATLYTICS_API_KEY" \
     -d "{\"target\": \"Starlink-V3\", \"logic_hash\": \"$CANARY_ID\"}")

echo $RESPONSE > $LOG_FILE

# Phase 2: Logic Check
# We use 'jq' to check if the agent found a high-confidence match.
MATCH=$(echo $RESPONSE | jq '.match_confidence // 0')

if [ "$MATCH" -gt 85 ]; then
    echo "!!! MATCH DETECTED ($MATCH%) !!!"
    
    # Phase 3: The Drafter (Harvey AI v2 API)
    echo "Instructing Harvey to draft $50M demand..."
    curl -s -X POST "https://api.harvey.ai/v2/completion" \
         -H "Authorization: Bearer $HARVEY_API_KEY" \
         -d '{
           "task": "Draft a formal Notice of Misappropriation citing new Starlink V3 firmware matches. Demand: $50M buyout + 15% royalty.",
           "context_file": "infringements.json",
           "compliance": ["TRAIGA-2026", "DTSA-Federal"]
         }' > demand_draft_$(date +%F).docx

    # Phase 4: The Lock (Hashing)
    # Lock the evidence immediately to ensure a court-ready chain of custody.
    chmod 600 $LEDGER
    shasum -a 256 $LOG_FILE >> $LEDGER
    chmod 400 $LEDGER
    echo "Evidence hashed and locked in $LEDGER."
else
    echo "No match found. Continuing surveillance."
fi

echo "[$(date)] Sweep complete."
