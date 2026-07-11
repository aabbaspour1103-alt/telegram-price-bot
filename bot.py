import os
import requests
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def get_navasan_prices():
    try:
        url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"
        response = requests.get(url, timeout=20)
        return response.json()
    except Exception as e:
        print("Navasan Error:", e)
        return {}


def get_price(data, keys):
    for key in keys:
        if key in data:
            try:
                return data[key]["value"]
            except:
                return data[key]
    return "ناموجود"


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }

    response = requests.post(url, data=payload, timeout=20)
    print(response.text)


prices = get_navasan_prices()


message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {get_price(prices, ['usd','dollar'])} تومان
💶 یورو اروپا: {get_price(prices, ['eur','euro'])} تومان
💷 پوند انگلیس: {get_price(prices, ['gbp','pound'])} تومان
🇨🇳 یوان چین: {get_price(prices, ['cny','yuan'])} تومان
🇦🇪 درهم امارات: {get_price(prices, ['aed','dirham'])} تومان
🇸🇦 ریال عربستان: {get_price(prices, ['sar','riyal'])} تومان

🥇 اونس جهانی طلا: {get_price(prices, ['ons','gold'])} دلار
🥇 طلای ۱۸ عیار: {get_price(prices, ['18ayar','gold18'])} تومان
🥇 طلای ۲۴ عیار: {get_price(prices, ['24ayar','gold24'])} تومان

🔶 بیت‌کوین (BTC): {get_price(prices, ['btc','bitcoin'])} دلار
🔷 اتریوم (ETH): {get_price(prices, ['eth','ethereum'])} دلار
🔸 سولانا (SOL): {get_price(prices, ['sol','solana'])} دلار
🔹 ریپل (XRP): {get_price(prices, ['xrp','ripple'])} دلار
🔸 کاردانو (ADA): {get_price(prices, ['ada','cardano'])} دلار
🔹 ترون (TRX): {get_price(prices, ['trx','tron'])} دلار

⏰ زمان بروزرسانی:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

➖➖➖➖➖➖➖
@CryptoBrew
"""


send_message(message)
print("Message sent successfully")
