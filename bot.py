import os
import requests
from datetime import datetime
import pytz
import jdatetime
import asyncio
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def format_number(value, decimals=False):
    try:
        num = float(value)

        if not decimals:
            return f"{int(num):,}"

        if num >= 1000:
            return f"{int(num):,}"

        return f"{num:,.6f}".rstrip("0").rstrip(".")

    except:
        return "نامشخص"


def get_value(data, keys):
    for key in keys:
        if key in data:
            item = data[key]

            if isinstance(item, dict):
                return (
                    item.get("value")
                    or item.get("price")
                    or item.get("current")
                )

            return item

    return None


def get_navasan():

    url = f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"

    try:
        data = requests.get(url, timeout=15).json()

        return {
            "usd": get_value(data, ["usd","usd_sell","dollar"]),
            "eur": get_value(data, ["eur","euro"]),
            "gbp": get_value(data, ["gbp","pound"]),
            "cny": get_value(data, ["cny","yuan"]),
            "aed": get_value(data, ["aed","dirham"]),
            "sar": get_value(data, ["sar"]),

            "gold18": get_value(
                data,
                ["gold18","gold_18","18k","gold_18k","geram18"]
            ),

            "gold24": get_value(
                data,
                ["gold24","gold_24","24k","gold_24k"]
            )
        }

    except:
        return {}


def get_crypto():

    ids = (
        "bitcoin,ethereum,binancecoin,"
        "solana,ripple,the-open-network,dogecoin"
    )

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd"
    )

    try:
        data = requests.get(url, timeout=15).json()

        return {
            "BTC": data.get("bitcoin", {}).get("usd"),
            "ETH": data.get("ethereum", {}).get("usd"),
            "BNB": data.get("binancecoin", {}).get("usd"),
            "SOL": data.get("solana", {}).get("usd"),
            "XRP": data.get("ripple", {}).get("usd"),
            "TON": data.get("the-open-network", {}).get("usd"),
            "DOGE": data.get("dogecoin", {}).get("usd")
        }

    except:
        return {}


def iran_time():

    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)

    jalali = jdatetime.datetime.fromgregorian(
        datetime=now
    )

    return jalali.strftime("%Y/%m/%d - %H:%M")


def create_message():

    money = get_navasan()
    crypto = get_crypto()

    return f"""
💰 قیمت لحظه‌ای بازار

🥈 ارز :

💵 دلار آمریکـــــــا: {format_number(money.get('usd'))} تومان
💶 یــــورو اروپـــا: {format_number(money.get('eur'))} تومان
💷 پـــوند انگلیس: {format_number(money.get('gbp'))} تومان
🇨🇳 یــــوان چـــین: {format_number(money.get('cny'))} تومان
🇦🇪 درهــم امارات: {format_number(money.get('aed'))} تومان
🇸🇦 ریال عربستان: {format_number(money.get('sar'))} تومان

🥇 طلا :

🥇 طلای ۱۸ عیار: {format_number(money.get('gold18'))} تومان
🥇 طلای ۲۴ عیار: {format_number(money.get('gold24'))} تومان

🥇 ارز دیجیتال:

🔶 بیــــت‌کوین (BTC): {format_number(crypto.get('BTC'),True)} دلار
🔷 اتــــریــــــوم (ETH): {format_number(crypto.get('ETH'),True)} دلار
🔸 بایننس‌کوین (BNB): {format_number(crypto.get('BNB'),True)} دلار
🔹 ســــــــــولانا (SOL): {format_number(crypto.get('SOL'),True)} دلار
🔸 ریـــــــــــــپل (XRP): {format_number(crypto.get('XRP'),True)} دلار
🔹 تـــــون‌کوین (TON): {format_number(crypto.get('TON'),True)} دلار
🔸 دوج‌کــــوین (DOGE): {format_number(crypto.get('DOGE'),True)} دلار

🕒 بــروزرسانــی: {iran_time()}

- @CryptoBrew
"""


async def main():

    bot = Bot(
        token=TOKEN
    )

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=create_message()
    )


if __name__ == "__main__":
    asyncio.run(main())
