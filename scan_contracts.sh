#!/bin/bash
# ======================================================================
# SOLID INTEGRATIONS LLC - ENTERPRISE CONTRACT & OPPORTUNITY SCANNER
# CAGE: 20U61 | UEI: XT2KK6DNSLR5
# ======================================================================

echo "=========================================================="
echo "=== INITIALIZING ENTERPRISE CONTRACT PROCUREMENT SCAN ==="
echo "=========================================================="
echo "Target Entity  : Solid Integrations LLC"
echo "Identifiers    : CAGE: 20U61 | UEI: XT2KK6DNSLR5"
echo "Jurisdiction   : Texas, USA / Federal"
echo "----------------------------------------------------------"

# Query SAM.gov Public API endpoint for active infrastructure & defense tech notices
echo "[*] Querying SAM.gov Public Opportunity Feed..."
curl -s "https://api.sam.gov/opportunities/v2/search?limit=5&ptype=o,p,k&q=telemetry,energy,fabrication" \
  -H "accept: application/json" | grep -o '"title":[^}]*' | head -n 5 || echo "API rate limit or connection optimized."

echo ""
echo "----------------------------------------------------------"
echo "[*] Target Sectors Locked:"
echo "    1. Federal Defense/Tech (U.S. Tech Force / War Force tracks)"
echo "    2. North Texas Energy Grid & Substation Telemetry Bids"
echo "    3. State Infrastructure & Smart Transit Engineering"
echo "----------------------------------------------------------"
echo "ACTION: Use './dispatch_invoice.sh [Client] [Tier] [Amount]' to "
echo "        close enterprise contracts upon award execution."
echo "=========================================================="
