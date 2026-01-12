#!/bin/bash
set -e

EDITION=$1
SRC="gdrive:Antisolid/Editions/$EDITION"
DST="content/editions/$EDITION"

mkdir -p "$DST"
rclone copy "$SRC" "$DST"
