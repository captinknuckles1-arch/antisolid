#!/bin/bash

JSON=$1
OUT=$2

if [ ! -f "$JSON" ]; then
  echo "ERROR: JSON file not found: $JSON"
  exit 1
fi

STATEMENT=$(jq -r .statement "$JSON")
WORKOUT=$(jq -r '.workout[]' "$JSON" | sed ':a;N;$!ba;s/\n/\\n/g')
CLOSE=$(jq -r .close "$JSON")

ffmpeg -y -loop 1 -i assets/character.png \
-filter_complex "
scale=1080:1920,
zoompan=z='min(zoom+0.0008,1.04)':d=660,
drawtext=text='$STATEMENT':fontfile=assets/font.ttf:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=120:enable='between(t,0,3)',
drawtext=text='$WORKOUT':fontfile=assets/font.ttf:fontsize=52:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,3,18)',
drawtext=text='$CLOSE':fontfile=assets/font.ttf:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h-200:enable='between(t,18,22)'
" -t 22 -r 30 -pix_fmt yuv420p "$OUT"
