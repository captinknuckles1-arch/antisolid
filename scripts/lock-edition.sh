#!/bin/bash
set -e

SLUG=$1
META="content/editions/$SLUG/meta.json"

node -e "
const fs = require('fs');
const meta = JSON.parse(fs.readFileSync('$META'));
meta.archived = true;
fs.writeFileSync('$META', JSON.stringify(meta, null, 2));
"
