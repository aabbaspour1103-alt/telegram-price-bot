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
    requests.post(url, data=data)

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

while True:
    send_message(get_message())
    time.sleep(14400)
