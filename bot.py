import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"  # در صورت نیاز نام یا شناسه عددی کانال را قرار بده

print("TOKEN:", TOKEN)

if not TOKEN:
    raise Exception("TOKEN is None. GitHub Secret تنظیم نشده است.")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHANNEL_ID,
    "text": "✅ تست موفق! ربات با GitHub Actions اجرا شد."
}

response = requests.post(url, data=data)

print("Status Code:", response.status_code)
print(response.text)
