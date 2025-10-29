import time
import requests
import os

TARGET_URL = os.getenv("TARGET_URL", "https://soccer-scraper-g8jg.onrender.com")

def ping():
    try:
        r = requests.get(TARGET_URL, timeout=10)
        print(f"[KEEPALIVE] Pinged {TARGET_URL} — status {r.status_code}")
    except Exception as e:
        print(f"[KEEPALIVE] Error pinging: {e}")

if __name__ == "__main__":
    print("[KEEPALIVE] Worker started…")
    while True:
        ping()
        time.sleep(14 * 60)  # every 14 minutes

