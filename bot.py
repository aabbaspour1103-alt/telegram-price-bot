import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "-1003901224506"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "✅ تست ارسال ربات انجام شد"
}

r = requests.post(url, data=data)
print(r.text)
