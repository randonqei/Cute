import requests
import time

def fetch_html():
    url = "https://www.cutebabyvote.com/july-2025/?contest=photo-detail&photo_id=449365"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print("=== HTML Response Start ===\n")
        print(response.text)
        print("\n=== HTML Response End ===\n")
    except Exception as e:
        print(f"Error fetching: {e}")

# Run every 5 minutes
while True:
    fetch_html()
    time.sleep(300)  # 5 minutes
