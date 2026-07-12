import os
import asyncio
import requests
import jdatetime
from telegram import Bot
from bonbast import Bonbast


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)


def toman(value):
    try:
        return f"{int(value):,} تومان"
    except:
        return "نامشخص"


def get_currency():

    try:
        bon = Bonbast()

        data = bon.get_rates()

        return {
            "USD": data.get("usd1"),
            "EUR": data.get("eur1"),
            "GBP": data.get("gbp1"),
            "CNY": data.get("cny1"),
            "AED": data.get("aed1"),
            "SAR": data.get("sar1"),
        }

    except Exception as e:
        print("Bonbast Error:", e)

        return {}


def get_crypto():

    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum"
            "&vs_currencies=usd"
        )

        r = requests.get(url, timeout=10)
        data = r.json()

        return {
            "BTC": data["bitcoin"]["usd"],
            "ETH": data["ethereum"]["usd"]
        }

    except Exception as e:
        print("Crypto Error:", e)

        return {
            "BTC": None,
            "ETH": None
        }


def create_message():

    currency = get_currency()
    crypto = get_crypto()

    now = jdatetime.datetime.now().strftime(
        "%Y/%m/%d - %H:%M"
    )

    text = f"""
💰 <b>قیمت لحظه‌ای بازار</b>

💵 دلار آمریکا: {toman(currency.get('USD'))}

💶 یورو اروپا: {toman(currency.get('EUR'))}

💷 پوند انگلیس: {toman(currency.get('GBP'))}

🇨🇳 یوان چین: {toman(currency.get('CNY'))}

🇦🇪 درهم امارات: {toman(currency.get('AED'))}

🇸🇦 ریال عربستان: {toman(currency.get('SAR'))}


🔶 بیت‌کوین (BTC):
${crypto.get('BTC') or 'نامشخص'}

🔷 اتریوم (ETH):
${crypto.get('ETH') or 'نامشخص'}


🕒 بروزرسانی:
{now}
"""

    return text


async def send_post():

    text = create_message()

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        parse_mode="HTML"
    )


if __name__ == "__main__":
    asyncio.run(send_post())
