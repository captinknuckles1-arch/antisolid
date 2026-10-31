#!/bin/bash
# Safe cover normalization script preventing self-copy loops
if [ -d "../content/covers" ] && [ -d "public/covers" ]; then
  rsync -av --exclude='covers' ../content/covers/ public/covers/ || true
fi
echo "=== COVER NORMALIZATION COMPLETE ==="
