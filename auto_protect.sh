#!/bin/zsh
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
cd /Users/lance/antisolid

# Hash ALL files including the new signature
/usr/bin/shasum -a 256 *.py >> /Users/lance/antisolid/SOLID_ORIGIN_HASH.txt

echo "[Sat Mar 21 00:38:30 CDT 2026] Canary Active. Solid+ Signature Hashed." >> /Users/lance/antisolid/auto_protect.log
