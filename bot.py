import os
import requests
import time

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print(response.text)

def get_message():
    return """
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
💶 یورو اروپا:
💷 پوند انگلیس:
🇨🇳 یوان چین:
🇦🇪 درهم امارات:
🥇 اونس جهانی طلا:
🥇 طلای ۱۸ عیار:
🔶 بیت‌کوین (BTC):
🔷 اتریوم (ETH):

⏰ بروزرسانی هر ۴ ساعت
"""

print("Bot started")

while True:
    message = get_message()
    send_message(message)
    print("Message sent")
    time.sleep(14400)
