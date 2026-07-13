import os
import requests
import datetime
import asyncio
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

bot = Bot(token=TOKEN)


def price_toman(x):
    try:
        return f"{int(x):,} تومان"
    except:
        return "نامشخص"


# TGJU
def get_tgju():

    url = "https://api.tgju.org/v1/data/sana/json"

    try:
        data = requests.get(url, timeout=10).json()

        dollar = data["data"]["sana"]["price"]

        return {
            "dollar": dollar
        }

    except Exception:
        return {
            "dollar": "نامشخص"
        }


# CoinGecko
def get_crypto():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,binancecoin,solana,ripple,the-open-network,dogecoin"
        "&vs_currencies=usd"
    )

    try:
        data = requests.get(url, timeout=10).json()

        return {
            "BTC": data["bitcoin"]["usd"],
            "ETH": data["ethereum"]["usd"],
            "BNB": data["binancecoin"]["usd"],
            "SOL": data["solana"]["usd"],
            "XRP": data["ripple"]["usd"],
            "TON": data["the-open-network"]["usd"],
            "DOGE": data["dogecoin"]["usd"],
        }

    except Exception:
        return {}


async def send():

    tgju = get_tgju()
    crypto = get_crypto()

    now = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )


    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا:
{price_toman(tgju['dollar'])}

🥇 طلا و ارز:
🥇 اونس جهانی طلا: دریافت از TGJU
🥇 طلای ۱۸ عیار: دریافت از TGJU
🥇 طلای ۲۴ عیار: دریافت از TGJU


🔶 ارز دیجیتال:

🔸 BTC: ${crypto.get('BTC','نامشخص')}
🔹 ETH: ${crypto.get('ETH','نامشخص')}
🟡 BNB: ${crypto.get('BNB','نامشخص')}
🟣 SOL: ${crypto.get('SOL','نامشخص')}
💧 XRP: ${crypto.get('XRP','نامشخص')}
🔵 TON: ${crypto.get('TON','نامشخص')}
🐶 DOGE: ${crypto.get('DOGE','نامشخص')}


🕒 بروزرسانی:
{now}
"""


    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )


asyncio.run(send())
