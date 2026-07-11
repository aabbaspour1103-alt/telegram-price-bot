import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "✅ تست ربات موفق بود"
}

response = requests.post(url, data=data)

print(response.text)
