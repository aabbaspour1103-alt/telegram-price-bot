import os
import requests
import jdatetime
import asyncio
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def toman(value):
    try:
        return f"{int(float(value)):,} تومان"
    except:
        return "نامشخص"


def get_navasan():

    url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"

    try:
        response = requests.get(url, timeout=15)
        data = response.json()

        return {
            "usd": data.get("usd_sell"),
            "eur": data.get("eur_sell"),
            "gbp": data.get("gbp_sell"),
            "aed": data.get("aed_sell"),
            "gold18": data.get("18ayar"),
            "gold24": data.get("24ayar"),
            "ounce": data.get("ounce")
        }

    except Exception as e:
        print("Navasan Error:", e)
        return {}


def get_crypto():

    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum"
            "&vs_currencies=usd"
        )

        response = requests.get(url, timeout=15)
        data = response.json()

        return {
            "btc": data["bitcoin"]["usd"],
            "eth": data["ethereum"]["usd"]
        }

    except Exception as e:
        print("CoinGecko Error:", e)
        return {
            "btc": 0,
            "eth": 0
        }


def create_message():

    currency = get_navasan()
    crypto = get_crypto()

    now = jdatetime.datetime.now().strftime("%Y/%m/%d - %H:%M")

    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {toman(currency.get('usd'))}

💶 یورو اروپا: {toman(currency.get('eur'))}

💷 پوند انگلیس: {toman(currency.get('gbp'))}

🇨🇳 یوان چین: نامشخص

🇦🇪 درهم امارات: {toman(currency.get('aed'))}

🇸🇦 ریال عربستان: نامشخص

🥇 اونس جهانی طلا: {toman(currency.get('ounce'))}

🥇 طلای ۱۸ عیار: {toman(currency.get('gold18'))}

🥇 طلای ۲۴ عیار: {toman(currency.get('gold24'))}

🔶 بیت‌کوین (BTC): ${crypto.get('btc'):,}

🔷 اتریوم (ETH): ${crypto.get('eth'):,}


🕒 آخرین بروزرسانی:
{now}
"""

    return text


async def send_message():

    message = create_message()

    async with Bot(token=TOKEN) as bot:

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=message
        )


if __name__ == "__main__":
    asyncio.run(send_message())
