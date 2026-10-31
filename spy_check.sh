#!/zsh
# SOVEREIGN SHIELD: EXFILTRATION AUDIT
echo "SEARCHING FOR FOREIGN HEARTBEATS (CHINA/RUSSIA/GREY-MARKET)..."

# Check for established connections to known high-risk IP blocks
netstat -ant | grep -E "(.cn|.ru|.su)" > ~/antisolid/foreign_connections.txt

# Check for hidden background processes using high CPU (Scrapers/Miners)
ps -eo pcpu,pmem,comm | sort -k 1 -r | head -10 > ~/antisolid/resource_hogs.txt

echo "AUDIT COMPLETE. Check ~/antisolid/ for findings."
if [ -s ~/antisolid/foreign_connections.txt ]; then
    echo "WARNING: ACTIVE CONNECTIONS TO FOREIGN DOMAINS DETECTED."
else
    echo "CLEAN: No direct foreign heartbeats found."
fi
