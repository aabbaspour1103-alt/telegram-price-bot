import os
import requests

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    response = requests.post(url, data=data, timeout=10)
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

message = get_message()
send_message(message)

print("Message sent successfully")
