#!/usr/bin/env bash
set -e

ROOT="$(pwd)"
EDITIONS=$(find "$ROOT/content" -type d -path "*editions/violent-*")

echo "Found editions:"
echo "$EDITIONS"
echo

for ED in $EDITIONS; do
  NAME=$(basename "$ED")
  DEST="$ROOT/content/covers/$NAME"

  mkdir -p "$DEST"

  find "$ED" -type f \( -iname "*.jpg" -o -iname "*.png" \) -print -exec cp -n {} "$DEST/" \;

  echo "✔ Normalized covers for $NAME"
done

rm -rf "$ROOT/public/covers"
ln -s ../content/covers "$ROOT/public/covers"

echo
echo "Public covers wired:"
ls "$ROOT/public/covers"
