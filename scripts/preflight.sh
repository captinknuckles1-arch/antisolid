#!/bin/bash
set -e

echo "✔ Git clean"
git diff --quiet

echo "✔ Editions present"
ls content/editions

echo "✔ Build passes"
npm run build

echo "✔ Ready for drop"
