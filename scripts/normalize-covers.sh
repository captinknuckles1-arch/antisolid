#!/bin/bash
# Completely safe cover normalization script
echo "=== NORMALIZING COVERS ==="
if [ -d "../content/covers" ] && [ "$(realpath ../content/covers)" != "$(realpath public/covers)" ]; then
  cp -rn ../content/covers/* public/covers/ 2>/dev/null || true
fi
echo "=== COVER NORMALIZATION COMPLETE ==="
