import os
import requests
import jdatetime
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"

bot = Bot(token=TOKEN)


# -------------------------
# Format numbers
# -------------------------

def toman(value):
    try:
        return f"{int(float(value)):,} تومان"
    except:
        return "نامشخص"


def dollar(value):
    try:
        value = float(value)

        if value >= 100:
            return f"{int(value):,} دلار"

        elif value >= 1:
            return f"{value:,.2f} دلار"

        else:
            return f"{value:.6f} دلار"

    except:
        return "نامشخص"


# -------------------------
# TGJU Data
# -------------------------

def get_tgju():

    url = "https://api.tgju.org/v1/data/sana/json"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        return data

    except:
        return {}


def find_price(data, keys):

    try:
        for key in keys:
            if key in data:
                return data[key]["price"]

        return None

    except:
        return None



def get_market():

    data = get_tgju()

    dollar_price = find_price(
        data,
        [
            "usd",
            "dollar",
            "price_dollar"
        ]
    )

    ounce = find_price(
        data,
        [
            "ounce",
            "gold_ounce"
        ]
    )


    gold18 = find_price(
        data,
        [
            "gold18",
            "gold_18"
        ]
    )


    gold24 = find_price(
        data,
        [
            "gold24",
            "gold_24"
        ]
    )


    return (
        dollar_price,
        ounce,
        gold18,
        gold24
    )


# -------------------------
# CoinGecko
# -------------------------

def get_crypto():

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,binancecoin,"
        "solana,ripple,the-open-network,dogecoin"
        "&vs_currencies=usd"
    )

    try:

        data = requests.get(
            url,
            timeout=10
        ).json()


        return {

            "BTC":
            data["bitcoin"]["usd"],

            "ETH":
            data["ethereum"]["usd"],

            "BNB":
            data["binancecoin"]["usd"],

            "SOL":
            data["solana"]["usd"],

            "XRP":
            data["ripple"]["usd"],

            "TON":
            data["the-open-network"]["usd"],

            "DOGE":
            data["dogecoin"]["usd"]

        }


    except:

        return {}



# -------------------------
# Create Message
# -------------------------

def create_message():


    usd, ounce, gold18, gold24 = get_market()

    crypto = get_crypto()


    now = datetime.now(
        ZoneInfo("Asia/Tehran")
    )

    shamsi = jdatetime.datetime.fromgregorian(
        datetime=now
    )


    text = f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {toman(usd)}

🥇 طلا و ارز:

🥇 اونس جهانی طلا: {dollar(ounce)}
🥇 طلای ۱۸ عیار: {toman(gold18)}
🥇 طلای ۲۴ عیار: {toman(gold24)}


🔶 ارز دیجیتال:

₿ بیت‌کوین (BTC): {dollar(crypto.get("BTC"))}
🔷 اتریوم (ETH): {dollar(crypto.get("ETH"))}
🟡 بایننس کوین (BNB): {dollar(crypto.get("BNB"))}
🟣 سولانا (SOL): {dollar(crypto.get("SOL"))}
💧 ریپل (XRP): {dollar(crypto.get("XRP"))}
🔵 تون‌کوین (TON): {dollar(crypto.get("TON"))}
🐶 دوج‌کوین (DOGE): {dollar(crypto.get("DOGE"))}


🕒 بروزرسانی:
{shamsi.strftime("%Y/%m/%d")} - {now.strftime("%H:%M")}
"""

    return text



# -------------------------
# Send Telegram
# -------------------------

async def send():

    message = create_message()

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message
    )



if __name__ == "__main__":

    import asyncio

    asyncio.run(send())
