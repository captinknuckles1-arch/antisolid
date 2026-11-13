#!/bin/bash
set -euo pipefail

echo "SOLID INTEGRATIONS: legacy invoice dispatcher is disabled."
echo "The previous script generated a local hash and a fabricated Stripe URL; it did not create a real Stripe checkout session or verify a receivable."
echo "No invoice was generated, no payment link was created, and no funds were requested."
echo "Use only an executed agreement, a verified amount due, and a tested payment processor workflow."
exit 2
