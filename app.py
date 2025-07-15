from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "CuteBaby Scraper Running..."

@app.route("/run")
def run_scraper():
    url = "https://www.cutebabyvote.com/july-2025/?contest=photo-detail&photo_id=449365"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html_output = response.text
        return f"<pre>{html_output}</pre>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
