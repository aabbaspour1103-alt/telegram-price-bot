import os
import requests
from datetime import datetime


TOKEN = os.getenv("TOKEN")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")
CHANNEL_ID = "@CryptoBrew"


def get_prices():

    url = f"https://api.navasan.tech/api/"

    headers = {
        "Api-Key": NAVASAN_API_KEY
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    try:
        dollar = data["usd"]["value"]
        euro = data["eur"]["value"]
        pound = data["gbp"]["value"]
        yuan = data["cny"]["value"]
        aed = data["aed"]["value"]
        sar = data["sar"]["value"]

        gold = data["ons"]["value"]
        gold18 = data["gold_18"]["value"]
        gold24 = data["gold_24"]["value"]

        btc = data["btc"]["value"]
        eth = data["eth"]["value"]
        sol = data["sol"]["value"]
        xrp = data["xrp"]["value"]
        ada = data["ada"]["value"]
        trx = data["trx"]["value"]

    except Exception:
        return "خطا در دریافت اطلاعات بازار"

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {dollar}
💶 یورو اروپا: {euro}
💷 پوند انگلیس: {pound}
🇨🇳 یوان چین: {yuan}
🇦🇪 درهم امارات: {aed}
🇸🇦 ریال عربستان: {sar}

🥇 اونس جهانی طلا: {gold}
🥇 طلای ۱۸ عیار: {gold18}
🥇 طلای ۲۴ عیار: {gold24}

🔶 بیت‌کوین (BTC): {btc}
🔷 اتریوم (ETH): {eth}
🔸 سولانا (SOL): {sol}
🔹 ریپل (XRP): {xrp}
🔸 کاردانو (ADA): {ada}
🔹 ترون (TRX): {trx}

⏰ زمان بروزرسانی: {now}

➖➖➖➖➖➖➖
@CryptoBrew
"""

    return message


def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL_ID,
        "text": text
    }

    response = requests.post(url, data=data)

    print(response.text)


if __name__ == "__main__":

    print("Bot started")

    message = get_prices()

    send_message(message)

    print("Message sent successfully")
