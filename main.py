import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import threading
from flask import Flask

# === CONFIGURATION ===
API_KEY = 'b053b424d79cf02ffc6f3cf1cda9a539'
CAMPAIGN_ID = 39024103
CHECK_INTERVAL = 300  # 5 minutes

TELEGRAM_TOKEN = '8014670303:AAEhi9_ajm8rZvu_LKUmBTMkIZNYnkxypok'
TELEGRAM_CHAT_ID = '7742052478'

VOTE_URL = "https://www.cutebabyvote.com/july-2025/?contest=photo-detail&photo_id=449487"

last_status = None
app = Flask(__name__)

# === Send Telegram Message ===
def send_telegram(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        requests.post(telegram_url, data=payload, timeout=10)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

# === Update 9Hits Campaign State ===
def update_campaign_state(new_state):
    url = f'https://panel.9hits.com/api/siteUpdate?key={API_KEY}'
    payload = {
        "id": CAMPAIGN_ID,
        "userState": new_state
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"→ 9Hits API Triggered: userState = '{new_state}'")
        print(f"→ Status Code: {response.status_code}")
        print(f"→ Response: {response.text.strip()[:300]}\n")
        send_telegram(f"🔄 API Update: userState = '{new_state.upper()}' ✅")
    except Exception as e:
        print(f"❌ Error sending API request: {e}\n")
        send_telegram(f"❌ API request error: {e}")

# === Check Voting Page ===
def check_voting_status():
    global last_status
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(VOTE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        warning_div = soup.find("div", class_="pc-image-info-box-button-btn-text")
        warning_present = warning_div and "The voting button is temporarily disabled" in warning_div.text
        current_status = "found" if warning_present else "not found"

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Current Status: {current_status}")

        if last_status is None:
            print("🔁 First run detected.")
            new_state = 'paused' if current_status == "found" else 'running'
            update_campaign_state(new_state)
            send_telegram(f"🕵️ First check: Warning {current_status.upper()}")

        elif last_status != current_status:
            print("🔁 Status change detected.")
            new_state = 'paused' if current_status == "found" else 'running'
            update_campaign_state(new_state)
            send_telegram(f"🔄 Status changed: Warning {current_status.upper()}")
        else:
            print("✅ No change, no API request sent.\n")

        last_status = current_status

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error checking site: {e}\n")
        send_telegram(f"❌ Error checking site: {e}")

# === Flask Route for UptimeRobot ===
@app.route('/')
def home():
    return "🟢 Bot is running! Status OK."

# === Start the background voting checker ===
def start_monitor():
    print("🟢 Voting Monitor + 9Hits Controller + Telegram Started...\n")
    send_telegram("🚀 Bot started! Monitoring every 5 minutes.")
    while True:
        check_voting_status()
        time.sleep(CHECK_INTERVAL)

# === Start Threads ===
if __name__ == "__main__":
    threading.Thread(target=start_monitor).start()
    app.run(host="0.0.0.0", port=10000)
