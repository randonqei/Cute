from flask import Flask
import requests
from bs4 import BeautifulSoup

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

        html = response.text

        # Parse with BeautifulSoup to find vote count
        soup = BeautifulSoup(html, "html.parser")
        
        # Try to extract the text where the vote count appears
        # This depends on structure, example assumes it's inside something like <strong>123 Votes</strong>
        vote_text = soup.find(string=lambda text: text and "Vote" in text)
        
        if vote_text:
            print(f"[LOG] Found vote text: {vote_text.strip()}")
            return f"<b>Current vote text:</b> {vote_text.strip()}<br><br><pre>{html}</pre>"
        else:
            print("[LOG] Vote text not found")
            return "Vote count not found.<br><br><pre>{}</pre>".format(html)

    except Exception as e:
        print(f"[ERROR] {e}")
        return f"Error occurred: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
