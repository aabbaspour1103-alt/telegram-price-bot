import os
import asyncio
import requests
from datetime import datetime
import pytz
import jdatetime
from telegram import Bot


TOKEN = os.getenv("TOKEN")
CHANNEL_ID = "@CryptoBrew"
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY")


def safe_request(url):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        print("API:", e)
    return {}


def format_number(value, crypto=False):
    try:
        if value is None:
            return "نامشخص"

        num = float(value)

        if not crypto and num > 1000000:
            num /= 10

        if crypto:
            if num >= 1000:
                return f"{num:,.2f}"
            return f"{num:,.6f}".rstrip("0").rstrip(".")

        return f"{int(num):,}"

    except:
        return "نامشخص"



def get_value(data, keys):
    try:
        for k in keys:
            if k in data:
                item = data[k]

                if isinstance(item, dict):
                    return (
                        item.get("value")
                        or item.get("price")
                        or item.get("current")
                    )

                return item
    except:
        pass

    return None



def get_currency():

    data = safe_request(
        f"https://api.navasan.tech/latest/?api_key={NAVASAN_API_KEY}"
    )

    return {
        "usd": get_value(data, ["usd","usd_sell","dollar"]),
        "eur": get_value(data, ["eur","euro"]),
        "gbp": get_value(data, ["gbp","pound"]),
        "cny": get_value(data, ["cny","yuan"]),
        "aed": get_value(data, ["aed","dirham"]),
        "sar": get_value(data, ["sar"]),
        "try": get_value(data, ["try"]),
        "rub": get_value(data, ["rub"]),
        "cad": get_value(data, ["cad"]),
        "aud": get_value(data, ["aud"])
    }



def get_crypto():

    coins = {
        "BTC":"bitcoin",
        "ETH":"ethereum",
        "BNB":"binancecoin",
        "SOL":"solana",
        "XRP":"ripple",
        "TON":"the-open-network",
        "DOGE":"dogecoin",
        "ADA":"cardano",
        "AVAX":"avalanche-2",
        "DOT":"polkadot",
        "LTC":"litecoin",
        "SHIB":"shiba-inu"
    }

    result = {}

    try:

        ids = ",".join(coins.values())

        data = safe_request(
            "https://api.coingecko.com/api/v3/simple/price"
            f"?ids={ids}&vs_currencies=usd"
        )

        for name, key in coins.items():
            result[name] = data.get(key, {}).get("usd")

    except Exception as e:
        print("Crypto:", e)

    return result



def iran_time():

    try:
        tz = pytz.timezone("Asia/Tehran")
        now = datetime.now(tz)

        j = jdatetime.datetime.fromgregorian(
            datetime=now
        )

        return j.strftime("%Y/%m/%d - %H:%M")

    except:
        return "نامشخص"



def create_message():

    money = get_currency()
    crypto = get_crypto()

    return f"""
💰 قیـمت لحظه‌ای بازار

🥈 ارز :

💵 دلار آمریکـــــــا: {format_number(money.get('usd'))} تومان
💶 یــــورو اروپـــا: {format_number(money.get('eur'))} تومان
💷 پـــوند انگلیس: {format_number(money.get('gbp'))} تومان
🇨🇳 یــــوان چـــین: {format_number(money.get('cny'))} تومان
🇦🇪 درهــم امارات: {format_number(money.get('aed'))} تومان
🇸🇦 ریال عربستان: {format_number(money.get('sar'))} تومان
🇹🇷 لـــــیــــر ترکیه: {format_number(money.get('try'))} تومان
🇷🇺 روبـــل روسیه: {format_number(money.get('rub'))} تومان
🇨🇦 دلار کـــــــانادا: {format_number(money.get('cad'))} تومان
🇦🇺 دلار اســترالیا: {format_number(money.get('aud'))} تومان


🥇 ارز دیجیتال:

🔶 بیــــت‌کوین (BTC): {format_number(crypto.get('BTC'),True)} دلار
🔷 اتــــریــــــوم (ETH): {format_number(crypto.get('ETH'),True)} دلار
🔸 بایننس‌کوین (BNB): {format_number(crypto.get('BNB'),True)} دلار
🔹 ســــــــــولانا (SOL): {format_number(crypto.get('SOL'),True)} دلار
🔸 ریـــــــــــــپل (XRP): {format_number(crypto.get('XRP'),True)} دلار
🔹 تـــــون‌کوین (TON): {format_number(crypto.get('TON'),True)} دلار
🔸 دوج‌کـوین (DOGE): {format_number(crypto.get('DOGE'),True)} دلار
🔹 کـــاردانــــــو (ADA): {format_number(crypto.get('ADA'),True)} دلار
🔸 آوالانـــــــچ (AVAX): {format_number(crypto.get('AVAX'),True)} دلار
🔹 پولـــکـــادات (DOT): {format_number(crypto.get('DOT'),True)} دلار
🔸 لایــــــت‌کوین (LTC): {format_number(crypto.get('LTC'),True)} دلار
🔹 شیـــــبا اینو (SHIB): {format_number(crypto.get('SHIB'),True)} دلار


🕒 بــروزرسانــی: {iran_time()}

- @CryptoBrew
"""


async def main():

    try:
        bot = Bot(token=TOKEN)

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=create_message()
        )

    except Exception as e:
        print("Telegram Error:", e)



if __name__ == "__main__":
    asyncio.run(main())
