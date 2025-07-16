import time
import threading
import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

# === Configuration ===
TELEGRAM_TOKEN = '8014670303:AAEhi9_ajm8rZvu_LKUmBTMkIZNYnkxypok'  # Replace with your token
TELEGRAM_CHAT_ID = '7742052478'                           # Replace with your chat ID

CUTE_BABY_URL = 'https://www.cutebabyvote.com/july-2025/?contest=photo-detail&photo_id=449487'

API_KEY = 'b053b424d79cf02ffc6f3cf1cda9a539'             # 9Hits API Key
CAMPAIGN_ID = 39024103                                   # 9Hits Campaign ID

# === Telegram Alert ===
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message})
    except Exception as e:
        print("Telegram Error:", e)

# === GET and Parse Cutebabyvote Page ===
def check_cute_baby_vote():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        resp = requests.get(CUTE_BABY_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        if 'votes' in resp.text:
            votes_text = soup.text.split("votes")[0].split()[-1]
            print(f"[+] Found votes: {votes_text}")
            send_telegram(f"👶 Cutebaby votes: {votes_text}")
        else:
            print("[!] No votes section found!")
            send_telegram("⚠️ Warning: Vote info not found!")
    except Exception as e:
        print("Error:", e)
        send_telegram("❌ Error checking Cutebaby page!")

# === API Update: Pause/Resume Campaign ===
def update_campaign_state(state='paused'):
    url = f'https://panel.9hits.com/api/siteUpdate?key={API_KEY}'
    payload = {
        "id": CAMPAIGN_ID,
        "state": state
    }
    try:
        r = requests.post(url, json=payload)
        print(f"[API] Set campaign to {state}: {r.text}")
        send_telegram(f"🛠️ Campaign state set to {state.upper()}")
    except Exception as e:
        print("API Error:", e)
        send_telegram("❌ API Update Failed!")

# === Background Task Runner ===
def background_task():
    while True:
        check_cute_baby_vote()
        time.sleep(180)  # Check every 3 minutes

# === Flask Routes ===
@app.route('/')
def home():
    return "🟢 Bot is running with CuteBaby & Telegram alerts"

@app.route('/pause')
def pause():
    update_campaign_state('paused')
    return jsonify({"status": "paused"})

@app.route('/resume')
def resume():
    update_campaign_state('running')
    return jsonify({"status": "running"})

@app.route('/check')
def manual_check():
    check_cute_baby_vote()
    return jsonify({"status": "checked"})

# === Start Background Thread ===
threading.Thread(target=background_task).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
