import os
import requests
from datetime import datetime
import pytz
from persiantools.jdatetime import JalaliDateTime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def get_price():
    url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"
    response = requests.get(url)
    data = response.json()

    return {
        "usd": data.get("usd", {}).get("value", "-"),
        "eur": data.get("eur", {}).get("value", "-"),
        "gbp": data.get("gbp", {}).get("value", "-"),
        "cny": data.get("cny", {}).get("value", "-"),
        "aed": data.get("aed", {}).get("value", "-"),
        "sar": data.get("sar", {}).get("value", "-"),
        "gold": data.get("ounce", {}).get("value", "-"),
        "18": data.get("18ayar", {}).get("value", "-"),
        "24": data.get("24ayar", {}).get("value", "-"),
        "btc": data.get("btc", {}).get("value", "-"),
        "eth": data.get("eth", {}).get("value", "-"),
        "sol": data.get("sol", {}).get("value", "-"),
        "xrp": data.get("xrp", {}).get("value", "-"),
        "ada": data.get("ada", {}).get("value", "-"),
        "trx": data.get("trx", {}).get("value", "-")
    }


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }

    requests.post(url, data=payload)


def main():
    prices = get_price()

    iran_time = datetime.now(pytz.timezone("Asia/Tehran"))
    jalali_time = JalaliDateTime(iran_time).strftime("%Y/%m/%d - %H:%M")

    message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {prices['usd']}
💶 یورو اروپا: {prices['eur']}
💷 پوند انگلیس: {prices['gbp']}
🇨🇳 یوان چین: {prices['cny']}
🇦🇪 درهم امارات: {prices['aed']}
🇸🇦 ریال عربستان: {prices['sar']}

🥇 اونس جهانی طلا: {prices['gold']}
🥇 طلای ۱۸ عیار: {prices['18']}
🥇 طلای ۲۴ عیار: {prices['24']}

🔶 بیت‌کوین (BTC): {prices['btc']}
🔷 اتریوم (ETH): {prices['eth']}
🔸 سولانا (SOL): {prices['sol']}
🔹 ریپل (XRP): {prices['xrp']}
🔸 کاردانو (ADA): {prices['ada']}
🔹 ترون (TRX): {prices['trx']}

⏰ زمان بروزرسانی:
{jalali_time}

➖➖➖➖➖➖➖
@CryptoBrew
"""

    send_message(message)
    print("Message sent successfully")


if __name__ == "__main__":
    main()
