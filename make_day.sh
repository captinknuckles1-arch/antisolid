#!/bin/bash

DAY=$1

JSON="data/day_${DAY}.json"
OUT="output/antisolid_${DAY}.mp4"

if [ ! -f "$JSON" ]; then
  echo "ERROR: Missing $JSON"
  exit 1
fi

if [ ! -f "scripts/render.sh" ]; then
  echo "ERROR: scripts/render.sh not found"
  exit 1
fi

scripts/render.sh "$JSON" "$OUT"

echo "Rendered: $OUT"
