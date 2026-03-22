import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1485360254467313785/vmwhDZNp3PkWG1-BhEwHkdEl0XhNdbheLqDObUY9g54v-iOVLHUFDI54IJmFKVohUSyl"
THRESHOLD = 100000

URL = "https://idleclanshub.vercel.app/market"

def send_discord(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def check_market():
    API_KEY = "demo"
    scraper_url = f"http://api.scraperapi.com?api_key={API_KEY}&url={URL}&render=true"

    r = requests.get(scraper_url)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.find_all("tr")

    alerts = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue

        item = cols[0].text.strip()
        total = cols[5].text.strip().replace(",", "")

        if total.isdigit():
            total_val = int(total)

            if total_val > THRESHOLD:
                alerts.append(f"{item} → {total_val}")

    if alerts:
        send_discord("🔥 TOTAL > 100000:\n" + "\n".join(alerts))

if __name__ == "__main__":
    check_market()
