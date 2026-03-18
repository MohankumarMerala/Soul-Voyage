
import time
import urllib.request
import os
import logging

logger = logging.getLogger(__name__)

def start_pinger():
    """Pings own health endpoint every 10 minutes to prevent sleep."""
    time.sleep(30)  # wait for server to fully start

    # Get URL from environment or hardcode your Render URL
    url = os.environ.get("SITE_URL", "https://soul-voyage.onrender.com")
    ping_url = url.rstrip("/") + "/health/"

    print(f"[keepalive] Pinging {ping_url} every 10 minutes.")

    while True:
        try:
            req = urllib.request.Request(
                ping_url,
                headers={"User-Agent": "SoulVoyage-Keepalive/1.0"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                print(f"[keepalive] Ping OK - {resp.status}")
        except Exception as e:
            print(f"[keepalive] Ping failed: {e}")
        time.sleep(600)  # 10 minutes
