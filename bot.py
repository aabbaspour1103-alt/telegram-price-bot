import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

print("TOKEN:", TOKEN)

if not TOKEN:
    raise Exception("TOKEN is None. GitHub Secret تنظیم نشده است.")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "✅ ربات با موفقیت از GitHub Actions اجرا شد."
}

response = requests.post(url, data=data)

print(response.text)
