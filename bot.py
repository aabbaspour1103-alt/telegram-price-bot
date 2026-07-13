import os
import requests
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
from datetime import datetime
import pytz
from khayyam import JalaliDatetime


TOKEN = os.getenv("TOKEN")
CHANNEL = "@CryptoBrew"


def format_number(value):
    try:
        value = float(str(value).replace(",", ""))

        if value >= 1000:
            return f"{int(value):,}"

        if value < 1:
            return f"{value:.6f}".rstrip("0").rstrip(".")

        return f"{value:,.2f}".rstrip("0").rstrip(".")

    except:
        return "نامشخص"


def get_tgju_prices():

    url = "https://www.tgju.org"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    result = {
        "dollar": "نامشخص",
        "euro": "نامشخص",
        "pound": "نامشخص",
        "yuan": "نامشخص",
        "dirham": "نامشخص",
        "riyal": "نامشخص",
        "ounce": "نامشخص",
        "gold18": "نامشخص",
        "gold24": "نامشخص"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        ids = {
            "dollar": "price_dollar_rl",
            "euro": "price_eur",
            "pound": "price_gbp",
            "yuan": "price_cny",
            "dirham": "price_aed",
            "riyal": "price_sar",
            "ounce": "ounce",
            "gold18": "geram18",
            "gold24": "geram24"
        }

        for key, item_id in ids.items():

            item = soup.find(
                id=item_id
            )

            if item:
                result[key] = item.text.strip()

    except Exception:
        pass

    return result



def get_crypto():

    coins = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "SOL": "solana",
        "XRP": "ripple",
        "TON": "the-open-network",
        "DOGE": "dogecoin"
    }

    result = {}

    try:

        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids="
            + ",".join(coins.values())
            + "&vs_currencies=usd"
        )

        data = requests.get(
            url,
            timeout=20
        ).json()

        for symbol, coin in coins.items():

            result[symbol] = format_number(
                data[coin]["usd"]
            )

    except Exception:

        for symbol in coins:
            result[symbol] = "نامشخص"

    return result



def create_message():

    market = get_tgju_prices()
    crypto = get_crypto()

    tehran = pytz.timezone(
        "Asia/Tehran"
    )

    now = datetime.now(
        tehran
    )

    date = JalaliDatetime(
        now
    ).strftime("%Y/%m/%d")

    time = now.strftime(
        "%H:%M"
    )


    return f"""
💰 قیمت لحظه‌ای بازار

💵 دلار آمریکا: {format_number(market['dollar'])} تومان
💶 یورو اروپا: {format_number(market['euro'])} تومان
💷 پوند انگلیس: {format_number(market['pound'])} تومان
🇨🇳 یوان چین: {format_number(market['yuan'])} تومان
🇦🇪 درهم امارات: {format_number(market['dirham'])} تومان
🇸🇦 ریال عربستان: {format_number(market['riyal'])} تومان

🥇 طلا و ارز:

🥇 اونس جهانی طلا: {format_number(market['ounce'])} دلار
🥇 طلای ۱۸ عیار: {format_number(market['gold18'])} تومان
🥇 طلای ۲۴ عیار: {format_number(market['gold24'])} تومان

🔶 ارز دیجیتال:

₿ بیت‌کوین (BTC): {crypto['BTC']} دلار
🔷 اتریوم (ETH): {crypto['ETH']} دلار
🟡 بایننس کوین (BNB): {crypto['BNB']} دلار
🟣 سولانا (SOL): {crypto['SOL']} دلار
💧 ریپل (XRP): {crypto['XRP']} دلار
🔵 تون‌کوین (TON): {crypto['TON']} دلار
🐶 دوج‌کوین (DOGE): {crypto['DOGE']} دلار

🕒 بروزرسانی:
{date} - {time}

- @CryptoBrew
"""


async def send_message():

    bot = Bot(
        token=TOKEN
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=create_message()
    )


if __name__ == "__main__":

    asyncio.run(
        send_message()
    )
