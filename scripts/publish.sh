#!/bin/bash
set -e

SLUG=$1

if [ -z "$SLUG" ]; then
  echo "Usage: npm run publish -- <edition-slug>"
  exit 1
fi

git add .
git commit -m "Publish edition $SLUG"
git push
