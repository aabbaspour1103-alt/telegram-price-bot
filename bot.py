import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL_ID,
        "text": text
    })

# دریافت قیمت‌ها از نوسان
url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"
data = requests.get(url).json()

usd = data["usd_sell"]["value"]
eur = data["eur"]["value"]
gbp = data["gbp"]["value"]
cny = data["cny"]["value"]

message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {usd} تومان
💶 یورو اروپا: {eur} تومان
💷 پوند انگلیس: {gbp} تومان
🇨🇳 یوان چین: {cny} تومان

⏰ بروزرسانی:
{datetime.now().strftime("%Y-%m-%d %H:%M")}
"""

send_message(message)

print("Message sent successfully")
