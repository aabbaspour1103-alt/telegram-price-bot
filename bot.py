import os
import requests
from datetime import datetime
import pytz
from persiantools.jdatetime import JalaliDateTime


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def get_prices():

    url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"

    data = requests.get(url).json()

    return {
        "usd": data["usd_sell"],
        "eur": data["eur_sell"],
        "gbp": data["gbp_sell"],
        "cny": data["cny_sell"],
        "aed": data["aed_sell"],
        "sar": data["sar_sell"],
        "gold18": data["18ayar"],
        "gold24": data["24ayar"],
        "ounce": data["ons"]
    }


def crypto_prices():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,solana,ripple,cardano,tron"
        "&vs_currencies=usd"
    )

    data = requests.get(url).json()

    return {
        "btc": data["bitcoin"]["usd"],
        "eth": data["ethereum"]["usd"],
        "sol": data["solana"]["usd"],
        "xrp": data["ripple"]["usd"],
        "ada": data["cardano"]["usd"],
        "trx": data["tron"]["usd"]
    }


def iran_time():

    iran = pytz.timezone("Asia/Tehran")

    now = datetime.now(iran)

    jalali = JalaliDateTime(now)

    return jalali.strftime("%Y/%m/%d  %H:%M")


def send_message(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }

    requests.post(url, data=payload)



def main():

    money = get_prices()
    crypto = crypto_prices()


    message = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {money['usd']} تومان

💶 یورو اروپا: {money['eur']} تومان

💷 پوند انگلیس: {money['gbp']} تومان

🇨🇳 یوان چین: {money['cny']} تومان

🇦🇪 درهم امارات: {money['aed']} تومان

🇸🇦 ریال عربستان: {money['sar']} تومان


🥇 اونس جهانی طلا: {money['ounce']} دلار

🥇 طلای ۱۸ عیار: {money['gold18']} تومان

🥇 طلای ۲۴ عیار: {money['gold24']} تومان


🔶 بیت‌کوین (BTC): ${crypto['btc']}

🔷 اتریوم (ETH): ${crypto['eth']}

🔸 سولانا (SOL): ${crypto['sol']}

🔹 ریپل (XRP): ${crypto['xrp']}

🔸 کاردانو (ADA): ${crypto['ada']}

🔹 ترون (TRX): ${crypto['trx']}


⏰ زمان بروزرسانی:
🇮🇷 {iran_time()}

➖➖➖➖➖➖➖
@CryptoBrew
"""


    send_message(message)



if name == "main":
    main()
