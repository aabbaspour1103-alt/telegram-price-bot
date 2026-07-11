import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")

CHANNEL_ID = "@CryptoBrew"

# دریافت قیمت‌ها از نوسان
url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"

response = requests.get(url)
data = response.json()

def price(name):
    try:
        return data[name]["value"]
    except:
        return "ناموجود"

message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {price("usd")}
💶 یورو اروپا: {price("eur")}
💷 پوند انگلیس: {price("gbp")}
🇨🇳 یوان چین: {price("cny")}
🇦🇪 درهم امارات: {price("aed")}
🇸🇦 ریال عربستان: {price("sar")}

🥇 اونس جهانی طلا: {price("ons")}
🥇 طلای ۱۸ عیار: {price("18ayar")}
🥇 طلای ۲۴ عیار: {price("24ayar")}

🔶 بیت‌کوین (BTC): {price("btc")}
🔷 اتریوم (ETH): {price("eth")}
🔸 سولانا (SOL): {price("sol")}
🔹 ریپل (XRP): {price("xrp")}
🔸 کاردانو (ADA): {price("ada")}
🔹 ترون (TRX): {price("trx")}

⏰ زمان بروزرسانی:
{datetime.now().strftime("%Y-%m-%d %H:%M")}

➖➖➖➖➖➖➖
@CryptoBrew
"""

telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

payload = {
    "chat_id": CHANNEL_ID,
    "text": message
}

send = requests.post(telegram_url, data=payload)

if send.json().get("ok"):
    print("Message sent successfully")
else:
    print(send.text)
