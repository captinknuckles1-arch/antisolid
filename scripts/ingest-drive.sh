#!/bin/bash
set -e

EDITION=$1
SRC='gdrive:Solid MAG/Editions/'"$EDITION"
DST="content/editions/$EDITION"

if ! rclone lsf "$SRC" >/dev/null 2>&1; then
  echo "Drive folder not found: $SRC"
  exit 1
fi

mkdir -p "$DST"
rclone copy "$SRC" "$DST"
