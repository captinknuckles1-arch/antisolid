#!/bin/bash
TEXT="$1"
OUT="$2"

magick -size 1080x1920 xc:black \
-fill white -gravity center \
-font Impact -pointsize 120 \
-interline-spacing -20 \
-annotate +0+0 "$TEXT" \
"$OUT"
