import time
import requests
import os
from datetime import datetime
import pytz

# === CONFIG ===
TARGET_URL = os.getenv("TARGET_URL", "https://soccer-scraper-g8jg.onrender.com")
PING_INTERVAL = 14 * 60  # 14 minutes between pings
TIMEZONE = pytz.timezone("America/Los_Angeles")  # adjust if needed
START_HOUR = 8   # 8 AM local time
END_HOUR = 23    # 11 PM local time

def ping():
    try:
        r = requests.get(TARGET_URL, timeout=10)
        print(f"[KEEPALIVE] ✅ Pinged {TARGET_URL} — status {r.status_code}")
    except Exception as e:
        print(f"[KEEPALIVE] ⚠️ Error pinging: {e}")

def within_active_hours():
    now = datetime.now(TIMEZONE)
    return START_HOUR <= now.hour < END_HOUR

if __name__ == "__main__":
    print("[KEEPALIVE] Worker started — keeping service alive between 8 AM and 11 PM PT.")
    while True:
        if within_active_hours():
            ping()
        else:
            print("[KEEPALIVE] 💤 Outside active hours — sleeping until next check.")
        time.sleep(PING_INTERVAL)

